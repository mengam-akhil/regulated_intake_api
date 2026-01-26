from pydantic import BaseModel, Field

class HealthObservation(BaseModel):
    patient_id: str
    systolic: int = Field(..., gt=0)
    diastolic: int = Field(..., gt=0)
