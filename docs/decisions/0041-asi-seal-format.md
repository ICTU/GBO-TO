# ADR-0041: Seal format of ASI results

- Status: proposed (waits for [Q-32](../traceability/open-questions.md#q-32))
- Date: 2026-11-02
- Satisfies: Implementing Regulation (EU) [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj) article 9(4), as replaced by Implementing Regulation (EU) [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj), from January 1, 2027, and [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
- Deliberation: [REQ-83](../requirements/asi.md#req-83), [F-80](../traceability/findings.md#f-80), and demo [ICTU/GBO-demo#498](https://github.com/ICTU/GBO-demo/issues/498), [PR #499](https://github.com/ICTU/GBO-demo/pull/499)
- Implemented in: demo grade, with a development certificate:
    - The seal in [seal.go#L18-L57](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/seal/seal.go#L18-L57).
    - The seal on successful responses only, in [handler.go#L402-L417](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L402-L417).
    - The header in the contract, in [completions.json#L25-L33](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/openapi/completions.json#L25-L33).
    - The validation by the reference QTSP, in [qtsp-reference/internal/seal/seal.go](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/qtsp-reference/internal/seal/seal.go).

## Context and problem statement

From January 1, 2027, every verification result of an ASIP must be
signed or sealed. The seal is at least an advanced electronic seal based
on a qualified certificate. The certificate belongs to the responsible
public sector body or to the designated intermediary
([F-80](../traceability/findings.md#f-80)). ETSI TS 119 478 defines no
seal on the response ([E4](../traceability/standards-feedback.md#e4)).

A QTSP that verifies at several ASIPs must validate every seal in the
same way. If each ASIP chooses its own format, every QTSP must implement
each format. For this reason, the format is an interface agreement. It
is not a choice per ASIP ([REQ-83](../requirements/asi.md#req-83)).
[Q-32](../traceability/open-questions.md#q-32) asks who decides the
format. This ADR stays proposed until that decision.

## Proposed decision

The proposal has five parts:

1. The ASIP seals the exact response body with a detached JWS (RFC 7515,
   Appendix F). The JWS goes in the header `X-JWS-Signature`
   (`<protected header>..<signature>`).
2. The algorithm is ES256. The protected header carries the certificate
   chain in `x5c`, leaf first.
3. The body stays plain JSON, as the ETSI OpenAPI prescribes. The
   contract of the data service names the header as an addition.
4. The ASIP seals every successful verify and retrieve response (200).
   An error response is not a verification result and gets no seal.
5. The QTSP validates the signature over the received body, and the
   chain against its trust anchors. The QTSP does not accept a result
   without a valid seal.

## Consequences

- With only the response and the trusted lists, the QTSP can establish
  that the response comes unchanged from this ASIP.
- The format works with any HTTP client. It leaves the ETSI response
  schema unchanged.
- The demo seals with a development certificate. Production needs a
  qualified certificate for electronic seals (Implementing Regulation
  (EU) 2025/1943, Annex II). The certificate has the registration number
  of the organization as `organizationIdentifier`.
- It is open who holds that certificate: the source holder, or the
  designated intermediary ([Q-17](../traceability/open-questions.md#q-17),
  [Q-28](../traceability/open-questions.md#q-28)).

## Considered options

- A detached JWS in a header (proposed). It is simple for a JSON API.
  The body stays as ETSI specifies.
- A JAdES baseline signature (ETSI TS 119 182-1). This is the EU format
  for JSON signatures, with the signing time and the certificate
  references in the header. It is more work for the QTSP and the ASIP,
  but it is closer to the eIDAS ecosystem.
- An enveloping JWS, with the result as the JWS payload. This option
  changes the response form that the ETSI OpenAPI prescribes.

## Open points

These points are open:

- Who decides the format for all Dutch ASIPs, and does ETSI ESI add it
  to TS 119 478 ([Q-32](../traceability/open-questions.md#q-32),
  [E4](../traceability/standards-feedback.md#e4))?
- Does every source response get one seal, regardless of the channel
  (DvTP, EUDI, ASI) ([Q-75](../traceability/open-questions.md#q-75))?

## Traceability

- Requirements: [REQ-83](../requirements/asi.md#req-83),
  [REQ-94](../requirements/asi.md#req-94)
- Findings: [F-80](../traceability/findings.md#f-80) (open)
- Open questions: [Q-17](../traceability/open-questions.md#q-17),
  [Q-28](../traceability/open-questions.md#q-28),
  [Q-32](../traceability/open-questions.md#q-32),
  [Q-75](../traceability/open-questions.md#q-75)
- Standards feedback: [E4](../traceability/standards-feedback.md#e4)
- Demo increments: [SL-28](../traceability/increments.md#sl-28)
