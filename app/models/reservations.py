from sqlalchemy import Column, Integer, Date, ForeignKey, Float, Enum
from app.enum_custom.hotel_enum import ReservationStateEnum
from app.models.custombase import CustomBase


class Reservations(CustomBase):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    partner_id = Column(Integer, ForeignKey("res_partner.id"))
    room_id = Column(Integer, ForeignKey("hotel_room.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_price = Column(Float, nullable=False)
    state = Column(Enum(ReservationStateEnum), default=ReservationStateEnum.DRAFT, nullable=False)
