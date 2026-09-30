"""Retest frozen audit cases after the source and routing fixes, up to eight calls."""
import json
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[1]
sys.path.insert(0, str(REPO / 'kdm-assistant'))
import server
import sol_answer

if (OUT / 'results.jsonl').exists():
    raise SystemExit('Results already exist; refusing a paid rerun.')
cases = []
for batch in ['2026-09-30-timing-age', '2026-09-30-combat']:
    for line in (OUT.parent / batch / 'questions.jsonl').read_text(encoding='utf-8').splitlines():
        case = json.loads(line)
        case['source_batch'] = batch
        if case['id'] == 'C02':
            case['original_question'] = case['question']
            case['question'] = case['question'].replace('is facing the lion and in its movement range', 'is in front of the lion, in the area the lion faces, and in its movement range')
            case['revision'] = 'Correct facing wording before retest; survivor orientation is irrelevant.'
        cases.append(case)
with (OUT / 'questions.jsonl').open('x', encoding='utf-8') as stream:
    for case in cases:
        stream.write(json.dumps(case) + '\n')

calls = []
active = {}
original_answer = server.sol_answer
original_output = sol_answer.output_text

def capture_output(payload):
    calls[-1].update(usage=payload.get('usage'), response_status=payload.get('status'))
    return original_output(payload)

def counted_answer(question, records):
    if len(calls) >= 8:
        raise RuntimeError('Eight-call limit reached.')
    calls.append({**active, 'record_ids': [r['id'] for r in records[:3]],
                  'source_payload': json.loads(sol_answer.source_payload(records))})
    return original_answer(question, records)

server.sol_answer = counted_answer
sol_answer.output_text = capture_output
metadata = {
    'date': '2026-09-30', 'model': sol_answer.MODEL, 'paid_call_limit': 8,
    'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
    'working_tree': subprocess.check_output(['git', 'status', '--short'], cwd=REPO, text=True),
    'method': 'Assistant-graded regression retest of prior source audits. C02 facing wording corrected before requests. No independent holdout claim. Production handler, isolated history, fresh chat except T07 follows T04. No model prompt change.',
}
with tempfile.TemporaryDirectory(prefix='kdm-fixes-') as directory, (OUT / 'results.jsonl').open('x', encoding='utf-8') as output:
    shutil.copyfile(server.DATA / 'manifest.json', Path(directory) / 'manifest.json')
    server.DATA = Path(directory)
    server.init()
    http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
    thread = threading.Thread(target=http.serve_forever, daemon=True)
    thread.start()
    chats = {}
    try:
        for case in cases:
            for mode in ('local', 'sol_enabled'):
                active.update(case=case['id'], mode=mode)
                body = {'question': case['question'], 'use_model': mode == 'sol_enabled'}
                if case.get('seed'):
                    body['chat_id'] = chats[(case['seed'], mode)]
                request = Request(f'http://127.0.0.1:{http.server_port}/api/ask',
                                  data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
                with urlopen(request, timeout=50) as response:
                    result = json.load(response)
                chats[(case['id'], mode)] = result['chat_id']
                output.write(json.dumps({'id': case['id'], 'mode': mode, 'question': case['question'], 'result': result}) + '\n')
                output.flush()
            print(f"{case['id']}: both modes completed.", flush=True)
    finally:
        http.shutdown()
        http.server_close()
        thread.join()
        metadata['calls'] = calls
        with (OUT / 'run-metadata.json').open('x', encoding='utf-8') as stream:
            json.dump(metadata, stream, indent=2)
        usage = [c.get('usage') or {} for c in calls]
        print(json.dumps({'api_calls': len(calls), 'usage': {
            key: sum(u.get(key, 0) for u in usage)
            for key in ('input_tokens', 'output_tokens', 'total_tokens')
        }}), flush=True)
