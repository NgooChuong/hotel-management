from pydantic import BaseModel
from typing import Optional


class HotelResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True
