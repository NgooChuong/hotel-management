from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.crud.rooms import get_room_crud
from app.enum_custom.status import StatusEnum
from app.schemas.request.base_list_request import BaseListRequest
from app.schemas.request.room.created_room import RoomCreate
from app.schemas.request.room.updated_room_request import RoomUpdateRequest
from app.schemas.response.room.room_response import RoomResponse


class RoomService:

    def get_list_rooms(
            self,
            db: Session,
            pagination: BaseListRequest,
            hotel_id: int | None = None,
            floor_id: int | None = None
    ) -> Page:
        query = get_room_crud().get_list(hotel_id=hotel_id, floor_id=floor_id, db=db)
        return paginate(query, params=pagination)

    def get_room_detail(self, db: Session, room_id: int) -> RoomResponse:
        room = get_room_crud().get_by_id(db=db, room_id=room_id)
        if not room:
            raise HTTPException(status_code=StatusEnum.NOT_FOUND.code,
                                detail=StatusEnum.NOT_FOUND.message)
        return RoomResponse.from_orm(room)

    def create_room(self, db: Session, floor_id: int, hotel_id: int, room_in: RoomCreate):
        return get_room_crud().create(db=db, hotel_id=hotel_id, floor_id=floor_id, room_in=room_in)

    def update_room(self, db: Session, room_id: int, room_in: RoomUpdateRequest):
        room = get_room_crud().update(db, room_id, room_in)
        if not room:
            raise HTTPException(status_code=StatusEnum.NOT_FOUND.code,
                                detail=StatusEnum.NOT_FOUND.message)
        return room

    def delete_room(self, db: Session, room_id: int):
        room = get_room_crud().get_by_id(db, room_id=room_id)
        if not room:
            raise HTTPException(status_code=StatusEnum.NOT_FOUND.code, detail=StatusEnum.NOT_FOUND.message)
        get_room_crud().delete(db, room)


def get_room_service():
    return RoomService()
