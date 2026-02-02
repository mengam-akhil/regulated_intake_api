from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from db.database import get_db
from db.schemas.ingest import IngestRequest
from db.audit_writer import write_audit_log
from db.enums import RegErrorCode

router = APIRouter()

ALLOWED_DOMAINS = {"banking", "fintech", "insurance"}


@router.post("/ingest")
def ingest(
    payload: IngestRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    request_id = str(uuid4())

    # Rule 1: Invalid document_id
    if payload.document_id <= 0:
        write_audit_log(
            db=db,
            document_id=None,
            action="INGEST_FAILED",
            status="REJECTED",
            actor="system",
            request_id=request_id,
            error_code=RegErrorCode.INVALID_DOCUMENT_ID,
        )
        raise HTTPException(
            status_code=422,
            detail={
                "status": "rejected",
                "error_code": RegErrorCode.INVALID_DOCUMENT_ID,
                "message": "document_id must be greater than zero",
                "request_id": request_id,
            },
        )

    # Rule 2: Unsupported domain
    if payload.domain not in ALLOWED_DOMAINS:
        write_audit_log(
            db=db,
            document_id=payload.document_id,
            action="INGEST_FAILED",
            status="REJECTED",
            actor="system",
            request_id=request_id,
            error_code=RegErrorCode.UNSUPPORTED_DOMAIN,
        )
        raise HTTPException(
            status_code=422,
            detail={
                "status": "rejected",
                "error_code": RegErrorCode.UNSUPPORTED_DOMAIN,
                "message": "unsupported domain",
                "request_id": request_id,
            },
        )

    # Success
    write_audit_log(
        db=db,
        document_id=payload.document_id,
        action="INGEST_SUCCESS",
        status="ACCEPTED",
        actor="system",
        request_id=request_id,
    )

    return {
        "status": "accepted",
        "request_id": request_id,
    }
