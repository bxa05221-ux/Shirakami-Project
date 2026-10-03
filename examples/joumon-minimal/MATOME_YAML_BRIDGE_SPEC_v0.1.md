# JOUMON Matome YAML Bridge Specification v0.1

status: experimental
purpose: Provide a minimal interchange bridge from JOUMON Semantic Handoff to a Matome-shaped document while preserving Context, Evidence, Lineage and authority boundaries.

## Boundary

    JOUMON Semantic Handoff
             |
             v
       Matome Bridge
             |
             v
       Matome-shaped document
             |
             v
       next Shirakami/runtime stage

## Preserved fields

- handoff identity
- Context identity
- Protocol identity
- Evidence records
- Evidence Lineage
- non-authoritative handoff status
- human final decision authority

## v0.1 implementation note

The PoC uses JSON-compatible output rather than a YAML dependency. This is intentional: the bridge demonstrates the interchange contract first. A canonical YAML serializer can be introduced later without changing the semantic fields.

## Security / authority boundary

The bridge rejects documents that claim a Runtime or other non-human actor as final decision authority.

Serialization does not create authority. A Matome document remains an interchange artifact, not a decision.

## Relationship to Shirakami

JOUMON does not redefine Shirakami's Matome YAML. This bridge is an experimental compatibility layer intended to make the semantic correspondence explicit before adopting a canonical Shirakami serialization.
