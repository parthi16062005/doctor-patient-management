from pydantic import BaseModel, ConfigDict, EmailStr


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: EmailStr


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)