from fastapi import FastAPI, HTTPException
from uuid import uuid4

from models.request import IngestRequest
from models.fintech import FintechTransaction
from models.health import HealthObservation

app = FastAPI(title="Regulated Intake API")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/ingest")
async def ingest_data(request: IngestRequest):
    request_id = str(uuid4())

    try:
        if request.domain == "fintech":
            validated = FintechTransaction(**request.payload)

        elif request.domain == "health":
            validated = HealthObservation(**request.payload)

        else:
            raise HTTPException(status_code=400, detail="Unsupported domain")

        return {
            "request_id": request_id,
            "domain": request.domain,
            "status": "success",
            "validated_data": validated.model_dump()
        }

    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail={
                "request_id": request_id,
                "error": str(e)
            }
        )
