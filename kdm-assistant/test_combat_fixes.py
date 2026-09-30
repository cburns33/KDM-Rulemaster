"""Regression checks from the September 30 source audits."""
import unittest
from engine import resolve
from records import RECORDS


class CombatFixTests(unittest.TestCase):
    def test_attacker_knockdown_retrieval_and_cancellation(self):
        for question in [
            'My survivor attacks and scores two hits. The reaction on the first hit location knocks the attacker down. Another survivor then Encourages them to stand. Can the attacker resolve the second hit location?',
            'Can an attacker continue unresolved hits after being knocked down and standing again?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['record']['id'], 'survivor-attack-sequence')
                self.assertIn('unresolved hits are canceled', result['answer'])
                self.assertIn('does not restore', result['answer'])

    def test_encourage_preserves_own_timing_and_limits(self):
        result = resolve('Must Encourage wait for a survival opportunity during the survivors turn?')
        self.assertEqual(result['record']['id'], 'survival-actions')
        for text in ['encourage at any time', 'Deaf survivors', 'once per round',
                     'cannot perform survival actions', 'current survival action remains unresolved']:
            self.assertIn(text, result['answer'])
        self.assertIn('Dash and Surge', result['answer'])

    def test_age_requires_identified_milestone_even_when_selected(self):
        for options in [{}, {'record_id': 'age-first-milestone'}]:
            result = resolve('For the Age event I rolled 8. What do I gain?', **options)
            self.assertEqual(result['status'], 'clarify')
            self.assertNotIn('row', result)
            self.assertEqual(result['context']['record_id'], 'age-first-milestone')

    def test_age_later_milestones_never_use_first_table(self):
        for question in ['Second Age milestone at 6 Hunt XP, rolled 8',
                         'Age milestone 3 roll 8', 'Fourth Age milestone roll 8',
                         'Age at 10 Hunt XP, rolled 8', 'Age at 15 Hunt XP roll 8']:
            for options in [{}, {'record_id': 'age-first-milestone'},
                            {'context': {'record_id': 'age-first-milestone', 'age_milestone': 1}}]:
                with self.subTest(question=question, options=options):
                    result = resolve(question, **options)
                    self.assertEqual(result['status'], 'unsupported')
                    self.assertNotIn('row', result)
                    self.assertIn('not reviewed', result['answer'])

    def test_age_followups_keep_scope_and_allow_topic_changes(self):
        second = resolve('I reached the second Age milestone at 6 Hunt XP. Which table?')
        for question in ['I rolled 8. What do I gain?', 'What about 8?', '8', 'Why?']:
            result = resolve(question, second['context'])
            self.assertEqual(result['status'], 'unsupported')
            self.assertEqual(result['context']['age_milestone'], 2)
        first = resolve('Actually the first milestone, rolled 8', second['context'])
        self.assertEqual(first['status'], 'resolved')
        self.assertIn('fighting art', first['answer'])
        self.assertEqual(resolve('What about the second?', first['context'])['status'], 'unsupported')
        for question, record in [('Severe head injury roll 8', 'severe-head-injury'),
                                 ('Hands of Heat roll 6', 'hands-of-heat')]:
            self.assertEqual(resolve(question, second['context'])['record']['id'], record)

    def test_age_conflicting_or_unrecognized_identity_needs_clarification(self):
        for question in ['First Age milestone at 6 Hunt XP, roll 8',
                         'First or second Age milestone, roll 8',
                         'Age at 7 Hunt XP, roll 8', 'Age milestone 5, roll 8']:
            result = resolve(question)
            self.assertEqual(result['status'], 'clarify')
            self.assertNotIn('row', result)

    def test_age_clarification_followup_and_first_milestone_completeness(self):
        pending = resolve('Age event rolled 8')
        self.assertEqual(resolve('second', pending['context'])['status'], 'unsupported')
        first = resolve('The first milestone', pending['context'])
        self.assertEqual(first['status'], 'reference')
        result = resolve('I rolled 8. What do I gain?', first['context'])
        self.assertEqual(result['status'], 'resolved')
        self.assertIn('Choose a weapon type', result['answer'])
        self.assertIn('once per survivor lifetime', result['answer'])
        self.assertEqual(resolve('Age first milestone roll 8 in 1.6')['status'], 'edition-check')

    def test_movement_targeting_evidence_and_routing(self):
        result = resolve('The White Lion already used its movement this round. A reaction now instructs a Basic Action. Can it move again?')
        self.assertEqual(result['record']['id'], 'monster-movement')
        self.assertIn('each instructed action', result['answer'])
        self.assertIn('white-lion-claw', [r['id'] for r in result['related_records']])
        result = resolve('Claw AI card versus Basic Action: closest knocked-down survivor or a standing threat?')
        records = [result['record']] + result.get('related_records', [])
        evidence = ' '.join(r['summary'] + ' '.join(r['notes']) for r in records)
        for text in ['not a threat', 'closest survivor in field of view', 'monster faces']:
            self.assertIn(text, evidence)

    def test_wound_formula_and_failure_evidence(self):
        result = resolve('Weapon strength 3, survivor strength +2, toughness 9: does wound roll 4 succeed and roll 3 cause Failure? This is not a critical wound.')
        self.assertEqual(result['record']['id'], 'survivor-attack-sequence')
        for text in ['weapon strength', 'survivor strength', 'meets or exceeds', 'Failure on failure']:
            self.assertIn(text, result['answer'])

    def test_critical_contrasts_have_general_rules(self):
        for qualifier in ['with a critical effect', 'with no critical effect', 'Impervious']:
            result = resolve(f'Natural 9, +1 luck, below toughness, {qualifier}: wound and Reflex?')
            self.assertEqual(result['record']['id'], 'critical-wound-examples')
            for text in ['no critical wound effect', 'does not turn', 'Impervious',
                         'below toughness', 'Cancel all reactions', 'natural 1']:
                self.assertIn(text, result['answer'])
            self.assertIn(80, result['record']['supporting_originals'])

    def test_source_links_resolve_and_payloads_fit(self):
        from sol_answer import source_payload
        ids = {r['id'] for r in RECORDS}
        for record in RECORDS:
            self.assertTrue(set(record.get('related_ids', [])) <= ids)
        import json
        for question in ['Encourage timing', 'Basic Action movement', 'Critical wound examples']:
            result = resolve(question)
            records = [result['record']] + result.get('related_records', [])
            self.assertLessEqual(len(records), 3)
            self.assertEqual(len(json.loads(source_payload(records))), len(records))


if __name__ == '__main__':
    unittest.main()
