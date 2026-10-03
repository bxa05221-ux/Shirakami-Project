"""End-to-end JOUMON demo: Runtime A -> Matome -> import -> Runtime B -> Evidence."""
from joumon_provider_contract_poc import Context, ProtocolSpec, RuntimeAdapter, RuntimeRequest, RuntimeResult
from joumon_evidence_adapter import to_evidence
from joumon_lineage import build_lineage
from joumon_semantic_handoff import create_handoff
from joumon_matome_yaml import handoff_to_matome_yaml, validate_matome_document
from joumon_handoff_import import matome_to_handoff


class ConsumerRuntime:
    def __init__(self, runtime_id: str, provider: str):
        self.runtime_id = runtime_id
        self.provider = provider

    def execute(self, request: RuntimeRequest) -> RuntimeResult:
        return RuntimeResult(
            runtime_id=self.runtime_id,
            context_id=request.context_id,
            output=f"{self.runtime_id} produced a candidate for task: {request.task}; human review remains required.",
            metadata={"provider": self.provider, "mode": "mock", "runtime_type": "model"},
        )

    def execute_handoff(self, handoff):
        prior = [e.evidence_id for e in handoff.evidence]
        return RuntimeResult(
            runtime_id=self.runtime_id,
            context_id=handoff.context_id,
            output=f"{self.runtime_id} consumed handoff with prior evidence: {','.join(prior)}; human review remains required.",
            metadata={"provider": self.provider, "mode": "mock", "runtime_type": "model"},
        )


def execute_roundtrip():
    context = Context("joumon-e2e-001", "Continue from prior multi-runtime observation.", ("Do not transfer decision authority.",))
    protocol = ProtocolSpec("joumon-e2e-protocol-001", context.context_id)

    source = RuntimeAdapter(ConsumerRuntime("runtime-a", "provider-a"))
    source_result = source.execute(context, protocol)
    source_evidence = to_evidence(context.context_id, protocol.protocol_id, source_result.runtime_id, source_result.output, source_result.metadata)
    source_lineage = build_lineage(context_id=context.context_id, protocol_id=protocol.protocol_id, runtime_id=source_evidence.runtime_id, evidence_id=source_evidence.evidence_id)
    handoff = create_handoff(handoff_id="e2e-handoff-001", context_id=context.context_id, protocol_id=protocol.protocol_id, evidence=(source_evidence,), lineage=(source_lineage,))

    artifact = handoff_to_matome_yaml(handoff)
    restored = matome_to_handoff(validate_matome_document(artifact))

    consumer = ConsumerRuntime("runtime-b", "provider-b")
    next_result = consumer.execute_handoff(restored)
    next_evidence = to_evidence(restored.context_id, restored.protocol_id, next_result.runtime_id, next_result.output, next_result.metadata)
    next_lineage = build_lineage(context_id=restored.context_id, protocol_id=restored.protocol_id, runtime_id=next_evidence.runtime_id, evidence_id=next_evidence.evidence_id)
    return restored, next_evidence, next_lineage
