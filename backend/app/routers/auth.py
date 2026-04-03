"""Auth router: register, login, and OTP endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.schemas import (
    OTPVerifyRequest,
    StudentLoginRequest,
    StudentRegisterRequest,
    TokenResponse,
)
from app.services import auth as auth_service
from app.services import card as card_service
from app.services import notification as notification_service

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: StudentRegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Register a new student, create their virtual card, and return a token pair."""
    user = await auth_service.register_student(db, payload)
    await card_service.create_virtual_card(db, user)
    tokens = auth_service.create_token_pair(user)
    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: StudentLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Authenticate a student and return a JWT token pair."""
    user = await auth_service.authenticate_user(db, payload)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return auth_service.create_token_pair(user)


@router.post("/otp/send", status_code=status.HTTP_200_OK)
async def send_otp(phone: str) -> dict:
    """Send a one-time password to the given phone number."""
    await notification_service.send_sms_otp(phone)
    return {"message": "OTP sent"}


@router.post("/otp/verify", status_code=status.HTTP_200_OK)
async def verify_otp(
    payload: OTPVerifyRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Verify the OTP and mark the user as verified."""
    verified = await auth_service.verify_otp(db, payload.phone, payload.otp_code)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP",
        )
    return {"message": "Phone verified"}
