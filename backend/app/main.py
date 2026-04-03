"""QARD FastAPI application entry point with CORS, lifespan, and router registration."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db
from app.middleware.logging import RequestLoggingMiddleware
from app.routers import academic, admin, auth, benefits, billing, card, health, usage


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    await init_db()
    yield


app = FastAPI(
    title="QARD API",
    description="Virtual Student Card SaaS Platform for Pakistani Universities",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(card.router, prefix="/api/v1/card", tags=["Card"])
app.include_router(academic.router, prefix="/api/v1/academic", tags=["Academic"])
app.include_router(benefits.router, prefix="/api/v1/benefits", tags=["Benefits"])
app.include_router(usage.router, prefix="/api/v1", tags=["Usage"])
app.include_router(billing.router, prefix="/api/v1/billing", tags=["Billing"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])
