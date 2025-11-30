import enum
from app import db

class ReservationStatus(enum.Enum):
    CLOSED = 'closed'
    PENDING = 'pending'
    CANCELED = 'canceled'
    ONGOING = 'ongoing'

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    checkin_date = db.Column(db.Date, nullable=False)
    checkout_date = db.Column(db.Date, nullable=False)

    reservation_status = db.Column(db.Enum("ReservationStatus", name='reservation_status'), nullable=False, default=ReservationStatus.ONGOING)

    user = db.relationship('User', backref='reservation')
    room = db.relationship('Room', backref='reservation')

    @property
    def total_value(self):
        days = (self.checkout_date - self.checkin_date).days()
        return self.room.room_type.daily_price * days

    def repr(self):
        return f"Reservation<id='{self.id}', user_id='{self.user_id}'>"