"""Card service: generate virtual card, QR code, scan events, and regeneration."""

import io
import uuid
from datetime import datetime, timedelta, timezone

import qrcode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, UsageEvent, VirtualCard
from app.models.schemas import VirtualCardResponse


async def create_virtual_card(db: AsyncSession, user: User) -> VirtualCard:
    """Issue a new virtual card for the given user."""
    card_number = str(uuid.uuid4()).replace("-", "").upper()[:20]
    qr_data = f"QARD:{user.tenant_id}:{user.student_id}:{card_number}"
    expires_at = datetime.now(timezone.utc) + timedelta(days=365)

    card = VirtualCard(
        user_id=user.id,
        card_number=card_number,
        qr_code_data=qr_data,
        expires_at=expires_at,
    )
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return card


def _generate_qr_base64(data: str) -> str:
    """Return a base64-encoded PNG QR code for the given data string."""
    import base64

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


async def get_active_card(db: AsyncSession, user: User) -> VirtualCardResponse:
    """Return the user's currently active virtual card."""
    result = await db.execute(
        select(VirtualCard)
        .where(VirtualCard.user_id == user.id, VirtualCard.is_active == True)  # noqa: E712
        .order_by(VirtualCard.issued_at.desc())
    )
    card = result.scalar_one_or_none()
    if card is None:
        card = await create_virtual_card(db, user)

    from app.db.models import Tenant, AcademicRecord

    tenant_result = await db.execute(
        select(Tenant).where(Tenant.id == user.tenant_id)
    )
    tenant = tenant_result.scalar_one_or_none()

    academic_result = await db.execute(
        select(AcademicRecord)
        .where(AcademicRecord.user_id == user.id)
        .order_by(AcademicRecord.synced_at.desc())
    )
    academic = academic_result.scalar_one_or_none()

    return VirtualCardResponse(
        card_number=card.card_number,
        holder_name=user.full_name,
        university_name=tenant.name if tenant else "",
        university_logo=tenant.logo_url if tenant else None,
        student_id=user.student_id or "",
        program=academic.program if academic else None,
        qr_code_data=card.qr_code_data or "",
        is_active=card.is_active,
        expires_at=card.expires_at,
    )


async def log_scan_event(
    db: AsyncSession,
    user: User,
    merchant_name: str,
    location: str,
) -> None:
    """Record a card scan usage event."""
    result = await db.execute(
        select(VirtualCard)
        .where(VirtualCard.user_id == user.id, VirtualCard.is_active == True)  # noqa: E712
        .order_by(VirtualCard.issued_at.desc())
    )
    card = result.scalar_one_or_none()
    if card is None:
        return

    event = UsageEvent(
        user_id=user.id,
        card_id=card.id,
        merchant_name=merchant_name,
        location=location,
        event_type="scan",
    )
    db.add(event)
    card.last_used_at = datetime.now(timezone.utc)
    await db.commit()


async def regenerate_card(db: AsyncSession, user: User) -> VirtualCardResponse:
    """Deactivate the current card and issue a new one."""
    result = await db.execute(
        select(VirtualCard).where(
            VirtualCard.user_id == user.id, VirtualCard.is_active == True  # noqa: E712
        )
    )
    for old_card in result.scalars().all():
        old_card.is_active = False

    await db.commit()
    await create_virtual_card(db, user)
    return await get_active_card(db, user)
