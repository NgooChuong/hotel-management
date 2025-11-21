from typing import Optional

from pydantic import BaseModel, constr, conint


class FloorCreateRequest(BaseModel):
    floor_number: conint(ge=1, le=2000)
    note: Optional[constr(max_length=1000)] = None
