# Runtime Execution Boundary Specification

## Purpose

The Runtime Execution Boundary defines the point at which a validated Semantic Handoff becomes executable runtime work.

The boundary transfers **execution context and provenance**, not decision authority.

## Flow

`Semantic Handoff → RuntimeRequest → ProviderAdapter → RuntimeResult → EvidenceRecord`

Each transition MUST preserve traceability and MUST NOT increase authority.

## RuntimeRequest

A RuntimeRequest carries:

- `handoff_id`
- `trace_id`
- `execution_id`
- `project`
- `objective`
- `protocol_ids`
- `evidence_ids`
- `verification_scope`
- `input_data`
- optional `runtime_target`

`runtime_target` identifies where or against what runtime work is intended. It is descriptive and MUST NOT grant authority.

## Provider Boundary

Provider adapters are replaceable execution implementations.

A provider MUST return a RuntimeResult that preserves:

- `handoff_id`
- `trace_id`
- `execution_id`
- provider identity
- output
- `protocol_ids`
- `evidence_ids`

Provider identity MUST NOT become decision authority.

## Authority Invariants

At the runtime boundary:

- `execution_authorized = false`
- `publish_authorized = false`
- `merge_authorized = false`
- `human_gate_required = true`

A provider result violating these invariants MUST be rejected.

Runtime execution therefore records **what was executed and by which provider**, but does not decide whether the result may be published, merged, or accepted as a human decision.

## Evidence Closure

A RuntimeResult MUST be convertible into an EvidenceRecord while preserving the originating handoff and provider lineage.

The EvidenceRecord then becomes the traceable observation surface for AIwitness and subsequent verification.

## Human Gate

The Runtime Execution Boundary does not contain a decision gate that substitutes for the human.

The Human Gate remains the authority boundary for:

- acceptance
- publication
- merge
- consequential decision

Thus:

> AI may execute a protocol-defined operation; execution does not become authorization.

## Verification Rule

Changes to this boundary follow the Shirakami rule:

**一変更一検証**

A boundary change is incomplete until its corresponding verification demonstrates both:

1. provenance/lineage preservation; and
2. authority non-escalation.

## Non-Goals

This specification does not define:

- a specific LLM or AI provider;
- a provider-specific API;
- automatic publication;
- automatic merge;
- autonomous human-decision substitution.

The Runtime Execution Boundary is therefore a **replaceable execution boundary, not an authority boundary**.
