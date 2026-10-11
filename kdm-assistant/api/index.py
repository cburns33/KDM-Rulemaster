"""Stateless Vercel API for Lantern Archive."""
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import json
import os
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import resolve, search
from records import RECORDS
from sol_answer import SolUnavailable, answer as sol_answer, status as sol_status
from access import COOKIE_NAME, SESSION_SECONDS, configured as access_configured, create_session, request_has_access, valid_code

DATA = ROOT / 'data'
MANIFEST = json.loads((DATA / 'manifest.json').read_text(encoding='utf-8'))

for page in MANIFEST:
    record = next((r for r in RECORDS if r['original'] == page['original']), None)
    if record is None:
        record = next((r for r in RECORDS if page['original'] in r.get('supporting_originals', [])), None)
    page.update(reviewed=record is not None, record_id=record['id'] if record else None)
    if record:
        page['title'] = record['title']


def enrich(record):
    if not record:
        return None
    page = next(p for p in MANIFEST if p['original'] == record['original'])
    sources = [page] + [next(p for p in MANIFEST if p['original'] == original) for original in record.get('supporting_originals', [])]
    return {**record, 'source': page, 'sources': sources, 'image': f"/pages/{page['revised']}.jpg"}


def library():
    return {
        'pages': MANIFEST,
        'records': [enrich(record) for record in RECORDS],
        'mode': 'Reviewed rules lookup',
        'edition': '1.5',
        'model': hosted_model_status(),
        'hosting': 'vercel',
    }


def hosted_model_status():
    model = sol_status()
    if os.environ.get('KDM_ENABLE_SOL') != 'true':
        return {**model, 'configured': False}
    return model


def ask(body):
    question = body.get('question', '')
    if not isinstance(question, str) or not question.strip() or len(question) > 4000:
        raise ValueError('Enter a question of up to 4,000 characters')
    use_model = body.get('use_model', False)
    if not isinstance(use_model, bool):
        raise ValueError('Use Sol must be true or false')
    context = body.get('context', {})
    if not isinstance(context, dict):
        raise ValueError('Conversation context is invalid')
    result = resolve(question, context, body.get('record_id'), body.get('table_id'), body.get('roll'), body.get('oven', 'unknown'))
    if use_model and result['status'] == 'reference' and result['record'] and hosted_model_status()['configured']:
        model_records = [result['record']] + result.get('related_records', [])
        try:
            result['answer'] = sol_answer(question, model_records)
            result['status'] = 'model-reference'
            result['model'] = {'used': True, 'name': 'GPT-6 Sol'}
        except SolUnavailable:
            result['model'] = {'used': False, 'name': 'GPT-6 Sol', 'message': 'Sol was unavailable. Showing the local reviewed reference.'}
    elif use_model and result['status'] == 'reference':
        result['model'] = {'used': False, 'name': 'GPT-6 Sol', 'message': 'Sol is disabled for this hosted deployment.'}
    result['record'] = enrich(result['record'])
    result['related_records'] = [enrich(record) for record in result.get('related_records', [])]
    return {'chat_id': secrets.token_hex(12), **result}


class handler(BaseHTTPRequestHandler):
    def send_json(self, status, body, headers=None):
        payload = json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(payload)

    def denied(self):
        return self.send_json(401, {'error': 'Enter the shared access code to use Lantern Archive.'})

    def route(self):
        uri = urlparse(self.path)
        query = parse_qs(uri.query)
        route = query.get('route', [''])[0]
        if route:
            return f'/api/{route}', query
        return uri.path, query

    def do_GET(self):
        path, query = self.route()
        if not request_has_access(self.headers):
            return self.denied()
        if path == '/api/library':
            return self.send_json(200, library())
        if path == '/api/search':
            question = query.get('q', [''])[0][:2000]
            return self.send_json(200, [enrich(record) for record in search(question)])
        if path == '/api/health':
            return self.send_json(200, {'ok': True, 'app': 'lantern-archive', 'pages': len(MANIFEST), 'records': len(RECORDS), 'sol_configured': sol_status()['configured'], 'hosting': 'vercel'})
        if path == '/api/chats':
            return self.send_json(200, [])
        return self.send_json(404, {'error': 'Not found'})

    def do_POST(self):
        path, _ = self.route()
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length < 1 or length > 16000:
                raise ValueError('Request is empty or too large')
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError('Expected an object')
            if path == '/api/access':
                if not access_configured():
                    return self.send_json(503, {'error': 'Hosted access has not been configured.'})
                if not valid_code(body.get('code')):
                    return self.send_json(401, {'error': 'The access code is incorrect.'})
                session = create_session()
                cookie = f'{COOKIE_NAME}={session}; Path=/; Max-Age={SESSION_SECONDS}; HttpOnly; Secure; SameSite=Lax'
                return self.send_json(200, {'ok': True}, {'Set-Cookie': cookie})
            if not request_has_access(self.headers):
                return self.denied()
            if path == '/api/ask':
                return self.send_json(200, ask(body))
            if path == '/api/corrections':
                return self.send_json(200, {'saved': False, 'message': 'Correction reports are available in the local app only.'})
            return self.send_json(404, {'error': 'Not found'})
        except (ValueError, TypeError, KeyError) as error:
            return self.send_json(400, {'error': str(error)})
