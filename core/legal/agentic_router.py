from enum import Enum
from typing import Dict


class Decision(str, Enum):
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


def cross_verify_lawfulness(context: Dict) -> Dict:
    """
    Rule-assisted legal reasoning.
    Deterministic, auditable, explainable.
    """

    gdpr_applies = context.get("gdpr_applies", False)
    fadp_applies = context.get("fadp_applies", False)

    has_consent = context.get("has_consent", False)
    pii_tokenized = context.get("pii_tokenized", False)
    right_to_delete_supported = context.get("rtbf_supported", False)

    reasons = []

    # GDPR checks
    if gdpr_applies:
        if not pii_tokenized:
            reasons.append("GDPR Art.5 violated: PII not minimized")
        if not right_to_delete_supported:
            reasons.append("GDPR Art.17 violated: RTBF unsupported")

    # Swiss FADP checks
    if fadp_applies:
        if not has_consent:
            reasons.append("Swiss FADP: missing lawful basis / consent")

    # Decision routing
    if reasons:
        decision = Decision.REVIEW if pii_tokenized else Decision.BLOCK
    else:
        decision = Decision.ALLOW

    return {
        "decision": decision,
        "reasons": reasons,
        "laws_evaluated": {
            "gdpr": gdpr_applies,
            "fadp": fadp_applies,
        },
    }
