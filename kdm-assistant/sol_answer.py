"""Optional, source-grounded GPT-6 Sol explanations for Lantern Archive."""
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
ENV_PATHS = (ROOT.parent / '.env', ROOT / '.env')
MODEL = 'gpt-6-sol'
SOURCE_LIMIT = 18000
OUTPUT_LIMIT = 700


class SolUnavailable(Exception):
    """A generic error that never exposes credentials or upstream response bodies."""


def dotenv_value(names):
    for path in ENV_PATHS:
        if not path.is_file():
            continue
        for line in path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            name, value = line.split('=', 1)
            if name.strip() in names:
                value = value.strip()
                if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"":
                    value = value[1:-1]
                if value:
                    return value
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def api_key():
    return dotenv_value(('OPENAI_API_KEY', 'OPENAI_API_SECRET_KEY'))


def status():
    return {
        'configured': bool(api_key()),
        'model': 'GPT-6 Sol',
        'max_output_tokens': OUTPUT_LIMIT,
        'source_limit_chars': SOURCE_LIMIT,
    }


def source_payload(records):
    source_records = []
    for record in records[:3]:
        source_records.append({
            'title': record['title'],
            'summary': record['summary'],
            'notes': record['notes'],
            'tables': [{
                'title': table['title'],
                'rows': [{'range': row['label'], 'effects': row['effects']} for row in table['rows']],
            } for table in record.get('tables', [])],
        })
    return json.dumps(source_records, ensure_ascii=False)[:SOURCE_LIMIT]


def output_text(response):
    if isinstance(response.get('output_text'), str) and response['output_text'].strip():
        return response['output_text'].strip()
    fragments = []
    for item in response.get('output', []):
        for content in item.get('content', []):
            if content.get('type') == 'output_text' and isinstance(content.get('text'), str):
                fragments.append(content['text'])
    return ''.join(fragments).strip()


def answer(question, records):
    key = api_key()
    if not key:
        raise SolUnavailable('GPT-6 Sol is not configured on this computer.')
    prompt = f'''You are Lantern Archive, a source-grounded rules assistant for Kingdom Death: Monster.
Answer the user's question using only the reviewed edition 1.5 source records below.
Do not use outside game knowledge, community posts, guesses, unlisted cards, or unverified edition changes.
If these records do not establish the answer, say what source is missing. Do not invent page numbers or citations. Keep the answer under 350 words and state conditions that change the ruling.

USER QUESTION:
{question}

REVIEWED SOURCE RECORDS:
{source_payload(records)}'''
    body = json.dumps({
        'model': MODEL,
        'instructions': 'The application adds verified clickable citations with revised PDF and printed-book page mappings. Do not include page numbers, page labels, links, or citation markers in your answer, even when the question or source text includes page references. Leave source navigation to those clickable citations. You may identify a rule or source by its title.',
        'reasoning': {'effort': 'low'},
        'max_output_tokens': OUTPUT_LIMIT,
        'store': False,
        'input': prompt,
    }).encode('utf-8')
    request = Request(
        'https://api.openai.com/v1/responses', data=body, method='POST',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Accept': 'application/json'},
    )
    try:
        with urlopen(request, timeout=35) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        raise SolUnavailable('GPT-6 Sol could not complete this request.') from error
    text = output_text(payload)
    if not text:
        raise SolUnavailable('GPT-6 Sol returned no answer.')
    return text
