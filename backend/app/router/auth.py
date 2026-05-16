from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.models.users import UserCreate, UserInDB, UserResponse, LoginResponse, LoginRequest
from app.controllers.auth import AuthController
from app.dependencies.users import get_auth_controller


router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def register_user(
    payload: UserCreate,
    controller: AuthController = Depends(get_auth_controller)
) -> UserResponse:
    return await controller.register_user(payload)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse
)
async def login_user(
    payload: LoginRequest,
    controller: AuthController = Depends(get_auth_controller)
) -> LoginResponse:
    return await controller.login_user(payload)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def me(
    token: str = Depends(oauth2_scheme),
    controller: AuthController = Depends(get_auth_controller)
) -> UserResponse:
    return await controller.get_me(token)