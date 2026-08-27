#!/usr/bin/env python3
"""统一入口：跑完全部分卷计算核验。

用法：
    python3 scripts/run_all_checks.py
    python3 scripts/run_all_checks.py --only 4,5,16
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

VOLUMES = list(range(1, 20)) + [24]  # 1–19 有脚本；20–23 无独立核验入口；24 衰变四档


def main() -> int:
    ap = argparse.ArgumentParser(description="比对续接——差异传态网络：分卷计算核验")
    ap.add_argument(
        "--only",
        type=str,
        default="",
        help="逗号分隔卷号，如 4,5,16；默认全部",
    )
    args = ap.parse_args()
    if args.only.strip():
        vols = [int(x) for x in args.only.split(",") if x.strip()]
    else:
        vols = VOLUMES

    failed: list[int] = []
    for n in vols:
        if n not in VOLUMES:
            print(f"跳过无效卷号 {n}")
            continue
        mod = importlib.import_module(f"check_vol{n:02d}")
        rc = mod.main()
        if rc != 0:
            failed.append(n)
        print()

    print("=" * 40)
    if failed:
        print(f"失败卷：{failed}")
        return 1
    print(f"全部通过（{len(vols)} 卷）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
