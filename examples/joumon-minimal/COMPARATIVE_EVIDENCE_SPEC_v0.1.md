# JOUMON Comparative Evidence Specification v0.1

status: experimental
purpose: Compare observations from multiple replaceable runtimes without converting comparison into authority or ranking.

## Model

One Context + one Protocol may produce multiple Evidence records.

    Context + Protocol
          |
      Runtime A ----> Evidence A
          |
      Runtime B ----> Evidence B
          |
      Runtime N ----> Evidence N
          |
      Comparative View
          |
      Verification
          |
      Human Gate

## Comparison dimensions

A comparative view may expose:

- context_id
- protocol_id
- runtime_id
- provider
- runtime_type
- execution mode
- observed output
- metadata
- evidence verification status
- provenance

It must not silently add:

- provider score
- model quality ranking
- recommendation
- final decision
- authority transfer

## Invariants

1. All compared records retain their original provenance.
2. Comparison does not modify the underlying Evidence.
3. A comparison is itself an observation/artifact, not an authoritative decision.
4. Human Gate remains the final decision boundary.
5. Missing, mock, or unverified observations remain explicitly marked.
6. Different outputs are not automatically interpreted as better or worse.

## Example

Two mock runtimes can produce different candidate outputs for the same Context and Protocol. The comparative artifact records the difference and its provenance; it does not select a winner.

## Non-goals

This specification does not define benchmark scores, model rankings, provider recommendations, or live-provider equivalence. Such evaluations, if later required, must be separately specified with explicit methodology and human review.
