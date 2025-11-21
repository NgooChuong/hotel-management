from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from requests import Session

from app.crud.floors import get_floor_crud
from app.crud.rooms import get_room_crud
from app.enum_custom.status import StatusEnum
from app.schemas.request.base_list_request import BaseListRequest
from app.schemas.request.floor.created_floor import FloorCreate
from app.schemas.request.floor.updated_floor_request import FloorUpdateRequest
from app.schemas.response.floor.detail_floor_response import DetailFloorResponse
from app.schemas.response.room.room_response import RoomResponse


class FloorService:

    def get_list_floors(
            self,
            db: Session,
            pagination: BaseListRequest,
            hotel_id: int | None,
            floor_number: int | None
    ) -> Page:
        query = get_floor_crud().get_list(db, hotel_id, floor_number)
        return paginate(query, params=pagination)

    def get_floor_detail(self, db: Session, floor_id: int):
        floor = get_floor_crud().get_by_id(db, floor_id)
        if not floor:
            raise HTTPException(
                status_code=StatusEnum.NOT_FOUND.code,
                detail=StatusEnum.NOT_FOUND.message
            )

        rooms = get_room_crud().get_by_floor(db, floor_id)
        num_of_room = get_room_crud().count_by_floor(db, floor_id)
        return DetailFloorResponse(
            id=floor.id,
            floor_number=floor.floor_number,
            note=floor.note,
            num_of_room=num_of_room,
            rooms=[RoomResponse.from_orm(r) for r in rooms]
        )

    def create_floor(self, db: Session, floor_in: FloorCreate):
        floor = get_floor_crud().create(db, floor_in)

        if floor_in.room_id is not None:
            get_room_crud().create_list(db=db, floor_id=floor.id, hotel_id=floor.hotel_id,
                                        list_room_rq=floor_in.room_id)
        return floor

    def update_floor(self, db: Session, floor_id: int, floor_in: FloorUpdateRequest):
        floor = get_floor_crud().update(db, floor_id, floor_in)
        if not floor:
            raise HTTPException(status_code=StatusEnum.NOT_FOUND.code, detail=StatusEnum.NOT_FOUND.message)
        return floor


    def delete_floor(self, db: Session, floor_id: int):
        floor = get_floor_crud().get_by_id(db, floor_id=floor_id)
        if not floor:
            raise HTTPException(status_code=StatusEnum.NOT_FOUND.code, detail=StatusEnum.NOT_FOUND.message)
        get_floor_crud().delete(db, floor)


def get_floor_service():
    return FloorService()
