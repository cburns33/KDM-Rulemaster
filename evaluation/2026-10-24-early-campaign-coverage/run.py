"""Bounded HTTP coverage checks with six explicit Sol calls and saved first results."""
from datetime import datetime, timezone
import hashlib
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import threading
from urllib.request import Request, urlopen

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT / 'kdm-assistant'))
import server
import sol_answer

CASES = [
    ('N01', 'The final AI card is now in the wound stack and both other piles are empty. Has the lion died?', 'monster-defeat', False),
    ('N02', 'We won the Prologue with one survivor dead. What happens to their gear and resources, and what rewards and XP do the survivors receive?', 'prologue-victory', True),
    ('N03', 'What does the White Lion Basic Action card say about targeting, its attack profile, and no target?', 'white-lion-basic-action', False),
    ('N04', 'How do we build a standard level 1 White Lion deck, and what are its movement and toughness?', 'white-lion-level-one', False),
    ('N05', 'For our first settlement, in what order do we handle returning survivors, First Day, endeavors, and the timeline?', 'first-settlement-return', True),
    ('N06', 'In our first settlement, how do we craft gear, spend resources, and put unworn gear into storage? What source gives the exact recipe?', 'first-settlement-develop', True),
    ('N07', 'How do we prepare the hunt board and advance through events until reaching the monster?', 'hunt-phase', False),
    ('N08', 'Standard level 1 White Lion victory: who gains weapon proficiency, what are the rewards, and when do we add Catarium?', 'white-lion-aftermath', True),
    ('N09', 'Ground Fighting is in play. Does spending activation trigger its attack before my action, and where can I see the Zone of Death diagram?', 'moods-and-flows', True),
    ('N10', 'Ground Fighting: is a space three squares directly behind the lion in the Zone of Death? Can I open its diagram here?', 'moods-and-flows', True),
    ('N11', 'Walk through the actual First Day card instructions and population outcomes.', None, False),
    ('N12', 'What does the Language innovation unlock for survival actions?', None, False),
    ('N13', 'We rolled 84 on the hunt-event table. What are the exact event results?', None, False),
    ('N14', 'What does Chomp instruct the White Lion to do?', None, False),
    ('N15', 'What happens when the full Enraged mood enters play?', None, False),
    ('N16', 'What does the Terrifying Roar card do?', None, False),
]


def save(name, value):
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def baseline_fingerprint():
    base = ROOT / 'evaluation/2026-10-24-release-baseline'
    paths = sorted(p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path.relative_to(base)).encode())
        digest.update(path.read_bytes())
    return {'files': len(paths), 'sha256': digest.hexdigest()}


def main():
    if (OUT / 'run-metadata.json').exists():
        raise SystemExit('Saved run exists; refusing to overwrite or repeat paid requests.')
    before = baseline_fingerprint()
    inputs = ['engine.py', 'records.py', 'core_records.py', 'early_campaign_records.py', 'sol_answer.py', 'server.py']
    fingerprints = {name: hashlib.sha256((ROOT / 'kdm-assistant' / name).read_bytes()).hexdigest() for name in inputs}
    save('run-metadata.json', {'started_utc': datetime.now(timezone.utc).isoformat(), 'baseline_before': before, 'fingerprints': fingerprints, 'protocol': '16 new local cases; 6 of those also use Sol; 8 affected baseline scenarios locally. No retries. Development evidence.'})
    # The user authorized this existing file. It is read only in memory, never copied.
    sol_answer.ENV_PATHS = (ROOT.parent / 'KDM-Rulemaster' / '.env',)
    usage = []
    original_output = sol_answer.output_text
    def capture(payload):
        usage.append(payload.get('usage', {}))
        return original_output(payload)
    sol_answer.output_text = capture
    checks = []
    citations = set()
    with tempfile.TemporaryDirectory(prefix='kdm-early-coverage-') as directory:
        server.DATA = Path(directory)
        shutil.copyfile(ROOT / 'kdm-assistant/data/manifest.json', server.DATA / 'manifest.json')
        server.init()
        httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        base_url = f'http://127.0.0.1:{httpd.server_port}'
        def ask(case, question, expected=None, model=False, chat_id=None, check=True):
            body = {'question': question, 'use_model': model}
            if chat_id:
                body['chat_id'] = chat_id
            request = Request(base_url + '/api/ask', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
            with urlopen(request, timeout=50) as response:
                result = json.load(response)
            save(case + '.json', {'question': question, 'response': result})
            actual = (result.get('record') or {}).get('id')
            checks.append({'case': case, 'expected': expected, 'actual': actual, 'status': result['status'], 'selection_pass': actual == expected if check else None, 'model_requested': model, 'model_used': result.get('model', {}).get('used', False)})
            for record in [result.get('record')] + result.get('related_records', []):
                if not record:
                    continue
                for source in record['sources']:
                    citations.add('/pages/' + str(source['revised']) + '.jpg')
                for source in record.get('card_sources', []):
                    if source['url'].startswith('/'):
                        citations.add(source['url'])
            return result
        try:
            for case, question, expected, model in CASES:
                ask(case + '-local', question, expected)
                if model:
                    ask(case + '-sol', question, expected, model=True)
            question_text = (ROOT / 'evaluation/2026-10-24-release-baseline/QUESTIONS.md').read_text(encoding='utf-8')
            selected = {'Q05', 'Q06', 'Q13', 'Q20', 'Q21', 'Q24', 'Q27', 'Q22'}
            for case, block in re.findall(r'^### (Q\d+)\s*\n(.*?)(?=^### |^## |\Z)', question_text, re.M | re.S):
                if case not in selected:
                    continue
                turns = re.findall(r'^Turn \d+: (.*?)(?=\n\s*Turn \d+:|\Z)', block.strip(), re.M | re.S) or [block.strip()]
                chat_id = None
                for number, question in enumerate(turns, 1):
                    result = ask(f'{case}-{number}-local', question.strip(), chat_id=chat_id, check=False)
                    chat_id = result['chat_id']
            for path in sorted(citations):
                with urlopen(base_url + path, timeout=10) as response:
                    if response.status != 200 or response.headers.get_content_type() != 'image/jpeg':
                        raise RuntimeError('Citation failed: ' + path)
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join()
    after = baseline_fingerprint()
    unchanged = fingerprints == {name: hashlib.sha256((ROOT / 'kdm-assistant' / name).read_bytes()).hexdigest() for name in inputs}
    save('checks.json', checks)
    summary = {'responses': len(checks), 'new_selection_checks': sum(c['selection_pass'] is not None for c in checks), 'new_selection_passes': sum(c['selection_pass'] is True for c in checks), 'model_requests': sum(c['model_requested'] for c in checks), 'model_used': sum(c['model_used'] for c in checks), 'api_responses': len(usage), 'input_tokens': sum(item.get('input_tokens', 0) for item in usage), 'output_tokens': sum(item.get('output_tokens', 0) for item in usage), 'citation_images_checked': len(citations), 'baseline_after': after, 'baseline_unchanged': before == after, 'answering_inputs_unchanged': unchanged}
    save('run-summary.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
