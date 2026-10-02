"""Minimal loader that turns a Matome YAML-shaped document into Protocol inputs.

v0.1 intentionally supports the repository's constrained key/value contract
without adding a YAML dependency. The loader is designed to be replaced by a
canonical YAML parser once the schema is frozen.
"""
from typing import Any, Mapping
from joumon_provider_contract_poc import Context, ProtocolSpec


def load_matome_mapping(document: Mapping[str, Any]) -> tuple[Context, ProtocolSpec]:
    matome = document.get("matome", {})
    if matome.get("codename") != "JOUMON":
        raise ValueError("unsupported Matome codename")
    purpose = document.get("purpose", {})
    primary = purpose.get("primary", [])
    statement = matome.get("statement", "")
    if not statement or not primary:
        raise ValueError("Matome requires a statement and primary purpose")
    context_id = f"matome:{matome.get('version', 'unknown')}:{matome.get('codename')}"
    protocol_id = f"protocol:{context_id}"
    constraints = tuple(document.get("human_gate", {}).get("input", []))
    context = Context(context_id, statement, constraints)
    protocol = ProtocolSpec(protocol_id, context.context_id)
    return context, protocol
