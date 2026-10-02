# JOUMON Handoff Chain Specification v0.1

status: experimental
purpose: Demonstrate that Semantic Handoff can carry Context, Evidence and Lineage into a subsequent Runtime stage while preserving provenance and human authority.

## Flow

    Runtime A
       |
    Evidence A
       |
    Lineage A
       |
    Semantic Handoff
       |
    Runtime B
       |
    Evidence B
       |
    Lineage B

## Required invariants

- Context identity remains stable across stages.
- Protocol identity remains stable across stages.
- Prior Evidence remains attached to the handoff.
- New Evidence receives its own Runtime provenance.
- Lineage distinguishes prior and new observations.
- Human remains final decision authority throughout the chain.

## Interpretation boundary

A receiving Runtime may use prior Evidence as input for another observation. It does not inherit the authority of the prior Runtime, Evidence, or Handoff.

The v0.1 chain is deterministic and uses mock runtimes. It does not establish live-provider interoperability, truth of generated outputs, or production readiness.
