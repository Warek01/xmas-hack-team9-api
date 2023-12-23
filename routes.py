from flask import jsonify, request

from __main__ import app

from database.database import db
from models.Group import Group
from models.Professor import Professor
from models.Room import Room
from models.Subject import Subject


@app.route('/api/groups', methods=['POST'])
def add_group():
    data = request.json
    new_group = Group(
        specialty=data['specialty'],
        number_of_people=data['no_of_people'],
        subject_ids=data['subject_ids'],
        language=data['language']
    )
    db.session.add(new_group)
    db.session.commit()
    return jsonify({"message": "Group added successfully"}), 201


@app.route('/api/subjects', methods=['POST'])
def add_subject():
    data = request.json
    new_subject = Subject(
        course_name=data['course_name'],
        student_year=data['year'],
        student_semester=data['semester'],
        theory_lessons=data['no_of_theory_hours'],
        practical_lessons=data['no_of_practice_hours'],
        lab_lessons=data['no_of_laboratory_hours'],
        total=data['total_no_hours']
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


@app.route('api/schedule', methods=['GET'])
def get_schedule():
    return jsonify({"message": "I guess schedule goes here."}), 201


@app.route('api/room', methods=['GET'])
def get_room_status():
    data = request.json
    '''
    Have to get room status after schedule is complete somehow...
    '''
    return jsonify({"message": "I guess room status goes here."}), 201

