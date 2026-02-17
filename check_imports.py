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
    
    # DB
    from app.db.session import SessionLocal, get_db, Base
    from app.db.base_class import Base as BaseClass
    
    # Models (all 9)
    from app.db.models import (
        User, Org, Membership, IntegrationGoogle,
        AuditLog, Approval, Conversation, Message, Memory
    )
    
    # Services
    from app.services.google_oauth import exchange_code_for_tokens, fetch_userinfo, expiry_from
    
    # Routers
    from app.routers.auth_google import router as auth_router
    
    # App
    from app.main import app
    
    # Verify Base is the same object (critical check)
    assert Base is BaseClass, "FATAL: session.py Base != base_class.py Base"
    
    # Verify all models are registered on the same Base
    table_names = sorted(Base.metadata.tables.keys())
    print(f"  Registered tables ({len(table_names)}): {table_names}")
    
    expected_tables = [
        'approvals', 'auditlogs', 'conversations', 'integrations_google',
        'memberships', 'memories', 'messages', 'orgs', 'users'
    ]
    
    for t in expected_tables:
        assert t in table_names, f"MISSING TABLE: {t}"
    
    print(f"  All {len(expected_tables)} expected tables found.")
    print("All modules imported successfully!")
    
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
