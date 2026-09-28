# Validated EvidenceCandidate → EvidenceRecord Boundary

This boundary is the point where a structurally validated observation candidate
may be materialized as an EvidenceRecord.

```text
EvidenceCandidate
  ↓
Structural Validation
  ↓
ValidatedEvidenceCandidate
  ↓
EvidenceRecord
  ↓
stable evidence_id
```

The EvidenceRecord preserves the observation and execution provenance chain:

`candidate_id → observation_id → witness_id → trace_id → approval_id → protocol_id → request_id`

The generated `evidence_id` is deterministic for the canonical record payload.
It is an identifier for the record, not a truth claim and not an authorization token.

The builder does not grant execution, publication, merge, or decision authority.
Human Gate remains required.

> Evidence identity is not decision authority.
