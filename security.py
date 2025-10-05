# security.py
# Purpose: Add hardened HTTP security headers and ensure secure cookies in production.
# Notes: HSTS only applies on HTTPS. Cookies are configured via Starlette SessionMiddleware.


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Awaitable
from settings import SETTINGS


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next: Callable[..., Awaitable[Response]]):
        response = await call_next(request)

        # Content Security Policy: self for everything. Allow data: for images (e.g., QR).
        # No inline scripts or styles. Our JS and CSS are local files under /static.
        csp_parts = [
            "default-src 'self'",
            "script-src 'self'",
            "style-src 'self'",
            "img-src 'self' data:",
            "font-src 'self'",
            "connect-src 'self'",
            "object-src 'none'",
            "base-uri 'self'",
            "frame-ancestors 'none'",
            "form-action 'self'",
            "upgrade-insecure-requests"
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_parts)

        # Other common security headers
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), interest-cohort=()"

        # HSTS for HTTPS only and only in production
        if SETTINGS.PRODUCTION and request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"

        return response
