"""Tenant resolution middleware: extracts tenant slug from JWT or subdomain."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class TenantMiddleware(BaseHTTPMiddleware):
    """Resolve the tenant identifier from the request's JWT claim or subdomain."""

    async def dispatch(self, request: Request, call_next) -> Response:
        tenant_slug = self._extract_from_header(request) or self._extract_from_host(request)
        request.state.tenant_slug = tenant_slug
        return await call_next(request)

    @staticmethod
    def _extract_from_header(request: Request) -> str | None:
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None
        token = auth.removeprefix("Bearer ")
        from app.services.auth import decode_access_token

        payload = decode_access_token(token)
        return payload.get("tenant_id") if payload else None

    @staticmethod
    def _extract_from_host(request: Request) -> str | None:
        host = request.headers.get("host", "")
        parts = host.split(".")
        return parts[0] if len(parts) > 2 else None
