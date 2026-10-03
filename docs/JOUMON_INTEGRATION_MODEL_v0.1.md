# JOUMON Integration Model v0.1

## Status

- status: conceptual-reference
- code_name: JOUMON
- scope: Shirakami multi-runtime integration
- publication_authorization: pending
- repository_creation_authorization: pending
- ip_review: pending
- human_gate: pending

## 1. Definition

**JOUMON** is the internal codename for the Shirakami multi-runtime integration model.

The model is designed to connect heterogeneous AI models, coding agents, agent harnesses, development platforms, OSS components, and local AI systems without making any one runtime canonical or authoritative.

JOUMON is an integration layer, not a new AI model.

## 2. English Expansion

**JOUMON**

**J**oint  
**O**pen  
**U**nified  
**M**ulti-runtime  
**O**rchestration  
**N**etwork

The expansion is a technical backronym for the codename. It does not claim that the historical Jōmon culture used or anticipated this technical architecture.

## 3. Conceptual Relationship

- **SHIRAKAMI** = forest / overall architecture and governance boundary
- **JOUMON** = cooperative multi-runtime integration model
- **Shirakami-Runtime-Integration** = proposed technical integration repository
- **shirakami-showcase** = proposed cooperative demonstration layer
- **Human Gate** = final human authority

A forest is not a single tree.

Accordingly, JOUMON does not seek to merge heterogeneous runtimes into one provider or one model. It provides boundaries through which they can coexist, interoperate, and remain replaceable.

## 4. Runtime Neutrality

Potentially connected runtimes include:

- OpenAI
- Gemini
- Claude
- Codex
- GitHub Copilot
- Copilot CLI
- GitHub Models
- ECC and other agent harnesses
- MCP-based agents
- local LLMs
- future AI agents and development platforms

These are examples of integration targets, not endorsements or canonical dependencies.

## 5. Core Flow

```text
Human Landscape
      |
Shirakami Context / Protocol
      |
    JOUMON
      |
Integration Adapter
      |
Model / Agent / Platform Runtime
      |
Observation / Evidence / AIwitness
      |
Human Gate
      |
Verification
```

The same Shirakami Context and Protocol should be capable of being executed through multiple replaceable runtimes.

## 6. Authority Boundary

JOUMON does not transfer decision authority to a model, agent, provider, platform, or OSS component.

The governing principle is:

> AI may move. Authority does not move.

Runtime execution may generate reasoning, simulation, code, observations, or other outputs. Human judgment remains the final authority within the Shirakami architecture.

## 7. Observation and Provenance

External runtimes are observable components, not authorities.

```text
Runtime
  |
Observation Adapter
  |
AgentActivity / Trace
  |
Evidence
  |
AIwitness
  |
Human Gate
```

For cooperative integration, upstream identity and provenance must remain distinguishable. At minimum, integrations should preserve:

- upstream repository
- author or project
- license
- pinned version or commit
- modification status
- Shirakami-authored integration code
- execution evidence where applicable

## 8. Integration Rules

1. Prefer adapters and connectors over copying complete upstream repositories.
2. Do not present upstream code as Shirakami-authored.
3. Do not imply endorsement or partnership without explicit authorization.
4. Keep credentials, private prompts, confidential provider material, and unreleased IP outside public integration artifacts.
5. Keep provider-specific implementation replaceable.
6. Keep Context, Protocol, Evidence, Provenance, Verification, AIwitness, and Human Gate semantics independent from any single runtime.
7. Treat reproducibility and observed execution as evidence, not as authority.

## 9. Initial Proof Target

The first technical proof should demonstrate runtime replacement rather than broad provider coverage.

```text
Same Context
   |
   +--> JOUMON --> Runtime A --> Evidence A
   |
   +--> JOUMON --> Runtime B --> Evidence B
```

The key observation is whether the Context, Protocol, Evidence, and Human Gate boundaries remain stable when the runtime changes.

## 10. Roadmap Position

JOUMON is introduced after the repository-boundary and dependency-inventory work.

Planned sequence:

1. Fix the repository boundary.
2. Define JOUMON.
3. Build a minimal multi-runtime PoC.
4. Add GitHub AI and agent-platform integrations.
5. Validate the third-party evaluator support protocol.
6. Validate Guide AI as a second domain.
7. Establish the cooperative showcase.
8. Connect ThreadRPG / Experience Feedback as an observation environment.
9. Reassess public repository boundaries.
10. Review the physical/gadget implementation separately after IP review.

## 11. Non-Goals

This document does not:

- claim patentability or novelty;
- authorize public release;
- create a repository;
- change repository visibility;
- authorize copying of third-party code;
- establish a preferred AI provider;
- transfer authority from humans to AI;
- define JOUMON as a historical claim about Jōmon culture.

## 12. Cultural Naming Note

The name **JOUMON** is inspired by the Jōmon cultural landscape of northern Japan and is used here as a project codename.

The project may draw conceptual inspiration from ideas of coexistence, exchange, and distributed human activity associated with archaeological interpretations of Jōmon societies, but this technical document does not make a historical claim that Jōmon society had this architecture or terminology.

---

**Related documents**

- `docs/SHIRAKAMI_FOREST_PRINCIPLE_v0.1.md`
- `docs/RUNTIME_INTEGRATION_INVENTORY_v0.1.md`
- `docs/RUNTIME_INTEGRATION_DEPENDENCY_MATRIX_v0.1.md`
- `docs/COOPERATIVE_SHOWCASE_SPEC_v0.1.md`
- `docs/COOPERATIVE_SHOWCASE_PROVENANCE_SCHEMA_v0.1.md`
- `docs/REPOSITORY_BOUNDARY_MAP.md`
