import unittest
from engine import resolve, search, select_row
from records import RECORDS

class RulesTests(unittest.TestCase):
    def test_experiment_boundaries(self):
        for roll, label in [(1,'1-3'),(3,'1-3'),(4,'4-6'),(6,'4-6'),(7,'7+'),(10,'7+'),(11,'7+')]:
            with self.subTest(roll=roll):
                r=resolve(f'Hands of Heat roll {roll}')
                self.assertEqual(r['row']['label'],label)
                self.assertEqual(r['table']['id'],'experiment')
                self.assertEqual(r['record']['original'],129)

    def test_branding_boundaries(self):
        for roll,label in [(1,'1-3'),(3,'1-3'),(4,'4-7'),(7,'4-7'),(8,'8-9'),(9,'8-9'),(10,'10+'),(12,'10+')]:
            with self.subTest(roll=roll):
                r=resolve(f'Lantern Branding roll {roll}')
                self.assertEqual(r['row']['label'],label)
                self.assertIn('half',r['answer'])

    def test_original_gate(self):
        r=resolve("In the story event Hands of Heat, if I roll a 6, what happens?")
        self.assertEqual(r['row']['label'],'4-6')
        for reward in ['+1 permanent strength','Red Fist','Lantern Oven']:
            self.assertIn(reward,r['answer'])
        self.assertIn('does not instruct',r['answer'])
        self.assertNotIn('next_table',r['row'])

    def test_high_experiment_has_new_branding_roll(self):
        r=resolve('Hands of Heat roll 7')
        self.assertEqual(r['row']['next_table'],'branding')
        self.assertIn('separate roll',r['answer'])
        self.assertNotIn('permanent strength',r['answer'])

    def test_existing_oven_routes_to_branding(self):
        r=resolve('Hands of Heat: we already have Lantern Oven and rolled 6')
        self.assertEqual(r['table']['id'],'branding')
        self.assertIn('permanent speed',r['answer'])
        self.assertNotIn('Red Fist',r['answer'])

    def test_no_oven_routes_to_experiment(self):
        r=resolve("Hands of Heat: we don't have Lantern Oven, rolled 6")
        self.assertEqual(r['table']['id'],'experiment')

    def test_followup(self):
        initial=resolve('Hands of Heat roll 6')
        followup=resolve('What about a 7?',initial['context'])
        self.assertEqual(followup['row']['label'],'7+')
        why=resolve('Why?',followup['context'])
        self.assertEqual(why['record']['id'],'hands-of-heat')

    def test_branding_context_persists(self):
        initial=resolve('Lantern Branding roll 5')
        followup=resolve('What about 9?',initial['context'])
        self.assertEqual(followup['table']['id'],'branding')
        self.assertEqual(followup['row']['label'],'8-9')

    def test_explicit_table_change(self):
        initial=resolve('Hands of Heat roll 7')
        followup=resolve('Lantern Branding roll 6',initial['context'])
        self.assertEqual(followup['row']['label'],'4-7')

    def test_conflicting_settlement_state(self):
        r=resolve('Hands of Heat roll 6',table_id='experiment',oven='yes')
        self.assertEqual(r['status'],'clarify')
        self.assertNotIn('row',r)

    def test_invalid_rolls(self):
        for roll in [-1,0,101,1.5,True,'six']:
            with self.subTest(roll=roll),self.assertRaises(ValueError):
                resolve('Hands of Heat',roll=roll)

    def test_edition_refusal(self):
        r=resolve('Hands of Heat in 1.6, roll 6')
        self.assertEqual(r['status'],'edition-check')
        self.assertNotIn('row',r)

    def test_unsupported_question(self):
        r=resolve('How does the Dragon King expansion work?')
        self.assertEqual(r['status'],'unsupported')
        self.assertIsNone(r['record'])

    def test_other_sources(self):
        for question,expected in [('How do puzzle affinities work?','affinities'),('Is a lantern 10 always a critical wound?','critical-wound-examples'),('What starting gear do survivors get?','create-survivor'),('White Lion setup AI deck','white-lion-setup')]:
            with self.subTest(question=question):
                self.assertEqual(search(question)[0]['id'],expected)

    def test_distractor_does_not_override_exact_event(self):
        r=resolve('Hands of Heat roll 6. Is this about critical wounds?')
        self.assertEqual(r['record']['id'],'hands-of-heat')

    def test_every_d10_has_exactly_one_band(self):
        for table in RECORDS[0]['tables']:
            for roll in range(1,11):
                matches=[row for row in table['rows'] if roll>=row['min'] and (row['max'] is None or roll<=row['max'])]
                self.assertEqual(len(matches),1)

if __name__=='__main__':
    unittest.main(verbosity=2)
