"""Source scope and neighboring questions for the opening campaign batch."""
from pathlib import Path
import unittest

from engine import resolve
from records import RECORDS
from early_campaign_records import EARLY_CAMPAIGN_RECORDS


class EarlyCampaignTests(unittest.TestCase):
    def test_last_card_is_not_the_killing_wound(self):
        for question in [
            'We just removed the final AI card from the discard pile. Is the lion dead?',
            'There are no AI cards in the deck or discard pile. Is the monster dead?',
            'Our level 1 White Lion deck has no AI cards left. Is it already dead?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['record']['id'], 'monster-defeat')
                self.assertIn('one more wound', result['answer'])
                self.assertIn('shuffling the discard', result['answer'])

    def test_opening_rewards_and_dead_survivor_gear_exception(self):
        for question in [
            'We won the opening fight. What happens to a dead survivor\'s gear?',
            'After the first fight, who receives rewards and Hunt XP?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['record']['id'], 'prologue-victory')
                self.assertIn('4 White Lion resources and 4 basic resources', result['answer'])
                self.assertIn('exception', result['answer'])

    def test_basic_action_card_and_encounter_attributes(self):
        result = resolve('What does the White Lion Basic Action card say?')
        self.assertEqual(result['record']['id'], 'white-lion-basic-action')
        for text in ['closest survivor in field of view', 'Speed 2, Accuracy 2+, Damage 1', 'toughness 6', 'toughness 8']:
            self.assertIn(text, result['answer'])
        self.assertEqual(result['record']['card_sources'][0]['url'], '/pages/31.jpg')

    def test_standard_deck_has_random_counts_and_coverage_limit(self):
        result = resolve('How do we build the standard level 1 White Lion AI deck?')
        self.assertEqual(result['record']['id'], 'white-lion-level-one')
        for text in ['7 random Basic', '3 random Advanced', 'no Legendary', 'toughness 8', 'inventory', 'Set aside special AI cards']:
            self.assertIn(text, result['answer'])
        self.assertEqual(resolve('For the Prologue, do we use that same AI deck?')['record']['id'], 'white-lion-setup')

    def test_level_one_rewards_preserve_proficiency_eligibility(self):
        result = resolve('Standard level 1 White Lion victory: what rewards and weapon proficiency do we gain?')
        self.assertEqual(result['record']['id'], 'white-lion-aftermath')
        for text in ['+1 Hunt XP', '4 basic resources and 4 White Lion resources', 'selected a weapon type', 'wounded a monster', 'Catarium']:
            self.assertIn(text, result['answer'])

    def test_first_settlement_order_is_distinct_from_first_day_outcomes(self):
        result = resolve('In our first settlement, in what order do returning survivors, First Day, endeavors, and the timeline happen?')
        self.assertEqual(result['record']['id'], 'first-settlement-return')
        for text in ['+1 survival', '1 endeavor', 'Permanent injuries remain', 'Resolve First Day, then', 'population']:
            self.assertIn(text, result['answer'])
        self.assertEqual(resolve('Walk through the actual First Day card instructions and population results.')['status'], 'unsupported')
        self.assertEqual(resolve('Which survival actions does the Language innovation unlock?')['status'], 'unsupported')

    def test_crafting_procedure_does_not_supply_unreviewed_recipe(self):
        result = resolve('In our first settlement how do we craft gear, pay the resources, and record storage?')
        self.assertEqual(result['record']['id'], 'first-settlement-develop')
        for text in ['Each location costs 1 endeavor', 'archives those resource cards', 'specific crafting recipe', 'unspent resources and unworn gear']:
            self.assertIn(text, result['answer'])

    def test_hunt_sequence_and_arrival_exceptions(self):
        for question in [
            'How do we prepare the hunt board and advance through events?',
            'How does the hunt event revealer handle stacked cards and arriving at the monster?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['record']['id'], 'hunt-phase')
                for text in ['top to bottom', 'before moving', 'except Starvation', 'tens 3 and ones 5']:
                    self.assertIn(text, result['answer'])
        self.assertEqual(resolve('We rolled 84 on the hunt-event table. What are its exact results?')['status'], 'unsupported')

    def test_new_evidence_is_linked_and_other_editions_remain_unverified(self):
        public = Path(__file__).parent / 'public'
        for record in EARLY_CAMPAIGN_RECORDS:
            with self.subTest(record=record['id']):
                self.assertEqual(resolve(record['title'] + ' in 1.6')['status'], 'edition-check')
                for source in record.get('card_sources', []):
                    self.assertTrue((public / source['url'].lstrip('/')).is_file())
        self.assertEqual(len({record['id'] for record in RECORDS}), len(RECORDS))

    def test_supporting_evidence_preserves_encounter_and_phase(self):
        prologue = resolve('We won the opening fight. What rewards and Hunt XP do the survivors receive?')
        self.assertNotIn('white-lion-aftermath', [r['id'] for r in prologue.get('related_records', [])])
        standard = resolve('Now a standard level 1 White Lion, not the Prologue. Do we copy the deployment and fixed deck?')
        sources = [r['id'] for r in standard.get('related_records', [])]
        self.assertIn('white-lion-level-one', sources)
        self.assertNotIn('prologue-victory', sources)
        hunt = resolve('How do we prepare the hunt board and advance through events?')
        self.assertNotIn('white-lion-aftermath', [r['id'] for r in hunt.get('related_records', [])])


if __name__ == '__main__':
    unittest.main()
