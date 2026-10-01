# Repository Boundary Map v0.2

This document defines the first-pass repository boundaries for the Shirakami project.

## Principle

The repository layout is itself a boundary:

- Public repositories contain reusable, reviewed software and specifications.
- Private repositories contain research, experiments, unreleased implementation, and IP candidates.
- New potentially protectable technical content is held for review before publication.
- Legacy repositories are preserved rather than destructively rewritten during the first phase.
- AI providers and execution systems are treated as replaceable Runtimes, not as part of Shirakami's core authority.

## Proposed public-facing set

1. `shirakami-model` — core architecture and model documentation
2. `shirakami-specification` — normative contracts and specifications
3. `Shirakami-Runtime-Integration` — provider/runtime adapters and interoperability contracts
4. `github-context-bridge-public` — public GitHub Context Bridge
5. `shirakami-ui-for-ai` — reusable UI/observation component

## Private set

- `Shirakami-Project` — integration/governance workspace
- `github-context-bridge` — bridge research
- `shirakami-research` — research and IP review
- `shirakami-os-lab` — experiments
- `shirakami-OS` — legacy history and current reference Runtime/Adapter implementation
- `shirakami-ai-governance` — governance/market experiments

## Runtime Integration boundary

`Shirakami-Runtime-Integration` is intended to become the neutral connection layer between Shirakami and replaceable AI/execution systems.

Examples:

- OpenAI / compatible APIs
- Gemini
- Claude
- Codex
- ECC
- local LLMs
- future runtimes

It should contain **how to connect**, not **which runtime is authoritative**.

The new repository is therefore a proposed destination, not yet a migration target. Existing Runtime/Adapter code in `shirakami-OS` remains untouched until a separate migration review.

## Not yet public

Concrete gadget/physical implementation details remain outside the public release path pending IP review.

## Migration policy

The first phase is deliberately non-destructive. Files are not deleted merely to make the tree look clean. Each future move should have its own PR and provenance note.
