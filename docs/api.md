# Local API and safe-change procedure

There is no HTTP or remote API. The application API is the Python module interface listed exhaustively in `contracts.md`; the user-facing boundary is a local Pygame window and event stream.

Authentication, authorization, rate limiting, version headers, error envelopes, OpenAPI/GraphQL/protobuf schemas, and deprecation windows are N/A for the current offline prototype.

Before changing an interface: check `contracts.md` and imports/tests; preserve return types and user-facing error strings unless intentionally changing them; preserve supported legacy JSON shapes; add focused tests; run the full suite; and update `contracts.md` plus this narrative in the same change. A future remote API requires an ADR, schema, security model, compatibility policy, and full playbook review.

## Update this document when

Update when public Python interfaces, screen events, data loading, persistence, or a remote protocol is added or changed.
