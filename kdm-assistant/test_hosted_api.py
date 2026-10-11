import importlib.util
import json
import os
from pathlib import Path
import threading
from urllib.error import HTTPError
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
        self.assertEqual(len(result['records']), 18)

    def test_ask_keeps_context_sent_by_the_browser(self):
        first = hosted_api.ask({'question': 'Hands of Heat roll 6'})
        second = hosted_api.ask({'question': 'What about 7?', 'context': first['context']})
        self.assertEqual(second['row']['label'], '7+')
        self.assertEqual(second['record']['source']['revised'], 90)

    def test_model_remains_opt_in(self):
        with patch.dict(os.environ, {'KDM_ENABLE_SOL': 'true'}), patch.object(hosted_api, 'sol_answer', return_value='Reviewed explanation.') as sol:
            result = hosted_api.ask({'question': 'How do puzzle affinities work?', 'use_model': True})
        self.assertEqual(result['status'], 'model-reference')
        sol.assert_called_once()

    def test_rewritten_route_serves_library(self):
        result = self.request('/api/index?route=library')
        self.assertEqual(result['hosting'], 'vercel')

    def test_shared_access_code_issues_a_signed_session(self):
        with patch.dict(os.environ, {'KDM_ACCESS_CODE': 'group-code', 'KDM_SESSION_SECRET': 'session-secret'}, clear=False):
            request = urllib.request.Request(
                self.url + '/api/index?route=access',
                data=json.dumps({'code': 'group-code'}).encode(),
                method='POST',
            )
            with urllib.request.urlopen(request) as response:
                cookie = response.headers['Set-Cookie']
            self.assertIn('HttpOnly', cookie)
            self.assertIn('Secure', cookie)
            library_request = urllib.request.Request(self.url + '/api/index?route=library', headers={'Cookie': cookie.split(';', 1)[0]})
            with urllib.request.urlopen(library_request) as response:
                result = json.load(response)
        self.assertEqual(result['hosting'], 'vercel')

    def test_shared_access_code_rejects_invalid_code(self):
        with patch.dict(os.environ, {'KDM_ACCESS_CODE': 'group-code', 'KDM_SESSION_SECRET': 'session-secret'}, clear=False):
            request = urllib.request.Request(
                self.url + '/api/index?route=access',
                data=json.dumps({'code': 'wrong-code'}).encode(),
                method='POST',
            )
            with self.assertRaises(HTTPError) as error:
                urllib.request.urlopen(request)
            error.exception.close()
        self.assertEqual(error.exception.code, 401)


if __name__ == '__main__':
    unittest.main()
