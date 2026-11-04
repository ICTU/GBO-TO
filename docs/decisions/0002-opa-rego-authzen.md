# ADR-0002: OPA/Rego in OpenFTV, the FSC Inway as PEP, AuthZEN with the FTV GraphQL profile

- Status: accepted
- Date: 2026-08-24 (updated 2026-11-02: includes the decision "the FSC Inway is the PEP")
- Satisfies: [S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie), [P-09](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [GO: consent and legal basis as an enforceable authorization mechanism](https://ictu.github.io/GBO-GO/main/#toestemming-en-grondslag-als-afdwingbaar-autorisatiemechanisme)
- Deliberation: Reference architecture v0.6.2, authorization models analysis (archived and unpublished), [F-35](../traceability/findings-closed.md#f-35), [Q-16](../traceability/answered-questions.md#q-16), demo [PR #60](https://github.com/ICTU/GBO-demo/pull/60), [PR #482](https://github.com/ICTU/GBO-demo/pull/482), [PR #337](https://github.com/ICTU/GBO-demo/pull/337)
- Implemented in: [fsc-infra/docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L769-L775) (Inway AuthZEN plugin, with body), [services/openftv-pdp/Dockerfile](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/Dockerfile#L3-L9) (OpenFTV v0.1.0), [mapper/ftvgraphql.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/mapper/ftvgraphql.go#L1-L13), [services/ftv-graphql-mapper](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper), [docs/ftv-graphql-profile.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/ftv-graphql-profile.md), [policies/](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies)

## Context and problem statement

GBO needs one policy engine and one PEP-PDP protocol for all routes.
Then the authorization logic is in policy and not in application code.

Every source also needs an enforcement point in front of it. The interface
of that point is the same at every source, so bronhouders must know it.

## Decision

The PDP is OpenFTV (Federatieve Toegangsverlening) release v0.1.0 with
embedded OPA/Rego. The same PDP does two jobs:

- It evaluates data requests. FSC Inways call it for these.
- It decides on contract acceptance. FSC Managers call it for these
  ([ADR-0015](0015-contract-acceptance-by-policy.md)).

The FSC Inway of the source is the PEP. There is no separate PEP service.
The AuthZEN plugin of the Inway sends every request to the PDP as an
AuthZEN question, with the request body (`AUTHZEN_WITH_BODY=true`). Then
the Inway enforces the answer.

The PEP-PDP interface is OpenID AuthZEN 1.0
(`POST /authzen/v1/evaluation`). For GraphQL, the request follows the FTV
GraphQL profile for AuthZEN (`ftv-graphql/0.1`). The PEP passes the raw
body unchanged and never parses it
([REQ-42](../requirements/authorization.md#req-42)). The PDP side builds
the field list ([ADR-0013](0013-pdp-request-mapper.md)).

## Considered options

The GBO team compared three places for the PEP:

1. FSC Inway as PEP (chosen). Every call to the source already goes
   through the Inway, and the Inway has an AuthZEN plugin
   ([F-35](../traceability/findings-closed.md#f-35)).
2. A separate PEP service between the Inway and the source (the earlier
   `pep-service`). It duplicates the PEP role. It also adds a hop. If that hop
   is in the wrong place, a request can go around it.
3. A PEP at the source gateway. The gateway then makes the decision call
   and does the substitution. Enforcement and data transformation then
   mix in one component.

## Consequences

- All authorization decisions come from Rego policies. The policies are
  versioned in Git and have tests.
- If the source gateway is reachable outside the Inway, a request can skip
  the decision. So the gateway must be reachable only through the Inway
  ([REQ-04](../requirements/authorization.md#req-04),
  [ADR-0033](0033-gateway-decrypts-after-allow.md)).
- The demo patches the FTV GraphQL profile mapper into the OpenFTV v0.1.0
  build. Each patch step checks that it changed something. When the
  upstream project includes the profile mapper, the demo removes the patch
  ([#331](https://github.com/ICTU/GBO-demo/issues/331)). CI keeps the PDP
  ref and the Manager image tags on one release tag.
- The PDP writes every decision to the ADL
  ([ADR-0036](0036-adl-decision-record.md)).
- The PSA mentions ODRL in S06. This design does not use ODRL.
  [Risks and technical debt](../risks.md) tracks the deviation.
- GBO follows the FTV GraphQL profile and AuthZEN. This answers the
  question of which profile GBO follows
  ([Q-16](../traceability/answered-questions.md#q-16)).

## Traceability

- Requirements: [REQ-04](../requirements/authorization.md#req-04), [REQ-42](../requirements/authorization.md#req-42), [REQ-44](../requirements/authorization.md#req-44), [REQ-17](../requirements/authorization.md#req-17). This ADR replaces the removed REQ-52.
- Findings: [F-02](../traceability/findings-closed.md#f-02) (closed), [F-27](../traceability/findings-closed.md#f-27) (closed), [F-31](../traceability/findings-closed.md#f-31) (closed), [F-35](../traceability/findings-closed.md#f-35) (resolved in demo)
- Open questions: [Q-16](../traceability/answered-questions.md#q-16) (answered)
- Demo increments: [SL-17](../traceability/increments.md#sl-17) (done), [SL-18](../traceability/increments.md#sl-18) (done), [SL-31](../traceability/increments.md#sl-31) (done), [SL-40](../traceability/increments.md#sl-40) (done)
