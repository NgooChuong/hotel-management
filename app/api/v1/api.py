from fastapi import APIRouter
from fastapi_pagination import add_pagination

from app.api.v1.endpoints import hotel, floor, room, login

api_router = APIRouter()
api_router.include_router(hotel.router, prefix="/hotels", tags=["Hotels"])
api_router.include_router(floor.router, prefix="/floors", tags=["Floors"])
api_router.include_router(room.router, prefix="/rooms", tags=["Rooms"])
api_router.include_router(login.router, prefix="/auth", tags=["Authentication"])

add_pagination(api_router)
