# Symbolic Human Gate Specification

Symbolic interpretation can produce a candidate, but never a decision.

```text
Symbol
  ↓
Interpretations
  ↓
Re-observation
  ↓
Observation provenance
  ↓
Candidate
  ↓
Human Gate
  ↓
Protocol / Runtime
```

## Required properties

- `human_gate_required: true`
- `decision_authority: false`
- at least one observation provenance reference
- multiple interpretations remain representable
- no symbolic candidate receives an Evidence ID merely by being generated

The purpose is not to prevent the system from saying "stop" or "act" as a
candidate. The purpose is to ensure that such a statement remains a candidate
until a human accepts, rejects, or revises it.

This is the implementation form of the distinction between internal conflict
and human decision: the system may strongly surface a conflict when the
observed consequences make a candidate unsafe, while retaining the final
authority at the Human Gate.
