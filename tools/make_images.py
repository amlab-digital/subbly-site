"""Converte as fotos para AVIF/WebP/JPEG responsivos e gera o fundo topográfico do CTA.

Uso:  python3 tools/make_images.py
Fonte: tools/src-img/*.jpg (originais exportados do canvas de design).
"""
import os
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "src-img"
OUT = HERE.parent / "docs" / "assets" / "img"

PHOTOS = {
    # nome de saída: (arquivo-fonte, larguras)
    "everest-violeta": ("everest-violeta.jpg", [640, 1024]),
    "escalada-violeta": ("escalada-violeta.jpg", [640, 1070]),
}


def photos():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (src, widths) in PHOTOS.items():
        im = Image.open(SRC / src).convert("RGB")
        for w in widths:
            h = round(im.height * w / im.width)
            r = im if w == im.width else im.resize((w, h), Image.LANCZOS)
            base = OUT / f"{name}-{w}"
            r.save(f"{base}.avif", quality=52, speed=4)
            r.save(f"{base}.webp", quality=74, method=6)
            r.save(f"{base}.jpg", quality=78, optimize=True, progressive=True)
            print(name, w, h, *(os.path.getsize(f"{base}.{e}") // 1024 for e in ("avif", "webp", "jpg")), "KB")


def topo_svg():
    """Curvas de nível (relevo) em lima para o fundo do CTA. Leve e vetorial."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(7)
    W, H = 1600, 900
    x = np.linspace(0, 1.78, 360)
    y = np.linspace(0, 1, 200)
    X, Y = np.meshgrid(x, y)
    Z = 1.2 * np.exp(-(((X - 1.25) / 0.34) ** 2 + ((Y - 0.42) / 0.30) ** 2))
    Z += 0.75 * np.exp(-(((X - 0.78) / 0.30) ** 2 + ((Y - 0.62) / 0.26) ** 2))
    Z += 0.45 * np.exp(-(((X - 1.62) / 0.22) ** 2 + ((Y - 0.85) / 0.25) ** 2))
    for _ in range(14):
        cx, cy, s, a = rng.uniform(0, 1.78), rng.uniform(0, 1), rng.uniform(0.08, 0.2), rng.uniform(-0.08, 0.1)
        Z += a * np.exp(-(((X - cx) / s) ** 2 + ((Y - cy) / s) ** 2))
    fig = plt.figure()
    cs = plt.contour(X, Y, Z, levels=np.linspace(0.06, 1.5, 22))
    paths = []
    for level_segs in cs.allsegs:
        for seg in level_segs:
            if len(seg) < 6:
                continue
            seg = seg[::2]
            pts = " ".join(f"{p[0] / 1.78 * W:.0f},{(1 - p[1]) * H:.0f}" for p in seg)
            paths.append(f'<polyline points="{pts}"/>')
    plt.close(fig)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
        f'<rect width="{W}" height="{H}" fill="#B4EC3C"/>'
        f'<g fill="none" stroke="#5E8F00" stroke-opacity=".32" stroke-width="1.4" stroke-linejoin="round">{"".join(paths)}</g></svg>'
    )
    (OUT / "relevo-lima.svg").write_text(svg)
    print("relevo-lima.svg", len(svg) // 1024, "KB")


if __name__ == "__main__":
    photos()
    topo_svg()
