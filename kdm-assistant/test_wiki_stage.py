import io
import json
import tempfile
import unittest
from pathlib import Path

from wiki_stage import fetch_candidate, save_candidate


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return io.BytesIO(self.payload)

    def __exit__(self, *_):
        return False


class WikiStageTests(unittest.TestCase):
    def test_fetch_preserves_source_and_review_boundary(self):
        payload = json.dumps({"query": {"pages": [{
            "pageid": 42,
            "title": "Sample Card",
            "revisions": [{
                "revid": 81,
                "timestamp": "2024-01-01T00:00:00Z",
                "slots": {"main": {"content": "Sample {{AI Card}} text"}},
            }],
        }]}}).encode()
        requests = []

        def opener(request, timeout):
            requests.append((request.full_url, timeout))
            return FakeResponse(payload)

        candidate = fetch_candidate("Sample Card", opener)
        self.assertEqual(candidate["revision_id"], 81)
        self.assertEqual(candidate["source_url"],
                         "https://kingdomdeath.fandom.com/wiki/Sample_Card")
        self.assertEqual(candidate["wikitext"], "Sample {{AI Card}} text")
        self.assertEqual(candidate["review_status"], "unreviewed")
        self.assertEqual(candidate["edition_status"], "unverified")
        self.assertIn("titles=Sample+Card", requests[0][0])

    def test_save_does_not_replace_existing_revision(self):
        candidate = {"page_id": 42, "revision_id": 81, "wikitext": "first"}
        with tempfile.TemporaryDirectory() as directory:
            path = save_candidate(candidate, Path(directory))
            candidate["wikitext"] = "changed"
            self.assertEqual(save_candidate(candidate, Path(directory)), path)
            self.assertEqual(json.loads(path.read_text())["wikitext"], "first")

    def test_missing_page_is_rejected(self):
        payload = b'{"query":{"pages":[{"title":"Absent","missing":true}]}}'
        with self.assertRaises(ValueError):
            fetch_candidate("Absent", lambda *_args, **_kwargs: FakeResponse(payload))


if __name__ == "__main__":
    unittest.main()
