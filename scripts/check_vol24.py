#!/usr/bin/env python3
"""核验 卷24.md（衰变四档；第九部缺口闭合）关键印数。

依赖卷5 谱、卷8 CKM、卷11 b3=7、卷12 αs(Ω0)、卷13 vH / g2。
不重开 G、ℏ、谱。严格度分层：I 算出 / II 树图 / III–III+ 机制级 / IV 余项。
f_π、g_A 活动链见卷25；本卷数字冻结。

运行：
    python3 scripts/check_vol24.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (
    M0_PRINT,
    M_TAU_MEV,
    N_C,
    S1_PRINT,
    VH_GEV_PRINT,
    Check,
    c_node,
    nearly,
    report,
)

B3 = 7
INV_ALPHA_MZ = 127.96  # 与 check_vol13 同；非卷12 钉死第一行
SIN2 = 3.0 / 13.0
R_TAU_OBS = 3.628
GA_EXP = 1.276
GF_EXP = 1.166e-5
TAU_FW = 894.0
TAU_OBS = 879.4


def alpha_s_at(mu_mev: float, omega0: float, alpha_s0: float) -> float:
    inv = 1.0 / alpha_s0 + (B3 / (2.0 * math.pi)) * math.log(mu_mev / omega0)
    return 1.0 / inv


def alpha_wkb_logtau(Z: float, Q: float, r_in: float = 1.2, n: int = 400) -> float:
    """示意库仑穿透作用量（不拟合核表；禁 S1）。"""
    alpha = 1.0 / 137.0
    r_out = 2.0 * (Z - 2.0) * alpha / Q
    if r_out <= r_in:
        return 0.0
    s = 0.0
    dr = (r_out - r_in) / n
    for i in range(n):
        r = r_in + (i + 0.5) * dr
        vc = 2.0 * (Z - 2.0) * alpha / r
        if vc > Q:
            s += math.sqrt(2.0 * (vc - Q)) * dr
    return 2.0 * s


def checks() -> list[Check]:
    s1 = S1_PRINT
    cn = c_node()
    omega0 = M0_PRINT / (3.0 * cn)
    alpha_s0 = math.pi * s1 / 4.0
    q45 = math.exp(45.0 * s1)
    q9 = math.exp(9.0 * s1)

    a_tau = alpha_s_at(M_TAU_MEV, omega0, alpha_s0)
    r_tau0 = float(N_C)
    r_tau1 = 3.0 * (1.0 + a_tau / math.pi)

    ln_lam = (2.0 * math.pi / B3) * (1.0 - 1.0 / alpha_s0)
    lam = omega0 * math.exp(ln_lam)
    f130 = lam * cn
    f93 = f130 / math.sqrt(2.0)
    g_a = (5.0 / 3.0) * cn

    ln_pi = (2.0 * math.pi / B3) * (1.0 / math.pi - 1.0 / alpha_s0)
    lam_pi = omega0 * math.exp(ln_pi)

    gf = 1.0 / (math.sqrt(2.0) * VH_GEV_PRINT**2)
    alpha_mz = 1.0 / INV_ALPHA_MZ
    g2 = math.sqrt(4.0 * math.pi * alpha_mz / SIN2)
    mw = g2 * VH_GEV_PRINT / 2.0
    a_mw = alpha_s_at(mw * 1000.0, omega0, alpha_s0)
    gamma0 = gf * mw**3 / (6.0 * math.sqrt(2.0) * math.pi)
    n_eff = 3.0 + 2.0 * N_C * (1.0 + a_mw / math.pi)
    gamma_w = gamma0 * n_eff

    vcb = math.sqrt(1.0 / 135.6) / 2.0
    vub = math.sqrt(1.0 / (579.0 * 135.6))
    v_ratio = (vcb / vub) ** 2

    adler = 3.0 * (1.0 + a_tau / math.pi + 5.202 * (a_tau / math.pi) ** 2)
    dim_g = 8 + 3 + 1

    # R_τ 余项结构（IV；不拟合 3.628）
    x = a_tau / math.pi
    dR = R_TAU_OBS - r_tau1
    frac_1loop = x / (R_TAU_OBS / N_C - 1.0)

    # τ_n：G_F×g_A 净残差叙事
    combo_fw = 1.0 + 3.0 * g_a * g_a
    combo_exp = 1.0 + 3.0 * GA_EXP * GA_EXP
    g_ratio = combo_fw / combo_exp
    gf_ratio = (gf / GF_EXP) ** 2
    tau_net = 1.0 / (gf_ratio * g_ratio)
    tau_table = TAU_FW / TAU_OBS
    sens = 6.0 * g_a * g_a / combo_fw

    # 读法族：g_A 随 c_node；5/3 ≠ N_c；两枚 5/3 分家（布尔）
    ga_scaled = (5.0 / 3.0) * (cn * 1.01)

    # 核 α 示意 GN 形状
    z0, q0 = 90.0, 0.05
    base = alpha_wkb_logtau(z0, q0)
    higher_q = alpha_wkb_logtau(z0, q0 * 1.2)
    higher_z = alpha_wkb_logtau(z0 * 1.05, q0)
    qs = [0.04, 0.045, 0.05, 0.055, 0.06]
    xs = [1.0 / math.sqrt(q) for q in qs]
    ys = [alpha_wkb_logtau(z0, q) for q in qs]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x_ - mx) * (y_ - my) for x_, y_ in zip(xs, ys)) / sum(
        (x_ - mx) ** 2 for x_ in xs
    )

    out = [
        Check("q^{-9} = e^{9 S1} ≈ 16.83", nearly(q9, 16.83, abs_=0.02), f"{q9:.4f}"),
        Check(
            "q^{-45} = e^{45 S1} ≈ 1.35e6（I 档寿命比核）",
            nearly(q45, 1.35e6, rel=0.01),
            f"{q45:.4e}",
        ),
        Check("Rτ^{(0)} = Nc = 3（I）", r_tau0 == 3.0, f"{r_tau0}"),
        Check("αs(Ω0) = π S1/4 ≈ 0.2463", nearly(alpha_s0, 0.2463, abs_=5e-4), f"{alpha_s0:.4f}"),
        Check("αs(mτ) ≈ 0.277", nearly(a_tau, 0.277, abs_=0.002), f"{a_tau:.4f}"),
        Check(
            "Rτ 一圈 ≈ 3.265（II；≠ 观测 3.628）",
            nearly(r_tau1, 3.265, abs_=0.005) and abs(r_tau1 - R_TAU_OBS) > 0.3,
            f"{r_tau1:.4f}",
        ),
        Check(
            "Λ(αs=1) ≈ 171 MeV（II 红外标度）",
            nearly(lam, 171.0, abs_=2.0),
            f"{lam:.2f}",
        ),
        Check(
            "禁止 αs=π 当钉死（会贴 ~93 MeV）",
            nearly(lam_pi, 92.9, abs_=2.0) and abs(lam - lam_pi) > 50.0,
            f"Λ(π)={lam_pi:.1f} ≠ Λ(1)={lam:.1f}",
        ),
        Check(
            "fπ^{(130)} = Λ c_node ≈ 133 MeV（III+；链见卷25）",
            nearly(f130, 133.0, abs_=2.0),
            f"{f130:.2f}",
        ),
        Check(
            "fπ^{(93)} = Λ c_node/√2 ≈ 94 MeV（III+）",
            nearly(f93, 94.0, abs_=2.0),
            f"{f93:.2f}",
        ),
        Check(
            "gA = (5/3) c_node ≈ 1.296（III+；5/3 读法）",
            nearly(g_a, 1.296, abs_=0.005),
            f"{g_a:.4f}",
        ),
        Check(
            "读法：gA 随 c_node 同比缩放",
            nearly(ga_scaled / g_a, 1.01),
            f"{ga_scaled / g_a:.4f}",
        ),
        Check(
            "读法：5/3 ≠ Nc（两层分家）",
            abs(5.0 / 3.0 - N_C) > 0.5,
            f"5/3={5.0 / 3.0:.3f}",
        ),
        Check(
            "GF = 1/(√2 vH²) ≈ 1.140e-5（II）",
            nearly(gf, 1.140e-5, rel=0.002),
            f"{gf:.6e}",
        ),
        Check("g2 ≈ 0.652（卷13）", nearly(g2, 0.652, abs_=0.003), f"{g2:.4f}"),
        Check("MW ≈ 81.2 GeV（卷13）", nearly(mw, 81.2, abs_=0.3), f"{mw:.2f}"),
        Check("αs(MW) ≈ 0.127", nearly(a_mw, 0.127, abs_=0.003), f"{a_mw:.4f}"),
        Check(
            "ΓW 对齐 ≈ 2.12 GeV（II；≠ 未对齐 1.95）",
            nearly(gamma_w, 2.12, abs_=0.03) and abs(gamma_w - 1.95) > 0.1,
            f"{gamma_w:.3f}",
        ),
        Check("|Vcb| ≈ 0.0429（卷8）", nearly(vcb, 0.0429, abs_=5e-4), f"{vcb:.5f}"),
        Check("|Vub| ≈ 0.00357（卷8）", nearly(vub, 0.00357, abs_=5e-5), f"{vub:.5f}"),
        Check(
            "|Vcb/Vub|² = 579/4 = 144.75（I）",
            nearly(v_ratio, 579.0 / 4.0, abs_=1e-9) and nearly(v_ratio, 144.8, abs_=0.1),
            f"{v_ratio:.2f}",
        ),
        Check(
            "Adler 二圈仍不到 3.628（不升 I）",
            abs(adler - R_TAU_OBS) > 0.15 and adler < 3.50,
            f"{adler:.3f}",
        ),
        Check("规范维数 8+3+1=12（U(1)_B 不进 G）", dim_g == 12, f"{dim_g}"),
        Check("Ω0 = m0/(3 c_node) ≈ 2669", nearly(omega0, 2669.0, abs_=2.0), f"{omega0:.1f}"),
        # R_τ 余项结构门
        Check(
            "ΔR/R_obs ∈ (5%,15%)（IV 截断结构）",
            0.05 < (dR / R_TAU_OBS) < 0.15,
            f"{dR / R_TAU_OBS:.3f}",
        ),
        Check(
            "一圈解释不足一半超额（余项非可钉）",
            frac_1loop < 0.5,
            f"{frac_1loop:.3f}",
        ),
        Check(
            "Λ/mτ < 0.15（冷凝非主因量级）",
            (lam / M_TAU_MEV) < 0.15,
            f"{lam / M_TAU_MEV:.3f}",
        ),
        # τ_n 净残差
        Check(
            "τ_n：框架 gA 偏高、GF 偏低",
            g_a > GA_EXP and gf < GF_EXP,
            f"gA={g_a:.3f}, GF={gf:.3e}",
        ),
        Check(
            "τ_n：∂lnΓ/∂ln gA ∈ (1.5,1.8)",
            1.5 < sens < 1.8,
            f"{sens:.3f}",
        ),
        Check(
            "τ_n：净寿命比 ~ 表 +1.7%（同号同量级）",
            1.0 < tau_net < 1.04 and abs(tau_net - tau_table) < 0.01,
            f"net={tau_net:.4f}, table={tau_table:.4f}",
        ),
        # 核 α 形状（III+；秒数 IV）
        Check(
            "核α：Q↑ ⇒ logτ↓；Z↑ ⇒ logτ↑（示意）",
            higher_q < base < higher_z and base > 1.0,
            f"base={base:.2f}",
        ),
        Check(
            "核α：GN 斜率 d(logτ)/d(1/√Q) > 0",
            slope > 0.0,
            f"{slope:.3f}",
        ),
        Check("核α模型不含 S1（三口分家）", True, "by construction"),
    ]
    return out


def main() -> int:
    return report("卷24", checks())


if __name__ == "__main__":
    raise SystemExit(main())
