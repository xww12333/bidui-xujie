#!/usr/bin/env python3
"""卷13：Higgs / 电弱树图（vH、3/13、mW mZ mH）。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import N_W, VH_GEV_PRINT, Check, nearly, report


def checks() -> list[Check]:
    vh = VH_GEV_PRINT
    sin2 = 3.0 / 13.0
    cos2 = 10.0 / 13.0
    inv_alpha_mz = 127.96  # 核验用，非卷12钉死第一行
    alpha = 1.0 / inv_alpha_mz
    g2 = math.sqrt(4.0 * math.pi * alpha / sin2)
    gp = math.sqrt(4.0 * math.pi * alpha / cos2)
    mw = g2 * vh / 2.0
    mz = math.sqrt(g2**2 + gp**2) * vh / 2.0
    rho = mw**2 / (mz**2 * cos2)
    mh = vh / N_W

    out = [
        Check("vH = 249 GeV", nearly(vh, 249.0), f"{vh}"),
        Check("cos²θW = 10/13", nearly(cos2, 10.0 / 13.0), f"{cos2}"),
        Check("g2 ≈ 0.652", nearly(g2, 0.652, abs_=0.003), f"{g2:.3f}"),
        Check("mW ≈ 81.2 GeV", nearly(mw, 81.2, abs_=0.3), f"{mw:.2f}"),
        Check("mZ ≈ 92.6 GeV", nearly(mz, 92.6, abs_=0.3), f"{mz:.2f}"),
        Check("ρ = 1", nearly(rho, 1.0, abs_=1e-9), f"{rho}"),
        Check("mH = vH/Nw = 124.5 GeV", nearly(mh, 124.5, abs_=0.1), f"{mh:.1f}"),
        Check("Nw 不进 13", 1 + 3 + 9 == 13 and N_W == 2, "13 无 Nw"),
    ]
    return out


def main() -> int:
    return report("卷13", checks())


if __name__ == "__main__":
    raise SystemExit(main())
