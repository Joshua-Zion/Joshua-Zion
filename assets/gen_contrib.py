"""生成过去一年的贡献格子图 assets/contrib.svg。

数据源：github-contributions-api.jogruber.de（只读公开数据）。
用法：python assets/gen_contrib.py   # 由 .github/workflows/contrib.yml 每天调用
"""

import json
import os
import sys
import urllib.request
from datetime import date, timedelta

USER = "Joshua-Zion"
API = f"https://github-contributions-api.jogruber.de/v4/{USER}?y=last"

PITCH, CELL, GAP = 14, 11, 3
LEFT, TOP = 26, 26
LEGEND_H = 22

LEVELS = ["#e9eef5", "#c2d6f6", "#8db1f0", "#4f83e3", "#2563eb"]
TEXT = "#8b98a9"
FONT = "Inter, -apple-system, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif"
MONTHS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]


def fetch_days(src=None):
    """src 可以是本地 JSON 路径（curl 下载好的），留空则直接请求接口。"""
    if src:
        with open(src, encoding="utf-8") as f:
            data = json.load(f)
    else:
        with urllib.request.urlopen(API, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
    out = []
    for d in data["contributions"]:
        lvl = d.get("level")
        out.append((date.fromisoformat(d["date"]), int(lvl) if lvl is not None else level_of(int(d["count"]))))
    return out


def level_of(count):
    if count <= 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 9:
        return 3
    return 4


def build(days):
    first = days[0][0]
    start = first - timedelta(days=(first.weekday() + 1) % 7)  # 回到周日
    cols = ((days[-1][0] - start).days // 7) + 1
    w = LEFT + cols * PITCH + 4
    h = TOP + 7 * PITCH + LEGEND_H

    squares, month_marks = [], []
    last_label_col = -9
    for i, (d, lvl) in enumerate(days):
        col = (d - start).days // 7
        row = (d - start).days % 7
        x = LEFT + col * PITCH
        y = TOP + row * PITCH
        squares.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.6" fill="{LEVELS[lvl]}"/>'
        )
        if d.day == 1 and col - last_label_col >= 4:
            last_label_col = col
            month_marks.append(f'<text x="{x}" y="{TOP - 6}" font-size="10" fill="{TEXT}">{MONTHS[d.month - 1]}</text>')

    # 星期标签：一 / 三 / 五
    for row, label in ((1, "一"), (3, "三"), (5, "五")):
        month_marks.append(
            f'<text x="{LEFT - 7}" y="{TOP + row * PITCH + CELL - 1.5}" font-size="10" fill="{TEXT}" text-anchor="end">{label}</text>'
        )

    # 图例
    lx = w - 4 - (5 * (CELL + GAP) - GAP) - 34
    ly = TOP + 7 * PITCH + 6
    legend = [f'<text x="{lx - 8}" y="{ly + 9}" font-size="10" fill="{TEXT}" text-anchor="end">少</text>']
    for i, color in enumerate(LEVELS):
        legend.append(
            f'<rect x="{lx + i * (CELL + GAP)}" y="{ly}" width="{CELL}" height="{CELL}" rx="2.6" fill="{color}"/>'
        )
    legend.append(
        f'<text x="{lx + 5 * (CELL + GAP) + 2}" y="{ly + 9}" font-size="10" fill="{TEXT}">多</text>'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="过去一年的贡献情况">
  <g font-family="{FONT}">
    {"".join(month_marks)}
  </g>
  {"".join(squares)}
  <g font-family="{FONT}">
    {"".join(legend)}
  </g>
</svg>
'''


if __name__ == "__main__":
    svg = build(fetch_days(sys.argv[1] if len(sys.argv) > 1 else None))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contrib.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print("written", out, len(svg))
