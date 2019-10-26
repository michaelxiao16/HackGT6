import CanvasDataSource
from datetime import datetime

class CanvasApi:

    def __init__(self):
        self.USER_ID = 24939504
        self.course_json = CanvasDataSource.getClasses()
        self.course_id_to_name = {course['id']: course['name'] for course in self.course_json}
        self.course_name_to_id = self.get_course_names_to_ids()
        self.courses = self.get_courses()

    def get_course_names_to_ids(self):
        base = {}
        for course in self.course_json:
            base[course['name']] = course['id']
            base[course['name'].split()[0]] = course['id']
            base[course['name'].replace(' ', '')] = course['id']
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
            for index, name  in enumerate(courses_names):
                if index < (len(courses_names) - 1):
                    text += f'{name}, '
                else:
                    text += f'and {name}.'
        return f'You are currently enrolled in {text}'

    def get_my_name(self):
        return str(list(self.courses.values())[0]['user']['name'])

    def get_grade(self, course_name: str):
        if course_name not in self.course_name_to_id:
            return f'Course name {course_name} could not be found'
        course_id = self.course_name_to_id[course_name]
        course = self.courses[course_id]
        return f"You have a {course['grades']['current_grade']} in {course_name}"
    
    def get_assignments(self, course_name: str):
        if course_name not in self.course_name_to_id:
            return f'Course name {course_name} could not be found'
        course_id = self.course_name_to_id[course_name]
        assignments = CanvasDataSource.getAssignments(self.USER_ID, course_id)

        assignments = sorted([(a['name'], self.get_date(a['due_at'])) for a in assignments if a['submission_types'][0] == 'online_upload'], key= lambda x: x[1])

        latest = f'{assignments[0][0]} is due {assignments[0][1].strftime("%B %d, %Y")}'
        return f'You have {len(assignments)} assignments in {course_name}. {latest}'

    def get_date(self, string):
        if string is None:
            return datetime.now()
        return datetime.strptime(string.split('T')[0], '%Y-%m-%d')

    def get_quizzes(self, course_name: str):
        if course_name not in self.course_name_to_id:
            return f'Course name {course_name} could not be found'
        course_id = self.course_name_to_id[course_name]
        quizzes = CanvasDataSource.getQuizzes(course_id)

        quizzes = sorted([(q['title'], self.get_date(q['due_at'])) for q in quizzes], key= lambda x: x[1])

        latest = f'{quizzes[0][0]} is due {quizzes[0][1].strftime("%B %d, %Y")}'
        quiz = 'quiz' if len(quizzes) == 1 else 'quizzes'
        return f'You have {len(quizzes)} {quiz} in {course_name}. {latest}'


