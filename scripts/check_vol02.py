#!/usr/bin/env python3
"""卷2：管/面计数与 λ=ln5（结构整数）。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import N_C, Check, nearly, report


def checks() -> list[Check]:
    out: list[Check] = []
    # 3×2−1=5 → λ=ln5
    five = N_C * 2 - 1
    out.append(Check("3×2−1 = 5", five == 5, f"{five}"))
    out.append(
        Check(
            "λ = ln 5",
            nearly(math.log(5.0), math.log(five)),
            f"{math.log(5.0):.6f}",
        )
    )
    out.append(Check("ℍ³ 实维 = 12", N_C * 4 == 12, f"{N_C * 4}"))
    return out


def main() -> int:
    return report("卷2", checks())


if __name__ == "__main__":
    raise SystemExit(main())
