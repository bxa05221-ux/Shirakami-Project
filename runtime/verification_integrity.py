"""Integrity boundary for verification results.

A verification result is evidence about checks performed; it is not a
human approval and cannot manufacture authority.
"""
from __future__ import annotations

from typing import Any, Mapping


class VerificationIntegrityError(ValueError):
    """Raised when a verification result is incomplete or claims authority."""


REQUIRED_FIELDS = (
    "verification_id",
    "target_id",
    "result",
    "verifier",
)


def validate_verification_result(result: Mapping[str, Any]) -> None:
    """Fail closed unless a verification result is structurally valid."""
    for field in REQUIRED_FIELDS:
        value = result.get(field)
        if value is None or value == "":
            raise VerificationIntegrityError(f"verification missing field: {field}")

    if result.get("result") not in {"pass", "fail"}:
        raise VerificationIntegrityError("verification result must be pass or fail")

    if result.get("human_approval") is True:
        raise VerificationIntegrityError(
            "verification cannot create human approval"
        )

    if result.get("runtime_authority") is True:
        raise VerificationIntegrityError(
            "verification cannot create runtime authority"
        )


def can_verification_authorize(result: Mapping[str, Any]) -> bool:
    """Always false: verification is never an authority source."""
    validate_verification_result(result)
    return False
