import json
from datetime import datetime
from uuid import uuid4
from pathlib import Path

EVENT_LOG_PATH = Path("audit_events.log")

def write_ingestion_event(
    source: str,
    document_id: int,
    payload_hash: str,
    actor: str = "system"
):
    event = {
        "event_id": str(uuid4()),
        "event_type": "INGEST_RECEIVED",
        "source": source,
        "document_id": document_id,
        "payload_hash": payload_hash,
        "actor": actor,
        "timestamp_utc": datetime.utcnow().isoformat()
    }

    with EVENT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return event
