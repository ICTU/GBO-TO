# ADR-0031: The authorization regime follows from the evidence a request carries

- Status: accepted
- Date: 2026-11-02
- Satisfies: [S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie), [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
- Supersedes: [ADR-0030](0030-grant-properties.md)
- Deliberation: [REQ-74](../requirements/authorization.md#req-74), [F-70](../traceability/findings.md#f-70), [Q-15](../traceability/answered-questions.md#q-15), and demo [#334](https://github.com/ICTU/GBO-demo/issues/334), [PR #363](https://github.com/ICTU/GBO-demo/pull/363), [CHANGELOG](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L653-L662)
- Implemented in:
    - [engine.rego (regime selection)](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L168-L181) and [consent.rego (token read)](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L44-L62).
    - The rule regimes in [dvt0001.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L18), [eud0001.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0001.rego#L21), and [asi0001.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/asi/asi0001.rego#L20).
    - The tests in [engine_test.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L227-L238).

## Context and problem statement

The PDP judges a request under one of two regimes:

- In the consent regime (DvTP), the consent of a citizen is the access
  basis.
- In the PID regime (EUDI issuance, ASI), a verified PID disclosure of
  the citizen is the basis.

Each regime has its own rules and its own reasons to deny.

A component must select the regime. If the consumer selects it, the
consumer chooses the basis for its own judgment. Earlier designs put the
selection in three places:

- A header.
- A signed claim of the provider
  ([ADR-0014](0014-provider-signed-flow-claims.md)).
- An FSC grant property ([ADR-0030](0030-grant-properties.md)).

All three are a declaration about the request. None of them is evidence
in the request.

## Decision

The regime follows from the evidence that the request carries:

- If a consent token is present (`X-GBO-Consent-Token`, verified or
  not), the request is in the consent regime. Only the rules with
  `regime := "consent"` bind: DVT0001 and LVG0001.
- If no consent token is present, the request is in the PID regime. Only
  the rules with `regime := "pid"` bind: EUD0001, EUD0002, and ASI0001.
- If two consent proofs are present, the policy denies with
  `CONSENT_CONTEXT_INVALID`. The policy does not pick one of them.

Every rule declares its regime. Only the rules of the active regime
bind, so the deny reason also comes from that regime. FSC grants carry
no properties. No component reads a `flow`.

## Considered options

1. Evidence in the request (chosen). The request carries no declaration
   that a party can forge or must maintain. Each rule still checks its own basis, so a wrong regime
   cannot give access.
2. `flow` as an FSC grant property ([ADR-0030](0030-grant-properties.md)).
   Both peers sign it, but it is a declaration per contract. Each
   consumer needs one contract per regime, and a change needs a new
   contract.
3. Dispatch from component metadata or from the certificate
   ([SL-24](../traceability/increments.md#sl-24), dropped). This option
   binds the regime to the caller, and not to the request. A party that
   acts in both regimes does not fit.
4. A request header or a default regime
   ([SL-48](../traceability/increments.md#sl-48)). With this option, the
   consumer chooses the regime. Not chosen.

## Consequences

- The rules already did the security work. DVT0001 and LVG0001 deny
  without a verified consent. The PID rules deny without a PID subject.
  The regime decides which reasons the PDP reports. The regime does not
  decide access. Engine tests pin the reason in both directions.
- Only consent is positive evidence. A request enters the PID regime
  because it has no consent proof
  ([F-70](../traceability/findings.md#f-70)). For this reason, the PID
  regime needs its own positive evidence: a verified PID disclosure
  ([REQ-45](../requirements/eudi-issuance.md#req-45)). In demo v0.9.0,
  the adapter callback that carries this evidence is not authenticated
  ([#133](https://github.com/ICTU/GBO-demo/issues/133)).
- The actor lists of the PID rules (`designated_issuers`, `asip`) must
  stay disjoint from the consent consumers in every environment. A test
  pins this for the seeded peers only
  ([engine_test.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L366-L376)).
- A Gov-to-Gov regime on a legal basis needs its own positive evidence.
  It cannot be a third regime that rests on an absence.
- The sidecar uses the same evidence. If a consent token is present, the
  sidecar takes the subject from it. If not, the sidecar passes the
  request through ([ADR-0033](0033-gateway-decrypts-after-allow.md)).

## Traceability

- Requirements: [REQ-74](../requirements/authorization.md#req-74), [REQ-48](../requirements/authorization.md#req-48), [REQ-45](../requirements/eudi-issuance.md#req-45), [REQ-18](../requirements/authorization.md#req-18)
- Findings: [F-70](../traceability/findings.md#f-70) (open), [F-32](../traceability/findings-closed.md#f-32) (resolved in demo), [F-43](../traceability/findings-closed.md#f-43) (superseded), [F-49](../traceability/findings-closed.md#f-49) (premise lapsed), [F-62](../traceability/findings-closed.md#f-62) (resolved in demo)
- Open questions: [Q-15](../traceability/answered-questions.md#q-15) (answered)
- Demo increments: [SL-24](../traceability/increments.md#sl-24) (dropped), [SL-48](../traceability/increments.md#sl-48) (done)
