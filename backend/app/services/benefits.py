"""Benefits service: catalog retrieval and benefit claim logic."""

from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Benefit, User, UsageEvent, VirtualCard
from app.models.schemas import BenefitResponse


async def get_benefits_for_tenant(
    db: AsyncSession, tenant_id: str
) -> list[BenefitResponse]:
    """Return all active benefits for a tenant, including global ones."""
    result = await db.execute(
        select(Benefit).where(
            or_(Benefit.tenant_id == tenant_id, Benefit.tenant_id.is_(None)),
            Benefit.is_active.is_(True),
        )
    )
    rows = result.scalars().all()
    now = datetime.now(timezone.utc)
    return [
        BenefitResponse(
            id=b.id,
            title=b.title,
            partner_name=b.partner_name,
            discount_percent=b.discount_percent,
            category=b.category,
            logo_url=b.logo_url,
            valid_until=b.valid_until,
        )
        for b in rows
        if b.valid_until is None or b.valid_until > now
    ]


async def claim_benefit(db: AsyncSession, user: User, benefit_id: str) -> None:
    """Log a benefit_claimed usage event for the user."""
    card_result = await db.execute(
        select(VirtualCard)
        .where(VirtualCard.user_id == user.id, VirtualCard.is_active == True)  # noqa: E712
        .order_by(VirtualCard.issued_at.desc())
    )
    card = card_result.scalar_one_or_none()
    if card is None:
        return

    benefit_result = await db.execute(
        select(Benefit).where(Benefit.id == benefit_id)
    )
    benefit = benefit_result.scalar_one_or_none()
    if benefit is None:
        return

    event = UsageEvent(
        user_id=user.id,
        card_id=card.id,
        merchant_name=benefit.partner_name,
        event_type="benefit_claimed",
        metadata={"benefit_id": benefit_id, "discount_percent": benefit.discount_percent},
    )
    db.add(event)
    await db.commit()
