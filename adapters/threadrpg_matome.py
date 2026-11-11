"""Boundaries for connecting ThreadRPG and the Matome YAML Library.

This module intentionally contains interfaces and validation only. It does not
perform repository writes or grant authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from runtime.reality_user_world_clutch import SemanticObject, SemanticType


@dataclass(frozen=True)
class MatomeReference:
    matome_id: str
    version: str
    content: str
    provenance: tuple[str, ...]
    retrieved_at: str


@dataclass(frozen=True)
class AuthorDialogueAnswer:
    answer: str
    references: tuple[MatomeReference, ...]
    status: str
    uncertainty: tuple[str, ...] = ()
    is_inference: bool = False


class MatomeQueryGateway(Protocol):
    def query_matome(self, query: str, *, permitted_ids: Sequence[str]) -> AuthorDialogueAnswer:
        ...


class ThreadRPGAdapter(Protocol):
    def to_semantic_objects(self, thread_state: object) -> Sequence[SemanticObject]:
        ...


def validate_threadrpg_objects(objects: Sequence[SemanticObject]) -> None:
    """Prevent ThreadRPG presentation state from masquerading as Reality evidence."""
    for obj in objects:
        if obj.source == "THREADRPG" and obj.semantic_type == SemanticType.EVIDENCE:
            raise ValueError(
                "ThreadRPG objects cannot be promoted to EVIDENCE at the adapter boundary"
            )


def validate_author_dialogue(answer: AuthorDialogueAnswer) -> None:
    """Require provenance and preserve reference/inference distinction."""
    if not answer.answer:
        raise ValueError("dialogue answer is required")
    for ref in answer.references:
        if not ref.matome_id or not ref.version or not ref.provenance:
            raise ValueError("Matome answers require source provenance")
    if answer.status not in {"ANSWERED", "UNKNOWN", "BLOCKED"}:
        raise ValueError("invalid dialogue status")
