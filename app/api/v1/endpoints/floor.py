from fastapi import APIRouter, Depends, Path
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.enum_custom.status import StatusEnum
from app.schemas.request.base_list_request import BaseListRequest
from app.schemas.request.floor.created_floor import FloorCreate
from app.schemas.request.floor.updated_floor_request import FloorUpdateRequest
from app.schemas.response.base_response import BaseResponse
from app.schemas.response.floor.detail_floor_response import DetailFloorResponse
from app.schemas.response.floor.floor_response import FloorResponse
from app.service.FloorService import get_floor_service

router = APIRouter()


@router.get("/", response_model=BaseResponse[Page[FloorResponse]])
def read_floors(
        hotel_id: int | None = None,
        floor_number: int | None = None,
        pagination: BaseListRequest = Depends(),
        db: Session = Depends(get_db),
        floor_service=Depends(get_floor_service)
):
    floors = floor_service.get_list_floors(db=db, pagination=pagination, hotel_id=hotel_id, floor_number=floor_number)
    return BaseResponse[Page[FloorResponse]](
        message=StatusEnum.SUCCESS.message,
        code=StatusEnum.SUCCESS.code,
        result=floors
    )


@router.get("/{floor_id}", response_model=BaseResponse[DetailFloorResponse])
def read_floor_detail(
        floor_id: int = Path(..., description="Floor ID"),
        db: Session = Depends(get_db),
        floor_service=Depends(get_floor_service)
):
    floor = floor_service.get_floor_detail(db=db, floor_id=floor_id)
    return BaseResponse[DetailFloorResponse](
        message=StatusEnum.SUCCESS.message,
        code=StatusEnum.SUCCESS.code,
        result=floor
    )


@router.post("/", response_model=BaseResponse[FloorResponse])
def create_floor(
        floor_in: FloorCreate,
        db: Session = Depends(get_db),
        floor_service=Depends(get_floor_service)
):
    floor = floor_service.create_floor(db=db, floor_in=floor_in)
    return BaseResponse[FloorResponse](
        message=StatusEnum.CREATED.message,
        code=StatusEnum.CREATED.code,
        result=floor
    )


@router.put("/{floor_id}", response_model=BaseResponse[FloorResponse])
def update_floor(
        floor_id: int,
        floor_in: FloorUpdateRequest,
        db: Session = Depends(get_db),
        floor_service=Depends(get_floor_service)
):
    floor = floor_service.update_floor(db=db, floor_id=floor_id, floor_in=floor_in)
    return BaseResponse[FloorResponse](
        message=StatusEnum.SUCCESS.message,
        code=StatusEnum.SUCCESS.code,
        result=floor
    )


@router.delete("/", response_model=BaseResponse[None])
def delete_floor(floor_id: int, db: Session = Depends(get_db),
                 floor_service=Depends(get_floor_service)):
    try:
        floor_service.delete_floor(db, floor_id)
        return BaseResponse[None](
            message=StatusEnum.DELETE.message,
            code=StatusEnum.DELETE.code,
            result=None
        )
    except:
        return BaseResponse[None](
            message=StatusEnum.DELETE_ERROR.message,
            code=StatusEnum.DELETE_ERROR.code,
            result=None
        )