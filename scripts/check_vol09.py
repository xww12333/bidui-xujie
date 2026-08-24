#!/usr/bin/env python3
"""卷9：中微子 Seesaw、大气/太阳隙、混合角。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import F_LOOP, M0_PRINT, Q_PRINT, Check, nearly, report


def checks() -> list[Check]:
    m0, q = M0_PRINT, Q_PRINT
    mr = m0 * q**8  # MeV
    md_kev = math.sqrt(2.0) * m0 * q**34 / F_LOOP  # keV if m0 in MeV? 
    # m_D = √2 m0 q^34 / 40；m0=6228 MeV → 结果约 5.15 keV
    # 6228 * q^34 是 MeV；/40 仍是 MeV；×√2 → 需换成 keV：×1000
    md_mev = math.sqrt(2.0) * m0 * (q**34) / F_LOOP
    md_kev = md_mev * 1000.0
    eta_cb = 26.0 / 27.0
    # m3 in eV: η m_D² / M_R；单位：m_D 用 MeV，M_R 用 MeV → (MeV)²/MeV = MeV = 1e6 eV? 
    # 文稿：m3 ≈ 0.050 eV。m_D≈5.15 keV = 5.15e-3 MeV，M_R≈507 MeV
    # m_D²/M_R = (5.15e-3)² / 507 MeV = 5.23e-8 MeV = 5.23e-8 * 1e6 eV = 0.0523 eV，×26/27≈0.050
    m3 = eta_cb * (md_mev**2) / mr  # MeV
    m3_ev = m3 * 1e6
    m2 = m3_ev / math.sqrt(33.0)
    dm_atm = m3_ev**2
    dm_sol = m3_ev**2 / 33.0
    th12 = math.degrees(math.asin(1.0 / math.sqrt(3.0)))
    th23 = math.degrees(math.asin(1.0 / math.sqrt(2.0)))

    out = [
        Check("MR = m0 q⁸ ≈ 507 MeV", nearly(mr, 507.0, abs_=2.0), f"{mr:.1f}"),
        Check("mD ≈ 5.15 keV", nearly(md_kev, 5.15, abs_=0.05), f"{md_kev:.3f}"),
        Check("η_cb = 26/27", nearly(eta_cb, 26.0 / 27.0), f"{eta_cb}"),
        Check("m3 ≈ 0.050 eV", nearly(m3_ev, 0.050, abs_=0.002), f"{m3_ev:.4f}"),
        Check("Δm²_atm ≈ 2.53e-3", nearly(dm_atm, 2.53e-3, abs_=0.05e-3), f"{dm_atm:.3e}"),
        Check("33 = 27+4+2", 27 + 4 + 2 == 33, "33"),
        Check("m2 = m3/√33 ≈ 0.0088 eV", nearly(m2, 0.0088, abs_=0.0002), f"{m2:.4f}"),
        Check("Δm²_sol ≈ 7.67e-5", nearly(dm_sol, 7.67e-5, abs_=0.15e-5), f"{dm_sol:.3e}"),
        Check("θ12 = arcsin(1/√3) ≈ 35.3°", nearly(th12, 35.3, abs_=0.1), f"{th12:.2f}"),
        Check("θ23 = 45°", nearly(th23, 45.0, abs_=0.01), f"{th23:.2f}"),
        Check("不写 θ13=1/√33", abs(math.asin(1 / math.sqrt(33)) * 180 / math.pi - 10) < 1, "禁升级"),
    ]
    return out


def main() -> int:
    return report("卷9", checks())


if __name__ == "__main__":
    raise SystemExit(main())
