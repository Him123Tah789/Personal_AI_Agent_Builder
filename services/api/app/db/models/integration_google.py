from sqlalchemy import Column, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class IntegrationGoogle(Base):
    __tablename__ = "integrations_google"

    org_id = Column(UUID(as_uuid=True), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    google_sub = Column(String, nullable=False)
    scopes = Column(String, nullable=False)
    access_token_enc = Column(String, nullable=False)
    refresh_token_enc = Column(String, nullable=True)
    expiry = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    org = relationship("Org", back_populates="integrations")
    user = relationship("User", back_populates="integrations")

    __table_args__ = (
        UniqueConstraint('org_id', 'user_id', name='unique_google_org_user'),
    )
