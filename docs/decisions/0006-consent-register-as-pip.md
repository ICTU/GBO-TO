# ADR-0006: Consent register as runtime PIP

- Status: superseded by [ADR-0007](0007-consent-signed-token.md), which [ADR-0032](0032-consent-proof.md) supersedes in turn
- Date: 2026-08-24 (ported from reference architecture v0.6.2)
- Satisfies: [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie), [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: Reference architecture v0.6.2, decision 2, and its DvTP PBAC alignment proposal (archived and unpublished)
- Implemented in: superseded before implementation

## Context and problem statement

DvTP draft v0.1 authorized requests through a custom gateway that checked
consent twice. GBO replaces this gateway with the standard PEP-PDP chain.
Then the question is how the consent evidence gets to the decision.

## Decision (superseded)

A register records the consent and acts as a Policy Information Point
(PIP). For each request, the PDP looks up the consent by `consent_id`. The
consent proof that the service provider (dienstverlener) receives is an opaque reference.

## Why it was superseded

With a pure lookup, the authorization evidence depends only on the
availability and integrity of the register. The consumer gives the PDP
nothing that the PDP can verify.

The implemented design keeps the register and its status check for
revocation on each request. But the consent itself becomes a signed
artifact that the consumer presents and that the PDP can verify. For this
design, see [ADR-0007](0007-consent-signed-token.md).

## Traceability

- Requirements: [REQ-68](../requirements/consent.md#req-68), [REQ-18](../requirements/authorization.md#req-18)
- Findings: [F-24](../traceability/findings-closed.md#f-24) (resolved in demo)
- Open questions: [Q-05](../traceability/answered-questions.md#q-05) (answered), [Q-23](../traceability/answered-questions.md#q-23) (closed)
- Demo increments: [SL-08](../traceability/increments.md#sl-08) (done)
