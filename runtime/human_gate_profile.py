"""Configurable Human Gate review profiles."""
from __future__ import annotations

from typing import Any, Mapping

STRATEGIC_PROFILE = {
    "id": "strategic",
    "checks": {
        "setting": {"enabled": True, "require_human_confirmation": True},
        "positioning": {"enabled": True, "compare_self_and_counterparty": True},
        "asymmetry": {"enabled": True, "dimensions": [
            "knowledge", "experience", "resources", "authority", "information", "time"
        ]},
        "assumptions": {"enabled": True, "expose_unverified_assumptions": True},
        "evidence": {"enabled": True, "separate_fact_from_interpretation": True},
        "alternatives": {"enabled": True, "preserve_all_branches": True},
        "strategy": {"enabled": True, "ai_may_generate": True, "ai_may_select": False},
        "reset": {"enabled": True, "allow_return_to_setting": True},
    },
    "authority": {
        "ai": {
            "may_observe": True, "may_analyze": True, "may_generate_options": True,
            "may_rank_options": False, "may_select_strategy": False,
            "may_commit_decision": False,
        },
        "human_gate": {
            "may_confirm_setting": True, "may_modify_setting": True,
            "may_select_strategy": True, "may_override_ai": True,
        },
    },
    "invariants": {
        "selection_authority": "human_gate",
        "execution_authorized": False, "publish_authorized": False,
        "merge_authorized": False, "human_gate_required": True,
    },
}


def get_profile(profile_id: str = "strategic") -> dict[str, Any]:
    if profile_id != "strategic":
        raise ValueError(f"unknown human gate profile: {profile_id}")
    return _copy(STRATEGIC_PROFILE)


def validate_profile(profile: Mapping[str, Any]) -> None:
    if profile.get("id") != "strategic":
        raise ValueError("profile.id must be strategic")
    authority = profile.get("authority")
    if not isinstance(authority, Mapping):
        raise ValueError("authority is required")
    ai = authority.get("ai", {})
    if ai.get("may_select_strategy") is not False:
        raise ValueError("AI must not select strategy")
    if ai.get("may_commit_decision") is not False:
        raise ValueError("AI must not commit decision")
    if ai.get("may_rank_options") is not False:
        raise ValueError("AI must not rank options")
    human = authority.get("human_gate", {})
    if human.get("may_select_strategy") is not True:
        raise ValueError("Human Gate must retain strategy selection")
    invariants = profile.get("invariants")
    if not isinstance(invariants, Mapping):
        raise ValueError("invariants are required")
    expected = {
        "selection_authority": "human_gate",
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }
    for key, value in expected.items():
        if invariants.get(key) != value:
            raise ValueError(f"invariant {key} must be {value!r}")
    strategy = profile.get("checks", {}).get("strategy", {})
    if strategy.get("ai_may_generate") is not True:
        raise ValueError("AI strategy generation must remain available")
    if strategy.get("ai_may_select") is not False:
        raise ValueError("AI strategy selection must remain disabled")


def review_requirements(profile_id: str = "strategic") -> list[str]:
    return [name for name, config in get_profile(profile_id)["checks"].items()
            if config.get("enabled")]


def _copy(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _copy(item) for key, item in value.items()}
    if isinstance(value, list):
        return list(value)
    return value
