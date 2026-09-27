# Re-observation Lineage Boundary Specification

## Purpose

Bind an unresolved re-observation request to the later Observation that
actually revisited it.

```
unresolved item
      ↓
re-observation request
      ↓
later Observation
      ↓
new Context Transition
```

The link records provenance, not resolution.

## 暗問層 connection

This adds the missing temporal edge to:

```
意味未決保持 → 再観測待ち → 再観測 → 次の観測
```

The system can now answer **which later Observation came from which
unresolved request**, without claiming that the later Observation resolved
the original meaning.

## Invariants

1. Every link identifies its source Observation.
2. Every link identifies its result Observation.
3. A request receives at most one recorded result link.
4. Lineage is append-only and monotonic.
5. Lineage does not resolve meaning.
6. Human Gate remains required.
7. Decision authority remains false.

## Non-goals

This boundary does not judge whether the new Observation is correct,
successful, sufficient, or preferable. It only preserves the temporal
relationship.
