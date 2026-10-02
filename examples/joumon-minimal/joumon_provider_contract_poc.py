"""Provider-neutral JOUMON runtime contract PoC."""
from dataclasses import dataclass
from typing import Protocol, Mapping

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
class RuntimeRequest:
    context_id: str
    protocol_id: str
    task: str
    constraints: tuple[str, ...]

@dataclass(frozen=True)
class RuntimeResult:
    runtime_id: str
    context_id: str
    output: str
    metadata: Mapping[str, str]

class Runtime(Protocol):
    runtime_id: str
    def execute(self, request: RuntimeRequest) -> RuntimeResult: ...

class RuntimeAdapter:
    """Provider-neutral exchange point."""

    def __init__(self, runtime: Runtime) -> None:
        self.runtime = runtime

    def execute(self, context: Context, protocol: ProtocolSpec) -> RuntimeResult:
        if protocol.input_context_id != context.context_id:
            raise ValueError("protocol/context mismatch")
        request = RuntimeRequest(
            context_id=context.context_id,
            protocol_id=protocol.protocol_id,
            task=context.task,
            constraints=context.constraints,
        )
        return self.runtime.execute(request)

class FakeOpenAI(Runtime):
    runtime_id = "openai-compatible"

    def execute(self, request: RuntimeRequest) -> RuntimeResult:
        return RuntimeResult(
            runtime_id=self.runtime_id,
            context_id=request.context_id,
            output="OpenAI-compatible candidate; requires human review.",
            metadata={"provider": "openai", "mode": "mock"},
        )

class FakeGemini(Runtime):
    runtime_id = "gemini-compatible"

    def execute(self, request: RuntimeRequest) -> RuntimeResult:
        return RuntimeResult(
            runtime_id=self.runtime_id,
            context_id=request.context_id,
            output="Gemini-compatible candidate; requires human review.",
            metadata={"provider": "gemini", "mode": "mock"},
        )

def run() -> tuple[Context, ProtocolSpec, tuple[RuntimeResult, ...]]:
    context = Context(
        context_id="joumon-provider-contract-001",
        task="Produce one candidate action.",
        constraints=("Candidate output requires human review.",),
    )
    protocol = ProtocolSpec(
        protocol_id="joumon-provider-contract-001",
        input_context_id=context.context_id,
    )
    adapters = (
        RuntimeAdapter(FakeOpenAI()),
        RuntimeAdapter(FakeGemini()),
    )
    return context, protocol, tuple(
        adapter.execute(context, protocol) for adapter in adapters
    )
