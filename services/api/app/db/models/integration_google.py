import uuid
from sqlalchemy import String, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class GoogleIntegration(Base):
    __tablename__ = "integrations_google"
    __table_args__ = (UniqueConstraint("org_id", "user_id", name="uq_google_org_user"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    google_sub: Mapped[str] = mapped_column(String, nullable=False)
    scopes: Mapped[str] = mapped_column(String, nullable=False)

    access_token_enc: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token_enc: Mapped[str | None] = mapped_column(String, nullable=True)
    expiry: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="google_integration")
