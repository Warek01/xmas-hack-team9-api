from database.database import db

subjects_groups = db.Table('subjects_groups',
                           db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
                           db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
                           )


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    academic_group = db.Column(db.String)  # speciality
    language_spoken = db.Column(db.String)  # language
    total_students = db.Column(db.Integer)  # nr_persoane
    subjects = db.relationship('Subject', secondary=subjects_groups,
                               backref=db.backref('groups', lazy='dynamic'))  # subject_ids relation
