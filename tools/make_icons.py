"""Gera o logo (SVG) e todas as variações de favicon/ícones do site Everni.

Uso:  python3 tools/make_icons.py
Saída: docs/ (favicons na raiz) e docs/assets/img/ (logo).
Requer: Pillow e Playwright (Chromium) para rasterizar o SVG.
"""
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs"
IMG = ROOT / "assets" / "img"

# Geometria do símbolo (unidades do traçado original)
GREEN = [(28, 42), (91, 59), (91, 80), (28, 61)]
GREEN_R = [7.5, 0, 7.5, 0]
VTOP = [(40, 51.0), (91, 25.5), (91, 66)]
VTOP_R = [0, 11, 0]
VBOT = [(28, 54), (28, 84.8), (66, 66.9)]
VBOT_R = [0, 8.5, 0]
MARK_CX, MARK_CY, MARK_W = 59.5, 55.15, 63


def rounded(pts, radii):
    n = len(pts)
    d = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        r = radii[i]
        if r <= 0:
            d.append(p1)
            continue

        def unit(a, b):
            l = math.dist(a, b)
            return ((b[0] - a[0]) / l, (b[1] - a[1]) / l)

        u1, u2 = unit(p1, p0), unit(p1, p2)
        ang = math.acos(max(-1, min(1, u1[0] * u2[0] + u1[1] * u2[1])))
        t = r / math.tan(ang / 2)
        a = (p1[0] + u1[0] * t, p1[1] + u1[1] * t)
        b = (p1[0] + u2[0] * t, p1[1] + u2[1] * t)
        d.append(("Q", a, p1, b))
    out = []
    for item in d:
        if isinstance(item, tuple) and item and item[0] == "Q":
            _, a, c, b = item
            out.append(("L" if out else "M") + "%.2f %.2f" % a)
            out.append("Q%.2f %.2f %.2f %.2f" % (c[0], c[1], b[0], b[1]))
        else:
            out.append(("L" if out else "M") + "%.2f %.2f" % item)
    return " ".join(out) + " Z"


G, VT, VB = rounded(GREEN, GREEN_R), rounded(VTOP, VTOP_R), rounded(VBOT, VBOT_R)

GRADS = """
  <linearGradient id="vt" x1="91" y1="25" x2="55" y2="58" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#5A2DB8"/><stop offset=".65" stop-color="#4A22A8"/><stop offset="1" stop-color="#2E1470"/></linearGradient>
  <linearGradient id="vb" x1="30" y1="84" x2="48" y2="63" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#5329B2"/><stop offset=".55" stop-color="#4420A0"/><stop offset="1" stop-color="#25105E"/></linearGradient>
  <linearGradient id="gr" x1="28" y1="44" x2="91" y2="78" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#B9D976"/><stop offset=".5" stop-color="#ABCB68"/><stop offset="1" stop-color="#9CBD5B"/></linearGradient>"""

MARK = f'<path d="{VT}" fill="url(#vt)"/><path d="{VB}" fill="url(#vb)"/><path d="{G}" fill="url(#gr)"/>'

# 1) Logo transparente (header, rodapé, mockups)
LOGO = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="27 24.5 65 61.5" width="65" height="61.5" role="img" aria-label="Everni">
<defs>{GRADS}</defs>{MARK}</svg>"""

# 2) Logo com contorno claro (para fundos escuros, ex.: hero)
LOGO_LIGHT = LOGO


def app_icon(size=512, mark_ratio=0.86, rounded_corners=0.0):
    s = size
    scale = (s * mark_ratio) / MARK_W
    tx, ty = s / 2 - MARK_CX * scale, s / 2 - MARK_CY * scale
    rx = s * rounded_corners
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}">
<defs>
  <radialGradient id="bg" cx="50%" cy="46%" r="72%"><stop offset="0" stop-color="#2A1650"/><stop offset=".48" stop-color="#1A1426"/><stop offset="1" stop-color="#121212"/></radialGradient>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#6B3FE0" stop-opacity=".38"/><stop offset=".55" stop-color="#5205B2" stop-opacity=".12"/><stop offset="1" stop-color="#5205B2" stop-opacity="0"/></radialGradient>{GRADS}
</defs>
<rect width="{s}" height="{s}" rx="{rx:.1f}" fill="url(#bg)"/>
<circle cx="{s/2}" cy="{s/2}" r="{s*0.46:.1f}" fill="url(#glow)"/>
<g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.4f})">{MARK}</g>
</svg>"""


# Ícone monocromático (Safari pinned tab): apenas silhueta
PINNED = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="27 24.5 65 61.5"><path d="{VT}"/><path d="{VB}"/><path d="{G}"/></svg>"""


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    (IMG / "logo-everni.svg").write_text(LOGO)
    # favicon.svg: quadrado arredondado, símbolo grande para leitura em 16 px
    (ROOT / "favicon.svg").write_text(app_icon(64, 0.86, 0.22))
    (ROOT / "safari-pinned-tab.svg").write_text(PINNED)

    # (arquivo, tamanho, proporção do símbolo, cantos)
    rasters = [
        ("favicon-16x16.png", 16, 0.92, 0.0),
        ("favicon-32x32.png", 32, 0.90, 0.0),
        ("favicon-48x48.png", 48, 0.88, 0.0),
        ("apple-touch-icon.png", 180, 0.74, 0.0),   # iOS aplica a máscara; sem transparência
        ("android-chrome-192x192.png", 192, 0.76, 0.0),
        ("android-chrome-512x512.png", 512, 0.76, 0.0),
        ("maskable-icon-192x192.png", 192, 0.58, 0.0),  # zona segura de 80%
        ("maskable-icon-512x512.png", 512, 0.58, 0.0),
        ("mstile-150x150.png", 150, 0.62, 0.0),
    ]
    from playwright.sync_api import sync_playwright
    from PIL import Image

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for name, size, ratio, rc in rasters:
            big = 1024
            svg = app_icon(big, ratio, rc)
            pg.set_viewport_size({"width": big, "height": big})
            pg.set_content('<html><body style="margin:0">' + svg + "</body></html>")
            tmp = f"/tmp/_icon_{size}.png"
            pg.screenshot(path=tmp, clip={"x": 0, "y": 0, "width": big, "height": big})
            im = Image.open(tmp).convert("RGB").resize((size, size), Image.LANCZOS)
            im.save(ROOT / name, optimize=True)
        b.close()

    # favicon.ico multi-tamanho (16/32/48)
    ims = [Image.open(ROOT / f"favicon-{n}x{n}.png") for n in (48, 32, 16)]
    ims[0].save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=ims[1:])
    for f in sorted(ROOT.glob("*.png")) + [ROOT / "favicon.ico", ROOT / "favicon.svg"]:
        print(f.name, os.path.getsize(f))


if __name__ == "__main__":
    main()
