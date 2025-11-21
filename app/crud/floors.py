from typing import Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.floors import Floor
from app.schemas.request.floor.created_floor import FloorCreate
from app.schemas.request.floor.updated_floor_request import FloorUpdateRequest


class CRUDFloor:
    @staticmethod
    def get_query(db: Session):
        return db.query(Floor)

    def get_by_hotel(self, db: Session, hotel_id: int):
        return self.get_query(db).filter(Floor.hotel_id == hotel_id).all()

    def count_by_hotel(self, db: Session, hotel_id: int) -> int:
        return self.get_query(db).filter(Floor.hotel_id == hotel_id).count()

    def get_list(self, db: Session, hotel_id: int | None = None, floor_number: int | None = None):
        query = self.get_query(db)
        filters = []
        if hotel_id is not None:
            filters.append(Floor.hotel_id == hotel_id)
        if floor_number is not None:
            filters.append(Floor.floor_number == floor_number)

        if filters:
            query = query.filter(and_(*filters))

        return query

    def get_by_id(self, db: Session, floor_id: int):
        return db.get(Floor, floor_id)

    def create(self, db: Session, floor_rq: FloorCreate) -> Floor:
        floor_data = floor_rq.model_dump(exclude={"room_id"})
        floor = Floor(**floor_data)
        db.add(floor)
        db.commit()
        db.refresh(floor)
        return floor

    def create_list(
            self,
            db: Session,
            hotel_id: int,
            list_floor_rq: list[FloorCreate]
    ) -> Optional[list[Floor]]:

        if not list_floor_rq:
            return None

        floors = []
        for item in list_floor_rq:
            floor_data = item.model_dump()
            floor_data["hotel_id"] = hotel_id
            floor = Floor(**floor_data)
            floors.append(floor)

        db.add_all(floors)
        db.commit()

        for floor in floors:
            db.refresh(floor)

        return floors

    def update(self, db: Session, floor_id: int, floor_rq: FloorUpdateRequest) -> Optional[Floor]:
        floor = db.get(Floor, floor_id)
        if not floor:
            return None
        for field, value in floor_rq.model_dump(exclude_unset=True).items():
            setattr(floor, field, value)
        db.commit()
        db.refresh(floor)
        return floor

    def delete(self, db: Session, floor: Floor ):
        if not floor:
            return None
        db.delete(floor)
        db.commit()


def get_floor_crud():
    return CRUDFloor()

