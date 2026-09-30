"""Bounded combat source audit using the production handler and isolated history."""
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
    ('C01', 'The White Lion already moved its full movement during the monster turn. During the survivors turn a hit-location reaction instructs it to perform a Basic Action. Its chosen target is now four spaces away and there are no obstacles or movement modifiers. Can it move again as part of that Basic Action, or has it used up its movement for the round?',
     'It can move again. Move & Attack Target instructs movement up to the current movement value until adjacent. Movement is per instruction, not a once-per-round pool. Revised PDF 9, 46, 135.'),
    ('C02', 'A knocked-down survivor is the closest survivor in the White Lion\'s field of view. A standing survivor is farther away but is facing the lion and in its movement range. There is no priority target, Sniff effect, or other targeting modifier. Who is selected by the Claw AI card, and who is selected by the Basic Action?',
     'Claw selects the qualifying standing threat; Basic Action selects the closest survivor in field of view, including the knocked-down survivor. Revised PDF 9 and 45.'),
    ('C03', 'For a wound attempt, my weapon has 3 strength and my survivor has +2 strength. The monster has toughness 9 with no modifiers. The hit location has a Failure reaction, no other special rules, and this is not a critical wound. Does a wound roll of 4 succeed? What changes if the die is 3?',
     '4+3+2=9 meets toughness, so it wounds and Failure does not trigger. 3+3+2=8 fails, so Failure triggers. Revised PDF 51.'),
    ('C04', 'My survivor has +1 luck and rolls a natural 9 to wound a hit location with a critical wound effect and a Reflex reaction. The wound total is below the monster\'s toughness. The location is not Impervious, and the monster has no luck modifiers. Does the monster suffer a wound, and does Reflex happen?',
     'Natural 9 with +1 luck causes a critical wound. It wounds despite insufficient total, applies critical effects, and cancels Reflex. Revised PDF 53.'),
    ('C05', 'My survivor has +1 luck and rolls a natural 9 to wound a hit location with NO critical wound effect. The wound total is below the monster\'s toughness and the monster has no luck modifiers. Does luck make this a successful wound anyway?',
     'No. Without a critical wound effect the location cannot be critically wounded. A natural 9 is not a lantern 10 and the total fails toughness. Revised PDF 51 and 53.'),
    ('C06', 'My survivor has +1 luck and rolls a natural 9 on an Impervious hit location with a critical wound effect and a Reflex reaction. The monster has no luck modifiers. Does the monster lose a wound, and do the critical effect and Reflex happen?',
     'Critical effect happens and Reflex is canceled, but Impervious prevents the monster wound. Revised PDF 53. Safe missing-evidence response is acceptable if the supplied records lack this rule.'),
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
    if len(calls) >= 6:
        raise RuntimeError('Six-call limit reached.')
    calls.append({**active, 'record_ids': [r['id'] for r in records[:3]],
                  'source_payload': json.loads(sol_answer.source_payload(records))})
    return original_answer(question, records)

server.sol_answer = counted_answer
sol_answer.output_text = capture_output
metadata = {
    'date': '2026-09-30', 'model': sol_answer.MODEL, 'paid_call_limit': 6,
    'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
    'working_tree': subprocess.check_output(['git', 'status', '--short'], cwd=REPO, text=True),
    'method': 'Unblinded assistant-graded targeted source audit of known coverage risks and contrasts. Prompts and expectations frozen before responses. Fresh chat per case/mode, production handler, temporary history. No app changes or prompt tuning.',
    'sources': [{'revised': r, 'printed': b, 'original': o} for r, b, o in
                [(9, 27, 31), (45, 68, 72), (46, 69, 73), (51, 74, 78), (53, 76, 80), (135, 232, 236)]],
}
with (OUT / 'questions.jsonl').open('x', encoding='utf-8') as stream:
    for case_id, question, expected in CASES:
        stream.write(json.dumps({'id': case_id, 'question': question, 'expected': expected}) + '\n')

with tempfile.TemporaryDirectory(prefix='kdm-combat-') as directory, (OUT / 'results.jsonl').open('x', encoding='utf-8') as output:
    shutil.copyfile(server.DATA / 'manifest.json', Path(directory) / 'manifest.json')
    server.DATA = Path(directory)
    server.init()
    http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
    thread = threading.Thread(target=http.serve_forever, daemon=True)
    thread.start()
    try:
        for case_id, question, expected in CASES:
            for mode in ('local', 'sol_enabled'):
                active.update(case=case_id, mode=mode)
                request = Request(f'http://127.0.0.1:{http.server_port}/api/ask',
                                  data=json.dumps({'question': question, 'use_model': mode == 'sol_enabled'}).encode(),
                                  headers={'Content-Type': 'application/json'})
                with urlopen(request, timeout=50) as response:
                    result = json.load(response)
                output.write(json.dumps({'id': case_id, 'mode': mode, 'question': question, 'result': result}) + '\n')
                output.flush()
            print(f'{case_id}: both modes completed.', flush=True)
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
