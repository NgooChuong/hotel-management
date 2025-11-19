from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page
from requests import Session

from app.api.deps import get_db
from app.enum_custom.status import StatusEnum
from app.schemas.request.base_list_request import BaseListRequest
from app.schemas.request.hotel.created_hotel_request import HotelCreateRequest
from app.schemas.request.hotel.updated_hotel_request import HotelUpdateRequest
from app.schemas.response.base_response import BaseResponse
from app.schemas.response.hotel.detail_hotel_response import DetailHotelResponse
from app.schemas.response.hotel.hotel_response import HotelResponse
from app.service import HotelService
from app.service.HotelService import get_hotel_service

router = APIRouter()


@router.get("/", response_model=BaseResponse[Page[HotelResponse]])
def read_hotels(
        db: Session = Depends(get_db),
        hotel_service: HotelService = Depends(get_hotel_service),
        pagination: BaseListRequest = Depends(),
        name: str | None = Query(None, description="Filter by hotel name")
):
    hotels = hotel_service.get_list_hotels(db, pagination, name)
    return BaseResponse[Page[HotelResponse]](message=StatusEnum.SUCCESS.message, code=StatusEnum.SUCCESS.code,
                                             result=hotels)


@router.get("/{hotel_id}", response_model=BaseResponse[DetailHotelResponse])
def read_hotel_detail(
        hotel_id: int,
        db: Session = Depends(get_db),
        hotel_service: HotelService = Depends(get_hotel_service),
):
    res = hotel_service.get_hotel_detail(db, hotel_id)
    return BaseResponse[DetailHotelResponse](message=StatusEnum.SUCCESS.message, code=StatusEnum.SUCCESS.code,
                                             result=res)


@router.post("/", response_model=BaseResponse[HotelResponse])
def create_hotel(
        hotel_in: HotelCreateRequest,
        db: Session = Depends(get_db),
        hotel_service: HotelService = Depends(get_hotel_service)
):
    res = hotel_service.create_hotel(db, hotel_in)
    return BaseResponse[HotelResponse](message=StatusEnum.CREATED.message, code=StatusEnum.CREATED.code,
                                       result=res)


@router.put("/{hotel_id}", response_model=BaseResponse[HotelResponse])
def update_hotel(
        hotel_id: int,
        hotel_in: HotelUpdateRequest,
        db: Session = Depends(get_db),
        hotel_service: HotelService = Depends(get_hotel_service)
):
    res = hotel_service.update_hotel(db, hotel_id, hotel_in)
    return BaseResponse[HotelResponse](message=StatusEnum.SUCCESS.message, code=StatusEnum.SUCCESS.code,
                                       result=res)
