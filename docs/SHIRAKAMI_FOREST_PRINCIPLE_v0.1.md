# Shirakami Forest Principle v0.1

## Status

Conceptual design principle.

This document does not authorize publication, repository creation, code migration, or any intellectual-property claim.

## 1. Principle

Shirakami is not a single AI model.

It is a structure in which heterogeneous AI models, agents, development platforms, and open-source components can coexist while remaining replaceable, observable, attributable, and subject to human authority.

> A forest is not a single tree.

## 2. Tree and Forest

Individual runtimes are treated as distinct components.

Examples include:

- OpenAI
- Gemini
- Claude
- Codex
- GitHub Copilot
- Copilot CLI
- GitHub Models
- ECC and other agent harnesses
- Local LLMs
- External open-source projects

Shirakami does not require these components to become identical.

Instead, Shirakami provides boundaries through which their execution can be connected to:

- Context
- Protocol
- Evidence
- Provenance
- Verification
- AIwitness
- Human Gate

## 3. No Canonical Tree

No provider or runtime becomes the authoritative center of Shirakami.

A runtime may be replaced without changing the human-authority boundary.

Therefore:

`Runtime A → Shirakami`

and

`Runtime B → Shirakami`

may execute the same conceptual Context/Protocol while preserving the same authority rules.

## 4. Provenance Is Part of the Forest

External projects remain identifiable as external projects.

When a project is integrated into a Shirakami showcase:

- upstream identity is preserved;
- author/project attribution is preserved;
- applicable license information is recorded;
- version or commit is pinned where practical;
- modifications are identified;
- Shirakami-authored integration code remains distinguishable.

Integration must not imply endorsement, partnership, ownership, or authorship without explicit authorization.

## 5. Observation Without Domination

Shirakami observes execution rather than granting authority to the runtime.

The intended observation path is:

`External Runtime → Observation Adapter → AgentActivity / Trace → Evidence → AIwitness → Human Gate`

Observation records what happened; they do not themselves authorize what should happen.

## 6. Forest Health

A healthy integration ecosystem should avoid:

- single-provider lock-in;
- hidden provenance;
- indistinguishable copied code;
- undocumented modifications;
- credentials entering source-controlled evidence;
- provider-specific authority assumptions;
- uncontrolled migration of experimental artifacts into public repositories.

The purpose is not to make every component equal.

The purpose is to make differences explicit while preserving interoperability.

## 7. Cooperative Showcase

The proposed `shirakami-showcase` repository should function as an integration forest rather than a clone collection.

Preferred pattern:

`Upstream Project → Adapter / Connector → Shirakami Context / Protocol → Execution → Evidence / Provenance`

Copying an entire upstream repository is not the default.

Reference, pinned dependency, adapter, connector, or other license-compatible integration should be preferred when technically sufficient.

## 8. Human Authority

The forest does not make decisions.

AI runtimes may reason, simulate, generate, execute within defined boundaries, or provide observations.

The final authority remains with the human-controlled gate.

> AI may move. Authority does not move.

## 9. Relation to the Shirakami Architecture

This principle is consistent with the Shirakami architecture:

`Landscape → Context → Protocol → Evidence → Runtime → Adapter → Backend → Human Gate → Verification`

The Forest Principle primarily describes the Runtime/Adapter ecosystem and its relationship to external projects.

It does not replace the normative architecture or its authority boundaries.
