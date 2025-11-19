from pydantic import BaseModel


class FloorResponse(BaseModel):
    id: int
    floor_number: int

    class Config:
        from_attributes = True
