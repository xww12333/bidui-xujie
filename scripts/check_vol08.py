#!/usr/bin/env python3
"""卷8：CKM 三模、|γ|=60°、Jarlskog（单路径）。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Check, nearly, report


def checks() -> list[Check]:
    vus = math.sqrt(1.0 / 20.0)
    vcb = math.sqrt(1.0 / 135.6) / 2.0
    vub = math.sqrt(1.0 / (579.0 * 135.6))
    gamma = 60.0  # deg, 单路径
    j60 = abs(vus * vcb * vub) * math.cos(math.radians(30.0))  # cos(π/6)=√3/2；文稿 J=|…|cos(π/6)
    # 文稿：J = |Vus Vcb Vub| cos(π/6) ≈ 2.97e-5
    banned_vcb = math.sqrt(1.0 / 135.6) / math.sqrt(2.0)  # 偶通道误入

    out = [
        Check("|Vus| = √(1/20) ≈ 0.2236", nearly(vus, 0.2236, abs_=1e-3), f"{vus:.4f}"),
        Check("|Vcb| = √(1/135.6)/2 ≈ 0.0429", nearly(vcb, 0.0429, abs_=1e-3), f"{vcb:.4f}"),
        Check("|Vub| = √(1/(579×135.6)) ≈ 0.00357", nearly(vub, 0.00357, abs_=5e-5), f"{vub:.5f}"),
        Check("|γ| = 60°（单路径）", nearly(gamma, 60.0), f"{gamma}"),
        Check("J(60°) ≈ 2.97e-5", nearly(j60, 2.97e-5, abs_=0.05e-5), f"{j60:.3e}"),
        Check("禁：偶通道 1/√2 进 Vcb（≈0.061）", nearly(banned_vcb, 0.061, abs_=0.002), f"{banned_vcb:.3f} 标禁"),
    ]
    return out


def main() -> int:
    return report("卷8", checks())


if __name__ == "__main__":
    raise SystemExit(main())
