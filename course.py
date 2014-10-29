# Assignment 2 - Course Planning!
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
"""Course prerequisite data structure.

This module contains the class that should store all of the
data about course prerequisites and track taken courses.
Note that by tracking "taken" courses, we are restricting the use
of this class to be one instance per student (otherwise,
"taken" doesn't make sense).

Course: a course and its prerequisites.
"""


class UntakeableError(Exception):
    pass


class PrerequisiteError(Exception):
    pass


class Course:
    """A tree representing a course and its prerequisites.

    This class not only tracks the underlying prerequisite relationships,
    but also can change over time by allowing courses to be "taken".

    Attributes:
    - name (str): the name of the course
    - prereqs (list of Course): a list of the course's prerequisites
    - taken (bool): represents whether the course has been taken or not
    """

    # Core Methods - implement all of these
    def __init__(self, name, prereqs=None):
        """ (Course, str, list of Courses) -> NoneType

        Create a new course with given name and prerequisites.
        By default, the course has no prerequisites (represent this
        with an empty list, NOT None).
        The newly created course is not taken.
        """
        self.name = name
        self.prereqs = prereqs or []
        self.taken = False

    def is_takeable(self):
        """ (Course) -> bool

        Return True if the user can take this course.
        A course is takeable if and only if all of its prerequisites are taken.
        """
        return all(p.taken for p in self.prereqs)

    def take(self):
        """ (Course) -> NoneType

        If this course is takeable, change self.taken to True.
        Do nothing if self.taken is already True.
        Raise UntakeableError if this course is not takeable.
        """
        if not self.is_takeable():
            raise UntakeableError()

        self.taken = True

    def add_prereq(self, prereq):
        """ (Course, Course) -> NoneType

        Add a prereq as a new prerequisite for this course.

        Raise PrerequisiteError if either:
        - prereq has this course in its prerequisite tree, or
        - this course already has prereq in its prerequisite tree
        """
        if self.has_prereq(prereq) or prereq.has_prereq(self):
            raise PrerequisiteError

        self.prereqs.append(prereq)

    def has_prereq(self, prereq):
        """ (Course, Course) -> bool
        Return True if course is a prerequisite of this or any child course.
        """
        if prereq in self.prereqs:
            return True

        return any(p.has_prereq(prereq) for p in self.prereqs)

    def flatten(self):
        """ (Course) -> list of Course
        Flattens the tree. Returns a list of all prerequisites of this course
        (recursively).
        """
        # Output a list of the self, and a concat'ed list of all the
        # flatted prerequisites.
        return [self] + [n for p in self.prereqs for n in p.flatten()]

    def count_prereqs(self):
        """ (Course) -> int
        Returns the total number of prerequisites that this course has.
        """
        count = len(self.prereqs)
        for p in self.prereqs:
            count += p.count_prereqs()

        return count

    def find(self, code):
        """ (Course, string) -> Course|NoneType
        Finds a course by its code (name) within the current course tree.
        """
        if self.name == code:
            return self

        for p in self.prereqs:
            out = p.find(code)
            if out is not None:
                return out

        return None

    def missing_prereqs(self):
        """ (Course) -> list of str

        Return a list of all of the names of the prerequisites of this course
        that are not taken.

        The returned list should be in alphabetical order, and should be empty
        if this course is not missing any prerequisites.
        """
        # Return a list of the names of courses in this tree, excluding
        # taken courses and the course itself
        output = [p.name for p in self.flatten() if not p.taken and p != self]

        return sorted(output)
