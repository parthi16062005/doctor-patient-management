from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.patient import PatientCreate, PatientResponse
from app.dependencies import get_current_user, admin_required
from app.models.user import User


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# Create Patient - Admin only
@router.post(
    "/",
    response_model=PatientResponse
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        phone=patient.phone
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


# Get all Patients - Admin only
@router.get(
    "/",
    response_model=list[PatientResponse]
)
def get_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    return db.query(Patient).all()


# Get Patient by ID - Admin only
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient