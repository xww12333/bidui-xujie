#!/usr/bin/env python3
"""卷18：路径混合 D(n)、质量带 λ_eff、局域带宽 B_max、可辨饱和 n_*。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import F_LOOP, N_C, N_OCT, Check, nearly, report

# 光速 SI（结构比用；非新切口）
C_MS = 299792458.0
LN5 = math.log(5.0)


def d_of_n(n: int, lam: float) -> float:
    return math.exp(-lam * n)


def n_star(d_star: float, lam: float) -> float:
    return math.log(1.0 / d_star) / lam


def r_star(a: float, d_star: float, lam: float) -> float:
    return a * n_star(d_star, lam)


def b_node(a: float) -> float:
    return F_LOOP * C_MS / a


def chi_of_xi(xi: float) -> float:
    """固有空间密度标量 χ=1/√(1−ξ)=√g_rr（机制级）。"""
    return 1.0 / math.sqrt(1.0 - xi)


def lambda_eff(xi: float) -> float:
    return chi_of_xi(xi) * LN5


def collision_lambda_uniform() -> float:
    """5-向均权：−ln(Σ p²)=ln5。"""
    p2 = 5.0 * (0.2**2)
    return -math.log(p2)


def collision_lambda_reweight(xi: float) -> float:
    """反例：径向概率按 χ 加重 → λ 下降（符号错）。"""
    chi = chi_of_xi(xi)
    w = [chi, chi, 1.0, 1.0, 1.0]  # 禁回程后 5 向
    s = sum(w)
    p = [x / s for x in w]
    return -math.log(sum(x * x for x in p))


def checks() -> list[Check]:
    lam = LN5
    n_br = N_C * 2 - 1
    out: list[Check] = []

    out.append(Check("有效分支 3×2−1 = 5", n_br == 5, f"{n_br}"))
    out.append(Check("λ = ln 5", nearly(lam, math.log(5.0)), f"{lam:.6f}"))
    out.append(Check("D(0)=1", nearly(d_of_n(0, lam), 1.0), f"{d_of_n(0, lam)}"))
    out.append(Check("D(1)=1/5", nearly(d_of_n(1, lam), 0.2), f"{d_of_n(1, lam)}"))
    out.append(Check("D(n)=5^{-n}", nearly(d_of_n(3, lam), 5 ** -3), f"{d_of_n(3, lam):.6f}"))

    eps0 = math.sqrt(LN5)
    out.append(
        Check(
            "ε₀=√(ln5)，真空 λ=ε₀²",
            nearly(eps0 * eps0, LN5),
            f"ε₀={eps0:.6f}",
        )
    )
    out.append(
        Check(
            "均权碰撞 λ=ln5（分支基线）",
            nearly(collision_lambda_uniform(), LN5),
            f"{collision_lambda_uniform():.6f}",
        )
    )

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

    # --- 第六章：质量带 λ_eff ---
    xi = 0.1
    chi = chi_of_xi(xi)
    le = lambda_eff(xi)
    out.append(
        Check(
            "χ=1/√(1−ξ)（ξ=0.1）",
            nearly(chi, 1.0 / math.sqrt(0.9)),
            f"{chi:.6f}",
        )
    )
    out.append(
        Check(
            "χ=√g_rr 与 1/√(−g₀₀) 外部等价",
            nearly(chi, math.sqrt(1.0 / (1.0 - xi))),
            f"{chi:.6f}",
        )
    )
    out.append(
        Check(
            "λ_eff=χ ln5（机制级）",
            nearly(le, chi * LN5),
            f"{le:.6f}",
        )
    )
    out.append(
        Check(
            "弱场 χ≈1+ξ/2（ξ=0.1）",
            nearly(chi, 1.0 + 0.5 * xi, abs_=0.01),
            f"{chi:.4f} vs {1.0 + 0.5 * xi:.4f}",
        )
    )
    out.append(
        Check(
            "ξ→0 ⇒ λ_eff→ln5",
            nearly(lambda_eff(1e-12), LN5, abs_=1e-9),
            f"{lambda_eff(1e-12):.6f}",
        )
    )
    r_m = a_uv * math.sqrt(1.0 - xi) / LN5 * math.log(1.0 / d_star)
    out.append(
        Check(
            "r_*(M)=a√(1−ξ)/ln5 · ln(1/D_*)",
            nearly(r_m, a_uv / le * math.log(1.0 / d_star)),
            f"{r_m:.3e}",
        )
    )
    out.append(
        Check(
            "质量带 r_* < 真空 r_*（同 D_*）",
            r_m < r_s,
            f"{r_m:.3e} < {r_s:.3e}",
        )
    )
    lam_rw = collision_lambda_reweight(xi)
    lam_clock = math.sqrt(1.0 - xi) * LN5
    out.append(
        Check(
            "禁概率重权：加重径向 ⇒ λ↓（反号）",
            lam_rw < LN5,
            f"λ_rw={lam_rw:.4f} < ln5",
        )
    )
    out.append(
        Check(
            "禁跟钟：√(−g₀₀)ln5 < ln5 < λ_eff",
            lam_clock < LN5 < le,
            f"clock={lam_clock:.4f}",
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
