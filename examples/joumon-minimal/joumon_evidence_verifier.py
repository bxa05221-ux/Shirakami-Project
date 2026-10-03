"""Deterministic verification for JOUMON Evidence provenance boundaries."""
from dataclasses import dataclass
from joumon_evidence_adapter import UnifiedEvidence

@dataclass(frozen=True)
class VerificationResult:
    evidence_id: str
    verified: bool
    checks: tuple[str, ...]
    verification_authority: str = "non-authoritative"
    final_decision_authority: str = "human"

def verify(evidence: UnifiedEvidence, *, expected_context_id: str, expected_protocol_id: str) -> VerificationResult:
    checks=[]
    ok=True
    if evidence.context_id == expected_context_id: checks.append("context_identity")
    else: ok=False
    if evidence.protocol_id == expected_protocol_id: checks.append("protocol_identity")
    else: ok=False
    if evidence.evidence_authority == "non-authoritative": checks.append("evidence_authority")
    else: ok=False
    if evidence.final_decision_authority == "human": checks.append("human_final_authority")
    else: ok=False
    if evidence.mode in {"mock", "live"}: checks.append("execution_mode_declared")
    else: ok=False
    if evidence.runtime_id and evidence.provider: checks.append("runtime_provenance")
    else: ok=False
    return VerificationResult(evidence.evidence_id, ok, tuple(checks))
