from flask import Flask, render_template, request
from random import shuffle
import json


def write_booking_json(bookings):
    try:
        data = json.load(open('bookings.json'))
    except:
        data = []

    data.append(bookings)

    with open('bookings.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def write_request_json(requests):
    try:
        data = json.load(open('requests.json'))
    except:
        data = []

    data.append(requests)

    with open('requests.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


app = Flask(__name__)
app.secret_key = 'perfect tutor online'


@app.route('/')
def index():
    with open('data_teachers.json') as file:
        data_teacher = json.loads(file.read())

    shuffle(data_teacher)

    return render_template('index.html', random_tutors=data_teacher)


@app.route('/goals/<goal>/')
def goal(goal):
    with open('data_teachers.json') as file:
        data_teacher = json.loads(file.read())

    sorted_rating_teachers = sorted(data_teacher, key=lambda x: x["rating"], reverse=True)

    list_teachers = []
    for i in range(len(sorted_rating_teachers)):
        for gl in sorted_rating_teachers[i]["goals"]:
            if gl == str(goal):
                list_teachers.append(sorted_rating_teachers[i])

    return render_template('goal.html', list_teachers=list_teachers, goal=goal)


@app.route('/tutors/')
def tutors():
    with open('data_teachers.json') as file:
        data_teachers = json.loads(file.read())

    return render_template('tutors.html', tutors=data_teachers)


@app.route('/profiles/<int:id_tutor>/')
def id_tutor(id_tutor):
    with open('data_teachers.json') as file_teachers:
        data_teacher = json.loads(file_teachers.read())

    with open('data_goals.json') as file_goals:
        data_goals = json.loads(file_goals.read())

    return render_template('profile.html', data=data_teacher, id=id_tutor,
                           goal=data_goals[data_teacher[id_tutor]["goals"][0]])


@app.route('/request/')
def request_send():
    return render_template('request.html')


@app.route('/request_done/', methods=["POST"])
def request_done():
    goal = request.form.get('goal')
    time = request.form.get('time')
    name = request.form.get('name')
    phone = request.form.get('phone')

    with open('data_goals.json') as file:
        dict_goals = json.loads(file.read())

    for key, value in dict_goals.items():
        if key == goal:
            dict_requests = {"goal": value, "time": time, "name": name, "phone": phone}
            write_request_json(dict_requests)

            return render_template('request_done.html', goal=value, time=time, name=name, phone=phone)


@app.route('/booking/<int:id_tutor>/<week_day>/<time>/')
def booking(id_tutor, week_day, time):
    with open('data_teachers.json') as file:
        data_teacher = json.loads(file.read())

    return render_template('booking.html', data=data_teacher, id=id_tutor, week_day=week_day, time=time)


@app.route('/booking_done/', methods=["GET", "POST"])
def booking_done():
    teacher_id = request.form.get("clientTeacherId")
    teacher_name = request.form.get("clientTeacherName")
    week_day = request.form.get("clientWeekday")
    time = request.form.get("clientTime")
    name = request.form.get("clientName")
    phone = request.form.get("clientPhone")

    dict_week_day = {'mon': 'Понедельник', 'tue': 'Вторник', 'wed': 'Среда', 'thu': 'Четверг', 'fri': 'Пятница', 'sat': 'Суббота', 'sun': 'Воскресенье'}

    for key, value in dict_week_day.items():
        if key == week_day:
            dict_bookings = {"teacher_id": teacher_id, "teacher_name": teacher_name, "week_day": value, "time": time, "name": name, "phone": phone}
            write_booking_json(dict_bookings)

            return render_template('booking_done.html', week_day=value, time=time, name=name, phone=phone)


app.run()
