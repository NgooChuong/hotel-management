from sqlalchemy import Column, Date

from app.core.db import Base


class CustomBase(Base):
    __abstract__ = True

    create_date = Column(Date)
    write_date = Column(Date)
