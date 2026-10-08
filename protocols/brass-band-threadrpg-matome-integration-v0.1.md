# Shirakami High School Brass Band — Foundation Integration

Reality–User World Clutch is the semantic foundation for the Shirakami High School Brass Band concept.

The application may present a character/world/story interface, but the runtime boundary remains Shirakami's:

- Reality is not User World.
- Story/role-play state is not Evidence.
- Character statements are not automatically user intent.
- Memory is time-indexed.
- Human decision authority remains outside the AI runtime.

## ThreadRPG connection

ThreadRPG is a presentation/interaction layer.

It consumes and emits explicit semantic objects rather than bypassing the Clutch boundary.

    User
      ↓
    ThreadRPG
      ↓
    SemanticObject
      ↓
    Reality–User World Clutch
      ↓
    Semantic Handoff
      ↓
    Human Gate / Verification

ThreadRPG may provide role, scene, thread state, anonymous/character perspective, response format, and narrative context.

ThreadRPG must not silently promote those fields to Evidence or user intent.

## Matome YAML Library connection

The Matome YAML Library is a semantic reference surface.

    Matome YAML Library
           ↓
    Matome Reference
           ↓
    Context / Protocol / Evidence boundary
           ↓
    ThreadRPG or other interface

A runtime may query the library for relevant meaning units, but a retrieved Matome is reference material, not an instruction with authority.

## Limited author dialogue

The library can expose a restricted author-dialogue capability.

The capability is intentionally asymmetric:

- read permitted Matome units
- ask questions against permitted Matome units
- return provenance with each answer
- distinguish library content from inference
- do not rewrite Matome content through ordinary dialogue
- do not grant repository write/merge/publish authority
- do not expose private Matome units without an explicit access boundary

The author dialogue endpoint is therefore a semantic query boundary, not an autonomous agent.

## Access model

    AUTHOR
      │
      ├── dialogue
      │      ↓
      │   Matome Query Gateway
      │      ↓
      │   permitted semantic units
      │
      └── explicit maintenance action
             ↓
          Human Gate
             ↓
          Repository change

A conversational answer must carry:

- source Matome IDs
- source version
- retrieval timestamp
- answer status
- uncertainty
- whether the statement is direct library content or inference

## Three-way separation

1. Reality: Evidence, environment, constraints, observations.
2. User World / Story World: Meaning, Dream, Presence, values, ThreadRPG state, character/world context.
3. Matome Library: Authored Shirakami knowledge and protocol meaning.

These surfaces may be connected, but must not be silently collapsed into one another.

## Key invariant

Reference != Authority

A Matome can explain how Shirakami works without thereby authorizing an action.

## Future adapter contract

A future adapter should expose:

- query_matome()
- get_matome_provenance()
- propose_threadrpg_context()
- build_semantic_handoff()
- request_human_gate()

It must not expose ordinary dialogue operations for:

- merge
- publish
- permission escalation
- policy override
- autonomous Matome mutation

This makes the Brass Band application a concrete consumer of the same Shirakami boundaries rather than a separate architecture.
