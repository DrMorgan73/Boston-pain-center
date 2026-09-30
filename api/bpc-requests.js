// BPC Back Office data API — Vercel Node Serverless Function.
// Session-gated via the bpc_session cookie (same HMAC scheme as middleware.js).
// Requests live in Vercel Blob under bpc-requests/<uuid>.json with unguessable
// pathnames; the listing is private to the back office and blob URLs never
// appear in public pages.
//
// Env required:
//   BPC_ADMIN_SECRET    - HMAC key for the session cookie
//   BLOB_READ_WRITE_TOKEN - Vercel Blob store token (auto-provisioned)
//
// Routes (all require a valid session):
//   GET            -> { requests: [{id, ref, createdAt, name, type, service, status, sample}] }
//   GET ?id=       -> { request: {...full record...} }
//   PATCH {id, status?, note?} -> updates status and/or appends a staff note
//   POST {sample:true} -> creates a clearly-marked sample request (for demos)
//   DELETE ?id=    -> deletes a request, samples only

import crypto from 'node:crypto';
import { put, list, del } from '@vercel/blob';

const PREFIX = 'bpc-requests/';
const STATUSES = ['new', 'contacted', 'scheduled', 'done', 'archived'];

const json = (res, obj, status = 200) => {
  res.status(status).setHeader('content-type', 'application/json');
  res.end(JSON.stringify(obj));
};

function getCookie(header, name) {
  if (!header) return null;
  for (const part of header.split(';')) {
    const i = part.indexOf('=');
    if (i < 0) continue;
    if (part.slice(0, i).trim() === name) return part.slice(i + 1).trim();
  }
  return null;
}

function validSession(value) {
  const secret = process.env.BPC_ADMIN_SECRET;
  if (!secret || typeof value !== 'string') return false;
  const parts = value.split('.');
  if (parts.length !== 3) return false;
  const [user, exp, sig] = parts;
  if (!/^[A-Za-z0-9_-]{1,64}$/.test(user)) return false;
  if (!/^\d+$/.test(exp)) return false;
  if (Number(exp) * 1000 < Date.now()) return false;
  const expected = crypto.createHmac('sha256', secret).update(user + '.' + exp).digest('hex');
  if (sig.length !== expected.length) return false;
  return crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected));
}

const clean = (v, max) =>
  String(v == null ? '' : v).replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g, '').trim().slice(0, max);

const summary = r => ({
  id: r.id, ref: r.ref, createdAt: r.createdAt, name: r.name,
  type: r.type, service: r.service, status: r.status, sample: !!r.sample,
});

// Reads every request blob (pilot scale: tens of records).
async function allRecords() {
  const { blobs } = await list({ prefix: PREFIX, limit: 500 });
  const out = [];
  for (const b of blobs) {
    if (!b.pathname.endsWith('.json')) continue;
    try {
      const r = await fetch(b.url).then(x => x.json());
      if (r && r.id && r.ref) out.push(r);
    } catch { /* skip unreadable blobs */ }
  }
  out.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  return out;
}

async function saveRecord(r) {
  const blob = await put(`${PREFIX}${r.id}.json`, JSON.stringify(r), {
    access: 'public', addRandomSuffix: false, contentType: 'application/json',
  });
  return blob;
}

export default async function handler(req, res) {
  if (!validSession(getCookie(req.headers.cookie, 'bpc_session')))
    return json(res, { ok: false, error: 'auth' }, 401);
  if (!process.env.BLOB_READ_WRITE_TOKEN)
    return json(res, { ok: false, error: 'blob_not_configured' }, 500);

  try {
    // ---- READ ----
    if (req.method === 'GET') {
      const records = await allRecords();
      if (req.query.id) {
        const hit = records.find(r => r.id === req.query.id);
        if (!hit) return json(res, { ok: false, error: 'not_found' }, 404);
        return json(res, { ok: true, request: hit });
      }
      return json(res, { ok: true, requests: records.map(summary) });
    }

    // ---- SAMPLE (demo data, clearly marked) ----
    if (req.method === 'POST') {
      if (!req.body || req.body.sample !== true)
        return json(res, { ok: false, error: 'bad_request' }, 400);
      const d = new Date();
      const p = n => String(n).padStart(2, '0');
      const id = crypto.randomUUID();
      const record = {
        id,
        ref: `SAMPLE-${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${Math.floor(1000 + Math.random() * 9000)}`,
        type: 'consultation',
        createdAt: d.toISOString(),
        name: 'Sample Patient',
        email: 'sample@example.com',
        phone: '(617) 555-0100',
        preferredDate: '',
        visitType: 'In person',
        service: 'Pain Management',
        reason: 'Sample request — created from the back office to demonstrate the workflow. Safe to delete.',
        language: 'es',
        consent: true,
        status: 'new',
        notes: [],
        sample: true,
      };
      await saveRecord(record);
      return json(res, { ok: true, request: summary(record) });
    }

    // ---- UPDATE ----
    if (req.method === 'PATCH') {
      const { id, status, note } = req.body || {};
      if (!id) return json(res, { ok: false, error: 'no_id' }, 400);
      const records = await allRecords();
      const hit = records.find(r => r.id === id);
      if (!hit) return json(res, { ok: false, error: 'not_found' }, 404);
      let changed = false;
      if (status && STATUSES.includes(status) && status !== hit.status) {
        hit.status = status; changed = true;
      }
      const noteText = clean(note, 2000);
      if (noteText) {
        hit.notes.push({ at: new Date().toISOString(), by: 'staff', text: noteText });
        changed = true;
      }
      if (!changed) return json(res, { ok: true, request: summary(hit) });
      await saveRecord(hit);
      return json(res, { ok: true, request: summary(hit) });
    }

    // ---- DELETE (samples only) ----
    if (req.method === 'DELETE') {
      const id = req.query.id;
      if (!id) return json(res, { ok: false, error: 'no_id' }, 400);
      const records = await allRecords();
      const hit = records.find(r => r.id === id);
      if (!hit) return json(res, { ok: false, error: 'not_found' }, 404);
      if (!hit.sample) return json(res, { ok: false, error: 'cannot_delete_real' }, 403);
      const { blobs } = await list({ prefix: `${PREFIX}${id}.json`, limit: 5 });
      for (const b of blobs) await del(b.url);
      return json(res, { ok: true });
    }

    return json(res, { ok: false, error: 'method' }, 405);
  } catch (e) {
    return json(res, { ok: false, error: 'failed' }, 500);
  }
}
