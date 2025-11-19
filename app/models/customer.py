from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.custombase import CustomBase


class Customer(CustomBase):
    __tablename__ = "res_partner"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    cccd = Column(String, nullable=False, index=True, unique=True)
    phone = Column(String(11), nullable=False, index=True, unique=True)
    email = Column(String, nullable=False, index=True, unique=True)
    user = relationship(argument="Users", uselist=False, backref="partner_user")
    reservations = relationship(argument="Reservations", backref="partner_reservations")
