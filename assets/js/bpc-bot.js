/* Boston Pain Center — visitor assistant engine (v1).
   Rules-based FAQ matcher, fully client-side. No network requests, no
   cookies, no storage of anything the visitor types. Language follows the
   site's EN/ES toggle (main.js dispatches 'bpc-lang'). */
(function () {
  'use strict';
  var DATA = (typeof window !== 'undefined' && window.BPC_BOT_DATA) || null;
  if (!DATA) return;

  function norm(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
  }
  /* The class above strips combining diacritical marks (U+0300–U+036F)
     after NFD decomposition, so accented and unaccented queries match. */

  var EMERGENCY = ['911', 'emergencia', 'emergency', 'urgent', 'urgencia',
    'chest pain', 'dolor de pecho', 'difficulty breathing', 'no puedo respirar',
    'overdose', 'sobredosis', 'unconscious', 'inconsciente', 'bleeding', 'sangrado'];
  var GUARD = ['tengo', 'me duele', 'siento', 'i have pain', 'i suffer',
    'should i', 'debo', 'puedo tomar', 'can i take', 'diagnose', 'que tengo',
    'what do i have', 'do i have'];

  function includesAny(hay, list) {
    for (var i = 0; i < list.length; i++) {
      if (hay.indexOf(list[i]) !== -1) return true;
    }
    return false;
  }

  function match(q) {
    var nq = norm(q);
    if (!nq) return null;
    if (includesAny(nq, EMERGENCY)) return { kind: 'emergency' };
    var best = null, bestScore = 0;
    DATA.faq.forEach(function (entry) {
      var score = 0;
      ['en', 'es'].forEach(function (l) {
        (entry.kw[l] || []).forEach(function (kw) {
          var nk = norm(kw);
          if (nk && nq.indexOf(nk) !== -1) score += nk.split(' ').length;
        });
      });
      if (score > bestScore) { bestScore = score; best = entry; }
    });
    if (best) return { kind: 'faq', entry: best };
    if (includesAny(nq, GUARD)) return { kind: 'guard' };
    return { kind: 'fallback' };
  }

  function curLang() {
    try {
      var l = document.documentElement.getAttribute('lang');
      if (l === 'en' || l === 'es') return l;
    } catch (e) {}
    return 'es';
  }

  function linkPrefix() {
    try {
      return window.location.pathname.indexOf('/guides/') !== -1 ? '../' : '';
    } catch (e) { return ''; }
  }

  function answerFor(q, lang) {
    var m = match(q);
    if (!m) return null;
    lang = (lang === 'en' || lang === 'es') ? lang : 'es';
    if (m.kind === 'emergency') return { text: DATA.emergency[lang] };
    if (m.kind === 'guard') {
      return { text: DATA.guard[lang],
        link: { href: 'booking.html', en: 'Request a Consultation', es: 'Solicitar una consulta' } };
    }
    if (m.kind === 'fallback') {
      return { text: DATA.fallback[lang],
        link: { href: 'contact.html', en: 'Contact Us', es: 'Contáctenos' } };
    }
    var e = m.entry;
    var out = { text: e.a[lang] || e.a.es };
    if (e.link) out.link = e.link;
    return out;
  }

  /* Exposed for testing/debugging only; the widget below is the interface. */
  if (typeof window !== 'undefined') {
    window.BPC_BOT_MATCH = match;
    window.BPC_BOT_ANSWER = answerFor;
  }

  /* ---------- widget UI (browser only) ---------- */
  if (typeof document === 'undefined') return;

  function $(id) { return document.getElementById(id); }

  function init() {
    var root = $('bpc-bot');
    if (!root) return;
    var btn = $('bpc-bot-btn'), panel = $('bpc-bot-panel'),
        title = $('bpc-bot-title'), msgs = $('bpc-bot-msgs'),
        chipsEl = $('bpc-bot-chips'), form = $('bpc-bot-form'),
        input = $('bpc-bot-input'), sendBtn = $('bpc-bot-send'),
        closeBtn = $('bpc-bot-close'), disc = $('bpc-bot-disc');
    if (!btn || !panel || !msgs || !form || !input) return;

    var opened = false;

    function ui() { return DATA.ui[curLang()] || DATA.ui.es; }

    function renderChrome() {
      var u = ui();
      title.textContent = u.title;
      input.setAttribute('placeholder', u.placeholder);
      sendBtn.textContent = u.send;
      closeBtn.setAttribute('aria-label', u.close);
      btn.setAttribute('aria-label', u.open);
      disc.textContent = u.disclaimer;
      chipsEl.innerHTML = '';
      u.chips.forEach(function (c) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'bpc-bot-chip';
        b.textContent = c;
        b.addEventListener('click', function () { send(c); });
        chipsEl.appendChild(b);
      });
    }

    function addMsg(text, who, link) {
      var d = document.createElement('div');
      d.className = 'bpc-bot-msg ' + who;
      var p = document.createElement('p');
      p.textContent = text;
      d.appendChild(p);
      if (link) {
        var a = document.createElement('a');
        a.href = linkPrefix() + link.href;
        a.textContent = link[curLang()] || link.en || link.href;
        d.appendChild(a);
      }
      msgs.appendChild(d);
      msgs.scrollTop = msgs.scrollHeight;
    }

    function send(q) {
      var query = (q || '').trim();
      if (!query) return;
      var mine = document.createElement('div');
      mine.className = 'bpc-bot-msg user';
      var p = document.createElement('p');
      p.textContent = query;
      mine.appendChild(p);
      msgs.appendChild(mine);
      var ans = answerFor(query, curLang());
      if (ans) addMsg(ans.text, 'bot', ans.link);
      msgs.scrollTop = msgs.scrollHeight;
    }

    btn.addEventListener('click', function () {
      var hidden = panel.hasAttribute('hidden');
      if (hidden) {
        panel.removeAttribute('hidden');
        if (!opened) {
          opened = true;
          var g = null;
          DATA.faq.forEach(function (e) { if (e.id === 'greeting') g = e; });
          if (g) addMsg(g.a[curLang()] || g.a.es, 'bot', null);
        }
        input.focus();
      } else {
        panel.setAttribute('hidden', '');
      }
    });
    closeBtn.addEventListener('click', function () { panel.setAttribute('hidden', ''); });
    panel.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') panel.setAttribute('hidden', '');
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = input.value;
      input.value = '';
      send(v);
      input.focus();
    });
    document.addEventListener('bpc-lang', renderChrome);
    renderChrome();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
