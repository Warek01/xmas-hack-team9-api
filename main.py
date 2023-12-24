import json

from flask import Flask
from flask_cors import CORS

from database.database import db

from dotenv import load_dotenv
import os

from models.Group import Group
from models.Professor import Professor
from models.Room import Room
from models.Subject import Subject


def load_data(db):
    with open('__mocks__/subjects.json', 'r') as file:
        subjects_data = json.load(file)
        for item in subjects_data:
            subject = Subject(id=int(item['id']), course_name=item['course_name'],
                              theory_lessons=item['theory_lessons'], practice_lessons=item['practice_lessons'],
                              laboratory_lessons=item['laboratory_lessons'],
                              project_lessons=item['project_lessons'], student_year=item['student_year'],
                              semester=item['semester'], )
            db.session.add(subject)
    db.session.commit()

    with open('__mocks__/academic_groups.json', 'r') as file:
        groups_data = json.load(file)
        for group_data in groups_data:
            subject_ids = [int(sid.strip()) for sid in group_data.pop('subject_ids', []) if len(sid)]
            print(subject_ids)
            group = Group(id=int(group_data['id']),
                          academic_group=group_data['academic_group'],
                          language_spoken=group_data['academic_group'], total_students=group_data['total_students'])
            subjects = Subject.query.filter(Subject.id.in_(subject_ids)).all()
            group.subjects.extend(subjects)
            db.session.add(group)
    db.session.commit()

    with open('__mocks__/professors.json', 'r') as file:
        professors_data = json.load(file)
        for item in professors_data:
            if len(item["subject"]) == 0:
                professor = Professor(
                    id=int(item["id"]),
                    name=item["name"],
                    lessons_type=item["lessons_type"],
                    availability=item["availability"],
                    subject_id=None
                )
            else:
                professor = Professor(
                    id=int(item["id"]),
                    name=item["name"],
                    lessons_type=item["lessons_type"],
                    availability=item["availability"],
                    subject_id=item["subject"]["id"]
                )
            db.session.add(professor)
    db.session.commit()

    with open('__mocks__/rooms.json', 'r') as file:
        rooms_data = json.load(file)
        for item in rooms_data:
            room = Room(
                id=item["id"],
                nr_persons=item["nr_persons"],
                is_lab_cab=int(item["is_lab_cab"])
            )
            db.session.add(room)
    db.session.commit()


def initialize_flask(host: str, port: int) -> Flask:
    load_dotenv()
    app = Flask(f'{host}:{port}')
    CORS(app)

    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")

    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_password}@127.0.0.1:5432/{postgres_db}'

    db.init_app(app)
    return app


def startup_server(host: str, port: int) -> Flask:
    flask_app = initialize_flask(host, port)
    return flask_app


if __name__ == "__main__":
    app = startup_server('127.0.0.1', 3000)
    '''
     Uncomment code below when first time starting the app to load initial data from mocks
    '''
    # with app.app_context():
    #     db.create_all()
    #     load_data(db)
    import routes

    app.run('127.0.0.1', 3000)
