"""Loopback-only rule reference app. Runs on Python's standard library."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import argparse
import json
import mimetypes
import secrets
import sqlite3
import time
import webbrowser
from engine import resolve, search
from records import RECORDS
from sol_answer import SolUnavailable, answer as sol_answer, status as sol_status

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
MANIFEST = []

@contextmanager
def connect():
    db = sqlite3.connect(DATA / 'history.sqlite3', timeout=10)
    db.row_factory = sqlite3.Row
    try:
        with db:
            yield db
    finally:
        db.close()

def init():
    global MANIFEST
    if not (DATA / 'manifest.json').exists():
        from prepare import prepare
        prepare()
    MANIFEST = json.loads((DATA / 'manifest.json').read_text(encoding='utf-8'))
    # Review coverage follows current records, including continuation pages.
    for page in MANIFEST:
        record = next((r for r in RECORDS if r['original'] == page['original']), None)
        if record is None:
            record = next((r for r in RECORDS if page['original'] in r.get('supporting_originals', [])), None)
        page.update(reviewed=record is not None, record_id=record['id'] if record else None)
        if record:
            page['title'] = record['title']
    with connect() as db:
        db.executescript('''CREATE TABLE IF NOT EXISTS chats (id TEXT PRIMARY KEY, title TEXT NOT NULL, context TEXT NOT NULL DEFAULT '{}', created REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, chat_id TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, payload TEXT);
        CREATE TABLE IF NOT EXISTS corrections (id INTEGER PRIMARY KEY, record_id TEXT NOT NULL, note TEXT NOT NULL, created REAL NOT NULL);''')

def enrich(record):
    if not record:
        return None
    page = next(p for p in MANIFEST if p['original'] == record['original'])
    sources = [page] + [next(p for p in MANIFEST if p['original'] == original) for original in record.get('supporting_originals', [])]
    return {**record, 'source': page, 'sources': sources, 'image': f"/pages/{page['revised']}.jpg"}

class Handler(BaseHTTPRequestHandler):
    def send(self, status, body, kind='application/json; charset=utf-8'):
        if not isinstance(body, bytes):
            body = json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'self'; img-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def allowed(self):
        return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}')

    def do_GET(self):
        if not self.allowed():
            return self.send(403, {'error': 'Local requests only'})
        uri = urlparse(self.path)
        path = uri.path
        if path == '/api/library':
            return self.send(200, {'pages': MANIFEST, 'records': [enrich(r) for r in RECORDS], 'mode': 'Local lookup', 'edition': '1.5', 'model': sol_status()})
        if path == '/api/search':
            q = parse_qs(uri.query).get('q', [''])[0][:2000]
            return self.send(200, [enrich(r) for r in search(q)])
        if path == '/api/chats':
            with connect() as db:
                return self.send(200, [dict(r) for r in db.execute('SELECT id,title FROM chats ORDER BY created DESC')])
        if path.startswith('/api/chats/'):
            chat_id = path.rsplit('/', 1)[-1]
            with connect() as db:
                rows = db.execute('SELECT role,content,payload FROM messages WHERE chat_id=? ORDER BY id', (chat_id,)).fetchall()
            return self.send(200, [{'role': r['role'], 'content': r['content'], 'payload': json.loads(r['payload']) if r['payload'] else None} for r in rows])
        if path == '/api/health':
            return self.send(200, {'ok': True, 'app': 'lantern-archive', 'pages': len(MANIFEST), 'records': len(RECORDS), 'sol_configured': sol_status()['configured']})
        if path.startswith('/pages/') and path.removeprefix('/pages/').removesuffix('.jpg').isdigit() and path.endswith('.jpg'):
            file = ROOT / 'public' / 'pages' / path.rsplit('/', 1)[-1]
        else:
            assets = {'/': 'index.html', '/app.js': 'app.js', '/style.css': 'style.css'}
            if path not in assets:
                return self.send(404, {'error': 'Not found'})
            file = ROOT / 'public' / assets[path]
        if not file.is_file():
            return self.send(404, {'error': 'Not found'})
        return self.send(200, file.read_bytes(), mimetypes.guess_type(file.name)[0] or 'application/octet-stream')

    def do_POST(self):
        origin = self.headers.get('Origin')
        if not self.allowed() or (origin and origin not in (f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}')):
            return self.send(403, {'error': 'Local requests only'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length < 1 or length > 16000:
                raise ValueError('Request is empty or too large')
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError('Expected an object')
            if self.path == '/api/corrections':
                note = body.get('note', '')
                record_id = body.get('record_id')
                if record_id not in {r['id'] for r in RECORDS} or not isinstance(note, str) or not note.strip() or len(note) > 4000:
                    raise ValueError('Choose a record and enter a correction of up to 4,000 characters')
                with connect() as db:
                    db.execute('INSERT INTO corrections(record_id,note,created) VALUES(?,?,?)', (record_id, note, time.time()))
                return self.send(200, {'saved': True, 'message': 'Saved for review. The verified record has not been changed.'})
            if self.path != '/api/ask':
                return self.send(404, {'error': 'Not found'})
            question = body.get('question', '')
            if not isinstance(question, str) or not question.strip() or len(question) > 4000:
                raise ValueError('Enter a question of up to 4,000 characters')
            use_model = body.get('use_model', False)
            if not isinstance(use_model, bool):
                raise ValueError('Use Sol must be true or false')
            chat_id = body.get('chat_id')
            with connect() as db:
                chat = db.execute('SELECT * FROM chats WHERE id=?', (chat_id,)).fetchone() if isinstance(chat_id, str) else None
                result = resolve(question, json.loads(chat['context']) if chat else {}, body.get('record_id'), body.get('table_id'), body.get('roll'), body.get('oven', 'unknown'))
                if use_model and result['status'] == 'reference' and result['record']:
                    model_records = [result['record']] + result.get('related_records', [])
                    try:
                        result['answer'] = sol_answer(question, model_records)
                        result['status'] = 'model-reference'
                        result['model'] = {'used': True, 'name': 'GPT-6 Sol'}
                    except SolUnavailable:
                        result['model'] = {'used': False, 'name': 'GPT-6 Sol', 'message': 'Sol was unavailable. Showing the local reviewed reference.'}
                if not chat:
                    chat_id = secrets.token_hex(12)
                    db.execute('INSERT INTO chats(id,title,created) VALUES(?,?,?)', (chat_id, question[:64], time.time()))
                result['record'] = enrich(result['record'])
                result['related_records'] = [enrich(r) for r in result.get('related_records', [])]
                db.execute('UPDATE chats SET context=? WHERE id=?', (json.dumps(result['context']), chat_id))
                db.execute('INSERT INTO messages(chat_id,role,content) VALUES(?,?,?)', (chat_id, 'user', question))
                db.execute('INSERT INTO messages(chat_id,role,content,payload) VALUES(?,?,?,?)', (chat_id, 'assistant', result['answer'], json.dumps(result)))
            return self.send(200, {'chat_id': chat_id, **result})
        except (ValueError, TypeError, KeyError) as error:
            return self.send(400, {'error': str(error)})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--open', action='store_true')
    args = parser.parse_args()
    init()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Lantern Archive is ready at http://127.0.0.1:{args.port}', flush=True)
    if args.open:
        webbrowser.open(f'http://127.0.0.1:{args.port}')
    server.serve_forever()
