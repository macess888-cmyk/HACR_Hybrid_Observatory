# Observability Path Discoverability

Observability Path Discoverability inspects whether reviewers can materially find the correct observability path across the repository.

The object is not documentation aesthetics.

The object is runtime review path reachability.

Primary question:

Can a reviewer locate the correct harness, note, metric, topology layer, coupling layer, or renderer artifact without practical traversal collapse?

Measured surfaces may include:

- index availability
- path depth
- filename clarity
- cross-layer references
- directory fragmentation
- route ambiguity
- recovery burden after wrong path selection

If observability path discoverability cannot be materially reconstructed:

UNKNOWN -> HOLD

If review paths become practically non-discoverable:

FAIL

If review paths remain materially discoverable:

PASS

Core locks:

- A file existing is not a reachable review path.
- Visibility is not reachability.
- Documentation presence is not traversal.
- UNKNOWN -> HOLD.