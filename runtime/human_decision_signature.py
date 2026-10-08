"""Test-only cryptographic boundary for Human Gate decisions.

This module deliberately uses HMAC only as a deterministic contract test.
It is not a production identity/signature system.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any, Mapping


class HumanDecisionSignatureError(ValueError):
    pass


BOUND_FIELDS = (
    "decision_id",
    "approval_id",
    "context_version",
    "evidence_hash",
    "protocol_hash",
    "proposal_id",
    "principal_id",
    "authentication_id",
    "decision",
)


def _canonical_payload(decision: Mapping[str, Any]) -> bytes:
    return json.dumps(
        {field: decision.get(field) for field in BOUND_FIELDS},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sign_human_decision(decision: Mapping[str, Any], secret: bytes) -> str:
    return hmac.new(secret, _canonical_payload(decision), hashlib.sha256).hexdigest()


def validate_human_decision_signature(
    decision: Mapping[str, Any], signature: str, secret: bytes
) -> None:
    if not signature:
        raise HumanDecisionSignatureError("missing decision signature")
    expected = sign_human_decision(decision, secret)
    if not hmac.compare_digest(signature, expected):
        raise HumanDecisionSignatureError("invalid decision signature")
    if decision.get("actor_type") != "human":
        raise HumanDecisionSignatureError("decision actor is not human")
    if decision.get("human_approval") is not True:
        raise HumanDecisionSignatureError("missing human approval")
    if decision.get("runtime_authority") is True:
        raise HumanDecisionSignatureError("runtime authority forbidden")
