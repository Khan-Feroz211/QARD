"""Periodic Celery task: check for expiring cards and send usage alerts."""

import asyncio
from datetime import datetime, timedelta, timezone

from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.send_alerts.send_pending_alerts", bind=True, max_retries=3)
def send_pending_alerts(self) -> dict:
    """Send expiry alerts for cards expiring within the next 7 days."""
    return asyncio.run(_send_pending_alerts_async())


async def _send_pending_alerts_async() -> dict:
    from sqlalchemy import select

    from app.db.database import AsyncSessionLocal
    from app.db.models import VirtualCard
    from app.services.usage import create_alert

    sent = 0
    threshold = datetime.now(timezone.utc) + timedelta(days=7)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(VirtualCard).where(
                VirtualCard.is_active == True,  # noqa: E712
                VirtualCard.expires_at <= threshold,
            )
        )
        cards = result.scalars().all()
        for card in cards:
            try:
                await create_alert(
                    db,
                    user_id=card.user_id,
                    alert_type="expiry",
                    title="Card Expiring Soon",
                    body=f"Your virtual card expires on {card.expires_at.strftime('%Y-%m-%d')}. Please renew.",
                )
                sent += 1
            except Exception:
                pass
    return {"alerts_sent": sent}
