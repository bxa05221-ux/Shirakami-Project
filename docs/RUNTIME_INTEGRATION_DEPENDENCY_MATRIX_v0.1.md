# Runtime Integration Dependency Matrix v0.1

Status: dependency review only. No files are moved, deleted, relicensed, or made public.

A migration candidate must be separable from Shirakami semantic authority, Context, Evidence, Trace, Human Gate, and core Runtime contracts.

## Findings

| Area | Assessment | Action |
|---|---|---|
| OpenAI backend | Provider-specific; depends on BackendResponse | Integration candidate |
| Real model adapter | Provider-neutral boundary | Keep canonical contract in Runtime |
| Provider transport | Provider-neutral contract | Keep canonical contract in Runtime |
| Async provider transport | Provider-neutral contract | Keep canonical contract in Runtime |
| GitHub client/auth | Provider/platform-specific | Integration candidates |
| GitHub Landscape adapters | Integration code crossing Evidence | Split interface before migration |
| GitHub repository observation | Read-only adapter | Integration candidate |
| Agent Activity | Provider-neutral observation schema | Keep in Runtime |
| Agent Activity trace/verification/evidence | Core provenance semantics | Keep in Runtime |
| Copilot activity hook | Platform-specific observation hook | Integration candidate |
| Copilot activity ingestion CLI | Thin platform adapter | Integration candidate |
| GitHub plugin adapter | Existing overlapping GitHub implementation | Consolidate boundary first |

## GitHub boundary

There are two GitHub-specific paths: `runtime/github_client.py` with Landscape adapters, and `plugins/adapters/github/github_adapter.py`.

Do not publish both as independent canonical implementations. Consolidate or explicitly classify one as compatibility/legacy before migration.

## Agent boundary

Copilot, Codex, ECC, and future agents should enter through platform-specific observation adapters:

```
External Agent
  -> platform observation adapter
  -> AgentActivity
  -> Trace / Verification / Evidence / AIwitness
  -> Human Gate
```

Agent Activity and its provenance pipeline are provider-neutral Shirakami semantics and should not be moved wholesale into Runtime Integration.

## Runtime integration split

```
Shirakami Runtime
  -> canonical ProviderRequest / ProviderTransport
  -> Runtime Integration
       -> OpenAI
       -> Gemini
       -> Claude
       -> Codex
       -> GitHub Copilot / Copilot SDK
       -> ECC
       -> local models
```

No provider becomes the canonical Runtime.

## Gate before migration

1. Confirm the public boundary.
2. Inspect imports and dependency graph.
3. Remove private deployment material.
4. Review third-party SDK licenses.
5. Review unreleased IP.
6. Human Gate.
7. Migrate one integration family at a time.
8. Run regression/interoperability tests.
9. Publish only reviewed material.

## Current conclusion

The dependency review supports creating `Shirakami-Runtime-Integration` as a neutral interoperability repository, but it does not yet authorize migration of the identified files.

Non-goals: no novelty or patentability claim, no provider endorsement, no authority transfer, no visibility change, and no destructive migration.
