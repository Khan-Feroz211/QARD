"""Periodic Celery task: sync academic records from the university LMS for all students."""

import asyncio

from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.sync_academic.sync_all_students", bind=True, max_retries=3)
def sync_all_students(self) -> dict:
    """Sync LMS academic data for every active student across all tenants."""
    return asyncio.run(_sync_all_students_async())


async def _sync_all_students_async() -> dict:
    from sqlalchemy import select

    from app.db.database import AsyncSessionLocal
    from app.db.models import User
    from app.services.academic import sync_from_lms

    synced = 0
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.is_active == True, User.role == "student")  # noqa: E712
        )
        users = result.scalars().all()
        for user in users:
            try:
                await sync_from_lms(db, user)
                synced += 1
            except Exception:
                pass
    return {"synced": synced}
