# JOUMON Full Cycle v0.1

status: experimental

## Cycle

    Matome
      ↓
    Context + Protocol
      ↓
    Runtime A/B/C/.../N
      ↓
    Evidence + Lineage
      ↓
    Semantic Handoff
      ↓
    Matome serialization
      ↓
    Handoff import
      ↓
    Verification
      ↓
    Human Gate
      ↓
    explicit human decision

## Core invariant

The cycle may automate observation, serialization, transfer, and structural verification. It must not automate or infer the final human decision.

## Provider neutrality

Runtime adapters are replaceable. Provider identity is recorded as provenance, not authority.

## Current status

The full cycle is implemented as a deterministic adapter-injection PoC. It has not yet been demonstrated with nine authenticated production providers.
