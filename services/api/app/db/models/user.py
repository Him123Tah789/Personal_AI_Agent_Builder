from sqlalchemy import Column, String, DateTime
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class User(Base):
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    memberships = relationship("Membership", back_populates="user", cascade="all, delete-orphan")
    integrations = relationship("IntegrationGoogle", back_populates="user", cascade="all, delete-orphan")
