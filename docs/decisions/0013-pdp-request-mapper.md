# ADR-0013: GraphQL request mapping in the PDP ahead of policy evaluation

- Status: accepted
- Date: 2026-08-24 (updated 2026-11-02: the mapper only maps)
- Satisfies: [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
- Supersedes: [ADR-0012](0012-opa-graphql-parse.md)
- Deliberation: [REQ-17](../requirements/authorization.md#req-17), [REQ-42](../requirements/authorization.md#req-42), demo [#364](https://github.com/ICTU/GBO-demo/issues/364), [#330](https://github.com/ICTU/GBO-demo/issues/330), [PR #370](https://github.com/ICTU/GBO-demo/pull/370), [PR #371](https://github.com/ICTU/GBO-demo/pull/371), [PR #482](https://github.com/ICTU/GBO-demo/pull/482), [FTV GraphQL profile](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/ftv-graphql-profile.md)
- Implemented in: [mapper/ftvgraphql.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/mapper/ftvgraphql.go#L1-L13) (OpenFTV adapter), [services/ftv-graphql-mapper](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper) (profile mapper), [schemas/pdp-mirror](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/pdp-mirror) (schema per FSC service), [graphql_schemas.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/graphql_schemas.rego) (schema pins), [scripts/check-schema-drift.sh](https://github.com/ICTU/GBO-demo/blob/v0.9.0/scripts/check-schema-drift.sh)

## Context and problem statement

Rules need clean, typed facts about the request instead of a raw query
string. These facts are the fields, with their parent types and with their
arguments as the source executes them.

The PEP passes the raw body unchanged
([ADR-0002](0002-opa-rego-authzen.md)). So a component on the PDP side
must turn the body into a field list. That list must be complete. If it is
not complete, the PDP denies the request
([REQ-17](../requirements/authorization.md#req-17)).

## Decision

A request mapper inside the OpenFTV PDP implements the mapping function of
the FTV GraphQL profile (`ftv-graphql/0.1`) and nothing else. The mapper
does these things:

- It parses the GraphQL body and builds the field list. The parent type of
  each field comes from the bundled schema of the FSC service of the
  request. The arguments are as the source executes them.
- It accepts only a query operation. A mutation or subscription gives
  `OPERATION_NOT_SUPPORTED`.
- It enforces these limits:
    - body: 1 MiB
    - nesting depth: 64
    - fragment definitions: 100
    - selection depth: 64
    - field records: 1000
    - aliased selections: 100
    - validation time: 1 second
- If a step fails, it marks the request `COVERAGE_UNVERIFIABLE` with a
  subcode (for example `PARSE_ERROR`, `LIMIT_EXCEEDED`). The engine denies
  the request.

The mapper does not verify the consent proof. It does not call BSNk, does
not pseudonymize, and reads no flow. The policy verifies the consent
itself ([ADR-0032](0032-consent-proof.md)). The regime follows from the
evidence ([ADR-0031](0031-regime-from-evidence.md)).

The profile mapper is a separate Go module. A thin adapter connects it to
OpenFTV.

## Consequences

- Rules stay declarative. Parsing happens once, in one place, in tested Go
  code. The conformance vectors of the profile run as tests.
- The PDP loads one schema for each FSC service. The policy bundle pins
  the digest of each schema and denies a schema that is not pinned
  (`CONFIG_ERROR SCHEMA_MISMATCH`). A CI job checks for drift between the
  pinned schema and the schema that the source executes.
- The source gateway accepts only the request shape that the PDP evaluated
  ([ADR-0033](0033-gateway-decrypts-after-allow.md)).
- The mapper is a patch on OpenFTV v0.1.0. The patch stays until the
  upstream project includes the profile mapper
  ([#331](https://github.com/ICTU/GBO-demo/issues/331)). For more
  information, see [Risks and technical debt](../risks.md).
- The mapper does not pseudonymize any more. So the EUDI and ASI routes
  put the plain BSN into the PDP input
  ([ADR-0043](0043-identifiers-out-of-pdp-input.md), proposed).

## Traceability

- Requirements: [REQ-17](../requirements/authorization.md#req-17), [REQ-42](../requirements/authorization.md#req-42), [REQ-18](../requirements/authorization.md#req-18), [REQ-60](../requirements/logging-audit.md#req-60)
- Findings: [F-25](../traceability/findings-closed.md#f-25) (closed), [F-54](../traceability/findings.md#f-54) (open)
- Open questions: [Q-14](../traceability/open-questions.md#q-14) (open)
- Demo increments: [SL-03a](../traceability/increments.md#sl-03a) (done), [SL-18](../traceability/increments.md#sl-18) (done), [SL-31](../traceability/increments.md#sl-31) (done)
