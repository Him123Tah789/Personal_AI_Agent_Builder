import sys
import os

# Add backend to path (services/api)
sys.path.append(os.path.join(os.getcwd(), 'services', 'api'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), 'services', 'api', '.env'))

try:
    print("Checking imports...")
    
    # Core
    from app.core.config import settings
    from app.core.crypto import encrypt, decrypt
    from app.core.security import create_access_token
    from app.core.deps import get_db, get_current_user
    
    # DB
    from app.db.session import SessionLocal
    from app.db.base import Base
    
    # Models (all 5)
    from app.db.models import User, Org, Membership, GoogleIntegration, AuditLog
    
    # Services
    from app.services.google_oauth import exchange_code_for_tokens, fetch_userinfo, expiry_from
    from app.services.token_store import get_valid_google_access_token
    from app.services.gmail_service import list_threads, get_thread, create_draft
    from app.services.calendar_service import list_upcoming_events
    
    # Routers
    from app.routers.auth_google import router as auth_router
    from app.routers.gmail import router as gmail_router
    from app.routers.calendar import router as cal_router
    
    # App
    from app.main import app
    
    # Verify all models are registered on Base
    table_names = sorted(Base.metadata.tables.keys())
    print(f"  Registered tables ({len(table_names)}): {table_names}")
    
    expected_tables = ['audit_logs', 'integrations_google', 'memberships', 'orgs', 'users']
    
    for t in expected_tables:
        assert t in table_names, f"MISSING TABLE: {t}"
    
    print(f"  All {len(expected_tables)} expected tables found.")
    
    # Verify app routes
    routes = [r.path for r in app.routes if hasattr(r, 'path')]
    print(f"  App routes: {routes}")
    
    expected_routes = ['/health', '/auth/google/callback', '/gmail/threads', '/gmail/thread/{thread_id}', '/gmail/draft', '/calendar/upcoming']
    for r in expected_routes:
        assert r in routes, f"MISSING ROUTE: {r}"
    
    print(f"  All {len(expected_routes)} expected routes found.")
    print("All modules imported successfully!")
    
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
