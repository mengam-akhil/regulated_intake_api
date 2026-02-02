from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.audit_log import AuditLog

router = APIRouter(prefix="/documents", tags=["Audit"])


@router.get("/{document_id}/audit")
def get_audit_trail(document_id: int, db: Session = Depends(get_db)):
    logs = (
        db.query(AuditLog)
        .filter(AuditLog.document_id == document_id)
        .order_by(AuditLog.created_at.asc())
        .all()
    )

    return [
        {
            "action": log.action,
            "actor": log.actor,
            "timestamp": log.created_at,
        }
        for log in logs
    ]
