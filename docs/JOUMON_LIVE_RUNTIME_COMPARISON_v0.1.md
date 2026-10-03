# JOUMON Live Runtime Comparison v0.1

## Status

- status: experimental-harness
- live_provider_calls: not performed by this harness
- credentials: caller supplied
- provider_sdk: caller supplied

## Purpose

This harness defines the next verification step after deterministic runtime
substitution:

> Hold Context and Protocol constant while changing the Runtime.

The comparison is about **boundary invariants**, not which runtime produces a
better answer.

## Fixed variables

- Context identity
- Protocol identity
- Human final-decision authority
- Human Gate requirement
- Evidence authority
- Evidence lineage

## Variable

- Runtime identity
- Provider identity
- Runtime output
- Provider-specific transport/client implementation

## Safety boundary

The harness does not store credentials and does not import a provider SDK.
Each runtime is supplied as an injected callable.

A live Fugu adapter may use Sakana AI's OpenAI-compatible API from an external
caller. Sakana documents Fugu as available through OpenAI-compatible Responses,
Chat Completions, and Models APIs.

## Interpretation

A passing comparison demonstrates only that the JOUMON boundary can preserve
declared invariants while runtime/provider/output change.

It does **not** establish:

- model quality;
- factual accuracy;
- provider reliability;
- cost efficiency;
- production readiness;
- superiority of one runtime over another.

## Next experiment

Use the same Context/Protocol with:

1. a live Sakana Fugu runtime;
2. another live runtime;
3. the same JOUMON Evidence and Human Gate boundary.

Record provenance and lineage without granting authority to either runtime.
