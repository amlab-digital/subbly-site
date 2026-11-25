/*! Everni · site.js — interações (menu, abas, calculadora, montanha, formulário). Sem dependências. */
(function () {
"use strict";
var $ = function (s, c) { return (c || document).querySelector(s); };
var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
/* ---------- Seletor de idioma: salva a escolha manual ---------- */
$$("[data-set-lang]").forEach(function (a) {
a.addEventListener("click", function () {
if (window.everniSetLang) window.everniSetLang(a.getAttribute("data-set-lang"));
});
});
/* ---------- Índice das páginas legais: aberto no desktop, recolhido no celular ---------- */
var toc = $(".toc details");
if (toc && window.matchMedia("(min-width: 64em)").matches) toc.open = true;
/* ---------- Menu mobile ---------- */
var toggle = $(".menu-toggle"), nav = $("#site-nav");
if (toggle && nav) {
var close = function (focusBack) {
toggle.setAttribute("aria-expanded", "false");
nav.classList.remove("is-open");
if (focusBack) toggle.focus();
};
toggle.addEventListener("click", function () {
var open = toggle.getAttribute("aria-expanded") !== "true";
toggle.setAttribute("aria-expanded", String(open));
nav.classList.toggle("is-open", open);
if (open) { var first = $("a", nav); if (first) first.focus(); }
});
nav.addEventListener("click", function (e) { if (e.target.closest("a")) close(false); });
document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("is-open")) close(true); });
window.addEventListener("resize", function () { if (window.innerWidth >= 1200) close(false); }, { passive: true });
}
/* ---------- Abas "Como funciona" (padrão WAI-ARIA Tabs) ---------- */
var tabs = $$('[role="tab"]');
if (tabs.length) {
var select = function (tab, focus) {
tabs.forEach(function (t) {
var on = t === tab;
t.setAttribute("aria-selected", String(on));
t.tabIndex = on ? 0 : -1;
var p = document.getElementById(t.getAttribute("aria-controls"));
if (p) { p.classList.toggle("is-active", on); p.hidden = false; }
});
if (focus) tab.focus();
};
tabs.forEach(function (t, i) {
t.addEventListener("click", function () { select(t); });
t.addEventListener("keydown", function (e) {
var n = null;
if (e.key === "ArrowRight") n = tabs[(i + 1) % tabs.length];
else if (e.key === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
else if (e.key === "Home") n = tabs[0];
else if (e.key === "End") n = tabs[tabs.length - 1];
if (n) { e.preventDefault(); select(n, true); }
});
});
var fromHash = function () {
var id = decodeURIComponent(location.hash.slice(1));
if (!id) return;
var panel = document.getElementById(id);
if (!panel || !panel.classList.contains("panel")) return;
var tab = $('[aria-controls="' + id + '"]');
if (tab) select(tab);
var sec = document.getElementById("produto");
if (sec) sec.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
};
window.addEventListener("hashchange", fromHash);
fromHash();
}
/* ---------- Calculadora ---------- */
var calc = $("#calc");
if (calc) {
var cfg = JSON.parse(calc.getAttribute("data-config"));
var range = $("#calc-gmv"), chips = $$(".chip", calc), list = $("#calc-rows");
var state = { idx: Number(range.value), ticket: Number((chips.filter(function (c) { return c.getAttribute("aria-pressed") === "true"; })[0] || chips[0]).getAttribute("data-v")) };
var nf = new Intl.NumberFormat(cfg.locale, { maximumFractionDigits: 0 });
var fmt = function (n) { return nf.format(Math.round(n)); };
var tierFor = function (gmv) {
for (var i = 0; i < cfg.tiers.length; i++) { if (cfg.tiers[i].max === null || gmv <= cfg.tiers[i].max) return cfg.tiers[i]; }
return cfg.tiers[cfg.tiers.length - 1];
};
var render = function () {
var gmv = cfg.steps[state.idx], orders = Math.round(gmv / state.ticket), tier = tierFor(gmv), ev = gmv * tier.rate;
var all = cfg.competitors.map(function (c) { return { name: c.name, formula: c.formula, cost: c.fixed + gmv * c.pct + orders * c.perOrder, everni: false }; });
var comps = all.slice();
all.push({ name: "Everni", formula: cfg.t.everniFormula.replace("{rate}", tier.label), cost: ev, everni: true });
all.sort(function (a, b) { return b.cost - a.cost; });
var max = all[0].cost;
var html = all.map(function (r) {
var w = Math.max(2, Math.round(r.cost / max * 1000) / 10);
return '<li class="row' + (r.everni ? " row--everni" : "") + '"><div class="row__top"><div><p class="row__name">' + r.name +
'</p><p class="row__formula">' + r.formula + '</p></div><span class="row__cost">' + cfg.t.cur + fmt(r.cost) + cfg.t.perMonth +
'</span></div><div class="row__track"><div class="row__bar" data-w="' + w + '"></div></div></li>';
}).join("");
list.innerHTML = html;
$$(".row__bar", list).forEach(function (b) { b.style.width = b.getAttribute("data-w") + "%"; });
var costs = comps.map(function (c) { return c.cost; });
var minC = Math.min.apply(null, costs), maxC = Math.max.apply(null, costs);
var sMin = (minC - ev) * 12, sMax = (maxC - ev) * 12;
$("#calc-gmv-out").textContent = cfg.t.cur + fmt(gmv);
range.setAttribute("aria-valuetext", cfg.t.cur + fmt(gmv));
$("#calc-orders").textContent = fmt(orders);
$("#calc-save").textContent = sMin > 0 ? cfg.t.cur + fmt(sMin) + cfg.t.to + cfg.t.cur2 + fmt(sMax) : cfg.t.upTo + cfg.t.cur + fmt(sMax);
$("#calc-pct").textContent = Math.round((1 - ev / minC) * 100) + "%" + cfg.t.pctTo + Math.round((1 - ev / maxC) * 100) + "%";
$("#calc-rate").textContent = tier.label;
};
var used = false;
var track = function () { if (used || !window.dataLayer) return; used = true; window.dataLayer.push({ event: "calculator_use", gmv: cfg.steps[state.idx], ticket: state.ticket }); };
range.addEventListener("input", function () { state.idx = Number(range.value) || 0; render(); });
range.addEventListener("change", track);
chips.forEach(function (c) {
c.addEventListener("click", function () {
chips.forEach(function (x) { x.setAttribute("aria-pressed", String(x === c)); });
state.ticket = Number(c.getAttribute("data-v"));
render();
track();
});
});
render();
}
/* ---------- Montanha interativa ---------- */
var mt = $("#mt");
if (mt) {
var stage = $(".mt__stage", mt), wps = $$(".wp", mt), steps = $$(".mt__step", mt), segs = $$(".mt__seg", mt);
var peak = 1, touched = false, hovering = false;
var setPeak = function (n) {
peak = n;
wps.forEach(function (w, i) {
var k = i + 1;
w.classList.toggle("is-on", k === n);
w.classList.toggle("is-done", k < n);
w.classList.toggle("is-next", k === n + 1);
$(".wp__btn", w).setAttribute("aria-pressed", String(k === n));
var card = $(".wp__card", w); if (card) card.setAttribute("aria-hidden", String(k !== n));
});
steps.forEach(function (s, i) {
var k = i + 1;
s.classList.toggle("is-on", k === n);
s.classList.toggle("is-done", k < n);
s.setAttribute("aria-pressed", String(k === n));
});
segs.forEach(function (s, i) { s.classList.toggle("is-drawn", n >= i + 2); });
};
var pick = function (n) { return function () { touched = true; if (peak !== n) setPeak(n); }; };
wps.forEach(function (w, i) {
var b = $(".wp__btn", w), fn = pick(i + 1);
b.addEventListener("mouseenter", fn); b.addEventListener("focus", fn); b.addEventListener("click", fn);
});
steps.forEach(function (s, i) {
var fn = pick(i + 1);
s.addEventListener("mouseenter", fn); s.addEventListener("focus", fn); s.addEventListener("click", fn);
});
if (!reduceMotion && window.matchMedia("(hover: hover)").matches) {
stage.addEventListener("mousemove", function (e) {
hovering = true;
var r = stage.getBoundingClientRect();
var px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
stage.style.setProperty("--ry", (px * 14).toFixed(2) + "deg");
stage.style.setProperty("--rx", (-py * 8).toFixed(2) + "deg");
});
stage.addEventListener("mouseleave", function () {
hovering = false;
stage.style.setProperty("--ry", "0deg");
stage.style.setProperty("--rx", "0deg");
});
}
setPeak(1);
if (!reduceMotion && "IntersectionObserver" in window) {
var timer = null;
new IntersectionObserver(function (entries) {
entries.forEach(function (en) {
if (en.isIntersecting && !timer) {
timer = setInterval(function () { if (!touched && !hovering) setPeak((peak % 4) + 1); }, 4200);
} else if (!en.isIntersecting && timer) { clearInterval(timer); timer = null; }
});
}, { threshold: 0.25 }).observe(mt);
}
}
/* ---------- Medição: cliques em CTAs vão para o dataLayer (GTM). Sem GTM, nada é enviado. ---------- */
document.addEventListener("click", function (e) {
if (!window.dataLayer) return;
var a = e.target.closest ? e.target.closest("a") : null;
if (!a) return;
var href = a.getAttribute("href") || "", type = a.getAttribute("data-track");
if (!type) {
if (/apps\.shopify\.com/.test(href)) type = "install";
else if (/wa\.me\//.test(href)) type = "whatsapp";
else if (/^mailto:/.test(href)) type = "email";
else return;
}
var sec = a.closest("section[id], .site-header, .topbar, footer");
window.dataLayer.push({ event: "cta_click", cta_type: type, cta_text: (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80),
cta_location: sec ? (sec.id || sec.className.split(" ")[0]) : "", link_url: a.href });
}, true);
/* ---------- Newsletter: honeypot + tempo mínimo + envio via fetch ---------- */
$$("form[data-newsletter]").forEach(function (form) {
var started = Date.now();
var status = $(".form-status", form);
var msg = JSON.parse(form.getAttribute("data-msg"));
form.addEventListener("submit", function (e) {
e.preventDefault();
var email = form.elements.email.value.trim();
var say = function (t, err) { status.textContent = t; status.classList.toggle("is-error", !!err); };
if (form.elements._gotcha && form.elements._gotcha.value) return say(msg.ok);       // robô: finge sucesso
if (Date.now() - started < 2500) return say(msg.slow, true);                       // envio rápido demais
if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return say(msg.invalid, true);
var action = form.getAttribute("action") || "";
if (/SEU_FORM_ID/.test(action)) {                                                   // endpoint não configurado: usa e-mail
location.href = "mailto:" + form.getAttribute("data-fallback") + "?subject=" + encodeURIComponent(msg.subject) + "&body=" + encodeURIComponent(email);
return say(msg.mail);
}
say(msg.sending);
fetch(action, { method: "POST", headers: { Accept: "application/json" }, body: new FormData(form) })
.then(function (r) { if (!r.ok) throw new Error(r.status); form.reset(); say(msg.ok); if (window.dataLayer) window.dataLayer.push({ event: "newsletter_signup" }); })
.catch(function () { say(msg.fail, true); });
});
});
})();
