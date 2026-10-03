# JOUMON Real Provider Runbook v0.1

status: experimental

## Goal

Run one authenticated provider through the already-tested JOUMON boundary without placing credentials, prompts, or provider responses in Git.

## Required environment

- `OPENAI_API_KEY`
- `OPENAI_MODEL`

Both must be supplied by the operator at runtime.

## Safety boundary

- Do not commit the API key.
- Do not put the API key in Matome YAML.
- Do not persist raw provider responses unless intentionally creating an Evidence artifact.
- Record provider/model identity as provenance.
- Keep Human Gate outside the provider call.

## Expected path

    Matome
      ↓
    Context + Protocol
      ↓
    LiveRuntimeAdapter
      ↓
    OpenAI-compatible provider
      ↓
    RuntimeResult
      ↓
    Evidence
      ↓
    Lineage
      ↓
    Verification
      ↓
    Human Gate

## Verification status

The repository contains the live entrypoint and configuration guard. A successful live API execution must be performed by an authenticated operator; repository tooling does not claim that execution occurred merely because the adapter exists.
