from typing import Optional

from app.schemas.request.floor.created_floor_request import FloorCreateRequest
from app.schemas.request.room.created_room_request import RoomCreateRequest


class FloorCreate(FloorCreateRequest):
    hotel_id: int
    room_id: Optional[list[RoomCreateRequest]]
