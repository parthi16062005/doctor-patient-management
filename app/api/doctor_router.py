
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.user import User

from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.schemas.patient import PatientResponse

from app.dependencies import get_current_user, admin_required


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


# Create Doctor - Admin only
@router.post(
    "/",
    response_model=DoctorResponse
)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor.email
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        email=doctor.email,
        is_active=True
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


# Get all Doctors - Logged-in users
@router.get(
    "/",
    response_model=list[DoctorResponse]
)
def get_doctors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Doctor).filter(
        Doctor.is_active == True
    ).all()


# Get Doctor by ID - Logged-in users
@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


# Update Doctor - Admin only
@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def update_doctor(
    doctor_id: int,
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Check if email is already used by another doctor
    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor_data.email,
        Doctor.id != doctor_id
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    doctor.name = doctor_data.name
    doctor.specialization = doctor_data.specialization
    doctor.email = doctor_data.email

    db.commit()
    db.refresh(doctor)

    return doctor


# Delete Doctor - Admin only
# Soft delete
@router.delete(
    "/{doctor_id}"
)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.is_active = False

    db.commit()

    return {
        "message": "Doctor deleted successfully"
    }


# Assign Patient to Doctor
@router.post(
    "/{doctor_id}/patients/{patient_id}",
    response_model=PatientResponse
)
def assign_patient(
    doctor_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    # Check Doctor
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Check Patient
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Assign patient
    patient.doctor_id = doctor_id

    db.commit()
    db.refresh(patient)

    return patient


# Get Patients assigned to a Doctor
@router.get(
    "/{doctor_id}/patients",
    response_model=list[PatientResponse]
)
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check Doctor
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id,
        Doctor.is_active == True
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Admin can view any doctor's patients
    if current_user.role == "admin":
        patients = db.query(Patient).filter(
            Patient.doctor_id == doctor_id
        ).all()

        return patients

    # Doctor can view only their own patients
    if current_user.role == "doctor":
        if current_user.username != doctor.email:
            raise HTTPException(
                status_code=403,
                detail="You can only view your own patients"
            )

        patients = db.query(Patient).filter(
            Patient.doctor_id == doctor_id
        ).all()

        return patients

    raise HTTPException(
        status_code=403,
        detail="Access denied"
    )

