from pydantic import BaseModel


class FloorResponse(BaseModel):
    id: int
    floor_number: int
    note: str | None

    class Config:
        from_attributes = True
