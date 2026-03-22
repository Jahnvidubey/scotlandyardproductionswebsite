#models.py
from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from database import Base
from sqlalchemy.sql import func

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Mandatory
    email = Column(String(255), nullable=False)  # Mandatory
    phone = Column(String(20), nullable=False)  # Mandatory - increased phone number length
    eventDate = Column(Date, nullable=True)  # Date type instead of String
    eventType = Column(String(100), nullable=False)  # Mandatory
    venueLocation = Column(String(255), nullable=False)  # Mandatory
    message = Column(Text, nullable=False)  # Mandatory
    created_at = Column(DateTime, server_default=func.now())  # Auto timestamp