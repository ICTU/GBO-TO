# Feedback on ETSI TS 119 478

The demo found gaps and conflicts in ETSI TS 119 478 V1.1.1. In increment
[SL-28](increments.md#sl-28), the demo built an Authentic Source Interface
Provider (ASIP) mock to that standard. Each item gives the clause, the
issue, and a proposal for the text. It also gives the related findings,
open questions, and requirements. The finding or the open question holds
the reasoning.

- **Audience**: ETSI ESI, the group that maintains the standard.
- **Route**: through the Ministry of the Interior (BZK) and the EUDI
  cooperation group, as for [Q-32](open-questions.md#q-32).
- **Who submits, and when**: not decided.
- **State**: collected and not sent.

Two kinds of items do not go to ETSI, so they are not on this list:

- Choices that the Netherlands makes itself. An example is which
  identification means an authorization server accepts
  ([Q-36](open-questions.md#q-36)).
- Gaps in the NL PID ([F-94](findings.md#f-94)).

## Overview

The feedback has ten items:

| # | Clause | Issue | Related |
|---|---|---|---|
| [E1](#e1) | 5.3.3 | No field for the authorization-server metadata in the contract | [F-91](findings.md#f-91), [Q-39](open-questions.md#q-39) |
| [E2](#e2) | 6.1.1.1, 6.1.1.2 | Value optional after Annex IV of 2026/1735, but the fuzzy-matching requirement stays | [F-92](findings.md#f-92), [Q-29](open-questions.md#q-29) |
| [E3](#e3) | 6.1.1.2, 6.1.2.2 | A response names one authentic source | [F-89](findings.md#f-89) |
| [E4](#e4) | 6.1.1 | No seal format for the verification result | [Q-32](open-questions.md#q-32), [F-80](findings.md#f-80) |
| [E5](#e5) | 6.1.3.2 | A token binds per operation and has no binding per attribute | [F-95](findings.md#f-95), [Q-33](open-questions.md#q-33) |
| [E6](#e6) | 6.1.3.3 | Identification by the QTSP and by the authorization server are not linked | [F-93](findings.md#f-93), [Q-40](open-questions.md#q-40) |
| [E7](#e7) | 6.1.3.1 | Identification data is readable for the QTSP in the token | [F-86](findings.md#f-86) |
| [E8](#e8) | 6.1.3.4 | Security profile left open, with conflicts on PAR and RS256 against the norms it references | [F-84](findings.md#f-84) |
| [E9](#e9) | 6.1.3 | RFC 9207 (`iss` in the authorization response) is missing | [F-96](findings.md#f-96) |
| [E10](#e10) | 6.1.3.2 | The meaning of a revoked right for issued tokens is not defined | [Q-41](open-questions.md#q-41) |

## E1: No field for the authorization-server metadata in the contract {#e1}

- **Clause**: 5.3.3.
- **Issue**: REQ-DIP-5.3.3-03-02-01 requires that the contract behind
  `endpointDescription` specifies the metadata of the OAuth authorization
  server. OpenAPI 3.0 has no field for this. `oauth2` has only endpoint
  URLs. `openIdConnectUrl` points to OpenID Connect Discovery. It does
  not point to RFC 8414 metadata.
- **Proposal**: prescribe one fixed field. One example is an extension
  `x-oauth-authorization-server` with the URL of the RFC 8414 metadata.
  Another example is the metadata URL in the `dataService` record itself.
- **Related**: [F-91](findings.md#f-91),
  [Q-39](open-questions.md#q-39),
  [REQ-100](../requirements/asi.md#req-100).
- **Status**: open (submitter not decided).

## E2: Value optional after Annex IV of 2026/1735, but the fuzzy-matching requirement stays {#e2}

- **Clause**: 6.1.1.1, 6.1.1.2.
- **Issue**: Annex IV of Commission Implementing Regulation (EU)
  2026/1735 makes `attributeValue` optional for `Match` and
  `MatchWithVariation`. REQ-ASIP-6.1.1.1-10-01 still requires that an
  ASIP with fuzzy matching returns the stored value. An ASIP cannot
  satisfy both.
- **Proposal**: change REQ-ASIP-6.1.1.1-10-01 to match the annex. The
  ASIP MAY return the stored value, but NEED NOT.
- **Related**: [F-92](findings.md#f-92),
  [Q-29](open-questions.md#q-29), [Q-70](open-questions.md#q-70),
  [REQ-85](../requirements/asi.md#req-85),
  [REQ-113](../requirements/asi.md#req-113). The demo returns
  `MatchWithVariation` and never returns the stored value.
- **Status**: open (submitter not decided).

## E3: A response names one authentic source {#e3}

- **Clause**: 6.1.1.2, 6.1.2.2.
- **Issue**: REQ-ASIP-6.1.1.2-08 and REQ-ASIP-6.1.2.2-04 let a response
  name one `authenticSource`. An ASIP that serves several sources cannot
  account for attributes of two sources in one response.
- **Proposal**: allow `authenticSource` per attribute result. As an
  alternative, state explicitly that an ASIP offers one data service per
  source.
- **Related**: [F-89](findings.md#f-89),
  [REQ-94](../requirements/asi.md#req-94),
  [REQ-95](../requirements/asi.md#req-95),
  [ADR-0038](../decisions/0038-asi-data-service-per-source.md). The demo
  follows the second option.
- **Status**: open (submitter not decided).

## E4: No seal format for the verification result {#e4}

- **Clause**: 6.1.1.
- **Issue**: Art. 9(4) of Commission Implementing Regulation (EU)
  2025/1569, as amended by 2026/1735, requires a seal on each
  verification result. Clause 6.1.1 sets no format. Each ASIP chooses its
  own format, so a QTSP must build a different check for each ASIP.
- **Proposal**: prescribe one seal profile. An example is JAdES baseline
  (ETSI TS 119 182-1) as a detached signature over the response body.
- **Related**: [Q-32](open-questions.md#q-32),
  [F-80](findings.md#f-80), [Q-75](open-questions.md#q-75),
  [REQ-83](../requirements/asi.md#req-83),
  [ADR-0041](../decisions/0041-asi-seal-format.md).
- **Status**: open (submitter not decided).

## E5: A token binds per operation and has no binding per attribute {#e5}

- **Clause**: 6.1.3.2.
- **Issue**: clause 6.1.3.2 defines the scopes `verify` and `retrieve`.
  A token is then valid for every attribute of the data service. The
  token does not show which attributes the citizen approved. The demo
  binds per attribute with RFC 9396 `authorization_details` and a type of
  its own. This works only between parties that know that type.
- **Proposal**: define an `authorization_details` type for the ASI, with
  data service, operations, and attribute identifiers. A member state that
  authorizes per attribute (art. 9(5)) can then do so in an interoperable
  way.
- **Related**: [F-95](findings.md#f-95),
  [Q-33](open-questions.md#q-33),
  [REQ-103](../requirements/asi.md#req-103),
  [ADR-0042](../decisions/0042-asi-attribute-token-binding.md).
- **Status**: open (submitter not decided).

## E6: Identification by the QTSP and by the authorization server are not linked {#e6}

- **Clause**: 6.1.3.3.
- **Issue**: the specification has no link between the two
  identifications:
    - In figure 3 of clause 6.1.3.3, only the authorization server
      identifies the citizen. Those identification data go into the token
      (steps 7 to 10 and 16).
    - The QTSP must identify the citizen to whom it issues (eIDAS
      art. 24(1)). The specification does not describe that
      identification and does not link the two.
    - Art. 9(3) of Commission Implementing Regulation (EU) 2025/1569 lets
      the request name the identification data of the subject. ETSI fills
      this in through the token.
- **Proposal**: describe how the QTSP shows that the subject of the
  request is the citizen it identified. For example, the QTSP sends its
  own identification data for verification too.
- **Related**: [F-93](findings.md#f-93),
  [Q-40](open-questions.md#q-40).
- **Status**: open (submitter not decided).

## E7: Identification data is readable for the QTSP in the token {#e7}

- **Clause**: 6.1.3.1.
- **Issue**: REQ-AZSP-6.1.3.1-08 lets the token carry the identification
  data of the user. The QTSP can read the token. It then also sees a
  national identification number that it is not allowed to process. In
  the Netherlands, this number is the BSN.
- **Proposal**: allow or prescribe that the identification data are
  encrypted for the resource server (JWE), or that the token carries a
  pseudonym.
- **Related**: [F-86](findings.md#f-86),
  [REQ-86](../requirements/asi.md#req-86).
  [ICTU/GBO-demo#595](https://github.com/ICTU/GBO-demo/issues/595) holds
  the demo work to protect the BSN in the token.
- **Status**: open (submitter not decided).

## E8: Security profile left open, with conflicts on PAR and RS256 against the norms it references {#e8}

- **Clause**: 6.1.3.4.
- **Issue**: clause 6.1.3.4 asks only to take RFC 6819, RFC 7636,
  RFC 9700, and FAPI 2.0 "into account". NOTE 3 at the PKCE requirement
  refers to FAPI 2.0 §5.3.2.2, which requires PAR. ETSI does not require
  PAR. RFC 9068 §2.1, mandatory through REQ-AZSP-6.1.3.1-08, lets
  resource servers support RS256. FAPI 2.0 forbids RS256. As a result, a
  QTSP meets a different profile at each authorization server.
- **Proposal**: fix one profile: client authentication, token binding,
  PAR or no PAR, and the algorithms.
- **Related**: [F-84](findings.md#f-84),
  [Q-66](open-questions.md#q-66). The demo records its choice per point
  in
  [`conformance/security-considerations.md`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/security-considerations.md).
- **Status**: open (submitter not decided).

## E9: RFC 9207 (`iss` in the authorization response) is missing {#e9}

- **Clause**: 6.1.3.
- **Issue**: a QTSP talks to one authorization server for each ASIP.
  RFC 9700 §2.1 then requires a defense against mix-up attacks,
  preferably with `iss` per RFC 9207. FAPI 2.0 requires that the
  authorization server returns it. Clause 6.1.3 does not name RFC 9207.
- **Proposal**: prescribe RFC 9207 for the authorization server, and the
  check of `iss` by the QTSP.
- **Related**: [F-96](findings.md#f-96).
- **Status**: open (submitter not decided).

## E10: The meaning of a revoked right for issued tokens is not defined {#e10}

- **Clause**: 6.1.3.2.
- **Issue**: clause 6.1.3.2 and figure 2 let the authorization server
  check the right of a QTSP again at intervals. The clause does not say
  what happens to tokens that are already issued when the right lapses.
  FAPI 2.0 §5.3.4 lets the resource server check the revocation status.
- **Proposal**: state how fast a revocation takes effect. The standard
  can choose one of two options:
    - Tokens stay valid until they expire, with a maximum lifetime.
    - The ASIP uses token introspection.
- **Related**: [Q-41](open-questions.md#q-41),
  [REQ-89](../requirements/asi.md#req-89),
  [Q-34](open-questions.md#q-34).
- **Status**: open (submitter not decided).

## Traceability

- Requirements: [REQ-83](../requirements/asi.md#req-83),
  [REQ-85](../requirements/asi.md#req-85),
  [REQ-86](../requirements/asi.md#req-86),
  [REQ-89](../requirements/asi.md#req-89),
  [REQ-94](../requirements/asi.md#req-94),
  [REQ-100](../requirements/asi.md#req-100),
  [REQ-103](../requirements/asi.md#req-103),
  [REQ-113](../requirements/asi.md#req-113)
- Findings: [F-80](findings.md#f-80), [F-84](findings.md#f-84),
  [F-86](findings.md#f-86), [F-89](findings.md#f-89),
  [F-91](findings.md#f-91), [F-92](findings.md#f-92),
  [F-93](findings.md#f-93), [F-95](findings.md#f-95),
  [F-96](findings.md#f-96) (all open)
- Open questions: [Q-29](open-questions.md#q-29),
  [Q-32](open-questions.md#q-32), [Q-33](open-questions.md#q-33),
  [Q-39](open-questions.md#q-39), [Q-40](open-questions.md#q-40),
  [Q-41](open-questions.md#q-41)
- Demo increments: [SL-28](increments.md#sl-28)
