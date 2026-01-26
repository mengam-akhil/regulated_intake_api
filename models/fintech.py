from pydantic import BaseModel, Field

class FintechTransaction(BaseModel):
    transaction_id: str
    amount: float = Field(..., gt=0)
    currency: str
