# JOUMON Provider-Neutral Runtime Contract v0.1

status: experimental
purpose: Define the minimum exchange contract for connecting different AI providers/runtimes without making any provider canonical.

## Contract

JOUMON exchanges:
- Context identity
- Protocol identity and binding
- task and constraints
- Runtime identity
- observable result metadata

Provider-specific details remain behind the Runtime implementation.

The canonical Context does not contain a provider selector. A provider may be recorded as execution provenance/metadata, but provider identity does not become authority.

## Current test doubles

The PoC uses provider-compatible test doubles labelled:
- `openai-compatible`
- `gemini-compatible`

These are **not live OpenAI or Gemini integrations**. No API call, credential, network access, or provider SDK is used.

## Required invariants

1. Same Context can reach different provider-compatible runtimes.
2. Protocol remains bound to that Context.
3. Runtime/provider identity is observable.
4. Provider identity is provenance, not authority.
5. Provider-specific details do not enter canonical Context.
6. Human remains final decision authority.

## Next boundary

Live provider adapters may later implement this contract. Such integration requires separate credential, SDK/license, privacy, reproducibility, and publication review.
