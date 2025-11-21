from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.rooms import Room
from app.schemas.request.room.created_room import RoomCreate
from app.schemas.request.room.updated_room_request import RoomUpdateRequest
from app.schemas.response.room.room_response import RoomResponse


class CRUDStateLog:
    pass
    # def create (self):
