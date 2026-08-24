#!/usr/bin/env python3
"""卷17：信息与认知 — 无新物理常数，仅纪律占位。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Check, report


def checks() -> list[Check]:
    return [
        Check("无新物理常数靶", True, "本卷不算出印数"),
        Check("不把认知图顶点并进物理图", True, "两张图共享 𝔠"),
        Check("不调用 HP=-1 当认知机制", True, "纪律"),
    ]


def main() -> int:
    return report("卷17", checks())


if __name__ == "__main__":
    raise SystemExit(main())
