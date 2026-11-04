# ADR-0042: Optional per-attribute token binding for ASI tokens

- Status: proposed (waits for [Q-33](../traceability/open-questions.md#q-33))
- Date: 2026-11-02
- Satisfies: Implementing Regulation (EU) [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj) article 9(5) (a member state can impose access control), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte), [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: [REQ-103](../requirements/asi.md#req-103), [F-95](../traceability/findings.md#f-95), and demo [PR #559](https://github.com/ICTU/GBO-demo/pull/559), [ICTU/GBO-demo#571](https://github.com/ICTU/GBO-demo/issues/571), [PR #572](https://github.com/ICTU/GBO-demo/pull/572)
- Implemented in:
    - The check at the authorization server in [authorization_details.go#L31-L79](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/authorization_details.go#L31-L79).
    - The request page in [pages.go#L109-L111](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/pages.go#L109-L111).
    - The token in [tokens.go#L70-L72](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/tokens.go#L70-L72).
    - The mandatory switch in [main.go#L109](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/main.go#L109).
    - The check at the ASIP in [accesstoken.go#L177-L197](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/accesstoken/accesstoken.go#L177-L197) and [handler.go#L346-L356](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L346-L356).

## Context and problem statement

ETSI TS 119 478 clause 6.1.3.2 binds an access token per operation only
(`verify`, `retrieve`). With one token, the QTSP can ask every attribute
of the data service, also when the citizen approved something else
([F-95](../traceability/findings.md#f-95),
[E5](../traceability/standards-feedback.md#e5)). Article 9(5) of
Implementing Regulation 2025/1569 lets a member state impose access
control. [Q-33](../traceability/open-questions.md#q-33) asks whether the
Netherlands imposes a binding per attribute. This ADR stays proposed
until that decision.

## Proposed decision

The proposal has four parts:

1. A QTSP can name the attributes in the authorization request as one
   RFC 9396 `authorization_details` entry. The entry has the provisional
   type
   `https://gbo.example/authorization-details/authentic-source-attributes`.
   The entry has these fields:
    - `locations`, equal to `resource`.
    - `actions`, equal to the scope.
    - `attribute_identifiers`, with 1 to 50 unique https URIs.
2. The authorization server validates the entry against the data
   service and the scope. It refuses an invalid entry with
   `invalid_request`. It shows the attributes on the request page and
   puts the entry unchanged in the token.
3. If the token carries the entry, the ASIP refuses a request for
   another attribute with 401 `insufficient_scope`.
4. By default, the binding is optional, so a QTSP that implements only
   ETSI can connect. Without the entry, the authorization is per
   operation, and the description of the data service is the limit. A
   configuration switch makes the entry mandatory
   (`AZSP_REQUIRE_AUTHORIZATION_DETAILS=true` in the demo).

## Consequences

- With the binding, the citizen sees exactly which attributes the QTSP
  asks ([REQ-91](../requirements/asi.md#req-91)). The token is not valid
  for other attributes.
- Only parties that know the GBO type can use the binding. The type
  identifier is provisional.
- If the Netherlands makes the binding mandatory, QTSPs that implement
  only ETSI cannot connect. This stays so until ETSI or a national
  profile defines the extension.

## Considered options

The proposal considered three other options:

- A binding per operation only, as ETSI specifies. This option is
  simpler for QTSPs, but the token is wider than the approval.
- A mandatory binding per attribute. This option is closer to
  [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/). But
  it excludes QTSPs that implement only ETSI, until the extension is
  standard.
- Attributes in the scope string. Not chosen. ETSI fixes the scopes, and
  RFC 9396 is the standard place for structured detail.

## Traceability

- Requirements: [REQ-91](../requirements/asi.md#req-91),
  [REQ-95](../requirements/asi.md#req-95),
  [REQ-103](../requirements/asi.md#req-103)
- Findings: [F-95](../traceability/findings.md#f-95) (open)
- Open questions: [Q-33](../traceability/open-questions.md#q-33)
- Standards feedback: [E5](../traceability/standards-feedback.md#e5)
- Demo increments: [SL-28](../traceability/increments.md#sl-28)
