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

# Day 27 — legal agentic router
from core.legal.agentic_router import cross_verify_lawfulness, Decision

# Day 28 — performance profiling
from core.performance.profiler import profile_block

# Day 29 — defensive API wrapper
from core.security.input_guard import validate_input


router = APIRouter()

ALLOWED_DOMAINS = {"banking", "fintech", "insurance"}


@router.post("/ingest")
def ingest(
    payload: IngestRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    request_id = str(uuid4())

    # =================================================
    # Day 29 — Defensive Input Validation (FAIL CLOSED)
    # =================================================
    validate_input(payload)

    # -------------------------------------------------
    # Rule 1: Invalid document_id
    # -------------------------------------------------
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

    # -------------------------------------------------
    # Rule 2: Unsupported domain
    # -------------------------------------------------
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
    # Day 28 — Profile critical compliance path
    # =================================================
    with profile_block("ingest_pipeline"):

        # =================================================
        # Day 26 — PII Tokenization (GDPR Art. 5)
        # =================================================
        pii_token = None
        if hasattr(payload, "customer_email") and payload.customer_email:
            pii_token = tokenize_pii(payload.customer_email)
            # Raw PII is never persisted

        # =================================================
        # Day 27 — Legal Cross-Verification (GDPR × FADP)
        # =================================================
        legal_context = {
            "gdpr_applies": payload.domain in {"banking", "fintech"},
            "fadp_applies": payload.domain == "banking",
            "has_consent": getattr(payload, "has_consent", False),
            "pii_tokenized": pii_token is not None,
            "rtbf_supported": True,
        }

        legal_result = cross_verify_lawfulness(legal_context)

        if legal_result["decision"] == Decision.BLOCK:
            write_audit_log(
                db=db,
                document_id=payload.document_id,
                action="INGEST_BLOCKED",
                status="REJECTED",
                actor="system",
                request_id=request_id,
                error_code="LEGAL_BLOCK",
            )

            raise HTTPException(
                status_code=403,
                detail={
                    "status": "blocked",
                    "reasons": legal_result["reasons"],
                    "request_id": request_id,
                },
            )

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
        )

    return {
        "status": "accepted",
        "request_id": request_id,
        "legal_decision": legal_result["decision"],
    }
