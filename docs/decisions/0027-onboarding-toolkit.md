# ADR-0027: Source holder onboarding toolkit

- Status: proposed
- Date: 2026-08-24, updated on 2026-11-02
- Satisfies: [D-06](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), [GO §6: impact op bronhouders](https://ictu.github.io/GBO-GO/main/#6-impact-op-betrokken-partijen)
- Deliberation: reference architecture v0.6.2, gap 6 "bronhouder onboarding toolkit" (archived and unpublished)
- Implemented in: partially. These parts of the demo are reusable starting points: the [Helm chart](https://github.com/ICTU/GBO-demo/blob/v0.9.0/deploy/helm/gbo-app), the source metadata contract ([ADR-0016](0016-source-owned-metadata.md)), the source gateway ([ADR-0033](0033-gateway-decrypts-after-allow.md)), and the [contract seed scripts](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/scripts).

## Context and problem statement

GBO has one API and one connectivity stack. Even so, the connection of a
source holder (bronhouder) involves PKI, FSC components, a source gateway, policies, and
metadata. Smaller source holders (gemeenten) can lack the capacity for this
work.

## Proposed decision

GBO packages the source-side stack as a deployable toolkit. The toolkit
has these parts:

- FSC Inway and Manager.
- The bron-sidecar.
- Contract seeds.
- Policy templates per route.
- A reference onboarding process: certificate, FSC registration,
  metadata publication, contract, and activation.

Some sources cannot host their own GraphQL endpoint. For these sources,
GBO offers a GBO-vertaallaag as a shared service.

## Open points

These points are open:

- Who operates the shared instances of the vertaallaag?
- The policy templates are guidance. Each source holder owns and
  publishes its own policy ([ADR-0021](0021-central-pap-signed-bundles.md)).
- How does a source get its BSNk decryption keys as an onboarding step
  ([BSNK-09](../requirements/pseudonymization.md#bsnk-09),
  [#467](https://github.com/ICTU/GBO-demo/issues/467))?
- Who builds the registration and onboarding facility
  ([Q-74](../traceability/open-questions.md#q-74))?
- The support model and the conformance testing for onboarded sources.

## Traceability

- Requirements: [REQ-64](../requirements/sources-identity.md#req-64), [REQ-65](../requirements/sources-identity.md#req-65), [AV-07](../requirements/admission.md#av-07), [AV-09](../requirements/admission.md#av-09), [BSNK-09](../requirements/pseudonymization.md#bsnk-09)
- Findings: [F-57](../traceability/findings.md#f-57) (open), [F-71](../traceability/findings.md#f-71) (open)
- Open questions: [Q-74](../traceability/open-questions.md#q-74) (open)
- Demo increments: [SL-09](../traceability/increments.md#sl-09) (mostly covered), [SL-46](../traceability/increments.md#sl-46) (done)
