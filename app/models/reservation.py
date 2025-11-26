from app import db

class Reservation:
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='reservation')

    def repr(self):
        return f"Reservation<id='{self.id}', user_id='{self.user_id}'>"