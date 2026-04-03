"""All Pydantic v2 request and response models for the QARD API."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# ── Auth ─────────────────────────────────────────────────────────────────────


class StudentRegisterRequest(BaseModel):
    """Payload for registering a new student account."""

    full_name: str = Field(..., min_length=2, max_length=256)
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=32)
    student_id: str = Field(..., min_length=2, max_length=64)
    password: str = Field(..., min_length=8)
    university_slug: str = Field(..., min_length=2, max_length=64)


class StudentLoginRequest(BaseModel):
    """Payload for student login."""

    email: EmailStr
    password: str
    university_slug: str


class OTPVerifyRequest(BaseModel):
    """Payload to verify a one-time password."""

    phone: str
    otp_code: str = Field(..., min_length=4, max_length=8)


class TokenResponse(BaseModel):
    """JWT token pair returned after successful authentication."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str


# ── Card ─────────────────────────────────────────────────────────────────────


class VirtualCardResponse(BaseModel):
    """Virtual student card data."""

    card_number: str
    holder_name: str
    university_name: str
    university_logo: Optional[str] = None
    student_id: str
    program: Optional[str] = None
    qr_code_data: str
    is_active: bool
    expires_at: Optional[datetime] = None


# ── Academic ─────────────────────────────────────────────────────────────────


class CourseResultSchema(BaseModel):
    """Single course result within an academic record."""

    course_code: str
    course_name: str
    credits: int
    grade: Optional[str] = None
    marks_obtained: Optional[float] = None
    max_marks: Optional[float] = None


class AcademicResponse(BaseModel):
    """Academic record for a single semester."""

    semester: str
    year: int
    gpa: Optional[float] = None
    cgpa: Optional[float] = None
    program: Optional[str] = None
    department: Optional[str] = None
    status: str
    courses: List[CourseResultSchema] = []


# ── Benefits ─────────────────────────────────────────────────────────────────


class BenefitResponse(BaseModel):
    """A single discount or benefit offered to students."""

    id: Optional[str] = None
    title: str
    partner_name: str
    discount_percent: float
    category: str
    logo_url: Optional[str] = None
    valid_until: Optional[datetime] = None


# ── Usage ────────────────────────────────────────────────────────────────────


class UsageEventResponse(BaseModel):
    """A single card usage event."""

    id: str
    merchant_name: str
    location: str
    amount_pkr: Optional[float] = None
    event_type: str
    timestamp: datetime


class AlertResponse(BaseModel):
    """A notification alert sent to a student."""

    id: str
    type: str
    title: str
    body: str
    is_read: bool
    sent_at: datetime


# ── Billing ──────────────────────────────────────────────────────────────────


class PlanUpgradeRequest(BaseModel):
    """Request to upgrade a student's plan."""

    plan: str = Field("pro", pattern="^(pro)$")
    payment_method: str = "stripe"


# ── Tenant / Super Admin ─────────────────────────────────────────────────────


class TenantCreateRequest(BaseModel):
    """Request to create a new university tenant (super-admin only)."""

    name: str = Field(..., min_length=2, max_length=256)
    slug: str = Field(..., min_length=2, max_length=64, pattern="^[a-z0-9-]+$")
    plan: str = Field("free", pattern="^(free|pro|enterprise)$")
    primary_color: Optional[str] = Field(None, max_length=16)
    lms_api_url: Optional[str] = None
