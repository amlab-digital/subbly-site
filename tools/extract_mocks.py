"""Extrai as 5 telas de exemplo (mockups) da seção "Como funciona" do canvas de design
e converte os estilos inline em classes CSS (para permitir uma CSP estrita, sem 'unsafe-inline').

Uso (só quando o design dos mockups mudar no canvas):
    python3 tools/extract_mocks.py Main.dc.html Main-EN.dc.html
Saída: tools/data/mocks_pt.json, tools/data/mocks_en.json, docs/assets/css/mocks.css
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
CSS_OUT = HERE / "data" / "mocks.css"

BLOBS = {
    "/_blob/95d1feebcb642efc3797f02d0155e942": "/assets/img/segmentos/cafe.png",
    "/_blob/8bcac59f38f97adb9bebbf622b429859": "/assets/img/logo-everni.svg",
}


def figures(path):
    s = Path(path).read_text()
    s = re.sub(r'<sc-if value="\{\{showSections\}\}".*?</sc-if>', "", s, flags=re.S)
    out = []
    for n in range(1, 6):
        i = s.index(f'id="painel-{n}"')
        f0 = s.index("<figure", i)
        f1 = s.index("</figure>", f0) + len("</figure>")
        fig = s[f0:f1]
        # conteúdo interno do figure (sem a tag <figure> e o figcaption)
        inner = fig[fig.index(">") + 1 : fig.rindex("<figcaption")]
        cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", fig, re.S).group(1)
        out.append((inner.strip(), cap.strip()))
    return out


def main(pt, en):
    styles = {}

    def cls_for(style):
        style = style.strip().rstrip(";")
        style = style.replace("'JetBrains Mono', ui-monospace, monospace", "var(--mono)")
        if style not in styles:
            styles[style] = f"mk{len(styles):03d}"
        return styles[style]

    def convert(html):
        for k, v in BLOBS.items():
            html = html.replace(k, v)

        def rep(m):
            tag_open = m.group(0)
            st = re.search(r' style="([^"]*)"', tag_open)
            if not st:
                return tag_open
            c = cls_for(st.group(1))
            tag_open = tag_open.replace(st.group(0), "")
            if ' class="' in tag_open:
                tag_open = tag_open.replace(' class="', f' class="{c} ', 1)
            else:
                tag_open = re.sub(r"^<([a-zA-Z0-9]+)", rf'<\1 class="{c}"', tag_open)
            return tag_open

        html = re.sub(r"<[a-zA-Z][^<>]*>", rep, html)
        # imagens dos mockups: dimensões explícitas + lazy
        html = re.sub(r"<img ", '<img loading="lazy" decoding="async" ', html)
        return html

    DATA.mkdir(exist_ok=True)
    for lang, path in (("pt", pt), ("en", en)):
        figs = [{"mock": convert(i), "caption": c} for i, c in figures(path)]
        (DATA / f"mocks_{lang}.json").write_text(json.dumps(figs, ensure_ascii=False, indent=1))
    css = ["/* Gerado por tools/extract_mocks.py — telas de exemplo da seção Como funciona */"]
    for st, c in styles.items():
        css.append(f".{c}{{{st}}}")
    CSS_OUT.write_text("\n".join(css) + "\n")
    print(len(styles), "classes")


if __name__ == "__main__":
    main(*sys.argv[1:3])
