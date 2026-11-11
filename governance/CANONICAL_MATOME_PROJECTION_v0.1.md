# Canonical Matome and Public Projection v0.1

## Decision

The Shirakami Matome YAML is treated as a **canonical semantic record**, not as a public configuration file.

The preferred operating model is:

```text
Private Canonical Matome Repository
        |
        | Publication Filter / Projection
        v
Project-specific Public Matome
        |
        v
Public Repository
```

## Canonical Matome

The canonical repository is the authoritative working archive for Matome meaning.

It may contain:

- complete semantic records
- design rationale
- design history
- alternatives and rejected designs
- private Context and Evidence references
- operational knowledge
- publication classification
- provenance and lineage
- release history

The canonical repository should remain private unless a deliberate publication decision is made.

## Public Projection

A public repository receives only the subset required for that repository's purpose.

A public Matome is therefore a **projection** of the canonical Matome, not an independent competing source of truth.

A projection may contain:

- public principles
- public protocol contracts
- public schemas
- public examples
- public verification evidence
- public provenance sufficient to understand the released material

A projection should not silently add private design history.

## Publication Filter

Each Matome intended for projection should carry an explicit publication classification.

Recommended classes:

- `public-contract`
- `public-example`
- `public-verification`
- `protected-design-history`
- `protected-operational`
- `protected-sensitive-data`

Only the first three are eligible for ordinary public projection.

## Project-specific selection

Different projects may publish different projections.

For example:

```text
Canonical Matome
   |
   +--> Shirakami-Project projection
   +--> ThreadRPG projection
   +--> Guide AI projection
   +--> Third-party evaluation projection
```

There is no requirement that every project receive the complete Matome library.

## Source-of-truth rule

The canonical Matome is the source of truth for semantic intent.

The public projection is the source of truth only for the **published contract of that project**.

Changes to a public projection should be traceable to a canonical Matome revision where appropriate, without exposing protected material.

## Security rule

Do not place credentials, API keys, private user data, or confidential operational records into either canonical Matome or public projections unless their storage is explicitly required and appropriately protected.

Matome publication policy does not replace repository access control, secret management, or legal review.

## Historical protection

Moving the canonical source into a private repository does not erase material already present in a public Git history.

Existing public history must be treated as already disclosed. Future publication should use the projection boundary.

## Operational principle

> **One semantic source. Many deliberate projections.**

This preserves continuity across projects while preventing accidental publication of the complete design history.

## Relationship to Semantic Handoff

Semantic Handoff remains a runtime/meaning-transfer mechanism.

Canonical Matome and public projection are a **publication-management layer** around that semantic content.

They should not be conflated:

- Semantic Handoff answers: "What meaning must travel?"
- Canonical Matome answers: "What is the authoritative semantic record?"
- Public Projection answers: "What part of that record is intentionally published here?"

## Current repository status

This public repository documents the model and provides public implementation/examples.

It is **not** itself declared to contain the complete canonical private Matome archive.
