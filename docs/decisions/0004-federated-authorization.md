# ADR-0004: Five authorization concerns, federated evaluation, no central authorization server

- Status: accepted
- Date: 2026-08-24 (updated 2026-11-02)
- Satisfies: [D-01](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie), [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: Reference architecture v0.6.2, decision 5 (archived and unpublished), [Q-02](../traceability/answered-questions.md#q-02), [Q-10](../traceability/answered-questions.md#q-10), [F-02](../traceability/findings-closed.md#f-02)
- Implemented in: [fsc-infra/docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml) (concerns ① ②), [services/openftv-pdp](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp) and [policies/gbo](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo) (concerns ③ ④ ⑤)

## Context and problem statement

The question "May this request proceed" splits into five questions. Each
question changes at its own rate and has its own decision makers:

- organization identity
- organization permission
- access basis
- data scope
- request validity

A central authorization server couples all five questions and is a single
choke point.

## Decision

GBO evaluates each concern where it belongs, federated per organization:

- mTLS and PKI answer identity at every connection.
- The FSC Manager of the provider answers permission when it issues a
  token. Contract acceptance itself is a policy decision
  ([ADR-0015](0015-contract-acceptance-by-policy.md)).
- The PDP at the Inway of the provider answers access basis, data scope,
  and request validity for each request.

There is no central authorization server. An FSC access token never
contains consent. Instead, the consumer presents a consent proof, and the
PDP verifies it for each request ([ADR-0032](0032-consent-proof.md)). The
regime follows from the evidence that the request carries
([ADR-0031](0031-regime-from-evidence.md)).

For legal-basis routes (Gov-to-Gov), the design evaluates the
grondslag locally from policy data, without a PIP call. The demo does not
implement this path. The path needs its own positive evidence, because a
declared flow is not sufficient ([ADR-0031](0031-regime-from-evidence.md)).
For more information, see [Risks and technical debt](../risks.md).

## Consequences

- A revocation takes effect on the next request. No token needs to be
  invalidated.
- In the consent regime, each request depends on two network calls:
    - the consent status, asked over FSC and never cached
    - the JWKS of the register, cached for five minutes
- Concern ② also has a part at request time for integrators. A delegated
  call needs a mandate in the admission register
  ([ADR-0034](0034-integrator-delegation.md)).
- For the mapping of the concerns to the components, see
  [Authorization](../concepts/authorization.md).
- The demo does not implement rate limiting (part of concern ⑤).
  [Risks and technical debt](../risks.md) tracks this gap.

## Traceability

- Requirements: [REQ-04](../requirements/authorization.md#req-04), [REQ-18](../requirements/authorization.md#req-18), [REQ-46](../requirements/sources-identity.md#req-46), [REQ-48](../requirements/authorization.md#req-48), [REQ-74](../requirements/authorization.md#req-74)
- Findings: [F-02](../traceability/findings-closed.md#f-02) (closed), [F-08](../traceability/findings-closed.md#f-08) (closed)
- Open questions: [Q-02](../traceability/answered-questions.md#q-02) (answered), [Q-09](../traceability/answered-questions.md#q-09) (answered), [Q-10](../traceability/answered-questions.md#q-10) (answered)
- Demo increments: none
