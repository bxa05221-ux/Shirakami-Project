# Re-observation Queue Boundary Specification

## Purpose

Carry unresolved meaning from a Context transition into a later observation
without resolving it automatically.

```
Context Transition
      ↓
unresolved item
      ↓
Re-observation Queue
      ↓
later Observation
      ↓
Context Transition
```

## Relationship to 暗問層

The queue gives the unresolved item a concrete lifecycle:

```
意味未決保持
    ↓
再観測待ち
    ↓
再観測
    ↓
新しいObservation
```

This is an implementation boundary, not a claim that the historical 暗問層
has been fully reconstructed.

## Invariants

1. Every request has a source Observation.
2. At least one unresolved item is required.
3. Requests are append-only in sequence.
4. Duplicate request IDs are rejected.
5. Marking an item observed does not resolve its meaning.
6. Human Gate remains required.
7. The queue has no decision authority.

## Non-goals

The queue does not:

- decide what an unresolved item means;
- rank unresolved items;
- infer human intent;
- convert observation into approval;
- replace Human Gate.

The queue only keeps the question alive long enough for another observation.
