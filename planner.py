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
"""Program for helping users plan schedules.

This module contains the main class that is used to interact with users
who are trying to plan their schedules. It requires the course module
to store prerequisite information.

TermPlanner: answers queries about schedules based on prerequisite tree.
"""
from course import Course
from course_parser import CourseParser


def parse_course_data(filename):
    """ (str) -> Course

    Read in prerequisite data from the file called filename,
    create the Course data structures for the data,
    and then return the root (top-most) course.

    See assignment handout for details.
    """
    parser = CourseParser()
    # Open the file and add every line to the parser via argument
    # unpacking. We were told to assume the file is perfectly structured,
    # so this should work well.
    with open(filename, 'r') as f:
        for line in f:
            # Each line has to be stripped, as it looks like we can
            # sometimes get trailing \n's at the end of the line
            parser.add(*line.strip().split(' '))

    return parser.root()


class TermPlanner:
    """Tool for planning course enrolment over multiple terms.

    Attributes:
    - course (Course): tree containing all available courses
    """

    def __init__(self, filename):
        """ (TermPlanner, str) -> NoneType

        Create a new term planning tool based on the data in the file
        named filename.

        You may not change this method in any way!
        """
        self.course = parse_course_data(filename)

    def is_valid(self, schedule):
        """ (TermPlanner, list of (list of str)) -> bool

        Return True if schedule is a valid schedule.
        Note that you are *NOT* required to specify why a schedule is invalid,
        though this is an interesting exercise!
        """
        for term in schedule:
            for cls in term:
                # Try to find the course in the tree. If we can't, it's
                # not a valid prereq tree.
                course = self.course.find(cls)
                if course is None:
                    return False

                # If the course has already been taken, it's a duplicate!
                if course.taken:
                    return False

                # If we can't take the course, we're missing a prerequisite.
                if not course.is_takeable():
                    return False

                # At this point, it's a valid course, so let's take it.
                course.take()

        # Then, loop through every course in the tree and make sure
        # every course that is possible to take has been taken.
        for course in self.course.flatten():
            if not course.taken and course.is_takeable():
                return False

        # If we got down to here, we're good!
        return True

    def generate_schedule(self, selected_courses):
        """ (TermPlanner, list of str) -> list of (list of str)

        Return a schedule containing the courses in selected_courses that
        satisfies the restrictions given in the assignment specification.
        """

        # Pick our all of our "target courses" that we want to take.
        targets = [self.course.find(c) for c in selected_courses]
        schedule = [[]]
        # For every one of the targets...
        for target in targets:
            # Flatten the prereq tree for that course
            courses = target.flatten()

            # While our target hasn't been taken, run the loop.
            while not target.taken:
                to_take = []
                # Add every course that can be taken currently to the list
                # of courses to take.
                for course in courses:
                    if course.is_takeable() and not course.taken:
                        to_take.append(course)

                # Take every course we selected before, limiting the the
                # maximum courses per term to five.
                for course in to_take:
                    if len(schedule[len(schedule) - 1]) < 5:
                        schedule[len(schedule) - 1].append(course.name)
                    else:
                        schedule.append([course.name])

                    course.take()

                # Append a new empty term to the schedule, so classes in the
                # next iteration (those we could not take this round) are
                # added in a new term.
                schedule.append([])

        return schedule
