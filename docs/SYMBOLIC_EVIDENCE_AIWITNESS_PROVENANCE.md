# Symbolic → Evidence → AIwitness Provenance Boundary

Phase 5 closes the provenance path without collapsing semantic layers.

```text
Symbol
  ↓
Interpretation(s)
  ↓
Re-observation Request
  ↓
Observation
  ↓
Evidence ID
  ↓
AIwitness provenance
  ↓
Human Gate
```

## Rule

The symbolic layer explains the origin of a re-observation. It does not prove
the resulting Evidence.

The Evidence ID belongs to the observed/validated evidence record. Symbolic
metadata is attached as provenance metadata and explicitly marked
`symbolic_is_evidence: false`.

AIwitness records execution/provenance facts. It does not convert provenance
into decision authority.

## Boundary invariant

```text
symbolic meaning != observation != evidence != decision
```

The layers may be linked, but they must remain distinguishable.
