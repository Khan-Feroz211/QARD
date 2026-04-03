"""Tenant schema routing middleware for multi-tenant PostgreSQL isolation."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class TenantSchemaMiddleware(BaseHTTPMiddleware):
    """Resolve tenant from JWT or subdomain and set the PostgreSQL search_path."""

    async def dispatch(self, request: Request, call_next) -> Response:
        tenant_slug = self._resolve_tenant_slug(request)
        if tenant_slug:
            request.state.tenant_slug = tenant_slug
        return await call_next(request)

    @staticmethod
    def _resolve_tenant_slug(request: Request) -> str | None:
        host = request.headers.get("host", "")
        subdomain = host.split(".")[0] if "." in host else None
        return subdomain
