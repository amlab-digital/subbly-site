/*
 * Subbly — geo language redirect
 * Detects the visitor's country via IP geolocation and, when they are NOT in
 * Brazil, redirects them to the English version (/en/). Runs once per session
 * and never bounces anyone already on the English site.
 */
(function () {
  'use strict';

  var KEY = 'subbly_geo_checked';
  var EN_PATH = '/en/';
  var TIMEOUT_MS = 4000;

  function storage() {
    try { return window.sessionStorage; } catch (e) { return null; }
  }

  var path = window.location.pathname.replace(/\/+$/, '') || '/';
  if (/^\/en(\/|$)/.test(path)) return; // already on the English site

  var store = storage();
  if (store && store.getItem(KEY)) return; // already decided this session

  function remember() {
    if (store) { try { store.setItem(KEY, '1'); } catch (e) {} }
  }

  function goEnglish() {
    remember();
    window.location.replace(EN_PATH + window.location.search);
  }

  function countryCode(data) {
    if (!data) return '';
    return String(data.country_code || data.country || data.countryCode || '').toUpperCase();
  }

  function isBrazil(code) {
    return code === 'BR' || code === 'BRA' || code === '076';
  }

  // Free, no-key HTTPS geolocation endpoints (primary → fallback).
  var endpoints = ['https://ipwho.is/', 'https://ipapi.co/json/'];

  function tryNext(i) {
    if (i >= endpoints.length) { remember(); return; } // offline / blocked → stay on PT

    var controller = (typeof AbortController !== 'undefined') ? new AbortController() : null;
    var timer = controller ? setTimeout(function () { controller.abort(); }, TIMEOUT_MS) : null;

    fetch(endpoints[i], {
      mode: 'cors',
      signal: controller ? controller.signal : undefined
    })
      .then(function (res) { return res.ok ? res.json() : Promise.reject(res.status); })
      .then(function (data) {
        var code = countryCode(data);
        if (!code) { tryNext(i + 1); return; }
        if (isBrazil(code)) { remember(); } else { goEnglish(); }
      })
      .catch(function () { tryNext(i + 1); })
      .finally(function () { if (timer) clearTimeout(timer); });
  }

  // Manual language choice wins: remember it so a return visit isn't bounced.
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('[data-lang-link]') : null;
    if (a) remember();
  }, true);

  tryNext(0);
})();
