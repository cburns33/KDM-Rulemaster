"""Affected-case regression using frozen baseline prompts and isolated history."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from http.server import ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

OUT = Path(__file__).resolve().parent / 'table-wording'
OUT.mkdir(exist_ok=True)
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT / 'kdm-assistant'))
import server
import sol_answer


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key-file', type=Path)
    args = parser.parse_args()
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    if branch != 'rules-v2':
        raise SystemExit('Run only from rules-v2.')
    if (OUT / 'run-metadata.json').exists():
        raise SystemExit('First-pass metadata exists; refusing to overwrite or repeat paid calls.')
    question_file = ROOT / 'evaluation/2026-10-24-release-baseline/QUESTIONS.md'
    question_text = question_file.read_text(encoding='utf-8')
    cases = []
    for case_id, block in re.findall(r'^### (Q\d+)\s*\n(.*?)(?=^### |^## |\Z)', question_text, re.M | re.S):
        turns = re.findall(r'^Turn \d+: (.*?)(?=\n\s*Turn \d+:|\Z)', block.strip(), re.M | re.S)
        cases.append((case_id, [turn.strip() for turn in turns] or [block.strip()]))
    if len(cases) != 32 or sum(len(turns) for _, turns in cases) != 36:
        raise SystemExit('Question structure differs from the frozen protocol.')
    selected = {'Q30'}
    cases = [(case, turns) for case, turns in cases if case in selected]
    expected_turns = sum(len(turns) for _, turns in cases)
    tracked_inputs = [question_file] + [ROOT / 'kdm-assistant' / name for name in
                     ['server.py', 'engine.py', 'records.py', 'core_records.py', 'sol_answer.py']]
    fingerprints = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in tracked_inputs}
    metadata = {'started_utc': utc_now(), 'root': str(ROOT), 'branch': branch,
                'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'worktree_status': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
                'question_version': 1, 'fingerprints': fingerprints,
                'history': 'temporary database, discarded after run',
                'key_source': 'user-authorized external file, memory only' if args.key_file else 'app configuration',
                'scenario_count': len(cases), 'turns_per_mode': expected_turns, 'selected_cases': sorted(selected)}
    save(OUT / 'run-metadata.json', metadata)
    api = {'attempts': 0, 'successful_responses': 0, 'usage': []}
    original_answer = server.sol_answer
    original_output = sol_answer.output_text

    def capture_output(payload):
        api['successful_responses'] += 1
        api['usage'].append(payload.get('usage', {}))
        return original_output(payload)

    def traced_answer(question, records):
        api['attempts'] += 1
        return original_answer(question, records)

    server.sol_answer = traced_answer
    sol_answer.output_text = capture_output
    summary = {'started_utc': metadata['started_utc'], 'modes': {}, 'api': api}
    with tempfile.TemporaryDirectory(prefix='kdm-release-baseline-') as directory:
        server.DATA = Path(directory)
        shutil.copyfile(ROOT / 'kdm-assistant/data/manifest.json', server.DATA / 'manifest.json')
        server.init()

        class QuietHandler(server.Handler):
            def log_message(self, *unused):
                pass

        http = ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
        thread = threading.Thread(target=http.serve_forever, daemon=True)
        thread.start()
        summary['port'] = http.server_port
        try:
            for mode in ['local', 'sol']:
                if mode == 'sol' and args.key_file:
                    if args.key_file.stat().st_size > 1_000_000:
                        raise RuntimeError('Key file exceeds file-read limit.')
                    for line in args.key_file.read_text(encoding='utf-8').splitlines():
                        name, separator, value = line.strip().partition('=')
                        if separator and name in {'OPENAI_API_KEY', 'OPENAI_API_SECRET_KEY'}:
                            os.environ[name] = value.strip().strip('\"\'')
                if mode == 'sol' and not sol_answer.status()['configured']:
                    summary['modes'][mode] = {'executed': 0, 'not_run': expected_turns, 'reason': 'API key unavailable'}
                    break
                destination = OUT / 'responses' / mode
                destination.mkdir(parents=True, exist_ok=True)
                totals = Counter()
                stop = False
                for case_id, turns in cases:
                    chat_id = None
                    for turn_index, question in enumerate(turns, 1):
                        body = {'question': question, 'use_model': mode == 'sol'}
                        if chat_id:
                            body['chat_id'] = chat_id
                        started = time.monotonic()
                        request = Request(f'http://127.0.0.1:{http.server_port}/api/ask',
                                          data=json.dumps(body).encode(),
                                          headers={'Content-Type': 'application/json'})
                        try:
                            with urlopen(request, timeout=50) as response:
                                result = json.load(response)
                            chat_id = result.get('chat_id')
                            totals[result.get('status', 'unknown')] += 1
                        except HTTPError as error:
                            result = {'execution_error': f'HTTP {error.code}',
                                      'body': error.read().decode('utf-8')}
                            totals['execution_error'] += 1
                        except Exception as error:
                            result = {'execution_error': type(error).__name__}
                            totals['execution_error'] += 1
                        save(destination / f'{case_id}-{turn_index}.json',
                             {'case': case_id, 'turn': turn_index, 'mode': mode, 'question': question,
                              'ended_utc': utc_now(), 'elapsed_seconds': round(time.monotonic() - started, 3),
                              'response': result})
                        totals['executed'] += 1
                        print(f'{mode} {case_id}.{turn_index}: {result.get("status", "execution_error")}', flush=True)
                        if mode == 'sol' and (result.get('execution_error') or
                                             result.get('model', {}).get('used') is False):
                            stop = True
                            break
                    if stop:
                        break
                summary['modes'][mode] = {**totals, 'not_run': expected_turns - totals['executed'],
                                          'stopped_after_failure': stop}
        finally:
            http.shutdown()
            http.server_close()
            thread.join()
    summary['finished_utc'] = utc_now()
    summary['inputs_unchanged'] = all(hashlib.sha256(path.read_bytes()).hexdigest() == fingerprints[str(path.relative_to(ROOT))]
                                      for path in tracked_inputs)
    save(OUT / 'run-summary.json', summary)
    print('First-pass responses and run summary preserved. No app inputs changed.', flush=True)


if __name__ == '__main__':
    main()
