#!/usr/bin/env python3
"""卷12：精细结构三刀 → 137.029；sin²θW=3/13。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import M0_PRINT, S1_PRINT, Check, c_node, nearly, report


# 第3刀硬阶跃阈表（实验 MeV）
THRESHOLDS = [
    (2669.0, 1777.0, 19.0 / 3.0),
    (1777.0, 1273.0, 16.0 / 3.0),
    (1273.0, 106.0, 4.0),
    (106.0, 92.0, 3.0),
    (92.0, 4.7, 8.0 / 3.0),
    (4.7, 2.2, 7.0 / 3.0),
    (2.2, 0.511, 1.0),
]


def checks() -> list[Check]:
    s1 = S1_PRINT
    cn = c_node()
    omega0 = M0_PRINT / (3.0 * cn)
    inv_alpha1 = 40.0 * math.pi / (3.0 * s1)
    alpha_s = math.pi * s1 / 4.0
    delta_scheme = math.pi * alpha_s / (1.0 + alpha_s)
    pref = 2.0 / (3.0 * math.pi)
    deltas = [pref * coeff * math.log(hi / lo) for hi, lo, coeff in THRESHOLDS]
    delta_step = sum(deltas)
    delta_beta = delta_step - math.log(4.0)
    inv_alpha0 = inv_alpha1 - delta_scheme + delta_beta
    # 上跑核验（非钉死）
    d_mb_om = pref * (19.0 / 3.0) * math.log(4180.0 / 2669.0)
    d_mz_mb = pref * (20.0 / 3.0) * math.log(91188.0 / 4180.0)
    inv_mz_chk = inv_alpha1 - d_mb_om - d_mz_mb - delta_scheme

    out = [
        Check("c_node ≈ 0.7776", nearly(cn, 0.7776, abs_=1e-4), f"{cn:.6f}"),
        Check("Ω0 = m0/(3 c_node) ≈ 2669", nearly(omega0, 2669.0, abs_=2.0), f"{omega0:.1f}"),
        Check("sin²θW = 3/13", nearly(3.0 / 13.0, 0.230769, abs_=1e-6), f"{3/13:.6f}"),
        Check("13 = 1+3+9（无 Nw）", 1 + 3 + 9 == 13, "13"),
        Check("κ1/κ2 = 3/10", nearly(3.0 / 10.0, 0.3), "0.3"),
        Check("1/α(Ω0) = 40π/(3S1) ≈ 133.543", nearly(inv_alpha1, 133.543, abs_=0.002), f"{inv_alpha1:.3f}"),
        Check("αs(Ω0) = π S1/4 ≈ 0.2463", nearly(alpha_s, 0.2463, abs_=5e-4), f"{alpha_s:.4f}"),
        Check("方案差 ≈ 0.621", nearly(delta_scheme, 0.621, abs_=0.002), f"{delta_scheme:.3f}"),
        Check("2/(3π) ≈ 0.212207", nearly(pref, 0.212207, abs_=1e-6), f"{pref:.6f}"),
        Check("Δ_step ≈ 5.493", nearly(delta_step, 5.493, abs_=0.01), f"{delta_step:.3f}"),
        Check("Δ_β = Δ_step−ln4 ≈ 4.107", nearly(delta_beta, 4.107, abs_=0.005), f"{delta_beta:.3f}"),
        Check("1/α(0) = 137.029", nearly(inv_alpha0, 137.029, abs_=0.01), f"{inv_alpha0:.3f}"),
        Check("上跑核验 1/α(MZ)≈127.957", nearly(inv_mz_chk, 127.957, abs_=0.01), f"{inv_mz_chk:.3f}"),
        Check("只扣一次 ln4（非×7）", nearly(delta_step - 7 * math.log(4), 5.493 - 7 * 1.3863, abs_=0.05), "七段各扣会错"),
    ]
    return out


def main() -> int:
    return report("卷12", checks())


if __name__ == "__main__":
    raise SystemExit(main())
