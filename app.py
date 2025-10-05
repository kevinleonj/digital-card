# app.py
# Framework: FastAPI + Starlette
# Purpose: Serve a single mobile-first profile page with session-aware random facts.
# Security: Cookie-only sessions (signed). No user input. Hardened CSP and headers.
# Audience routing: /r (recruiter), /f (friend), or /?audience=recruiter|friend|general

from __future__ import annotations

import os
from typing import Dict, List

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from settings import SETTINGS
from security import SecurityHeadersMiddleware
from facts import FACTS

app = FastAPI(title="Kevin Card", version="1.1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    SessionMiddleware,
    secret_key=SETTINGS.SECRET_KEY,
    session_cookie="kc_s",
    same_site="lax",
    https_only=SETTINGS.PRODUCTION,
)

app.add_middleware(SecurityHeadersMiddleware)

def _wa_link_from_number(number: str) -> str:
    digits = "".join(ch for ch in number if ch.isdigit())
    return f"https://wa.me/{digits}" if len(digits) >= 8 else "#"

def _cv_link() -> str:
    url = SETTINGS.CV_URL.strip()
    if url:
        return url
    local_path = os.path.join("static", "cv", "cv.pdf")
    if os.path.exists(local_path):
        return "/static/cv/cv.pdf"
    return "/static/cv/PUT_YOUR_CV_HERE.txt"

def build_links(audience: str) -> List[Dict[str, str]]:
    common = [
        {"label": "LinkedIn", "href": SETTINGS.LINKEDIN_URL, "id": "lnk_linkedin"},
        {"label": "WhatsApp", "href": _wa_link_from_number(SETTINGS.WHATSAPP_NUMBER), "id": "lnk_whatsapp"},
        {"label": "Email", "href": f"mailto:{SETTINGS.EMAIL_ADDRESS}", "id": "lnk_email"},
        {"label": "CV (PDF)", "href": _cv_link(), "id": "lnk_cv"},
        {"label": "Instagram", "href": SETTINGS.INSTAGRAM_URL, "id": "lnk_instagram"},
        {"label": "Save Contact (vCard)", "href": "/static/kevin.vcf", "id": "lnk_vcard"},
    ]
    if audience == "recruiter":
        order = ["CV (PDF)", "LinkedIn", "Email", "WhatsApp", "Save Contact (vCard)", "Instagram"]
    else:
        order = ["Instagram", "WhatsApp", "LinkedIn", "Email", "CV (PDF)", "Save Contact (vCard)"]
    label_to_item = {x["label"]: x for x in common}
    return [label_to_item[lbl] for lbl in order]

def pick_fact_and_update_session(request: Request) -> str:
    session = request.session
    seen = session.get("seen_facts", [])
    idx, fact = FACTS.pick_unique(seen=seen)
    if idx >= 0:
        seen = list(seen) + [idx]
        if len(seen) > 64:
            seen = seen[-64:]
        session["seen_facts"] = seen
    return fact

def resolve_audience(request: Request) -> str:
    q = request.query_params.get("audience")
    if q in {"recruiter", "friend"}:
        request.session["audience"] = q
        return q
    current = request.session.get("audience")
    if current in {"recruiter", "friend"}:
        return current
    return SETTINGS.DEFAULT_AUDIENCE

@app.get("/healthz", response_class=JSONResponse)
async def healthz() -> dict:
    return {"status": "ok"}

@app.get("/r")
async def recruiter(request: Request):
    request.session["audience"] = "recruiter"
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.get("/f")
async def friend(request: Request):
    request.session["audience"] = "friend"
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    try:
        audience = resolve_audience(request)
        fact = pick_fact_and_update_session(request)
        links = build_links(audience)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "full_name": SETTINGS.FULL_NAME,
            "tagline": SETTINGS.TAGLINE,
            "audience": audience,
            "fact": fact,
            "links": links,
            "base_url": SETTINGS.BASE_URL,
        }, status_code=status.HTTP_200_OK)
    except Exception:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "full_name": SETTINGS.FULL_NAME,
            "tagline": SETTINGS.TAGLINE,
            "audience": "friend",
            "fact": "Content temporarily unavailable.",
            "links": build_links("friend"),
            "base_url": SETTINGS.BASE_URL,
        }, status_code=status.HTTP_200_OK)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return templates.TemplateResponse("404.html", {"request": request, "path": request.url.path}, status_code=404)
    return JSONResponse({"error": "Unexpected error."}, status_code=exc.status_code)

# --------------- Local dev entry ----------------

# For local dev: `uvicorn app:app --reload`
# In production (Azure App Service), run via gunicorn with uvicorn workers:
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
