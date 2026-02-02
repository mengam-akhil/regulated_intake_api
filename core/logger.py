import logging
import json
import uuid
from datetime import datetime

def get_request_id():
    return str(uuid.uuid4())

class RegTechLogger:
    def __init__(self):
        self.logger = logging.getLogger("regtech")
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))

        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def log(self, *, level, code, message, request_id, document_id=None, extra=None):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "error_code": code,
            "message": message,
            "request_id": request_id,
            "document_id": document_id,
            "extra": extra
        }
        self.logger.info(json.dumps(log_entry))
