"""Shared-code access sessions for the hosted Lantern Archive."""
import base64
import hashlib
import hmac
import json
import os
import time


COOKIE_NAME = 'kdm_access'
SESSION_SECONDS = 30 * 24 * 60 * 60


def configured():
    return bool(os.environ.get('KDM_ACCESS_CODE') and os.environ.get('KDM_SESSION_SECRET'))


def valid_code(code):
    expected = os.environ.get('KDM_ACCESS_CODE', '')
    return isinstance(code, str) and bool(expected) and hmac.compare_digest(code, expected)


def _encode(value):
    return base64.urlsafe_b64encode(value).rstrip(b'=').decode('ascii')


def _decode(value):
    padding = '=' * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def create_session(now=None):
    secret = os.environ.get('KDM_SESSION_SECRET', '')
    if not secret:
        return None
    issued = int(time.time() if now is None else now)
    payload = _encode(json.dumps({'exp': issued + SESSION_SECONDS}, separators=(',', ':')).encode('utf-8'))
    signature = _encode(hmac.new(secret.encode('utf-8'), payload.encode('ascii'), hashlib.sha256).digest())
    return f'{payload}.{signature}'


def valid_session(token, now=None):
    secret = os.environ.get('KDM_SESSION_SECRET', '')
    if not isinstance(token, str) or not secret or token.count('.') != 1:
        return False
    payload, signature = token.split('.', 1)
    try:
        expected = hmac.new(secret.encode('utf-8'), payload.encode('ascii'), hashlib.sha256).digest()
        if not hmac.compare_digest(_decode(signature), expected):
            return False
        expiry = json.loads(_decode(payload).decode('utf-8'))['exp']
        return isinstance(expiry, int) and expiry > int(time.time() if now is None else now)
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError):
        return False


def request_has_access(headers):
    if not configured():
        return True
    cookies = headers.get('Cookie', '')
    for cookie in cookies.split(';'):
        name, separator, value = cookie.strip().partition('=')
        if separator and name == COOKIE_NAME:
            return valid_session(value)
    return False
