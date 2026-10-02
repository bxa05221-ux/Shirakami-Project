# JOUMON Semantic Handoff Specification v0.1

status: experimental
purpose: Transfer Context, Protocol identity, Evidence and Lineage between execution stages without losing semantic continuity or authority boundaries.

## Handoff payload

A Semantic Handoff contains:
- Context identity
- Protocol identity
- one or more Unified Evidence records
- corresponding Evidence Lineage
- explicit non-authoritative status
- explicit human final decision authority

## Boundary

    Runtime A
       |
    Evidence A
       |
    Lineage A
       |
    Semantic Handoff
       |
    Runtime B / next stage

The handoff carries meaning and provenance forward. It does not carry decision authority forward.

## Invariants

1. Evidence must match the handoff Context and Protocol.
2. Every included Lineage record must refer to included Evidence.
3. Provider/runtime identity remains provenance.
4. Evidence remains non-authoritative.
5. Human remains final decision authority.
6. A receiving Runtime may interpret the handoff but may not silently rewrite its authority semantics.

## Relationship to Shirakami

This is a minimal JOUMON analogue of semantic handoff. It intentionally avoids depending on Shirakami-specific YAML syntax so that the boundary remains provider/runtime independent. A later bridge may serialize this structure as Matome YAML or another interchange format.

## Non-goals

This specification does not establish truth of observations, model quality, provider superiority, cryptographic attestation, production readiness, or IP conclusions.
