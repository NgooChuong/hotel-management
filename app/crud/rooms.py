from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.rooms import Room
from app.schemas.request.room.created_room import RoomCreate
from app.schemas.request.room.updated_room_request import RoomUpdateRequest
from app.schemas.response.room.room_response import RoomResponse


class CRUDRoom:
    @staticmethod
    def get_query(db: Session):
        return db.query(Room)

    def get_by_hotel(self, db: Session, hotel_id: int):
        return self.get_query(db).filter(Room.hotel_id == hotel_id).all()

    def get_by_floor(self, db: Session, floor_id: int):
        return self.get_query(db).filter(Room.floor_id == floor_id).all()

    def get_by_id(self, db: Session, room_id: int):
        return db.get(Room, room_id)

    def count_by_hotel(self, db: Session, hotel_id: int) -> int:
        return self.get_query(db).filter(Room.hotel_id == hotel_id).count()

    def count_by_floor(self, db: Session, floor_id: int) -> int:
        return self.get_query(db).filter(Room.floor_id == floor_id).count()

    def get_list(self, db: Session, room_number: int | None = None, hotel_id: int | None = None,
                 floor_id: int | None = None):
        query = self.get_query(db)

        filters = []
        if room_number is not None:
            filters.append(Room.room_number == room_number)
        if hotel_id is not None:
            filters.append(Room.hotel_id == hotel_id)
        if floor_id is not None:
            filters.append(Room.floor_id == floor_id)

        if filters:
            query = query.filter(and_(*filters))

        return query

    def create(
            self,
            db: Session,
            hotel_id: int,
            floor_id: int,
            room_in: RoomCreate
    ) -> RoomResponse:
        room_data = room_in.model_dump()
        room_data["hotel_id"] = hotel_id
        room_data["floor_id"] = floor_id
        room = Room(**room_data)
        db.add(room)
        db.commit()
        db.refresh(room)

        return room

    def create_list(
            self,
            db: Session,
            hotel_id: int,
            floor_id: int,
            list_room_rq: list[RoomCreate]
    ) -> Optional[list[Room]]:

        if not list_room_rq:
            return None

        rooms = []
        for item in list_room_rq:
            room_data = item.model_dump()
            room_data["hotel_id"] = hotel_id
            room_data["floor_id"] = floor_id
            room = Room(**room_data)
            rooms.append(room)

        db.add_all(rooms)
        db.commit()

        for room in rooms:
            db.refresh(room)

        return rooms

    def update(self, db: Session, room_id: int, room_rq: RoomUpdateRequest) -> Optional[Room]:
        room = db.get(Room, room_id)
        if not room:
            return None
        for field, value in room_rq.model_dump(exclude_unset=True).items():
            setattr(room, field, value)
        db.commit()
        db.refresh(room)
        return room


    def delete(self, db: Session, room: Room ):
        if not room:
            return None
        db.delete(room)
        db.commit()

def get_room_crud():
    return CRUDRoom()
