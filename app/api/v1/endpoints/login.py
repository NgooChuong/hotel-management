from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette import status

from app.api.deps import get_db
from app.schemas.request.login_request import LoginRequest, UserCreate
from app.schemas.response.login_response import LoginResponse
from app.schemas.response.user_response import UserResponse
from app.service import UserService
from app.service.UserService import get_user_service, user_service

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = user_service.authenticate(db, req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = Authorize.create_access_token(subject=user.id)
    refresh_token = Authorize.create_refresh_token(subject=user.id)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/register", response_model=UserResponse)
def register_user(req: UserCreate, db: Session = Depends(get_db),
                  user_service: UserService = Depends(get_user_service)):
    try:
        user = user_service.register(db, req.username, req.password)
        return UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh")
def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=current_user)
        return {"access_token": new_access_token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))