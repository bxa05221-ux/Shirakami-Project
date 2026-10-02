# JOUMON Matome Roundtrip Specification v0.1

status: experimental
purpose: Demonstrate that a JOUMON Semantic Handoff can be serialized into a Matome-shaped interchange artifact and reconstructed without losing semantic identity, Evidence, Lineage, or authority boundaries.

## Flow

    Semantic Handoff
          |
          v
    Matome-shaped artifact
          |
          v
    Handoff Import
          |
          v
    Semantic Handoff

## Roundtrip invariants

- handoff_id is preserved.
- context_id is preserved.
- protocol_id is preserved.
- Evidence identities and runtime provenance are preserved.
- Lineage relationships are preserved.
- handoff remains non-authoritative.
- human remains final decision authority.

## Why this matters

Serialization is no longer a one-way export. A receiving system can reconstruct the same semantic boundary from the interchange artifact, enabling a future Runtime B to consume the handoff without depending on Runtime A's internal representation.

## Scope

v0.1 is a local deterministic PoC. It does not claim compatibility with any production Matome YAML implementation until a canonical schema is agreed and tested.
