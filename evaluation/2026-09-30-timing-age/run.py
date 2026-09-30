"""Bounded source-audit scenarios through production HTTP, with isolated history."""
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

CASES = [
    ('T01', 'My survivor attacks and scores two hits. The reaction on the first hit location knocks the attacker down. Another survivor then Encourages them to stand. Can the attacker resolve the second hit location?',
     'Unresolved hits are canceled when the attacker is knocked down; standing again does not restore them. Revised PDF 50, printed 73.'),
    ('T02', 'During the survivors turn, can a standing survivor Encourage another knocked-down survivor at any time, or must they wait for a survival opportunity? Encourage is unlocked, the helper has 1 survival, has not used Encourage this round, is not attacking, and no other survival action is unresolved. The recipient is not deaf.',
     'Encourage explicitly permits any-time use subject to the stated restrictions. Do not impose Dash/Surge opportunity windows. Revised PDF 55, printed 78.'),
    ('T03', 'I reached the first Age milestone at 2 Hunt XP and rolled 8 on its 2d10 table. What do I gain?',
     'Milestone 1 Weapon Proficiency: choose a weapon type and gain one random fighting art for 8. Revised PDF 24/81, printed 43/107.'),
    ('T04', 'I reached the second Age milestone at 6 Hunt XP. Which Age table should I use?',
     'Milestone 2 Improved Reflexes. Its rules are outside current reviewed coverage, so a specific missing-coverage notice is acceptable. Do not instruct milestone 1.'),
    ('T05', 'I reached the second Age milestone at 6 Hunt XP and rolled 8 on its 2d10 table. What do I gain?',
     'Milestone 2 Improved Reflexes: +1 permanent strength. With current coverage, abstain rather than resolve milestone 1. Revised PDF 81, printed 107.'),
    ('T06', 'For the Age event I rolled 8. What do I gain?',
     'Ask which milestone was reached; 8 has different outcomes across milestones. Revised PDF 81, printed 107.'),
]

if (OUT / 'results.jsonl').exists():
    raise SystemExit('Results already exist; refusing a paid rerun.')
calls = []
active = {}
original_answer = server.sol_answer
original_output = sol_answer.output_text

def capture_output(payload):
    calls[-1].update(usage=payload.get('usage'), response_status=payload.get('status'))
    return original_output(payload)

def counted_answer(question, records):
    if len(calls) >= 5:
        raise RuntimeError('Five-call limit reached.')
    calls.append({**active, 'record_ids': [r['id'] for r in records[:3]],
                  'source_payload': json.loads(sol_answer.source_payload(records))})
    return original_answer(question, records)

server.sol_answer = counted_answer
sol_answer.output_text = capture_output
metadata = {
    'date': '2026-09-30', 'model': sol_answer.MODEL, 'paid_call_limit': 5,
    'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
    'working_tree': subprocess.check_output(['git', 'status', '--short'], cwd=REPO, text=True),
    'method': 'Unblinded assistant-graded targeted source audit; prompts frozen before responses. Fresh chat per case/mode except labeled follow-up. Production handler and temporary history database. No application changes.',
    'sources': [{'revised': r, 'printed': b, 'original': o} for r, b, o in
                [(24, 43, 47), (50, 73, 77), (55, 78, 82), (56, 79, 83), (81, 107, 111)]],
}
with (OUT / 'questions.jsonl').open('x', encoding='utf-8') as stream:
    for case_id, question, expected in CASES:
        stream.write(json.dumps({'id': case_id, 'question': question, 'expected': expected}) + '\n')
    stream.write(json.dumps({'id': 'T07', 'seed': 'T04', 'question': 'I rolled 8. What do I gain?',
                             'expected': 'Preserve second-milestone scope and abstain with current coverage, or resolve +1 permanent strength with reviewed milestone 2 evidence.'}) + '\n')

with tempfile.TemporaryDirectory(prefix='kdm-timing-age-') as directory, (OUT / 'results.jsonl').open('x', encoding='utf-8') as output:
    shutil.copyfile(server.DATA / 'manifest.json', Path(directory) / 'manifest.json')
    server.DATA = Path(directory)
    server.init()
    http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
    thread = threading.Thread(target=http.serve_forever, daemon=True)
    thread.start()

    def ask(case_id, question, mode, chat_id=None):
        active.update(case=case_id, mode=mode)
        body = {'question': question, 'use_model': mode == 'sol_enabled'}
        if chat_id:
            body['chat_id'] = chat_id
        request = Request(f'http://127.0.0.1:{http.server_port}/api/ask',
                          data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
        with urlopen(request, timeout=50) as response:
            result = json.load(response)
        output.write(json.dumps({'id': case_id, 'mode': mode, 'question': question, 'result': result}) + '\n')
        output.flush()
        print(json.dumps({'id': case_id, 'mode': mode, 'status': result['status'],
                          'record': (result.get('record') or {}).get('id'), 'answer': result['answer']}), flush=True)
        return result

    try:
        for case_id, question, expected in CASES:
            for mode in ('local', 'sol_enabled'):
                result = ask(case_id, question, mode)
                if case_id == 'T04':
                    ask('T07', 'I rolled 8. What do I gain?', mode, result['chat_id'])
    finally:
        http.shutdown()
        http.server_close()
        thread.join()
        metadata['calls'] = calls
        with (OUT / 'run-metadata.json').open('x', encoding='utf-8') as stream:
            json.dump(metadata, stream, indent=2)
        print(json.dumps({'api_calls': len(calls), 'usage': [c.get('usage') for c in calls]}), flush=True)
