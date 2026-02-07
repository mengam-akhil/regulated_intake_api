import hashlib
from uuid import uuid4

# In real systems this would be a secure vault or KMS-backed store
PII_VAULT = {}

def tokenize_pii(value: str) -> str:
    """
    Converts raw PII into a non-reversible token
    """
    token = f"pii_{uuid4().hex}"
    PII_VAULT[token] = value
    return token


def anonymize_pii(token: str):
    """
    Irreversibly removes PII for GDPR Art. 17 (right to be forgotten)
    """
    if token in PII_VAULT:
        del PII_VAULT[token]
