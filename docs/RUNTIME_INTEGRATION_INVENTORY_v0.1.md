# Shirakami-OS Runtime / Integration Inventory v0.1

Status: inventory only — no files are moved, deleted, or relicensed by this document.

## 1. Boundary

The proposed `Shirakami-Runtime-Integration` repository is a neutral interoperability layer for replaceable AI models, coding agents, agent harnesses, and development platforms.

It should contain connection contracts and provider/platform-specific integration code when that code is intentionally separated from Shirakami Runtime Core.

It must not become the canonical home of Shirakami authority, Human Gate semantics, normative protocol definitions, or provider credentials.

The existing `shirakami-OS` repository remains the current Runtime/Adapter implementation home until an explicit migration is reviewed and merged.

## 2. Classification

| Area | Current location | Classification | Migration decision |
|---|---|---|---|
| Runtime core | `runtime/` | Runtime Core candidate | Keep in `shirakami-OS` |
| Provider-neutral transport | `runtime/provider_transport.py`, `runtime/async_provider_transport.py` | Integration/Core boundary | Review before any split |
| OpenAI-specific backend | `runtime/openai_backend.py` | Runtime Integration candidate | Candidate for new repo |
| Real-model adapter | `runtime/real_model_adapter.py` | Integration candidate | Candidate for new repo |
| GitHub client/auth | `runtime/github_client.py`, `runtime/github_auth.py` | GitHub Integration candidate | Candidate for new repo; credentials stay out |
| GitHub Landscape | `runtime/github_landscape_adapter.py`, `runtime/github_repository_landscape.py`, `runtime/operational_github_read.py`, `runtime/live_github_probe.py` | GitHub Integration candidate | Candidate; preserve Runtime boundary |
| GitHub protocol loading | `runtime/github_protocol_loader.py` | Integration/Core boundary | Review before split |
| Agent activity / Copilot observation | `runtime/agent_activity*.py`, Copilot tests/hooks | Agent-platform Integration candidate | Candidate for new repo |
| Protocol execution | `runtime/protocol_*.py`, `runtime/approved_protocol_pipeline.py` | Runtime Core / Protocol boundary | Keep; specs belong in specification repo |
| Context / handoff | `runtime/context_bundle.py`, `runtime/context_routing.py`, handoff/lineage modules | Runtime Core | Keep |
| Evidence / verification | `runtime/evidence*.py`, replay/verification modules | Runtime Core | Keep |
| Human Gate / approval | `runtime/human_gate.py`, approval modules | Runtime Core | Keep |
| Operation execution | `runtime/operation_*.py`, execution modules | Runtime Core | Keep unless an external executor boundary is later defined |
| AIwitness | `aiwitness/` | Evidence / observation boundary | Keep; separate only after explicit boundary review |
| Reviewer | `reviewer/` | Reviewer/Evidence layer | Keep; not Runtime Integration |
| Protocols | `protocols/` | Normative/application protocol | Candidate for specification/application repos after review |
| Specs | `spec/` | Specification | Candidate for `shirakami-specification` after review |
| Examples | `examples/` | Public examples / integration examples | Split by dependency and publication review |
| Experiments | `experiments/` | Experimental evidence | Keep/private until reviewed |
| Tests | `tests/` | Evidence / regression | Keep with implementation initially; migrate with code only when history can be preserved |
| CI workflows | `.github/workflows/` | Repository execution/evidence | Keep with owning implementation unless provider-specific |
| Copilot experiments | `docs/experiments/GitHub_Copilot_*.md`, `experiments/copilot_activity_hook.py`, related tests | Agent-platform Integration candidate | Review for public release |
| OPPAI | `runtime/oppai_*.py`, related API/examples/tests | Runtime Integration candidate | Review whether OPPAI is a backend/runtime or remains internal |
| Application work | `works/`, `products/`, `community/`, `apps/` | Application/product | Do not move into Integration |

## 3. Runtime Integration candidates

Initial high-confidence candidates are:

- `runtime/openai_backend.py`
- `runtime/real_model_adapter.py`
- `runtime/provider_transport.py`
- `runtime/async_provider_transport.py`
- `runtime/github_client.py`
- `runtime/github_auth.py`
- `runtime/github_landscape_adapter.py`
- `runtime/github_repository_landscape.py`
- `runtime/live_github_probe.py`
- `runtime/operational_github_read.py`
- `runtime/agent_activity.py`
- `runtime/agent_activity_ingestor.py`
- `runtime/agent_activity_trace.py`
- `runtime/agent_activity_evidence.py`
- `runtime/agent_activity_evidence_closure.py`
- `runtime/agent_activity_verification.py`
- `experiments/copilot_activity_hook.py`
- `experiments/ingest_copilot_activity.py`
- `docs/experiments/GitHub_Copilot_SDK_Async_Boundary_v0.1.md`
- `docs/experiments/GitHub_Copilot_SDK_Provider_Transport_Contract_v0.1.md`

These are candidates, not an authorization to publish or move them.

## 4. Keep in Runtime Core

The following conceptual groups remain canonical in `shirakami-OS`:

- Context bundle and routing
- Protocol loading/registry where implementation is required
- Execution request/planning/execution boundaries
- Evidence storage, lineage, replay, and verification
- Human Gate and approval envelope
- Runtime loop and state continuity
- Core adapter contract
- Provider-neutral interfaces when they are part of the Runtime contract rather than a provider implementation

## 5. GitHub / Copilot boundary

GitHub itself is both an external landscape and an execution platform. Therefore the integration boundary is:

`GitHub / Copilot / Copilot CLI / GitHub Models / external agents`
→ integration adapter
→ Shirakami Context / Protocol
→ Runtime
→ Evidence / AIwitness
→ Human Gate

GitHub-specific credentials, private prompts, private repositories, confidential provider material, and unreleased IP are never part of a public integration repository.

Copilot activity is treated as observable execution evidence, not as authoritative Shirakami policy.

## 6. Tests

Tests should normally travel with the implementation they verify.

Before migration, classify each test as:

1. Runtime Core regression
2. Provider/platform integration test
3. Contract/interoperability test
4. Evidence/replay test
5. Application experiment

Do not bulk-move the entire `tests/` directory.

## 7. Migration sequence

1. Inventory — complete by this document.
2. Identify high-confidence Integration candidates.
3. Inspect imports/dependencies for each candidate.
4. Define public Integration contracts.
5. Check license/IP/publication status.
6. Create the new repository only when the repository boundary is approved.
7. Move one integration family at a time, preserving history where practical.
8. Run regression and interoperability tests.
9. Human Gate.
10. Publish only reviewed material.

## 8. Explicit non-goals

This inventory does not:

- declare patentability;
- declare novelty;
- authorize public release;
- change repository visibility;
- delete historical implementation;
- make any AI provider canonical;
- move Human Gate authority into an AI provider;
- treat Copilot, Codex, ECC, Gemini, Claude, OpenAI, or any other runtime as a Shirakami authority.

## 9. Target architecture

`Human Landscape`
→ `Shirakami Context / Protocol`
→ `Runtime Integration`
→ `Model / Agent / Platform Runtime`
→ `Observation / Evidence / AIwitness`
→ `Experience Feedback`
→ `Human Gate`

The same Shirakami Context may therefore be executed through multiple replaceable runtimes without changing who holds decision authority.
