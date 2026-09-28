"""Validate an EvidenceCandidate before it can become an EvidenceRecord.

Validation changes structural state only. It does not create an evidence_id,
grant authority, or perform execution.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from runtime.observation_evidence_candidate import EvidenceCandidate


@dataclass(frozen=True)
class ValidatedEvidenceCandidate:
    candidate_id: str
    observation_id: str
    witness_id: str
    trace_id: str
    approval_id: str
    protocol_id: str
    request_id: str
    source: str
    execution_status: str
    scope: Tuple[str, ...]
    validation_status: str = "validated"
    evidence_id: str | None = None
    decision_authority: bool = False


_REQUIRED = (
    "candidate_id",
    "observation_id",
    "witness_id",
    "trace_id",
    "approval_id",
    "protocol_id",
    "request_id",
    "source",
    "execution_status",
)


def validate_evidence_candidate(
    candidate: EvidenceCandidate,
) -> ValidatedEvidenceCandidate:
    for field in _REQUIRED:
        value = getattr(candidate, field)
        if not value:
            raise ValueError(f"{field} is required")

    if candidate.validation_status != "pending":
        raise ValueError("candidate must enter validation from pending state")
    if candidate.evidence_id is not None:
        raise ValueError("evidence_id must remain unset during validation")
    if candidate.decision_authority is not False:
        raise ValueError("decision_authority must remain false")
    if not candidate.scope:
        raise ValueError("scope is required")

    return ValidatedEvidenceCandidate(
        candidate_id=candidate.candidate_id,
        observation_id=candidate.observation_id,
        witness_id=candidate.witness_id,
        trace_id=candidate.trace_id,
        approval_id=candidate.approval_id,
        protocol_id=candidate.protocol_id,
        request_id=candidate.request_id,
        source=candidate.source,
        execution_status=candidate.execution_status,
        scope=candidate.scope,
    )
