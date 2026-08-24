#!/usr/bin/env python3
"""各卷核验共用：印数、容差比较、报告。

工作印数与文稿钉死表对齐；精确对照路径在检查里另标，不回改钉死。
仅用标准库。
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# --- 整数座位 ---
N_C = 3
N_W = 2
F_LOOP = 1 + N_C + N_C**2 + N_C**3  # 40
N_OCT = N_C * (N_C + 1)  # 12

# --- 实验 / 字典（一位能量标定 + 朗读用） ---
M_TAU_MEV = 1776.86
HBARC_MS = 197.3  # MeV·fm（文稿钉死链）
LP_MS = 1.616e-35  # m（文稿钉死链）
HBARC_CODATA = 197.32698  # MeV·fm（卷16 对照）
LP_CODATA = 1.616255e-35  # m（卷16 对照）

# --- 工作印数（后卷收录用；中间取位叠出的 0.9998 不采用） ---
S1_PRINT = 0.31367
Q_PRINT = 0.7308
M0_PRINT = 6228.0  # MeV；严格 m_τ/q^4 ≃ 6230，差标为取位
C_NODE_PRINT = 0.7776
OMEGA0_PRINT = 2669.0  # MeV
VH_GEV_PRINT = 249.0  # 40 × 6.23 GeV


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def nearly(a: float, b: float, rel: float = 1e-9, abs_: float = 1e-12) -> bool:
    return abs(a - b) <= max(abs_, rel * max(abs(a), abs(b), 1.0))


def rho() -> float:
    return 1.0 - (2.0 * math.pi) ** (-4)


def s1(rho_val: float | None = None) -> float:
    r = rho() if rho_val is None else rho_val
    return 2.0 * math.sqrt(2.0) * r**3 / 9.0


def q_from_s1(s1_val: float | None = None) -> float:
    return math.exp(-(s1() if s1_val is None else s1_val))


def kappa_w() -> float:
    return math.sqrt(1.0 + N_W / N_C**3)  # √(29/27)


def c_node() -> float:
    return math.sqrt(math.pi / (3.0 * math.sqrt(3.0)))


def c_kappa(kw: float | None = None) -> float:
    k = kappa_w() if kw is None else kw
    return k / (4.0 * math.pi * math.sqrt(2.0))


def den_geometry(kw: float | None = None) -> float:
    """16π c_κ = 2√2 κ_w。"""
    k = kappa_w() if kw is None else kw
    return 2.0 * math.sqrt(2.0) * k


def report(vol: str, checks: list[Check]) -> int:
    failed = [c for c in checks if not c.ok]
    print(f"=== {vol}：{len(checks) - len(failed)}/{len(checks)} 通过 ===")
    for c in checks:
        mark = "OK" if c.ok else "FAIL"
        print(f"  [{mark}] {c.name}: {c.detail}")
    if failed:
        print(f">>> {vol} 失败 {len(failed)} 项")
        return 1
    return 0
