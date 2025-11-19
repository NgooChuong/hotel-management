from pydantic import BaseModel, constr
from typing import Optional


class HotelUpdateRequest(BaseModel):
    name: Optional[constr(max_length=50)] = None
    phone: Optional[constr(min_length=7, max_length=20)] = None
    address: Optional[str] = None
