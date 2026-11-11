# JOUMON × Sakana Fugu Runtime Adapter Boundary v0.1

## Status

- status: conceptual-boundary
- implementation: deterministic adapter PoC
- live_provider_verification: not yet performed
- credentials_required: no
- provider_sdk_required: no

## Purpose

This document defines how Sakana Fugu can be represented as one replaceable
runtime inside JOUMON.

The purpose is not to reproduce Fugu's internal orchestration. Fugu remains
responsible for its own multi-agent/model orchestration. JOUMON treats that
system as a runtime boundary and preserves the surrounding Context, Protocol,
Evidence, provenance, and Human Gate semantics.

## Boundary

```
Human
  |
Human Gate
  |
JOUMON Context / Protocol / Evidence Contract
  |
  +---- OpenAI Runtime
  +---- Gemini Runtime
  +---- Sakana Fugu Runtime
  +---- Local Runtime
  |
Evidence / Verification
```

Fugu may itself coordinate multiple models internally. That internal topology
is not required to be exposed to the JOUMON protocol core.

## Provider Identity

The adapter records:

- `runtime_id`: JOUMON runtime identity
- `provider`: `sakana-ai`
- `model`: supplied to the injected invocation function
- `mode`: `live`
- `runtime_type`: `model`

Provider identity is provenance metadata, not authority.

## OpenAI-Compatible API

Sakana AI documents Fugu as available through an OpenAI-compatible API.
JOUMON therefore may use the same client pattern as an OpenAI-compatible
endpoint, but must not collapse the provider identity into
`openai-compatible`.

The distinction matters:

```
transport/client compatibility != provider identity
```

A Fugu execution can use an OpenAI-compatible client while remaining
provenanced as Sakana Fugu.

## Non-Goals

This boundary does not:

- claim that Fugu is superior to other runtimes;
- inspect or reproduce Fugu's internal agent selection;
- make Sakana AI dependent on JOUMON;
- require a live API key;
- make JOUMON responsible for provider authentication;
- delegate Human Gate authority to Fugu or any other runtime.

## Verification Target

The next useful experiment is runtime substitution:

1. Hold Context and Protocol constant.
2. Execute with a deterministic Fugu-shaped adapter.
3. Execute the same contract through another runtime adapter.
4. Compare RuntimeResult and Evidence metadata.
5. Verify that the runtime can change without changing the authority boundary.

A later live experiment may use Sakana Fugu through its documented API, but
that should remain an explicitly opt-in integration test rather than part of
the protocol core.

## Architectural Significance

The interesting question is not whether JOUMON can call Fugu.

It is:

> Can a sophisticated multi-agent orchestrator be swapped into JOUMON
> without changing the semantic contract or moving decision authority?

If the answer is demonstrated experimentally, Sakana Fugu becomes a useful
test case for the runtime-neutral boundary rather than a dependency of it.
