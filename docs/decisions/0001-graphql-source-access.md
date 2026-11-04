# ADR-0001: GraphQL as the source access interface

- Status: accepted
- Date: 2026-08-24 (ported from reference architecture v0.6.2)
- Satisfies: [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [D-09](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [GO: GraphQL as a selective query mechanism](https://ictu.github.io/GBO-GO/main/#graphql-als-selectief-bevragingsmechanisme)
- Deliberation: Reference architecture v0.6.2, decision 1, and its GraphQL + PBAC proposal (archived and unpublished)
- Implemented in: [services/graphql-server](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server), [services/brp-graphql-server](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server), [services/lvg-graphql-server](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/lvg-graphql-server)

## Context and problem statement

Data minimization (dataminimalisatie) requires a different set of fields
for each consent scope. With REST, each scope needs a separate endpoint or
separate filter parameters. Policies must then also state who can use
which filter. As a result, the API layer and the policy layer hold the
same logic twice.

## Decision

Bronhouders expose GraphQL endpoints. The selection set of the consumer is
the data minimization: the query names exactly the fields that the
consumer wants. The policy engine authorizes that query field by field.

Selectors that matter for authorization, such as the `belastingjaren` year
filter, must travel inside the query. Then the PDP can enforce them.

## Consequences

- The query is the authorization object. For more information, see
  [ADR-0009](0009-closed-world-rules.md) and
  [ADR-0013](0013-pdp-request-mapper.md).
- GraphQL runs over HTTP, so FSC proxies it unchanged
  ([ADR-0003](0003-fsc-connectivity.md)).
- GraphQL is not a recognized type of FDS data service (datadienst).
  [ADR-0025](0025-graphql-fds-datadienst.md) proposes to standardize it.
  The iWlz/nID production precedent supports the pattern.

## Traceability

- Requirements: [REQ-08](../requirements/authorization.md#req-08), [REQ-11](../requirements/authorization.md#req-11), [REQ-17](../requirements/authorization.md#req-17)
- Findings: none
- Open questions: [Q-11](../traceability/answered-questions.md#q-11) (answered), [Q-14](../traceability/open-questions.md#q-14) (open)
- Demo increments: [SL-03a](../traceability/increments.md#sl-03a) (done), [SL-03b](../traceability/increments.md#sl-03b) (done)
