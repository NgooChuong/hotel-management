from sqlalchemy import Column, Integer, Text, ForeignKey

from app.models.custombase import CustomBase


class Floor(CustomBase):
    __tablename__ = "hotel_floor"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    floor_number = Column(Integer, nullable=False, index=True)
    note = Column(Text, nullable=True)
    hotel_id = Column(Integer, ForeignKey("hotel_hotel.id"))
