"""Sakana Fugu runtime adapter boundary for JOUMON.

This module treats Sakana Fugu as one replaceable runtime. Provider
credentials, SDKs and network behavior stay outside the JOUMON protocol core.
"""

from typing import Callable

from joumon_live_adapter_boundary import LiveAdapterRequest, LiveRuntimeAdapter


def build_sakana_fugu_adapter(
    *,
    runtime_id: str = "runtime-sakana-fugu",
    model: str = "fugu",
    invoke: Callable[[LiveAdapterRequest, str], str],
) -> LiveRuntimeAdapter:
    """Create a JOUMON adapter around an injected Sakana Fugu invocation.

    The injected callable may use Sakana's OpenAI-compatible API, another
    compatible client, or a deterministic test double. JOUMON does not
    depend on the Sakana SDK or own authentication.
    """

    def call(request: LiveAdapterRequest) -> str:
        return invoke(request, model)

    return LiveRuntimeAdapter(runtime_id, "sakana-ai", call)
