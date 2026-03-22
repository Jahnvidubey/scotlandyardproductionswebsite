from sqlalchemy import Column, Integer, String, Text
from database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    eventDate = Column(String(50), nullable=False)
    eventType = Column(String(100), nullable=False)
    venue = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
