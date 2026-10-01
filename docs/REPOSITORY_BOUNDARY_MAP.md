# Repository Boundary Map v0.1

This document defines the first-pass repository boundaries for the Shirakami project.

## Principle

The repository layout is itself a boundary:

- Public repositories contain reusable, reviewed software and specifications.
- Private repositories contain research, experiments, unreleased implementation, and IP candidates.
- New potentially protectable technical content is held for review before publication.
- Legacy repositories are preserved rather than destructively rewritten during the first phase.

## Proposed public-facing set

1. `shirakami-model` — core architecture and model documentation
2. `shirakami-specification` — normative contracts and specifications
3. `github-context-bridge-public` — public GitHub Context Bridge
4. `shirakami-ui-for-ai` — reusable UI/observation component

## Private set

- `Shirakami-Project` — integration/governance workspace
- `github-context-bridge` — bridge research
- `shirakami-research` — research and IP review
- `shirakami-os-lab` — experiments
- `shirakami-OS` — legacy history
- `shirakami-ai-governance` — governance/market experiments

## Not yet public

Concrete gadget/physical implementation details remain outside the public release path pending IP review.

## Migration policy

The first phase is deliberately non-destructive. Files are not deleted merely to make the tree look clean. Each future move should have its own PR and provenance note.
