from pydantic import BaseModel, Field
from typing import Literal, Dict, Any

class IngestRequest(BaseModel):
    domain: Literal["fintech", "health"]
    payload: Dict[str, Any] = Field(
        ..., description="Raw domain-specific payload"
    )
