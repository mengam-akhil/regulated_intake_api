from pydantic import BaseModel

class ErrorResponse(BaseModel):
    status: str
    error_code: str
    message: str
    request_id: str
