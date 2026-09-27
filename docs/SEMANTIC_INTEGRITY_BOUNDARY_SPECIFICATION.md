# Semantic Integrity Boundary Specification

## Purpose

Define the boundary that verifies the semantic identity of a Protocol referenced by a Semantic Handoff.

This boundary verifies meaning and provenance. It does not grant execution, publication, merge, or decision authority.

## Scope

The boundary answers:

> Does this Protocol ID resolve to the Protocol definition and lineage that the Handoff claims to use?

It does not answer:

> Should this Protocol be approved?

Approval remains a Human Gate decision.

## Required distinction

- Protocol ID: identifies a protocol definition.
- Evidence ID: identifies evidence supporting the protocol or observed result.
- Trace ID: identifies execution/observation lineage.
- Handoff ID: identifies the context envelope crossing a boundary.
- Provider: identifies the execution implementation.
- Human Gate: retains decision authority.

No identifier is itself an authority token.

## Proposed verification flow

```text
Protocol ID
    |
    v
Protocol Registry
    |
    +--> Protocol definition
    +--> Protocol version
    +--> source candidate
    +--> evidence IDs
    +--> approval provenance
    |
    v
Semantic Integrity Verification
    |
    +--> resolved
    +--> lineage-consistent
    +--> approval provenance consistent
    |
    v
Semantic Handoff
```

## Integrity conditions

A referenced Protocol is semantically valid only when:

1. the Protocol ID resolves to exactly one Protocol definition;
2. the resolved Protocol ID matches the Handoff's protocol ID;
3. the Protocol definition is structurally valid;
4. the Protocol's source candidate and evidence lineage are present;
5. approval provenance identifies the Human Gate;
6. approval provenance is descriptive of a human decision and does not become execution authority;
7. any mismatch produces a verification failure rather than an inferred correction.

## Failure behavior

Verification must fail closed for semantic integrity.

Examples:

- unknown Protocol ID -> `unresolved`
- multiple definitions for one Protocol ID -> `ambiguous`
- missing evidence lineage -> `incomplete`
- approval provenance missing -> `unverified`
- Protocol ID mismatch -> `mismatch`

A failed integrity check MUST NOT:

- authorize execution;
- authorize publication;
- authorize merge;
- substitute a different Protocol;
- convert an AI-generated proposal into approval.

## Authority invariant

```yaml
authority:
  execution_authorized: false
  publish_authorized: false
  merge_authorized: false
  human_gate_required: true
```

Semantic verification describes whether a Protocol reference is internally coherent. It does not decide whether a human should accept the Protocol.

## Relationship to Trace

Trace remains an execution/observation record.

Trace does not need to own `protocol_ids` merely because Semantic Handoff verifies them.

The intended separation remains:

```text
Trace
  = what happened

Protocol
  = which rule/procedure was referenced

Semantic Handoff
  = where execution lineage and protocol context are connected
```

## Implementation rule

The first implementation of this boundary should introduce verification without changing the existing Trace schema.

Verification must be independently testable before it is connected to Runtime or API.

## Verification rule

One conceptual change, one verification.

The first implementation should therefore contain:

- one Protocol Registry/Resolver boundary;
- one Semantic Integrity verification result;
- tests for valid resolution;
- tests for unknown, ambiguous, and mismatched references;
- tests proving authority remains unchanged.

## Non-goals

This boundary does not:

- select a Protocol;
- approve a Protocol;
- execute a Protocol;
- publish a result;
- merge repository changes;
- infer human intent;
- replace the Human Gate;
- require a specific AI provider.

## Closing principle

Semantic Integrity answers whether the meaning and provenance of a referenced Protocol can be verified.

It does not answer what humans should decide.
