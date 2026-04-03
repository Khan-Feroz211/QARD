"""Celery application instance with RabbitMQ broker configuration."""

from celery import Celery

from app.config import settings

celery_app = Celery(
    "qard",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.sync_academic",
        "app.tasks.send_alerts",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Karachi",
    enable_utc=True,
    beat_schedule={
        "sync-academic-every-hour": {
            "task": "app.tasks.sync_academic.sync_all_students",
            "schedule": 3600.0,
        },
        "send-alerts-every-15-minutes": {
            "task": "app.tasks.send_alerts.send_pending_alerts",
            "schedule": 900.0,
        },
    },
)
