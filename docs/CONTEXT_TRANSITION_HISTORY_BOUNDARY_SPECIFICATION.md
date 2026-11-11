# Context Transition History Boundary Specification

## Purpose

Record the transition between Context states as an explicit lineage boundary
derived from an Observation.

This boundary is intended to reconnect:

```
Observation
    ↓
Context Transition
    ↓
unresolved meaning
    ↓
next Context
    ↓
re-observation
```

The boundary does not decide which Context should be adopted.

## Relationship to 暗問層

The transition history provides a concrete place to preserve unresolved
items across Context changes.

It therefore supports the observed design relationship:

```
意味未決保持
    ↕
Context Transition History
    ↕
暗問層
    ↕
再観測
```

This document does not claim that the implementation is a complete
reconstruction of the historical 暗問層.

## Transition record

Each record contains:

- `transition_id`: stable identity for the transition record.
- `sequence`: monotonic position in the history.
- `observation_id`: source Observation identity.
- `from_context_id`: preceding Context identity.
- `to_context_id`: resulting or candidate Context identity.
- `unresolved_items`: unresolved meaning carried forward.
- `transition_kind`: `observed` or `candidate`.
- `provenance`: descriptive source information.
- `human_gate_required`: always `true`.
- `decision_authority`: always `false`.

## Invariants

1. A transition must identify its source Observation.
2. Transition history is append-only.
3. Sequence numbers increase monotonically.
4. Duplicate transition IDs are rejected.
5. Unresolved items are preserved rather than resolved by the boundary.
6. A candidate transition is not treated as an adopted decision.
7. The boundary never grants decision authority.
8. Human Gate remains outside the transition history.

## Non-goals

This boundary does not:

- determine the correct Context;
- resolve ambiguous meaning;
- infer human intent;
- replace the Human Gate;
- turn an Observation into Evidence automatically;
- claim that historical Shirakami layers have been fully reconstructed.

## Verification

The first implementation verifies:

- unresolved-item preservation;
- append-only monotonic history;
- duplicate/non-monotonic rejection;
- authority invariants.

One conceptual change, one verification.
