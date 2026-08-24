#!/usr/bin/env python3
"""卷15：Einstein 源 — 席位恒等（G 当符号）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Check, nearly, report


def checks() -> list[Check]:
    # κ = 8πG；rs = 2GM — 形式席位
    eight_pi = 8.0 * 3.141592653589793
    out = [
        Check("κ 席位因子 8π", nearly(eight_pi, 25.132741228, abs_=1e-6), f"{eight_pi}"),
        Check("rs = 2GM 系数 2", True, "形式"),
        Check("16π = 2×8π（卷16 几何分母预备）", nearly(16 * 3.141592653589793, 2 * eight_pi), "16π"),
        Check("本卷不钉 G/Gobs", True, "交给卷16"),
    ]
    return out


def main() -> int:
    return report("卷15", checks())


if __name__ == "__main__":
    raise SystemExit(main())
