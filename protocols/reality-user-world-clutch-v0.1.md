# Reality–User World Clutch Protocol v0.1

Status: implementation candidate

This protocol defines provider-neutral runtime primitives for keeping Reality-side
information separate from User World information while allowing an explicit
connection between them.

## Invariants

- Evidence is not Dream.
- Meaning is not Evidence.
- Presence is not automatically Evidence.
- Past Dream is not Current Dream.
- Observation Space is not World Totality.
- Unknown is not silently completed.
- Connection is not Decision.
- Decision Authority remains Human.

## Runtime boundary

The runtime deliberately does not infer semantic types from raw prose. A model may
propose a classification, but the proposal must enter this boundary explicitly.
Unresolved input becomes UNKNOWN.

## Pipeline

SemanticObject → TemporalMemory → ClutchState → FrameReview → Human Gate → Verification

## Failure semantics

- FAIL: an invariant was violated; decision flow must stop.
- UNKNOWN: required information is missing or unresolved; preserve uncertainty.
- BLOCKED: reserved for an upstream authority/security boundary.

## Initial implementation scope

The first implementation is intentionally small and deterministic. It proves the
state model and invariants before adding provider-specific NLP or storage.
