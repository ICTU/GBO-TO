# ADR-0025: GraphQL as a recognized FDS datadienst type

- Status: proposed
- Date: 2026-08-24
- Satisfies: [D-08](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [D-13](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [PSA: REST versus GraphQL noot](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
- Deliberation: reference architecture v0.6.2, gap 4 (archived and unpublished)
- Implemented in: not applicable (standardization action)

## Context and problem statement

FDS mandates the REST API Design Rules. GraphQL is not a recognized
datadienst type in FDS. The data access pillar of GBO
([ADR-0001](0001-graphql-source-access.md)) depends on GraphQL. For this
reason, GBO must bring the deviation to the standards gremia (pas toe of
leg uit).

## Proposed decision

GBO proposes GraphQL as an additional datadienst type through the FDS
and Forum Standaardisatie processes. The proposal includes a
Digikoppeling GraphQL profile. The proposal positions GraphQL as follows:

- GraphQL runs over FSC, and the transport does not change.
- The iWlz/nID production deployment and gbo-demo are the precedent.
- The AuthZEN mapping of the query structure to the authorization input
  is the enforcement story.

## Open points

These points are open:

- The owner and the timeline of the standardization submission.
- The scope of a Digikoppeling GraphQL profile (pagination, errors,
  introspection policy).

## Traceability

- Requirements: none directly. The data access pillar it supports is
  [ADR-0001](0001-graphql-source-access.md).
