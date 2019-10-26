import asyncio
import json
import datetime
import TextClient

import CanvasApi


async def report_result(delay):
    await asyncio.sleep(delay)
    c = CanvasApi.CanvasApi()
    grade_data = c.get_all_grades()
    print(str(grade_data))
    with open('student_data.json') as f:
        student = json.load(f)
        last_date = datetime.datetime.fromisoformat(student['last_check'])
        announcements_tuples = c.get_all_new_announcements(last_date)
        for course, announcements in announcements_tuples:
            if len(announcements) != 0:
                TextClient.send_announcement_message()
        assignment_tuples = c.get_all_new_assignments(last_date)
        for course, assignments in assignment_tuples:
            if len(assignments) != 0:
                TextClient.send_assignment_message()
        quiz_tuples = c.get_all_new_quizzes(last_date)
        for course, quizzes in quiz_tuples:
            if len(quizzes) != 0:
                TextClient.send_quiz_message()
        for cl, grade in grade_data:
            if student["current_grades"][cl] != grade:
                student["current_grades"][cl] = grade
                TextClient.send_grade_change_message()
        student['last_check'] = str(datetime.datetime.now())
        with open('student_data.json', 'w') as w:
            json.dump(student, w)


async def checker():
    print("started!")
    while True:
        await report_result(3)
    # print("finished!")


if __name__ == '__main__':
    c = CanvasApi.CanvasApi()
    data = c.get_all_grades()
    print(data)
    with open('student_data.json') as f:
        student = json.load(f)
        for cl, grade in data:
            student['current_grades'][cl] = grade
        student['last_check'] = str(datetime.datetime.now())
    with open('student_data.json', 'w') as w:
        json.dump(student, w)
    asyncio.run(checker())
