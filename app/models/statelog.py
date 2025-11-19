from sqlalchemy import Column, Integer, ForeignKey, Date, Text, Enum

from app.enum_custom.hotel_enum import RoomStateEnum
from app.models.custombase import CustomBase


class StateLog(CustomBase):
    __tablename__ = "hotel_state_log"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("hotel_room.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    note = Column(Text, nullable=True)
    state = Column(Enum(RoomStateEnum), default=RoomStateEnum.AVAILABLE, nullable=False)


