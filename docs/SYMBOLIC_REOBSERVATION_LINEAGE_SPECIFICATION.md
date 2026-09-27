# Symbolic Recursion → Re-observation Lineage Boundary Specification

## Purpose

Bind a symbolic observation to the temporal lineage of a later re-observation
without treating the symbol as resolved.

```
symbolic expression
      ↓
multiple interpretations
      ↓
unresolved re-observation request
      ↓
later Observation
      ↓
new Context Transition
```

The bridge records provenance across two existing boundaries:

- Symbolic Recursion preserves multiple interpretations.
- Re-observation Lineage preserves the temporal relationship between a request
  and its later Observation.

Neither record determines what the symbol ultimately means.

## Invariants

1. Symbolic interpretations remain plural.
2. Re-observation lineage remains append-only.
3. A re-observation request still receives at most one recorded result link.
4. Symbolic meaning is not converted into evidence merely by being recorded.
5. The later Observation does not retroactively resolve the symbol.
6. Human Gate remains required.
7. Decision authority remains false.

## Flow

```
Symbol
  ↓
Symbolic Recursion
  ↓
Re-observation Request
  ↓
Later Observation
  ↓
Context Transition
  ↓
Evidence / Human Gate
```

The final Evidence boundary must still distinguish lived/external evidence
from symbolic interpretation and preserve provenance rather than collapsing
the two.
