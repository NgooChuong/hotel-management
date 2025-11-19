from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.custombase import CustomBase


class Room(CustomBase):
    __tablename__ = "hotel_room"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_number = Column(String, nullable=False, index=True)
    note = Column(Text, nullable=True)
    hotel_id = Column(Integer, ForeignKey("hotel_hotel.id"))
    reservations = relationship(argument="Reservations", backref="room_reservations")
    state_log_id = relationship(argument="StateLog", backref="room_state_log")
