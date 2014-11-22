import unittest
from course_parser import CourseParser
from planner import parse_course_data


class TestCourseParser(unittest.TestCase):

    def setUp(self):
        self.parser = CourseParser()

    def test_checkout(self):
        instance = self.parser.checkout('CSC148')
        self.assertEqual('CSC148', instance.name)
        self.assertEqual(instance, self.parser.checkout('CSC148'))

    def test_add(self):
        self.parser.add('B', 'A')
        self.parser.add('C', 'A')
        self.parser.add('D', 'B')

        a = self.parser.checkout('A')
        b = self.parser.checkout('B')
        c = self.parser.checkout('C')
        d = self.parser.checkout('D')
        self.assertEqual([b, c], a.prereqs)
        self.assertEqual([d], b.prereqs)

    def test_root(self):
        self.parser.add('B', 'A')
        self.parser.add('C', 'A')
        self.parser.add('D', 'B')
        self.assertEqual(self.parser.checkout('A'), self.parser.root())
        self.parser.add('A', 'Z')
        self.assertEqual(self.parser.checkout('Z'), self.parser.root())

    def test_file_parser(self):
        root = parse_course_data('fixture_1.txt')
        self.assertEqual('AWE400', root.name)
        self.assertEqual(['AWE300'], [c.name for c in root.prereqs])
        self.assertEqual(['AWE200', 'AWE250'],
                         [c.name for c in root.prereqs[0].prereqs])

if __name__ == '__main__':
    unittest.main(exit=False)
