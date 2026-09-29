"""Local retrieval and deterministic resolution. No model is needed for table lookup."""
import json
import re
import sqlite3
from records import RECORDS

STOP = set('a an the of on in is are do does can i my we our what happens how why it this that if with to for and roll rolled result have has already get give me tell about'.split())

def words(text):
    return [w for w in re.findall(r"[a-z]+", text.lower()) if w not in STOP]

def search(query):
    # Complete records are indexed as a unit, including every table and outcome.
    db = sqlite3.connect(':memory:')
    db.execute('CREATE VIRTUAL TABLE rules USING fts5(id UNINDEXED, title, body)')
    for r in RECORDS:
        db.execute('INSERT INTO rules VALUES (?, ?, ?)', (r['id'], r['title'], json.dumps(r)))
    terms = words(query)
    if not terms:
        db.close()
        return []
    ids = [row[0] for row in db.execute('SELECT id FROM rules WHERE rules MATCH ? ORDER BY bm25(rules) LIMIT 5', (' OR '.join('"'+w+'"' for w in terms),))]
    db.close()
    by_id = {r['id']: r for r in RECORDS}
    ranked = [by_id[i] for i in ids]
    ranked.sort(key=lambda r: (r['title'].lower() not in query.lower(), -len(set(terms) & set(words(r['keywords']+' '+r['title'])))))
    return ranked

def parse_roll(question):
    match = re.search(r'\b(?:roll(?:ed|ing)?|result)\s*(?:of\s+)?(?:a\s+|an\s+)?(?:lantern\s+)?(-?\d+)\b', question, re.I)
    if not match:
        match = re.search(r'\b(?:what about|how about|on|a)\s+(-?\d+)\b', question, re.I)
    if not match and re.fullmatch(r'\s*\d+\s*', question):
        return int(question)
    return int(match[1]) if match else None

def select_row(table, roll):
    return next((r for r in table['rows'] if roll >= r['min'] and (r['max'] is None or roll <= r['max'])), None)

def resolve(question, context=None, record_id=None, table_id=None, roll=None, oven='unknown'):
    context = context or {}
    if record_id and record_id not in {r['id'] for r in RECORDS}:
        raise ValueError('Unknown record')
    if oven not in {'unknown', 'yes', 'no'}:
        raise ValueError('Choose yes, no, or unknown for Lantern Oven')
    hits = search(question)
    by_id = {r['id']: r for r in RECORDS}
    explicit = next((r for r in RECORDS if r['title'].lower() in question.lower()), None)
    chosen = by_id.get(record_id) or explicit or (hits[0] if hits else None)
    q = question.lower()
    # Do not return adjacent rules for card text or tables not yet reviewed.
    unreviewed_detail = bool(
        re.search(r'severe\s+(?:arm|leg|body|waist)\s+injur(?:y|ies).*\b(?:roll|result)\b', q)
        or re.search(r'\b(?:chomp|maul|power swat|grasp)\s+card\b.*\b(?:instruct|do|effect)', q)
    )
    if unreviewed_detail and not record_id:
        return {'status': 'unsupported', 'answer': 'The reviewed records do not include that specific table or card text. Consult the source page or card; I cannot give its result from this collection.', 'record': None, 'context': {}}
    card_interaction = bool(re.search(r'ground\s*fighting', question, re.I) and
                        re.search(r'fuzzy\s+groin|permanent(?:ly)?\s+(?:marked|priority)|priority\s+target', question, re.I))
    fuzzy = bool(re.search(r'fuzzy\s+groin', question, re.I))
    if card_interaction and not record_id and not explicit:
        chosen = by_id['priority-target']
    elif fuzzy and not record_id and not explicit:
        chosen = by_id['priority-target']
    elif not record_id and re.search(r'\bage\b.*(?:milestone|hunt xp)|(?:milestone|hunt xp).*\bage\b', q):
        chosen = by_id['age-first-milestone']
    elif not record_id and re.search(r'severe\s+head\s+injur(?:y|ies)', q):
        chosen = by_id['severe-head-injury']
    elif not record_id and re.search(r'\bclaw\s+(?:ai\s+)?card\b', q):
        chosen = by_id['white-lion-claw']
    if chosen is None and (parse_roll(question) is not None or re.search(r'\b(why|that|it|oven|edition|1\.6|branding|yes|no)\b', question.lower())):
        chosen = by_id.get(context.get('record_id'))
    if not chosen:
        return {'status': 'unsupported', 'answer': 'I do not have a reviewed rule record for this question yet. Use the source browser to inspect the book. I cannot make a supported ruling from the current collection.', 'record': None, 'context': {}}
    reply = {'record': chosen, 'status': 'reference', 'answer': chosen['summary'], 'context': {'record_id': chosen['id']}}
    if re.search(r'\b(?:which|what) (?:edition|version)\b', q):
        reply['answer'] = 'This reviewed record uses the supplied 1.5 scan. Edition 1.6 changes have not been verified.'
        return reply
    if re.search(r'\b1\.6\b|\bcurrent (?:rules|edition)\b', q):
        reply.update(status='edition-check', answer='This record is verified against the supplied 1.5 scan. No 1.6 errata or replacement source has been verified here, so I cannot confirm this as a 1.6 ruling.')
        return reply
    if chosen['id'] in {'age-first-milestone', 'severe-head-injury'}:
        # An XP value is not a table roll. Require an explicit roll phrase.
        result_roll = parse_roll(question)
        if result_roll is not None:
            table = chosen['tables'][0]
            row = select_row(table, result_roll)
            if row is None or (chosen['id'] == 'age-first-milestone' and result_roll > 20):
                raise ValueError('Roll is outside this table.')
            reply.update(status='resolved', table=table, row=row, roll=result_roll,
                         answer=f"{table['title']}: {result_roll} is {row['label']}. " + ' '.join(row['effects']))
        else:
            reply['answer'] += '\n\n' + '\n'.join(chosen['notes'])
        return reply
    if chosen['id'] != 'hands-of-heat':
        reply['answer'] += '\n\n' + '\n'.join(chosen['notes'])
        related = [by_id[rid] for rid in chosen.get('related_ids', [])]
        if card_interaction:
            reply['answer'] = ('Fuzzy Groin makes the attacker the White Lion\'s permanent priority target until either dies. Ground Fighting stops normal AI draws and instead triggers a Basic Action against a survivor who spends an activation in its Zone of Death. That named target is set by the mood; priority targeting applies to Pick Target actions and does not redirect this trigger. The permanent priority effect remains for later applicable targeting.\n\n' + reply['answer'])
            related = [by_id['moods-and-flows']]
        elif fuzzy:
            reply['answer'] = ('Fuzzy Groin makes the attacker the White Lion\'s permanent priority target until either dies. Hiding in Tall Grass or being picked once does not end that card-specific effect.\n\n' + reply['answer'])
        if related:
            reply['related_records'] = related
            reply['answer'] += '\n\nRelated reviewed rules:\n' + '\n\n'.join(r['title'] + ': ' + r['summary'] for r in related)
        return reply
    same = context.get('record_id') == chosen['id']
    if oven == 'unknown' and same:
        oven = context.get('oven', 'unknown')
    if re.search(r"(?:don't|do not|doesn't|does not|haven't|have not|no)\s+(?:have\s+)?(?:a\s+)?lantern oven", q):
        oven = 'no'
    elif re.search(r'(?:already (?:have|has|innovated)|we have|we own)\s+(?:the\s+)?lantern oven', q):
        oven = 'yes'
    explicit_table = table_id or ('branding' if 'branding' in q else 'experiment' if 'experiment' in q else None)
    table_key = explicit_table or ('branding' if oven == 'yes' else context.get('table_id', 'experiment') if same else 'experiment')
    if oven == 'no' and not explicit_table and ('lantern oven' in q):
        table_key = 'experiment'
    table = next((t for t in chosen['tables'] if t['id'] == table_key), None)
    if not table:
        raise ValueError('Unknown table')
    roll = parse_roll(question) if roll is None else roll
    reply['context'].update(table_id=table_key, oven=oven)
    reply['table'] = table
    if explicit_table == 'experiment' and oven == 'yes':
        reply.update(status='clarify', answer='The recorded settlement state says Lantern Oven is already present. The entry box directs you to Lantern Branding. Confirm the intended table or change the settlement state before resolving this experiment.')
        return reply
    if roll is None:
        reply['answer'] = chosen['summary'] + '\n\n' + '\n'.join(chosen['notes']) + '\n\nChoose a table and enter its roll to resolve an outcome.'
        return reply
    if isinstance(roll, bool) or not isinstance(roll, int) or roll < 1 or roll > 100:
        raise ValueError('Enter an integer result from 1 to 100. Results above 10 must include applicable modifiers.')
    row = select_row(table, roll)
    reply.update(status='resolved', row=row, roll=roll)
    if table_key == 'experiment':
        condition = 'Assuming the settlement does not already have Lantern Oven. Before this roll, nominate a survivor and grant +1 courage.'
    else:
        condition = "For Lantern Branding, discard half the settlement's total resources (including storage), rounded down. Nominate a survivor and roll separately."
    reply['answer'] = f"{table['title']}: {roll} falls in {row['label']}.\n\n" + '\n'.join(row['effects']) + '\n\n' + condition
    if table_key == 'experiment' and row['label'] == '4-6':
        reply['answer'] += '\nThis outcome does not instruct you to roll on Lantern Branding.'
    return reply
