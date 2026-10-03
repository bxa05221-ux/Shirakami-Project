# Repository Boundary Map v0.3

This document defines the repository boundaries and the public/private/cooperative layers for the Shirakami project.

## Three-layer architecture

### Public

Public repositories contain **stable, reviewed artifacts intended for reuse**:

- `shirakami-model`
- `shirakami-specification`
- `Shirakami-Runtime-Integration`
- `github-context-bridge-public`
- `shirakami-ui-for-ai`

### Private development

The development environment remains deliberately closed:

- `Shirakami-Project`
- `github-context-bridge`
- `shirakami-research`
- `shirakami-os-lab`
- `shirakami-OS`
- `shirakami-ai-governance`

This boundary allows experiments, provider-specific testing, unreleased implementation, internal evaluation, and IP-sensitive material to mature before publication.

**Private status is a development-control boundary, not a guarantee of secrecy, confidentiality, or patent protection.** Publication and IP questions remain subject to separate review.

## Cooperative showcase

A proposed `shirakami-showcase` repository will demonstrate cooperation between Shirakami and external projects.

Its purpose is not to collect other projects into Shirakami or claim their work as Shirakami's own. It will show how independently maintained projects can be connected through Shirakami.

For each external project, the showcase should record:

- upstream repository
- author/project credit
- applicable license
- version or commit used
- modifications, if any
- Shirakami-authored adapter/integration
- execution evidence where appropriate
- provenance

The preferred integration pattern is:

```
External Project
      ↓
Adapter / Connector
      ↓
Shirakami Runtime Integration
      ↓
Context / Protocol
      ↓
Evidence / AIwitness
      ↓
Human Gate
```

External code should remain distinguishable from Shirakami-authored code. Whole-repository copying should not be the default.

The showcase must not imply endorsement, official partnership, or ownership by an upstream project without explicit authorization.

## Runtime Integration boundary

`Shirakami-Runtime-Integration` is the neutral connection layer between Shirakami and replaceable AI/execution systems.

Examples include:

- OpenAI / compatible APIs
- Gemini
- Claude
- Codex
- GitHub Copilot
- Copilot CLI
- GitHub Models
- ECC
- local LLMs
- future AI agents and development platforms

It should contain **how to connect**, not **which runtime is authoritative**.

The new repository is a proposed destination, not yet a migration target. Existing Runtime/Adapter code in `shirakami-OS` remains untouched until a separate migration review.

## Not yet public

Concrete gadget/physical implementation details remain outside the public release path pending IP review.

## Migration policy

The first phase is deliberately non-destructive. Files are not deleted merely to make the tree look clean. Each future move should have its own PR and provenance note.

## Publication gate

```
classify
   ↓
license_check
   ↓
ip_review
   ↓
human_gate
   ↓
release
```

When uncertain, hold publication.
