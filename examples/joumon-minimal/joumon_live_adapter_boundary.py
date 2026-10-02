"""Live runtime adapter boundary without embedding a provider SDK.

The adapter receives an injected callable. Provider credentials, SDKs and
network behavior stay outside the protocol layer.
"""
from dataclasses import dataclass
from typing import Callable, Mapping
from joumon_provider_contract_poc import Context, ProtocolSpec, RuntimeResult


@dataclass(frozen=True)
class LiveAdapterRequest:
    context_id: str
    protocol_id: str
    prompt: str


class LiveRuntimeAdapter:
    def __init__(self, runtime_id: str, provider: str, invoke: Callable[[LiveAdapterRequest], str]):
        self.runtime_id = runtime_id
        self.provider = provider
        self.invoke = invoke

    def execute(self, context: Context, protocol: ProtocolSpec) -> RuntimeResult:
        request = LiveAdapterRequest(context.context_id, protocol.protocol_id, context.description)
        output = self.invoke(request)
        return RuntimeResult(
            runtime_id=self.runtime_id,
            context_id=context.context_id,
            output=output,
            metadata={"provider": self.provider, "mode": "live", "runtime_type": "model"},
        )


def adapter_contract_snapshot(context: Context, protocol: ProtocolSpec, adapter: LiveRuntimeAdapter) -> Mapping[str, str]:
    return {
        "context_id": context.context_id,
        "protocol_id": protocol.protocol_id,
        "runtime_id": adapter.runtime_id,
        "provider": adapter.provider,
        "mode": "live",
    }
