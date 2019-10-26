## Getting all canvas info
import requests


ACCESS_TOKEN = '7~fxv2FzexxnfWEu2MzAYVnxlzRVvDFZnvzqhTppuhMO8i8xdZN0THcq5yZfSJmHL3'

def getClasses():
    auth = requests.get(f"https://canvas.instructure.com/api/v1/courses?access_token={ACCESS_TOKEN}")
    return auth.json()

def get_enrollment(course_id: int):
    return requests.get(f'https://canvas.instructure.com/api/v1/courses/{course_id}/enrollments?access_token={ACCESS_TOKEN}').json()




if __name__ == '__main__':
    getClasses()