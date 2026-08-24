#!/usr/bin/env python3
"""卷3：超荷入账 ∑Y=0 与 Y0=1/6。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Check, nearly, report


def checks() -> list[Check]:
    y0 = 1.0 / 6.0
    # 一代：6×(1/6) + 3×(−2/3) + 3×(1/3) + 2×(−1/2) + 1 = 0
    # 文稿：6·1/6 + 3(−2/3) + 3(1/3) + 2(−1/2) + 1
    s = 6 * y0 + 3 * (-2.0 / 3.0) + 3 * (1.0 / 3.0) + 2 * (-0.5) + 1.0
    out = [
        Check("Y0 = 1/6", nearly(y0, 1.0 / 6.0), f"{y0}"),
        Check("一代 ∑Y = 0", nearly(s, 0.0, abs_=1e-12), f"{s}"),
    ]
    return out


def main() -> int:
    return report("卷3", checks())


if __name__ == "__main__":
    raise SystemExit(main())
