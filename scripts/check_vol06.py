#!/usr/bin/env python3
"""卷6：代隙比四格（文稿 §16 原样）。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import N_C, S1_PRINT, Check, kappa_w, nearly, report


def checks() -> list[Check]:
    s1 = S1_PRINT
    kw = kappa_w()
    lam1 = 1.0 + s1 / 27.0
    sqrt_lam = math.sqrt(lam1)
    f1d = sqrt_lam / kw
    f1u = kw * sqrt_lam * 27.0
    eta = 1.0 - s1 / N_C
    r1_bare = 207.0 / 9.0  # 23
    r2_bare = 16.83

    ms_md = f1d * r1_bare * eta
    mc_mu = f1u * r1_bare * eta
    mb_ms = 3.0 * r2_bare * eta
    mt_mc = 9.0 * r2_bare * eta

    out = [
        Check("κ_w = √(29/27) ≈ 1.036375", nearly(kw, 1.036375, abs_=1e-5), f"{kw:.6f}"),
        Check("√λ1 ≈ 1.005792", nearly(sqrt_lam, 1.005792, abs_=1e-6), f"{sqrt_lam:.6f}"),
        Check("F̃1(d) ≈ 0.970490", nearly(f1d, 0.970490, abs_=1e-5), f"{f1d:.6f}"),
        Check("F̃1(u) ≈ 28.144", nearly(f1u, 28.144, abs_=0.002), f"{f1u:.3f}"),
        Check("η_QCD ≈ 0.895443", nearly(eta, 0.895443, abs_=1e-5), f"{eta:.6f}"),
        Check("ms/md ≈ 19.987 → 20", nearly(ms_md, 19.987, abs_=0.01), f"{ms_md:.3f}"),
        Check("mc/mu ≈ 579.6 → 579", nearly(mc_mu, 579.6, abs_=0.5), f"{mc_mu:.1f}"),
        Check("mb/ms ≈ 45.211 → 45.2", nearly(mb_ms, 45.211, abs_=0.02), f"{mb_ms:.3f}"),
        Check("mt/mc ≈ 135.63 → 135.6", nearly(mt_mc, 135.63, abs_=0.05), f"{mt_mc:.2f}"),
        Check("禁止再乘 27 进 F̃1(u)", nearly(f1u * 27 * 23 * eta, 15647, abs_=50), "双重计数≈15647≠579"),
    ]
    # 最后一项是说明双重计数爆掉，应断言「不等于 579」
    out[-1] = Check(
        "禁止 F×F̃×R×η（≈15647 ≠ 579）",
        abs(f1u * 27 * 23 * eta - 579) > 1000,
        f"{f1u * 27 * 23 * eta:.0f}",
    )
    return out


def main() -> int:
    return report("卷6", checks())


if __name__ == "__main__":
    raise SystemExit(main())
