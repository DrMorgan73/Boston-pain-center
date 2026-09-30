// BPC Back Office gate — Vercel Edge Middleware.
// Protects "/admin/*" (except the sign-in page). Unauthenticated visitors are
// redirected to /admin/login.html. Public site pages are untouched.
//
// Env required: BPC_ADMIN_SECRET (HMAC key for the session cookie).

export const config = { matcher: ['/admin', '/admin/:path*'] };

const enc = new TextEncoder();

async function hmacHex(secret, data) {
  const key = await crypto.subtle.importKey(
    'raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(data));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
}

function timingSafeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

function getCookie(header, name) {
  if (!header) return null;
  for (const part of header.split(';')) {
    const i = part.indexOf('=');
    if (i < 0) continue;
    if (part.slice(0, i).trim() === name) return part.slice(i + 1).trim();
  }
  return null;
}

async function validSession(value) {
  const secret = process.env.BPC_ADMIN_SECRET;
  if (!secret) return false;
  const parts = String(value).split('.');
  if (parts.length !== 3) return false;
  const [user, exp, sig] = parts;
  if (!/^[A-Za-z0-9_-]{1,64}$/.test(user)) return false;
  if (!/^\d+$/.test(exp)) return false;
  if (Number(exp) * 1000 < Date.now()) return false;
  const expected = await hmacHex(secret, user + '.' + exp);
  return timingSafeEqual(sig, expected);
}

export default async function middleware(request) {
  const { pathname } = new URL(request.url);
  // The sign-in page itself must stay public.
  if (pathname === '/admin/login.html') return undefined;
  const session = getCookie(request.headers.get('cookie'), 'bpc_session');
  if (session && (await validSession(session))) return undefined;
  return Response.redirect(new URL('/admin/login.html', request.url));
}
