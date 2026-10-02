"""JOUMON Runtime Adapter boundary PoC."""
from dataclasses import dataclass
from typing import Protocol, Tuple

@dataclass(frozen=True)
class Context:
    context_id: str
    task: str
    constraints: tuple[str, ...]
    final_decision_authority: str = "human"

@dataclass(frozen=True)
class ProtocolSpec:
    protocol_id: str
    input_context_id: str
    human_gate_required: bool = True

@dataclass(frozen=True)
class RuntimeResult:
    runtime_id: str
    context_id: str
    output: str

@dataclass(frozen=True)
class Evidence:
    context_id: str
    runtime_id: str
    observed_output: str
    authority: str = "non-authoritative"

@dataclass(frozen=True)
class HumanGate:
    decision_authority: str = "human"
    decision_status: str = "pending"

class Runtime(Protocol):
    runtime_id: str
    def execute(self, context: Context, protocol: ProtocolSpec) -> RuntimeResult: ...

class MockRuntime:
    def __init__(self, runtime_id: str, behavior: str) -> None:
        self.runtime_id = runtime_id
        self.behavior = behavior

    def execute(self, context: Context, protocol: ProtocolSpec) -> RuntimeResult:
        if protocol.input_context_id != context.context_id:
            raise ValueError("protocol/context mismatch")
        return RuntimeResult(
            runtime_id=self.runtime_id,
            context_id=context.context_id,
            output=f"{self.behavior}: candidate requires human review.",
        )

class RuntimeAdapter:
    def __init__(self, runtime: Runtime) -> None:
        self.runtime = runtime

    def execute(self, context: Context, protocol: ProtocolSpec) -> tuple[RuntimeResult, Evidence]:
        result = self.runtime.execute(context, protocol)
        evidence = Evidence(
            context_id=result.context_id,
            runtime_id=result.runtime_id,
            observed_output=result.output,
        )
        return result, evidence

def run() -> tuple[Context, ProtocolSpec, tuple[RuntimeResult, ...], tuple[Evidence, ...], HumanGate]:
    context = Context(
        context_id="joumon-adapter-context-001",
        task="Produce one candidate action.",
        constraints=("Candidate output requires human review.",),
    )
    protocol = ProtocolSpec(
        protocol_id="joumon-adapter-protocol-001",
        input_context_id=context.context_id,
    )
    adapters = (
        RuntimeAdapter(MockRuntime("runtime-a", "A")),
        RuntimeAdapter(MockRuntime("runtime-b", "B")),
    )
    pairs = tuple(adapter.execute(context, protocol) for adapter in adapters)
    results = tuple(pair[0] for pair in pairs)
    evidence = tuple(pair[1] for pair in pairs)
    return context, protocol, results, evidence, HumanGate()
