from sqlalchemy import ForeignKey

from database.database import db


class Subject(db.Model):
    id = db.Column(db.String, primary_key=True)
    course_name = db.Column(db.String)  # unitate_curs
    theory_lessons = db.Column(db.Integer)  # teorie
    practice_lessons = db.Column(db.Integer)  # practica
    laboratory_lessons = db.Column(db.Integer)  # lab
    project_lessons = db.Column(db.String)  # idk total
    student_year = db.Column(db.Integer)  # anul
    semester = db.Column(db.Integer)  # semestru

    group_id = db.Column(db.String, ForeignKey('group.id'))

    def __repr__(self):
        return (f"<Subject id='{self.id}', course_code='{self.course_name}', "
                f"theory_lessons={self.theory_lessons}, practical_lessons={self.practical_lessons}, "
                f"lab_lessons={self.laboratory_lessons}, total='{self.project_lessons}', "
                f"student_year={self.student_year}, student_semester={self.semester}>")
