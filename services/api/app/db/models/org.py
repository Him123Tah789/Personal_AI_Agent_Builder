from sqlalchemy import Column, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Org(Base):
    name = Column(String, nullable=False)
    
    # Relationships
    memberships = relationship("Membership", back_populates="org", cascade="all, delete-orphan")
    integrations = relationship("IntegrationGoogle", back_populates="org", cascade="all, delete-orphan")
