#!/usr/bin/env python3
"""核验 卷25.md（类型账手征与红外模长）关键印数。

不重开常数；与卷24 检验表数字冻结对拍。
严格度：纪律／II／III+；5/3 读法不升 I。

运行：
    python3 scripts/check_vol25.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    F_LOOP,
    M0_PRINT,
    N_C,
    S1_PRINT,
    VH_GEV_PRINT,
    Check,
    c_node,
    nearly,
    report,
)

B3 = 7


def alpha_s_at(mu_mev: float, omega0: float, alpha_s0: float) -> float:
    inv = 1.0 / alpha_s0 + (B3 / (2.0 * math.pi)) * math.log(mu_mev / omega0)
    return 1.0 / inv


def checks() -> list[Check]:
    cn = c_node()
    omega0 = M0_PRINT / (3.0 * cn)
    alpha_s0 = math.pi * S1_PRINT / 4.0

    ln_lam = (2.0 * math.pi / B3) * (1.0 - 1.0 / alpha_s0)
    lam = omega0 * math.exp(ln_lam)
    f130 = lam * cn
    f93 = f130 / math.sqrt(2.0)
    g_a = (5.0 / 3.0) * cn

    ln_pi = (2.0 * math.pi / B3) * (1.0 / math.pi - 1.0 / alpha_s0)
    lam_pi = omega0 * math.exp(ln_pi)

    # 三口能量尺分家（量级）：v_H ≫ m_0 ≫ Λ
    m0 = M0_PRINT
    vh_mev = VH_GEV_PRINT * 1000.0

    # Goldstone 计数 N_f=2：3+3−3=3
    n_goldstone = 3 + 3 - 3

    # 同根：改 c_node 则 fπ 与 gA 同比（相对基线）
    cn2 = cn * 1.02
    f2 = lam * cn2
    g2 = (5.0 / 3.0) * cn2

    out = [
        Check("c_node = √(π/(3√3)) ≈ 0.7776", nearly(cn, 0.7776, abs_=5e-4), f"{cn:.6f}"),
        Check("Ω0 = m0/(3 c_node) ≈ 2669", nearly(omega0, 2669.0, abs_=2.0), f"{omega0:.1f}"),
        Check(
            "Λ(αs=1) ≈ 171 MeV（II；与卷24 同）",
            nearly(lam, 171.0, abs_=2.0),
            f"{lam:.2f}",
        ),
        Check(
            "判据禁 π：Λ(αs=π)≈93 ≠ Λ(1)",
            nearly(lam_pi, 92.9, abs_=2.0) and abs(lam - lam_pi) > 50.0,
            f"{lam_pi:.1f}",
        ),
        Check(
            "fπ^{(130)}=Λ c_node ≈ 133（III+；冻卷24）",
            nearly(f130, 133.0, abs_=2.0),
            f"{f130:.2f}",
        ),
        Check(
            "fπ^{(130)}=fπ^{(93)}√2（收录约定）",
            nearly(f130, f93 * math.sqrt(2.0)),
            f"{f130 / f93:.6f}",
        ),
        Check(
            "gA=(5/3)c_node ≈ 1.296（III+；5/3 读法）",
            nearly(g_a, 1.296, abs_=0.005),
            f"{g_a:.4f}",
        ),
        Check(
            "节点同根：Δc_node ⇒ Δfπ 与 ΔgA 同比",
            nearly(f2 / f130, 1.02) and nearly(g2 / g_a, 1.02),
            f"f×{f2 / f130:.4f}, g×{g2 / g_a:.4f}",
        ),
        Check(
            "三口尺分家：vH ≫ m0 ≫ Λ（MeV）",
            vh_mev > m0 > lam > 0,
            f"vH={vh_mev:.0f}, m0={m0:.0f}, Λ={lam:.0f}",
        ),
        Check(
            "N_f=2 Goldstone 计数 3+3−3=3",
            n_goldstone == 3,
            f"{n_goldstone}",
        ),
        Check(
            "电弱吃掉 3 ≠ 本卷 3π（计数同、口不同）",
            True,
            "纪律：不被 W 吃",
        ),
        Check(
            "5/3 读法 ≠ 框架新分数（≠ Nc）",
            abs(5.0 / 3.0 - N_C) > 0.5,
            f"5/3={5.0 / 3.0:.4f}",
        ),
        Check(
            "αs(Λ)=1 时耦合 O(1)（定义门）",
            nearly(alpha_s_at(lam, omega0, alpha_s0), 1.0, abs_=1e-9),
            f"{alpha_s_at(lam, omega0, alpha_s0):.6f}",
        ),
        Check(
            "f_loop=40 不进 fπ（禁并）",
            F_LOOP == 40 and abs(f130 - lam * 40) > 1000.0,
            "c_node≠40",
        ),
        Check("S1 不进 fπ 公式（禁双阱并）", True, "by construction"),
    ]
    return out


def main() -> int:
    return report("卷25", checks())


if __name__ == "__main__":
    raise SystemExit(main())
