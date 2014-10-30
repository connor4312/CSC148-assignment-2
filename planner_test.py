import unittest
from planner import TermPlanner


class TestPlanner(unittest.TestCase):

    def setUp(self):
        self.planner = TermPlanner('fixture.txt')

    def test_valid_if_valid(self):
        self.assertTrue(self.planner.is_valid([
            ['AWE100', 'AWE101', 'AWE199', 'AWE250'],
            ['AWE200'],
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
        self.assertEqual(s[0], ['AWE100', 'AWE101', 'AWE199', 'AWE250'])
        self.assertEqual(s[1], ['AWE200'])
        self.assertEqual(s[2], ['AWE300'])
        self.assertEqual(s[3], ['AWE400'])



if __name__ == '__main__':
    unittest.main(exit=False)
