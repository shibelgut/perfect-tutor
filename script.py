from data import goals, teachers
import json


with open('data_goals.json', 'w') as file_goals:
    json.dump(goals, file_goals, ensure_ascii=False, indent=4)


with open('data_teachers.json', 'w') as file_teachers:
    json.dump(teachers, file_teachers, ensure_ascii=False, indent=4)



