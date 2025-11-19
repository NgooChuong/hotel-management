from app.schemas.response.floor.floor_response import FloorResponse
from app.schemas.response.hotel.hotel_response import HotelResponse
from app.schemas.response.room.room_response import RoomResponse


class DetailHotelResponse(HotelResponse):
    num_of_floor: int
    num_of_room: int
    floor: list[FloorResponse]
    room: list[RoomResponse]

    class Config:
        from_attributes = True
