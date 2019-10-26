import asyncio
import json
import datetime
import TextClient

import CanvasApi


async def report_result(delay):
    await asyncio.sleep(delay)
    c = CanvasApi.CanvasApi()
    data = c.get_all_grades()
    print(str(data))
    with open('student_data.json') as f:
        student = json.load(f)
        for cl, grade in data:
            if student["current_grades"][cl] != grade:
                student["current_grades"][cl] = grade
                TextClient.send_message()
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
