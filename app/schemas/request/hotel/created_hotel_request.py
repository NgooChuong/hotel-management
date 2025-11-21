from typing import Optional

from pydantic import BaseModel, constr

from app.schemas.request.floor.created_floor_request import FloorCreateRequest


class HotelCreateRequest(BaseModel):
    name: constr(max_length=50)
    phone: constr(min_length=7, max_length=20)
    address: Optional[str] = None
    floors: Optional[list[FloorCreateRequest]] = None
