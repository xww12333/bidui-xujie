#!/usr/bin/env python3
"""核验 19卷.md（宇宙学推导整理）关键印数。

依赖卷16 钉死链（a_UV）与卷18 的 λ=ln5；不重证路径混合机制。
严格度分层：算出 / 恒等 / 估计 / 文稿自标待补。

运行：
    python3 scripts/check_vol19.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    F_LOOP,
    HBARC_MS,
    M0_PRINT,
    N_C,
    N_OCT,
    OMEGA0_PRINT,
    Check,
    c_node,
    den_geometry,
    nearly,
    report,
)

# SI / 字典
C_SI = 299792458.0
MPC_M = 3.0856775814913673e22
SEC_PER_GYR = 365.25 * 24 * 3600 * 1e9
HBAR_MEV_S = 6.582119569e-22  # MeV·s
WIEN_B = 2.8978e-3  # m·K（文稿）
N_TOTAL = 38
N_ADD = 26  # N_total - N_oct


def lambda_mix() -> float:
    return math.log(5.0)


def a_uv_m() -> float:
    """钉死链：L_IR = 2π ħc / Ω0，a_UV = L_IR / 40^12。"""
    l_ir_fm = 2.0 * math.pi * HBARC_MS / OMEGA0_PRINT
    return (l_ir_fm * 1e-15) / (F_LOOP**N_OCT)


def a_eff_m(n_total: int = N_TOTAL) -> float:
    """a_eff = a_UV · 40^{N_total}（从 UV 起总粗粒化层）。"""
    return a_uv_m() * (F_LOOP**n_total)


def h0_si(n_total: int = N_TOTAL) -> float:
    return lambda_mix() * C_SI / a_eff_m(n_total)


def h0_kms_mpc(n_total: int = N_TOTAL) -> float:
    return h0_si(n_total) * (MPC_M / 1000.0)


def checks() -> list[Check]:
    lam = lambda_mix()
    auv = a_uv_m()
    ae = a_eff_m()
    h0 = h0_kms_mpc()
    h0s = h0_si()
    rh = C_SI / h0s
    t0_gyr = (1.0 / h0s) / SEC_PER_GYR
    geom = math.sqrt(auv * rh)
    t_cmb = WIEN_B / (4.0 * math.pi * math.sqrt(2.0) * geom)
    den = den_geometry()
    ns = 1.0 - lam / N_TOTAL
    g = math.exp(lam / 2.0)
    ell1 = math.pi * F_LOOP

    # MeV 路径：H0 = λ Ω0 / (2π · 40^26)，ħ=c=1；再 / ħ → 1/s
    h0_mev = lam * OMEGA0_PRINT / (2.0 * math.pi * (F_LOOP**N_ADD))
    h0_from_mev = (h0_mev / HBAR_MEV_S) * (MPC_M / 1000.0)

    out: list[Check] = []

    # --- 收录恒等 ---
    out.append(Check("λ = ln 5", nearly(lam, math.log(5.0)), f"{lam:.6f}"))
    out.append(Check("N_br = 3×2−1 = 5", N_C * 2 - 1 == 5, "5"))
    out.append(Check("f_loop=40, N_oct=12", F_LOOP == 40 and N_OCT == 12, f"{F_LOOP},{N_OCT}"))
    out.append(
        Check(
            "N_total = 3 N_oct + 2 = 38",
            3 * N_OCT + 2 == N_TOTAL,
            f"{3 * N_OCT + 2}",
        )
    )
    out.append(
        Check(
            "代数合一：13=1+N_oct 且 N_add=2(1+N_oct)",
            (1 + N_OCT == 1 + N_C + N_C**2)
            and (N_ADD == 2 * (1 + N_OCT))
            and (N_OCT + N_ADD == 3 * N_OCT + 2),
            f"13={1+N_OCT}, add={N_ADD}",
        )
    )
    out.append(
        Check(
            "N_add = 2(1+Nc+Nc²) = 26",
            2 * (1 + N_C + N_C**2) == N_ADD and N_OCT + N_ADD == N_TOTAL,
            f"{N_ADD}",
        )
    )
    out.append(
        Check(
            "a_UV ≈ 2.769e-35 m（钉死链）",
            nearly(auv, 2.769e-35, rel=5e-4),
            f"{auv:.4e}",
        )
    )

    # --- Hubble ---
    out.append(
        Check(
            "邻层排除：N=37 → H0≫观测",
            h0_kms_mpc(37) > 2000,
            f"{h0_kms_mpc(37):.0f}",
        )
    )
    out.append(
        Check(
            "邻层排除：N=39 → H0≪观测",
            h0_kms_mpc(39) < 5,
            f"{h0_kms_mpc(39):.2f}",
        )
    )
    out.append(
        Check(
            "H0 ≈ 71.0 km/s/Mpc（文稿印数；复算≈71.17）",
            nearly(h0, 71.0, abs_=0.3),
            f"{h0:.2f}",
        )
    )
    out.append(
        Check(
            "H0 MeV 路径与 a_UV 路径同位",
            nearly(h0_from_mev, h0, rel=1e-3),
            f"MeV链 {h0_from_mev:.2f} vs UV链 {h0:.2f}",
        )
    )
    out.append(
        Check(
            "H0_mev ≈ 1.517e-39（文稿中间印数）",
            nearly(h0_mev, 1.517e-39, rel=2e-3),
            f"{h0_mev:.4e}",
        )
    )
    out.append(
        Check(
            "R_H = a_eff/λ = a_UV·40^38/λ",
            nearly(rh, ae / lam) and nearly(rh, auv * (40**38) / lam),
            f"{rh:.4e} m",
        )
    )
    out.append(
        Check(
            "D(R_H) = 1/e",
            nearly(math.exp(-lam * rh / ae), 1.0 / math.e),
            f"{math.exp(-1):.6f}",
        )
    )
    out.append(
        Check(
            "t0 = 1/H0 ≈ 13.77 Gyr（印数；复算≈13.74）",
            nearly(t0_gyr, 13.77, abs_=0.05),
            f"{t0_gyr:.3f}",
        )
    )
    out.append(Check("t0·H0 = 1（精确）", nearly(t0_gyr * h0s * SEC_PER_GYR, 1.0), "1"))

    # --- CMB ---
    out.append(
        Check(
            "√(a_UV R_H) ≈ 6.00e-5 m",
            nearly(geom, 6.00e-5, rel=5e-3),
            f"{geom:.4e}",
        )
    )
    out.append(
        Check(
            "4π√2 ≈ 17.772",
            nearly(4 * math.pi * math.sqrt(2), 17.7715, abs_=1e-3),
            f"{4*math.pi*math.sqrt(2):.4f}",
        )
    )
    out.append(
        Check(
            "T_CMB ≈ 2.718 K",
            nearly(t_cmb, 2.718, abs_=0.005),
            f"{t_cmb:.4f}",
        )
    )
    out.append(
        Check(
            "相对观测 2.7255 偏差 ≈0.3%",
            abs(t_cmb - 2.7255) / 2.7255 < 0.005,
            f"{abs(t_cmb-2.7255)/2.7255*100:.3f}%",
        )
    )
    out.append(
        Check(
            "宇宙学 Wien：T√(aUV RH)=b/(4π√2)",
            nearly(t_cmb * geom, WIEN_B / (4 * math.pi * math.sqrt(2)), rel=1e-9),
            f"{t_cmb*geom:.6e}",
        )
    )
    # 刀 A 失败模式：错误标度选择必须远离观测（防回退）
    pref = 4 * math.pi * math.sqrt(2)
    t_arith = WIEN_B / (pref * 0.5 * (auv + rh))
    t_no_lam = WIEN_B / (pref * auv * (40 ** (N_TOTAL / 2)))
    t_bare = WIEN_B / geom
    out.append(
        Check(
            "失败模式：算术均值 T 远离 2.7K",
            abs(t_arith - 2.7255) / 2.7255 > 0.5,
            f"{t_arith:.3e} K",
        )
    )
    out.append(
        Check(
            "失败模式：Lmax=a_eff（无√λ）T 偏离 >10%",
            abs(t_no_lam - 2.7255) / 2.7255 > 0.1,
            f"{t_no_lam:.3f} K",
        )
    )
    out.append(
        Check(
            "失败模式：缺 4π√2 则 T~48K",
            abs(t_bare - 2.7255) / 2.7255 > 5,
            f"{t_bare:.1f} K",
        )
    )
    out.append(
        Check(
            "对照 Ξ=b/(T_obs√(aUV RH)) ≈ 4π√2",
            nearly(WIEN_B / (2.7255 * geom), pref, rel=5e-3),
            f"{WIEN_B/(2.7255*geom):.4f}",
        )
    )
    out.append(
        Check(
            "(16π cκ)^{1/4} ≈ 1.308",
            nearly(den**0.25, 1.3083, abs_=5e-4),
            f"{den**0.25:.4f}",
        )
    )

    # --- 估计档（文稿标估计，只核算术）---
    out.append(Check("ns = 1−ln5/38 ≈ 0.958", nearly(ns, 0.958, abs_=0.001), f"{ns:.4f}"))
    out.append(Check("g = e^{λ/2} ≈ 2.24（α=1/2）", nearly(g, 2.24, abs_=0.01), f"{g:.3f}"))
    out.append(
        Check(
            "ℓ1 启发式 π·40 ≈ 125.7（非观测命中）",
            nearly(ell1, 125.7, abs_=0.1),
            f"{ell1:.1f}",
        )
    )
    ell1_s3 = math.pi * math.sqrt(3.0) * F_LOOP
    out.append(
        Check(
            "对照 π√3·40 ≈ 217.7（√3 候选；非钉死）",
            nearly(ell1_s3, 217.7, abs_=0.1),
            f"{ell1_s3:.1f}",
        )
    )
    out.append(
        Check(
            "启发式对观测220偏差约43%",
            abs(ell1 - 220) / 220 > 0.35,
            f"{abs(ell1-220)/220*100:.1f}%",
        )
    )

    # --- 结构纪律占位 ---
    out.append(Check("ΩΛ=0、Ωm=1（结构断言；超新星对账待）", True, "函数形推断言；非已拟合"))
    out.append(
        Check(
            "N_total=38：代数算出；每侧一层待升",
            True,
            "两式合一算出；3N_oct+2 结构候选",
        )
    )
    out.append(Check("α≈0.5：估计旋钮，非钉死", True, "增长因子对照用"))

    # Ω0 / c_node 收录
    cn = c_node()
    out.append(
        Check(
            "Ω0 印数与 m0/(3 c_node) 同位",
            nearly(M0_PRINT / (3 * cn), OMEGA0_PRINT, abs_=3.0),
            f"{M0_PRINT/(3*cn):.1f}",
        )
    )
    return out


def main() -> int:
    return report("19卷（宇宙学整理）", checks())


if __name__ == "__main__":
    raise SystemExit(main())
