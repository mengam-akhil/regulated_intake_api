from enum import Enum

class RegErrorCode(str, Enum):
    INVALID_DOCUMENT_ID = "ERR-REG-001"
    UNSUPPORTED_DOMAIN = "ERR-REG-002"
