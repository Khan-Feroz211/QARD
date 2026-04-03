"""All SQLAlchemy ORM models for the QARD platform."""

import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Tenant(Base):
    """One row per university / institution."""

    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    logo_url: Mapped[str | None] = mapped_column(Text)
    primary_color: Mapped[str | None] = mapped_column(String(16))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    plan: Mapped[str] = mapped_column(
        Enum("free", "pro", "enterprise", name="tenant_plan"), default="free"
    )
    lms_api_url: Mapped[str | None] = mapped_column(Text)
    lms_api_key: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    users: Mapped[list["User"]] = relationship(back_populates="tenant")
    benefits: Mapped[list["Benefit"]] = relationship(back_populates="tenant")


class User(Base):
    """A student, university admin, or super-admin."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    tenant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("tenants.id"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(32))
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    full_name: Mapped[str] = mapped_column(String(256), nullable=False)
    student_id: Mapped[str | None] = mapped_column(String(64))
    profile_photo_url: Mapped[str | None] = mapped_column(Text)
    role: Mapped[str] = mapped_column(
        Enum("student", "admin", "superadmin", name="user_role"), default="student"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    plan: Mapped[str] = mapped_column(
        Enum("free", "pro", name="user_plan"), default="free"
    )
    stripe_customer_id: Mapped[str | None] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="users")
    virtual_cards: Mapped[list["VirtualCard"]] = relationship(back_populates="user")
    academic_records: Mapped[list["AcademicRecord"]] = relationship(
        back_populates="user"
    )
    usage_events: Mapped[list["UsageEvent"]] = relationship(back_populates="user")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="user")


class VirtualCard(Base):
    """A student's digital identity card."""

    __tablename__ = "virtual_cards"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    card_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    qr_code_data: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="virtual_cards")
    usage_events: Mapped[list["UsageEvent"]] = relationship(back_populates="card")


class AcademicRecord(Base):
    """Semester-level academic record synced from the university LMS."""

    __tablename__ = "academic_records"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    semester: Mapped[str] = mapped_column(String(32), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    gpa: Mapped[float | None] = mapped_column(Float)
    cgpa: Mapped[float | None] = mapped_column(Float)
    program: Mapped[str | None] = mapped_column(String(256))
    department: Mapped[str | None] = mapped_column(String(256))
    status: Mapped[str] = mapped_column(
        Enum("enrolled", "graduated", "on_leave", name="academic_status"),
        default="enrolled",
    )
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="academic_records")
    course_results: Mapped[list["CourseResult"]] = relationship(
        back_populates="academic_record"
    )


class CourseResult(Base):
    """Individual course result within an academic record."""

    __tablename__ = "course_results"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    academic_record_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("academic_records.id"), nullable=False
    )
    course_code: Mapped[str] = mapped_column(String(32), nullable=False)
    course_name: Mapped[str] = mapped_column(String(256), nullable=False)
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
    grade: Mapped[str | None] = mapped_column(String(8))
    marks_obtained: Mapped[float | None] = mapped_column(Float)
    max_marks: Mapped[float | None] = mapped_column(Float)

    academic_record: Mapped["AcademicRecord"] = relationship(
        back_populates="course_results"
    )


class Benefit(Base):
    """A discount or benefit offered to students."""

    __tablename__ = "benefits"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    tenant_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("tenants.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    partner_name: Mapped[str] = mapped_column(String(256), nullable=False)
    discount_percent: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(
        Enum(
            "food",
            "transport",
            "books",
            "health",
            "entertainment",
            name="benefit_category",
        ),
        nullable=False,
    )
    logo_url: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    tenant: Mapped["Tenant | None"] = relationship(back_populates="benefits")


class UsageEvent(Base):
    """A card scan, login, or benefit claim event."""

    __tablename__ = "usage_events"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    card_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("virtual_cards.id"), nullable=False
    )
    merchant_name: Mapped[str | None] = mapped_column(String(256))
    location: Mapped[str | None] = mapped_column(String(512))
    amount_pkr: Mapped[float | None] = mapped_column(Numeric(12, 2))
    event_type: Mapped[str] = mapped_column(
        Enum("scan", "login", "benefit_claimed", name="event_type"), nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    metadata: Mapped[dict | None] = mapped_column(JSON)

    user: Mapped["User"] = relationship(back_populates="usage_events")
    card: Mapped["VirtualCard"] = relationship(back_populates="usage_events")


class Alert(Base):
    """A notification or alert sent to a user."""

    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=_uuid
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    type: Mapped[str] = mapped_column(
        Enum("usage", "expiry", "academic", "system", name="alert_type"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="alerts")
