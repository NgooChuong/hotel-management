from app.schemas.response.floor.floor_response import FloorResponse
from app.schemas.response.room.room_response import RoomResponse


class DetailFloorResponse(FloorResponse):
    num_of_room: int
    rooms: list[RoomResponse]

    class Config:
        from_attributes = True
