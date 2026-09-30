// Public intake endpoint for consultation / second-opinion requests.
// Vercel Node Serverless Function. Validates the submission, stores it as a
// JSON blob under bpc-requests/<uuid>.json (unguessable pathname), and returns
// a human-friendly reference number.
//
// NOTE: this endpoint is built and deployed, but the public booking form is
// intentionally NOT wired to it yet. Request data is patient health information
// (PHI) — live intake stays off until a HIPAA-covered backend (BAA) is in place
// and DrMorgan authorizes it.
//
// Env required:
//   BLOB_READ_WRITE_TOKEN - Vercel Blob store token (auto-provisioned)

import crypto from 'node:crypto';
import { put } from '@vercel/blob';

const PREFIX = 'bpc-requests/';

const json = (res, obj, status = 200) => {
  res.status(status).setHeader('content-type', 'application/json');
  res.end(JSON.stringify(obj));
};

const clean = (v, max) =>
  String(v == null ? '' : v).replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g, '').trim().slice(0, max);
const validEmail = v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, { ok: false }, 405);
  if (!process.env.BLOB_READ_WRITE_TOKEN)
    return json(res, { ok: false, error: 'not_configured' }, 503);

  const b = req.body || {};
  const name = clean(b.name, 120);
  const email = clean(b.email, 160);
  const phone = clean(b.phone, 40);
  const reason = clean(b.reason, 2000);

  if (name.length < 2 || !validEmail(email) || phone.replace(/\D/g, '').length < 7)
    return json(res, { ok: false, error: 'validation' }, 400);
  if (b.consent !== true)
    return json(res, { ok: false, error: 'consent' }, 400);

  const d = new Date();
  const p = n => String(n).padStart(2, '0');
  const ref = `BPC-${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${Math.floor(1000 + Math.random() * 9000)}`;
  const id = crypto.randomUUID();

  const record = {
    id,
    ref,
    type: ['consultation', 'second-opinion', 'telehealth'].includes(b.type) ? b.type : 'consultation',
    createdAt: d.toISOString(),
    name,
    email,
    phone,
    preferredDate: clean(b.preferredDate, 20),
    visitType: clean(b.visitType, 40),
    service: clean(b.service, 120),
    reason,
    language: b.language === 'en' ? 'en' : 'es',
    consent: true,
    status: 'new',
    notes: [],
    sample: false,
  };

  try {
    await put(`${PREFIX}${id}.json`, JSON.stringify(record), {
      access: 'public', addRandomSuffix: false, contentType: 'application/json',
    });
  } catch (e) {
    return json(res, { ok: false, error: 'store_failed' }, 500);
  }
  return json(res, { ok: true, ref });
}
