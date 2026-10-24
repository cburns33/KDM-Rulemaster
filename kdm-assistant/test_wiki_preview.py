import io
import json
import unittest
from unittest.mock import patch

from sol_answer import SolUnavailable
from wiki_preview import check_draft, model_answer, preview, select_draft


DRAFT = {
    'title': 'Sample Card', 'source_url': 'https://example.org/Sample_Card',
    'revision_id': 42, 'revision_timestamp': '2024-01-01T00:00:00Z',
    'extraction_status': 'draft', 'review_status': 'unreviewed',
    'blocks': [{'type': 'list_item', 'text': 'victim of Grab last round'}],
    'linked_pages': ['Grab'],
}


class FakeResponse:
    def __enter__(self):
        return io.BytesIO(json.dumps({'status': 'completed', 'output_text':
                                      'The card targets the previous Grab victim.'}).encode())

    def __exit__(self, *_):
        return False


class WikiPreviewTests(unittest.TestCase):
    def test_preview_labels_source_and_missing_definitions(self):
        result = preview('What does Grab do?', DRAFT, lambda *_: 'Grab is not defined here.')
        self.assertIn('UNREVIEWED WIKI DRAFT | Edition 1.5 unverified', result)
        self.assertIn('Requested linked definition not loaded: Grab.', result)
        self.assertIn('https://example.org/Sample_Card | Revision: 42', result)

    def test_ordinary_question_omits_link_footer(self):
        result = preview('Who does it target?', DRAFT, lambda *_: 'The previous Grab victim.')
        self.assertNotIn('definition not loaded', result)

    def test_refuses_reviewed_record_and_blank_question(self):
        with self.assertRaises(ValueError):
            check_draft({**DRAFT, 'review_status': 'reviewed'})
        with self.assertRaises(ValueError):
            preview(' ', DRAFT, lambda *_: 'answer')

    def test_model_receives_only_one_draft_and_missing_link_signal(self):
        requests = []

        def opener(request, timeout):
            requests.append((request, timeout))
            return FakeResponse()

        with patch('wiki_preview.api_key', return_value='test-key'):
            answer = model_answer('What does the card say?', DRAFT, opener)
        self.assertIn('Grab victim', answer)
        request, timeout = requests[0]
        body = json.loads(request.data)
        source = json.loads(body['input'])['draft']
        self.assertEqual(source['title'], 'Sample Card')
        self.assertEqual(source['unresolved_linked_pages'], ['Grab'])
        self.assertEqual(source['blocks'], DRAFT['blocks'])
        self.assertFalse(body['store'])
        self.assertEqual(timeout, 35)

    def test_model_without_key_reports_unavailable(self):
        with patch('wiki_preview.api_key', return_value=None):
            with self.assertRaises(SolUnavailable):
                model_answer('What does the card say?', DRAFT)

    def test_selects_named_or_distinctive_draft(self):
        other = {**DRAFT, 'title': 'Combo Claw', 'blocks': [
            {'type': 'text', 'text': 'Speed 2, Accuracy 4+, Damage 1'}], 'linked_pages': []}
        self.assertIs(select_draft('What does Sample Card say?', [DRAFT, other]), DRAFT)
        self.assertIs(select_draft('What does Combo Claw do?', [DRAFT, other]), other)

    def test_declines_missing_or_ambiguous_source(self):
        other = {**DRAFT, 'title': 'Other Card'}
        for question in ('What does the Phoenix do?', 'If there is no target, what happens?'):
            with self.subTest(question=question), self.assertRaises(ValueError):
                select_draft(question, [DRAFT, other])


if __name__ == '__main__':
    unittest.main()
