# ADR-0007: Consent as a signed token with a live status check

- Status: superseded by [ADR-0032](0032-consent-proof.md)
- Date: 2026-08-24 (superseded 2026-11-02)
- Satisfies: [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie), [S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal), [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Supersedes: [ADR-0006](0006-consent-register-as-pip.md)
- Superseded by: [ADR-0032](0032-consent-proof.md)
- Deliberation: signed, actor-bound consent proof ([PR #238](https://github.com/ICTU/GBO-demo/pull/238), [SL-47](../traceability/increments.md#sl-47))
- Implemented in: changed in gbo-demo. Since [PR #469](https://github.com/ICTU/GBO-demo/pull/469), the token does not carry `pi`. Verification moved from the request mapper into the policy ([#330](https://github.com/ICTU/GBO-demo/issues/330), [PR #371](https://github.com/ICTU/GBO-demo/pull/371)). The status goes over FSC ([#383](https://github.com/ICTU/GBO-demo/issues/383)).

## Why superseded

The demo changed three parts of this decision:

- The token carries no PI. It carries an encrypted value for each source
  (`encrypted_subject`). The consumer names the citizen with a placeholder
  ([SL-51](../traceability/increments.md#sl-51)).
- The policy verifies the token and gets the status itself. The request
  mapper only maps.
- The PDP asks for the status over FSC, through its own Outway, and not
  directly at the register.

For this reason, [ADR-0032](0032-consent-proof.md) records the consent
proof again. The signed token, the live status check for each request, and
the bearer-token consequence stay. The following sections keep the
original decision as history.

## Context and problem statement

The PDP needs consent evidence that it can verify and that can be revoked.
The evidence must work without exposing the BSN. Also, one consent must
cover more than one source holder (bronhouder).

## Decision (superseded)

The consent register (toestemmingsregister) issues an ES256-signed JWT of type
`gbo-consent+jwt` with these claims:

- `consent_id`
- `pi`
- `scopes`
- `scope_entries` (per source holder)
- `dienstverlener_oin`
- `valid_until` (= `exp`)

The service provider (dienstverlener) presents the token in the `X-Gbo-Consent-Token` header.
For each request, the PDP does three things:

1. It verifies the signature against the JWKS of the register.
2. It cross-checks the claims.
3. It gets the live status of exactly that `consent_id`. Thus a
   revocation takes effect immediately.

The register stores no BSN and no PI.

## Consequences (at the time)

- The decision binds to verified claims:
    - actor binding (`subject.id == dienstverlener_oin`)
    - subject binding (the PI in the query equals the PI in the token)
    - scope and year coverage
- The token is a bearer token. Actor binding blocks use by another
  consumer. It does not block replay by the same consumer. Production
  needs a shorter validity and a proof-of-possession binding to the FSC
  identity. [Risks and technical debt](../risks.md) tracks this.
- The register stays a runtime dependency only for the status check. This
  check fails closed (`CONSENT_STATUS_UNAVAILABLE`).

## Traceability

- Requirements: [REQ-68](../requirements/consent.md#req-68), [REQ-79](../requirements/pseudonymization.md#req-79)
- Findings: [F-04](../traceability/findings-closed.md#f-04) (closed), [F-44](../traceability/findings-closed.md#f-44) (resolved in demo)
- Open questions: [Q-05](../traceability/answered-questions.md#q-05) (answered)
- Demo increments: [SL-23](../traceability/increments.md#sl-23) (done), [SL-47](../traceability/increments.md#sl-47) (done), [SL-51](../traceability/increments.md#sl-51) (done)
