from course import Course


class CourseParser():

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
        Returns the root course of the tree.
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
