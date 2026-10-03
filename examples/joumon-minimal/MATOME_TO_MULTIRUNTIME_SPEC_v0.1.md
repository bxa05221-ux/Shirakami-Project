# JOUMON Matome-to-MultiRuntime v0.1

status: experimental

## Complete PoC entry path

    Matome-shaped document
             |
             v
       Matome Loader
             |
             v
       Context + Protocol
             |
       +-----+-----+
       |           |
       v           v
   Runtime A   Runtime B
       |           |
       v           v
   Evidence A  Evidence B
       |           |
       +-----+-----+
             |
          Lineage

## Invariants

- One Matome entry point can feed multiple replaceable Runtime adapters.
- Runtime provenance remains distinct.
- Context and Protocol identity remain shared.
- Evidence remains non-authoritative.
- Human Gate remains outside Runtime execution.

## Scope

This is a deterministic adapter-injection PoC. The provider callables are test doubles unless explicitly replaced by an authenticated live provider integration.
