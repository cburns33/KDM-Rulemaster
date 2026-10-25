"""Scope and table transfer checks using baseline failures and nearby wording."""
import unittest

from engine import parse_roll, resolve


class RetrievalScopeTests(unittest.TestCase):
    def test_roll_grammar_does_not_require_a_bare_number_after_roll(self):
        for question, expected in [
            ('I rolled a total of 13.', 13),
            ('The final roll is still 8.', 8),
            ('Our result was a 6.', 6),
            ('We rolled a final 4.', 4),
            ('roll6', 6),
            ('I have 2 Hunt XP.', None),
        ]:
            with self.subTest(question=question):
                self.assertEqual(parse_roll(question), expected)

    def test_xp_box_ordinals_identify_the_age_milestone(self):
        for ordinal, expected in [('first', 'resolved'), ('second', 'unsupported')]:
            result = resolve(f'The {ordinal} heavy-bordered Hunt XP box is filled; I rolled a total of 13 on Age.')
            self.assertEqual(result['status'], expected)
        result = resolve('First Hunt XP milestone, result was 13')
        self.assertIn('random fighting art', result['answer'])
        self.assertIn('does not immediately grant a proficiency level', result['answer'])

    def test_unrelated_rolls_and_rewards_do_not_select_age(self):
        for question in [
            'We rolled 72 on the hunt-event table. What does it say?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['status'], 'unsupported')
                self.assertIsNone(result['record'])

    def test_unreviewed_named_sources_do_not_borrow_a_neighbor(self):
        for question in [
            'Claw is discarded. The current AI card is Chomp. Resolve its targets and attack.',
            'We have finished Claw and next draw Terrifying Roar. What does that card say?',
            'What does Language unlock for our settlement?',
            'Please explain First Day and the starting population.',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['status'], 'unsupported')
                self.assertIsNone(result['record'])

    def test_early_prologue_setup_wins_over_a_mentioned_standard_level(self):
        result = resolve('Opening Prologue: do we start at the usual level 1 distance and use a random AI deck?')
        self.assertEqual(result['record']['id'], 'white-lion-setup')
        self.assertIn('6 spaces away', result['answer'])
        changed = resolve('Now standard level 1 deployment, not the Prologue setup.', result['context'])
        self.assertEqual(changed['record']['id'], 'white-lion-deployment')

    def test_location_correction_retains_injury_topic_after_a_decline(self):
        initial = resolve('Severe Arms injury, final roll is 8')
        self.assertEqual(initial['status'], 'unsupported')
        corrected = resolve('Actually it was Head instead; the final roll is still 8.', initial['context'])
        self.assertEqual(corrected['status'], 'resolved')
        self.assertEqual(corrected['record']['id'], 'severe-head-injury')
        self.assertIn('Concussion', corrected['answer'])
        self.assertIn('bleeding token', corrected['answer'])

    def test_explicit_damage_question_can_leave_an_injury_followup(self):
        initial = resolve('Severe Arms injury roll 8')
        changed = resolve('During a hunt, what happens to ordinary body damage?', initial['context'])
        self.assertEqual(changed['record']['id'], 'hunt-event-damage')

    def test_pending_injury_does_not_capture_a_different_table(self):
        initial = resolve('Severe Arms injury roll 8')
        for question, record in [('Hands of Heat roll 6', 'hands-of-heat'),
                                 ('Age first milestone roll 13', 'age-first-milestone')]:
            with self.subTest(question=question):
                changed = resolve(question, initial['context'])
                self.assertEqual(changed['status'], 'resolved')
                self.assertEqual(changed['record']['id'], record)
        unknown = resolve('Hunt-event table, final roll is 72', initial['context'])
        self.assertEqual(unknown['status'], 'unsupported')
        self.assertNotIn('Head injury', unknown['answer'])

    def test_completed_card_mentions_do_not_hide_a_later_active_card(self):
        for question in ['Claw is discarded. We draw Claw again. What does it do?',
                         'We resolved Maul. What does Claw do next?']:
            with self.subTest(question=question):
                self.assertEqual(resolve(question)['record']['id'], 'white-lion-claw')

    def test_unreviewed_full_card_does_not_hide_a_reviewed_bounded_interaction(self):
        result = resolve('Level 1 White Lion: Enraged mood is in play and Grasp deals damage. Does the token increase Grab?')
        self.assertEqual(result['record']['id'], 'white-lion-grasp-damage')
        self.assertIn('token does not increase Grab', result['answer'])
        unknown = resolve('What happens on entry when the Enraged mood is drawn?')
        self.assertEqual(unknown['status'], 'unsupported')

    def test_new_oven_state_replaces_the_previous_table_branch(self):
        first = resolve('Hands of Heat: we do not have Lantern Oven and rolled a final 6.')
        self.assertEqual(first['status'], 'resolved')
        self.assertEqual(first['table']['id'], 'experiment')
        changed = resolve('A separate occurrence: we already have Lantern Oven. The final roll is 6 again.', first['context'])
        self.assertEqual(changed['status'], 'resolved')
        self.assertEqual(changed['table']['id'], 'branding')
        self.assertIn('+1 permanent speed', changed['answer'])
        self.assertIn('supplied Branding roll', changed['answer'])
        self.assertNotIn('roll separately', changed['answer'])

    def test_unmentioned_named_cards_cannot_be_primary_generic_references(self):
        result = resolve('There are no AI cards in the deck or discard pile. Is the monster dead?')
        self.assertEqual(result['record']['id'], 'monster-defeat')
        self.assertIn('one more wound', result['answer'])


if __name__ == '__main__':
    unittest.main()
