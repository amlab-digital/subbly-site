/*! Everni · gtm.js — Google Tag Manager com Consent Mode v2 (carregado só quando GTM_ID está definido em tools/build.py). */
(function () {
  "use strict";
  var me = document.currentScript, id = me && me.getAttribute("data-gtm-id");
  if (!id) return;
  window.dataLayer = window.dataLayer || [];
  var gtag = function () { window.dataLayer.push(arguments); };
  window.gtag = window.gtag || gtag;
  // Espaço Econômico Europeu + Reino Unido + Suíça: tudo negado até existir um banner de consentimento (CMP).
  var EEA = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
    "PL", "PT", "RO", "SK", "SI", "ES", "SE", "IS", "LI", "NO", "GB", "CH"];
  gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied", region: EEA, wait_for_update: 500 });
  // Demais países: medição e conversões de anúncios liberadas; personalização de anúncios desligada por padrão.
  gtag("consent", "default", { ad_storage: "granted", ad_user_data: "granted", ad_personalization: "denied", analytics_storage: "granted" });
  gtag("set", "ads_data_redaction", true);
  window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js", site_lang: document.documentElement.getAttribute("data-lang") || "" });
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(id);
  document.head.appendChild(s);
})();
