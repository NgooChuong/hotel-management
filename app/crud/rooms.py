from sqlalchemy.orm import Session

from app.models.rooms import Room


class CRUDRoom:
    @staticmethod
    def get_query(db: Session):
        return db.query(Room)

    def get_by_hotel(self, db: Session, hotel_id: int):
        return self.get_query(db).filter(Room.hotel_id == hotel_id).all()

    def count_by_hotel(self, db: Session, hotel_id: int) -> int:
        return self.get_query(db).filter(Room.hotel_id == hotel_id).count()

    def get_list(self, db: Session, room_number: str | None = None):
        query = self.get_query(db)
        if room_number:
            query = query.filter(Room.room_number.__eq__(room_number))
        return query


def get_room_crud():
    return CRUDRoom()
