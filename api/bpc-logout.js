// BPC Back Office sign-out — clears the session cookie.
export default function handler(req, res) {
  res.setHeader('Set-Cookie',
    'bpc_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax; Secure');
  res.status(200).setHeader('content-type', 'application/json');
  res.end(JSON.stringify({ ok: true }));
}
