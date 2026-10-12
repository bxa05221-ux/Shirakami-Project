"""Tamper-evident binding for verification results."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


class VerificationForgeryError(ValueError):
    """Raised when a verification record is incomplete or tampered with."""


BOUND_FIELDS = ("verification_id", "target_id", "result", "verifier", "verifier_instance")


def verification_digest(result: Mapping[str, Any]) -> str:
    payload = {field: result.get(field) for field in BOUND_FIELDS}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def validate_verification_integrity(
    result: Mapping[str, Any],
    expected_digest: str,
) -> None:
    """Require exact identity/content binding and preserve non-authority."""
    for field in BOUND_FIELDS:
        if result.get(field) in (None, ""):
            raise VerificationForgeryError(f"verification missing field: {field}")

    actual = verification_digest(result)
    if actual != expected_digest:
        raise VerificationForgeryError("verification digest mismatch")

    if result.get("human_approval") is True:
        raise VerificationForgeryError(
            "verification cannot create human approval"
        )
    if result.get("runtime_authority") is True:
        raise VerificationForgeryError(
            "verification cannot create runtime authority"
        )
