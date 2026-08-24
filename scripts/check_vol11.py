#!/usr/bin/env python3
"""卷11：b3=7 与一圈系数读法（算术核验）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Check, nearly, report


def checks() -> list[Check]:
    # 色账六味：11 − 4 = 7（文稿算出）
    b3 = 11 - 4
    out = [
        Check("b3 = 11−4 = 7", b3 == 7, f"{b3}"),
        Check("11/3 为读法（非本卷新预言）", nearly(11.0 / 3.0, 3.666666, abs_=1e-5), "读法标记"),
        Check("本卷不闭 137", True, "交给卷12"),
    ]
    return out


def main() -> int:
    return report("卷11", checks())


if __name__ == "__main__":
    raise SystemExit(main())
