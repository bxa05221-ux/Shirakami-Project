"""Unified Evidence adapter for the JOUMON provider-neutral PoC."""
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class UnifiedEvidence:
    evidence_id: str
    context_id: str
    protocol_id: str
    runtime_id: str
    provider: str
    runtime_type: str
    mode: str
    observed_output: str
    evidence_authority: str = "non-authoritative"
    final_decision_authority: str = "human"

def to_evidence(context_id: str, protocol_id: str, runtime_id: str, output: str, metadata: Mapping[str, str]) -> UnifiedEvidence:
    return UnifiedEvidence(
        evidence_id=f"evidence-{runtime_id}-{context_id}", context_id=context_id, protocol_id=protocol_id,
        runtime_id=runtime_id, provider=metadata.get("provider", "unknown"),
        runtime_type=metadata.get("runtime_type", "model"), mode=metadata.get("mode", "unknown"),
        observed_output=output,
    )
