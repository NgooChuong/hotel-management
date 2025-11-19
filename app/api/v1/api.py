from fastapi import APIRouter
from fastapi_pagination import add_pagination

from app.api.v1.endpoints import hotel

api_router = APIRouter()
api_router.include_router(hotel.router, prefix="/hotels", tags=["Hotels"])
add_pagination(api_router)

