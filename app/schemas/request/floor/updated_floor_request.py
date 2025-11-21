from typing import Optional

from pydantic import BaseModel, constr, conint


class FloorUpdateRequest(BaseModel):
    floor_number: Optional[conint(ge=1, le=2000)] = None
    note: Optional[constr(max_length=1000)] = None
