from sqlalchemy import Column, String, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Conversation(Base):
    org_id = Column(UUID(as_uuid=True), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    title = Column(String, nullable=True)
    
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False) # user, assistant, tool
    content = Column(Text, nullable=False)
    meta = Column(JSON, nullable=True)
    
    conversation = relationship("Conversation", back_populates="messages")
