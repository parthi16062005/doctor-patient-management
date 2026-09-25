from pydantic import BaseModel, ConfigDict, Field


class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str = Field(
        pattern=r"^\d{10,15}$"
    )


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    doctor_id: int | None = None

    model_config = ConfigDict(
        from_attributes=True
    )