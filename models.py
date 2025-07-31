from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(255), primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255))
    avatar = Column(String(500))
    discriminator = Column(String(10))
    role = Column(String(50), default='Player')
    hasPassword = Column(Integer, default=0)
    passwordHash = Column(Text)
    isActive = Column(Integer, default=1)
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())
    lastLogin = Column(DateTime)

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role = Column(String(50), nullable=False)
    permission = Column(String(100), nullable=False)
    createdAt = Column(DateTime, server_default=func.now()) 