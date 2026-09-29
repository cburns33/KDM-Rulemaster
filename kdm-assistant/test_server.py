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

    def test_coverage_and_continuation_citations(self):
        library = self.request('/api/library')
        self.assertEqual(len(library['records']), 12)
        self.assertEqual(sum(p['reviewed'] for p in library['pages']), 16)
        continuation = next(p for p in library['pages'] if p['revised'] == 56)
        self.assertTrue(continuation['reviewed'])
        self.assertEqual(continuation['record_id'], 'survival-actions')
        result = self.request('/api/ask', {'question': 'Survival actions and timing'})
        self.assertEqual([p['revised'] for p in result['record']['sources']], [55, 56])
        self.assertEqual([p['printed'] for p in result['record']['sources']], [78, 79])

    def test_missing_card_status_and_related_sources_survive_history(self):
        result = self.request('/api/ask', {'question': 'Fuzzy Groin and Ground Fighting'})
        restored = self.request('/api/chats/' + result['chat_id'])[-1]['payload']
        self.assertEqual(restored['status'], 'source-needed')
        self.assertEqual([p['revised'] for p in restored['record']['sources']], [45, 46])
        self.assertEqual(restored['related_records'][0]['source']['revised'], 44)

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
