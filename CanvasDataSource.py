## Getting all canvas info
import requests


ACCESS_TOKEN = '7~fxv2FzexxnfWEu2MzAYVnxlzRVvDFZnvzqhTppuhMO8i8xdZN0THcq5yZfSJmHL3'


def getClasses():
    auth = requests.get(f"https://canvas.instructure.com/api/v1/courses?access_token={ACCESS_TOKEN}")
    return auth.json()

def get_enrollment(course_id: int):
    return requests.get(f'https://canvas.instructure.com/api/v1/courses/{course_id}/enrollments?access_token={ACCESS_TOKEN}').json()


def getAssignments(user_id: int, course_id: int):
    assignments = requests.get(f"https://canvas.instructure.com/api/v1/users/{user_id}/courses/{course_id}/assignments?access_token={ACCESS_TOKEN}")
    return assignments.json()

def getQuizzes(course_id: int):
    return requests.get(f"https://canvas.instructure.com/api/v1/courses/{course_id}/quizzes?access_token={ACCESS_TOKEN}").json()

def getAnnouncement(course_id: int):
    return requests.get(f"https://canvas.instructure.com/api/v1/courses/{course_id}/discussion_topics?only_announcements=true&access_token={ACCESS_TOKEN}").json()




if __name__ == '__main__':
    getClasses()