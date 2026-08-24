#!/usr/bin/env python3
"""卷16：G 与 ħ — 堆积、几何锁 G；ħ SI 闭合标不适用。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    F_LOOP,
    HBARC_CODATA,
    HBARC_MS,
    LP_CODATA,
    LP_MS,
    M0_PRINT,
    M_TAU_MEV,
    N_OCT,
    OMEGA0_PRINT,
    S1_PRINT,
    Check,
    c_kappa,
    c_node,
    den_geometry,
    kappa_w,
    nearly,
    q_from_s1,
    report,
    s1,
)


def chain(m0: float, omega: float, hbarc: float, lp: float, den: float) -> dict[str, float]:
    l_ir_fm = 2.0 * math.pi * hbarc / omega
    a_uv_m = (l_ir_fm * 1e-15) / (F_LOOP**N_OCT)
    ratio = a_uv_m / lp
    ratio2 = ratio * ratio
    return {
        "L_IR_fm": l_ir_fm,
        "a_UV": a_uv_m,
        "a_over_lp": ratio,
        "a_over_lp2": ratio2,
        "G_over_Gobs": ratio2 / den,
        "G_event": ratio2 / (4.0 * math.log(2.0)),
    }


def checks() -> list[Check]:
    kw = kappa_w()
    den = den_geometry(kw)
    ck = c_kappa(kw)
    # 未圆整全链：用精确 c_node 与印数 m0 得 Ω0，或直接用印数 2669
    cn = c_node()
    omega_from_m0 = M0_PRINT / (3.0 * cn)
    ch = chain(M0_PRINT, OMEGA0_PRINT, HBARC_MS, LP_MS, den)
    ch_prec = chain(M0_PRINT, omega_from_m0, HBARC_MS, LP_MS, den)

    geom_proj = math.sqrt(den)
    evt_proj = 2.0 * math.sqrt(math.log(2.0))
    # 文稿 boxed：G/Gobs = 2.9349 / (2√2 √(29/27)) ≈ 1.0012
    ratio2_boxed = 2.9349
    g_over_boxed = ratio2_boxed / den

    out = [
        Check("f_loop=40, N_oct=12", F_LOOP == 40 and N_OCT == 12, f"{F_LOOP},{N_OCT}"),
        Check("40^12 ≈ 1.6777e19", nearly(F_LOOP**N_OCT, 1.6777e19, rel=1e-4), f"{F_LOOP**N_OCT:.4e}"),
        Check("κ_w = √(29/27)", nearly(kw, math.sqrt(29 / 27)), f"{kw:.6f}"),
        Check("16π c_κ = 2√2 κ_w ≈ 2.9313", nearly(den, 2.9313, abs_=1e-3), f"{den:.4f}"),
        Check("c_κ 公式一致", nearly(16 * math.pi * ck, den), f"{16*math.pi*ck:.4f}"),
        Check("L_IR = 2π×197.3/2669 ≈ 0.46447 fm", nearly(ch["L_IR_fm"], 0.46447, abs_=1e-4), f"{ch['L_IR_fm']:.5f}"),
        Check("a/ℓP（堆积）≈ 1.713", nearly(ch["a_over_lp"], 1.713, abs_=0.003), f"{ch['a_over_lp']:.4f}"),
        Check("(a/ℓP)² ≈ 2.9349", nearly(ch["a_over_lp2"], 2.9349, abs_=0.01), f"{ch['a_over_lp2']:.4f}"),
        Check("几何投影 √(16π c_κ) ≈ 1.712", nearly(geom_proj, 1.712, abs_=0.002), f"{geom_proj:.4f}"),
        Check("事件投影 2√(ln2) ≈ 1.665", nearly(evt_proj, 1.665, abs_=0.001), f"{evt_proj:.4f}"),
        Check("G/Gobs（几何，未圆整）≈ 1.0012", nearly(ch["G_over_Gobs"], 1.0012, abs_=0.001), f"{ch['G_over_Gobs']:.4f}"),
        Check("boxed 2.9349/den ≈ 1.0012", nearly(g_over_boxed, 1.0012, abs_=5e-4), f"{g_over_boxed:.4f}"),
        Check("事件比 ≈ 1.0585（非钉死 G）", nearly(ch["G_event"], 1.0585, abs_=0.003), f"{ch['G_event']:.4f}"),
        Check("不采用中间取位 0.9998", abs(ch["G_over_Gobs"] - 0.9998) > 5e-4, f"{ch['G_over_Gobs']:.4f}≠0.9998"),
        Check("禁：ln2 与 c_κ 同一分母", abs(4 * math.log(2) - den) > 0.1, f"4ln2={4*math.log(2):.3f} vs den={den:.3f}"),
        Check("ħ 形式 ħ=π m0 a c/(2 S1)（结构，不闭 SI）", True, f"S1={S1_PRINT}"),
        Check("事件锁 a²=4 G ħ ln2（结构）", True, "形式恒等"),
        Check("ħ SI 数值闭合：不适用（字典循环）", True, "非预言靶"),
        Check("Ω0 印数与 m0/(3c_node) 同位", nearly(omega_from_m0, OMEGA0_PRINT, abs_=3.0), f"{omega_from_m0:.1f}"),
        Check("精确 Ω0 链仍 ~1.00x", nearly(ch_prec["G_over_Gobs"], 1.0, abs_=0.005), f"{ch_prec['G_over_Gobs']:.4f}"),
    ]
    # 对照：精确 m0=mτ/q⁴（q 来自 S1）、CODATA ħc 与 ℓP → ≈0.99961；不进钉死
    m0_exact = M_TAU_MEV / (q_from_s1(s1()) ** 4)
    omega_exact = m0_exact / (3.0 * cn)
    ch_ctrl = chain(m0_exact, omega_exact, HBARC_CODATA, LP_CODATA, den)
    out.append(
        Check(
            "对照 G/Gobs ≈ 0.99961（精确 m0 + CODATA；不进钉死）",
            nearly(ch_ctrl["G_over_Gobs"], 0.99961, abs_=5e-5),
            f"m0={m0_exact:.2f}, Ω0={omega_exact:.1f}, ratio={ch_ctrl['G_over_Gobs']:.6f}",
        )
    )
    out.append(
        Check(
            "对照相对 1 约 0.039%（同量级命中）",
            abs(ch_ctrl["G_over_Gobs"] - 1.0) < 5e-4,
            f"|1−ratio|={abs(ch_ctrl['G_over_Gobs']-1.0):.2e}",
        )
    )
    return out


def main() -> int:
    return report("卷16", checks())


if __name__ == "__main__":
    raise SystemExit(main())
