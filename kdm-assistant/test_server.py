import json
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from unittest.mock import patch
from pathlib import Path
from http.server import ThreadingHTTPServer
import server

class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.old_data = server.DATA
        cls.old_manifest = server.MANIFEST
        cls.manifest = json.loads((server.DATA / 'manifest.json').read_text(encoding='utf-8'))
        server.DATA = Path(cls.temp.name)
        (server.DATA / 'manifest.json').write_text(json.dumps(cls.manifest))
        server.init()
        cls.http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.http.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.thread.join()
        server.DATA = cls.old_data
        server.MANIFEST = cls.old_manifest
        cls.temp.cleanup()

    def request(self, path, body=None, headers=None):
        request = urllib.request.Request(self.url+path, data=json.dumps(body).encode() if body is not None else None, headers=headers or {})
        with urllib.request.urlopen(request) as response:
            return json.load(response)

    def test_health(self):
        self.assertEqual(self.request('/api/health')['app'],'lantern-archive')

    def test_sol_is_opt_in_and_only_for_references(self):
        with patch('server.sol_answer', return_value='A source-grounded explanation.') as sol:
            reference = self.request('/api/ask', {'question':'How do puzzle affinities work?', 'use_model':True})
            self.assertEqual(reference['status'], 'model-reference')
            self.assertTrue(reference['model']['used'])
            self.assertEqual(sol.call_count, 1)
            table = self.request('/api/ask', {'question':'Hands of Heat roll 6', 'use_model':True})
            self.assertEqual(table['status'], 'resolved')
            self.assertEqual(sol.call_count, 1)

    def test_sol_failure_keeps_the_local_reference(self):
        with patch('server.sol_answer', side_effect=server.SolUnavailable('unavailable')):
            result = self.request('/api/ask', {'question':'How do puzzle affinities work?', 'use_model':True})
        self.assertEqual(result['status'], 'reference')
        self.assertFalse(result['model']['used'])
        self.assertIn('Adjacent half-squares', result['answer'])

    def test_waist_injury_is_unsupported_in_both_answer_modes(self):
        with patch('server.sol_answer') as sol:
            for use_model in [False, True]:
                with self.subTest(use_model=use_model):
                    result = self.request('/api/ask', {
                        'question': 'In edition 1.5, I rolled an 8 on the severe injuries table for my waist. What happens to my survivor?',
                        'use_model': use_model,
                    })
                    self.assertEqual(result['status'], 'unsupported')
                    self.assertIsNone(result['record'])
                    self.assertNotIn('row', result)
                    restored = self.request('/api/chats/' + result['chat_id'])[-1]['payload']
                    self.assertEqual(restored['status'], 'unsupported')
            sol.assert_not_called()

    def test_hunt_damage_source_reaches_model_and_saved_citations(self):
        question = ('During a hunt event, my survivor suffers 3 damage to the body. '
                    'They have 1 armor in that location and 1 insanity. What happens to '
                    'the remaining damage, and does it cause a severe injury or brain trauma?')
        with patch('server.sol_answer', return_value='Hunt event damage is nonlethal.') as sol:
            local = self.request('/api/ask', {'question': question})
            self.assertEqual(local['status'], 'reference')
            self.assertEqual(local['record']['id'], 'hunt-event-damage')
            sol.assert_not_called()
            result = self.request('/api/ask', {'question': question, 'use_model': True})
            self.assertEqual(result['status'], 'model-reference')
            sol.assert_called_once()
            supplied = sol.call_args.args[1]
            self.assertEqual(supplied[0]['id'], 'hunt-event-damage')
            self.assertIn('does not cause severe injuries or brain trauma', supplied[0]['summary'])
            self.assertEqual([p['revised'] for p in result['record']['sources']], [41, 47, 48])
            self.assertEqual([p['printed'] for p in result['record']['sources']], [63, 70, 71])
            restored = self.request('/api/chats/' + result['chat_id'])[-1]['payload']
            self.assertEqual(restored['record']['sources'], result['record']['sources'])

    def test_coverage_and_continuation_citations(self):
        library = self.request('/api/library')
        self.assertEqual(len(library['records']), 17)
        self.assertEqual(sum(p['reviewed'] for p in library['pages']), 23)
        continuation = next(p for p in library['pages'] if p['revised'] == 56)
        self.assertTrue(continuation['reviewed'])
        self.assertEqual(continuation['record_id'], 'survival-actions')
        result = self.request('/api/ask', {'question': 'Survival actions and timing'})
        self.assertEqual([p['revised'] for p in result['record']['sources']], [55, 56])
        self.assertEqual([p['printed'] for p in result['record']['sources']], [78, 79])
        age = self.request('/api/ask', {'question': 'How does the Age milestone work at 2 hunt XP?'})
        self.assertEqual({p['printed'] for p in age['record']['sources']}, {43, 107})
        head = self.request('/api/ask', {'question': 'Severe head injury roll of 8'})
        self.assertEqual(head['status'], 'resolved')
        self.assertEqual(head['record']['source']['printed'], 86)
        claw = self.request('/api/ask', {'question': 'What does White Lion Claw card do?'})
        self.assertEqual([p['printed'] for p in claw['record']['sources']], [27, 28])

    def test_card_source_and_related_sources_survive_history(self):
        result = self.request('/api/ask', {'question': 'Fuzzy Groin and Ground Fighting'})
        restored = self.request('/api/chats/' + result['chat_id'])[-1]['payload']
        self.assertEqual(restored['status'], 'reference')
        self.assertEqual([p['revised'] for p in restored['record']['sources']], [45, 46])
        self.assertEqual(restored['related_records'][0]['source']['revised'], 44)
        self.assertEqual(restored['record']['card_sources'][0]['url'], 'https://kingdomdeath.fandom.com/wiki/Fuzzy_Groin')

    def test_age_guard_and_followup_persist_without_model_calls(self):
        with patch('server.sol_answer') as sol:
            for use_model in [False, True]:
                second = self.request('/api/ask', {'question': 'Second Age milestone at 6 Hunt XP, rolled 8', 'use_model': use_model})
                self.assertEqual(second['status'], 'unsupported')
                followup = self.request('/api/ask', {'question': 'I rolled 8. What do I gain?', 'chat_id': second['chat_id'], 'use_model': use_model})
                self.assertEqual(followup['status'], 'unsupported')
                self.assertEqual(followup['context']['age_milestone'], 2)
                saved = self.request('/api/chats/' + second['chat_id'])[-1]['payload']
                self.assertEqual(saved['context'], followup['context'])
                self.assertEqual(saved['record']['source']['revised'], 81)
                unknown = self.request('/api/ask', {'question': 'Age rolled 8', 'use_model': use_model})
                self.assertEqual(unknown['status'], 'clarify')
                first = self.request('/api/ask', {'question': 'First Age milestone roll 8', 'use_model': use_model})
                self.assertEqual(first['status'], 'resolved')
                self.assertIn('Choose a weapon type', first['answer'])
            sol.assert_not_called()

    def test_combat_evidence_and_citations_reach_model(self):
        cases = [
            ('Attacker knocked down: can unresolved hits resume after Encourage?', 'unresolved hits are canceled', 50),
            ('Must Encourage wait for a survival opportunity?', 'encourage at any time', 55),
            ('Basic Action movement after moving this round?', 'each instructed action', 46),
            ('Natural 9 with +1 luck on an Impervious critical location: wound?', 'Impervious prevents', 53),
        ]
        for question, text, revised in cases:
            with self.subTest(question=question), patch('server.sol_answer', return_value='Reviewed explanation.') as sol:
                result = self.request('/api/ask', {'question': question, 'use_model': True})
                self.assertEqual(result['status'], 'model-reference')
                supplied = sol.call_args.args[1]
                self.assertIn(text, ' '.join(r['summary'] + ' '.join(r['notes']) for r in supplied))
                self.assertIn(revised, [p['revised'] for r in [result['record']] + result['related_records'] for p in r['sources']])

    def test_all_page_mapping(self):
        self.assertEqual(len(self.manifest),138)
        self.assertEqual([p['revised'] for p in self.manifest],list(range(1,139)))
        self.assertEqual(len({p['original'] for p in self.manifest}),138)
        self.assertEqual(self.manifest[0]['original'],2)
        self.assertEqual(self.manifest[89]['original'],129)
        self.assertEqual(self.manifest[89]['printed'],125)
        self.assertEqual(self.manifest[-1]['printed'],235)

    def test_saved_chat_and_followup(self):
        first=self.request('/api/ask',{'question':'Hands of Heat roll 6'})
        second=self.request('/api/ask',{'question':'What about 7?','chat_id':first['chat_id']})
        self.assertEqual(second['row']['label'],'7+')
        self.assertEqual(second['record']['source']['revised'],90)
        self.assertEqual(len(self.request('/api/chats/'+first['chat_id'])),4)

    def test_correction_is_pending_only(self):
        result=self.request('/api/corrections',{'record_id':'hands-of-heat','note':'Test note'})
        self.assertTrue(result['saved'])
        with server.connect() as db:
            self.assertEqual(db.execute('SELECT note FROM corrections').fetchone()[0],'Test note')

    def test_cross_origin_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as result:
            self.request('/api/ask',{'question':'Hands of Heat'}, {'Origin':'https://example.com'})
        self.assertEqual(result.exception.code,403)
        result.exception.close()

    def test_path_traversal_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as result:
            self.request('/pages/../../server.py')
        self.assertEqual(result.exception.code,404)
        result.exception.close()

    def test_empty_question_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as result:
            self.request('/api/ask',{'question':''})
        self.assertEqual(result.exception.code,400)
        result.exception.close()

if __name__=='__main__':
    unittest.main(verbosity=2)
