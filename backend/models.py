#models.py
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    eventDate = Column(Date, nullable=True)
    eventType = Column(String(100), nullable=False)
    venueLocation = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    date = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    cover_image = Column(String(500), nullable=True)
    category = Column(String(100), nullable=False)
    testimonial = Column(Text, nullable=True)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    images = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan", order_by="ProjectImage.sort_order")

class ProjectImage(Base):
    __tablename__ = "project_images"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    src = Column(String(500), nullable=False)
    alt = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    event_group = Column(String(100), nullable=True)   # e.g. "haldi", "wedding"
    sort_order = Column(Integer, default=0)
    project = relationship("Project", back_populates="images")
