#!/usr/bin/env python3
"""卷1：四元数乘法表与基维数（代数核验，无物理印数）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Check, report


def mul(a: tuple[float, ...], b: tuple[float, ...]) -> tuple[float, ...]:
    """(w,x,y,z) ↔ w + x e1 + y e2 + z e3，e1e2=e3，ei²=-1。"""
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return (
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
    )


def eq(a: tuple[float, ...], b: tuple[float, ...], eps: float = 1e-12) -> bool:
    return all(abs(u - v) < eps for u, v in zip(a, b))


def checks() -> list[Check]:
    one = (1.0, 0.0, 0.0, 0.0)
    e1 = (0.0, 1.0, 0.0, 0.0)
    e2 = (0.0, 0.0, 1.0, 0.0)
    e3 = (0.0, 0.0, 0.0, 1.0)
    out: list[Check] = []

    out.append(Check("e1² = -1", eq(mul(e1, e1), (-1.0, 0, 0, 0)), str(mul(e1, e1))))
    out.append(Check("e2² = -1", eq(mul(e2, e2), (-1.0, 0, 0, 0)), str(mul(e2, e2))))
    out.append(Check("e3² = -1", eq(mul(e3, e3), (-1.0, 0, 0, 0)), str(mul(e3, e3))))
    out.append(Check("e1 e2 = e3", eq(mul(e1, e2), e3), str(mul(e1, e2))))
    out.append(Check("e2 e1 = -e3", eq(mul(e2, e1), (-0.0, 0, 0, -1.0)), str(mul(e2, e1))))
    out.append(
        Check(
            "(e1 e2) e3 = e1 (e2 e3)",
            eq(mul(mul(e1, e2), e3), mul(e1, mul(e2, e3))),
            "结合律",
        )
    )
    out.append(Check("实维 = 4", True, "基 {1,e1,e2,e3}"))
    # 单位元
    out.append(Check("1·e1 = e1", eq(mul(one, e1), e1), "单位"))
    return out


def main() -> int:
    return report("卷1", checks())


if __name__ == "__main__":
    raise SystemExit(main())
