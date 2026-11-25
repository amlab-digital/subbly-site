# -*- coding: utf-8 -*-
"""Gera o site estático da Everni em docs/ (raiz publicada pelo GitHub Pages).

Uso:  python3 tools/build.py
Edite textos em tools/content_home.py e tools/content_pages.py, preços em PRICING abaixo.
"""
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

from content_home import HOME
from content_pages import ABOUT, COMPANY, PRIVACY, PRIVACY_COOKIES_GTM, TERMS, UPDATED

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent / "docs"

# =============================================================================
# CONFIGURAÇÃO GERAL — tudo que muda com frequência está aqui
# =============================================================================
SITE = "https://geteverni.com"
# Data da última alteração de conteúdo da home (sitemap, dateModified, llms-full.txt)
SITE_UPDATED = "2026-11-25"
EMAIL = "contato@amlab.com.br"
PHONE = "+55 11 95506-1996"  # WhatsApp Business da Everni
INSTALL = {"pt": "https://apps.shopify.com/subbly-subscriptions-app?locale=pt-BR",
           "en": "https://apps.shopify.com/subbly-subscriptions-app?locale=en"}
WHATSAPP = {"pt": "https://wa.me/5511955061996?text=Ol%C3%A1%2C%20Gostaria%20de%20saber%20como%20posso%20gerenciar%20melhor%20minhas%20assinaturas%20com%20a%20EVERNI.",
            "en": "https://wa.me/5511955061996?text=Hi%2C%20I%27d%20like%20to%20learn%20how%20Everni%20can%20help%20me%20manage%20my%20subscriptions."}
LINKEDIN = "https://www.linkedin.com/company/everni-official/"
AMLAB = "https://amlab.com.br"
# Formulário de novidades: crie um formulário grátis em https://formspree.io e troque SEU_FORM_ID.
# Enquanto não trocar, o botão abre o app de e-mail do visitante (fallback automático).
FORM_ENDPOINT = "https://formspree.io/f/SEU_FORM_ID"

# GOOGLE TAG MANAGER — cole o ID do container (ex.: "GTM-ABC1234") e rode o build.
# Vazio = nenhum script de medição é carregado e a Política de Privacidade continua dizendo que o site não usa cookies.
# Preenchido = carrega o GTM com Consent Mode v2 (negado por padrão na UE/Reino Unido/Suíça), libera os domínios do Google
# na CSP e troca a seção de cookies da Política de Privacidade pelo texto de medição (revise com o jurídico).
GTM_ID = ""

# PREÇOS — plano único Growth (taxa sobre o GMV mensal de assinaturas) + Enterprise sob consulta.
# Mudou a taxa? Troque "rate": hero, tabela comparativa, FAQ, JSON-LD, calculadora, montanha e llms.txt acompanham.
PRICING = [
    {"name": "Growth", "rate": 0.01, "max": None},
]
# Calculadora: degraus do controle deslizante (GMV mensal em USD), posição inicial e tickets
CALC_STEPS = [5000, 10000, 20000, 30000, 40000, 50000, 75000, 100000, 150000, 200000, 300000, 400000, 500000,
              750000, 1000000, 1500000, 2000000, 2500000, 3000000, 5000000, 7500000, 10000000]
CALC_START, CALC_TICKETS, CALC_TICKET_START = 5, [25, 40, 60], 40

ROUTES = {
    "home": {"pt": "/", "en": "/en/"},
    "about": {"pt": "/sobre-nos/", "en": "/en/about/"},
    "terms": {"pt": "/termos-de-uso/", "en": "/en/terms-of-use/"},
    "privacy": {"pt": "/politica-de-privacidade/", "en": "/en/privacy-policy/"},
}
LOCALE = {"pt": "pt-BR", "en": "en"}
OG_LOCALE = {"pt": "pt_BR", "en": "en_US"}

def csp():
    gtm = bool(GTM_ID)
    g_script = " https://www.googletagmanager.com" if gtm else ""
    g_img = " https://www.googletagmanager.com https://*.google-analytics.com https://*.g.doubleclick.net https://*.google.com" if gtm else ""
    g_conn = " https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com https://*.g.doubleclick.net" if gtm else ""
    g_frame = "frame-src https://www.googletagmanager.com; " if gtm else ""
    return ("default-src 'self'; script-src 'self'" + g_script + "; style-src 'self'; img-src 'self' data:" + g_img + "; font-src 'self'; "
            "connect-src 'self' https://api.country.is https://ipapi.co https://formspree.io" + g_conn + "; " + g_frame +
            "form-action 'self' https://formspree.io; base-uri 'self'; object-src 'none'; manifest-src 'self'; "
            "upgrade-insecure-requests")

UI = {
    "pt": {"skip": "Pular para o conteúdo", "home_label": "Everni, página inicial", "nav_label": "Principal",
           "menu": "Menu", "lang_label": "Idioma", "install": "Instalar", "install_full": "Instalar na Shopify",
           "other_lang_aria": "English version", "home": "Início", "updated": "Última atualização",
           "docs_label": "Documentos legais", "breadcrumb": "Você está aqui", "demo": "Agendar demo",
           "nav": [("Como funciona", "product"), ("Para quem é", "who"), ("Quanto custa", "calc"), ("Integrações", "integrations"),
                   ("Migração", "migration"), ("Preços", "pricing"), ("FAQ", "faq")],
           "footer": {"tag": "Subscription platform", "blurb": "Assinaturas na Shopify, sem mensalidade e com provedores de pagamento locais.",
                      "label": "Rodapé", "platform": "Plataforma",
                      "platform_links": ["Planos de assinatura", "Cobrança recorrente", "Retenção", "Portal do assinante", "Relatórios"],
                      "company": "Empresa", "about": "Sobre nós", "pricing": "Preços", "partners": "Parceiros", "contact": "Contato",
                      "dev": "Desenvolvedores", "dev_item": "API, webhooks e documentação", "soon": "em breve",
                      "support": "Atendimento", "faq": "Perguntas frequentes", "terms": "Termos de uso", "privacy": "Política de privacidade",
                      "here": "Brasil · Português", "other": "English", "copy": "© 2026 Everni · Nativo da Shopify"},
           "announce": "Aviso"},
    "en": {"skip": "Skip to content", "home_label": "Everni, home page", "nav_label": "Main",
           "menu": "Menu", "lang_label": "Language", "install": "Install", "install_full": "Install on Shopify",
           "other_lang_aria": "Versão em português", "home": "Home", "updated": "Last updated",
           "docs_label": "Legal documents", "breadcrumb": "You are here", "demo": "Book a demo",
           "nav": [("How it works", "product"), ("Who it’s for", "who"), ("Savings", "calc"), ("Integrations", "integrations"),
                   ("Migration", "migration"), ("Pricing", "pricing"), ("FAQ", "faq")],
           "footer": {"tag": "Subscription platform", "blurb": "Subscriptions for Shopify brands. No monthly fee, local payment providers.",
                      "label": "Footer", "platform": "Platform",
                      "platform_links": ["Subscription plans", "Recurring billing", "Retention", "Subscriber portal", "Reports"],
                      "company": "Company", "about": "About", "pricing": "Pricing", "partners": "Partners", "contact": "Contact",
                      "dev": "Developers", "dev_item": "API, webhooks and docs", "soon": "soon",
                      "support": "Support", "faq": "Frequently asked questions", "terms": "Terms of use", "privacy": "Privacy policy",
                      "here": "Worldwide · English", "other": "Português", "copy": "© 2026 Everni · Built for Shopify"},
           "announce": "Announcement"},
}

# =============================================================================
# Utilitários
# =============================================================================
e = lambda s: html.escape(str(s), quote=True)
OTHER = {"pt": "en", "en": "pt"}


def num(n, lang):
    s = f"{round(n):,}"
    return s.replace(",", ".") if lang == "pt" else s


def pct(rate, lang):
    s = f"{rate * 100:.2f}".rstrip("0").rstrip(".") + "%"
    return s.replace(".", ",") if lang == "pt" else s


def money_short(v, lang):
    if lang == "pt":
        if v >= 1e6:
            return "US$ " + (f"{v / 1e6:.1f}".rstrip("0").rstrip(".")).replace(".", ",") + " mi"
        return "US$ " + f"{v / 1e3:.0f}" + " mil"
    if v >= 1e6:
        return "$" + f"{v / 1e6:.1f}".rstrip("0").rstrip(".") + "M"
    return "$" + f"{v / 1e3:.0f}" + "K"


def money(v, lang):
    return ("US$ " if lang == "pt" else "$") + num(v, lang)


def tier_for(gmv):
    for t in PRICING:
        if t["max"] is None or gmv <= t["max"]:
            return t
    return PRICING[-1]


def price_vars(lang):
    """Variáveis de preço usadas nos textos: {rate} = taxa do plano Growth."""
    return {"rate": pct(PRICING[0]["rate"], lang)}


def fill_price(s, lang):
    return s.format(**price_vars(lang))


def url(lang, key, anchor=None):
    u = ROUTES[key][lang]
    return u + ("#" + anchor if anchor else "")


def abs_url(path):
    return SITE + path


def asset_version():
    h = hashlib.sha1()
    for p in sorted((DOCS / "assets").rglob("*")):
        if p.is_file() and p.suffix in (".css", ".js"):
            h.update(p.read_bytes())
    return h.hexdigest()[:10]


GLOBE = '<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'
FLAG_BR = '<svg role="img" aria-label="Brasil" width="30" height="21" viewBox="0 0 30 21"><rect width="30" height="21" rx="3" fill="#009C3B"/><path d="M15 2.6 27 10.5 15 18.4 3 10.5Z" fill="#FFDF00"/><circle cx="15" cy="10.5" r="4.6" fill="#002776"/><path d="M10.6 9.6c2.9-.6 6-.2 8.7 1.2" stroke="#FFFFFF" stroke-width="0.9" fill="none"/></svg>'


def ext_link(href, text, cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{e(href)}" target="_blank" rel="noopener"{extra}>{text}</a>'


# =============================================================================
# JSON-LD (dados estruturados)
# =============================================================================
def org_ld():
    return {
        "@type": "Organization", "@id": SITE + "/#org", "name": "Everni", "url": SITE + "/",
        "legalName": COMPANY["legal_name"], "taxID": COMPANY["cnpj"],
        "logo": {"@type": "ImageObject", "url": SITE + "/android-chrome-512x512.png", "width": 512, "height": 512},
        "image": SITE + "/assets/img/og-pt.jpg",
        "email": EMAIL, "telephone": PHONE, "foundingDate": "2026",
        "address": {"@type": "PostalAddress", "streetAddress": COMPANY["street"], "addressLocality": COMPANY["city"],
                    "addressRegion": COMPANY["region"], "postalCode": COMPANY["zip"], "addressCountry": COMPANY["country"]},
        "contactPoint": [{"@type": "ContactPoint", "contactType": "customer support", "email": EMAIL, "telephone": PHONE,
                          "availableLanguage": ["Portuguese", "English"], "areaServed": "Worldwide"}],
        "sameAs": [LINKEDIN],
        "brand": {"@type": "Brand", "name": "Everni"},
        "parentOrganization": {"@type": "Organization", "name": "AM Lab", "url": AMLAB},
    }


def website_ld():
    return {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Everni",
            "alternateName": "Everni Subscriptions", "inLanguage": ["pt-BR", "en"], "publisher": {"@id": SITE + "/#org"}}


def app_ld(lang):
    c = HOME[lang]
    rate = price_vars(lang)["rate"]
    pr = c["pricing"]
    offer_desc = (f"Instalação gratuita. Plano Growth: {rate} do GMV mensal de assinaturas, sem mensalidade e sem taxa por pedido, cobrado em USD pela Shopify. "
                  "Plano Enterprise com condições negociadas para operações de alto volume." if lang == "pt" else
                  f"Free to install. Growth plan: {rate} of monthly subscription GMV, no monthly fee and no per-order fee, billed in USD through Shopify. "
                  "Enterprise plan with negotiated rates for high-volume brands.")
    return {
        "@type": "SoftwareApplication", "@id": SITE + ROUTES["home"][lang] + "#app", "name": "Everni",
        "applicationCategory": "BusinessApplication", "applicationSubCategory": "Subscription management",
        "operatingSystem": "Web (Shopify Admin)", "url": SITE + ROUTES["home"][lang], "installUrl": INSTALL[lang],
        "description": c["description"], "inLanguage": LOCALE[lang], "publisher": {"@id": SITE + "/#org"},
        "image": SITE + f"/assets/img/og-{lang}.jpg",
        "featureList": pr["growth"]["features"] + pr["growth"]["service"],
        "audience": {"@type": "BusinessAudience", "audienceType": "Shopify merchants (DNVBs, B2C, D2C and B2B)"},
        "offers": {"@type": "Offer", "name": pr["growth"]["name"], "price": "0", "priceCurrency": "USD",
                   "availability": "https://schema.org/InStock", "url": INSTALL[lang], "description": offer_desc},
    }


def faq_ld(lang):
    return {"@type": "FAQPage", "@id": SITE + ROUTES["home"][lang] + "#faq-ld", "inLanguage": LOCALE[lang],
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": fill_price(a, lang)}} for q, a in HOME[lang]["faq"]["items"]]}


def breadcrumb_ld(lang, key, name):
    return {"@type": "BreadcrumbList", "@id": SITE + ROUTES[key][lang] + "#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": UI[lang]["home"], "item": SITE + ROUTES["home"][lang]},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + ROUTES[key][lang]}]}


def webpage_ld(lang, key, title, desc, ptype="WebPage", crumb=None):
    d = {"@type": ptype, "@id": SITE + ROUTES[key][lang] + "#webpage", "url": SITE + ROUTES[key][lang], "name": title,
         "description": desc, "inLanguage": LOCALE[lang], "isPartOf": {"@id": SITE + "/#website"},
         "about": {"@id": SITE + ROUTES["home"][lang] + "#app"}, "publisher": {"@id": SITE + "/#org"},
         "dateModified": SITE_UPDATED if key == "home" else UPDATED["iso"], "primaryImageOfPage": SITE + f"/assets/img/og-{lang}.jpg"}
    if crumb:
        d["breadcrumb"] = {"@id": SITE + ROUTES[key][lang] + "#breadcrumb"}
    return d


def ld_script(graph):
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f'<script type="application/ld+json">\n{data}\n</script>'


# =============================================================================
# Layout: <head>, header, footer
# =============================================================================
def head(lang, key, title, desc, graph, preload="", robots="index, follow, max-image-preview:large, max-snippet:-1"):
    v = asset_version()
    canon = abs_url(ROUTES[key][lang]) if key else None
    alts = ""
    if key:
        alts = (f'<link rel="alternate" hreflang="pt-BR" href="{abs_url(ROUTES[key]["pt"])}">\n'
                f'<link rel="alternate" hreflang="en" href="{abs_url(ROUTES[key]["en"])}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{abs_url(ROUTES[key]["en"])}">')
    og_img = abs_url(f"/assets/img/og-{lang}.jpg")
    og_alt = "Everni · " + (HOME[lang]["hero"]["h1a"] + " " + HOME[lang]["hero"]["h1b"])
    return f"""<!DOCTYPE html>
<html lang="{LOCALE[lang]}" data-lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="{csp()}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
{f'<link rel="canonical" href="{canon}">' if canon else ''}
{alts}
<meta name="theme-color" content="#181818">
<meta name="color-scheme" content="light">
<meta name="format-detection" content="telephone=no">
<meta name="author" content="Everni">
<meta name="application-name" content="Everni">
<meta name="apple-mobile-web-app-title" content="Everni">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Everni">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:locale:alternate" content="{OG_LOCALE[OTHER[lang]]}">
{f'<meta property="og:url" content="{canon}">' if canon else ''}
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/favicon-16x16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5205B2">
<link rel="manifest" href="/site.webmanifest">
<meta name="msapplication-TileColor" content="#181818">
<meta name="msapplication-config" content="/browserconfig.xml">
<link rel="preload" href="/assets/fonts/montserrat-var-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}
<link rel="stylesheet" href="/assets/css/everni.css?v={v}">
{gtm_head()}<script src="/assets/js/lang.js?v={v}"></script>
<script src="/assets/js/site.js?v={v}" defer></script>
{ld_script(graph)}
</head>"""


def gtm_head():
    """Carrega o Google Tag Manager (com Consent Mode v2) só quando GTM_ID estiver preenchido."""
    if not GTM_ID:
        return ""
    return (f'<link rel="preconnect" href="https://www.googletagmanager.com">\n'
            f'<script src="/assets/js/gtm.js?v={asset_version()}" data-gtm-id="{e(GTM_ID)}"></script>\n')


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={e(GTM_ID)}" height="0" width="0" '
            f'hidden title="Google Tag Manager"></iframe></noscript>\n')


def header(lang, key):
    t = UI[lang]
    on_home = key == "home"
    ids = HOME[lang]["ids"]
    base = "" if on_home else ROUTES["home"][lang]
    nav = "".join(f'<li><a href="{base}#{ids[k]}">{e(lbl)}</a></li>' for lbl, k in t["nav"])
    other = OTHER[lang]
    alt_href = ROUTES[key][other] if key else ROUTES["home"][other]
    cur_lbl, oth_lbl = ("PT", "EN") if lang == "pt" else ("EN", "PT")
    cur = f'<span aria-current="true" lang="{LOCALE[lang]}">{cur_lbl}</span>'
    oth = f'<a href="{alt_href}" hreflang="{LOCALE[other]}" lang="{LOCALE[other]}" data-set-lang="{other}">{oth_lbl}<span class="visually-hidden"> · {e(t["other_lang_aria"])}</span></a>'
    switch = (cur + oth) if lang == "pt" else (oth + cur)
    tb_text, tb_link, tb_key = HOME[lang]["topbar"]
    return f"""<a class="skip-link" href="#conteudo">{t['skip']}</a>
<div class="topbar" role="region" aria-label="{t['announce']}"><div class="wrap topbar__in"><span>{e(tb_text)}</span><a href="{base}#{ids[tb_key]}">{e(tb_link)}</a></div></div>
<header class="site-header">
<div class="wrap site-header__in">
<a class="brand" href="{ROUTES['home'][lang]}" aria-label="{t['home_label']}"{' aria-current="page"' if on_home else ''}><img src="/assets/img/logo-everni.svg" alt="" width="34" height="32"><span class="brand__name" aria-hidden="true">EVERNI</span></a>
<nav id="site-nav" class="site-nav" aria-label="{t['nav_label']}">
<ul>{nav}</ul>
<a class="btn btn--dark btn--block site-nav__cta" href="{INSTALL[lang]}" target="_blank" rel="noopener">{t['install_full']}</a>
<a class="btn btn--outline btn--block site-nav__cta" href="{WHATSAPP[lang]}" target="_blank" rel="noopener" data-track="demo">{t['demo']}</a>
</nav>
<div class="header-actions">
<nav class="lang-switch" aria-label="{t['lang_label']}">{switch}</nav>
<a class="btn btn--dark header-cta" href="{INSTALL[lang]}" target="_blank" rel="noopener">{t['install']}</a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="visually-hidden">{t['menu']}</span><span class="menu-toggle__bars" aria-hidden="true"></span></button>
</div>
</div>
</header>"""


def footer(lang, key):
    t = UI[lang]["footer"]
    ids, pids = HOME[lang]["ids"], HOME[lang]["panel_ids"]
    home = ROUTES["home"][lang] if key != "home" else ""
    plat = "".join(f'<li><a href="{home}#{pid}">{e(lbl)}</a></li>' for lbl, pid in zip(t["platform_links"], pids))
    cur = ' aria-current="page"'
    other = OTHER[lang]
    alt_href = ROUTES[key][other] if key else ROUTES["home"][other]
    return f"""<footer class="site-footer">
<div class="wrap site-footer__in">
<div class="footer-top">
<div class="footer-brand">
<a class="brand" href="{ROUTES['home'][lang]}" aria-label="{UI[lang]['home_label']}"><img src="/assets/img/logo-everni.svg" alt="" width="34" height="32" loading="lazy"><span class="brand__name" aria-hidden="true">EVERNI</span></a>
<p class="tag">{t['tag']}</p>
<p>{e(t['blurb'])}</p>
</div>
<nav class="footer-nav" aria-label="{t['label']}">
<div><h2>{t['platform']}</h2><ul>{plat}</ul></div>
<div><h2>{t['company']}</h2><ul><li><a href="{ROUTES['about'][lang]}"{cur if key == 'about' else ''}>{t['about']}</a></li><li><a href="{home}#{ids['pricing']}">{t['pricing']}</a></li><li><a href="{home}#{ids['integrations']}">{t['partners']}</a></li><li><a href="{home}#{ids['contact']}">{t['contact']}</a></li></ul></div>
<div><h2>{t['dev']}</h2><ul><li><span class="soon">{t['dev_item']} <span class="badge">{t['soon']}</span></span></li></ul></div>
<div><h2>{t['support']}</h2><ul><li><a href="{home}#{ids['faq']}">{t['faq']}</a></li><li><a href="{ROUTES['terms'][lang]}"{cur if key == 'terms' else ''}>{t['terms']}</a></li><li><a href="{ROUTES['privacy'][lang]}"{cur if key == 'privacy' else ''}>{t['privacy']}</a></li></ul></div>
</nav>
</div>
<div class="footer-bottom">
<div class="langs"><span>{GLOBE}{t['here']}</span><a href="{alt_href}" hreflang="{LOCALE[other]}" lang="{LOCALE[other]}" data-set-lang="{other}">{t['other']}</a></div>
<div class="social">{ext_link(LINKEDIN, 'LinkedIn')}</div>
<span>{t['copy']}</span>
</div>
<p class="footer-legal">{COMPANY['legal_name']} · CNPJ {COMPANY['cnpj']} · {COMPANY['street']}, {COMPANY['city']}/{COMPANY['region']} · CEP {COMPANY['zip']} · <a href="mailto:{EMAIL}" class="link-plain">{EMAIL}</a></p>
</div>
</footer>"""


def page(lang, key, title, desc, graph, main_html, preload="", robots=None):
    h = head(lang, key, title, desc, graph, preload, **({"robots": robots} if robots else {}))
    return f"""{h}
<body>
{gtm_body()}{header(lang, key)}
<main id="conteudo" tabindex="-1">
{main_html}
</main>
{footer(lang, key)}
</body>
</html>
"""


def breadcrumb(lang, name):
    return (f'<nav class="breadcrumb" aria-label="{UI[lang]["breadcrumb"]}"><ol>'
            f'<li><a href="{ROUTES["home"][lang]}">{UI[lang]["home"]}</a></li>'
            f'<li><span aria-current="page">{e(name)}</span></li></ol></nav>')


def picture(name, widths, alt, cls="", sizes="100vw", loading="lazy", fetchpriority=None, w=None, h=None):
    srcset = lambda ext: ", ".join(f"/assets/img/{name}-{x}.{ext} {x}w" for x in widths)
    big = widths[-1]
    fp = f' fetchpriority="{fetchpriority}"' if fetchpriority else ""
    ld = f' loading="{loading}"' if loading else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img{c} src="/assets/img/{name}-{big}.jpg" srcset="{srcset("jpg")}" sizes="{sizes}" alt="{e(alt)}" width="{w}" height="{h}"{ld}{fp} decoding="async"></picture>')


# =============================================================================
# HOME — seções
# =============================================================================
def sec_head(eyebrow, h2, hid, lead=None):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    eb = f'<p class="eyebrow">{e(eyebrow)}</p>' if eyebrow else ""
    return f'<div class="sec-head reveal">{eb}<h2 class="h2" id="{hid}">{e(h2)}</h2>{lead_html}</div>'


def s_hero(lang, c):
    hh = c["hero"]
    ids = c["ids"]
    flag = FLAG_BR if hh["flag"] else ""
    strip = "".join(f'<span class="brand-name">{e(x)}</span>' for x in hh["strip"])
    pic = picture("everest-violeta", [1024], hh["img_alt"], loading=None, fetchpriority="high", w=1024, h=682)
    return f"""<section class="hero on-dark" id="{ids['top']}" aria-labelledby="hero-titulo">
<div class="hero__media parallax"><div class="hero__frame">{pic}</div></div>
<div class="hero__shade" aria-hidden="true"></div>
<div class="hero__content">
<h1 id="hero-titulo">{e(hh['h1a'])}<span>{e(hh['h1b'])}</span></h1>
<p class="hero__sub"><span>{e(hh['sub'])}</span>{flag}<span class="soft">{e(hh['sub2'])}</span></p>
<div class="hero__ctas"><a class="btn btn--lime btn--pill" href="{INSTALL[lang]}" target="_blank" rel="noopener">{e(hh['cta1'])}</a><a class="btn btn--ghost btn--pill" href="#{ids['calc']}">{e(hh['cta2'])}</a></div>
</div>
<div class="hero__strip"><div class="wrap"><span class="label">{e(hh['strip_label'])}</span>{strip}</div></div>
</section>"""


def s_relationship(lang, c):
    r = c["relationship"]
    return f"""<section class="section rel" id="{c['ids']['relationship']}" aria-labelledby="relacao-titulo">
<div class="wrap rel__grid reveal"><h2 class="rel__h" id="relacao-titulo">{e(r['h2'])}</h2><p class="rel__p">{e(r['p'])}</p></div>
</section>"""


ICON_X = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>'
ICON_OK = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'


def s_problem(lang, c):
    """Quadro comparativo 'Hoje x Com a Everni' como <table> semântica (vira cartões no celular)."""
    p = c["problem"]
    c1, c2, c3 = p["cols"]
    rows = "".join(
        f'<tr class="reveal"><th scope="row">{e(topic)}</th>'
        f'<td class="cmp__today" data-label="{e(c2)}"><span class="cmp__ico" aria-hidden="true">{ICON_X}</span><div><span class="cmp__lbl" aria-hidden="true">{e(c2)}</span><p>{e(today)}</p></div></td>'
        f'<td class="cmp__ev" data-label="{e(c3)}"><span class="cmp__ico" aria-hidden="true">{ICON_OK}</span><div><span class="cmp__lbl" aria-hidden="true">{e(c3)}</span><p>{e(fill_price(ev, lang))}</p></div></td></tr>'
        for topic, today, ev in p["rows"])
    return f"""<section class="section section--line cmp-sec" id="{c['ids']['problem']}" aria-labelledby="problema-titulo">
<div class="wrap">
<h2 class="visually-hidden" id="problema-titulo">{e(p['h2'])}</h2>
<table class="cmp">
<caption class="visually-hidden">{e(p['caption'])}</caption>
<thead><tr><th scope="col">{e(c1)}</th><th scope="col">{e(c2)}</th><th scope="col" class="cmp__ev-head"><img src="/assets/img/logo-everni.svg" alt="" width="30" height="28">{e(c3)}</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<p class="closing reveal">{e(p['closing'])} <a class="link-u" href="#{c['ids']['product']}">{e(p['closing_link'])}</a></p>
</div></section>"""


def s_who(lang, c):
    w = c["who"]
    def seg(s, dup=False):
        slug, h, t, alt = s
        a = ' aria-hidden="true"' if dup else ""
        img = (f'<picture><source type="image/webp" srcset="/assets/img/segmentos/{slug}.webp">'
               f'<img src="/assets/img/segmentos/{slug}.png" alt="{"" if dup else e(alt)}" width="400" height="370" loading="lazy" decoding="async"></picture>')
        return f'<li class="seg{" seg--dup" if dup else ""}"{a}>{img}<h3>{e(h)}</h3><p>{e(t)}</p></li>'
    items = "".join(seg(s) for s in w["segments"]) + "".join(seg(s, True) for s in w["segments"])
    return f"""<section class="section section--line" id="{c['ids']['who']}" aria-labelledby="para-quem-titulo">
<div class="wrap">{sec_head(w['eyebrow'], w['h2'], 'para-quem-titulo', e(w['lead']))}</div>
<div class="marquee reveal" tabindex="0" role="region" aria-label="{e(w['region'])}"><ul class="marquee__track" role="list">{items}</ul></div>
</section>"""


def calc_default(lang, c):
    gmv = CALC_STEPS[CALC_START]
    orders = round(gmv / CALC_TICKET_START)
    t = tier_for(gmv)
    ev = gmv * t["rate"]
    comps = [{"name": x["name"], "formula": x["formula"], "cost": x["fixed"] + gmv * x["pct"] + orders * x["perOrder"], "ev": False}
             for x in c["calc"]["competitors"]]
    js = c["calc"]["js"]
    rows = comps + [{"name": "Everni", "formula": js["everniFormula"].replace("{rate}", pct(t["rate"], lang)), "cost": ev, "ev": True}]
    rows.sort(key=lambda r: -r["cost"])
    mx = rows[0]["cost"]
    costs = [x["cost"] for x in comps]
    smin, smax = (min(costs) - ev) * 12, (max(costs) - ev) * 12
    save = (js["cur"] + num(smin, lang) + js["to"] + js["cur2"] + num(smax, lang)) if smin > 0 else js["upTo"] + js["cur"] + num(smax, lang)
    pcts = f"{round((1 - ev / min(costs)) * 100)}%{js['pctTo']}{round((1 - ev / max(costs)) * 100)}%"
    rows_html = "".join(
        f'<li class="row{" row--everni" if r["ev"] else ""}"><div class="row__top"><div><p class="row__name">{e(r["name"])}</p><p class="row__formula">{e(r["formula"])}</p></div>'
        f'<span class="row__cost">{js["cur"]}{num(r["cost"], lang)}{js["perMonth"]}</span></div><div class="row__track"><div class="row__bar" data-w="{max(2, round(r["cost"] / mx * 1000) / 10)}"></div></div></li>'
        for r in rows)
    return {"gmv": js["cur"] + num(gmv, lang), "orders": num(orders, lang), "save": save, "pct": pcts,
            "tier": t["name"], "rate": pct(t["rate"], lang), "rows": rows_html}


def s_calc(lang, c):
    k = c["calc"]
    d = calc_default(lang, c)
    cfg = {"locale": LOCALE[lang], "steps": CALC_STEPS, "t": k["js"], "competitors": k["competitors"],
           "tiers": [{"name": t["name"], "rate": t["rate"], "max": t["max"], "label": pct(t["rate"], lang)} for t in PRICING]}
    chips = "".join(f'<button type="button" class="chip" data-v="{v}" aria-pressed="{"true" if v == CALC_TICKET_START else "false"}">{k["js"]["cur"]}{v}</button>' for v in CALC_TICKETS)
    note = e(k["save_note"]).replace("{pct}", f'<span id="calc-pct">{d["pct"]}</span>').replace("{rate}", f'<span id="calc-rate">{d["rate"]}</span>')
    return f"""<section class="section section--sand section--line" id="{c['ids']['calc']}" aria-labelledby="calc-titulo">
<div class="wrap">{sec_head(k['eyebrow'], k['h2'], 'calc-titulo', e(k['lead']))}
<div class="calc reveal" id="calc" data-config="{e(json.dumps(cfg, ensure_ascii=False))}">
<div class="calc__panel">
<div class="calc__field"><label class="calc__label" for="calc-gmv">{e(k['gmv_label'])}</label>
<output class="calc__big" id="calc-gmv-out" for="calc-gmv" aria-live="polite">{d['gmv']}</output>
<input id="calc-gmv" type="range" min="0" max="{len(CALC_STEPS) - 1}" step="1" value="{CALC_START}" aria-valuetext="{d['gmv']}">
<div class="calc__scale" aria-hidden="true"><span>{k['scale'][0]}</span><span>{k['scale'][1]}</span></div></div>
<div class="calc__field"><span class="calc__label" id="calc-ticket-label">{e(k['ticket_label'])}</span>
<div class="chips" role="group" aria-labelledby="calc-ticket-label">{chips}</div>
<p class="calc__note">≈ <span id="calc-orders">{d['orders']}</span> {e(k['orders'])}</p></div>
<div class="calc__save" aria-live="polite"><span class="calc__label">{e(k['save_label'])}</span><span class="calc__big calc__big--violet" id="calc-save">{d['save']}</span><p class="calc__note">{note}</p></div>
<a class="btn btn--dark" href="{INSTALL[lang]}" target="_blank" rel="noopener">{e(k['cta'])}</a>
</div>
<div class="calc__panel"><h3 class="calc__label" id="calc-rows-label">{e(k['rows_label'])}</h3>
<ol class="rows" id="calc-rows" aria-labelledby="calc-rows-label">{d['rows']}</ol>
<p class="fine">{e(k['fine'])}</p></div>
</div></div></section>"""


def s_product(lang, c):
    p = c["product"]
    mocks = json.loads((HERE / "data" / f"mocks_{lang}.json").read_text())
    pids = c["panel_ids"]
    tabs = "".join(f'<button type="button" class="tab" role="tab" id="aba-{pids[i]}" aria-controls="{pids[i]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(lbl)}</button>'
                   for i, lbl in enumerate(p["tabs"]))
    panels = []
    for i, ((h3, txt), m) in enumerate(zip(p["panels"], mocks)):
        mock = m["mock"]
        if lang == "en":
            mock = mock.replace("96,4%", "96.4%")
        panels.append(f"""<div class="panel{' is-active' if i == 0 else ''}" role="tabpanel" id="{pids[i]}" aria-labelledby="aba-{pids[i]}" tabindex="0">
<div class="panel__text"><h3>{e(h3)}</h3><p>{e(txt)}</p></div>
<figure><div aria-hidden="true">{mock}</div><figcaption>{m['caption']}</figcaption></figure>
</div>""")
    return f"""<section class="section section--line" id="{c['ids']['product']}" aria-labelledby="produto-titulo">
<div class="wrap">{sec_head(p['eyebrow'], p['h2'], 'produto-titulo')}
<div class="tabs" role="tablist" aria-label="{e(p['tablist'])}">{tabs}</div>
<div class="panels reveal">{''.join(panels)}</div>
</div></section>"""


ROUTE_D = {
    "route": "M321,539 L326,537 L331,534 L337,532 L343,529 L348,526 L354,523 L360,521 L365,518 L371,515 L376,512 L382,509 L387,506 L392,502 L398,499 L403,495 L408,491 L414,487 L421,485 L427,483 L434,481 L441,479 L448,477 L455,475 L461,472 L468,469 L475,467 L482,464 L488,461 L495,458 L502,457 L509,456 L515,455 L522,455 L529,454 L535,454 L542,452 L549,451 L555,449 L562,448 L560,445 L555,442 L550,439 L546,434 L541,430 L536,425 L532,420 L527,415 L522,410 L518,406 L513,401 L509,397 L504,393 L500,389 L496,384 L495,381 L502,379 L508,378 L514,376 L521,375 L527,373 L533,371 L540,368 L546,366 L552,363 L558,361 L565,359 L571,359 L577,359 L583,359 L590,359 L596,358 L602,357 L608,354 L614,352 L621,351 L627,350 L633,348 L637,345 L632,342 L627,338 L622,334 L617,329 L612,324 L607,319 L601,312 L596,305 L591,298 L586,291 L581,284 L576,276 L571,266 L567,265 L565,262 L571,251 L576,246 L582,244 L588,244 L594,244 L600,246 L606,249 L612,248 L617,243 L623,234 L629,232 L635,230 L640,229 L645,227 L642,220 L637,214 L633,202 L629,180 L625,157 L620,129 L616,102 L612,74 L609,54",
    "s1": "M321,539 L326,537 L331,534 L337,532 L343,529 L348,526 L354,523 L360,521 L365,518 L371,515 L376,512 L382,509 L387,506 L392,502 L398,499 L403,495 L408,491 L414,487 L421,485 L427,483 L434,481 L441,479 L448,477 L455,475 L461,472 L468,469 L475,467 L482,464 L488,461 L495,458 L502,457 L509,456 L515,455 L520,455",
    "s2": "M520,455 L527,454 L534,454 L540,453 L547,451 L554,450 L560,448 L561,446 L556,443 L551,440 L547,435 L542,431 L537,426 L533,421 L528,416 L523,411 L519,406 L514,402 L510,398 L505,394 L501,389 L497,385 L494,381 L500,379 L507,378 L513,377 L519,375 L526,373 L532,371 L538,369 L545,366 L551,364 L557,362 L563,360 L570,359 L576,359 L582,359 L588,359 L595,358 L601,357 L607,355 L613,353 L619,351 L625,350 L632,348 L637,346 L634,343 L628,339 L623,335 L618,330 L613,325 L608,320 L603,314 L598,307 L592,300 L587,293 L582,286 L577,279 L573,268 L568,265 L564,263 L565,262",
    "s3": "M565,262 L571,251 L576,246 L582,244 L588,244 L594,244 L600,246 L606,249 L612,248 L617,243 L623,234 L629,232 L635,230 L640,229 L645,227 L642,220 L637,214 L633,202 L629,180 L625,157 L620,129 L616,102 L612,74 L609,54",
}


def s_climb(lang, c):
    m = c["climb"]
    steps = [(k, t, fill_price(d, lang)) for k, t, d in m["steps"]]
    wps = "".join(f"""<div class="wp wp--{i + 1}{' is-on' if i == 0 else ''}{' is-next' if i == 1 else ''}">
<button type="button" class="wp__btn" aria-label="{i + 1}. {e(t)} · {e(k)}" aria-pressed="{'true' if i == 0 else 'false'}" aria-describedby="wp-d{i + 1}"><span class="wp__ping" aria-hidden="true"></span><span class="wp__sq" aria-hidden="true"></span></button>
<span class="wp__tag" aria-hidden="true">0{i + 1}</span>
<div class="wp__card" aria-hidden="{'false' if i == 0 else 'true'}"><span class="k">0{i + 1} · {e(k)}</span><span class="t">{e(t)}</span><span class="d" id="wp-d{i + 1}">{e(d)}</span></div>
</div>""" for i, (k, t, d) in enumerate(steps))
    bar = "".join(f'<li><button type="button" class="mt__step{" is-on" if i == 0 else ""}" aria-pressed="{"true" if i == 0 else "false"}"><span class="k">0{i + 1} · {e(k)}</span><span class="t">{e(t)}</span><span class="d">{e(d)}</span></button></li>'
                  for i, (k, t, d) in enumerate(steps))
    segs = "".join(f'<path class="mt__seg" d="{ROUTE_D["s" + str(n)]}" pathLength="1" fill="none" stroke="#99E604" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1"/>' for n in (1, 2, 3))
    return f"""<section class="mt on-dark" id="{c['ids']['climb']}" aria-labelledby="escalada-titulo">
<div class="mt__grid" aria-hidden="true"></div>
<div class="mt__wrap" id="mt">
<div class="mt__copy reveal">
<p class="mt__eyebrow">{e(m['eyebrow'])}</p>
<h2 id="escalada-titulo">{e(m['h2'])}</h2>
<p class="mt__lead">{e(m['lead'])}</p>
<p class="mt__hint" aria-hidden="true"><span class="hover">{e(m['hint_hover'])}</span><span class="touch">{e(m['hint_touch'])}</span></p>
</div>
<div class="mt__stage" role="group" aria-label="{e(m['group'])}">
<div class="mt__rise"><div class="mt__tilt">
<div class="mt__layer mt__mountain"><div><img src="/assets/img/montanha-3d.svg" alt="" width="1000" height="620" loading="lazy" decoding="async" draggable="false"></div></div>
<div class="mt__layer mt__mist-layer" aria-hidden="true"><div class="mt__mist mt__mist--1"></div><div class="mt__mist mt__mist--2"></div></div>
<div class="mt__layer mt__route-layer" aria-hidden="true"><svg viewBox="0 0 1000 620" preserveAspectRatio="xMidYMid meet" focusable="false"><path class="mt__route" d="{ROUTE_D['route']}" fill="none" stroke="#FEFEFE" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round"/>{segs}<g transform="translate(609.0 54.4)"><path d="M0 -6 V-46" stroke="#FEFEFE" stroke-width="2"/><path class="mt__flag" d="M1 -46 L26 -39 L1 -31 Z" fill="#99E604"/></g></svg></div>
<div class="mt__layer mt__wps">{wps}</div>
</div></div>
</div>
<ol class="mt__steps" role="list">{bar}</ol>
</div>
</section>"""


def s_migration(lang, c):
    m = c["migration"]
    steps = "".join(f'<li class="step-card"><span class="num" aria-hidden="true">0{i + 1}</span><h3>{e(h)}</h3><p>{e(t)}</p></li>' for i, (h, t) in enumerate(m["steps"]))
    pic = picture("escalada-violeta", [640, 1070], "", sizes="100vw", w=1070, h=1276)
    return f"""<section class="banner on-dark" id="{c['ids']['migration']}" aria-labelledby="migracao-titulo">
<div class="banner__bg parallax" aria-hidden="true">{pic}</div>
<div class="banner__shade" aria-hidden="true"></div>
<div class="banner__in reveal">
<p class="eyebrow">{e(m['eyebrow'])}</p>
<h2 class="h2" id="migracao-titulo">{e(m['h2'])}</h2>
<p class="lead">{e(m['lead'])}</p>
<ol class="steps-3" role="list">{steps}</ol>
<div class="banner__ctas"><a class="btn btn--lime btn--block" href="{INSTALL[lang]}" target="_blank" rel="noopener">{e(m['cta1'])}</a>{ext_link(WHATSAPP[lang], e(m['cta2']), 'link-u')}</div>
</div>
</section>"""


def s_integrations(lang, c):
    g = c["integrations"]
    feat = "".join(f'<li class="provider"><img src="/assets/img/logos/{f}" alt="{e(n)}" width="{w}" height="{h}" loading="lazy" decoding="async"></li>'
                   for n, f, w, h in g["featured"])
    groups = "".join(f'<div><h3>{e(h)}</h3><ul class="tags" role="list">{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></div>' for h, items in g["groups"])
    return f"""<section class="section section--line" id="{c['ids']['integrations']}" aria-labelledby="integracoes-titulo">
<div class="wrap"><div class="sec-head reveal"><h2 class="eyebrow eyebrow--h" id="integracoes-titulo">{e(g['h2'])}</h2><p class="lead lead--strong">{e(g['lead'])}</p></div>
<ul class="providers reveal" role="list" aria-label="{e(g['list_label'])}">{feat}</ul>
<details class="more reveal"><summary>{e(g['more'])}<span class="see" aria-hidden="true">{e(g['see'])}</span></summary>
<div class="more__body">{groups}<p>{g['other'].format(wa=e(WHATSAPP[lang]))}</p><p class="fine">{e(g['fine'])}</p></div></details>
</div></section>"""


def s_pricing(lang, c):
    """Dois planos: Growth (taxa única) e Enterprise (sob medida). Cada plano é um <article> com a lista do que inclui."""
    p = c["pricing"]
    g, en = p["growth"], p["enterprise"]
    rate = price_vars(lang)["rate"]
    li = lambda x: f"<li>{e(x)}</li>"
    g_body = (f'<p class="plan__head">{e(g["head"])}</p><ul class="checks" role="list">{"".join(li(x) for x in g["features"])}</ul>'
              f'<ul class="checks plan__service" role="list">{"".join(li(x) for x in g["service"])}</ul>')
    e_body = (f'<p class="plan__head">{e(en["head"])}</p><ul class="checks checks--rich" role="list">'
              + "".join(f'<li><span><strong>{e(t)}<span class="visually-hidden">:</span></strong> <span>{e(d)}</span></span></li>' for t, d in en["features"]) + "</ul>")
    growth = f"""<article class="plan plan--featured" aria-labelledby="plano-growth">
<header class="plan__top"><h3 class="plan__name" id="plano-growth">{e(g['name'])}</h3><p class="plan__price">{rate}</p><p class="plan__sub">{e(g['sub'])}</p>
<a class="btn btn--dark btn--block" href="{INSTALL[lang]}" target="_blank" rel="noopener">{e(g['btn'])}</a></header>
<div class="plan__body">{g_body}</div></article>"""
    ent = f"""<article class="plan plan--ent" aria-labelledby="plano-enterprise">
<header class="plan__top"><h3 class="plan__name" id="plano-enterprise">{e(en['name'])}</h3><p class="plan__price">{e(en['price'])}</p><p class="plan__sub">{e(en['sub'])}</p>
<a class="btn btn--outline btn--block" href="{e(WHATSAPP[lang])}" target="_blank" rel="noopener" data-track="enterprise">{e(en['btn'])}</a></header>
<div class="plan__body">{e_body}</div></article>"""
    strip = "".join(li(x) for x in p["strip"])
    return f"""<section class="section section--line" id="{c['ids']['pricing']}" aria-labelledby="precos-titulo">
<div class="wrap">{sec_head(p['eyebrow'], p['h2'], 'precos-titulo', e(fill_price(p['lead'], lang)))}
<div class="plans reveal">{growth}{ent}</div>
<div class="price-strip reveal"><ul class="checks checks--row" role="list">{strip}</ul><p>{e(p['note'])}</p></div>
</div></section>"""


def s_cta(lang, c, data=None, hid="cta-titulo"):
    k = data or c["cta"]
    second = f'{ext_link(WHATSAPP[lang], e(k["b2"]), "btn btn--outline")}' if "b2" in k else ""
    btn = k.get("btn") or k.get("b1")
    sid = c["ids"]["cta"] if c else "comece"
    return f"""<section class="cta" id="{sid}" aria-labelledby="{hid}">
<img class="cta__bg parallax" src="/assets/img/relevo-lima.svg" alt="" width="1600" height="900" loading="lazy" decoding="async">
<div class="wrap cta__in reveal">
<p class="eyebrow">{e(k['eyebrow'])}</p>
<h2 id="{hid}">{e(k['h2'])}</h2>
<p>{e(k['p'])}</p>
<div class="cta__ctas"><a class="btn btn--dark" href="{INSTALL[lang]}" target="_blank" rel="noopener">{e(btn)}</a>{second}</div>
</div>
</section>"""


def s_faq(lang, c):
    f = c["faq"]
    items = "".join(f'<details class="faq__item"{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(fill_price(a, lang))}</p></details>'
                    for i, (q, a) in enumerate(f["items"]))
    return f"""<section class="section" id="{c['ids']['faq']}" aria-labelledby="faq-titulo">
<div class="wrap faq reveal">
<div class="sec-head"><p class="eyebrow">{e(f['eyebrow'])}</p><h2 class="h2" id="faq-titulo">{e(f['h2'])}</h2></div>
<div class="faq__list">{items}</div>
</div></section>"""


def s_contact(lang, c):
    k = c["contact"]
    msg = dict(k["msg"])
    note = k["privacy_note"].format(privacy=ROUTES["privacy"][lang])
    return f"""<section class="section section--sand" id="{c['ids']['contact']}" aria-labelledby="contato-titulo">
<div class="wrap contact reveal">
<div class="contact__col"><h2 id="contato-titulo">{e(k['c1h'])}</h2><p>{e(k['c1p'])}</p>
<div class="contact__links"><a href="mailto:{EMAIL}">{e(k['email'])}</a>{ext_link(WHATSAPP[lang], e(k['wa']))}</div></div>
<div class="contact__col"><h2>{e(k['c2h'])}</h2><p>{e(k['c2p'])}</p><div class="contact__links">{ext_link(WHATSAPP[lang], e(k['c2b']))}</div></div>
<div class="contact__col">
<h2 id="news-titulo">{e(k['c3h'])}</h2>
<form class="stack" action="{FORM_ENDPOINT}" method="POST" data-newsletter data-fallback="{EMAIL}" data-msg="{e(json.dumps(msg, ensure_ascii=False))}" aria-labelledby="news-titulo" novalidate>
<label for="news-email"><p>{e(k['c3p'])}</p></label>
<div class="form-row"><input id="news-email" name="email" type="email" autocomplete="email" inputmode="email" required placeholder="{e(k['placeholder'])}"><button type="submit">{e(k['submit'])}</button></div>
<div class="hp" aria-hidden="true"><label for="news-gotcha">Não preencha</label><input id="news-gotcha" type="text" name="_gotcha" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="_language" value="{lang}">
<p class="form-status" role="status" aria-live="polite"></p>
<p class="fine">{note}</p>
</form>
</div>
</div></section>"""


SECTIONS = {"relationship": s_relationship, "problem": s_problem, "who": s_who, "calc": s_calc, "product": s_product, "climb": s_climb,
            "migration": s_migration, "integrations": s_integrations, "pricing": s_pricing, "cta": s_cta,
            "faq": s_faq, "contact": s_contact}


def build_home(lang):
    c = HOME[lang]
    body = s_hero(lang, c) + "\n" + "\n".join(SECTIONS[k](lang, c) for k in c["order"])
    graph = [org_ld(), website_ld(), app_ld(lang), webpage_ld(lang, "home", c["title"], c["description"]), faq_ld(lang)]
    preload = '<link rel="preload" as="image" href="/assets/img/everest-violeta-1024.avif" type="image/avif" fetchpriority="high">'
    return page(lang, "home", c["title"], c["description"], graph, body, preload)


# =============================================================================
# SOBRE
# =============================================================================
def build_about(lang):
    a = ABOUT[lang]
    hero_pic = picture("escalada-violeta", [640, 1070], "", sizes="100vw", loading=None, fetchpriority="high", w=1070, h=1276)
    story = "".join(f"<p>{e(p)}</p>" for p in a["story"]["paras"])
    values = "".join(f'<li class="value"><h3>{e(h)}</h3><p class="big">{e(b)}</p><p class="small">{e(s)}</p></li>' for h, b, s in a["values"]["items"])
    tl = "".join(f'<li><span class="when">{e(w)}</span><h3>{e(h)}</h3><p>{e(t)}</p></li>' for w, h, t in a["climb"]["items"])
    fig = picture("everest-violeta", [640, 1024], a["climb"]["img_alt"], sizes="(min-width: 64em) 55vw, 100vw", w=1024, h=682)
    main = f"""<section class="page-hero on-dark" aria-labelledby="sobre-titulo">
<div class="page-hero__bg zoom" aria-hidden="true">{hero_pic}</div>
<div class="page-hero__shade" aria-hidden="true"></div>
<div class="page-hero__in">
{breadcrumb(lang, a['crumb'])}
<p class="eyebrow">{e(a['hero']['eyebrow'])}</p>
<h1 id="sobre-titulo">{e(a['hero']['h1'])}</h1>
<p class="lead">{e(a['hero']['lead'])}</p>
</div>
</section>
<section class="section" aria-labelledby="historia-titulo">
<div class="wrap split reveal">
<div class="split__head"><p class="eyebrow">{e(a['story']['eyebrow'])}</p><h2 class="h2" id="historia-titulo">{e(a['story']['h2'])}</h2></div>
<div class="prose">{story}</div>
</div></section>
<section class="section section--sand" aria-labelledby="missao-titulo">
<div class="wrap reveal"><h2 class="eyebrow" id="missao-titulo">{e(a['values']['h2'])}</h2><ul class="values" role="list">{values}</ul></div>
</section>
<section class="section timeline-sec on-dark" aria-labelledby="escalada-sobre-titulo">
<div class="wrap timeline-grid reveal">
<div class="stack"><p class="eyebrow">{e(a['climb']['eyebrow'])}</p><h2 class="h2" id="escalada-sobre-titulo">{e(a['climb']['h2'])}</h2><ol class="timeline" role="list">{tl}</ol></div>
<figure class="timeline-fig">{fig}</figure>
</div></section>
<section class="section" aria-labelledby="quem-faz-titulo">
<div class="wrap center-block reveal"><p class="eyebrow">{e(a['who']['eyebrow'])}</p><h2 class="h2" id="quem-faz-titulo">{e(a['who']['h2'])}</h2><p>{e(a['who']['p'])}</p>{ext_link(AMLAB, e(a['who']['link']), 'link-caps')}</div>
</section>
{s_cta(lang, None, a['cta'], 'sobre-cta-titulo')}"""
    graph = [org_ld(), website_ld(), webpage_ld(lang, "about", a["title"], a["description"], "AboutPage", True),
             breadcrumb_ld(lang, "about", a["crumb"])]
    graph[2]["mainEntity"] = {"@id": SITE + "/#org"}
    preload = '<link rel="preload" as="image" href="/assets/img/escalada-violeta-1070.avif" type="image/avif" fetchpriority="high">'
    return page(lang, "about", a["title"], a["description"], graph, main, preload)


# =============================================================================
# PÁGINAS LEGAIS
# =============================================================================
def legal_page(lang, key, doc):
    other_key = "privacy" if key == "terms" else "terms"
    ph = {"privacy": ROUTES["privacy"][lang], "terms": ROUTES["terms"][lang], "email": EMAIL}
    fill = lambda s: s.format(**ph)
    prefix = "t" if key == "terms" else "p"
    toc = "".join(f'<li><a href="#{prefix}-{i + 1:02d}"><span aria-hidden="true">{i + 1:02d}</span>{e(t)}</a></li>' for i, (t, _) in enumerate(doc["clauses"]))
    clauses = []
    for i, (title, blocks) in enumerate(doc["clauses"]):
        cid = f"{prefix}-{i + 1:02d}"
        parts = []
        for kind, val in blocks:
            if kind == "p":
                parts.append(f"<p>{fill(val)}</p>")
            elif kind == "ul":
                parts.append("<ul>" + "".join(f"<li>{fill(x)}</li>" for x in val) + "</ul>")
            elif kind == "dl":
                parts.append('<dl class="deflist">' + "".join(f"<div><dt>{e(dt)}</dt><dd>{fill(dd)}</dd></div>" for dt, dd in val) + "</dl>")
        clauses.append(f'<section class="clause" id="{cid}" aria-labelledby="{cid}-titulo"><h2 id="{cid}-titulo"><span aria-hidden="true">{i + 1:02d}</span>{e(title)}</h2>{"".join(parts)}</section>')
    intro = "".join(f"<p>{fill(p)}</p>" for p in doc["intro"])
    names = {"terms": UI[lang]["footer"]["terms"], "privacy": UI[lang]["footer"]["privacy"]}
    tabs = "".join((f'<span aria-current="page">{e(names[k])}</span>' if k == key else f'<a href="{ROUTES[k][lang]}">{e(names[k])}</a>') for k in ("terms", "privacy"))
    ct, cs, cb = doc["callout"]
    main = f"""<div class="legal-head">
<div class="wrap">
{breadcrumb(lang, doc['crumb'])}
<p class="eyebrow">Legal</p>
<h1>{e(doc['h1'])}</h1>
<p class="lead">{e(doc['lead'])}</p>
<p class="updated">{UI[lang]['updated']}: <time datetime="{UPDATED['iso']}">{UPDATED[lang]}</time></p>
<nav class="doc-tabs" aria-label="{UI[lang]['docs_label']}">{tabs}</nav>
</div>
</div>
<div class="wrap legal">
<aside class="toc" aria-labelledby="toc-titulo"><details><summary id="toc-titulo">{e(doc['toc'])}</summary><nav aria-labelledby="toc-titulo"><ol>{toc}</ol></nav></details></aside>
<article class="legal-body">
{intro}
{''.join(clauses)}
<div class="callout"><div><p class="t">{e(ct)}</p><p class="s">{fill(cs)}</p></div><a class="btn btn--outline" href="{ROUTES[other_key][lang]}">{e(cb)}</a></div>
</article>
</div>"""
    graph = [org_ld(), website_ld(), webpage_ld(lang, key, doc["title"], doc["description"], "WebPage", True),
             breadcrumb_ld(lang, key, doc["crumb"])]
    return page(lang, key, doc["title"], doc["description"], graph, main)


# =============================================================================
# 404
# =============================================================================
def build_404():
    main = """<section class="notfound on-dark" aria-labelledby="nf-titulo">
<div class="wrap">
<p class="code">404</p>
<h1 id="nf-titulo">Página não encontrada <span lang="en">· Page not found</span></h1>
<p>O endereço pode ter mudado. Volte ao início ou acesse uma das páginas abaixo.</p>
<p lang="en">This address may have changed. Go back home or pick one of the pages below.</p>
<div class="row-links"><a class="btn btn--lime" href="/">Início (PT)</a><a class="btn btn--ghost" href="/en/" lang="en">Home (EN)</a></div>
<ul class="row-links" role="list">
<li><a class="link-u" href="/sobre-nos/">Sobre nós</a></li><li><a class="link-u" href="/termos-de-uso/">Termos de uso</a></li><li><a class="link-u" href="/politica-de-privacidade/">Política de privacidade</a></li>
<li><a class="link-u" href="/en/about/" lang="en">About</a></li><li><a class="link-u" href="/en/terms-of-use/" lang="en">Terms of use</a></li><li><a class="link-u" href="/en/privacy-policy/" lang="en">Privacy policy</a></li>
</ul>
</div></section>"""
    graph = [org_ld(), website_ld()]
    html_ = head("pt", None, "Página não encontrada · Everni", "A página procurada não existe.", graph, robots="noindex, follow")
    html_ = html_.replace('<link rel="stylesheet"', '<link rel="stylesheet"')
    hdr = header("pt", "home").replace(' aria-current="page"', "").replace('href="#', 'href="/#').replace('href="/#conteudo"', 'href="#conteudo"')
    ftr = footer("pt", "home").replace('href="#', 'href="/#')
    return f"""{html_}
<body>
{hdr}
<main id="conteudo" tabindex="-1">
{main}
</main>
{ftr}
</body>
</html>
"""


# =============================================================================
# Arquivos de indexação, LLMs e PWA
# =============================================================================
def sitemap():
    urls = []
    prio = {"home": "1.0", "about": "0.7", "terms": "0.3", "privacy": "0.3"}
    for key in ROUTES:
        for lang in ("pt", "en"):
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{abs_url(ROUTES[key][l])}"/>'
                           for h, l in (("pt-BR", "pt"), ("en", "en"), ("x-default", "en")))
            urls.append(f"<url><loc>{abs_url(ROUTES[key][lang])}</loc><lastmod>{SITE_UPDATED if key == 'home' else UPDATED['iso']}</lastmod>"
                        f"<changefreq>{'weekly' if key == 'home' else 'yearly'}</changefreq><priority>{prio[key]}</priority>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")


ROBOTS = f"""# Everni · robots.txt
User-agent: *
Allow: /
Disallow: /404.html

# Assistentes e buscadores de IA são bem-vindos (conteúdo público de produto)
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
"""


class _Text(__import__("html.parser").parser.HTMLParser):
    """Converte o <main> gerado em Markdown simples para o llms-full.txt."""
    SKIP = {"script", "style", "svg", "button", "figure", "form", "nav", "input", "caption", "thead"}
    INLINE = {"span", "a", "div", "output", "label", "time", "strong", "em", "b"}

    def __init__(self):
        super().__init__()
        self.out, self.skip, self.stack, self.li = [], 0, [], 0
        self.li_fresh = False
        self.tbl = 0

    def _sep(self):
        if self.out and not self.out[-1].endswith((" ", "\n")):
            self.out.append(" ")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        hidden = a.get("aria-hidden") == "true" or "seg--dup" in cls or cls == "hp" or "calc__scale" in cls or "mt__steps" in cls
        skip = hidden or tag in self.SKIP
        self.stack.append((tag, skip))
        if skip:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "table":
            self.tbl += 1
        elif self.tbl and tag == "p":
            self._sep()
        elif tag == "tr":
            self.out.append("\n- ")
        elif tag == "th" and a.get("scope") == "row":
            self.out.append("**")
        elif tag == "td":
            self.out.append(" — " + (a.get("data-label") + ": " if a.get("data-label") else ""))
        elif tag == "li":
            self.li += 1
            self.out.append("\n- ")
            self.li_fresh = True
        elif self.li and tag in ("h3", "p", "dt", "dd"):
            if not self.li_fresh:
                self.out.append(" — " if tag != "dd" else ": ")
            self.li_fresh = False
            if tag == "h3":
                self.out.append("**")
        elif tag in ("h1", "h2", "h3"):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in ("p", "summary", "dt", "details"):
            self.out.append("\n\n")
        elif tag == "dd":
            self.out.append(": ")
        elif tag == "br":
            self.out.append(" ")
        elif tag in self.INLINE:
            self._sep()

    def handle_endtag(self, tag):
        while self.stack:
            t, sk = self.stack.pop()
            if sk:
                self.skip -= 1
            elif not self.skip:
                if t == "th":
                    self.out.append("**")
                if t == "table":
                    self.tbl -= 1
                if t == "li":
                    self.li -= 1
                elif t == "h3" and self.li:
                    self.out.append("**")
                elif t in self.INLINE or t in ("h1",):
                    self._sep()
            if t == tag:
                break

    def handle_data(self, data):
        if not self.skip:
            txt = re.sub(r"\s+", " ", data)
            if txt.strip():
                self.li_fresh = False if not txt.strip() else self.li_fresh
            self.out.append(txt)

    def text(self):
        t = "".join(self.out)
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        t = t.replace("**—", "** —").replace(" :", ":")
        return re.sub(r"\n{3,}", "\n\n", t).strip()


def main_text(page_html):
    m = re.search(r'<main id="conteudo"[^>]*>(.*)</main>', page_html, re.S)
    p = _Text()
    p.feed(m.group(1))
    return p.text()


def llms_txt():
    r_pt, r_en = price_vars("pt")["rate"], price_vars("en")["rate"]
    feats_en = "; ".join(HOME["en"]["pricing"]["growth"]["features"])
    ent_en = "; ".join(t for t, _ in HOME["en"]["pricing"]["enterprise"]["features"])
    return f"""# Everni

> Everni is a native Shopify app for subscriptions and recurring billing, built in Brazil (B2C, D2C and B2B). It covers subscription plans, recurring billing, failed payment recovery and retention, a self-serve customer portal and recurring revenue analytics. Pricing: free to install, then a flat {r_en} of monthly subscription GMV on the Growth plan, with no monthly fee and no per-order fee, billed in USD through Shopify. An Enterprise plan with negotiated rates is available for high-volume brands. Free assisted migration from Recharge, Skio, other apps or spreadsheets, with a 30-day pilot.

Everni é um app de assinaturas e cobrança recorrente nativo da Shopify, feito no Brasil. Instalação gratuita e plano Growth com taxa única de {r_pt} do GMV mensal de assinaturas, sem mensalidade e sem taxa por pedido; plano Enterprise com condições negociadas para alto volume. Parceira oficial no Brasil: Stone. Também integra Barte, Stripe, PayPal, Shopify Payments e Authorize.net.

## Key facts
- Plans: Growth ({r_en} of monthly subscription GMV, free to install, no monthly fee, no per-order fee) and Enterprise (custom pricing).
- Growth includes: {feats_en}.
- Enterprise adds: {ent_en}.
- Payment providers: Shopify Payments, Stripe, PayPal and Authorize.net (US, Canada, Europe); Stone (official partner) and Barte (Brazil).
- Migration: free and assisted, from Recharge, Skio, other apps or spreadsheets, with a 30-day pilot.
- Last updated: {SITE_UPDATED}.

Company: {COMPANY['legal_name']} (CNPJ {COMPANY['cnpj']}), {COMPANY['street']}, {COMPANY['city']}/{COMPANY['region']}, Brazil. Developed by AM Lab ({AMLAB}). Contact: {EMAIL} · WhatsApp {PHONE}.

## Pages (English)
- [Home]({SITE}/en/): product overview, comparison, how it works, industries, savings calculator vs Recharge and Skio, integrations, migration, pricing (Growth and Enterprise), FAQ
- [About]({SITE}/en/about/): story, mission, vision and values
- [Terms of use]({SITE}/en/terms-of-use/)
- [Privacy policy]({SITE}/en/privacy-policy/)

## Páginas (Português)
- [Início]({SITE}/): visão geral, comparativo, como funciona, segmentos, calculadora, integrações, migração, preços (Growth e Enterprise), FAQ
- [Sobre nós]({SITE}/sobre-nos/)
- [Termos de uso]({SITE}/termos-de-uso/)
- [Política de privacidade]({SITE}/politica-de-privacidade/)

## Optional
- [Full text of every page (PT + EN)]({SITE}/llms-full.txt)
- [Install on the Shopify App Store]({INSTALL['en']})
"""


MANIFEST = {
    "name": "Everni · Subscriptions for Shopify", "short_name": "Everni",
    "description": "Native Shopify subscriptions and recurring billing app.",
    "start_url": "/?source=pwa", "scope": "/", "display": "standalone",
    "background_color": "#181818", "theme_color": "#181818", "lang": "pt-BR", "dir": "ltr",
    "icons": [
        {"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "/maskable-icon-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
        {"src": "/maskable-icon-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
    ],
}

BROWSERCONFIG = """<?xml version="1.0" encoding="utf-8"?>
<browserconfig><msapplication><tile><square150x150logo src="/mstile-150x150.png"/><TileColor>#181818</TileColor></tile></msapplication></browserconfig>
"""

SECURITY_TXT = f"""Contact: mailto:{EMAIL}
Expires: 2027-11-23T00:00:00.000Z
Preferred-Languages: pt, en
Canonical: {SITE}/.well-known/security.txt
Policy: {SITE}/politica-de-privacidade/
"""

HUMANS = f"""/* TEAM */
Everni · desenvolvida pela AM Lab ({AMLAB})
Contato: {EMAIL}
Local: Americana/SP, Brasil

/* SITE */
Última atualização: {SITE_UPDATED}
Padrões: HTML5, CSS3, JavaScript sem dependências, Schema.org (JSON-LD)
Fontes: Montserrat, JetBrains Mono (auto-hospedadas, SIL OFL)
"""


def minify_css(css):
    css = re.sub(r"/\*(?!!).*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    # devolve espaços exigidos em media queries ("and (") e valores
    css = re.sub(r"\band\(", "and (", css)
    return css.strip()


def minify_js(js):
    # remoção conservadora: só comentários de linha inteira e espaços de indentação
    out = []
    for line in js.splitlines():
        s = line.strip()
        if not s or (s.startswith("//")):
            continue
        out.append(s)
    return "\n".join(out) + "\n"


def write(path, content):
    p = DOCS / path.lstrip("/")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def main():
    # assets: CSS (site + mockups) e JS
    css = (HERE / "src" / "site.css").read_text() + "\n" + (HERE / "data" / "mocks.css").read_text()
    write("assets/css/everni.css", minify_css(css))
    write("assets/js/lang.js", minify_js((HERE / "src" / "lang.js").read_text()))
    write("assets/js/site.js", minify_js((HERE / "src" / "site.js").read_text()))
    gtm_file = DOCS / "assets/js/gtm.js"
    if GTM_ID:
        write("assets/js/gtm.js", minify_js((HERE / "src" / "gtm.js").read_text()))
    elif gtm_file.exists():
        gtm_file.unlink()

    pages = {}
    for lang in ("pt", "en"):
        pages[ROUTES["home"][lang]] = build_home(lang)
        pages[ROUTES["about"][lang]] = build_about(lang)
        pages[ROUTES["terms"][lang]] = legal_page(lang, "terms", TERMS[lang])
        priv = PRIVACY[lang]
        if GTM_ID:  # com medição ativa, a seção de cookies passa a descrever o GTM/Analytics
            priv = dict(priv, clauses=[PRIVACY_COOKIES_GTM[lang] if t.startswith("Cookies") else (t, b) for t, b in priv["clauses"]])
        pages[ROUTES["privacy"][lang]] = legal_page(lang, "privacy", priv)
    for route, content in pages.items():
        write(route + "index.html", content)
    write("404.html", build_404())

    write("sitemap.xml", sitemap())
    write("robots.txt", ROBOTS)
    write("llms.txt", llms_txt())
    full = ["# Everni — full site content (PT-BR + EN)\n", f"Source: {SITE} · Last updated {SITE_UPDATED}\n"]
    for route in ["/", "/sobre-nos/", "/termos-de-uso/", "/politica-de-privacidade/", "/en/", "/en/about/", "/en/terms-of-use/", "/en/privacy-policy/"]:
        full.append(f"\n\n---\n\nURL: {SITE}{route}\n\n" + main_text(pages[route]))
    write("llms-full.txt", "".join(full) + "\n")
    write("site.webmanifest", json.dumps(MANIFEST, ensure_ascii=False, indent=2))
    write("browserconfig.xml", BROWSERCONFIG)
    write(".well-known/security.txt", SECURITY_TXT)
    write("humans.txt", HUMANS)
    write("CNAME", "geteverni.com\n")
    write(".nojekyll", "")
    print("OK:", len(pages), "páginas + 404")


if __name__ == "__main__":
    main()
