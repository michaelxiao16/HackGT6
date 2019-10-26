import CanvasDataSource


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
        return f"Your name is: {list(self.courses.values())[0]['user']['name']}"

    def get_grade(self, course_name: str):
        if course_name not in self.course_name_to_id:
            return f'Course name {course_name} could not be found'
        course_id = self.course_name_to_id[course_name]
        course = self.courses[course_id]
        return f"You have a {course['grades']['current_grade']} in {course_name}"


