# JOUMON Evidence Lineage Specification v0.1

status: experimental
purpose: Preserve the provenance path from Context and Protocol through Runtime to observed Evidence.

## Lineage

    Context
      | bound-by
    Protocol
      | executed-by
    Runtime
      | produced-observation
    Evidence

Lineage answers **where this Evidence came from**. It does not answer whether the observed output is correct.

## Required properties

- Context identity is retained.
- Protocol identity is retained.
- Runtime identity is retained.
- Evidence identity is retained.
- Relationships between these nodes are explicit.
- Lineage is observational and non-authoritative.
- Human Gate remains outside the lineage as the final decision boundary.

## Failure boundary

A lineage record with mismatched or missing identity relationships must not be treated as verified provenance.

## Non-goals

Lineage does not establish truth, model quality, provider superiority, production readiness, or IP conclusions. Cryptographic attestation and remote execution logs are future extensions, not part of v0.1.
