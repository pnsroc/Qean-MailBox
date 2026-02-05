from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship("EmailAccount", back_populates="user")


class EmailAccount(Base):
    __tablename__ = "email_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String, index=True)

    provider = Column(String, default="manual")

    encrypted_username = Column(String)
    encrypted_password = Column(String)

    imap_host = Column(String)
    imap_port = Column(Integer)
    imap_ssl = Column(Boolean, default=True)

    smtp_host = Column(String)
    smtp_port = Column(Integer)
    smtp_ssl = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="accounts")
