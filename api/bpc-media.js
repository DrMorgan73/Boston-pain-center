// BPC Back Office media API — Vercel Node Serverless Function.
// Session-gated via the bpc_session cookie (same HMAC scheme as middleware.js).
// Media files live in Vercel Blob under bpc-media-files/ ; metadata records
// under bpc-media/<uuid>.json. Files are uploaded directly from the browser
// (serverless functions cap request bodies at ~4.5MB) using a short-lived
// client token issued by this API.
//
// Env required:
//   BPC_ADMIN_SECRET    - HMAC key for the session cookie
//   BLOB_READ_WRITE_TOKEN - Vercel Blob store token (auto-provisioned)
//
// Routes (all require a valid session):
//   GET ?action=token&type=podcast|video|other&name=<file>&mime=<type>
//       -> { token, pathname } — short-lived client upload token scoped to one file
//   GET            -> { items: [metadata records, newest first] }
//   POST {type,title_en,title_es,desc_en,desc_es,category,url,pathname,contentType,size,duration}
//       -> saves the metadata record for an already-uploaded file
//   DELETE ?id=    -> deletes the metadata record and the file blob

import crypto from 'node:crypto';
import { list, del, put } from '@vercel/blob';
import { generateClientTokenFromReadWriteToken } from '@vercel/blob/client';

const PREFIX = 'bpc-media/';
const FILE_PREFIX = 'bpc-media-files/';
const TYPES = ['podcast', 'video', 'other'];
const MAX_BYTES = 500 * 1024 * 1024; // 500 MB

const ALLOWED_MIME = {
  podcast: ['audio/mpeg', 'audio/mp4', 'audio/wav', 'audio/x-wav', 'audio/ogg', 'audio/webm', 'audio/aac', 'audio/x-m4a'],
  video: ['video/mp4', 'video/webm', 'video/quicktime'],
  other: ['application/pdf', 'image/jpeg', 'image/png', 'image/webp'],
};

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

const safeName = (name) =>
  clean(name, 120).replace(/[^a-zA-Z0-9._-]+/g, '-').replace(/^-+|-+$/g, '') || 'file';

async function allRecords() {
  const { blobs } = await list({ prefix: PREFIX, limit: 500 });
  const out = [];
  for (const b of blobs) {
    if (!b.pathname.endsWith('.json')) continue;
    try {
      const r = await fetch(b.url).then((x) => x.json());
      if (r && r.id && r.url) out.push(r);
    } catch { /* skip unreadable */ }
  }
  out.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  return out;
}

export default async function handler(req, res) {
  const sessionUser = (() => {
    const v = getCookie(req.headers.cookie, 'bpc_session');
    if (!validSession(v)) return null;
    return v.split('.')[0];
  })();
  if (!sessionUser) return json(res, { ok: false, error: 'auth' }, 401);
  if (!process.env.BLOB_READ_WRITE_TOKEN)
    return json(res, { ok: false, error: 'blob_not_configured' }, 500);

  try {
    // ---- CLIENT UPLOAD TOKEN (scoped to one file, 10 minutes) ----
    if (req.method === 'GET' && req.query.action === 'token') {
      const type = String(req.query.type || '');
      const mime = String(req.query.mime || '');
      if (!TYPES.includes(type)) return json(res, { ok: false, error: 'bad_type' }, 400);
      if (!ALLOWED_MIME[type].includes(mime))
        return json(res, { ok: false, error: 'bad_mime' }, 400);
      const pathname = `${FILE_PREFIX}${crypto.randomUUID()}-${safeName(req.query.name)}`;
      const token = await generateClientTokenFromReadWriteToken({
        token: process.env.BLOB_READ_WRITE_TOKEN,
        pathname,
        allowedContentTypes: ALLOWED_MIME[type],
        maximumSizeInBytes: MAX_BYTES,
        validUntil: Date.now() + 10 * 60 * 1000,
      });
      return json(res, { ok: true, token, pathname });
    }

    // ---- LIST ----
    if (req.method === 'GET') {
      const records = await allRecords();
      return json(res, { ok: true, items: records });
    }

    // ---- SAVE METADATA (file already uploaded to Blob by the browser) ----
    if (req.method === 'POST') {
      const b = req.body || {};
      const type = String(b.type || '');
      if (!TYPES.includes(type)) return json(res, { ok: false, error: 'bad_type' }, 400);
      const url = clean(b.url, 2000);
      const pathname = clean(b.pathname, 500);
      if (!/^https:\/\/[a-z0-9-]+\.blob\.vercel-storage\.com\//i.test(url))
        return json(res, { ok: false, error: 'bad_url' }, 400);
      if (!pathname.startsWith(FILE_PREFIX))
        return json(res, { ok: false, error: 'bad_pathname' }, 400);
      const contentType = clean(b.contentType, 120);
      if (!ALLOWED_MIME[type].includes(contentType))
        return json(res, { ok: false, error: 'bad_mime' }, 400);
      const size = Number(b.size);
      if (!Number.isFinite(size) || size <= 0 || size > MAX_BYTES)
        return json(res, { ok: false, error: 'bad_size' }, 400);

      const id = crypto.randomUUID();
      const now = new Date();
      const record = {
        id,
        type,
        title: { en: clean(b.title_en, 160), es: clean(b.title_es, 160) },
        description: { en: clean(b.desc_en, 600), es: clean(b.desc_es, 600) },
        category: clean(b.category, 80),
        date: now.toISOString().slice(0, 10),
        duration: clean(b.duration, 20),
        url,
        pathname,
        contentType,
        size,
        createdAt: now.toISOString(),
        by: sessionUser,
      };
      if (!record.title.es && !record.title.en)
        return json(res, { ok: false, error: 'no_title' }, 400);
      await put(`${PREFIX}${id}.json`, JSON.stringify(record), {
        access: 'public', addRandomSuffix: false, contentType: 'application/json',
      });
      return json(res, { ok: true, item: record });
    }

    // ---- DELETE ----
    if (req.method === 'DELETE') {
      const id = clean(req.query.id, 100);
      if (!id || !/^[0-9a-f-]{36}$/i.test(id))
        return json(res, { ok: false, error: 'no_id' }, 400);
      const records = await allRecords();
      const hit = records.find((r) => r.id === id);
      if (!hit) return json(res, { ok: false, error: 'not_found' }, 404);
      try { await del(hit.url); } catch { /* file may already be gone */ }
      const { blobs } = await list({ prefix: `${PREFIX}${id}.json`, limit: 5 });
      for (const bl of blobs) await del(bl.url);
      return json(res, { ok: true });
    }

    return json(res, { ok: false, error: 'method' }, 405);
  } catch (e) {
    return json(res, { ok: false, error: 'failed' }, 500);
  }
}
