from pydantic import BaseModel


class FloorHotelResponse(BaseModel):
    id: int
    floor_number: int
    hotel_name: str

    class Config:
        from_attributes = True
