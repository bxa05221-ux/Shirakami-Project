"""Reality–User World Clutch runtime primitives.

Provider-neutral, deterministic primitives for preserving the distinction between
Reality-side evidence and User World semantics. This module does not make life
decisions and does not infer a user's semantic type from prose.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable
from uuid import uuid4


class SemanticType(str, Enum):
    EVIDENCE = "EVIDENCE"
    INTERPRETATION = "INTERPRETATION"
    MEANING = "MEANING"
    PRESENCE = "PRESENCE"
    DREAM = "DREAM"
    VALUE = "VALUE"
    UNKNOWN = "UNKNOWN"


class MemoryStatus(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    SUPERSEDED = "SUPERSEDED"
    UNKNOWN = "UNKNOWN"


class ProcessingStatus(str, Enum):
    RECEIVED = "RECEIVED"
    CLASSIFIED = "CLASSIFIED"
    STORED = "STORED"
    CONNECTED = "CONNECTED"
    FRAME_REVIEW = "FRAME_REVIEW"
    HUMAN_GATE = "HUMAN_GATE"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class SemanticObject:
    object_id: str
    semantic_type: SemanticType
    content: str
    source: str
    timestamp: datetime
    provenance: tuple[str, ...] = ()
    confidence: float | None = None
    status: MemoryStatus = MemoryStatus.CURRENT

    def __post_init__(self) -> None:
        if not self.object_id or not self.content or not self.source:
            raise ValueError("object_id, content, and source are required")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")

    @classmethod
    def create(
        cls,
        semantic_type: SemanticType,
        content: str,
        *,
        source: str = "USER",
        provenance: Iterable[str] = (),
        confidence: float | None = None,
        timestamp: datetime | None = None,
    ) -> "SemanticObject":
        return cls(
            object_id=f"SEM-{uuid4().hex[:12]}",
            semantic_type=semantic_type,
            content=content,
            source=source,
            timestamp=timestamp or datetime.now(timezone.utc),
            provenance=tuple(provenance),
            confidence=confidence,
        )


@dataclass(frozen=True)
class MemoryTransition:
    previous: SemanticObject | None
    current: SemanticObject
    changed: bool


class TemporalMemory:
    """Time-aware User World memory reference implementation."""

    def __init__(self) -> None:
        self._objects: dict[str, list[SemanticObject]] = {}

    def store(self, obj: SemanticObject) -> MemoryTransition:
        history = self._objects.setdefault(obj.semantic_type.value, [])
        previous = next(
            (item for item in reversed(history) if item.status == MemoryStatus.CURRENT),
            None,
        )

        if previous is not None and previous.content != obj.content:
            history[:] = [
                SemanticObject(
                    object_id=item.object_id,
                    semantic_type=item.semantic_type,
                    content=item.content,
                    source=item.source,
                    timestamp=item.timestamp,
                    provenance=item.provenance,
                    confidence=item.confidence,
                    status=(
                        MemoryStatus.HISTORICAL
                        if item.object_id == previous.object_id
                        else item.status
                    ),
                )
                for item in history
            ]

        history.append(obj)
        return MemoryTransition(
            previous=previous,
            current=obj,
            changed=previous is not None and previous.content != obj.content,
        )

    def current(self, semantic_type: SemanticType) -> SemanticObject | None:
        history = self._objects.get(semantic_type.value, [])
        return next(
            (item for item in reversed(history) if item.status == MemoryStatus.CURRENT),
            None,
        )

    def history(self, semantic_type: SemanticType) -> tuple[SemanticObject, ...]:
        return tuple(self._objects.get(semantic_type.value, ()))


@dataclass(frozen=True)
class ClutchState:
    reality: tuple[SemanticObject, ...]
    user_world: tuple[SemanticObject, ...]
    relationships: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    status: ProcessingStatus = ProcessingStatus.CONNECTED

    def __post_init__(self) -> None:
        reality_types = {SemanticType.EVIDENCE, SemanticType.INTERPRETATION}
        user_types = {
            SemanticType.MEANING,
            SemanticType.PRESENCE,
            SemanticType.DREAM,
            SemanticType.VALUE,
        }
        if any(obj.semantic_type not in reality_types for obj in self.reality):
            raise ValueError("reality side contains a User World semantic type")
        if any(obj.semantic_type not in user_types for obj in self.user_world):
            raise ValueError("user_world side contains a Reality semantic type")


def build_clutch(
    reality: Iterable[SemanticObject],
    user_world: Iterable[SemanticObject],
) -> ClutchState:
    reality_items = tuple(reality)
    user_items = tuple(user_world)
    relationships: list[str] = []

    for dream in (x for x in user_items if x.semantic_type == SemanticType.DREAM):
        relationships.append(f"{dream.object_id}:requires_reality_mapping")
    for meaning in (x for x in user_items if x.semantic_type == SemanticType.MEANING):
        relationships.append(f"{meaning.object_id}:preserve_user_meaning")

    unknowns = tuple(
        f"{obj.object_id}:relationship_not_established"
        for obj in user_items
        if not any(rel.startswith(obj.object_id + ":") for rel in relationships)
    )
    return ClutchState(
        reality=reality_items,
        user_world=user_items,
        relationships=tuple(relationships),
        unknowns=unknowns,
    )


@dataclass(frozen=True)
class FrameReview:
    current_frame: str
    assumptions: tuple[str, ...]
    excluded_regions: tuple[str, ...]
    unasked_questions: tuple[str, ...]
    triggers: tuple[str, ...]
    alternative_frames: tuple[str, ...] = ()


FRAME_TRIGGERS = {
    "contradiction",
    "stagnation",
    "boundary_pressure",
    "unexplained_gap",
    "user_correction",
}


def reopen_frame(
    *,
    current_frame: str,
    assumptions: Iterable[str],
    excluded_regions: Iterable[str],
    unasked_questions: Iterable[str],
    triggers: Iterable[str],
    alternative_frames: Iterable[str] = (),
) -> FrameReview:
    active = tuple(triggers)
    if not any(trigger in FRAME_TRIGGERS for trigger in active):
        raise ValueError("at least one recognized frame-reopening trigger is required")
    return FrameReview(
        current_frame=current_frame,
        assumptions=tuple(assumptions),
        excluded_regions=tuple(excluded_regions),
        unasked_questions=tuple(unasked_questions),
        triggers=active,
        alternative_frames=tuple(alternative_frames),
    )


@dataclass(frozen=True)
class VerificationResult:
    status: str
    violations: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in {"PASS", "FAIL", "UNKNOWN"}:
            raise ValueError("invalid verification status")


def verify_clutch(
    clutch: ClutchState,
    *,
    decision_owner: str | None = None,
    frame_review: FrameReview | None = None,
) -> VerificationResult:
    violations: list[str] = []

    if any(obj.semantic_type == SemanticType.DREAM for obj in clutch.reality):
        violations.append("DREAM_ON_REALITY_SIDE")
    if any(obj.semantic_type == SemanticType.EVIDENCE for obj in clutch.user_world):
        violations.append("EVIDENCE_ON_USER_WORLD_SIDE")
    if decision_owner not in (None, "HUMAN"):
        violations.append("NON_HUMAN_DECISION_OWNER")
    if frame_review is not None and not frame_review.current_frame:
        violations.append("MISSING_CURRENT_FRAME")

    if violations:
        return VerificationResult(status="FAIL", violations=tuple(violations))
    if not clutch.reality or not clutch.user_world:
        return VerificationResult(
            status="UNKNOWN",
            notes=("clutch side is incomplete",),
        )
    return VerificationResult(status="PASS")


def classify_user_statement(
    content: str,
    *,
    declared_type: SemanticType | None = None,
) -> SemanticObject:
    """Never guess a semantic type from raw prose.

    An upstream model may propose a type, but this boundary stores the proposal
    only when the caller explicitly supplies it. Otherwise the object is UNKNOWN.
    """
    return SemanticObject.create(
        declared_type or SemanticType.UNKNOWN,
        content,
        source="USER",
    )
