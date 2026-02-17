from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from sqlalchemy.sql import func

class Memory(Base):
    __tablename__ = "memories" # override default if needed, though pluralizer usually works

    org_id = Column(UUID(as_uuid=True), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    kind = Column(String, nullable=False) # PREFERENCE, PERSON, PROJECT, RULE, SUMMARY
    key = Column(String, nullable=True)
    value = Column(Text, nullable=False)
    source = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
