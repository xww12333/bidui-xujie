#!/usr/bin/env python3
"""卷4：n_k、ρ、S1、q。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import Check, nearly, q_from_s1, report, rho, s1


def checks() -> list[Check]:
    n1, n2, n3 = 4, 13, 30
    r_top = (n3 - n2) / (n2 - n1)
    fb = 8.0 / 3.0
    r = rho()
    s = s1(r)
    s_flat = 2.0 * math.sqrt(2.0) / 9.0
    q = q_from_s1(s)

    out = [
        Check("n1,n2,n3 = 4,13,30", (n1, n2, n3) == (4, 13, 30), f"{n1},{n2},{n3}"),
        Check("R = (n3−n2)/(n2−n1) = 17/9", nearly(r_top, 17.0 / 9.0), f"{r_top}"),
        Check("fb = 8/3", nearly(fb, 8.0 / 3.0), f"{fb}"),
        Check("ρ = 1−(2π)^(−4) ≈ 0.99936", nearly(r, 0.99936, abs_=5e-6), f"{r:.8f}"),
        Check("S1 = 2√2 ρ³/9 ≈ 0.31367", nearly(s, 0.31367, abs_=5e-6), f"{s:.8f}"),
        Check("ρ=1 ⇒ S1 = 2√2/9 ≈ 0.31427", nearly(s_flat, 0.31427, abs_=1e-5), f"{s_flat:.8f}"),
        Check("q = e^(−S1) ≈ 0.7308", nearly(q, 0.7308, abs_=5e-5), f"{q:.6f}"),
    ]
    return out


def main() -> int:
    return report("卷4", checks())


if __name__ == "__main__":
    raise SystemExit(main())
