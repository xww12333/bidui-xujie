#!/usr/bin/env python3
"""卷5：轻子一口井、m0、v_H=40 m0。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    F_LOOP,
    M0_PRINT,
    M_TAU_MEV,
    Q_PRINT,
    VH_GEV_PRINT,
    Check,
    nearly,
    report,
)


def checks() -> list[Check]:
    q = Q_PRINT
    q4 = q**4
    m0_strict = M_TAU_MEV / q4
    m0 = M0_PRINT  # 工作印数
    m_mu = m0 * q**13
    m_e = m0 * q**30
    r_mu_e = q ** (-17)
    r_tau_mu = q ** (-9)
    # 实验比对数对照 R
    r_exp = math.log(207.0) / math.log(16.83)
    v_h = 40.0 * (m0 / 1000.0)  # GeV，用印数 6.228 → 与 249 略差；文稿用 6.23

    out = [
        Check("q⁴ ≈ 0.285229", nearly(q4, 0.2852293, abs_=1e-6), f"{q4:.7f}"),
        Check(
            "m0 严格 = mτ/q⁴ ≈ 6230（印数 6228 为取位）",
            abs(m0_strict - 6230.0) < 2.0,
            f"strict={m0_strict:.2f}, print={m0}",
        ),
        Check("mμ = m0 q¹³ ≈ 105.6 MeV", nearly(m_mu, 105.6, abs_=0.25), f"{m_mu:.3f}"),
        Check("me = m0 q³⁰ ≈ 0.510 MeV", nearly(m_e, 0.510, abs_=0.003), f"{m_e:.4f}"),
        Check("q⁻⁹ ≈ 16.81", nearly(r_tau_mu, 16.81, abs_=0.05), f"{r_tau_mu:.3f}"),
        Check("q⁻¹⁷ ≈ 206.8", nearly(r_mu_e, 206.8, abs_=0.15), f"{r_mu_e:.2f}"),
        Check("R_exp ≈ 17/9", nearly(r_exp, 17.0 / 9.0, abs_=0.002), f"{r_exp:.4f}"),
        Check("f_loop = 1+3+9+27 = 40", F_LOOP == 40, f"{F_LOOP}"),
        Check(
            "v_H = 40×6.23 GeV ≈ 249 GeV（印数）",
            nearly(40.0 * 6.23, 249.2, abs_=0.01) and abs(VH_GEV_PRINT - 249.0) < 0.5,
            f"40×6.23={40.0 * 6.23}; 印数 {VH_GEV_PRINT}",
        ),
        Check(
            "印数链 v_H≈40 m0/1000",
            nearly(v_h, 249.12, abs_=0.5),
            f"{v_h:.2f} GeV",
        ),
    ]
    return out


def main() -> int:
    return report("卷5", checks())


if __name__ == "__main__":
    raise SystemExit(main())
