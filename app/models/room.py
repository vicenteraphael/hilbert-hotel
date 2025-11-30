import enum
from app import db

class RoomType(db.Model):
    __tablename__ = 'room_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    min_capacity = db.Column(db.Integer, nullable=False)
    daily_price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)

    rooms = db.relationship("Room", back_populates='room_type')

class CLEANING_STATUS (enum.Enum):
    DIRTY = "dirty"
    CLEANING = "cleaning"
    CLEAN = "clean"


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'))
    
    number = db.Column(db.String(10), nullable=False, unique=True)
    cleaning_status = db.Column(db.Enum(CLEANING_STATUS, name="cleaning_status"), nullable=False, default=CLEANING_STATUS.CLEAN)
    localization = db.Column(db.String(50))

    room_type = db.relationship("RoomType", back_populates='rooms')