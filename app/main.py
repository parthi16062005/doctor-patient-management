from fastapi import FastAPI

from app.database import Base, engine

from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient

from app.api.auth import router as auth_router
from app.api.doctor_router import router as doctor_router
from app.api.patient_router import router as patient_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Doctor Patient Management API"
)


# Authentication APIs
app.include_router(auth_router)

# Doctor APIs
app.include_router(doctor_router)

# Patient APIs
app.include_router(patient_router)


@app.get("/")
def home():
    return {
        "message": "Doctor Patient API is working!"
    }