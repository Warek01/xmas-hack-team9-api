from database.database import db


class Room(db.Model):
    id = db.Column(db.String, primary_key=True)
    is_lab_cab = db.Column(db.Boolean)
    nr_persons = db.Column(db.Integer)

    def __repr__(self):
        return f'<Room {self.id}>'
