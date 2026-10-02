"""OpenAI-compatible adapter boundary for JOUMON.

No credentials are stored here. The caller injects the actual SDK/API
callable, keeping provider-specific authentication outside the protocol core.
"""
from typing import Callable
from joumon_live_adapter_boundary import LiveAdapterRequest, LiveRuntimeAdapter


def build_openai_compatible_adapter(
    *, runtime_id: str = "runtime-openai",
    model: str,
    invoke: Callable[[LiveAdapterRequest, str], str],
) -> LiveRuntimeAdapter:
    """Create an adapter around an injected OpenAI-compatible invocation.

    `invoke` is intentionally injected so this module remains usable with the
    OpenAI SDK, an OpenAI-compatible endpoint, or a test double without making
    the JOUMON protocol depend on any provider package.
    """
    def call(request: LiveAdapterRequest) -> str:
        return invoke(request, model)

    return LiveRuntimeAdapter(runtime_id, "openai-compatible", call)
