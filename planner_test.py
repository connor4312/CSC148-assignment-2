import unittest
from planner import TermPlanner


class TestPlanner(unittest.TestCase):

    def setUp(self):
        self.planner = TermPlanner('fixture_1.txt')

    def test_valid_if_valid(self):
        self.assertTrue(self.planner.is_valid([
            ['AWE100', 'AWE101', 'AWE199', 'AWE250'],
            ['AWE200'],
            ['AWE300'],
            ['AWE400']
        ]))

    def test_not_valid_same_term(self):
        self.assertFalse(self.planner.is_valid([
            ['AWE100', 'AWE101', 'AWE199', 'AWE250', 'AWE200'],
            ['AWE300'],
            ['AWE400']
        ]))

    def test_not_valid_if_duplicate(self):
        self.assertFalse(self.planner.is_valid([
            ['AWE100', 'AWE101', 'AWE199', 'AWE250'],
            ['AWE200', 'AWE101'],
            ['AWE300'],
            ['AWE400']
        ]))

    def test_not_valid_if_missing_prereq(self):
        self.assertFalse(self.planner.is_valid([
            ['AWE100', 'AWE101', 'AWE250'],
            ['AWE200'],
            ['AWE300'],
            ['AWE400']
        ]))

    def test_not_valid_if_dont_take_all(self):
        self.assertFalse(self.planner.is_valid([
            ['AWE100', 'AWE101', 'AWE199', 'AWE250'],
            ['AWE200'],
            ['AWE300']
        ]))

    def test_makes_valid_course(self):
        s = self.planner.generate_schedule(['AWE400'])
        self.assertEqual(s, [
            ['AWE100', 'AWE101', 'AWE199', 'AWE250'],
            ['AWE200'],
            ['AWE300'],
            ['AWE400']
        ])
        self.assertTrue(self.planner.is_valid(s))

    def test_handles_multiple_in_same_tree(self):
        s = self.planner.generate_schedule(['AWE400', 'AWE200'])
        self.assertEqual(s, [
            ['AWE100', 'AWE101', 'AWE199', 'AWE250'],
            ['AWE200'],
            ['AWE300'],
            ['AWE400']
        ])
        self.assertTrue(self.planner.is_valid(s))

    def test_single_course(self):
        s = self.planner.generate_schedule(['AWE199'])
        self.assertEqual(s, [['AWE199']])
        self.assertTrue(self.planner.is_valid(s))

    def test_course_one_prereq(self):
        self.planner = TermPlanner('fixture_2.txt')
        s = self.planner.generate_schedule(['A2'])
        self.assertEqual(s, [['A1'], ['A2']])
        self.assertTrue(self.planner.is_valid(s))

    def test_course_require_both_prereq_and_self(self):
        self.planner = TermPlanner('fixture_2.txt')
        s = self.planner.generate_schedule(['A2', 'A1'])
        self.assertEqual(s, [['A1'], ['A2']])
        self.assertTrue(self.planner.is_valid(s))

    def test_single(self):
        self.planner = TermPlanner('fixture_4.txt')
        s = self.planner.generate_schedule(['A1'])
        self.assertEqual(s, [])
        self.assertTrue(self.planner.is_valid(s))

        s = self.planner.generate_schedule(['B1'])
        self.assertEqual(s, [['A1'], ['B1']])
        self.assertTrue(self.planner.is_valid(s))

    def test_long_trees(self):
        self.planner = TermPlanner('fixture_5.txt')
        s = self.planner.generate_schedule(['A5', 'B5'])
        self.assertEqual(s, [
            ['A1', 'B1'],
            ['A2', 'B2'],
            ['A3', 'B3'],
            ['A4', 'B4'],
            ['A5', 'B5']
        ])
        self.assertTrue(self.planner.is_valid(s))


if __name__ == '__main__':
    unittest.main(exit=False)
