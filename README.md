# Kevin QR Card

Mobile-first personal contact card with audience-aware layout and random fun facts per session.

## Modes
- **Friend (default)** at `/` shows Instagram, WhatsApp, LinkedIn first.
- **Recruiter** at `/r` shows CV, LinkedIn, Email, WhatsApp, vCard first.

## Setup
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# generate secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
uvicorn app:app --reload
```

## QR
Set `BASE_URL` in `.env` then:
```bash
python tools/generate_qr.py
```
Creates `static/qr/friend.png` and `static/qr/recruiter.png`.

## Notes
- No database. Facts come from `data/facts.json`.
- Signed cookie session prevents repeated facts in one session.
- CSP forbids inline JS/CSS and third‑party scripts by default.
- Health check at `/healthz`.
