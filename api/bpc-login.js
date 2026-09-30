// BPC Back Office sign-in — Vercel Node Serverless Function.
// POST {username, password} as JSON. Constant-time compare against env
// credentials; on success sets the signed `bpc_session` cookie (HttpOnly, 7 days).
//
// Env required:
//   BPC_ADMIN_USER   - the staff sign-in username
//   BPC_ADMIN_PASS   - the staff sign-in password
//   BPC_ADMIN_SECRET - HMAC key for the session cookie (long random string)

import crypto from 'node:crypto';

const json = (res, obj, status = 200) => {
  res.status(status).setHeader('content-type', 'application/json');
  res.end(JSON.stringify(obj));
};

function safeEq(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  const ab = Buffer.from(a), bb = Buffer.from(b);
  if (ab.length !== bb.length) return false;
  return crypto.timingSafeEqual(ab, bb);
}

export default function handler(req, res) {
  if (req.method !== 'POST') return json(res, { ok: false }, 405);

  const { username, password } = req.body || {};
  const expUser = (process.env.BPC_ADMIN_USER || '').trim();
  const expPass = process.env.BPC_ADMIN_PASS || '';
  const secret = process.env.BPC_ADMIN_SECRET || '';

  let ok = false;
  if (username && password && expUser && expPass && secret &&
      /^[A-Za-z0-9_.@-]{1,64}$/.test(String(username))) {
    ok = safeEq(String(username).trim(), expUser) && safeEq(String(password), expPass);
  }
  if (!ok) return json(res, { ok: false }, 401);

  const user = String(username).trim();
  const exp = Math.floor(Date.now() / 1000) + 7 * 24 * 3600; // 7 days
  const sig = crypto.createHmac('sha256', secret).update(user + '.' + exp).digest('hex');
  res.setHeader('Set-Cookie',
    `bpc_session=${user}.${exp}.${sig}; Path=/; Max-Age=604800; HttpOnly; SameSite=Lax; Secure`);
  return json(res, { ok: true });
}
