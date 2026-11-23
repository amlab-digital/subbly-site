/*! Everni · seleção automática de idioma (PT-BR para Brasil e Portugal; EN para o resto)
 * Carregado no <head> (síncrono e pequeno) para redirecionar antes da página pintar quando possível.
 * Ordem de decisão:
 *   1. ?lang=pt|en na URL  -> força e salva a escolha
 *   2. escolha manual salva (botão PT/EN)            -> localStorage "everni_lang"
 *   3. país em cache (consulta anterior, 30 dias)    -> localStorage "everni_geo"
 *   4. país pelo IP (api.country.is, reserva ipapi.co), limite de 1,5 s
 *   5. reserva: fuso horário do aparelho
 * Robôs de busca e ferramentas de teste NUNCA são redirecionados (o Google indexa as duas versões via hreflang).
 */
(function () {
  "use strict";
  var d = document.documentElement;
  d.className = d.className.replace(/\bno-js\b/, "js");

  var PT_COUNTRIES = { BR: 1, PT: 1 };
  var PT_ZONES = [
    "America/Sao_Paulo", "America/Araguaina", "America/Bahia", "America/Belem", "America/Boa_Vista",
    "America/Campo_Grande", "America/Cuiaba", "America/Eirunepe", "America/Fortaleza", "America/Maceio",
    "America/Manaus", "America/Noronha", "America/Porto_Velho", "America/Recife", "America/Rio_Branco",
    "America/Santarem", "Europe/Lisbon", "Atlantic/Madeira", "Atlantic/Azores"
  ];
  var GEO_TTL = 30 * 24 * 3600 * 1000;
  var TIMEOUT = 1500;
  var IP_SERVICES = [
    { url: "https://api.country.is/", parse: function (t) { return JSON.parse(t).country; } },
    { url: "https://ipapi.co/country/", parse: function (t) { return t.trim(); } }
  ];

  var page = d.getAttribute("data-lang") === "en" ? "en" : "pt";

  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function read(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  function alternate(lang) {
    var el = document.querySelector('link[rel="alternate"][hreflang="' + (lang === "pt" ? "pt-BR" : "en") + '"]');
    if (!el) return null;
    try { return new URL(el.getAttribute("href"), location.href).pathname; } catch (e) { return null; }
  }

  function go(lang) {
    if (lang === page) return;
    var path = alternate(lang);
    if (!path || path === location.pathname) return;
    location.replace(path + location.hash);
  }

  // Expõe para o seletor PT/EN do header salvar a escolha manual
  window.everniSetLang = function (lang) { if (lang === "pt" || lang === "en") store("everni_lang", lang); };

  try {
    var ua = navigator.userAgent || "";
    var isBot = navigator.webdriver ||
      /bot|crawl|spider|slurp|archiver|bingpreview|mediapartners|facebookexternalhit|embedly|quora|whatsapp|telegram|discord|linkedin|twitter|skype|pinterest|lighthouse|pagespeed|gtmetrix|headless|prerender|validator|preview/i.test(ua);
    if (isBot) return;

    var q = /[?&]lang=(pt|en)\b/.exec(location.search);
    if (q) { store("everni_lang", q[1]); return; }   // a URL forçada já é a versão desejada

    var saved = read("everni_lang");
    if (saved === "pt" || saved === "en") return go(saved);

    var geo = null;
    try { geo = JSON.parse(read("everni_geo") || "null"); } catch (e) {}
    if (geo && geo.c && Date.now() - geo.t < GEO_TTL) return go(PT_COUNTRIES[geo.c] ? "pt" : "en");

    var decided = false;
    function decide(country, source) {
      if (decided) return;
      decided = true;
      if (country) store("everni_geo", JSON.stringify({ c: country, t: Date.now(), s: source }));
      go(country ? (PT_COUNTRIES[country] ? "pt" : "en") : byTimezone());
    }
    function byTimezone() {
      var tz = "";
      try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) {}
      if (tz) return PT_ZONES.indexOf(tz) !== -1 ? "pt" : "en";
      var l = String((navigator.languages && navigator.languages[0]) || navigator.language || "").toLowerCase();
      return l.indexOf("pt") === 0 ? "pt" : "en";
    }

    if (!window.fetch) return decide(null);
    var deadline = setTimeout(function () { decide(null); }, TIMEOUT);

    (function tryService(i) {
      if (decided || i >= IP_SERVICES.length) { clearTimeout(deadline); return decide(null); }
      var svc = IP_SERVICES[i];
      fetch(svc.url, { cache: "no-store", credentials: "omit", referrerPolicy: "no-referrer" })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then(function (t) {
          var c = String(svc.parse(t) || "").toUpperCase();
          if (!/^[A-Z]{2}$/.test(c)) throw new Error("bad");
          clearTimeout(deadline);
          decide(c, i);
        })
        .catch(function () { tryService(i + 1); });
    })(0);
  } catch (e) {}
})();
