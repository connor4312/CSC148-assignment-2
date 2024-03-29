# Assignment 2 - Course Planning!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# Connor Peet, 100108820
#
#
#
# ---------------------------------------------

from course import Course


class CourseParser():
    """
    The CourseParser is responsible for building course trees. Courses can be
    added by code to it, with a prerequisite, and they are then built into
    a proper tree.


    Attributes:
        - (dict) -> course
    """

    def __init__(self):
        self.courses = {}

    def checkout(self, course):
        """ (CourseParser, string) -> Course
        Gets the instance of the given course name, creating one if it does
        not exist.
        """
        if course not in self.courses:
            self.courses[course] = Course(course)

        return self.courses[course]

    def add(self, prereq, course):
        """ (CourseParser, string, string) -> NoneType
        Adds the prereq to the given course.
        """
        prereq_instance = self.checkout(prereq)

        self.checkout(course).add_prereq(prereq_instance)

    def root(self):
        """ (CourseParser) -> Course
        Returns the root course of the tree by iterating through the tree
        and removing items which appear as a subtree of another.
        """
        # Get a list of the course objects.
        hitlist = list(self.courses.values())
        # Iterate through all the courses we have. Remove items in the
        # "hitlist" that are prerequisites (child nodes) of anything else.
        for _, course in self.courses.items():
            for p in course.prereqs:
                if p in hitlist:
                    hitlist.remove(p)

        # Take the first (and only!) remaining element in the hitlist.
        return hitlist[0]
