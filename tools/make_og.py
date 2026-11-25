"""Gera as imagens de compartilhamento (Open Graph / Twitter) 1200x630 em PT e EN.
Uso: python3 tools/make_og.py   (requer Playwright)
"""
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent / "docs"
BG = (DOCS / "assets/img/everest-violeta-1024.jpg").as_uri()
LOGO = (DOCS / "assets/img/logo-everni.svg").as_uri()
FONT = (DOCS / "assets/fonts/montserrat-var-latin.woff2").as_uri()

TEXT = {
    "pt": ("Receita Recorrente", "em uma só plataforma.", "App de assinaturas nativo da Shopify · feito no Brasil", "Sem mensalidade · 1% do GMV"),
    "en": ("Every subscription.", "One platform.", "Native subscriptions app for Shopify", "No monthly fee · flat 1% of GMV"),
}

TPL = """<!DOCTYPE html><html><head><style>
@font-face{{font-family:M;src:url({font}) format('woff2');font-weight:300 600}}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;font-family:M,Montserrat,sans-serif;color:#FEFEFE;background:#1A1240}}
.bg{{position:absolute;inset:0;background:url({bg}) center 30%/cover}}
.sh{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(16,11,38,.94) 0%,rgba(16,11,38,.78) 48%,rgba(16,11,38,.15) 100%)}}
.in{{position:absolute;inset:0;padding:64px 72px;display:flex;flex-direction:column;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:16px}}
.brand img{{width:56px}}
.brand span{{font-size:28px;font-weight:500;letter-spacing:.42em}}
h1{{font-size:68px;line-height:1.05;font-weight:500;letter-spacing:-.02em}}
h1 b{{display:block;color:#99E604;font-weight:500}}
p{{font-size:26px;line-height:1.4;color:#E4E0F0;margin-top:22px;font-weight:500}}
.foot{{display:flex;justify-content:space-between;align-items:center;font-size:20px;letter-spacing:.12em;text-transform:uppercase;color:#C9C2E6}}
.foot strong{{color:#99E604;font-weight:600;letter-spacing:.04em;text-transform:none;font-size:22px}}
</style></head><body><div class="bg"></div><div class="sh"></div><div class="in">
<div class="brand"><img src="{logo}" alt=""><span>EVERNI</span></div>
<div><h1>{a}<b>{b}</b></h1><p>{c}</p></div>
<div class="foot"><span>{d}</span><strong>geteverni.com</strong></div>
</div></body></html>"""


def main():
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1200, "height": 630})
        for lang, (a, b, c, d) in TEXT.items():
            html = TPL.format(font=FONT, bg=BG, logo=LOGO, a=a, b=b, c=c, d=d)
            tmp = HERE / f"_og_{lang}.html"
            tmp.write_text(html)
            pg.goto(tmp.as_uri())
            pg.wait_for_timeout(300)
            pg.screenshot(path=f"/tmp/og_{lang}.png")
            tmp.unlink()
            Image.open(f"/tmp/og_{lang}.png").convert("RGB").save(DOCS / f"assets/img/og-{lang}.jpg", quality=84, optimize=True, progressive=True)
        br.close()
    print("ok")


if __name__ == "__main__":
    main()
