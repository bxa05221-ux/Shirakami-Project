# Observation → Evidence Structural Validation Boundary

This boundary establishes the missing structural step between an EvidenceCandidate and an EvidenceRecord.

```text
AIwitness
  ↓
Observation
  ↓
EvidenceCandidate (pending)
  ↓
Structural Validation
  ↓
ValidatedEvidenceCandidate
  ↓
EvidenceRecord / evidence_id
```

Validation confirms that provenance fields are present and that the candidate is still non-authoritative.

Structural validation does **not**:

- create an `evidence_id`
- convert a candidate into an EvidenceRecord
- grant execution, publication, or merge authority
- bypass Human Gate

The candidate remains separate from Evidence until the next boundary explicitly constructs an EvidenceRecord.

> Observation is not Evidence merely because it is observable.
>
> Validation is a structural checkpoint, not a truth oracle.
