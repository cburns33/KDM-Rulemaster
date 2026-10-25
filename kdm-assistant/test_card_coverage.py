"""Source selection, card exceptions, and image citations for the next batch."""
import unittest

from engine import resolve


class NextCardCoverageTests(unittest.TestCase):
    def test_founding_stone_profile_and_sling_are_distinct(self):
        for question in [
            'What does the Founding Stone card do when I sling it?',
            "What are Founding Stone's speed, accuracy, and strength for a normal attack?",
            'Can I sling Founding Stone from across the board, and do I keep it afterward?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['record']['id'], 'founding-stone')
                self.assertIn('Speed 2, Accuracy 7+, and Strength 1', result['answer'])
                self.assertIn('anywhere on the board', result['answer'])
                self.assertIn('archive the card for 1 automatic hit', result['answer'])
                self.assertEqual(result['record']['card_sources'][0]['url'], '/pages/12.jpg')

    def test_sling_preserves_hit_location_exceptions(self):
        result = resolve('Founding Stone hits an Impervious location with a critical wound. What happens?')
        self.assertEqual(result['record']['id'], 'founding-stone')
        self.assertIn('prevents the monster wound', result['answer'])
        self.assertIn('without a critical wound effect cannot be critically wounded', result['answer'])

    def test_strange_hand_failure_and_optional_reward(self):
        for question in [
            'Strange Hand failed to wound. Who gets the Basic Action?',
            'A critical wound on Strange Hand: is the strength free, and does the card stay in play?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['record']['id'], 'white-lion-strange-hand')
                self.assertIn('Basic Action targeting the attacker', result['answer'])
                self.assertIn('may spend 1 survival to gain +1 permanent strength', result['answer'])
                self.assertIn('even if that payment is not made', result['answer'])
                self.assertEqual(result['record']['card_sources'][0]['url'], '/pages/13.jpg')

    def test_lost_hand_replaces_combo_claw_actions(self):
        result = resolve("Combo Claw is drawn while Strange Hand's Lost Hand is in play. Do we still attack?")
        self.assertEqual(result['record']['id'], 'white-lion-combo-claw')
        self.assertIn('ignore the normal Combo Claw actions', result['answer'])
        self.assertIn('once per lifetime', result['answer'])
        self.assertIn('moods-and-flows', [r['id'] for r in result['related_records']])

    def test_clever_ploy_doom_and_trap_resolution(self):
        for question in [
            'What does Clever Ploy do, and can the attacker dodge it?',
            'We draw Clever Ploy while the White Lion is knocked down. What happens to our remaining hits?',
            'Is Clever Ploy left in the discard pile after the trap?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['record']['id'], 'white-lion-clever-ploy')
                self.assertIn('cannot dodge this Basic Action', result['answer'])
                self.assertIn('it stands to resolve it', result['answer'])
                self.assertIn('discard unresolved hit locations', result['answer'])
                self.assertIn('including the trap card', result['answer'])
                self.assertIn("survivor's act can continue", result['answer'])
                self.assertEqual(result['record']['card_sources'][0]['url'], '/pages/14.jpg')

    def test_ground_fighting_links_its_spatial_evidence(self):
        result = resolve('Ground Fighting triggers on my activation. What bonuses does its attack get, and where is its zone?')
        self.assertEqual(result['record']['id'], 'moods-and-flows')
        self.assertIn('+2 speed and +1 damage', result['answer'])
        self.assertEqual(result['record']['card_sources'][0]['url'], '/pages/44.jpg')

    def test_new_card_coverage_does_not_certify_other_editions_or_missing_cards(self):
        for name in ['Founding Stone', 'Strange Hand', 'Clever Ploy', 'Ground Fighting']:
            with self.subTest(name=name):
                self.assertEqual(resolve(name + ' in 1.6')['status'], 'edition-check')
        for question in [
            'What does the White Lion Chomp card instruct it to do?',
            'What does the Phoenix do on its Basic Action?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['status'], 'unsupported')
                self.assertIsNone(result['record'])


if __name__ == '__main__':
    unittest.main()
