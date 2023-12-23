import json

from flask import Flask

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
            subject = Subject(**item)
            db.session.add(subject)
    db.session.commit()

    with open('__mocks__/academic_groups.json', 'r') as file:
        groups_data = json.load(file)
        for group_data in groups_data:
            subject_ids = group_data.pop('subject_ids', [])
            group = Group(**group_data)
            subjects = Subject.query.filter(Subject.id.in_(subject_ids)).all()
            group.subjects.extend(subjects)
            db.session.add(group)
    db.session.commit()

    with open('__mocks__/professors.json', 'r') as file:
        professors_data = json.load(file)
        for item in professors_data:
            if len(item["subject"]) == 0:
                professor = Professor(
                    id=item["id"],
                    name=item["name"],
                    lessons_type=item["lessons_type"],
                    availability=item["availability"],
                    subject_id=None
                )
            else:
                professor = Professor(
                    id=item["id"],
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
    '''
         with app.app_context():
         db.create_all()
         load_data(db)
    '''
    import routes

    app.run('127.0.0.1', 3000)
