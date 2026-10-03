"""Explicit final decision boundary for JOUMON."""
from dataclasses import dataclass
from typing import Tuple
from joumon_evidence_adapter import UnifiedEvidence

@dataclass(frozen=True)
class HumanGateInput:
    context_id: str
    protocol_id: str
    evidence: Tuple[UnifiedEvidence, ...]
    verification_ids: Tuple[str, ...]
    decision_authority: str = "human"

@dataclass(frozen=True)
class HumanGateRecord:
    gate_id: str
    context_id: str
    evidence_ids: Tuple[str, ...]
    verification_ids: Tuple[str, ...]
    decision: str
    authority: str = "human"


def prepare_human_gate(*, gate_id: str, context_id: str, protocol_id: str,
                       evidence: Tuple[UnifiedEvidence, ...],
                       verification_ids: Tuple[str, ...]) -> HumanGateInput:
    if any(e.context_id != context_id or e.protocol_id != protocol_id for e in evidence):
        raise ValueError("Human Gate input contains mismatched Evidence")
    return HumanGateInput(context_id, protocol_id, evidence, verification_ids)


def record_human_decision(gate_input: HumanGateInput, *, decision: str) -> HumanGateRecord:
    if gate_input.decision_authority != "human":
        raise ValueError("Human Gate authority must remain human")
    if not decision.strip():
        raise ValueError("decision must be explicitly supplied")
    return HumanGateRecord(
        gate_id=f"gate-{gate_input.context_id}",
        context_id=gate_input.context_id,
        evidence_ids=tuple(e.evidence_id for e in gate_input.evidence),
        verification_ids=gate_input.verification_ids,
        decision=decision,
    )
