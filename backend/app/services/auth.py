"""Authentication service: password hashing, JWT creation/decoding, and OTP logic."""

import random
import string
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import Tenant, User
from app.models.schemas import StudentLoginRequest, StudentRegisterRequest, TokenResponse

_OTP_STORE: dict[str, str] = {}

ALGORITHM = "HS256"


def hash_password(plain: str) -> str:
    """Return the bcrypt hash of the given plain-text password."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if the plain-text password matches the bcrypt hash."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict) -> str:
    """Create a signed JWT access token that expires after configured hours."""
    expire = datetime.now(timezone.utc) + timedelta(
        hours=settings.ACCESS_TOKEN_EXPIRE_HOURS
    )
    return jwt.encode(
        {**data, "exp": expire, "type": "access"},
        settings.JWT_SECRET,
        algorithm=ALGORITHM,
    )


def create_refresh_token(data: dict) -> str:
    """Create a signed JWT refresh token that expires after configured days."""
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    return jwt.encode(
        {**data, "exp": expire, "type": "refresh"},
        settings.JWT_SECRET,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict | None:
    """Decode and validate a JWT access token; return the payload or None."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None


def create_token_pair(user: User) -> TokenResponse:
    """Build an access + refresh token pair for the given user."""
    data = {"sub": user.id, "tenant_id": user.tenant_id, "role": user.role}
    return TokenResponse(
        access_token=create_access_token(data),
        refresh_token=create_refresh_token(data),
        token_type="bearer",
        user_id=user.id,
    )


async def register_student(db: AsyncSession, payload: StudentRegisterRequest) -> User:
    """Create and persist a new student user after resolving their tenant."""
    result = await db.execute(
        select(Tenant).where(Tenant.slug == payload.university_slug)
    )
    tenant = result.scalar_one_or_none()
    if tenant is None:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"University '{payload.university_slug}' not found",
        )
    user = User(
        tenant_id=tenant.id,
        email=payload.email,
        phone=payload.phone,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        student_id=payload.student_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(
    db: AsyncSession, payload: StudentLoginRequest
) -> User | None:
    """Return the User if credentials are valid, otherwise None."""
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.hashed_password):
        return None
    return user


def _generate_otp(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


async def send_otp(phone: str) -> str:
    """Generate a 6-digit OTP, store it, and return it (actual send handled by notification service)."""
    otp = _generate_otp()
    _OTP_STORE[phone] = otp
    return otp


async def verify_otp(db: AsyncSession, phone: str, code: str) -> bool:
    """Verify the OTP for a phone number and mark the user as verified."""
    stored = _OTP_STORE.get(phone)
    if stored is None or stored != code:
        return False
    del _OTP_STORE[phone]
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    if user:
        user.is_verified = True
        await db.commit()
    return True
