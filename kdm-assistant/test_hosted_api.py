import importlib.util
import json
from pathlib import Path
import threading
import urllib.request
from unittest.mock import patch
import unittest
from http.server import ThreadingHTTPServer


MODULE_PATH = Path(__file__).with_name('api') / 'index.py'
SPEC = importlib.util.spec_from_file_location('hosted_api', MODULE_PATH)
hosted_api = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(hosted_api)


class HostedApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = ThreadingHTTPServer(('127.0.0.1', 0), hosted_api.handler)
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.http.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.thread.join()

    def request(self, path, body=None):
        request = urllib.request.Request(self.url + path, data=json.dumps(body).encode() if body else None)
        with urllib.request.urlopen(request) as response:
            return json.load(response)

    def test_library_marks_the_hosted_mode(self):
        result = hosted_api.library()
        self.assertEqual(result['hosting'], 'vercel')
        self.assertEqual(len(result['records']), 17)

    def test_ask_keeps_context_sent_by_the_browser(self):
        first = hosted_api.ask({'question': 'Hands of Heat roll 6'})
        second = hosted_api.ask({'question': 'What about 7?', 'context': first['context']})
        self.assertEqual(second['row']['label'], '7+')
        self.assertEqual(second['record']['source']['revised'], 90)

    def test_model_remains_opt_in(self):
        with patch.object(hosted_api, 'sol_answer', return_value='Reviewed explanation.') as sol:
            result = hosted_api.ask({'question': 'How do puzzle affinities work?', 'use_model': True})
        self.assertEqual(result['status'], 'model-reference')
        sol.assert_called_once()

    def test_rewritten_route_serves_library(self):
        result = self.request('/api/index?route=library')
        self.assertEqual(result['hosting'], 'vercel')


if __name__ == '__main__':
    unittest.main()
