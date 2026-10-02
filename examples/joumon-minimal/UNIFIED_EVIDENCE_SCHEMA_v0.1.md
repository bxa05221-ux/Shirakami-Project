# JOUMON Unified Evidence Schema v0.1

status: experimental
purpose: Normalize observations from replaceable Runtime implementations into one provider-neutral Evidence record.

## Design principle

Runtime diversity is preserved in provenance; Evidence semantics remain common.

Runtime-specific result -> Evidence Adapter -> Unified Evidence -> Verification -> Human Gate

## Canonical record

    evidence_id: "<stable-id>"
    context_id: "<context-id>"
    protocol_id: "<protocol-id>"
    runtime:
      runtime_id: "<runtime-id>"
      provider: "<provider-or-platform>"
      runtime_type: "<model|agent|platform|local>"
      mode: "<live|mock>"
    observation:
      output: "<observed-output>"
      observed: true
    authority:
      evidence: "non-authoritative"
      final_decision: "human"
    provenance:
      source: "<adapter-or-execution-source>"
      version_or_commit: "<version-or-commit>"
    verification:
      status: "pending"
      method: null

## Invariants

- context_id and protocol_id identify the same execution context.
- Runtime/provider identity is retained.
- Runtime/provider identity does not become decision authority.
- Evidence is observational and non-authoritative.
- Final decision authority remains human.
- Mock execution is never represented as live provider execution.

## Interoperability target

The same Evidence schema is intended for OpenAI-compatible runtimes, Gemini-compatible runtimes, Claude-compatible runtimes, Codex, GitHub Copilot / Copilot CLI, GitHub Models, ECC or other agent harnesses, local LLMs, and future runtimes.

This document does not assert that any listed runtime currently implements this schema.

## Non-goals

This schema does not rank providers, evaluate model quality, authorize provider use, grant authority to an AI runtime, establish production readiness, or establish patentability/novelty/IP conclusions.

Live integrations require separate SDK/license, credential, privacy, security, reproducibility, and publication review.
