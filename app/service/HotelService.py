from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from requests import Session

from app.crud.floors import get_floor_crud
from app.crud.hotels import get_hotel_crud
from app.crud.rooms import get_room_crud
from app.enum_custom.status import StatusEnum
from app.schemas.request.base_list_request import BaseListRequest
from app.schemas.request.hotel.created_hotel_request import HotelCreateRequest
from app.schemas.request.hotel.updated_hotel_request import HotelUpdateRequest
from app.schemas.response.floor.floor_response import FloorResponse
from app.schemas.response.hotel.detail_hotel_response import DetailHotelResponse
from app.schemas.response.room.room_response import RoomResponse


class HotelService:

    def get_list_hotels(
            self,
            db: Session,
            pagination: BaseListRequest,
            name: str | None
    ) -> Page:
        query = get_hotel_crud().get_list(db, name)
        return paginate(query, params=pagination)

    def get_hotel_detail(self, db: Session, hotel_id: int):
        hotel = get_hotel_crud().get_by_id(db, hotel_id)
        if not hotel:
            raise HTTPException(
                status_code=StatusEnum.NOT_FOUND.code,
                detail=StatusEnum.NOT_FOUND.message
            )

        floors = get_floor_crud().get_by_hotel(db, hotel_id)
        num_of_floor = get_floor_crud().count_by_hotel(db, hotel_id)

        rooms = get_room_crud().get_by_hotel(db, hotel_id)
        num_of_room = get_room_crud().count_by_hotel(db, hotel_id)
        return DetailHotelResponse(
            id=hotel.id,
            name=hotel.name,
            phone=hotel.phone,
            address=hotel.address,
            num_of_floor=num_of_floor,
            num_of_room=num_of_room,
            floor=[FloorResponse.from_orm(f) for f in floors],
            room=[RoomResponse.from_orm(r) for r in rooms]
        )

    def create_hotel(self, db: Session, hotel_in: HotelCreateRequest):
        return get_hotel_crud().create(db, hotel_in)

    def update_hotel(self, db: Session, hotel_id: int, hotel_in: HotelUpdateRequest):
        hotel = get_hotel_crud().update(db, hotel_id, hotel_in)
        if not hotel:
            raise HTTPException(status_code=StatusEnum.NOT_FOUND.code, detail=StatusEnum.NOT_FOUND.message)
        return hotel


def get_hotel_service():
    return HotelService()
