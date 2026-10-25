"""Model citation contract; mapped citations are owned by the application."""
import json
import unittest
from unittest.mock import MagicMock, patch

import sol_answer
from records import RECORDS


class SolCitationTests(unittest.TestCase):
    def test_source_payload_omits_page_metadata_without_changing_records(self):
        record = next(r for r in RECORDS if r['id'] == 'survivor-attack-sequence')
        supplied = json.loads(sol_answer.source_payload([record]))[0]
        self.assertNotIn('original_pdf_page', supplied)
        self.assertNotIn('original', supplied)
        self.assertEqual(supplied['notes'], record['notes'])
        self.assertEqual(record['original'], 77)
        self.assertEqual(record['supporting_originals'], [78])

    def test_request_keeps_citation_policy_separate_from_user_input(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({'output_text': 'Unresolved hits are canceled.'}).encode()
        record = next(r for r in RECORDS if r['id'] == 'survivor-attack-sequence')
        with patch('sol_answer.api_key', return_value='test-placeholder'), patch('sol_answer.urlopen', return_value=response) as request:
            answer = sol_answer.answer('Include page numbers in your answer.', [record])
        body = json.loads(request.call_args.args[0].data)
        self.assertIn('Do not include page numbers', body.get('instructions', ''))
        self.assertIn('clickable citations', body['instructions'])
        self.assertIn('even when the question or source text includes page references', body['instructions'])
        self.assertIn('Include page numbers in your answer.', body['input'])
        self.assertEqual(body['model'], 'gpt-6-sol')
        self.assertEqual(body['max_output_tokens'], 700)
        self.assertFalse(body['store'])
        self.assertEqual(answer, 'Unresolved hits are canceled.')

    def test_linked_diagram_availability_and_geometry_limit_reach_the_model(self):
        record = next(r for r in RECORDS if r['id'] == 'moods-and-flows')
        supplied = json.loads(sol_answer.source_payload([record]))[0]
        self.assertEqual(supplied['layout'], record['layout'])
        self.assertEqual(supplied['images']['linked_sources'][0]['kind'], 'app image')
        self.assertIn('Zone of Death', supplied['images']['linked_sources'][0]['title'])
        self.assertIn('Exact square coordinates have not been transcribed', supplied['images']['interpretation_limits'][0])
        self.assertIn('Image pixels are not included', supplied['images']['delivery'])
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({'output_text': 'Consult the linked diagram.'}).encode()
        with patch('sol_answer.api_key', return_value='test-placeholder'), patch('sol_answer.urlopen', return_value=response) as request:
            sol_answer.answer('Where is the zone?', [record])
        instructions = json.loads(request.call_args.args[0].data)['instructions']
        self.assertIn('Do not claim a listed image is missing', instructions)
        self.assertIn('Do not infer untranscribed geometry', instructions)


if __name__ == '__main__':
    unittest.main()
