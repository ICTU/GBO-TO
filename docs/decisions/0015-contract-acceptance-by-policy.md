# ADR-0015: FSC contract acceptance by policy

- Status: accepted
- Date: 2026-08-24 (updated 2026-11-02: ordered refusal codes, delegated grants)
- Satisfies: [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel), [P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: [autosign.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego) (design notes in comments), [REQ-61](../requirements/admission.md#req-61), [F-55](../traceability/findings-closed.md#f-55), [F-56](../traceability/findings-closed.md#f-56), demo [#491](https://github.com/ICTU/GBO-demo/issues/491), [PR #464](https://github.com/ICTU/GBO-demo/pull/464)
- Implemented in: [policies/fsc/autosign.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L165-L175) (ordered checks), [services/dvtp-onboarding-register](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dvtp-onboarding-register), [pip-pull/dvtp-onboarding.yaml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/pip-pull/dvtp-onboarding.yaml), [fsc-infra/docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L701-L702) (Manager autosign call)

## Context and problem statement

An FSC Manager can sign all incoming contracts automatically, or it can
require a manual review. Neither option scales to an admission model. DvTP
participation is a governed status, and a provider must accept contracts
only from admitted parties. Admission comes from a register and not from
decision policy ([REQ-61](../requirements/admission.md#req-61)).

## Decision

The Manager of each provider sends every submitted contract through the
PDP. The AuthZEN autosign call of the Manager evaluates a dedicated
contract-acceptance policy (package `doelbinding.auto_sign_contract`).

The policy reads the Admission register. OpenFTV pulls this register
every 5 seconds (attributes `name`, `active`, `allowed_source_peer_ids`,
`acts_for`).

The policy accepts grant type 2 (service connection) and grant type 3
(delegated service connection, [ADR-0034](0034-integrator-delegation.md)).
It runs eight checks in a fixed order, and the first check that fails
names the refusal:

| # | Code | Refuses when |
|---|---|---|
| 1 | `NOT_AN_AUTOSIGN_REQUEST` | The input is not a well-formed autosign request |
| 2 | `GRANT_TYPE_NOT_ALLOWED` | The grants are not all type 2 or all type 3 |
| 3 | `NO_COUNTERPARTY` | The contract has no party other than the provider itself |
| 4 | `ADMISSION_REGISTER_UNAVAILABLE` | The PIP pull supplied no register |
| 5 | `PARTY_NOT_IN_REGISTRY` | A party is not in the register |
| 6 | `PARTY_NOT_ACTIVE` | A party is suspended |
| 7 | `SOURCE_NOT_ALLOWED` | The party is not admitted for this source peer |
| 8 | `DELEGATION_NOT_REGISTERED` | A delegated grant has no registered integration |

A missing register (check 4) differs from an empty register (check 5). An
empty register is available data that admits nobody.

After a refusal, the contract stays proposed, so it can be submitted again
([REQ-63](../requirements/admission.md#req-63)). The contract does not
become rejected.

## Consequences

- Admission is data. If an operator activates or deactivates a
  participant in the register, the contract outcomes change without a
  policy edit. The register deactivates participants and does not delete
  them.
- The contract question ("may these parties connect at all") stays
  separate from the request question ("may this field be read now") on
  purpose ([REQ-62](../requirements/admission.md#req-62)). The request
  policy reads the same register only for integrator mandates.
- The autosign input of the Manager carries only peer IDs and grant types.
  So the policy decides about the parties and not about the services.
  Admission per service is a known limitation
  ([F-56](../traceability/findings-closed.md#f-56)).
  [Risks and technical debt](../risks.md) tracks it.
- The Manager fixes the package name. If someone renames the package, the
  policy resolves to nothing and every contract stays pending.
- A suspended consumer keeps its existing contract and can still send
  queries ([REQ-110](../requirements/admission.md#req-110),
  [Q-53](../traceability/open-questions.md#q-53)). Changes to admissions
  are not logged ([REQ-123](../requirements/admission.md#req-123)).

## Traceability

- Requirements: [REQ-61](../requirements/admission.md#req-61), [REQ-62](../requirements/admission.md#req-62), [REQ-63](../requirements/admission.md#req-63), [REQ-110](../requirements/admission.md#req-110), [REQ-123](../requirements/admission.md#req-123), [AV-06](../requirements/admission.md#av-06)
- Findings: [F-55](../traceability/findings-closed.md#f-55) (closed), [F-56](../traceability/findings-closed.md#f-56) (closed), [F-52](../traceability/findings.md#f-52) (open)
- Open questions: [Q-22](../traceability/answered-questions.md#q-22) (answered), [Q-53](../traceability/open-questions.md#q-53) (open), [Q-74](../traceability/open-questions.md#q-74) (open)
- Demo increments: [SL-09](../traceability/increments.md#sl-09) (mostly covered), [SL-45](../traceability/increments.md#sl-45) (done)
