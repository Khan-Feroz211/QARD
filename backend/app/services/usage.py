"""Usage service: log usage events, alert triggers, and history queries."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Alert, User, UsageEvent
from app.models.schemas import AlertResponse, UsageEventResponse


async def get_usage_history(
    db: AsyncSession, user: User
) -> list[UsageEventResponse]:
    """Return all usage events for the student, most recent first."""
    result = await db.execute(
        select(UsageEvent)
        .where(UsageEvent.user_id == user.id)
        .order_by(UsageEvent.timestamp.desc())
    )
    rows = result.scalars().all()
    return [
        UsageEventResponse(
            id=e.id,
            merchant_name=e.merchant_name or "",
            location=e.location or "",
            amount_pkr=float(e.amount_pkr) if e.amount_pkr else None,
            event_type=e.event_type,
            timestamp=e.timestamp,
        )
        for e in rows
    ]


async def get_unread_alerts(db: AsyncSession, user: User) -> list[AlertResponse]:
    """Return all unread alerts for the student."""
    result = await db.execute(
        select(Alert)
        .where(Alert.user_id == user.id, Alert.is_read == False)  # noqa: E712
        .order_by(Alert.sent_at.desc())
    )
    rows = result.scalars().all()
    return [
        AlertResponse(
            id=a.id,
            type=a.type,
            title=a.title,
            body=a.body,
            is_read=a.is_read,
            sent_at=a.sent_at,
        )
        for a in rows
    ]


async def mark_alert_read(db: AsyncSession, user: User, alert_id: str) -> None:
    """Mark a specific alert as read for the given user."""
    result = await db.execute(
        select(Alert).where(Alert.id == alert_id, Alert.user_id == user.id)
    )
    alert = result.scalar_one_or_none()
    if alert:
        alert.is_read = True
        await db.commit()


async def create_alert(
    db: AsyncSession,
    user_id: str,
    alert_type: str,
    title: str,
    body: str,
) -> Alert:
    """Create and persist a new alert for the given user."""
    alert = Alert(user_id=user_id, type=alert_type, title=title, body=body)
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert
