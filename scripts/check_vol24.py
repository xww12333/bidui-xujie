#!/usr/bin/env python3
"""核验 卷24.md（衰变四档；第九部缺口闭合）关键印数。

依赖卷5 谱、卷8 CKM、卷11 b3=7、卷12 αs(Ω0)、卷13 vH / g2。
不重开 G、ℏ、谱。严格度分层：I 算出 / II 树图 / III 机制级 / IV 余项。

运行：
    python3 scripts/check_vol24.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    M0_PRINT,
    M_TAU_MEV,
    N_C,
    S1_PRINT,
    VH_GEV_PRINT,
    Check,
    c_node,
    nearly,
    report,
)

B3 = 7
INV_ALPHA_MZ = 127.96  # 与 check_vol13 同；非卷12 钉死第一行
SIN2 = 3.0 / 13.0


def alpha_s_at(mu_mev: float, omega0: float, alpha_s0: float) -> float:
    inv = 1.0 / alpha_s0 + (B3 / (2.0 * math.pi)) * math.log(mu_mev / omega0)
    return 1.0 / inv


def checks() -> list[Check]:
    s1 = S1_PRINT
    cn = c_node()
    omega0 = M0_PRINT / (3.0 * cn)
    alpha_s0 = math.pi * s1 / 4.0
    q45 = math.exp(45.0 * s1)
    q9 = math.exp(9.0 * s1)

    a_tau = alpha_s_at(M_TAU_MEV, omega0, alpha_s0)
    r_tau0 = float(N_C)
    r_tau1 = 3.0 * (1.0 + a_tau / math.pi)

    ln_lam = (2.0 * math.pi / B3) * (1.0 - 1.0 / alpha_s0)
    lam = omega0 * math.exp(ln_lam)
    f130 = lam * cn
    f93 = f130 / math.sqrt(2.0)
    g_a = (5.0 / 3.0) * cn

    # 禁止：αs(Λ)=π 贴 fπ≈92.4
    ln_pi = (2.0 * math.pi / B3) * (1.0 / math.pi - 1.0 / alpha_s0)
    lam_pi = omega0 * math.exp(ln_pi)

    gf = 1.0 / (math.sqrt(2.0) * VH_GEV_PRINT**2)
    alpha_mz = 1.0 / INV_ALPHA_MZ
    g2 = math.sqrt(4.0 * math.pi * alpha_mz / SIN2)
    mw = g2 * VH_GEV_PRINT / 2.0
    a_mw = alpha_s_at(mw * 1000.0, omega0, alpha_s0)
    gamma0 = gf * mw**3 / (6.0 * math.sqrt(2.0) * math.pi)
    n_eff = 3.0 + 2.0 * N_C * (1.0 + a_mw / math.pi)
    gamma_w = gamma0 * n_eff

    vcb = math.sqrt(1.0 / 135.6) / 2.0
    vub = math.sqrt(1.0 / (579.0 * 135.6))
    v_ratio = (vcb / vub) ** 2

    adler = 3.0 * (1.0 + a_tau / math.pi + 5.202 * (a_tau / math.pi) ** 2)
    dim_g = 8 + 3 + 1

    out = [
        Check("q^{-9} = e^{9 S1} ≈ 16.83", nearly(q9, 16.83, abs_=0.02), f"{q9:.4f}"),
        Check(
            "q^{-45} = e^{45 S1} ≈ 1.35e6（I 档寿命比核）",
            nearly(q45, 1.35e6, rel=0.01),
            f"{q45:.4e}",
        ),
        Check("Rτ^{(0)} = Nc = 3（I）", r_tau0 == 3.0, f"{r_tau0}"),
        Check("αs(Ω0) = π S1/4 ≈ 0.2463", nearly(alpha_s0, 0.2463, abs_=5e-4), f"{alpha_s0:.4f}"),
        Check("αs(mτ) ≈ 0.277", nearly(a_tau, 0.277, abs_=0.002), f"{a_tau:.4f}"),
        Check(
            "Rτ 一圈 ≈ 3.265（II；≠ 观测 3.628）",
            nearly(r_tau1, 3.265, abs_=0.005) and abs(r_tau1 - 3.628) > 0.3,
            f"{r_tau1:.4f}",
        ),
        Check(
            "Λ(αs=1) ≈ 171 MeV（II 红外标度）",
            nearly(lam, 171.0, abs_=2.0),
            f"{lam:.2f}",
        ),
        Check(
            "禁止 αs=π 当钉死（会贴 ~93 MeV）",
            nearly(lam_pi, 92.9, abs_=2.0) and abs(lam - lam_pi) > 50.0,
            f"Λ(π)={lam_pi:.1f} ≠ Λ(1)={lam:.1f}",
        ),
        Check(
            "fπ^{(130)} = Λ c_node ≈ 133 MeV（III）",
            nearly(f130, 133.0, abs_=2.0),
            f"{f130:.2f}",
        ),
        Check(
            "fπ^{(93)} = Λ c_node/√2 ≈ 94 MeV（III）",
            nearly(f93, 94.0, abs_=2.0),
            f"{f93:.2f}",
        ),
        Check(
            "gA = (5/3) c_node ≈ 1.296（III；5/3 读法）",
            nearly(g_a, 1.296, abs_=0.005),
            f"{g_a:.4f}",
        ),
        Check(
            "GF = 1/(√2 vH²) ≈ 1.140e-5（II）",
            nearly(gf, 1.140e-5, rel=0.002),
            f"{gf:.6e}",
        ),
        Check("g2 ≈ 0.652（卷13）", nearly(g2, 0.652, abs_=0.003), f"{g2:.4f}"),
        Check("MW ≈ 81.2 GeV（卷13）", nearly(mw, 81.2, abs_=0.3), f"{mw:.2f}"),
        Check("αs(MW) ≈ 0.127", nearly(a_mw, 0.127, abs_=0.003), f"{a_mw:.4f}"),
        Check(
            "ΓW 对齐 ≈ 2.12 GeV（II；≠ 未对齐 1.95）",
            nearly(gamma_w, 2.12, abs_=0.03) and abs(gamma_w - 1.95) > 0.1,
            f"{gamma_w:.3f}",
        ),
        Check("|Vcb| ≈ 0.0429（卷8）", nearly(vcb, 0.0429, abs_=5e-4), f"{vcb:.5f}"),
        Check("|Vub| ≈ 0.00357（卷8）", nearly(vub, 0.00357, abs_=5e-5), f"{vub:.5f}"),
        Check(
            "|Vcb/Vub|² = 579/4 = 144.75（I）",
            nearly(v_ratio, 579.0 / 4.0, abs_=1e-9) and nearly(v_ratio, 144.8, abs_=0.1),
            f"{v_ratio:.2f}",
        ),
        Check(
            "Adler 二圈仍不到 3.628（不升 I）",
            abs(adler - 3.628) > 0.15 and adler < 3.50,
            f"{adler:.3f}",
        ),
        Check("规范维数 8+3+1=12（U(1)_B 不进 G）", dim_g == 12, f"{dim_g}"),
        Check("Ω0 = m0/(3 c_node) ≈ 2669", nearly(omega0, 2669.0, abs_=2.0), f"{omega0:.1f}"),
    ]
    return out


def main() -> int:
    return report("卷24", checks())


if __name__ == "__main__":
    raise SystemExit(main())
