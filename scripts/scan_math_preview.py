#!/usr/bin/env python3
"""扫描各卷 Markdown 数学符号的预览风险项。"""
from __future__ import annotations

import glob
import re
from collections import defaultdict


def vol_num(path: str) -> int:
    m = re.search(r"卷(\d+)", path)
    return int(m.group(1)) if m else 0


def scan() -> None:
    risk: dict[str, list[tuple[int, str, str]]] = defaultdict(list)
    stats: dict[str, dict[str, int]] = {}

    def sort_key(path: str):
        return (vol_num(path), 1 if "补" in path else 0, path)

    for path in sorted(glob.glob("卷*.md"), key=sort_key):
        v = path.replace("\\", "/").split("/")[-1].removeprefix("卷").removesuffix(".md")
        lines = open(path, encoding="utf-8").read().splitlines()
        s = {"lines": len(lines), "inline": 0, "display": 0, "table_math": 0, "boxed": 0}
        in_code = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if line.strip().startswith("|") and "$" in line:
                s["table_math"] += 1
            if re.search(r"\$\$.*\\boxed", line) or (
                line.strip().startswith("$$") and "\\boxed" in line
            ):
                s["boxed"] += 1
            if line.strip().startswith("$$") and line.strip().endswith("$$") and line.count("$$") == 2:
                s["display"] += 1
            tmp = re.sub(r"\$\$.*?\$\$", "", line)
            if tmp.count("$") >= 2:
                s["inline"] += tmp.count("$") // 2
            if "\\(" in line or "\\)" in line:
                risk[v].append((i, "\\\\( \\\\) 定界符（部分预览不支持）", line.strip()[:80]))
            if re.search(r"\$[^$]*<[^$]*\$", line):
                risk[v].append((i, "$ 内含 <（部分预览当 HTML）", line.strip()[:80]))
            if line.strip().startswith("|") and "$" in line and "\\|" in line:
                risk[v].append((i, "表内 \\\\|（偶发拆列）", line.strip()[:80]))
            if re.match(r"^#{1,6} ", line) and "$" in line:
                risk[v].append((i, "标题内 $（GitHub 标题不渲公式）", line.strip()[:80]))
            if "\\operatorname" in line:
                risk[v].append((i, "operatorname（GitHub 禁此宏）", line.strip()[:80]))
            in_math = False
            k = 0
            while k < len(line):
                if line[k] == "$":
                    if k + 1 < len(line) and line[k + 1] == "$":
                        k += 2
                        continue
                    if not in_math:
                        prev = line[k - 1] if k else ""
                        ok = (not prev) or prev.isspace() or (
                            prev.isascii() and not prev.isalnum() and prev not in "_\\"
                        )
                        if not ok:
                            risk[v].append((i, "开 $ 左邻非空格/英文标点（GitHub 不认）", line.strip()[:80]))
                            break
                        in_math = True
                    else:
                        in_math = False
                    k += 1
                else:
                    k += 1
        stats[v] = s

    def key_order(v: str):
        n = int(re.search(r"\d+", v).group())
        return (n, 1 if "补" in v else 0, v)

    print("卷 | 行数 | 行内$ | 块级$$ | 表内$ | boxed")
    print("---:|---:|---:|---:|---:|---:")
    for v in sorted(stats, key=key_order):
        s = stats.get(v, {})
        print(f"{v} | {s.get('lines',0)} | {s.get('inline',0)} | {s.get('display',0)} | {s.get('table_math',0)} | {s.get('boxed',0)}")

    print("\n## 风险明细\n")
    total = sum(len(risk[v]) for v in risk)
    if not total:
        print("无已知结构性风险。")
        return
    for v in sorted(risk, key=key_order):
        if not risk[v]:
            continue
        print(f"### 卷{v}（{len(risk[v])} 项）\n")
        for ln, kind, snippet in risk[v]:
            print(f"- L{ln} [{kind}] `{snippet}`")
        print()


if __name__ == "__main__":
    scan()
