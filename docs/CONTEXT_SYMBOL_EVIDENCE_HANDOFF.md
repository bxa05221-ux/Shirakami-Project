# Context → Symbol → Re-observation → Evidence Handoff

This document defines the Phase 5 boundary for symbolic context work.

```text
Lived Context
    ↓
Observation
    ↓
Symbol / expression
    ↓
Multiple interpretations
    ↓
Re-observation request
    ↓
Later Observation
    ↓
Evidence candidate
    ↓
Structural Validation
    ↓
Human Gate
```

## Rule

The symbol is a navigation layer for context, not a source of truth.

The interpretation may explain why a re-observation was requested, but it does
not establish the observed fact. The later Observation must retain its own
provenance and Evidence ID when it enters the evidence pipeline.

## Example

A person says `「生きろ」`.

Possible contextual readings might include survival, renewal, responsibility,
or resistance. Shirakami does not select one as the person's true meaning.
Instead, the interpretation can initiate re-observation of the person's actual
circumstances.

Only what is subsequently observed and validated can enter Evidence.

## Human Gate

Symbolic interpretation may generate candidates and questions. It may not
become an instruction, diagnosis, decision, or approval merely because the
system generated it.
