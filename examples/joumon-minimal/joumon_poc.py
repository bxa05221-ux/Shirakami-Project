"""Minimal executable JOUMON PoC."""
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class Context:
    context_id: str
    task: str
    constraints: tuple[str, ...]
    final_decision_authority: str = "human"

@dataclass(frozen=True)
class Protocol:
    protocol_id: str
    input_context_id: str
    runtime_role: str = "replaceable"
    human_gate_required: bool = True

@dataclass(frozen=True)
class RuntimeResult:
    runtime_id: str
    context_id: str
    output: str
    observed: bool = True

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    context_id: str
    runtime_id: str
    observed_output: str
    authority: str = "non-authoritative"

@dataclass(frozen=True)
class HumanGate:
    decision_status: str = "pending"
    decision_authority: str = "human"

class MockRuntime:
    def __init__(self, runtime_id: str) -> None:
        self.runtime_id = runtime_id

    def execute(self, context: Context, protocol: Protocol) -> RuntimeResult:
        if protocol.input_context_id != context.context_id:
            raise ValueError("protocol/context mismatch")
        return RuntimeResult(
            runtime_id=self.runtime_id,
            context_id=context.context_id,
            output=f"Candidate action from {self.runtime_id}; requires human review.",
        )

def run(runtime_ids=("mock-runtime-a", "mock-runtime-b")) -> Dict[str, object]:
    context = Context(
        context_id="joumon-poc-context-001",
        task="Produce one short candidate action for the supplied Context.",
        constraints=("The candidate requires human review.",),
    )
    protocol = Protocol(
        protocol_id="joumon-poc-protocol-001",
        input_context_id=context.context_id,
    )
    results, evidence = [], []
    for runtime_id in runtime_ids:
        result = MockRuntime(runtime_id).execute(context, protocol)
        results.append(result)
        evidence.append(Evidence(
            evidence_id=f"joumon-poc-evidence-{runtime_id.rsplit('-', 1)[-1]}",
            context_id=result.context_id,
            runtime_id=result.runtime_id,
            observed_output=result.output,
        ))
    return {
        "context": context, "protocol": protocol,
        "results": tuple(results), "evidence": tuple(evidence),
        "human_gate": HumanGate(),
    }
