# ADR-0044: Issuance offers the authorization code flow, and pre-auth only after identification in the same session

- Status: proposed (waits for the open question on the authorization server for issuance)
- Date: 2026-11-10
- Satisfies: [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
- Deliberation: HAIP 1.0 section 4, ARF v3.0.0 ISSU_01a, ETSI TS 119 472-3 GEN-REQ-4.1-03 and -04, demo [#614](https://github.com/ICTU/GBO-demo/issues/614)
- Implemented in: not implemented in gbo-demo v0.9.0. Work in [#614](https://github.com/ICTU/GBO-demo/issues/614).

## Context and problem statement

[ADR-0018](0018-eudi-disclosure-issuance.md) issues after a PID disclosure
on the nl-wallet issuance server. That variant is no standard OpenID4VCI
flow, and it works with one wallet only. The standards set the flows:

- HAIP 1.0 section 4: the wallet and the issuer support the authorization
  code flow. ARF ISSU_01a follows HAIP.
- ETSI TS 119 472-3: the wallet supports both flows (GEN-REQ-4.1-03). The
  issuer implements at least one (GEN-REQ-4.1-04).

The two flows identify the citizen in different places. In the
authorization code flow, an authorization server identifies the citizen
inside the flow. In the pre-authorized code flow, the issuer identifies
the citizen before it makes the offer, outside the flow. The offer itself
carries no binding to the citizen.

## Proposed decision

- The issuance facility offers the authorization code flow as the main
  route. Which authorization server identifies the citizen is an open
  question.
- The facility also offers the pre-authorized code flow, but only after
  it identified the citizen in the same session. Example: the wallet
  presents its PID over OpenID4VP to the issuer. The answer of the issuer
  sends the wallet to a pre-authorized offer. The offer goes back to the
  wallet that presented the PID, and is short-lived and single-use.
- An offer that another component makes and shows needs a binding to
  the citizen. An example is a QR code after a login in a portal. Which
  binding is enough is open.
- A deviation that one wallet needs is documented, and does not weaken
  the other routes.

## Why proposed, not accepted

Three points are open:

- the authorization server for issuance
- the binding of an offer that another component makes
- whether the NL Wallet will support the authorization code flow at an
  external issuer

## Considered options

1. Pre-authorized code flow only, always after identification. This meets
   TS 119 472-3 and works with every wallet. It deviates from HAIP and
   the ARF. The NOTE to GEN-REQ-4.1-05 calls the flow insufficient
   against hijacking in remote scenarios.
2. Authorization code flow only. This meets HAIP and the ARF. A wallet
   that does not support the flow at an external issuer gets no
   attestation.
3. Both flows, with pre-authorized only after identification in the same
   session (proposed). HAIP for the wallets that support it, and a route
   for the other wallets and for issuance that the issuer starts.
4. Keep the variant of ADR-0018. Rejected: it is no standard flow, and it
   works with one wallet only.

## Consequences

- This ADR replaces the protocol and the flow of
  [ADR-0018](0018-eudi-disclosure-issuance.md). The adapter path, the PID
  regime, the projection, and the certificate set of ADR-0018 stay.
- [REQ-45](../requirements/eudi-issuance.md#req-45) takes the subject only
  from a verified PID disclosure. In the authorization code flow, the
  subject comes from the identification at the authorization server, so
  REQ-45 must change.
- When the issuer asks for the PID, it is a wallet relying party for that
  request. It needs a registration of its intended use and attributes,
  next to its registration as attestation provider.
- Two routes mean two paths to test and to secure.

## Traceability

- Requirements: [REQ-45](../requirements/eudi-issuance.md#req-45), [REQ-58](../requirements/eudi-issuance.md#req-58)
- Open questions: [Q-36](../traceability/open-questions.md#q-36) (open)
- Decisions: [ADR-0018](0018-eudi-disclosure-issuance.md), [ADR-0028](0028-pubeaa-productization.md)
