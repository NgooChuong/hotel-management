from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.custombase import CustomBase


class Users(CustomBase):
    __tablename__ = "res_users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False, index=True)
    partner_id = Column(Integer, ForeignKey("res_partner.id"), unique=True)