# JOUMON Minimal PoC — Executable Harness

This directory contains the first executable boundary test for JOUMON.

## Run

From this directory:

```text
python -m pytest -q
```

Or inspect the harness without pytest:

```text
python -c "from joumon_poc import run; print(run())"
```

## What is tested

- the same Context reaches multiple runtimes;
- the Protocol remains runtime-neutral;
- Evidence preserves runtime provenance;
- Evidence remains non-authoritative;
- Human Gate remains human;
- replacing one runtime with another does not change the authority boundary.

No live provider, network call, or credential is required.

## Architectural statement

**Same Context. Different Runtime. Same Authority Boundary.**

This is a boundary-preservation PoC, not a model-quality benchmark.
