"""Opt-in live OpenAI entrypoint for the JOUMON PoC.

This module is intentionally inert unless executed by a user in an
authenticated environment with OPENAI_API_KEY set. No key or response is
stored in the repository.
"""
import os
from joumon_openai_adapter import build_openai_compatible_adapter
from joumon_live_adapter_boundary import LiveAdapterRequest


def require_live_config() -> tuple[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    model = os.environ.get("OPENAI_MODEL")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set; live execution is opt-in")
    if not model:
        raise RuntimeError("OPENAI_MODEL is not set; choose the model explicitly")
    return api_key, model


def build_live_adapter():
    api_key, model = require_live_config()

    def invoke(request: LiveAdapterRequest, selected_model: str) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=selected_model,
            input=request.prompt,
        )
        return response.output_text

    return build_openai_compatible_adapter(model=model, invoke=invoke)


if __name__ == "__main__":
    adapter = build_live_adapter()
    print({"runtime_id": adapter.runtime_id, "provider": adapter.provider, "mode": "live"})
    print("Adapter ready. Execute it from an authenticated JOUMON pipeline; no output is persisted here.")
