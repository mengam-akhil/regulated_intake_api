from pydantic import BaseModel, Field

class IngestRequest(BaseModel):
    document_id: int = Field(..., gt=0)
    domain: str
    payload: dict
