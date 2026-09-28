"""Build an EvidenceRecord from a structurally validated candidate."""
from __future__ import annotations

import hashlib
import json

from runtime.observation_evidence_validation import ValidatedEvidenceCandidate


def build_evidence_record_from_validated(
    candidate: ValidatedEvidenceCandidate,
    *,
    observed: object,
) -> dict:
    if candidate.validation_status != "validated":
        raise ValueError("candidate must be structurally validated")
    if candidate.evidence_id is not None:
        raise ValueError("validated candidate must not already contain evidence_id")
    if candidate.decision_authority is not False:
        raise ValueError("decision_authority must remain false")

    payload = {
        "candidate_id": candidate.candidate_id,
        "observation_id": candidate.observation_id,
        "witness_id": candidate.witness_id,
        "trace_id": candidate.trace_id,
        "approval_id": candidate.approval_id,
        "protocol_id": candidate.protocol_id,
        "request_id": candidate.request_id,
        "source": candidate.source,
        "execution_status": candidate.execution_status,
        "scope": list(candidate.scope),
        "observed": observed,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    evidence_id = f"EVIDENCE-{hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]}"

    return {
        "version": "0.2",
        "evidence_id": evidence_id,
        "kind": "observed_candidate",
        "source": {
            "candidate_id": candidate.candidate_id,
            "observation_id": candidate.observation_id,
            "witness_id": candidate.witness_id,
            "trace_id": candidate.trace_id,
            "approval_id": candidate.approval_id,
            "protocol_id": candidate.protocol_id,
            "request_id": candidate.request_id,
            "source": candidate.source,
        },
        "observed": observed,
        "scope": list(candidate.scope),
        "authority": {
            "decision_authority": False,
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }
