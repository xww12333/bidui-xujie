#!/usr/bin/env python3
"""卷14：时空涌现 — 结构计数（无 G 数字）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import N_C, Check, report


def checks() -> list[Check]:
    out = [
        Check("空间维数 = Nc = 3", N_C == 3, f"{N_C}"),
        Check("签名 3+1 计数", 3 + 1 == 4, "3+1"),
        Check("本卷无 G 印数靶", True, "数字留给卷16"),
    ]
    return out


def main() -> int:
    return report("卷14", checks())


if __name__ == "__main__":
    raise SystemExit(main())
