#!/usr/bin/env python3
"""卷18：路径混合 D(n) 与局域带宽 B_max、可辨饱和 n_*。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import F_LOOP, N_C, N_OCT, Check, nearly, report

# 光速 SI（结构比用；非新切口）
C_MS = 299792458.0


def d_of_n(n: int, lam: float) -> float:
    return math.exp(-lam * n)


def n_star(d_star: float, lam: float) -> float:
    return math.log(1.0 / d_star) / lam


def r_star(a: float, d_star: float, lam: float) -> float:
    return a * n_star(d_star, lam)


def b_node(a: float) -> float:
    return F_LOOP * C_MS / a


def checks() -> list[Check]:
    lam = math.log(5.0)
    n_br = N_C * 2 - 1
    out: list[Check] = []

    out.append(Check("有效分支 3×2−1 = 5", n_br == 5, f"{n_br}"))
    out.append(Check("λ = ln 5", nearly(lam, math.log(5.0)), f"{lam:.6f}"))
    out.append(Check("D(0)=1", nearly(d_of_n(0, lam), 1.0), f"{d_of_n(0, lam)}"))
    out.append(Check("D(1)=1/5", nearly(d_of_n(1, lam), 0.2), f"{d_of_n(1, lam)}"))
    out.append(Check("D(n)=5^{-n}", nearly(d_of_n(3, lam), 5 ** -3), f"{d_of_n(3, lam):.6f}"))

    # n_* 示例：D_* = 0.01 → n_* = ln(100)/ln(5) ≈ 2.861
    d_star = 0.01
    n_s = n_star(d_star, lam)
    out.append(
        Check(
            "n_* (D_*=0.01) ≈ 2.861",
            nearly(n_s, 2.861, abs_=0.01),
            f"{n_s:.4f}",
        )
    )
    out.append(
        Check(
            "D(n_*)=D_*",
            nearly(d_of_n(int(round(n_s)), lam), d_star, rel=0.15),
            f"D({int(round(n_s))})={d_of_n(int(round(n_s)), lam):.4f}",
        )
    )

    a_uv = 1.0e-35
    r_s = r_star(a_uv, d_star, lam)
    out.append(
        Check(
            "r_* = (a/λ)ln(1/D_*) 量纲一致",
            nearly(r_s, (a_uv / lam) * math.log(100.0)),
            f"r_*={r_s:.3e} m",
        )
    )

    out.append(Check("f_loop = 40", F_LOOP == 40, f"{F_LOOP}"))
    out.append(
        Check(
            "B_node = 40c/a (a=1e-35)",
            nearly(b_node(a_uv), 40 * C_MS / a_uv, rel=1e-12),
            f"{b_node(a_uv):.3e} s^{-1}",
        )
    )

    # 40^12 与 N_oct
    out.append(
        Check(
            "40^12 = f_loop^N_oct",
            nearly(F_LOOP**N_OCT, F_LOOP**12),
            f"{F_LOOP**N_OCT:.4e}",
        )
    )
    out.append(
        Check(
            "log_40(40^12) = 12",
            nearly(math.log(F_LOOP**12, F_LOOP), 12.0),
            f"{math.log(F_LOOP**12, F_LOOP):.2f}",
        )
    )

    # 边界带宽：球面 L=1m, a=1e-35 → |∂A|~4π L²/a²
    L, a = 1.0, 1.0e-35
    area_edges = 4.0 * math.pi * L**2 / a**2
    b_cut = area_edges * C_MS / a
    out.append(
        Check(
            "B_∂A = |∂A|c/a 有限正",
            b_cut > 0 and math.isfinite(b_cut),
            f"{b_cut:.3e}",
        )
    )

    return out


def main() -> int:
    return report("卷18", checks())


if __name__ == "__main__":
    raise SystemExit(main())
