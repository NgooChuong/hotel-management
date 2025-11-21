from typing import Optional

from app.schemas.request.floor.created_floor_request import FloorCreateRequest
from app.schemas.request.room.created_room_request import RoomCreateRequest


class RoomCreate(RoomCreateRequest):
    hotel_id: int
    floor_id: int
