import CanvasDataSource


class CanvasApi:

    def __init__(self):
        self.course_data = {course['name']: course['account_id'] for course in []}

    def get_course_names(self):
        return list(self.course_data.keys())

    def get_gradebook_history(self, course_name: str):
        if course_name not in self.course_data:
            return f'Course name {course_name} could not be found'
        data = [self.course_data[course_name]]

