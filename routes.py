import json

from flask import jsonify, request

from __main__ import app

from database.database import db
from models.Group import Group
from models.Professor import Professor
from models.Room import Room
from models.Subject import Subject
import scheduler2


@app.route('/api/groups', methods=['POST', 'GET'])
def add_group():
    if request.method == 'POST':
        data = request.json

        subjects = []

        for s in data['subject_ids']:
            subjects.append(
                db.session.query(Subject).filter(Subject.id == s).first()
            )

        new_group = Group(
            academic_group=data['academic_group'],  # speciality
            total_students=data['total_students'],  # nr_persoane
            language_spoken=data['language_spoken']
        )
        db.session.add(new_group)
        db.session.commit()
        return jsonify({"message": "Group added successfully"}), 201
    else:
        groups = db.session.query(Group).all()
        val = []

        for g in groups:
            subjects = []
            for s in g.subjects:
                subjects.append(s.course_name)
            val.append({
                'name': g.academic_group,
                'language': g.language_spoken,
                'peopleCount': g.total_students,
                'subjects': subjects
            })

        return jsonify(val)


@app.route('/api/subjects', methods=['POST'])
def add_subject():
    data = request.json
    new_subject = Subject(
        course_name=data['course_name'],
        student_year=data['year'],
        semester=data['semester'],
        theory_lessons=data['theory_lessons'],
        practice_lessons=data['practice_lessons'],
        laboratory_lessons=data['laboratory_lessons'],
        project_lessons=data['project_lessons']
    )
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({"message": "Subject added successfully"}), 201


@app.route('/api/rooms', methods=['POST'])
def add_room():
    data = request.json
    new_room = Room(
        room=data['room'],
        number_of_people=data['no_of_people'],
        is_lab=data['lab']
    )
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"message": "Room added successfully"}), 201


@app.route('/api/professor', methods=['POST'])
def add_professor():
    data = request.json
    new_professor = Professor(
        name=data['name'],
        lessons_type=data['lessons_type'],
        availability=data['availability'],
        subject_id=data['subject_id']
    )
    db.session.add(new_professor)
    db.session.commit()
    return jsonify({"message": "Professor added successfully"}), 201


@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    try:
        f = open("schedule.txt", "r")
        return f.read()
    except:
        serie = scheduler2.get_schedule(1)
        print(serie)
        with open("schedule.txt", "w") as f:
            f.write(json.dumps(serie))
        return jsonify(serie), 201


@app.route('/api/room', methods=['GET'])
def get_room_status():
    data = request.json
    '''
    Have to get room status after schedule is complete somehow...
    '''
    return jsonify({"message": "I guess room status goes here."}), 201
