from database.database import db


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lessons_type = db.Column(db.PickleType) # array [string]
    availability = db.Column(db.PickleType)  # 2d array
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=True)

    subject = db.relationship('Subject', backref=db.backref('professors', lazy=True))
