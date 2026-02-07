from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
import hashlib
import json

from db.database import get_db
from db.schemas.ingest import IngestRequest
from db.audit_writer import write_audit_log
from db.enums import RegErrorCode

# Day 25 — ingestion lineage
from core.ingestion.event_log import write_ingestion_event

# Day 26 — privacy shield
from core.privacy.pii_tokenizer import tokenize_pii

router = APIRouter()

ALLOWED_DOMAINS = {"banking", "fintech", "insurance"}


@router.post("/ingest")
def ingest(
    payload: IngestRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    request_id = str(uuid4())

    # -----------------------------
    # Rule 1: Invalid document_id
    # -----------------------------
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

    # -----------------------------
    # Rule 2: Unsupported domain
    # -----------------------------
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

    # =================================================
    # Day 26 — PII Tokenization (GDPR Art. 5)
    # =================================================
    pii_token = None
    if hasattr(payload, "customer_email") and payload.customer_email:
        pii_token = tokenize_pii(payload.customer_email)
        # IMPORTANT: raw PII stops here and is never stored

    # =================================================
    # Day 25 — Kafka-style ingestion lineage event
    # =================================================
    payload_hash = hashlib.sha256(
        json.dumps(payload.dict(), sort_keys=True).encode()
    ).hexdigest()

    write_ingestion_event(
        source="api:/ingest",
        document_id=payload.document_id,
        payload_hash=payload_hash,
        actor="system",
    )

    # =================================================
    # Business audit log
    # =================================================
    write_audit_log(
        db=db,
        document_id=payload.document_id,
        action="INGEST_SUCCESS",
        status="ACCEPTED",
        actor="system",
        request_id=request_id,
        # pii_token=pii_token  # include only if your audit schema supports it
    )

    return {
        "status": "accepted",
        "request_id": request_id,
    }
