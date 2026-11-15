# Subbly — Site público

Site estático de marketing do Subbly, app de assinaturas e recorrência
nativo para Shopify. Hospedado no GitHub Pages com domínio próprio
`trysubbly.com`. Cada página é um HTML único com CSS, fontes e lógica
embutidos — sem servidor, build nem dependências.

## Estrutura

- `index.html` — Landing page em português (PT-BR) → `/`
- `en/index.html` — Landing page em inglês (EN) → `/en/`
- `privacy/index.html` — Política de Privacidade (PT/EN com toggle) → `/privacy/`
- `terms/index.html` — Termos de Serviço (PT/EN com toggle) → `/terms/`
- `robots.txt` / `sitemap.xml` — SEO para crawlers (inclui hreflang PT/EN)
- `images/favicons/` — favicons e `site.webmanifest` (PWA)
- `CNAME` — domínio `trysubbly.com`

## Navegação entre idiomas

- Landing: seletor `PT`/`EN` no cabeçalho alterna entre `/` e `/en/`.
- Legal: toggle `PT`/`EN` no cabeçalho alterna o conteúdo na mesma página
  (ou acesse `/privacy/?lang=en` / `/terms/?lang=en` para abrir direto em inglês).

## Testar localmente

```
python3 -m http.server 8000
# abra http://localhost:8000
```

## Publicar com GitHub Pages

1. Suba todo o conteúdo desta pasta para o branch `main`:
   `git add . && git commit -m "site" && git push`.
2. No GitHub: **Settings → Pages → Source** → branch `main`, pasta `/ (root)`.
3. O  
### Domínio próprio

- **Settings → Pages → Custom domain** → `trysubbly.com`.
- DNS: registros `A` (ou `AAAA`) para os IPs do GitHub Pages, ou um `CNAME`.
- O arquivo `CNAME` deste repositório já fixa o domínio.

## Observação

Estas são as páginas **institucionais**. O aplicativo de assinaturas em si
(cobrança em cartão, planos, portal do assinante) é um software à parte.
