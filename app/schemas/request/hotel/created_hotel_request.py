from pydantic import BaseModel, constr
from typing import Optional


class HotelCreateRequest(BaseModel):
    name: constr(max_length=50)
    phone: constr(min_length=7, max_length=20)
    address: Optional[str] = None
