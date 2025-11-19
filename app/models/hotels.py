from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.custombase import CustomBase


class Hotel(CustomBase):
    __tablename__ = "hotel_hotel"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    phone = Column(String, nullable=False, index=True)
    address = Column(Text, nullable=True, index=True)
    floors = relationship(argument="Floor", backref="hotel_floors")
    rooms = relationship(argument="Room", backref="hotel_rooms")
