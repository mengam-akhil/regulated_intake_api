from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from datetime import datetime


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer)
    action = Column(String)
    status = Column(String)
    actor = Column(String)
    request_id = Column(String)
    error_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)