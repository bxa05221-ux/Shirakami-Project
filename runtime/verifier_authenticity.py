"""Verifier authenticity boundary.

Testable HMAC-based authenticity envelope. Production trust-store/key management
is intentionally outside this module.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Mapping


class VerifierAuthenticityError(ValueError):
    pass


def canonical_verification_payload(record: Mapping[str, Any]) -> bytes:
    payload = {
        "verification_id": record.get("verification_id"),
        "target_id": record.get("target_id"),
        "result": record.get("result"),
        "verifier": record.get("verifier"),
        "verifier_instance": record.get("verifier_instance"),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def sign_verification(record: Mapping[str, Any], secret: bytes) -> str:
    return hmac.new(
        secret, canonical_verification_payload(record), hashlib.sha256
    ).hexdigest()


def validate_verifier_authenticity(
    record: Mapping[str, Any],
    signature: str,
    secret: bytes,
) -> None:
    expected = sign_verification(record, secret)
    if not hmac.compare_digest(expected, signature):
        raise VerifierAuthenticityError("verifier signature mismatch")

    if record.get("human_approval") is True:
        raise VerifierAuthenticityError(
            "authenticated verifier output cannot create human approval"
        )

    if record.get("runtime_authority") is True:
        raise VerifierAuthenticityError(
            "authenticated verifier output cannot create runtime authority"
        )
