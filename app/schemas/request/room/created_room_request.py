from typing import Optional

from pydantic import BaseModel, constr, conint


class RoomCreateRequest(BaseModel):
    room_number: conint(ge=1, le=2000)
    note: Optional[constr(max_length=1000)] = None
    price: conint(ge=1)
