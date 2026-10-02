# JOUMON Live Provider Matrix v0.1

status: experimental

The matrix is a testing plan, not a claim that all providers are already connected.

| Adapter slot | Provider-specific SDK | JOUMON contract | Evidence | Human Gate |
|---|---|---|---|---|
| Runtime-1 | external | shared | shared | shared |
| Runtime-2 | external | shared | shared | shared |
| Runtime-3 | external | shared | shared | shared |
| Runtime-4 | external | shared | shared | shared |
| Runtime-5 | external | shared | shared | shared |
| Runtime-6 | external | shared | shared | shared |
| Runtime-7 | external | shared | shared | shared |
| Runtime-8 | external | shared | shared | shared |
| Runtime-9 | external | shared | shared | shared |

## Acceptance criteria

A provider adapter is accepted only if it can:

1. consume Context + Protocol without changing their semantics;
2. return an observation through the common RuntimeResult boundary;
3. produce Unified Evidence with provider/runtime provenance;
4. produce Lineage;
5. participate in Semantic Handoff without transferring authority;
6. reach Human Gate without bypassing it.

No provider is assumed to be equivalent in capability or output quality. The matrix tests interoperability, not model ranking.
