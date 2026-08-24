#!/usr/bin/env python3
"""卷7：夸克绝对谱（收录 v_H 与四比）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import F_LOOP, VH_GEV_PRINT, Check, nearly, report


def checks() -> list[Check]:
    vh = VH_GEV_PRINT
    mt = vh / (2.0**0.5)
    mb = mt / 40.0
    mc = mt / 135.6
    mu = mc / 579.0  # GeV
    ms = mb / 45.2  # GeV
    md = ms / 20.0
    same_gen = 40.0 * 45.2 / 135.6
    banned = mt / 27.0

    out = [
        Check("mt = vH/√2 ≈ 176.1 GeV", nearly(mt, 176.1, abs_=0.05), f"{mt:.2f}"),
        Check("mb = mt/40 ≈ 4.40 GeV", nearly(mb, 4.40, abs_=0.01), f"{mb:.3f}"),
        Check("mc = mt/135.6 ≈ 1.30 GeV", nearly(mc, 1.30, abs_=0.01), f"{mc:.3f}"),
        Check("mu = mc/579 ≈ 2.24 MeV", nearly(mu * 1000, 2.24, abs_=0.03), f"{mu*1000:.3f}"),
        Check("ms = mb/45.2 ≈ 97.4 MeV", nearly(ms * 1000, 97.4, abs_=0.3), f"{ms*1000:.2f}"),
        Check("md = ms/20 ≈ 4.87 MeV", nearly(md * 1000, 4.87, abs_=0.03), f"{md*1000:.3f}"),
        Check("同代比 40×45.2/135.6 ≈ 13.3", nearly(same_gen, 13.3, abs_=0.05), f"{same_gen:.2f}"),
        Check("排除 mt/27 ≈ 6.53（禁）", nearly(banned, 6.53, abs_=0.02), f"{banned:.2f} 标为禁值"),
        Check("f_loop=40 不抄进每一代比", F_LOOP == 40, "座位只在 vH、mb/mt"),
    ]
    return out


def main() -> int:
    return report("卷7", checks())


if __name__ == "__main__":
    raise SystemExit(main())
