"""Provider-neutral comparative Evidence view."""
from dataclasses import dataclass
from typing import Sequence
from joumon_evidence_adapter import UnifiedEvidence

@dataclass(frozen=True)
class ComparativeEvidence:
    context_id: str
    protocol_id: str
    observations: tuple[UnifiedEvidence, ...]
    comparison_authority: str = "non-authoritative"
    final_decision_authority: str = "human"

def compare(records: Sequence[UnifiedEvidence]) -> ComparativeEvidence:
    if not records:
        raise ValueError("at least one Evidence record is required")
    contexts={r.context_id for r in records}
    protocols={r.protocol_id for r in records}
    if len(contexts) != 1 or len(protocols) != 1:
        raise ValueError("records must share Context and Protocol identity")
    return ComparativeEvidence(next(iter(contexts)), next(iter(protocols)), tuple(records))
