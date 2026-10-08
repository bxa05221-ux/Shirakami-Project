"""Verifier provenance boundary.

A verifier identifier is evidence about which verifier produced a result;
it is not, by itself, proof of identity or authority.
"""
from __future__ import annotations

from typing import Any, Mapping


class VerifierProvenanceError(ValueError):
    pass


REQUIRED = ("verification_id", "target_id", "verifier", "verifier_instance")


def validate_verifier_provenance(record: Mapping[str, Any]) -> None:
    for field in REQUIRED:
        if record.get(field) in (None, ""):
            raise VerifierProvenanceError(f"missing verifier provenance: {field}")

    if record.get("verifier_authority") is True:
        raise VerifierProvenanceError(
            "verifier provenance cannot create authority"
        )

    if record.get("human_approval") is True:
        raise VerifierProvenanceError(
            "verifier provenance cannot create human approval"
        )

    if record.get("runtime_authority") is True:
        raise VerifierProvenanceError(
            "verifier provenance cannot create runtime authority"
        )
