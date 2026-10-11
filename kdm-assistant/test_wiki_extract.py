import unittest

from wiki_extract import extract


class WikiExtractTests(unittest.TestCase):
    def test_preserves_target_order_and_attack_table(self):
        candidate = {
            "title": "Sample", "source_url": "https://example.org/Sample",
            "revision_id": 7, "revision_timestamp": "2024-01-01T00:00:00Z",
            "wikitext": "==Card Text==\n===Pick Target===\n* closest [[threat]]\n"
                        "* no [[target]]: [[sniff]]\n{{Flow}}\n"
                        "===Move & Attack Target===\n{|\n|-\n! |Speed\n! |Accuracy\n"
                        "|-\n| |2\n| |4+\n|}\n[[Category:Cards]]",
        }
        draft = extract(candidate)
        self.assertEqual([b["text"] for b in draft["blocks"] if b["type"] == "list_item"],
                         ["closest threat", "no target: sniff"])
        table = next(b for b in draft["blocks"] if b["type"] == "table")
        self.assertEqual([c["text"] for c in table["rows"][1]["cells"]], ["2", "4+"])
        self.assertIn({"type": "flow"}, draft["blocks"])
        self.assertEqual(draft["review_status"], "unreviewed")
        self.assertEqual(draft["linked_pages"], ["sniff", "target", "threat"])
        self.assertEqual(draft["categories"], ["Cards"])

    def test_keeps_icon_and_later_section(self):
        candidate = {
            "title": "Sample", "source_url": "https://example.org/Sample",
            "revision_id": 7, "revision_timestamp": "2024-01-01T00:00:00Z",
            "wikitext": "==Card Text==\nDraw {{AI Card}}.\n==Basic Action==\n"
                        "* closest survivor\n[[Category:Cards]]",
        }
        draft = extract(candidate)
        self.assertIn("Draw [AI Card icon].", [b.get("text") for b in draft["blocks"]])
        self.assertIn("Basic Action", [b.get("text") for b in draft["blocks"]])
        self.assertEqual(draft["templates"], ["AI Card"])

    def test_refuses_page_without_card_text(self):
        with self.assertRaises(ValueError):
            extract({"wikitext": "==Overview==\nNo card content"})

    def test_preserves_merged_effect_cell(self):
        candidate = {
            "title": "Sample", "source_url": "https://example.org/Sample",
            "revision_id": 7, "revision_timestamp": "2024-01-01T00:00:00Z",
            "wikitext": "==Card Text==\n{|\n|-\n|{{Trigger}}\n"
                        "| colspan=\"3\" |[[Bash]]: Target is knocked down.\n|}",
        }
        table = extract(candidate)["blocks"][0]
        self.assertEqual(table["rows"][0]["cells"][1]["colspan"], 3)


if __name__ == "__main__":
    unittest.main()
