# Cooperative Showcase Specification v0.1

## Purpose

`shirakami-showcase` is a proposed public repository for demonstrating cooperative integration between Shirakami and independently maintained external projects.

It is **not** a repository for claiming, absorbing, or rebranding upstream work.

## Core principle

> Respect the upstream project as an independent work while making the Shirakami integration boundary observable and reproducible.

## Required provenance

Each showcased integration should record:

- upstream repository
- project/author credit
- license
- version or commit
- modification status
- Shirakami-authored integration code
- execution evidence, where applicable

## Preferred structure

```
Upstream Project
      ↓
Adapter / Connector
      ↓
Shirakami-Runtime-Integration
      ↓
Context / Protocol
      ↓
Evidence / AIwitness
      ↓
Human Gate
```

## Cooperation rules

1. Do not copy an entire upstream repository unless its license and purpose explicitly justify that approach.
2. Prefer adapters, connectors, references, and pinned upstream versions.
3. Keep upstream code distinguishable from Shirakami-authored code.
4. Preserve required copyright and license notices.
5. Do not imply endorsement, official partnership, or ownership without authorization.
6. Do not place credentials, private prompts, confidential provider material, or unreleased IP in the showcase.
7. Record enough provenance to reproduce which upstream artifact was used.

## Licensing

The license of each external component is reviewed individually. A Shirakami-authored adapter may use the intended Shirakami license only when its own licensing conditions permit it.

This specification does not make any determination about third-party license compatibility.

## Initial candidate integrations

Candidate categories include:

- AI model/API runtimes
- coding agents
- GitHub Copilot / Copilot CLI / GitHub Models
- agent harnesses such as ECC
- local LLM runtimes
- GitHub-based tools and repositories

Candidates remain subject to license, dependency, IP, and publication review.

## Status

This is a design specification only. It does not create the repository, migrate code, change repository visibility, or authorize publication.
