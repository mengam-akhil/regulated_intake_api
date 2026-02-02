from sqlalchemy.orm import Session

def write_audit_log(
    db: Session,
    document_id,
    action,
    status,
    actor,
    request_id,
    error_code=None,
):
    # ✅ LAZY IMPORT (THIS IS THE KEY)
    from db.models.audit_log import AuditLog

    log = AuditLog(
        document_id=document_id,
        action=action,
        status=status,
        actor=actor,
        request_id=request_id,
        error_code=error_code,
    )

    db.add(log)
    db.commit()
