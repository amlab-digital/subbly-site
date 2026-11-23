# Everni · site institucional (geteverni.com)

Site estático, bilíngue (PT-BR / EN), mobile-first, sem frameworks e sem dependências em produção.
A pasta **`docs/`** é exatamente o que vai ao ar. A pasta **`tools/`** gera o `docs/` a partir dos textos.

```
docs/                     ← raiz publicada pelo GitHub Pages
  index.html              /                         (PT-BR)
  sobre-nos/              /sobre-nos/
  termos-de-uso/          /termos-de-uso/
  politica-de-privacidade/
  en/                     /en/                      (EN)
  en/about/  en/terms-of-use/  en/privacy-policy/
  404.html                página de erro bilíngue (noindex)
  assets/css/everni.css   CSS único, mobile-first
  assets/js/lang.js       seleção de idioma por país (IP + fuso)
  assets/js/site.js       menu, abas, calculadora, montanha, formulário
  assets/fonts/           Montserrat e JetBrains Mono auto-hospedadas (woff2)
  assets/img/             fotos AVIF/WebP/JPEG, SVGs, imagens de compartilhamento
  favicon.ico/.svg, apple-touch-icon, android-chrome, maskable, mstile, safari-pinned-tab
  site.webmanifest  browserconfig.xml
  sitemap.xml  robots.txt  llms.txt  llms-full.txt  humans.txt
  .well-known/security.txt  CNAME  .nojekyll
tools/
  build.py                gera todas as páginas (só Python 3, sem bibliotecas)
  content_home.py         textos da home (PT e EN)
  content_pages.py        Sobre, Termos e Privacidade (PT e EN)
  src/site.css src/site.js src/lang.js   fontes do CSS/JS (o build minifica)
  make_icons.py make_images.py make_og.py extract_mocks.py   (gerar imagens; precisam de Pillow + Playwright)
```

---

## 1. Publicar no GitHub Pages (uma vez)

1. Crie o repositório (ex.: `everni-site`) e envie esta pasta inteira:
   ```bash
   git init && git add . && git commit -m "Site Everni"
   git branch -M main
   git remote add origin git@github.com:SUA-ORG/everni-site.git
   git push -u origin main
   ```
2. No GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / pasta `/docs` → Save**.
3. Em **Custom domain**, confirme `geteverni.com` (o arquivo `docs/CNAME` já contém o domínio).
4. **DNS no registrador do domínio** (apex, sem www):
   | Tipo | Nome | Valor |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | AAAA | @ | 2606:50c0:8000::153 |
   | AAAA | @ | 2606:50c0:8001::153 |
   | AAAA | @ | 2606:50c0:8002::153 |
   | AAAA | @ | 2606:50c0:8003::153 |
   | CNAME | www | SUA-ORG.github.io |

   Com o `www` apontado, o GitHub redireciona `www.geteverni.com` → `geteverni.com` automaticamente.
5. Quando o certificado sair (minutos a 24 h), marque **Enforce HTTPS**.
6. Recomendado: **Settings da conta/organização → Pages → Verified domains** e verifique `geteverni.com` (impede que outra conta "sequestre" o domínio).
7. Indexação: cadastre o domínio no **Google Search Console** e no **Bing Webmaster Tools** e envie `https://geteverni.com/sitemap.xml`.

## 2. Editar textos, preços e links

```bash
cd tools
python3 build.py        # regenera docs/ em ~1 s
```

- **Textos**: `tools/content_home.py` e `tools/content_pages.py` (PT e EN lado a lado, mesma estrutura).
- **Preços**: lista `PRICING` no topo de `tools/build.py`. Faixas, taxas, exemplos da seção Preços, FAQ, JSON-LD, calculadora, `llms.txt` e a etapa "Cume" da montanha são recalculados a partir dela. Só as imagens de compartilhamento têm o texto fixo (`tools/make_og.py`).
- **Links**: `INSTALL` (App Store), `WHATSAPP`, `EMAIL`, `LINKEDIN` no topo de `tools/build.py`.
- **Data de atualização dos documentos legais**: `UPDATED` em `tools/content_pages.py`.
- O CSS e o JS recebem `?v=hash` automático, então o cache do navegador nunca serve versão velha.

## 3. Formulário de novidades (anti-spam)

GitHub Pages não processa formulários. O site já está pronto para o **Formspree** (plano grátis):
1. Crie um formulário em https://formspree.io e copie o ID (ex.: `xyzabcd`).
2. Em `tools/build.py`, troque `SEU_FORM_ID` em `FORM_ENDPOINT` e rode `python3 build.py`.
3. No painel do Formspree, ative reCAPTCHA/“spam filtering” e restrinja o domínio a `geteverni.com`.

Proteções já no site: campo-armadilha (`_gotcha`, honeypot), tempo mínimo de 2,5 s antes do envio, validação do e-mail e CSP limitando o envio ao Formspree.
Enquanto o ID não for trocado, o botão abre o app de e-mail do visitante com a inscrição preenchida (nada quebra).

## 4. Idioma automático (geolocalização)

`assets/js/lang.js`, carregado no `<head>`:
1. `?lang=pt` ou `?lang=en` na URL força e salva a escolha;
2. escolha manual no seletor PT/EN vence tudo (fica salva no navegador);
3. país em cache (30 dias);
4. país pelo IP: `api.country.is` (reserva `ipapi.co`), com limite de 1,5 s;
5. reserva final: fuso horário do aparelho.

**Brasil e Portugal → PT-BR; qualquer outro país → EN.** Cada página redireciona para a equivalente traduzida
(ex.: `/en/terms-of-use/` ↔ `/termos-de-uso/`). Robôs de busca, ferramentas de teste (Lighthouse/PageSpeed) e
navegadores automatizados **não** são redirecionados: o Google indexa as duas versões pelas tags `hreflang`.
Isso está informado nas Políticas de Privacidade (PT e EN).

## 5. SEO, LLMs e acessibilidade — o que já está feito

- HTML semântico (`header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `details/summary`), um `h1` por página, hierarquia de títulos correta.
- `title` e `description` únicos por página, `canonical`, `hreflang` (pt-BR, en, x-default), Open Graph e Twitter Card com imagens 1200×630.
- JSON-LD: `Organization` (razão social, CNPJ, endereço, contato), `WebSite`, `SoftwareApplication` (oferta de instalação grátis e faixas), `FAQPage`, `AboutPage`, `BreadcrumbList`, `WebPage`.
- `sitemap.xml` com alternates de idioma, `robots.txt` liberando buscadores e assistentes de IA, `llms.txt` (resumo) e `llms-full.txt` (texto integral das 8 páginas).
- Acessibilidade WCAG 2.1 AA: link "pular para o conteúdo", foco visível, navegação por teclado (abas com setas, Esc fecha o menu), ARIA nas abas/menu/montanha, `alt` descritivo, alvos de toque ≥ 44 px, contraste aprovado, respeito a `prefers-reduced-motion`. Auditoria axe-core: 0 violações nas 9 páginas (celular e desktop).
- Performance: fontes auto-hospedadas com subset e `font-display: swap`, imagem principal pré-carregada em AVIF com `fetchpriority="high"`, AVIF/WebP/JPEG responsivos, `loading="lazy"` abaixo da dobra, `width/height` em todas as imagens (CLS 0), 1 CSS e 2 JS pequenos, sem bibliotecas. Lighthouse (celular): Performance 98 · Acessibilidade 100 · Boas práticas 100 · SEO 100.

## 6. Segurança e infraestrutura

- **HTTPS**: forçado pelo GitHub Pages (passo 1.5) + `upgrade-insecure-requests`.
- **Cabeçalhos**: GitHub Pages não permite cabeçalhos HTTP próprios. Por isso o site define, via `<meta>`, a **Content-Security-Policy** (sem scripts/estilos inline, só domínios necessários) e a **Referrer-Policy**.
  Para ter também `Strict-Transport-Security`, `X-Frame-Options`/`frame-ancestors`, `X-Content-Type-Options` e `Permissions-Policy`, coloque o domínio atrás do **Cloudflare (grátis)** com proxy ativo e crie uma regra *Transform Rules → Modify Response Header*:
  ```
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Content-Security-Policy: frame-ancestors 'none'
  ```
- **Backups**: o repositório Git é o backup versionado (cada commit é um ponto de restauração). Recomendado: proteger a branch `main` (Settings → Branches) e manter um clone/mirror em outra conta ou no Drive.
- **Hospedagem**: GitHub Pages (CDN global, 99,9%+, grátis). `security.txt` publicado para relato de vulnerabilidades.

## 7. Pendências conhecidas

- **Fotos dos segmentos (café, suplementos, cosméticos, pet, B2B)**: as fotos do canvas de design não puderam ser exportadas; foram substituídas por ilustrações vetoriais em `docs/assets/img/segmentos/*.svg`. Para usar fotos, salve-as como `cafe.jpg`, etc., e troque a extensão em `content_home.py`/`build.py` (ou mantenha o mesmo nome em `.svg`).
- O link da App Store ainda aponta para `apps.shopify.com/subbly-subscriptions-app`; troque em `INSTALL` quando o app da Everni tiver o endereço definitivo.
- Instagram foi retirado do rodapé até existir um perfil com link.
- Termos de Uso e Política de Privacidade: revisar com advogado (ex.: limitação de responsabilidade e cláusula "não reembolsável" frente ao CDC). A versão em inglês declara que a versão em português prevalece.

## 8. Regenerar imagens (só se mudar logo/fotos)

```bash
pip install pillow playwright matplotlib && python3 -m playwright install chromium
python3 tools/make_icons.py     # favicons e logo
python3 tools/make_images.py    # fotos AVIF/WebP/JPEG + fundo topográfico do CTA
python3 tools/make_og.py        # imagens de compartilhamento PT/EN
python3 tools/build.py
```
