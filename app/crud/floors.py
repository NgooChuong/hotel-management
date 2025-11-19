from sqlalchemy.orm import Session

from app.models.floors import Floor


class CRUDFloor:
    @staticmethod
    def get_query(db: Session):
        return db.query(Floor)

    def get_by_hotel(self, db: Session, hotel_id: int):
        return self.get_query(db).filter(Floor.hotel_id == hotel_id).all()

    def count_by_hotel(self, db: Session, hotel_id: int) -> int:
        return self.get_query(db).filter(Floor.hotel_id == hotel_id).count()

    def get_list(self, db: Session, floor_number: str | None = None):
        query = self.get_query(db)
        if floor_number:
            query = query.filter(Floor.floor_number.__eq__(floor_number))  # tìm tương đối, không phân biệt hoa thường
        return query


def get_floor_crud():
    return CRUDFloor()
