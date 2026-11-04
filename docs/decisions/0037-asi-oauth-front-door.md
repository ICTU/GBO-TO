# ADR-0037: Authentic Source Interface as an OAuth front door per ETSI TS 119 478 clause 6.1

- Status: accepted (demo grade)
- Date: 2026-11-02
- Satisfies: eIDAS [article 45e](https://eur-lex.europa.eu/eli/reg/2014/910/oj), Implementing Regulation (EU) [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj) article 9, Implementing Regulation (EU) [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj) Annex IV, [GO: verificatie- en retrievedienst voor QTSPs](https://ictu.github.io/GBO-GO/main/#verificatie-en-retrievedienst-voor-qtsps-asi-provider), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte), [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
- Supersedes: [ADR-0029](0029-authentic-source-interface.md)
- Deliberation: [SL-28](../traceability/increments.md#sl-28), [F-80](../traceability/findings.md#f-80), [F-87](../traceability/findings.md#f-87), and demo epic [ICTU/GBO-demo#336](https://github.com/ICTU/GBO-demo/issues/336)
- Implemented in:
    - [services/asi-provider](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-provider): the ASIP.
    - [services/asi-authorization-server](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-authorization-server) and [services/asi-wallet-verifier](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-wallet-verifier).
    - [services/asi-discovery-stub](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/asi-discovery-stub): a stub.
    - [services/qtsp-reference](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/qtsp-reference): the reference client.
    - [asi0001.rego](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/asi/asi0001.rego): the rule.
    - The ASIP FSC peer in [fsc-infra/docker-compose.yml#L1664-L1669](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L1664-L1669).
    - The [conformance matrix](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/etsi-ts-119478.yaml) and [docs/asi-route.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/asi-route.md).

## Context and problem statement

Article 45e of eIDAS lets a qualified trust service provider (QTSP)
verify attributes of a citizen at an authentic source. The QTSP does
this at the request of that citizen. ETSI TS 119 478 V1.1.1 specifies
the interfaces.

Two regulations make clause 6.1.1 (verify) the legal interface: article
9 of Implementing Regulation 2025/1569, and Annex IV of Implementing
Regulation 2026/1735. From January 1, 2027, every verification result
must be sealed (article 9(4)). The regulations do not designate clause
6.1.3 (authorization) or clause 5 (discovery). For this reason, the
design of the authorization part is a national choice
([F-80](../traceability/findings.md#f-80)).

The reference architecture placed the interface "in front of" the FSC
and PEP-PDP chain ([ADR-0029](0029-authentic-source-interface.md)). The
demo showed that this placement is not correct. A QTSP is an EU party
with an access certificate and a register entitlement. A QTSP has no FSC
peer, no OIN, and no PKIoverheid certificate
([F-87](../traceability/findings.md#f-87)). GBO needs two parts:

- A trust model for the QTSP and the citizen that ends before FSC.
- A chain behind that trust model that a source can judge like any other
  consumer.

## Decision

GBO offers the Authentic Source Interface as an OAuth front door with
its own trust model. The generic chain starts behind it. The front door
works as follows:

1. Interface. The Authentic Source Interface Provider (ASIP) offers
   clause 6.1 only: 6.1.1 verify, 6.1.2 retrieve, and 6.1.3
   authorization with the scopes `verify` and `retrieve`. The ASIP does
   not offer clause 6.2 (ISO 15000)
   ([REQ-112](../requirements/asi.md#req-112),
   [Q-64](../traceability/open-questions.md#q-64)). Each authentic
   source gets its own data service under `/<data service>/authsrc-api`
   ([ADR-0038](0038-asi-data-service-per-source.md)).
2. Two services with separate keys. The ASIP and the authorization
   server are separate services. The ASIP gets the token keys of the
   authorization server from its RFC 8414 metadata.
3. The QTSP is an OAuth client. It is not an FSC participant. QTSP
   admission is not a PDP rule. The authorization server admits a QTSP
   as follows ([REQ-88](../requirements/asi.md#req-88),
   [REQ-89](../requirements/asi.md#req-89)):
    - The QTSP registers through RFC 7591. The QTSP seals the software
      statement with its certificate (`x5c`, `registryURI`).
    - The server verifies the chain against its trust anchors.
    - Then the server looks up the register entry. The entry must carry
      the entitlement `QEAA_Provider` and the `organizationIdentifier`
      of the certificate.
    - The client key is the certificate key.
    - The server repeats the lookup periodically. It deactivates a
      client without entitlement.
4. Login is approval. Before login, the citizen sees one request page
   ([REQ-91](../requirements/asi.md#req-91)). The page shows the legal
   name of the QTSP from the register, the operation, the source, and
   the attributes, if they are bound. The citizen approves by logging
   in, or refuses without login
   ([REQ-90](../requirements/asi.md#req-90)). The approval is one login
   per request: it is not a stored consent, and it has no relation to
   the toestemmingsregister. Approval in a wallet is not a legal basis
   ([F-83](../traceability/findings.md#f-83)).
5. Token. The authorization server uses the authorization code flow
   with PKCE S256 and `private_key_jwt`. It issues a DPoP-bound RFC 9068
   JWT (ES256, 10 minutes). The token carries the identification data
   and the means used (`acr`, `amr`)
   ([REQ-86](../requirements/asi.md#req-86)). The `resource` parameter
   names exactly one data service
   ([REQ-95](../requirements/asi.md#req-95)). As an option, the token is
   bound to the attributes
   ([ADR-0042](0042-asi-attribute-token-binding.md)).
6. The ASIP takes the citizen only from the token. The ASIP verifies the
   token and the DPoP proof before anything else
   ([REQ-87](../requirements/asi.md#req-87)). Then the ASIP sends one
   GraphQL query per request through its own FSC Outway, as peer `…1200`
   ([REQ-92](../requirements/asi.md#req-92),
   [REQ-46](../requirements/sources-identity.md#req-46)). The PDP of the
   source sees the ASIP as actor, and never the QTSP or the citizen. Rule
   ASI0001 grants the ASIP peer the fields behind the attributes, on
   service `brp` only.
7. Results. Per attribute, the ASIP answers `Match`, `NoMatch`,
   `MatchWithVariation`, or `Unknown`:
    - A verify response contains no source value
      ([REQ-85](../requirements/asi.md#req-85)).
    - `Unknown` means only that the source has no complete value
      ([REQ-84](../requirements/asi.md#req-84)).
    - If the chain does not answer, the result is 503 or 500, and never
      `Unknown` ([REQ-93](../requirements/asi.md#req-93)).
    - If a retrieve finds no value, the result is 404, with no partial
      result ([REQ-101](../requirements/asi.md#req-101)).
    - If a request has `mandate`, the result is 501
      ([REQ-114](../requirements/asi.md#req-114)).
8. Seal. The ASIP seals every successful response
   ([REQ-83](../requirements/asi.md#req-83)).
   [ADR-0041](0041-asi-seal-format.md) sets the format.
9. Discovery. The ASIP publishes a `dataService` record per attribute
   and data service. The contract of the data service names the metadata
   of the authorization server
   ([REQ-99](../requirements/asi.md#req-99),
   [REQ-100](../requirements/asi.md#req-100)).
10. Conformance. A conformance matrix gives every ETSI requirement ID a
    status and named tests. If an ID or a test is missing, CI fails.

## Consequences

- The ASIP is a channel adapter in the sense of
  [REQ-44](../requirements/authorization.md#req-44). The source decides
  with its own PDP. The source needs no ASI-specific logic.
- The source sees only the ASIP. The ASIP passes nothing about the QTSP
  into the chain, and it writes no LDV record. A citizen cannot see which
  QTSP verified data ([F-87](../traceability/findings.md#f-87)).
- Rule ASI0001 checks the actor, the service, and the field list. It
  also checks that the subject is a BSN, and not a placeholder. The rule
  does not check the token or the QTSP. The BSN is in the PDP input and
  in the decision log
  ([REQ-60](../requirements/logging-audit.md#req-60),
  [ADR-0043](0043-identifiers-out-of-pdp-input.md)).
- EUDI issuance does not replace retrieve, because the QTSP issues the
  QEAA, and GBO does not.
- QTSP admission depends on a register and on access certificates that
  do not exist on November 2, 2026. The demo uses a register file and
  test certificates ([F-85](../traceability/findings.md#f-85)).
- If a QTSP needs attributes of two sources, it authorizes twice
  ([ADR-0038](0038-asi-data-service-per-source.md)).
- The conformance matrix of v0.9.0 has 55 passed, 4 stub, 21 not
  applicable, and 1 failing. The failing item is
  REQ-ASIP-6.1.1.1-10-01: fuzzy matching asks for the value, and the
  ASIP returns none ([F-92](../traceability/findings.md#f-92),
  [Q-29](../traceability/open-questions.md#q-29)).
- The route runs locally only.
  [ICTU/GBO-demo#594](https://github.com/ICTU/GBO-demo/issues/594)
  tracks a deployment to the simulation environment with an external
  QTSP.

## Considered options

The decision considered four other options:

- Skip retrieve, as ADR-0029 proposed. Not chosen. A QTSP needs the
  value to issue a QEAA. The EUDI issuance chain does not replace that,
  because the QTSP issues the attestation, and GBO does not.
- Make the QTSP an FSC participant. Not chosen. QTSPs are EU parties
  with access certificates and register entitlements. Clause 6.1 is
  HTTPS with OAuth.
- Admit the QTSP in the PDP of the source (a Trusted List check as a
  rule). Not chosen. The PDP sees only the FSC actor. Admission belongs
  where the token is issued.
- Offer clause 6.2 (ISO 15000) as well. Not in demo v0.9.0:
  [Q-64](../traceability/open-questions.md#q-64) holds this point open.

## Open points

### Security profile of the authorization server

The security profile is open
([Q-66](../traceability/open-questions.md#q-66)). ETSI leaves the
profile open and conflicts with FAPI 2.0 on PAR and RS256
([F-84](../traceability/findings.md#f-84),
[E8](../traceability/standards-feedback.md#e8)).

The demo uses
`private_key_jwt` and DPoP. It has no mTLS client authentication, no
PAR, and no refresh tokens. The authorization server signs with ES256.
The ASIP also accepts RS256, because RFC 9068 requires it.
[security-considerations.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/security-considerations.md)
lists the demo choices.

These points of the profile are open:

- The authorization response has no `iss` (RFC 9207). A QTSP that uses
  several ASIPs has no mix-up defense
  ([F-96](../traceability/findings.md#f-96),
  [E9](../traceability/standards-feedback.md#e9)).
- Tokens stay valid for up to 10 minutes after the withdrawal of the
  entitlement ([Q-41](../traceability/open-questions.md#q-41),
  [E10](../traceability/standards-feedback.md#e10)).
- If the register is unreachable during a re-check, the client stays
  active ([Q-34](../traceability/open-questions.md#q-34)).
- Which identifier links the access certificate to the register entry
  ([Q-35](../traceability/open-questions.md#q-35))?

### Citizen identification at the authorization server

Citizen identification is open
([Q-36](../traceability/open-questions.md#q-36)). The demo accepts two
means:

- The NL Wallet over OpenID4VP, through the nl-wallet
  `verification_server`. It asks only the PID attributes of its
  registration, and it requires a BSN in `urn:eudi:pid:nl:1`
  ([REQ-102](../requirements/asi.md#req-102)). The trusted PID issuers
  are a fixed list, and not a trusted list. The verifier accepts a PID
  with an undetermined revocation status.
- A DigiD mock (stub). DigiD supplies only the BSN
  ([F-88](../traceability/findings.md#f-88)).

These related points are open:

- The NL PID has no place of birth, but the implementing regulation
  makes it mandatory ([F-94](../traceability/findings.md#f-94)).
- The BSN is in plain text in the token, so the QTSP can read it
  ([F-86](../traceability/findings.md#f-86),
  [E7](../traceability/standards-feedback.md#e7),
  [ICTU/GBO-demo#595](https://github.com/ICTU/GBO-demo/issues/595)).
- Nothing links the citizen who logs in at the QTSP to the citizen who
  logs in at the authorization server
  ([F-93](../traceability/findings.md#f-93),
  [Q-40](../traceability/open-questions.md#q-40),
  [E6](../traceability/standards-feedback.md#e6)).
- The same-device wallet login did not run on a phone in demo v0.9.0
  ([ICTU/GBO-demo#596](https://github.com/ICTU/GBO-demo/issues/596)).
- [P-05](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
  decides which means are recognized at the correct assurance level.

### Role, legal basis, and registration

These points are open:

- Who designates the ASI intermediary, and what is the role of GBO
  ([Q-28](../traceability/open-questions.md#q-28),
  [Q-37](../traceability/open-questions.md#q-37))? The
  [besluitregister](https://ictu.github.io/GBO-PSA/main/vraagstukken/#besluitregister)
  holds this point as PSA open decision B-14.
- What is the legal basis to verify for private QTSPs, and does the ASIP
  return the value on a match
  ([Q-29](../traceability/open-questions.md#q-29))?
- Who registers the data services in the catalogue of attributes and
  the Discover Interface, and how does the contract name the
  authorization server ([Q-31](../traceability/open-questions.md#q-31),
  [Q-67](../traceability/open-questions.md#q-67),
  [Q-39](../traceability/open-questions.md#q-39),
  [F-91](../traceability/findings.md#f-91))?
- How do requests on behalf of another person work
  ([Q-65](../traceability/open-questions.md#q-65))?

## Traceability

- Requirements: [REQ-83](../requirements/asi.md#req-83),
  [REQ-84](../requirements/asi.md#req-84),
  [REQ-85](../requirements/asi.md#req-85),
  [REQ-86](../requirements/asi.md#req-86),
  [REQ-87](../requirements/asi.md#req-87),
  [REQ-88](../requirements/asi.md#req-88),
  [REQ-89](../requirements/asi.md#req-89),
  [REQ-90](../requirements/asi.md#req-90),
  [REQ-91](../requirements/asi.md#req-91),
  [REQ-92](../requirements/asi.md#req-92),
  [REQ-93](../requirements/asi.md#req-93),
  [REQ-99](../requirements/asi.md#req-99),
  [REQ-100](../requirements/asi.md#req-100),
  [REQ-101](../requirements/asi.md#req-101),
  [REQ-102](../requirements/asi.md#req-102),
  [REQ-112](../requirements/asi.md#req-112),
  [REQ-114](../requirements/asi.md#req-114),
  [REQ-44](../requirements/authorization.md#req-44),
  [REQ-46](../requirements/sources-identity.md#req-46),
  [REQ-60](../requirements/logging-audit.md#req-60). Profile:
  [GBO profile on ETSI TS 119 478](../requirements/asi.md#asi-profile)
- Findings: [F-80](../traceability/findings.md#f-80) (open),
  [F-83](../traceability/findings.md#f-83) (open),
  [F-84](../traceability/findings.md#f-84) (open),
  [F-85](../traceability/findings.md#f-85) (open),
  [F-86](../traceability/findings.md#f-86) (open),
  [F-87](../traceability/findings.md#f-87) (open),
  [F-88](../traceability/findings.md#f-88) (open),
  [F-91](../traceability/findings.md#f-91) (open),
  [F-92](../traceability/findings.md#f-92) (open),
  [F-93](../traceability/findings.md#f-93) (open),
  [F-94](../traceability/findings.md#f-94) (open),
  [F-96](../traceability/findings.md#f-96) (open)
- Open questions: [Q-28](../traceability/open-questions.md#q-28),
  [Q-29](../traceability/open-questions.md#q-29),
  [Q-31](../traceability/open-questions.md#q-31),
  [Q-34](../traceability/open-questions.md#q-34),
  [Q-35](../traceability/open-questions.md#q-35),
  [Q-36](../traceability/open-questions.md#q-36),
  [Q-37](../traceability/open-questions.md#q-37),
  [Q-39](../traceability/open-questions.md#q-39),
  [Q-40](../traceability/open-questions.md#q-40),
  [Q-41](../traceability/open-questions.md#q-41),
  [Q-64](../traceability/open-questions.md#q-64),
  [Q-65](../traceability/open-questions.md#q-65),
  [Q-66](../traceability/open-questions.md#q-66),
  [Q-67](../traceability/open-questions.md#q-67)
- Standards feedback: [E6](../traceability/standards-feedback.md#e6),
  [E7](../traceability/standards-feedback.md#e7),
  [E8](../traceability/standards-feedback.md#e8),
  [E9](../traceability/standards-feedback.md#e9),
  [E10](../traceability/standards-feedback.md#e10)
- Demo increments: [SL-28](../traceability/increments.md#sl-28)
