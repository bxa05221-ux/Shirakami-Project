# Real Provider Integration Notes v0.1

status: boundary-ready, execution-pending

## First target

The first concrete adapter slot is an OpenAI-compatible runtime boundary.

This repository intentionally contains no API key, token, credential, or provider secret.

## Integration contract

A local caller supplies an authenticated `invoke(request, model)` callable. JOUMON only sees:

- Context ID
- Protocol ID
- task description
- returned observation text
- runtime/provider metadata

The resulting observation enters the same Unified Evidence and Lineage path as a mock runtime.

## Why execution is pending

A real provider call requires credentials and an explicitly configured runtime environment. The repository must not manufacture, embed, or commit those credentials.

## Acceptance test

A live adapter is considered boundary-compatible when a real invocation can pass through:

`Context -> Protocol -> LiveRuntimeAdapter -> RuntimeResult -> Unified Evidence -> Lineage -> Semantic Handoff -> Human Gate`

without changing the protocol semantics.

## Non-claim

This document does not claim that a live OpenAI call has been executed by the repository test suite. The current automated test uses a deterministic test double.
