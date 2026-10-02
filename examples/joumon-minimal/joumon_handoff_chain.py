"""Chained JOUMON execution: Runtime A -> Handoff -> Runtime B -> Evidence."""
from dataclasses import dataclass
from typing import Tuple
from joumon_evidence_adapter import UnifiedEvidence, to_evidence
from joumon_lineage import EvidenceLineage, build_lineage
from joumon_semantic_handoff import SemanticHandoff, create_handoff
from joumon_provider_contract_poc import Context, ProtocolSpec, Runtime, RuntimeAdapter, RuntimeRequest, RuntimeResult


class HandoffAwareRuntime:
    def __init__(self, runtime_id: str, provider: str, prefix: str):
        self.runtime_id = runtime_id
        self.provider = provider
        self.prefix = prefix

    def execute(self, request: RuntimeRequest) -> RuntimeResult:
        return RuntimeResult(
            runtime_id=self.runtime_id,
            context_id=request.context_id,
            output=f"{self.prefix}: received prior semantic handoff; candidate requires human review.",
            metadata={"provider": self.provider, "mode": "mock", "runtime_type": "model"},
        )


def run_chain() -> Tuple[Context, ProtocolSpec, SemanticHandoff, UnifiedEvidence, EvidenceLineage]:
    context = Context("joumon-chain-001", "Continue a candidate action from prior observation.", ("Human review required.",))
    protocol = ProtocolSpec("joumon-chain-protocol-001", context.context_id)

    first = RuntimeAdapter(HandoffAwareRuntime("runtime-a", "provider-a", "A"))
    first_result = first.execute(context, protocol)
    first_evidence = to_evidence(context.context_id, protocol.protocol_id, first_result.runtime_id, first_result.output, first_result.metadata)
    first_lineage = build_lineage(context_id=context.context_id, protocol_id=protocol.protocol_id, runtime_id=first_evidence.runtime_id, evidence_id=first_evidence.evidence_id)
    handoff = create_handoff(handoff_id="handoff-chain-001", context_id=context.context_id, protocol_id=protocol.protocol_id, evidence=(first_evidence,), lineage=(first_lineage,))

    second = RuntimeAdapter(HandoffAwareRuntime("runtime-b", "provider-b", "B"))
    second_result = second.execute(context, protocol)
    second_evidence = to_evidence(context.context_id, protocol.protocol_id, second_result.runtime_id, second_result.output, second_result.metadata)
    second_lineage = build_lineage(context_id=context.context_id, protocol_id=protocol.protocol_id, runtime_id=second_evidence.runtime_id, evidence_id=second_evidence.evidence_id)
    return context, protocol, handoff, second_evidence, second_lineage
