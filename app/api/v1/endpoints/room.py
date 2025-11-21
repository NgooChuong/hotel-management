from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.enum_custom.status import StatusEnum
from app.schemas.request.base_list_request import BaseListRequest
from app.schemas.request.room.created_room import RoomCreate
from app.schemas.request.room.updated_room_request import RoomUpdateRequest
from app.schemas.response.base_response import BaseResponse
from app.schemas.response.room.room_response import RoomResponse
from app.service.RoomService import get_room_service

router = APIRouter()


@router.get("/", response_model=BaseResponse[Page[RoomResponse]])
def read_rooms(
        hotel_id: int | None = None,
        floor_id: int | None = None,
        pagination: BaseListRequest = Depends(),
        db: Session = Depends(get_db),
        room_service=Depends(get_room_service)
):
    rooms = room_service.get_list_rooms(db=db, pagination=pagination, hotel_id=hotel_id, floor_id=floor_id)
    return BaseResponse[Page[RoomResponse]](
        message=StatusEnum.SUCCESS.message,
        code=StatusEnum.SUCCESS.code,
        result=rooms
    )


@router.get("/{room_id}", response_model=BaseResponse[RoomResponse])
def read_room_detail(
        room_id: int = Path(..., description="Room ID"),
        db: Session = Depends(get_db),
        room_service=Depends(get_room_service)
):
    room = room_service.get_room_detail(db=db, room_id=room_id)
    return BaseResponse[RoomResponse](
        message=StatusEnum.SUCCESS.message,
        code=StatusEnum.SUCCESS.code,
        result=room
    )


@router.post("/", response_model=BaseResponse[RoomResponse])
def create_room(
        room_in: RoomCreate,
        db: Session = Depends(get_db),
        room_service=Depends(get_room_service)
):
    room = room_service.create_room(db=db, hotel_id=room_in.hotel_id, floor_id=room_in.floor_id, room_in=room_in)
    return BaseResponse[RoomResponse](
        message=StatusEnum.CREATED.message,
        code=StatusEnum.CREATED.code,
        result=room
    )


@router.put("/{room_id}", response_model=BaseResponse[RoomResponse])
def update_room(
        room_id: int,
        room_in: RoomUpdateRequest,
        db: Session = Depends(get_db),
        room_service=Depends(get_room_service)
):
    room = room_service.update_room(db=db, room_id=room_id, room_in=room_in)
    return BaseResponse[RoomResponse](
        message=StatusEnum.SUCCESS.message,
        code=StatusEnum.SUCCESS.code,
        result=room
    )


@router.delete("/", response_model=BaseResponse[None])
def delete_room(room_id: int, db: Session = Depends(get_db),
                room_service=Depends(get_room_service)):
    try:
        room_service.delete_room(db, room_id)
        return BaseResponse[None](
            message=StatusEnum.DELETE.message,
            code=StatusEnum.DELETE.code,
            result=None
        )
    except:
        return BaseResponse[None](
            message=StatusEnum.DELETE_ERROR.message,
            code=StatusEnum.DELETE_ERROR.code,
            result=None
        )
