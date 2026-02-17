# Jarvis MVP — Production-Ready Backend Walkthrough

## What Changed

Complete rewrite of all backend modules to production-quality code.

### Models (Modern `Mapped` Syntax)

| Model | Table | File |
|-------|-------|------|
| `User` | `users` | `services/api/app/db/models/user.py` |
| `Org` | `orgs` | `services/api/app/db/models/org.py` |
| `Membership` | `memberships` | `services/api/app/db/models/membership.py` |
| `GoogleIntegration` | `integrations_google` | `services/api/app/db/models/integration_google.py` |
| `AuditLog` | `audit_logs` | `services/api/app/db/models/audit_log.py` |

### Core Services

| File | Purpose |
|------|---------|
| `app/core/deps.py` | JWT bearer extraction → `get_current_user` |
| `app/services/token_store.py` | Decrypt token, check expiry, auto-refresh via Google |
| `app/services/gmail_service.py` | `list_threads`, `get_thread`, `create_draft` |
| `app/services/calendar_service.py` | `list_upcoming_events` |

### API Routes (6 endpoints)

| Route | Method | Auth | Router |
|-------|--------|------|--------|
| `/health` | GET | None | `app/main.py` |
| `/auth/google/callback` | POST | None | `app/routers/auth_google.py` |
| `/gmail/threads` | GET | JWT | `app/routers/gmail.py` |
| `/gmail/thread/{id}` | GET | JWT | `app/routers/gmail.py` |
| `/gmail/draft` | POST | JWT | `app/routers/gmail.py` |
| `/calendar/upcoming` | GET | JWT | `app/routers/calendar.py` |

### Alembic

Initialized at `services/api/alembic.ini` with custom `app/db/migrations/env.py` that loads `Base` + all models.

## Verification

```
$ python check_imports.py
Checking imports...
  Registered tables (5): ['audit_logs', 'integrations_google', 'memberships', 'orgs', 'users']
  All 5 expected tables found.
  App routes: ['/health', '/auth/google/callback', '/gmail/threads', ...]
  All 6 expected routes found.
All modules imported successfully!
```

## How to Run

```bash
# From services/api/
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Start Postgres + Redis
docker compose -f ../../infra/docker-compose.yml up -d

# Run migrations
alembic revision --autogenerate -m "init"
alembic upgrade head

# Start API
uvicorn app.main:app --reload --port 8000
```

## Next Steps

1. Set `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` in `services/api/.env`
2. Build the LLM provider interface (`openai_provider.py`) with `/chat` endpoint
3. Build the Next.js Dashboard UI
