"""QARD application configuration via pydantic-settings and environment variables."""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All application settings loaded from environment variables."""

    # App
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "replace-with-32-char-random-string"
    JWT_SECRET: str = "replace-with-long-random-string"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/qard"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # RabbitMQ (Celery broker)
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"

    # MinIO / S3
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "qard-assets"

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRO_PRICE_ID: str = ""

    # JazzCash (Pakistan)
    JAZZCASH_MERCHANT_ID: str = ""
    JAZZCASH_PASSWORD: str = ""
    JAZZCASH_INTEGRITY_SALT: str = ""
    JAZZCASH_ENV: str = "sandbox"

    # Firebase FCM
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_CREDENTIALS_JSON: str = "path/to/serviceAccountKey.json"

    # Twilio (SMS OTP)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_FROM_NUMBER: str = ""

    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5001"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
