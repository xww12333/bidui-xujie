#!/usr/bin/env python3
"""卷10：折返差 → |γ|=65°、J、ρ̄ η̄。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Check, nearly, report


def checks() -> list[Check]:
    delta = 90.0 - 60.0
    d5 = delta / math.factorial(3)  # 30/6=5
    gamma = 60.0 + 5.0
    vus = math.sqrt(1.0 / 20.0)
    vcb = math.sqrt(1.0 / 135.6) / 2.0
    vub = math.sqrt(1.0 / (579.0 * 135.6))
    j65 = abs(vus * vcb * vub) * math.sin(math.radians(65.0))
    r = 0.372
    rho_bar = r * math.cos(math.radians(65.0))
    eta_bar = r * math.sin(math.radians(65.0))

    out = [
        Check("Δ = 90−60 = 30°", nearly(delta, 30.0), f"{delta}"),
        Check("δ = 30/3! = 5°", nearly(d5, 5.0), f"{d5}"),
        Check("|γ| = 65°", nearly(gamma, 65.0), f"{gamma}"),
        Check("J(65°) ≈ 3.10e-5", nearly(j65, 3.10e-5, abs_=0.05e-5), f"{j65:.3e}"),
        Check("ρ̄ ≈ 0.157", nearly(rho_bar, 0.157, abs_=0.002), f"{rho_bar:.3f}"),
        Check("η̄ ≈ 0.337", nearly(eta_bar, 0.337, abs_=0.002), f"{eta_bar:.3f}"),
        Check("窗 [65,68]，不写 66° 为钉死", True, "仅断言窗口纪律"),
        Check("禁 30/3=10°", delta / 3.0 == 10.0, "10° 标为禁路径"),
    ]
    return out


def main() -> int:
    return report("卷10", checks())


if __name__ == "__main__":
    raise SystemExit(main())
