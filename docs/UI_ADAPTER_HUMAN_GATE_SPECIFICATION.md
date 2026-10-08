# UI / Adapter Human Gate Boundary v0.1

The UI and adapter are transport/presentation layers. They may transmit a human interaction, but they must not manufacture authority.

A decision may cross the boundary only when the UI event explicitly represents a human interaction and matches the decision exactly on Decision ID, Approval ID, Context, Evidence, Protocol, and Proposal.

Synthetic or runtime-generated UI events are rejected. A non-human actor cannot claim human approval. An action/decision mismatch is rejected.

The boundary prevents this collapse:

`runtime -> UI -> fake click -> human approval -> execution`

into the valid path:

`runtime proposal -> genuine human interaction -> bound human decision -> Human Gate`.

This is structural protection; device/user authentication is a separate layer.
