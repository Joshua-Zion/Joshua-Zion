"""生成 profile 横幅 assets/banner.svg（单一浅色配色）。"""

import math
import os

W, H = 1200, 260
CX, CY, R = 140, 130, 92

C = dict(
    g1="#ffffff", g2="#eef2f7", text="#0f172a", sub="#5b6b7f",
    accent="#2563eb", ring="#cbd5e1", dot="#e2e8f0", mono="#94a3b8", glow="#2563eb",
)


def polar(r, deg):
    a = math.radians(deg)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def lens(c):
    """光学刻度盘：外环 + 刻度 + 内环 + 高亮弧。"""
    o = [f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{c["ring"]}" stroke-width="1.6"/>']
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R - 17}" fill="none" stroke="{c["ring"]}" stroke-width="1" opacity="0.75"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R - 17}" fill="{c["glow"]}" opacity="0.05"/>')

    for i in range(36):
        a = i * 10
        major = i % 3 == 0
        r1 = R - 13 if major else R - 9
        x1, y1 = polar(r1, a)
        x2, y2 = polar(R - 4, a)
        o.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c["accent"]}" '
            f'stroke-width="{1.7 if major else 1}" stroke-linecap="round" opacity="{0.55 if major else 0.28}"/>'
        )

    o.append(f'<circle cx="{CX}" cy="{CY}" r="38" fill="none" stroke="{c["accent"]}" stroke-width="1.5" opacity="0.5"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="23" fill="none" stroke="{c["accent"]}" stroke-width="1" opacity="0.28"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="4.6" fill="{c["accent"]}"/>')

    p1, p2 = polar(R, -152), polar(R, -28)
    o.append(
        f'<path d="M {p1[0]:.1f} {p1[1]:.1f} A {R} {R} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}" '
        f'fill="none" stroke="{c["accent"]}" stroke-width="3.6" stroke-linecap="round"/>'
    )

    for x1, y1, x2, y2 in (
        (CX, CY - 18, CX, CY - 11),
        (CX, CY + 11, CX, CY + 18),
        (CX - 18, CY, CX - 11, CY),
        (CX + 11, CY, CX + 18, CY),
    ):
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["accent"]}" stroke-width="1.3" opacity="0.6"/>')

    return "\n  ".join(o)


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Joshua — 做一些顺手、离线、不打扰的小工具">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{C['g1']}"/>
      <stop offset="100%" stop-color="{C['g2']}"/>
    </linearGradient>
    <radialGradient id="haze" cx="14%" cy="20%" r="62%">
      <stop offset="0%" stop-color="{C['glow']}" stop-opacity="0.09"/>
      <stop offset="100%" stop-color="{C['glow']}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="1.3" cy="1.3" r="1.3" fill="{C['dot']}"/>
    </pattern>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.5"/>
  <rect width="{W}" height="{H}" fill="url(#haze)"/>
  <circle cx="1108" cy="222" r="132" fill="none" stroke="{C['ring']}" stroke-width="1" opacity="0.4"/>
  <circle cx="1108" cy="222" r="90" fill="none" stroke="{C['ring']}" stroke-width="1" opacity="0.26"/>

  {lens(C)}

  <g font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif">
    <text x="276" y="110" font-size="56" font-weight="700" fill="{C['text']}" letter-spacing="-1.2">Joshua</text>
    <text x="278" y="148" font-size="21" fill="{C['sub']}">做一些顺手、离线、不打扰的小工具</text>
    <text x="278" y="186" font-size="14.5" fill="{C['mono']}">Windows 原生 · 纯前端 · Android 离线应用</text>
  </g>

  <text x="{W - 40}" y="236" text-anchor="end" font-family="'SFMono-Regular', Consolas, 'Liberation Mono', monospace" font-size="12.5" fill="{C['mono']}" opacity="0.85">github.com/Joshua-Zion</text>
</svg>
'''

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "banner.svg"), "w", encoding="utf-8") as f:
    f.write(svg)
print("ok")
