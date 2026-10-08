# ThreadRPG → Shirakami Model → Shirakami OS: Origin and Abstraction Lineage v0.1

Status: research record / bounded architecture history
Date: 2026-10-08

## 1. Purpose

This document records the current evidence for the development lineage:

ThreadRPG → Shirakami Model → Shirakami Architecture → Shirakami OS

The purpose is not to claim that every later architectural component was explicitly designed inside ThreadRPG. The purpose is to distinguish:

- concepts first demonstrated or discovered through ThreadRPG;
- concepts subsequently generalized into the Shirakami Model;
- architectural boundaries later made explicit in Shirakami Architecture;
- implementation mechanisms subsequently built in Shirakami OS.

This document therefore treats ThreadRPG as an origin / discovery system, not merely as an application to be integrated into an already-existing OS.

## 2. Primary conclusion

The strongest current reading of the repository and published development record is:

> ThreadRPG is the experimental origin through which the central Shirakami Model pattern was discovered and articulated.

The later Shirakami OS is an abstraction and implementation of principles that became visible through that experiment.

The correct direction of interpretation is therefore:

```
ThreadRPG
  ↓
multi-view observation
  ↓
human Landscape changes
  ↓
state/context must survive between observations
  ↓
Matome YAML / handoff
  ↓
Shirakami Model
  ↓
generalization beyond threads
  ↓
Landscape / Evidence / Protocol / Runtime
  ↓
Shirakami Architecture
  ↓
Runtime / Adapter / API / Human Gate / Verification
  ↓
Shirakami OS
```

This reverses the weaker interpretation that ThreadRPG is simply a product feature waiting to be re-integrated into Shirakami OS.

## 3. Documentary evidence

### 3.1 Published ThreadRPG description

The 2026-08-24 publication explicitly describes ThreadRPG as arising from the observation that a good anonymous-board thread can cause the thread starter's own thinking to become organized through diverse responses.

It then defines ThreadRPG as multiple threads observing the same Human Landscape from different viewpoints, with the resulting observations returning to Landscape and causing Landscape Change.

The same publication explicitly states:

- Shirakami Model = what is aimed for;
- Protocol = how it is observed;
- Shirakami OS = how it is executed;
- ThreadRPG = the first experiment / public gateway.

Source:
https://note.com/kuromoka_kona/n/n04bec4c08a0f

This is direct evidence that ThreadRPG was positioned as an experimental realization of the Shirakami Model, not merely as a later application of an independently completed OS.

### 3.2 Matome / context continuity

The same publication describes Matome YAML as the intermediate representation used to pass the observed state to the next observation, preserving:

- state;
- observation;
- interpretation;
- uncertainty;
- unresolved items;
- next observation.

This is structurally continuous with the later Semantic Handoff concern: preserve meaning and provenance across changes in runtime, model, or observation.

### 3.3 Earlier development account

The 2026-09-07 development account describes the path from a practical YAML state/context mechanism to the discovery of Thread format as a useful way to expose multiple AI-generated viewpoints, followed by the naming of ThreadRPG as a protocol.

Source:
https://note.com/kuromoka_kona/n/ndf1ad4df334c

This is important because it shows that the thread mechanism and externalized state/context were discovered through practical experimentation rather than introduced as implementation details of a pre-existing OS specification.

## 4. Repository evidence

The historical Shirakami OS repository contains a substantial ThreadRPG body of work.

At commit d7c585f8245462198a501bc80723e7af4edae457, the repository contains:

- protocols/thread-rpg-v1.2.1.yaml
- docs/threadrpg-reintegration-draft-0.1.md
- docs/audits/threadrpg-consistency-audit-v0.1.md
- docs/protocols/ThreadRPG_Protocol_Generation_Policy_v0.1.md
- protocol-system index entries
- AATS-related runtime/test references
- architecture and protocol audit references

The canonical ThreadRPG protocol artifact defines it as an application-level protocol, explicitly keeping character/domain semantics outside the Runtime kernel.

The reintegration draft is especially significant: it defines ThreadRPG as a multi-view observation / conference / compression protocol family and explicitly connects:

Landscape → Perspective / Thread → Observation → Evidence → Landscape.

That document was added on 2026-08-24.

## 5. Abstraction map

| ThreadRPG-origin concept | Later Shirakami abstraction | Evidence status |
|---|---|---|
| Human brings a Landscape | Landscape First / canonical Landscape | Direct conceptual continuity |
| Multiple threads see the same Landscape differently | Multiple observations / projections / replaceable runtimes | Strong continuity |
| Thread is a viewpoint, not necessarily a personality | Perspective / renderer separation | Explicit in reintegration draft |
| Observation rather than answer generation | Observation boundary | Later Runtime implementation |
| Differences may remain unresolved | Evidence + uncertainty preservation | Explicit in policy and architecture |
| State must survive to the next observation | Matome YAML → Semantic Handoff | Strong conceptual continuity |
| Observation results return to Landscape | Evidence → Landscape / canonical promotion | Later Runtime implementation |
| Human's Landscape changes | Human-authoritative state transition | Later formalized by Human Gate |
| Thread must not become authority | AI non-authority | Explicit continuity |
| Thread rendering is presentation | Renderer / Projection separation | Later formalized |
| Re-observation closes the loop | Verification / observation loop | Later formalized |
| Multiple AI/model implementations can participate | Runtime / Adapter replaceability | Later generalized |

## 6. What was generalized

The central generalization was not "ThreadRPG → another chat UI."

It was:

### From conversation threads

```
Human Landscape
→ Thread
→ Observation
→ different viewpoints
→ Landscape Change
→ re-observation
```

### To a model-independent runtime principle

```
Reality
→ Observation
→ Model Analysis
→ Proposal
→ Human Gate
→ Landscape
→ Projection
→ Renderer
→ User
```

The later architecture therefore removes ThreadRPG-specific semantics while retaining the underlying authority and state-transition pattern.

This is why the current architecture can be model-independent while ThreadRPG remains one concrete expression of the original pattern.

## 7. Human Gate as a later explicit formalization

ThreadRPG's policy already contains the essential rule:

- viewpoints are non-authoritative;
- discussion is not authorization;
- generated candidates require human review;
- unresolved authority must stop the process;
- final responsibility remains human.

The current Shirakami Architecture makes that implicit rule explicit as a system boundary:

```
Proposal
   ↓
Human Gate
   ↓
accepted canonical Landscape
```

The current Strategic Human Gate API further exposes this boundary without granting decision or execution authority to AI.

Therefore Human Gate should not be described as an unrelated later safety feature. It is a formalization of the human-authority property already present in the ThreadRPG design philosophy.

## 8. AIwitness / Evidence as a later formalization

ThreadRPG already requires the distinction between:

- observation;
- interpretation;
- proposal;
- decision;
- uncertainty;
- provenance.

The current AIwitness boundary formalizes the corresponding evidence/provenance discipline:

- trace identity;
- execution identity;
- handoff identity;
- evidence identity;
- verification status;
- explicit non-propagation of authority.

This is a generalization from "what happened in the thread?" to "what happened in an AI-mediated execution path?"

## 9. What should NOT be claimed

The following claims are not established by this record:

1. Every current Shirakami component was directly invented inside ThreadRPG.
2. ThreadRPG itself is equivalent to the current Shirakami Runtime.
3. The old AATS execution path is already the canonical ThreadRPG implementation.
4. Matome API v3.2 is a normative Shirakami Foundation specification.
5. ThreadRPG must be moved into the Runtime kernel.
6. Perspective, Renderer, or Conference already have final normative schemas.

These remain separate implementation/design questions.

## 10. Architectural consequence

The ThreadRPG question should therefore be reframed.

Previous framing:

> How do we integrate ThreadRPG into Shirakami OS?

Corrected framing:

> Which principles discovered through ThreadRPG became Shirakami Model invariants, and which of those invariants are now implemented and verified by Shirakami OS?

This changes the next engineering task from "port ThreadRPG" to "trace and verify the abstraction."

## 11. Next bounded milestone

The next milestone should be:

**threadrpg-derived-core-mapping**

Acceptance criteria:

1. Identify the minimum set of ThreadRPG-origin invariants.
2. Map each invariant to the current Shirakami boundary.
3. Mark each mapping as implemented, documented-only, or unverified.
4. Do not add a Runtime layer solely for historical compatibility.
5. Do not reopen completed API/Human Gate/verification milestones.
6. Only after the mapping is complete decide whether a minimal ThreadRPG adapter is technically necessary.

## 12. Current confidence

- ThreadRPG predates and materially informs the published Shirakami Model: **high confidence**.
- Matome/context continuity from ThreadRPG into later handoff architecture: **high confidence**.
- Human-authority principle is continuous from ThreadRPG policy into Human Gate: **high confidence**.
- Every current Runtime component directly derives from ThreadRPG: **not established**.
- Old AATS is the canonical current ThreadRPG runtime: **not established**.

The historical relationship is therefore strong enough to guide architecture and documentation, while remaining careful about claims of direct implementation ancestry.


## 13. Implementation-level mapping from the historical runtime

A second pass over the historical repository shows that the lineage is not only conceptual. Several ThreadRPG-shaped operations were actually exercised in the old Runtime.

At commit `d7c585f8245462198a501bc80723e7af4edae457`, the AATS Wayfinding path is documented and tested as:

```
AATS → Thread → Renzan → Kasen → Landscape → Small Step
     → Transition → Evidence → Landscape re-observation
```

The repository describes:

- `Renzan` as collecting Thread posts as separate observable viewpoints, without interpreting them;
- `Kasen` as a human-facing re-expression boundary that preserves the viewpoints;
- Landscape as the state being observed;
- Evidence as the record of observable transition;
- re-observation as the loop back into Landscape.

This is a concrete implementation specimen of the earlier ThreadRPG pattern, although it is not evidence that AATS is the canonical or only implementation of ThreadRPG.

### 13.1 Mapping status

| Origin invariant | Historical implementation evidence | Current Shirakami boundary | Status |
|---|---|---|---|
| Same Landscape, multiple viewpoints | AATS Thread + Renzan | Landscape / observation boundary | **implemented historically; generalized current boundary** |
| Viewpoints remain distinguishable | Renzan collects posts without interpretation | Observation / Evidence separation | **implemented** |
| Human-facing synthesis is separate from observation | Kasen re-expression boundary | Renderer / Projection separation | **implemented as boundary** |
| Observation does not itself authorize execution | Small Step selection described as external policy boundary | Human Gate / authority chain | **implemented and strengthened** |
| Observable transition is recorded | AATS → Transition → Evidence | Evidence / AIwitness | **implemented and generalized** |
| Evidence returns to Landscape | Re-observation cycle + later explicit Evidence → Landscape boundary | Landscape projection | **implemented and verified in later Runtime work** |
| Context/state survives between observations | Thread / Landscape state in AATS; Matome YAML in ThreadRPG protocol | Semantic Handoff | **conceptually strong; exact schema lineage requires further mapping** |
| Disagreement / plurality is preserved | Thread posts remain separate viewpoints | Observation plurality / branch preservation | **documented and partially implemented; current canonical schema not yet fixed** |
| Human remains final authority | ThreadRPG policy + external Small Step boundary | Strategic Human Gate | **implemented and verified** |
| Model/backend is replaceable | AATS wayfinding notes backend choice remains replaceable | Runtime / Adapter boundary | **implemented and verified** |
| Re-observation closes the loop | AATS wayfinding cycle | Verification / Landscape loop | **implemented and verified** |

### 13.2 Important correction

The old AATS path is therefore best understood as a **historical implementation specimen** showing how ThreadRPG-derived ideas were exercised in Runtime.

It should not be promoted automatically to:

> "the ThreadRPG Runtime"

because the old ThreadRPG consistency audit explicitly found unresolved questions around Human Gate placement, execution authorization semantics, and the exact relationship between AATS and the proposed ThreadRPG reintegration cycle.

That distinction is important: the implementation evidence strengthens the lineage claim without collapsing historical experiments into today's normative architecture.

## 14. The strongest surviving invariant

Across the documents and implementation experiments, the most persistent invariant is not "thread."

It is:

> **A human Landscape is observed from multiple non-authoritative perspectives; observations remain distinguishable and uncertain; observable transitions are recorded; the resulting state can be observed again; final authority remains human.**

This invariant survives even when:

- Thread becomes a generic Perspective;
- the renderer changes;
- the AI model changes;
- the Runtime changes;
- the transport becomes HTTP;
- the observation becomes an API operation;
- Evidence becomes provider-neutral AIwitness data.

That is the strongest evidence that ThreadRPG was the **discovery mechanism**, while Shirakami Architecture is the **generalized architecture**.

## 15. Mapping completion boundary

This mapping is complete enough to establish the historical-to-current correspondence without requiring a new ThreadRPG Runtime implementation.

Remaining uncertainty is deliberately isolated to three questions:

1. the exact canonical Semantic Handoff schema inherited from Matome YAML;
2. the minimum normative representation of Perspective / plurality;
3. whether a dedicated ThreadRPG adapter provides enough practical value to justify implementation.

Those are new design questions, not missing prerequisites for the existing Shirakami core.

