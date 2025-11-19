from typing import Any, Type

from sqlalchemy.orm import Session
from app.models.hotels import Hotel
from app.schemas.request.hotel.created_hotel_request import HotelCreateRequest
from app.schemas.request.hotel.updated_hotel_request import HotelUpdateRequest


class CRUDHotel:
    @staticmethod
    def get_query(db: Session):
        return db.query(Hotel)

    def get_list(self, db: Session, name: str | None = None):
        query = self.get_query(db)
        if name:
            query = query.filter(Hotel.name.ilike(f"%{name}%"))  # tìm tương đối, không phân biệt hoa thường
        return query

    def get_by_id(self, db: Session, hotel_id: int):
        return self.get_query(db).filter(Hotel.id == hotel_id).first()

    def create(self, db: Session, hotel_in: HotelCreateRequest) -> Hotel:
        hotel = Hotel(**hotel_in.dict())
        db.add(hotel)
        db.commit()
        db.refresh(hotel)
        return hotel

    def update(self, db: Session, hotel_id: int, hotel_in: HotelUpdateRequest) -> Type[Hotel] | None:
        hotel = self.get_by_id(db,hotel_id)
        if not hotel:
            return None
        for field, value in hotel_in.dict(exclude_unset=True).items():
            setattr(hotel, field, value)
        db.commit()
        db.refresh(hotel)
        return hotel


def get_hotel_crud():
    return CRUDHotel()
