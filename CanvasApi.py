import CanvasDataSource
from datetime import datetime
from brewtils import system, parameter, Plugin, command


@system
class CanvasApi(object):

    def __init__(self):
        self.USER_ID = 24939504
        self.course_json = CanvasDataSource.getClasses()
        self.course_id_to_name = {course['id']: course['name'] for course in self.course_json}
        self.course_name_to_id = self.get_course_names_to_ids()
        self.courses = self.get_courses()
        self.all_unique_course_names = [self.course_id_to_name[id] for id in self.courses]

    def get_course_names_to_ids(self):
        base = {}
        for course in self.course_json:
            base[course['name'].lower()] = course['id']
            base[course['name'].split()[0].lower()] = course['id']
            base[course['name'].replace(' ', '').lower()] = course['id']
        return base

    @command(description='Get all the courses as a json file of the current student.', output_type='JSON')
    def get_courses(self):
        courses = {}
        for course_id in self.course_id_to_name:
            for enrolled in CanvasDataSource.get_enrollment(course_id):
                if enrolled['user_id'] == self.USER_ID:
                    courses[course_id] = enrolled
        return courses

    @command(description='Get all the courses of the current student.')
    def get_course_names(self):
        courses_names = [self.course_id_to_name[course_id] for course_id in self.courses]
        text = ""
        if len(courses_names) == 2:
            text = f'{courses_names[0]} and {courses_names[1]}.'
        else:
            for index, name in enumerate(courses_names):
                if index < (len(courses_names) - 1):
                    text += f'{name}, '
                else:
                    text += f'and {name}.'
        return f'You are currently enrolled in {text}'

    @command(description='Get the name of the current student.', output_type='STRING')
    def get_my_name(self):
        return str(list(self.courses.values())[0]['user']['name'])

    @parameter(key="course_name", description="The Canvas Course Name (Example: English 1331)",
               display_name="Course Name", default="English 1101")
    @command(description="Get the current students grade for a specific course.", output_type='STRING')
    def get_grade(self, course_name: str):
        course_name = course_name.lower()
        if course_name not in self.course_name_to_id:
            return f'Course name {course_name} could not be found'
        course_id = self.course_name_to_id[course_name]
        course = self.courses[course_id]
        return f"You have a {course['grades']['current_score']} in {course_name}"

    @parameter(key="course_name", description="The Canvas Course Name (Example: English 1331)",
               display_name="Course Name",
               default="English 1101")
    @command(description="Get the current students grade for a specific course.")
    def get_grade_raw(self, course_name: str):
        course_id = self.course_name_to_id[course_name.lower()]
        course = self.courses[course_id]
        return course['grades']['current_score']

    @command(description="Get the all the grades for the current student.", output_type='STRING')
    def get_all_grades(self):
        return [(name, self.get_grade_raw(name)) for name in self.all_unique_course_names]

    @parameter(key="course_name", description="The Canvas Course Name (Example: English 1331)",
               display_name="Course Name",
               default="English 1101")
    @command(description="Get the all the assignments of a course for the current student.")
    def get_assignments(self, course_name: str):
        course_name = course_name.lower()
        if course_name not in self.course_name_to_id:
            return f'Course name {course_name} could not be found'
        course_id = self.course_name_to_id[course_name]
        assignments = CanvasDataSource.getAssignments(self.USER_ID, course_id)

        assignments = sorted([(a['name'], self.get_date(a['due_at'])) for a in assignments if
                              a['submission_types'][0] == 'online_upload' and self.get_date(
                                  a['due_at']) > datetime.now()], key=lambda x: x[1])

        if len(assignments) == 0:
            return f'You have no assignments in {course_name}'

        latest = f'{assignments[0][0]} is due {assignments[0][1].strftime("%B %d, %Y")}'
        return f'You have {len(assignments)} assignments in {course_name}. {latest}'

    @parameter(key="course_name", description="The Canvas Course Name (Example: English 1331)",
               display_name="Course Name",
               default="English 1101")
    @parameter(key="after_date", description="Show assignments after this date",
               display_name="After Date", type='DateTime', optional=True, nullable=True)
    @command(description="Get the current students grade for a specific course.")
    def get_assignments_raw(self, course_name: str, after_date: datetime = None):
        if type(after_date) == int:
            after_date = datetime.utcfromtimestamp(after_date / 1000)
        course_id = self.course_name_to_id[course_name.lower()]
        assignments = CanvasDataSource.getAssignments(self.USER_ID, course_id)

        if after_date is None:
            return sorted([(a['name'], self.get_date(a['due_at'])) for a in assignments if
                           a['submission_types'][0] == 'online_upload' and self.get_date(a['due_at']) > datetime.now()],
                          key=lambda x: x[1])
        else:
            return sorted([(a['name'], self.get_date(a['due_at'])) for a in assignments if
                           a['submission_types'][0] == 'online_upload' and self.get_date(a['due_at']) > after_date],
                          key=lambda x: x[1])

    @command(description="Get the all the assignments for the current student.")
    def get_all_assignments(self):
        return [(name, self.get_assignments_raw(name)) for name in self.all_unique_course_names]

    @parameter(key="date", description="Show assignments after this date",
               display_name="After Date", type='DateTime')
    @command(description="Get the current students newest assignments.")
    def get_all_new_assignments(self, date: datetime):
        if type(date) == int:
            date = datetime.utcfromtimestamp(date / 1000)
        return [(name, self.get_assignments_raw(name, after_date=date)) for name in self.all_unique_course_names]

    def get_date(self, string):
        if string is None:
            return datetime.now()
        return datetime.strptime(string.split('T')[0], '%Y-%m-%d')

    @parameter(key="course_name", description="The Canvas Course Name (Example: English 1331)",
               display_name="Course Name",
               default="English 1101")
    @command(description="Get the current students quizzes for a specific course.")
    def get_quizzes(self, course_name: str):
        course_name = course_name.lower()
        if course_name not in self.course_name_to_id:
            return f'Course name {course_name} could not be found'
        course_id = self.course_name_to_id[course_name]
        quizzes = CanvasDataSource.getQuizzes(course_id)

        quizzes = sorted(
            [(q['title'], self.get_date(q['due_at'])) for q in quizzes if self.get_date(q['due_at']) > datetime.now()],
            key=lambda x: x[1])

        latest = f'{quizzes[0][0]} is due {quizzes[0][1].strftime("%B %d, %Y")}'
        quiz = 'quiz' if len(quizzes) == 1 else 'quizzes'
        return f'You have {len(quizzes)} {quiz} in {course_name}. {latest}'

    @parameter(key="course_name", description="The Canvas Course Name (Example: English 1331)",
               display_name="Course Name",
               default="English 1101")
    @parameter(key="after_date", description="Show assignments after this date",
               display_name="After Date", type='DateTime', optional=True, nullable=True)
    @command(description="Get the current students quizzes for a specific course.")
    def get_quizzes_raw(self, course_name: str, after_date: datetime = None):
        if type(after_date) == int:
            after_date = datetime.utcfromtimestamp(after_date / 1000)
        course_id = self.course_name_to_id[course_name.lower()]
        quizzes = CanvasDataSource.getQuizzes(course_id)

        if after_date is None:
            return sorted(
                [(q['title'], self.get_date(q['due_at'])) for q in quizzes if
                 self.get_date(q['due_at']) > datetime.now()],
                key=lambda x: x[1])
        else:
            return sorted([(q['title'], self.get_date(q['due_at'])) for q in quizzes if
                           self.get_date(q['due_at']) > after_date],
                          key=lambda x: x[1])

    @command(description="Get the all the quizzes for the current student.")
    def get_all_quizzes(self):
        return [(name, self.get_quizzes_raw(name)) for name in self.all_unique_course_names]

    @parameter(key="date", description="Show assignments after this date",
               display_name="After Date", type='DateTime')
    @command(description="Get the current students quizzes past a date")
    def get_all_new_quizzes(self, date):
        if type(date) == int:
            date = datetime.utcfromtimestamp(date / 1000)
        return [(name, self.get_quizzes_raw(name, after_date=date)) for name in self.all_unique_course_names]

    @parameter(key="course_name", description="The Canvas Course Name (Example: English 1331)",
               display_name="Course Name",
               default="English 1101")
    @command(description="Get the current students announcements for a specific course.")
    def get_announcement(self, course_name):
        course_name = course_name.lower()
        if course_name not in self.course_name_to_id:
            return f'Course name {course_name} could not be found'
        course_id = self.course_name_to_id[course_name]
        announcements = CanvasDataSource.getAnnouncement(course_id)
        info = sorted(
            [(a['title'], self.get_date(a['posted_at'])) for a in announcements],
            key=lambda x: x[1])

        if len(info) == 0:
            return f'There are no announcements for {course_name}'
        return f'The latest announcement for {course_name} is {info[0]}'


@parameter(key="course_name", description="The Canvas Course Name (Example: English 1331)",
           display_name="Course Name",
           default="English 1101")
@parameter(key="after_date", description="Show assignments after this date",
           display_name="After Date", type='DateTime', optional=True, nullable=True)
@command(description="Get the current students announcements for a specific course.")
def get_announcement_raw(self, course_name, after_date: datetime = None):
    if type(after_date) == int:
        after_date = datetime.utcfromtimestamp(after_date / 1000)
    course_name = course_name.lower()
    course_id = self.course_name_to_id[course_name]
    announcements = CanvasDataSource.getAnnouncement(course_id)
    if after_date is None:
        return sorted(
            [(a['title'], self.get_date(a['posted_at'])) for a in announcements],
            key=lambda x: x[1])
    else:
        return sorted([(a['title'], self.get_date(a['posted_at'])) for a in announcements if
                       self.get_date(a['posted_at']) > after_date],
                      key=lambda x: x[1])


@command(description="Get the all the announcements for each course for the current student.")
def get_all_announcements(self):
    return [(name, self.get_announcement_raw(name)) for name in self.all_unique_course_names]


@parameter(key="date", description="Show announcements after this date",
           display_name="After Date", type='DateTime')
@command(description="Get the current students announcements past a date")
def get_all_new_announcements(self, date):
    if type(date) == int:
        date = datetime.utcfromtimestamp(date / 1000)
    return [(name, self.get_announcement_raw(name, after_date=date)) for name in self.all_unique_course_names]
