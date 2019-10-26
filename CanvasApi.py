import CanvasDataSource
from datetime import datetime


class CanvasApi:

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

    def get_courses(self):
        courses = {}
        for course_id in self.course_id_to_name:
            for enrolled in CanvasDataSource.get_enrollment(course_id):
                if enrolled['user_id'] == self.USER_ID:
                    courses[course_id] = enrolled
        return courses

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

    def get_my_name(self):
        return str(list(self.courses.values())[0]['user']['name'])

    def get_grade(self, course_name: str):
        course_name = course_name.lower()
        if course_name not in self.course_name_to_id:
            return f'Course name {course_name} could not be found'
        course_id = self.course_name_to_id[course_name]
        course = self.courses[course_id]
        return f"You have a {course['grades']['current_score']} in {course_name}"

    def get_grade_raw(self, course_name: str):
        course_id = self.course_name_to_id[course_name.lower()]
        course = self.courses[course_id]
        return course['grades']['current_score']

    def get_all_grades(self):
        return [(name, self.get_grade_raw(name)) for name in self.all_unique_course_names]

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

    def get_assignments_raw(self, course_name: str, after_date: datetime = None):
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

    def get_all_assignments(self):
        return [(name, self.get_assignments_raw(name)) for name in self.all_unique_course_names]

    def get_all_new_assignments(self, date: datetime):
        return [(name, self.get_assignments_raw(name, after_date=date)) for name in self.all_unique_course_names]

    def get_date(self, string):
        if string is None:
            return datetime.now()
        return datetime.strptime(string.split('T')[0], '%Y-%m-%d')

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

    def get_quizzes_raw(self, course_name: str, after_date: datetime = None):
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

    def get_all_quizzes(self):
        return [(name, self.get_quizzes_raw(name)) for name in self.all_unique_course_names]

    def get_all_new_quizzes(self, date: datetime):
        return [(name, self.get_quizzes_raw(name, after_date=date)) for name in self.all_unique_course_names]
