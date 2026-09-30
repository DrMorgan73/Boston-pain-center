/* BPC Back Office — shared helpers (staff UI, English). */
(function () {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Fetch wrapper: on 401 the session is gone -> back to the sign-in page.
  async function api(path, opts) {
    opts = opts || {};
    const headers = Object.assign({}, opts.headers || {});
    if (opts.body && !headers['content-type']) headers['content-type'] = 'application/json';
    const r = await fetch(path, Object.assign({}, opts, { headers }));
    if (r.status === 401) { location.href = '/admin/login.html'; throw new Error('auth'); }
    let data = null;
    try { data = await r.json(); } catch (e) { /* non-JSON */ }
    if (!r.ok || !data || data.ok === false) {
      const err = new Error((data && data.error) || 'request_failed');
      err.code = (data && data.error) || 'request_failed';
      err.status = r.status;
      throw err;
    }
    return data;
  }

  function logout() {
    fetch('/api/bpc-logout', { method: 'POST' })
      .finally(function () { location.href = '/admin/login.html'; });
  }

  var STATUS_LABELS = {
    new: 'New', contacted: 'Contacted', scheduled: 'Scheduled',
    done: 'Done', archived: 'Archived'
  };
  var TYPE_LABELS = {
    consultation: 'Consultation', 'second-opinion': 'Second opinion', telehealth: 'Telehealth'
  };

  function pill(status, sample) {
    if (sample) return '<span class="pill sample">Sample</span>';
    var cls = STATUS_LABELS[status] ? status : 'new';
    return '<span class="pill ' + cls + '">' + esc(STATUS_LABELS[cls]) + '</span>';
  }

  function fmtDate(iso) {
    try {
      return new Date(iso).toLocaleString('en-US', {
        month: 'short', day: 'numeric', year: 'numeric',
        hour: 'numeric', minute: '2-digit'
      });
    } catch (e) { return iso || ''; }
  }

  window.BPCAdmin = { esc, api, logout, pill, fmtDate, STATUS_LABELS, TYPE_LABELS };
})();
