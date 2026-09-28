# Symbolic Interpretation / Evidence Boundary Specification

## Purpose

Prevent symbolic interpretation from being silently promoted to evidence.

A symbolic trace records how an expression is interpreted within a context.
Evidence records an externally or operationally grounded observation with its
own provenance. The two may be related, but they are not interchangeable.

## Boundary

```text
Symbol
  ↓
Interpretation
  ↓
Re-observation Request
  ↓
Observation
  ↓
Evidence Candidate
  ↓
Structural Validation
  ↓
Human Gate
```

## Invariants

1. Symbolic interpretation is never evidence by itself.
2. A symbol may trigger re-observation, but cannot validate itself.
3. Re-observation produces an Observation, not an automatic Decision.
4. Evidence provenance must point to the Observation or external source, not
   merely to the symbolic expression.
5. Multiple symbolic interpretations may coexist.
6. Human Gate remains the final authority for consequential decisions.

## Example

`"神"` may be associated with rescue, judgment, authority, absence, hope,
or other meanings. Those interpretations are context observations. If the
interpretation leads to a question about lived reality, the system can create
a re-observation request. Only the resulting observation and its provenance
can enter the evidence pipeline.

## Architectural consequence

```text
Symbolic Recursion
        │
        ├── interpretation provenance
        │
        └── Re-observation
                 ↓
             Observation
                 ↓
              Evidence
                 ↓
            AIwitness trace
                 ↓
            Human Gate
```

This preserves the distinction between meaning-making and fact-finding while
allowing the two processes to communicate.
