from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: int
    room_number: int

    class Config:
        from_attributes = True
