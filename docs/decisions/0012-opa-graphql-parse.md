# ADR-0012: Query AST inspection with OPA's graphql.parse_query

- Status: superseded by [ADR-0013](0013-pdp-request-mapper.md)
- Date: 2026-08-24 (ported from reference architecture v0.6.2)
- Satisfies: [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: Reference architecture v0.6.2, component architecture "GraphQL schema registry and scope-driven field authorization", and its GraphQL + PBAC proposal (archived and unpublished)
- Implemented in: superseded before implementation

## Context and problem statement

For authorization per field, the PDP must read the structure of the
incoming GraphQL query, in addition to its metadata.

## Decision (superseded)

Rego parses the query with the built-in OPA function
`graphql.parse_query()`. The policy code then walks the AST. This follows
the nID/iWlz production pattern.

## Why it was superseded

If Rego walks a raw AST, the parsing mechanics go into every rule. Rego
also cannot resolve parent types, verify consent proofs, or pseudonymize
identifiers.

The implemented design moves the request preparation into a mapper inside
the PDP service, before policy evaluation. The rules then use clean facts
for each field. For this design, see [ADR-0013](0013-pdp-request-mapper.md).
The intent stays the same: the query is the authorization object.

## Traceability

- Requirements: [REQ-17](../requirements/authorization.md#req-17)
- Findings: [F-25](../traceability/findings-closed.md#f-25) (closed)
- Open questions: [Q-14](../traceability/open-questions.md#q-14) (open)
- Demo increments: [SL-03a](../traceability/increments.md#sl-03a) (done)
