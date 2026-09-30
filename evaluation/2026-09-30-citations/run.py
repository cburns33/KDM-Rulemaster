"""One-call citation smoke test; no application history writes."""
import json
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parents[1] / 'kdm-assistant'))
from engine import resolve
import sol_answer

result_path = OUT / 'result.json'
if result_path.exists():
    raise SystemExit('Result already exists; refusing a paid rerun.')
question = 'My survivor attacks and scores two hits. The reaction on the first hit location knocks the attacker down. Another survivor then Encourages them to stand. Can the attacker resolve the second hit location?'
result = resolve(question)
records = [result['record']] + result.get('related_records', [])
metadata = {'question': question, 'model': sol_answer.MODEL,
            'record_ids': [r['id'] for r in records], 'paid_call_limit': 1}
original_output = sol_answer.output_text

def capture_output(payload):
    metadata.update(usage=payload.get('usage'), response_status=payload.get('status'))
    return original_output(payload)

sol_answer.output_text = capture_output
metadata['answer'] = sol_answer.answer(question, records)
metadata['has_page_reference'] = bool(re.search(r'\b(?:p\.|pp\.|pages?|pdf)\s*\d+', metadata['answer'], re.I))
with result_path.open('x', encoding='utf-8') as stream:
    json.dump(metadata, stream, indent=2)
print(json.dumps(metadata), flush=True)
