# Assignment 2 - Unit Tests for Course
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
#
#
#
# ---------------------------------------------
"""Unit tests for course.py

Submit this file, containing *thorough* unit tests
for your code in course.py.
Note that you should not have any tests involving
standard input or output in here.
"""
import unittest
from course import Course, UntakeableError, PrerequisiteError


class TestCourse(unittest.TestCase):

    def setUp(self):
        self.a = Course('A')
        self.b = Course('B')
        self.c = Course('C', [self.a])
        self.d = Course('D', [self.b, self.c])

    def test_initializes_with_values(self):
        self.assertEqual([self.b, self.c], self.d.prereqs)
        self.assertEqual([], self.a.prereqs)
        self.assertEqual('A', self.a.name)
        self.assertEqual(False, self.a.taken)

    def test_is_not_takeable_without_prereqs(self):
        self.assertEqual(False, self.d.is_takeable())
        self.assertEqual(False, self.c.is_takeable())

    def test_is_takeable_with_prereqs(self):
        self.a.take()
        self.assertEqual(True, self.c.is_takeable())
        self.assertEqual(False, self.d.is_takeable())
        self.b.take()
        self.assertEqual(False, self.d.is_takeable())
        self.c.take()
        self.assertEqual(True, self.d.is_takeable())

    def test_take_works(self):
        self.assertEqual(False, self.a.taken)
        self.a.take()
        self.assertEqual(True, self.a.taken)
        self.a.take()
        self.assertEqual(True, self.a.taken)

    def test_raises_error_if_cant_take(self):
        self.assertEqual(False, self.d.is_takeable())
        with self.assertRaises(UntakeableError):
            self.d.take()

    def test_add_prereq_works(self):
        self.a.add_prereq(self.b)
        self.assertEqual([self.b], self.a.prereqs)

    def test_add_prereq_fails_if_already_there(self):
        with self.assertRaises(PrerequisiteError):
            self.c.add_prereq(self.a)

    def test_add_prereq_fails_if_circular(self):
        with self.assertRaises(PrerequisiteError):
            self.a.add_prereq(self.c)

    def test_missing_prereqs_works(self):
        self.assertEqual([], self.a.missing_prereqs())
        self.assertEqual(['A'], self.c.missing_prereqs())
        self.assertEqual(['A', 'B', 'C'], self.d.missing_prereqs())

if __name__ == '__main__':
    unittest.main(exit=False)
