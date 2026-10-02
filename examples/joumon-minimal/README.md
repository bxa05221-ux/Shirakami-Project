# JOUMON Minimal PoC

This directory contains a dependency-free reference fixture for the first JOUMON boundary test.

Files:

- `context.yaml` — shared Context
- `protocol.yaml` — shared Protocol
- `run.yaml` — two runtime results and their Evidence records

The fixture demonstrates:

```
Same Context
   |
 JOUMON
 /    \
A      B
|      |
EA     EB
 \    /
 Human Gate
```

No live provider is called and no credentials are required.

The fixture is illustrative until the executable test harness is added.
