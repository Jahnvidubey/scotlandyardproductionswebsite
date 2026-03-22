#main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel, EmailStr, Field, validator
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import date
import re

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log validation errors for debugging
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Validation error: {exc.errors()}")
    print(f"Body: {await request.body()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    eventDate: Optional[date] = None
    eventType: str = Field(..., min_length=2, max_length=100)
    venueLocation: str = Field(..., min_length=2, max_length=255)
    message: str = Field(..., min_length=5, max_length=1000)

    @validator('phone')
    def validate_phone(cls, v):
        cleaned = re.sub(r'[\s\-\(\)\+]', '', v)
        if not re.match(r'^[6-9]\d{9}$', cleaned):
            raise ValueError('Phone number must be a valid 10-digit Indian number')
        return cleaned

    @validator('eventDate')
    def validate_future_date(cls, v):
        if v is not None:
            today = date.today()
            if v < today:
                raise ValueError('Event date cannot be in the past')
        return v

@app.get("/")
def root():
    return {"status": "Backend running successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/contact")
def submit_contact(contact: ContactRequest, db: Session = Depends(get_db)):
    print(f"Received data: {contact}")
    try:
        new_contact = models.Contact(
            name=contact.name,
            email=contact.email,
            phone=contact.phone,
            eventDate=contact.eventDate,
            eventType=contact.eventType,
            venueLocation=contact.venueLocation,
            message=contact.message
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return {
            "message": "Your inquiry has been saved successfully!",
            "id": new_contact.id,
            "status": "success"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contacts")
def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).offset(skip).limit(limit).all()
    return contacts
