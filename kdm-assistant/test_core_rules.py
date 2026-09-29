"""Source and retrieval checks for community scenarios and nearby counterexamples."""
import unittest
from engine import resolve
from records import RECORDS


class CoreRuleTests(unittest.TestCase):
    def test_standard_deployment_is_separate_from_prologue(self):
        for question in [
            'On the White Lion showdown setup, does start within the blue zone mean only the marked blue squares, or the whole area enclosed by them?',
            'Can we start inside the blue outline for a level 1 White Lion?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['record']['original'], 183)
                self.assertIn('blue marked squares', result['answer'])
        result = resolve('First Story: White Lion setup')
        self.assertEqual(result['record']['original'], 30)

    def test_survival_example_preserves_activation_not_movement(self):
        for question in [
            'One survivor has moved adjacent to the monster and is about to attack. Can a different survivor Surge to activate Tall Grass and hide before that attack?',
            'Can I Surge to move into Tall Grass?',
            'When can I use survival actions before an attack?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['record']['id'], 'survival-actions')
                self.assertIn('Dash spends 1 survival to gain movement', result['answer'])
                self.assertIn('Surge spends 1 survival to gain an activation', result['answer'])
                self.assertIn('already near Tall Grass', result['answer'])

    def test_attacker_and_fellow_survivor_are_distinguished(self):
        result = resolve('Can the attacking survivor dodge a wound reaction?')
        self.assertEqual(result['record']['id'], 'survival-actions')
        self.assertIn('cannot perform survival actions, including dodge', result['answer'])
        self.assertIn('if the hit location has no reaction, this window is absent', result['answer'])
        self.assertIn('after critical wound effects are applied', result['answer'])

    def test_damage_is_per_hit_and_dodge_is_conditional(self):
        result = resolve('A monster attack has Speed 2 and Damage 3, and both attack rolls hit. If the target Dodges one hit, how is the remaining hit resolved?')
        self.assertEqual(result['record']['id'], 'monster-hit-damage')
        self.assertIn('If the survivor is allowed to dodge', result['answer'])
        self.assertIn('remaining hit deals 3 damage', result['answer'])
        self.assertIn('depends on that location', result['answer'])
        self.assertIn('survival-actions', [r['id'] for r in result['related_records']])

    def test_repeated_location_hits_remain_separate(self):
        result = resolve('How do multiple hits to the same hit location cause severe injuries?')
        self.assertEqual(result['record']['id'], 'monster-hit-damage')
        self.assertIn('one severe injury roll', result['answer'])
        self.assertIn('Another hit to the same location is a separate instance', result['answer'])

    def test_damage_outside_attacks_has_own_reference(self):
        result = resolve('Can I dodge Grab damage outside an attack profile?')
        self.assertEqual(result['record']['id'], 'attack-effects')
        self.assertIn('cannot be dodged', result['answer'])

    def test_permanent_priority_requires_missing_card(self):
        for question in [
            'A White Lion critical wound creates a permanent priority target, then the Lion has Ground Fighting in play. How do those effects interact?',
            'Fuzzy Groin and Groundfighting: which wins?',
        ]:
            with self.subTest(question=question):
                result = resolve(question)
                self.assertEqual(result['status'], 'source-needed')
                self.assertEqual(result['record']['id'], 'priority-target')
                self.assertIn('moods-and-flows', [r['id'] for r in result['related_records']])
                self.assertIn('not establish the complete card-specific ruling', result['answer'])

    def test_general_ground_fighting_has_reviewed_source(self):
        result = resolve('What does the Ground Fighting mood do?')
        self.assertEqual(result['record']['id'], 'moods-and-flows')
        self.assertEqual(result['status'], 'reference')
        self.assertIn('stops normal AI draws', result['answer'])

    def test_new_topics_preserve_edition_guard(self):
        for question in ['White Lion blue zone setup in 1.6', 'Survival actions under current rules']:
            with self.subTest(question=question):
                self.assertEqual(resolve(question)['status'], 'edition-check')

    def test_continuation_page_identifiers(self):
        records = {r['id']: r for r in RECORDS}
        self.assertEqual(records['survival-actions']['supporting_originals'], [83])
        self.assertEqual(records['priority-target']['original'], 72)
        self.assertEqual(records['priority-target']['supporting_originals'], [73])
        self.assertEqual(records['moods-and-flows']['original'], 71)


if __name__ == '__main__':
    unittest.main(verbosity=2)
