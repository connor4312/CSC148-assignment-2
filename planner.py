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
"""Program for helping users plan schedules.

This module contains the main class that is used to interact with users
who are trying to plan their schedules. It requires the course module
to store prerequisite information.

TermPlanner: answers queries about schedules based on prerequisite tree.
"""
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


def reset_before(fn):
    """ (Function) -> Function
    After we generate a schedule or check the validity of a schedule,
    some/all courses will be marked as taken. We want to reset them so as
    not to cause issue down the line. This is a simple decorator to do that.
    """
    # Define the function we want to replace the original with.
    def swapped(planner, *args):
        # Loop through and un-take every course in the planner tree.
        for course in planner.course.flatten():
            course.taken = False

        # Pass through the arguments we get.
        return fn(planner, *args)

    return swapped


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

    def _check_taken_after_prereqs(self):
        """ (TermPlanner) -> bool
        This checks to make sure that all courses are taken after their
        prereqs are taken. That is, for all leaf nodes in the prereq tree,
        if is_takeable() returns true then they must also have been taken.
        """
        for course in self.course.flatten():
            # If it's been taken, that's fine...
            if course.taken:
                continue
            # If it's a leaf node, we're not required to take it.
            if len(course.prereqs) == 0:
                continue
            # If it's not takeable, we don't have to take it...
            if not course.is_takeable():
                continue

            # Otherwise, it's invalid!
            return False

        # At this point, the tree is valid.
        return True

    def to_course_tree(self, schedule):
        """ (TermPlanner, [][]str) -> [][]Course
        Converts schedule of strings to a schedule of courses!
        """
        out = []
        for term in schedule:
            mapped = map(self.course.find, term)
            out.append(list(mapped))

        return out

    def _extract_prereqs(self, targets):
        """ (TermPlanner, []str) -> []Course
        Returns a list containing all prereqs of every target and the
        targets themselves.
        """

        courses = []
        # Loop through every course we selected that we want to take...
        for target in [self.course.find(c) for c in targets]:
            # Loop through that course and their prereq
            for item in target.flatten():
                # Add that to the list of courses we want to take, if
                # it isn't already in there.
                if item not in courses:
                    courses.append(item)

        return courses

    def _place_in_schedule(self, schedule, course):
        """ (TermPlanner, [][]Course, Course) -> NoneType
        Places the course in the schedule as "deep" as it is able to go - the
        last term if possible or, if full, it creates a new term.
        """
        if len(schedule[-1]) >= 5:
            schedule.append([course.name])
        else:
            schedule[-1].append(course.name)

    def _add_possible_to_schedule(self, schedule, courses):
        """ (TermPlanner, [][]Course, []Course) -> NoneType
        Adds all courses we can from the "courses" list into the schedule,
        for the "current" term; this basically adds one level of prereqs
        onto the schedule.
        """
        # Loop through all the courses so long as we're still taking
        # courses! When the number_taken is zero after an entire
        # iteration, then we need to append a new term and start
        # adding courses there.
        in_schedule = []
        count_taken = -1
        while count_taken != len(in_schedule):
            count_taken = len(in_schedule)

            # Take courses that are not already taken but are available.
            for course in courses:
                if course.taken or not course.is_takeable():
                    continue
                if course in in_schedule:
                    continue

                self._place_in_schedule(schedule, course)
                in_schedule.append(course)

        # Mark all courses up to this point to be taken. We don't do this
        # until we tried every course, otherwise we'd place prereqs in
        # the same semester as their parent courses!
        for course in in_schedule:
            course.take()

    @reset_before
    def is_valid(self, schedule):
        """ (TermPlanner, list of (list of str)) -> bool

        Return True if schedule is a valid schedule.
        Note that you are *NOT* required to specify why a schedule is invalid,
        though this is an interesting exercise!
        """

        schedule = self.to_course_tree(schedule)

        for term in schedule:
            for course in term:
                # If we couldn't find the course, the schedule is invalid.
                if course is None:
                    return False

                # If the course has already been taken, it's a duplicate!
                if course.taken:
                    return False

                # If we can't take the course, we're missing a prerequisite.
                if not course.is_takeable():
                    return False

            # At this point, go back and "take" all courses in the term.
            for course in term:
                course.take()

        # If we got down to here, we just need to check prereqs!
        return self._check_taken_after_prereqs()

    @reset_before
    def generate_schedule(self, selected_courses):
        """ (TermPlanner, list of str) -> list of (list of str)

        Return a schedule containing the courses in selected_courses that
        satisfies the restrictions given in the assignment specification.
        """

        # Pick our all of our "target courses" that we want to take.
        courses = self._extract_prereqs(selected_courses)

        # Define the base schedule
        schedule = [[]]

        # While there is any course not taken...
        while any(not course.taken for course in courses):
            # Add all the courses we can to the schedule
            self._add_possible_to_schedule(schedule, courses)
            # Then append a new term for courses to be added to.
            schedule.append([])

        # Return an empty list if we didn't make a valid schedule.
        if not self.is_valid(schedule):
            return []
        else:
            return schedule[0:-1]
