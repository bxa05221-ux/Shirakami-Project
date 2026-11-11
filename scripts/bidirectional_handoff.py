"""Deterministic, non-authoritative Project-to-Project handoff round trip."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


REQUIRED_KEYS = ("context", "evidence", "provenance", "unresolved", "human_gate")


def receive_from_project_a(package: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and reconstruct only the non-authoritative handoff state."""
    missing = [key for key in REQUIRED_KEYS if key not in package]
    if missing:
        raise ValueError("missing handoff fields: " + ", ".join(missing))
    if package["human_gate"].get("required") is not True:
        raise ValueError("human_gate.required must remain true")
    if package.get("authority_transfer") is not False:
        raise ValueError("authority_transfer must remain false")
    return deepcopy(dict(package))


def respond_from_project_b(received: Mapping[str, Any], response_context: Mapping[str, Any]) -> dict[str, Any]:
    """Return Project B's observation without changing lineage or authority."""
    response = receive_from_project_a(received)
    response["direction"] = "project-b-to-project-a"
    response["context"] = {**response["context"], **dict(response_context)}
    response["authority_transfer"] = False
    response["authority_transferred"] = False
    response["human_gate"] = {**response["human_gate"], "required": True}
    return response


def validate_returned_to_project_a(package: Mapping[str, Any]) -> None:
    """Validate the returned state before Project A may use it as context."""
    receive_from_project_a(package)
    if package.get("direction") != "project-b-to-project-a":
        raise ValueError("returned handoff direction is invalid")
    if package.get("authority_transferred") is not False:
        raise ValueError("returned handoff must not transfer authority")
