from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Enable CORS (important for frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] for frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Pydantic model for validation
class ContactRequest(BaseModel):
    name: str
    email: str
    phone: str
    eventDate: str
    eventType: str
    venue: str
    message: str

@app.get("/")
def root():
    return {"status": "Backend running successfully 🚀"}

@app.post("/contact")
def submit_contact(contact: ContactRequest, db: Session = Depends(get_db)):
    new_contact = models.Contact(
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
        eventDate=contact.eventDate,
        eventType=contact.eventType,
        venue=contact.venue,
        message=contact.message
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return {"message": "Your inquiry has been saved!", "id": new_contact.id}
