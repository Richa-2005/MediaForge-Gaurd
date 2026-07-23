from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_user,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    user = create_user(payload, db)
    return TokenResponse(
        access_token=create_access_token(user),
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login_user(
    payload: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(payload.email, payload.password, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=create_access_token(user),
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user
