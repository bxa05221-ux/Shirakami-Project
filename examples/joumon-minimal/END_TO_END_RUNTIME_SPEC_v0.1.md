# JOUMON End-to-End Runtime Roundtrip v0.1

status: experimental

## Flow

    Runtime A
       |
       v
    Evidence A
       |
       v
    Semantic Handoff
       |
       v
    Matome-shaped artifact
       |
       v
    Handoff Import
       |
       v
    Runtime B consumes restored Handoff
       |
       v
    Evidence B

## What this demonstrates

Runtime B does not need Runtime A's internal representation. It consumes the semantic boundary reconstructed from the interchange artifact.

The two runtimes retain separate provenance, while Context and Protocol identity remain continuous.

## Authority invariant

The entire roundtrip remains non-authoritative. The receiving Runtime cannot inherit decision authority from the sending Runtime or from the Handoff.

## Scope

This is a deterministic mock-runtime PoC. It demonstrates the protocol boundary, not live-provider interoperability or correctness of model outputs.
