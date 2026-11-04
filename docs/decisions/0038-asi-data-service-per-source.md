# ADR-0038: One data service per authentic source, one token per data service

- Status: accepted
- Date: 2026-11-02
- Satisfies: Implementing Regulation (EU) [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj) article 9(4), as replaced by Implementing Regulation (EU) [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj) (the result names the body that is responsible for the authentic source), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte), [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
- Deliberation: [F-89](../traceability/findings.md#f-89), and demo [PR #529](https://github.com/ICTU/GBO-demo/pull/529), [PR #534](https://github.com/ICTU/GBO-demo/pull/534), [PR #535](https://github.com/ICTU/GBO-demo/pull/535)
- Implemented in:
    - [config/dataservices.json](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/config/dataservices.json): the data services.
    - [handler.go#L99-L105](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L99-L105): the routes per data service.
    - [main.go#L115-L125](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/main.go#L115-L125) and [accesstoken.go#L148](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/accesstoken/accesstoken.go#L148): the token audience per data service.
    - [service.go#L201-L204](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service.go#L201-L204): one `resource` at the authorization server.

## Context and problem statement

ETSI TS 119 478 lets a verify or retrieve response name one authentic
source (`authenticSource`, REQ-ASIP-6.1.1.2-08 and REQ-ASIP-6.1.2.2-04).
Article 9(4) requires that the result names the body that is responsible
for that source. GBO offers one ASIP for several sources. For this
reason, that ASIP must keep every request inside one source
([F-89](../traceability/findings.md#f-89)).

The token has the same problem. The citizen approves a request for one
source ([REQ-91](../requirements/asi.md#req-91)). If the token is also
valid at another source, the QTSP can verify data at a source that the
citizen did not see. ETSI does not specify the reach of a token per data
service.

## Decision

The decision has four parts:

1. An ASIP that serves several authentic sources offers one data service
   per source. Each data service has its own base URL
   (`/<data service>/authsrc-api`), its own contract, its own
   `dataService` records, and its own token audience
   ([REQ-94](../requirements/asi.md#req-94),
   [REQ-99](../requirements/asi.md#req-99)).
2. Every response names the ASIP (`provider`) and the one authentic
   source of the data service (`authenticSource`). Since step 5 of
   [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592), the
   legal name comes from the description of the source
   ([ADR-0039](0039-asi-source-described-attributes.md)). A data service
   without an authentic source is not possible.
3. If an attribute belongs to another data service, the ASIP answers 404.
   The ASIP then asks no source.
4. An authorization request names exactly one data service as `resource`
   (RFC 8707):
    - If the request has no `resource`, two, or an unknown one, the
      result is `invalid_target`.
    - The token has the base URL of that data service as `aud`.
    - The ASIP refuses a token for another data service with 401
      ([REQ-95](../requirements/asi.md#req-95)).

## Consequences

- If a QTSP needs attributes of two sources, it authorizes twice. The
  citizen logs in twice.
- The request page can name one source and its legal name
  ([REQ-91](../requirements/asi.md#req-91)).
- Every data service needs its own records in the Data Service
  Directory. It is open who registers them
  ([Q-67](../traceability/open-questions.md#q-67)).
- The demo has one data service: `brp`, with source `rvig`. A second data
  service exists only in unit tests.
- The authorization server takes its list of data services from the
  configuration (`AZSP_RESOURCES`). It does not take the list from the
  source descriptions ([ADR-0039](0039-asi-source-described-attributes.md),
  an open part of #592).
- It is open whether an ASIP for several sources makes GBO an
  intermediary in the sense of article 9(4)
  ([Q-37](../traceability/open-questions.md#q-37)).

## Considered options

The decision considered three other options:

- One endpoint for all sources that refuses requests across sources. Not
  chosen. With this option, the contract, the records, and the token
  audience do not show which source answers.
- One authorization for several resources, with a token per resource
  (RFC 8707 §2.2). Not chosen. This option saves the citizen a login.
  But the request page then shows several sources at once, and ETSI
  clients do not expect that.
- One token for several sources. Not chosen. With this option, the token
  is valid at a source that the citizen did not see.

## Traceability

- Requirements: [REQ-91](../requirements/asi.md#req-91),
  [REQ-94](../requirements/asi.md#req-94),
  [REQ-95](../requirements/asi.md#req-95),
  [REQ-99](../requirements/asi.md#req-99)
- Findings: [F-89](../traceability/findings.md#f-89) (open)
- Open questions: [Q-37](../traceability/open-questions.md#q-37),
  [Q-67](../traceability/open-questions.md#q-67)
- Standards feedback: [E3](../traceability/standards-feedback.md#e3)
- Demo increments: [SL-28](../traceability/increments.md#sl-28)
