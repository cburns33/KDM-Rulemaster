const encoder = new TextEncoder();
const decoder = new TextDecoder();

function cookie(request, name) {
  for (const item of (request.headers.get('cookie') || '').split(';')) {
    const [key, ...value] = item.trim().split('=');
    if (key === name) return value.join('=');
  }
  return null;
}

function decode(value) {
  const padded = value.replace(/-/g, '+').replace(/_/g, '/') + '='.repeat((4 - value.length % 4) % 4);
  const binary = atob(padded);
  return Uint8Array.from(binary, character => character.charCodeAt(0));
}

function equal(first, second) {
  if (first.length !== second.length) return false;
  let difference = 0;
  for (let index = 0; index < first.length; index += 1) difference |= first[index] ^ second[index];
  return difference === 0;
}

async function hasAccess(request) {
  const secret = process.env.KDM_SESSION_SECRET;
  const token = cookie(request, 'kdm_access');
  if (!secret || !token || token.split('.').length !== 2) return false;
  const [payload, signature] = token.split('.');
  try {
    const key = await crypto.subtle.importKey('raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
    const expected = new Uint8Array(await crypto.subtle.sign('HMAC', key, encoder.encode(payload)));
    const body = JSON.parse(decoder.decode(decode(payload)));
    return equal(decode(signature), expected) && Number.isInteger(body.exp) && body.exp > Math.floor(Date.now() / 1000);
  } catch {
    return false;
  }
}

export default async function middleware(request) {
  if (!process.env.KDM_ACCESS_CODE || !process.env.KDM_SESSION_SECRET || await hasAccess(request)) return;
  const url = new URL(request.url);
  url.pathname = '/access.html';
  url.search = '';
  url.searchParams.set('next', request.nextUrl.pathname + request.nextUrl.search);
  return Response.redirect(url, 302);
}

export const config = {
  matcher: ['/((?!access\\.html|access\\.js|style\\.css|api/access).*)'],
};
