# Authentic Source Interface requirements

In the Authentic Source Interface (ASI) route, a qualified trust service
provider (QTSP) verifies or retrieves attributes of a citizen at an
authentic source. The QTSP does this at the request of that citizen. eIDAS
[article 45e](https://eur-lex.europa.eu/eli/reg/2014/910/oj) gives the QTSP this right. The Authentic Source
Interface Provider (ASIP) offers the interface. Its authorization server
admits QTSPs and lets the citizen approve each request.

The interface follows [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) V1.1.1, clause 6.1.
Article 9 of Implementing Regulation (EU) [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj) and Annex IV
of Implementing Regulation (EU) [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj) make clause 6.1.1 the
legal interface for verification. Annex IV and the seal obligation of
article 9(4) apply from January 1, 2027.

The requirements on the ASIP and its authorization server cover these
topics:

- the verify and retrieve interface
- the seal
- the authorization server
- the admission of QTSPs
- the request page with citizen identification
- the chain behind the ASIP, with one data service per source
- discovery

[F-80](../traceability/findings.md#f-80) describes the legal frame. [F-84](../traceability/findings.md#f-84) to [F-89](../traceability/findings.md#f-89)
describe the open design choices.

Evidence links to gbo-demo point at two versions. A link at `v0.9.0`
shows the code of demo v0.9.0. A link at commit `819f3eb` shows the code
at the time of the review of the requirement. Use that link as historical
evidence, because the file changed or moved after that commit.

## GBO profile on ETSI TS 119 478 {#asi-profile}

The specification for a Dutch ASIP is ETSI TS 119 478 V1.1.1, as Annex IV
of Implementing Regulation (EU) 2026/1735 adapts it (Implementing
Regulation 2025/1569, article 9(2a)). The profile does not repeat that
text. For each clause, the profile records two things:

- what GBO chooses, adds, or interprets on top of ETSI
- where that choice is recorded: in a requirement on this page, an open
  question, or a finding

A requirement that the profile does not name follows ETSI unchanged.

The profile is for the build of the ASIP and its authorization server.
That build does not reuse the code of the demo ASIP. The content for each
requirement comes from two documents of the demo: the conformance matrix
([`etsi-ts-119478.yaml`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/etsi-ts-119478.yaml)) and the
documentation of the ASI route ([`asi-route.md`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/asi-route.md)).
If nobody decided on a choice of the demo, the profile records it as an
open question and does not make it a requirement.

- **Source**: design. The source is the line on ETSI TS 119 478 in
  "Afspraken en standaarden" of [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte). The profile fills the open
  point "PubEAA-/ASI-profielen" from the summary of S11. Matters about the
  ASI provider and its conditions belong to PSA open decision
  [B-14](https://ictu.github.io/GBO-PSA/main/vraagstukken/).

### Categories

The profile puts each GBO choice in one of eight categories:

| Code | Meaning |
|---|---|
| **K** | a choice where ETSI leaves room |
| **N** | not applicable because of a GBO choice |
| **R** | requirements on a role outside the ASIP and its authorization server (DIP, TSP) |
| **A** | an addition: GBO requires something that ETSI does not specify |
| **I** | an interpretation, or a conflict in the text |
| **X** | applies, but depends on an external facility |
| **O** | applies to the operator and not to the software |
| **open** | no decision |

### Per clause

For each ETSI clause, the profile gives the ETSI requirements, the
category, the GBO choice, and where the choice is recorded:

| Clause | ETSI requirements | Cat. | GBO choice | Recorded in |
|---|---|---|---|---|
| 4.3 | REQ-ASIP-4.3-04 | **K** | only the interface of clause 6.1 (HTTP, OAuth) | [REQ-112](#req-112), [Q-64](../traceability/open-questions.md#q-64) |
| 4.4, 6.2, Annex C | REQ-AZP-4.4-02, REQ-ASIP-6.2.\*, REQ-ASIP-C-01 | **N** | follows from REQ-112 | [REQ-112](#req-112) |
| 4.3 | REQ-ASIP-4.3-03 | **X** | a legitimate user and an entitled QTSP depend on the identification means and the register of relying parties | [REQ-88](#req-88), [REQ-102](#req-102), [Q-36](../traceability/open-questions.md#q-36) |
| 4.2 | — | **A** | the ASIP queries the source through the chain, with one query per request, and the source judges that query | [REQ-92](#req-92), [Q-38](../traceability/open-questions.md#q-38) |
| 5 | REQ-DIP-\*, REQ-TSP-5.4-\* | **R** | these requirements are for the common OOTS services of the Commission. How Dutch data services get there is open. | [Q-67](../traceability/open-questions.md#q-67) |
| 5.3 | — | **A** | the ASIP publishes a `dataService` record for each attribute and data service | [REQ-99](#req-99) |
| 5.3 | — | **I** | the contract names the metadata of the authorization server. ETSI gives no field for it. | [REQ-100](#req-100), [Q-39](../traceability/open-questions.md#q-39), [F-91](../traceability/findings.md#f-91) |
| 6.1.1.1 | REQ-ASIP-6.1.1.1-06-01, -06-02-01 | **X** | attribute IDs and value schemas come from the EU catalogue of attributes. Until that catalogue exists, the source describes them. | [Q-38](../traceability/open-questions.md#q-38) |
| 6.1.1.1 | REQ-ASIP-6.1.1.1-09 | **K** | the ASIP supports attribute fragments | [REQ-115](#req-115) |
| 6.1.1.1 | REQ-ASIP-6.1.1.1-10 | **K** | fuzzy matching only on text values, with published rules | [REQ-113](#req-113), [Q-70](../traceability/open-questions.md#q-70) |
| 6.1.1.1 | REQ-ASIP-6.1.1.1-10-01 | **I** | conflicts with Annex IV, which makes the value optional | [REQ-85](#req-85), [Q-29](../traceability/open-questions.md#q-29), [E2](../traceability/standards-feedback.md#e2) |
| 6.1.1, 6.1.2 | REQ-ASIP-6.1.1.1-11 to -13, -6.1.1.2-10, -11, -6.1.2.1-04, -6.1.2.2-05, -05-01 | **K** | a request on behalf of another person (`mandate`) gets 501 | [REQ-114](#req-114), [Q-65](../traceability/open-questions.md#q-65) |
| 6.1.1.2 | REQ-ASIP-6.1.1.2-04 | **I** | `Unknown` means that the source has no value, or no complete value. ETSI takes precedence over the ARF. | [REQ-84](#req-84) |
| 6.1.1.2 | REQ-ASIP-6.1.1.2-04-01 to -03, -06-03, -06-04-\* | **K** | no value in the response | [REQ-85](#req-85), [Q-29](../traceability/open-questions.md#q-29) |
| 6.1.1.2 | REQ-ASIP-6.1.1.2-08, -6.1.2.2-04 | **I** | one authentic source per response, so one data service per source | [REQ-94](#req-94), [F-89](../traceability/findings.md#f-89) |
| 6.1.2.2 | REQ-ASIP-6.1.2.2-02-01 | **I** | a retrieve without a value in the source gets 404 and no partial result | [REQ-101](#req-101) |
| 6.1 | — | **open** | synchronous processing only. ETSI has deferred responses only in clause 6.2. | [Q-64](../traceability/open-questions.md#q-64) |
| 6.1 | — | **A** | a chain that does not answer gives 500 or 503 and never `Unknown` | [REQ-93](#req-93) |
| 6.1 | — | **A + X** | the ASIP seals every successful response (Implementing Regulation 2025/1569, article 9(4)). The format is open. The qualified seal certificate is external. | [REQ-83](#req-83), [Q-32](../traceability/open-questions.md#q-32), [Q-17](../traceability/open-questions.md#q-17) |
| 6.1.3.1 | REQ-AZSP-6.1.3.1-02, -03 | **X** | identification with the EUDI wallet. Other means are open. | [REQ-90](#req-90), [REQ-102](#req-102), [Q-36](../traceability/open-questions.md#q-36) |
| 6.1.3.1 | REQ-AZSP-6.1.3.1-05, -06 | **open** | client authentication (mTLS, or `private_key_jwt`, or both) and token binding (mTLS or DPoP) | [Q-66](../traceability/open-questions.md#q-66), [F-84](../traceability/findings.md#f-84) |
| 6.1.3.1 | REQ-AZSP-6.1.3.1-08 | **I** | the identification data in the token. The NL PID has no place of birth. | [REQ-86](#req-86), [F-86](../traceability/findings.md#f-86), [F-94](../traceability/findings.md#f-94) |
| 6.1.3.1 | — | **A** | `resource` is mandatory, with one token for one data service | [REQ-95](#req-95) |
| 6.1.3.1 | — | **A** | optional binding of the token to the attributes (`authorization_details`) | [REQ-103](#req-103) |
| 6.1.3.1 | — | **A** | the citizen sees the QTSP, the source, and the operation before he logs in | [REQ-90](#req-90), [REQ-91](#req-91) (absorbs the former REQ-96) |
| 6.1.3.2 | REQ-AZSP-6.1.3.2-01, -02 | **A + X** | registration with a software statement of the QTSP. The entitlement is in the register. Access certificates are external. | [REQ-88](#req-88), [F-85](../traceability/findings.md#f-85) |
| 6.1.3.2 | — | **A + open** | a periodic re-check of the entitlement. The behavior when the register is unreachable is open. | [REQ-89](#req-89), [Q-34](../traceability/open-questions.md#q-34) |
| 6.1.3.4 | REQ-AZSP-6.1.3.4-01 | **I + open** | GBO weighs each security consideration. The security profile, `iss`, and tokens after withdrawal are open. | [Q-66](../traceability/open-questions.md#q-66), [F-96](../traceability/findings.md#f-96), [Q-41](../traceability/open-questions.md#q-41) |
| 6.1.3.4 | REQ-AZSP-6.1.3.4-02 | **O** | follows ETSI (an ISMS) and applies to the operator. Who the operator is stays open. | [Q-37](../traceability/open-questions.md#q-37) |
| 6.1.3 | REQ-TSP-6.1.3.\* | **R** | requirements on the QTSP | — |
| — | — | **R** | the QTSP identifies the citizen itself, and issues only to that citizen. This is a duty of the QTSP under ETSI and eIDAS. GBO only checks that the QTSP is on the trusted list as qualified. | [REQ-88](#req-88) |

### External dependencies

Some parts are a stub in the demo. For the build, each of these parts is
a facility that must come from outside. They are not requirements on the
ASIP. The profile needs these external facilities to apply in full:

- the register of relying parties, and the API to look up the entitlement
  of a QTSP ([F-85](../traceability/findings.md#f-85))
- access certificates for QTSPs according to ETSI TS 119 411-8
  ([Q-35](../traceability/open-questions.md#q-35))
- a qualified seal certificate for the ASIP ([Q-17](../traceability/open-questions.md#q-17))
- DigiD or another identification means next to the EUDI wallet
  ([Q-36](../traceability/open-questions.md#q-36))
- the EU catalogue of attributes, with IDs and value schemas
  ([Q-38](../traceability/open-questions.md#q-38))
## REQ-83: Every ASIP verification result is sealed {#req-83}

> The ASIP MUST seal every successful response to verify and to retrieve. With
> only the received response and the trusted lists, the QTSP can then
> establish that the response comes unchanged from this ASIP. The seal MUST
> cover the response exactly and carry the certificate chain. The seal MUST
> be at least an advanced electronic seal. This seal MUST be based on a
> qualified seal certificate of the responsible public sector body or of
> the designated intermediary.

| Case | Outcome |
|---|---|
| verify, 200 | sealed (code) |
| retrieve, 200 | sealed (code) |
| error response (400, 401, 404, 500, 501, 503) | not sealed (code, design choice) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design for verify, and derived for retrieve. The
      requirement has these sources:
        - Article 9(4) of Implementing Regulation (EU)
          [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj). Article 1(3)(b) of Implementing Regulation (EU)
          [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj) replaces it from January 1, 2027 ("the
          verification result shall be signed or sealed … using at least … an
          advanced electronic seal based on a qualified certificate").
        - [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) ("ETSI-profielen voor gekwalificeerde zegels").
        - For retrieve, the requirement serves
          [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte). A QTSP can put a retrieved value in a
          qualified attestation. It must then show in the same way that the
          value comes from the source.
    - **Addressee**: GBO-delivered component: the ASIP. Interface agreement:
      the form of the seal, for every ASIP.
    - **Evidence**: [ICTU/GBO-demo#498](https://github.com/ICTU/GBO-demo/issues/498), [PR #499](https://github.com/ICTU/GBO-demo/pull/499). Code and tests:
        - The seal is in [`seal.go#L18-L57`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/seal/seal.go#L18-L57).
        - Only a successful response gets the seal, in
          [`handler.go#L393-L408`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L393-L408).
          Errors get no seal, in
          [`#L410-L420`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L410-L420).
        - The header is an addition to the contract, in
          [`completions.json#L25-L33`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/openapi/completions.json#L25-L33).
        - The tests are in [`handler_test.go#L240-L254`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L240-L254),
          [`#L310-L312`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L310-L312),
          and [`contract_test.go#L120-L121`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/contract_test.go#L120-L121).
        - Code at v0.9.0: [`handler.go#L402-L417`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L402-L417),
          tested in [`handler_test.go#L238-L252`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L238-L252).
    - **Related**: [REQ-94](#req-94), [REQ-112](#req-112), [F-80](../traceability/findings.md#f-80),
      [Q-17](../traceability/open-questions.md#q-17), [Q-28](../traceability/open-questions.md#q-28), [Q-32](../traceability/open-questions.md#q-32),
      [ADR 0041](../decisions/0041-asi-seal-format.md).
    - **Notes**:
        - The seal format is a design choice. It is a detached JWS (RFC 7515,
          Annex F) over the exact body, in the header `X-JWS-Signature`. It
          uses ES256 and carries the chain in `x5c`.
        - The body stays plain JSON, as the ETSI OpenAPI prescribes.
        - ETSI TS 119 478 defines no seal on the response. The format must be
          the same for all ASIPs ([Q-32](../traceability/open-questions.md#q-32), [E4](../traceability/standards-feedback.md#e4)).
        - An error response is not a verification result, so it gets no seal.
        - The demo seals with a development certificate. Who holds the
          qualified seal certificate is [Q-17](../traceability/open-questions.md#q-17). Who the intermediary
          is, is [Q-28](../traceability/open-questions.md#q-28).

## REQ-84: `Unknown` only means the source has no (complete) value {#req-84}

> If the source has no value, or no complete value, for this citizen, the
> ASIP MUST answer an attribute or fragment with `Unknown`. It MUST NOT
> give `NoMatch` in that case. An attribute that the data service does not
> deliver MUST get 404 ([REQ-94](#req-94)) and MUST NOT get `Unknown`. A
> source that does not answer MUST NOT get `Unknown` either ([REQ-93](#req-93)).

| Case | Outcome |
|---|---|
| The source has an equal value | `Match` (code) |
| The source has a different value | `NoMatch` (code) |
| The source does not know the BSN | `Unknown` (code) |
| The source has no value for this citizen, for example no residential address because he is not a resident | `Unknown` (code) |
| The source has an incomplete value: an address without street, house number, postal code, or town | `Unknown` (code) |
| An attribute that this data service does not deliver | 404, and the ASIP does not ask the source (code) |
| The source is unreachable, or the chain refuses | 503 or 500, see [REQ-93](#req-93) (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-ASIP-6.1.1.2-04, item 4 ("no authentic
          source data was available to determine a match for the attribute
          for the user").
        - Annex IV of Implementing Regulation (EU)
          [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj), which designates clause 6.1.1.

        The ARF (QTSPAS_02) calls this case `no match`. GBO follows ETSI,
        because the regulation designates ETSI and the ARF does not bind. GBO
        interprets an incomplete value as no value.

    - **Addressee**: interface agreement: every ASIP. GBO-delivered component:
      the ASIP and its source connection.
    - **Evidence**: [PR #499](https://github.com/ICTU/GBO-demo/pull/499), [PR #527](https://github.com/ICTU/GBO-demo/pull/527), [PR #529](https://github.com/ICTU/GBO-demo/pull/529).
      Historical code and tests:
        - No value gives `Unknown` in
          [`service.go#L169-L206`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service.go#L169-L206).
        - The source gives no value in
          [`source.go#L74-L108`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source.go#L74-L108)
          and [`#L147-L161`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source.go#L147-L161).
        - An attribute of another source is not in the catalogue
          ([`catalogue.go#L8-L10`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/catalogue.go#L8-L10)).
        - The tests are in [`handler_test.go#L144-L165`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L144-L165),
          [`token_test.go#L252-L258`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L252-L258),
          [`source_test.go#L98-L120`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source_test.go#L98-L120),
          [`#L219-L226`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source_test.go#L219-L226),
          [`service_test.go#L66-L80`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service_test.go#L66-L80),
          and [`#L133-L148`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service_test.go#L133-L148).

        Code at v0.9.0: steps 1 to 5 of [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592) removed the
        BRP code adapter ([PR #611](https://github.com/ICTU/GBO-demo/pull/611), [PR #613](https://github.com/ICTU/GBO-demo/pull/613), [PR #620](https://github.com/ICTU/GBO-demo/pull/620),
        [PR #622](https://github.com/ICTU/GBO-demo/pull/622), [PR #623](https://github.com/ICTU/GBO-demo/pull/623), [PR #624](https://github.com/ICTU/GBO-demo/pull/624)). The ASIP builds
        each attribute from the `asi` description that the source publishes.
        An attribute without a value gets `Unknown` in
        [`service.go#L166-L179`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L166-L179). An
        attribute that the description does not name gets 404 in
        [`#L238-L251`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L238-L251). The test is in
        [`handler_test.go#L140-L161`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L140-L161).

    - **Related**: [REQ-93](#req-93), [REQ-94](#req-94), [REQ-101](#req-101),
      [REQ-113](#req-113), [F-80](../traceability/findings.md#f-80), [Q-38](../traceability/open-questions.md#q-38).
    - **Notes**: the value schema of the attribute defines what a complete
      value is. Until the EU catalogue of attributes exists, the source
      describes it ([Q-38](../traceability/open-questions.md#q-38), [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592)). `Unknown`
      also tells something about the person, for example that he has no Dutch
      residential address. The citizen approved the request himself
      ([REQ-90](#req-90)).

## REQ-85: The verify response contains no value from the source {#req-85}

> On `Match` and `MatchWithVariation`, the ASIP MUST NOT return an
> `attributeValue`, and for fragments no `fragmentValue`. The QTSP only
> learns whether its value is correct.

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: derived. The requirement serves
      [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
      (minimal data processing). If the response carries the value on
      `MatchWithVariation`, the QTSP learns the value from the source. The
      QTSP does not need that value for the verification. The legal frame is
      as follows:
        - Annex IV of Implementing Regulation (EU) [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj) makes the
          value optional (REQ-ASIP-6.1.1.2-04-01 and -06-04-01).
        - Unchanged [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) requires the value.
    - **Addressee**: interface agreement: every ASIP. GBO-delivered component:
      the ASIP.
    - **Evidence**: [ICTU/GBO-demo#498](https://github.com/ICTU/GBO-demo/issues/498), [PR #499](https://github.com/ICTU/GBO-demo/pull/499). Code and tests:
        - The response has no value field
          ([`handler.go#L177-L192`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L177-L192),
          [`service.go#L100-L103`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service.go#L100-L103)).
        - The test is in [`handler_test.go#L112-L136`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L112-L136),
          with [`#L418-L425`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L418-L425).
        - The conformance matrix has the rows
          [`etsi-ts-119478.yaml#L173-L181`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/etsi-ts-119478.yaml#L173-L181)
          and [`#L132-L135`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/etsi-ts-119478.yaml#L132-L135).
        - Code at v0.9.0: [`handler.go#L186-L201`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L186-L201).
    - **Related**: [REQ-113](#req-113), [F-80](../traceability/findings.md#f-80), [F-92](../traceability/findings.md#f-92),
      [Q-29](../traceability/open-questions.md#q-29).
    - **Notes**: sub-questions 2 and 3 of [Q-29](../traceability/open-questions.md#q-29) are open.
        - REQ-ASIP-6.1.1.1-10-01 still requires the source value from an ASIP
          that supports fuzzy matching. Annex IV does not adapt that
          requirement.
        - Read literally, the ASIP does not meet REQ-ASIP-6.1.1.1-10-01
          ([E2](../traceability/standards-feedback.md#e2)). The conformance matrix marks the row `failing`.
        - On `Match`, the value is equal to the value of the QTSP. Only on
          `MatchWithVariation` does the omission of the value share less data.
          For that reason, on `MatchWithVariation` the QTSP records its own
          value.

## REQ-86: The access token carries the citizen's identification data and the means used to identify him {#req-86}

> The authorization server MUST issue access tokens as a JWT according to
> RFC 9068. Each token MUST be bound to a key of the QTSP and MUST carry
> the scope for each operation (`verify`, `retrieve`). The token MUST
> carry the identification data of the citizen as the identification means
> delivers them. It MUST always carry the BSN. Of the mandatory PID
> attributes, it MUST carry only those that the means delivers.
>
> The token MUST name the means in `acr` and `amr`. The authorization
> server MUST establish that means itself, and MUST NOT copy what the
> means declares. An identification without a BSN MUST NOT lead to a
> token. The BSN in the token MUST be readable only for the ASIP. A QTSP
> without BSN authority that holds the token MUST NOT be able to read it.

| Case | Outcome |
|---|---|
| Logged in with DigiD (mock) | the BSN, with `acr` and `amr` set to `digid-mock`, and no PID attributes (code) |
| A QTSP without BSN authority reads the token | no readable BSN. *This is a proposal. In the demo, the BSN in the token is readable.* |
| Logged in with the NL Wallet | the BSN, `family_name`, `given_name`, `birthdate`, and `nationalities`, with `acr` and `amr` set to `nl-wallet`. No place of birth ([F-94](../traceability/findings.md#f-94)) (code). |
| The means delivers no BSN | no authorization code. The citizen sees the request page again, and the transaction stays (code). |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-AZSP-6.1.3.1-06 (token binding), -08 (JWT
          according to RFC 9068 "which shall contain the required
          identification data of the user"), and clause 6.1.3.2 (the scopes).
        - Article 9(3) of Implementing Regulation (EU) [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj) ("the
          verification request shall set out the attributes and the
          identification data of the subject"). NOTE 6 of -08 refers to this
          article.
        - [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte). Implementing Regulation 2026/1735 does not
          designate clause 6.1.3. S11 names TS 119 478 as a whole.
        - For a BSN that only the ASIP can read:
          [PSA S03](https://ictu.github.io/GBO-PSA/main/capabilities/#s03-burgeridentificatie-pseudonimisering)
          ("een private afnemer zonder wettelijke BSN-bevoegdheid ontvangt een
          partijspecifieke identiteit of pseudoniem") and
          [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
        - For the means in the token, the requirement is derived. It serves
          [P-05](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/):
          the ASIP and the audit must see with which means, and so at which
          level, the citizen was identified.
    - **Addressee**: GBO-delivered component: the authorization server.
      Interface agreement: the content of the token between the authorization
      server and the ASIP.
    - **Evidence**: [ICTU/GBO-demo#605](https://github.com/ICTU/GBO-demo/issues/605) is not built in demo v0.9.0. A BSN that
      only the ASIP can read is not built either:
      [ICTU/GBO-demo#595](https://github.com/ICTU/GBO-demo/issues/595) (open). The built parts come from
      [ICTU/GBO-demo#503](https://github.com/ICTU/GBO-demo/issues/503), [#544](https://github.com/ICTU/GBO-demo/issues/544),
      [#546](https://github.com/ICTU/GBO-demo/issues/546), [PR #504](https://github.com/ICTU/GBO-demo/pull/504), [PR #524](https://github.com/ICTU/GBO-demo/pull/524),
      [PR #545](https://github.com/ICTU/GBO-demo/pull/545), and [PR #552](https://github.com/ICTU/GBO-demo/pull/552) (with a run with the real NL
      Wallet). Code and tests:
        - The issuance is in
          [`tokens.go#L53-L85`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/tokens.go#L53-L85).
        - The DPoP binding at the token request is in
          [`service.go#L326`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service.go#L326).
        - The core establishes the means, and allows no identification without
          a BSN, in
          [`identification.go#L45-L51`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/identification.go#L45-L51)
          and [`#L358-L363`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/identification.go#L358-L363).
        - The tests are in [`handler_test.go#L62-L122`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/handler_test.go#L62-L122)
          (DigiD), [`wallet_test.go#L243-L268`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/wallet_test.go#L243-L268)
          (NL Wallet), and [`handler_test.go#L138-L149`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/handler_test.go#L138-L149)
          (`sub`).
        - The conformance claim is in
          [`etsi-ts-119478.yaml#L371-L377`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/etsi-ts-119478.yaml#L371-L377).
    - **Related**: [REQ-87](#req-87), [REQ-95](#req-95), [REQ-102](#req-102),
      [REQ-103](#req-103), [F-84](../traceability/findings.md#f-84), [F-86](../traceability/findings.md#f-86), [F-88](../traceability/findings.md#f-88),
      [F-94](../traceability/findings.md#f-94), [Q-33](../traceability/open-questions.md#q-33), [Q-36](../traceability/open-questions.md#q-36), [Q-66](../traceability/open-questions.md#q-66).
    - **Notes**: design choices:
        - The binding is DPoP (RFC 9449) and not mTLS ([Q-66](../traceability/open-questions.md#q-66)).
        - The token has a lifetime of ten minutes.
        - The `sub` differs for each token.
        - The PID attributes use the names of the IANA JWT Claims Registry.
          The SD-JWT VC encoding of the PID also uses these names.
        - The BSN has a provisional claim name.

        GBO interprets -08 so that the token with DigiD carries only the BSN
        ([F-88](../traceability/findings.md#f-88), [Q-36](../traceability/open-questions.md#q-36)). How the claims become readable only for
        the ASIP is a design choice, for example encryption for the ASIP
        (RFC 9068 §6). See [ICTU/GBO-demo#595](https://github.com/ICTU/GBO-demo/issues/595) and [F-86](../traceability/findings.md#f-86). With the NL
        Wallet, the demo puts `place_of_birth` as an empty object in the token
        ([`tokens.go#L73-L78`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/tokens.go#L73-L78)).
        The requirement asks to leave it out.

## REQ-87: The ASIP takes the citizen only from a valid token bound to the QTSP that covers the operation {#req-87}

> On every verify and retrieve request, before any other check, the ASIP
> MUST validate the access token according to RFC 9068 §4 (signature with
> a key of the authorization server, issuer, audience, validity). It MUST
> validate the binding to the key of the QTSP with a valid DPoP proof for
> this request according to RFC 9449. It MUST check that the scope covers
> the operation. The identification data of the citizen MUST come from
> that token, never from the request. Every authentication or
> authorization error MUST be 401, with a `WWW-Authenticate` challenge. If
> the keys of the authorization server are not available, the ASIP MUST
> give 503.

| Case | Outcome |
|---|---|
| No token | 401, challenge without an error code (code) |
| Signature, issuer, audience, expiry, or `typ` is wrong, or the token has no `cnf` or no BSN | 401 `invalid_token` (code) |
| No proof | 401 `invalid_request` (code) |
| Proof invalid, reused, or with another key than `cnf.jkt` | 401 `invalid_dpop_proof` (code) |
| The scope does not cover the operation | 401 `insufficient_scope`, with the scope in the challenge (code) |
| The token names attributes and the request asks another attribute | 401 `insufficient_scope` ([REQ-103](#req-103)) (code) |
| An invalid token and an invalid request | 401: the token comes first (code) |
| Keys of the authorization server not available | 503 (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-ASIP-6.1.1.2-12 (401 "due to an
          authentication or authorization error"). Implementing Regulation
          (EU) [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj) designates clause 6.1.1.
        - ETSI REQ-ASIP-4.3-03 ("access controls … to determine that the
          requester is a trust service provider and is acting at the request
          of a legitimate user").
        - [RFC 9068](https://www.rfc-editor.org/rfc/rfc9068) §4, and
          [RFC 9449](https://www.rfc-editor.org/rfc/rfc9449) §4.3 and §7.
        - [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) ("uitgifte, verificatie en retrieval gebruiken
          passende authenticatie, autorisatie en logging").
        - For the 503, the requirement is derived. It serves
          [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte): a 401 blames the QTSP for a failure on
          the side of the ASIP.
    - **Addressee**: GBO-delivered component: the ASIP. Interface agreement:
      every ASIP.
    - **Evidence**: [ICTU/GBO-demo#503](https://github.com/ICTU/GBO-demo/issues/503), [PR #504](https://github.com/ICTU/GBO-demo/pull/504). Code and tests:
        - The check is in [`accesstoken.go#L112-L175`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/accesstoken/accesstoken.go#L112-L175)
          and [`dpop.go#L35-L80`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/accesstoken/dpop.go#L35-L80).
        - The citizen from the token, the 401, and the 503 are in
          [`handler.go#L211-L249`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L211-L249).
        - The 503 is an addition to the contract, in
          [`completions.json#L86-L95`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/openapi/completions.json#L86-L95).
        - The tests are in [`token_test.go#L34-L109`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L34-L109),
          [`#L158-L231`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L158-L231),
          [`#L233-L250`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L233-L250),
          and [`#L260-L296`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L260-L296).
        - Code at v0.9.0: [`handler.go#L220-L258`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L220-L258).
    - **Related**: [REQ-86](#req-86), [REQ-95](#req-95), [REQ-103](#req-103),
      [F-84](../traceability/findings.md#f-84), [Q-41](../traceability/open-questions.md#q-41), [Q-66](../traceability/open-questions.md#q-66).
    - **Notes**: GBO interprets ETSI so that `insufficient_scope` is also 401.
      RFC 6750 §3.1 gives 403 for this case. The ASIP accepts RS256, because
      RFC 9068 §2.1 requires it. The authorization server signs with ES256.
      The ASIP gets the keys from the metadata of the authorization server.
      If the entitlement of a QTSP is withdrawn, its token stays valid until
      it expires ([Q-41](../traceability/open-questions.md#q-41)).

## REQ-88: Only a QTSP with the `QEAA_Provider` right in the register becomes a client {#req-88}

> The authorization server MUST register a client only with a software
> statement that the QTSP signed or sealed with the key of its
> certificate. That certificate MUST have a chain to a trusted anchor. The
> statement refers to an entry in the register of relying parties
> (`registryURI`). That entry MUST carry the entitlement `QEAA_Provider`
> and MUST name the organization of the certificate.
>
> After registration, the client MUST be able to authenticate only with
> the key of that certificate. If the register cannot be consulted, the
> authorization server MUST refuse the registration. It MUST register only
> a QTSP that is on the trusted list as a qualified provider, and MUST NOT
> know clients outside this registration.

| Case | Outcome |
|---|---|
| Valid statement, and an entry with `QEAA_Provider` and the organization of the certificate | client registered, `private_key_jwt` with the certificate key (code) |
| No statement, `alg none`, signed with another key, or no `x5c` | `invalid_software_statement` (code) |
| The chain reaches no trusted anchor, or the certificate is expired, has no `organizationIdentifier`, or has no digitalSignature | `invalid_software_statement` (code) |
| The statement is expired, has `iat` in the future, or has no `iss`, `iat`, `exp` or `registryURI` | `invalid_software_statement` (code) |
| `registryURI` unknown in the register | `unapproved_software_statement` (code) |
| Entry without `QEAA_Provider` | `unapproved_software_statement` (code) |
| The organization of the certificate is not in the entry | `unapproved_software_statement` (code) |
| The registration names `jwks` or `jwks_uri` | `invalid_client_metadata` (code) |
| The register cannot be consulted | 503 `temporarily_unavailable` (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - Article 9(5) of Implementing Regulation (EU)
          [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj). The member state can impose access controls "to
          determine that the requester is a qualified trust service provider".
        - eIDAS [article 45e](https://eur-lex.europa.eu/eli/reg/2014/910/oj). The verification is for QTSPs that issue
          qualified electronic attestations of attributes.
        - [Annex I item 12 of Implementing Regulation (EU) 2025/848](https://eur-lex.europa.eu/eli/reg_impl/2025/848/oj),
          which defines the entitlement `QEAA_Provider`.
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-AZSP-6.1.3.2-01, -02, and figure 2
          (informative).
        - [P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the authorization server.
    - **Evidence**: [ICTU/GBO-demo#607](https://github.com/ICTU/GBO-demo/issues/607) is not built in demo v0.9.0. The
      built parts come from [ICTU/GBO-demo#503](https://github.com/ICTU/GBO-demo/issues/503) and
      [PR #522](https://github.com/ICTU/GBO-demo/pull/522). Code and tests:
        - Registration and approval are in [`registration.go#L154-L215`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L154-L215).
        - The statement and the certificate are in
          [`#L253-L303`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L253-L303).
        - The client has no key of its own, in
          [`#L345-L354`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L345-L354).
        - The tests are in [`registration_test.go#L41-L83`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L41-L83),
          [`#L105-L169`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L105-L169),
          [`#L173-L220`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L173-L220),
          and [`#L323-L329`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L323-L329).
    - **Related**: [REQ-89](#req-89), [REQ-91](#req-91), [F-85](../traceability/findings.md#f-85),
      [Q-07](../traceability/answered-questions.md#q-07), [Q-35](../traceability/open-questions.md#q-35).
    - **Notes**:
        - The register with its API does not exist. The access certificates
          according to ETSI TS 119 411-8 do not exist either. The demo uses a
          file and certificates of the development CA ([F-85](../traceability/findings.md#f-85)).
        - Which identifier links the certificate and the entry is
          [Q-35](../traceability/open-questions.md#q-35). The demo uses `organizationIdentifier`.
        - What the QTSP must deliver (REQ-TSP-6.1.3.2-01 to -03) is a
          requirement on the QTSP. It belongs in a candidate connection
          condition.
        - A client from the configuration file of the demo
          (`AZSP_CLIENTS_FILE`) bypasses this admission. A production setup
          does not have that entry point.
        - The demo keeps registrations in memory only.

## REQ-89: The right of a registered client is re-checked periodically {#req-89}

> The authorization server MUST periodically re-check the entitlement of
> every registered client in the register. A client can lose the
> entitlement: its entry no longer carries `QEAA_Provider`, or no longer
> names the organization of the certificate. The authorization server MUST
> then deactivate the client. A deactivated client gets no more
> authorizations and no more tokens.

| Case | Outcome |
|---|---|
| Entitlement unchanged | the client stays active, and the authorization server takes over the name from the entry ([REQ-91](#req-91)) (code) |
| Entitlement withdrawn | client deactivated. A token request gets `invalid_client`. An authorization request gets an error page without redirect (code). |
| The register cannot be consulted | the client stays active until the next check (code, demo choice, [Q-34](../traceability/open-questions.md#q-34)) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) clause 6.1.3.2, figure 2, step 2 ("verified
          again in regular intervals determined by the applicable policy").
          This figure is informative.
        - Article 9(5) of Implementing Regulation (EU) [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj).
        - The requirement is also derived. It serves
          [P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/):
          a QTSP whose entitlement is withdrawn must not continue to verify
          because it registered earlier.
    - **Addressee**: GBO-delivered component: the authorization server.
    - **Evidence**: [PR #522](https://github.com/ICTU/GBO-demo/pull/522). Code and tests:
        - The re-check is in
          [`registration.go#L222-L244`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L222-L244).
        - The interval is in [`main.go#L101-L104`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/main.go#L101-L104)
          and [`#L155-L169`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/main.go#L155-L169).
        - The tests are in [`registration_test.go#L224-L242`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L224-L242),
          [`#L273-L304`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L273-L304)
          (through the stub register), and
          [`#L306-L321`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L306-L321).
    - **Related**: [REQ-88](#req-88), [REQ-91](#req-91), [F-85](../traceability/findings.md#f-85),
      [Q-34](../traceability/open-questions.md#q-34), [Q-41](../traceability/open-questions.md#q-41).
    - **Notes**: the interval is policy. The operator can configure it with
      `AZSP_ENTITLEMENT_RECHECK_INTERVAL`, and the default is one hour. What
      happens when the register is unreachable, and how often to check, is
      [Q-34](../traceability/open-questions.md#q-34). Tokens issued before the deactivation stay valid until
      they expire, at most ten minutes ([Q-41](../traceability/open-questions.md#q-41)). The stub register of
      the demo reads its file on every lookup, so a withdrawal works without
      a restart.

## REQ-90: The citizen approves the request by logging in, or refuses {#req-90}

> The authorization server MUST show every valid authorization request to
> the citizen before it issues an authorization code. The citizen MUST be
> able to refuse, or to log in with an identification means. The approval
> MUST become fixed only after the means identifies the citizen. A refusal
> MUST give `access_denied` and MAY happen without a login.
>
> The pending request MUST be single-use, short-lived, and bound to the
> browser in which it started. A session with a means MUST be bound to
> that request. If a decision does not belong to a valid pending request
> of that browser, the authorization server MUST NOT send it back to the
> client. If the login fails or the means is unreachable, the request MUST
> stay open for a new attempt or another means.

| Case | Outcome |
|---|---|
| The citizen refuses, before or instead of a login | `access_denied` to the QTSP, without a login (code) |
| The citizen logs in and the means identifies him | authorization code to the QTSP (code) |
| The means does not identify him: DigiD (mock) gets no BSN of nine digits, or the wallet gives no usable PID | the page again, with the reason. The transaction stays (code). |
| Refused in the wallet, or the session expired | the request page again, with the reason. The transaction stays (code). |
| The means is unreachable. This includes the case where the shared attributes cannot be fetched after a completed session. | error page (503). The transaction stays for another means (code). |
| A decision without a transaction cookie, with the cookie of another transaction, or for an unknown, used, or expired transaction | error page (400), no redirect (code) |
| A wallet session of another transaction, or a session token from the browser | no identification (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - eIDAS [article 45e(1)](https://eur-lex.europa.eu/eli/reg/2014/910/oj) ("at the request of the user").
        - Article 9(5) of Implementing Regulation (EU)
          [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj) ("acting at the request of a legitimate user").
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-AZSP-6.1.3.1-02 ("shall identify the
          user"), and clause 6.1.3.3, steps 7 to 11. These steps are
          informative ("the authorization of the later resource request by the
          user").
        - [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) §3.1, and
          [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) §2.1.1 and §4.11.
          ETSI refers to RFC 9700.
    - **Addressee**: GBO-delivered component: the authorization server.
    - **Evidence**: [ICTU/GBO-demo#523](https://github.com/ICTU/GBO-demo/issues/523), [#544](https://github.com/ICTU/GBO-demo/issues/544),
      [#546](https://github.com/ICTU/GBO-demo/issues/546), [#548](https://github.com/ICTU/GBO-demo/issues/548), [PR #524](https://github.com/ICTU/GBO-demo/pull/524),
      [PR #545](https://github.com/ICTU/GBO-demo/pull/545), [PR #552](https://github.com/ICTU/GBO-demo/pull/552), [PR #573](https://github.com/ICTU/GBO-demo/pull/573). Code and tests:
        - The transaction is in [`service.go#L210-L231`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service.go#L210-L231)
          and [`identification.go#L107-L120`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/identification.go#L107-L120).
          It is single-use and bound to the browser in
          [`#L195-L207`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/identification.go#L195-L207).
        - Refuse and log in are in
          [`#L275-L317`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/identification.go#L275-L317)
          and [`#L358-L371`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/identification.go#L358-L371).
        - The decision and the wallet are in
          [`handler.go#L81-L116`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/handler.go#L81-L116)
          and [`#L158-L190`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/handler.go#L158-L190).
        - The page and the cookie are in
          [`pages.go#L206-L229`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/pages.go#L206-L229).
        - The tests are in [`login_test.go#L60-L188`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/login_test.go#L60-L188),
          [`wallet_test.go#L148-L173`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/wallet_test.go#L148-L173),
          and [`#L270-L354`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/wallet_test.go#L270-L354).
        - The trade-off is in
          [`security-considerations.md#L21`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/security-considerations.md#L21)
          and [`#L77-L79`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/security-considerations.md#L77-L79).
    - **Related**: [REQ-86](#req-86), [REQ-91](#req-91), [REQ-102](#req-102),
      [Q-36](../traceability/open-questions.md#q-36), [Q-40](../traceability/open-questions.md#q-40).
    - **Notes**: design choices:
        - The transaction is valid for five minutes.
        - The cookie is HttpOnly and SameSite=Strict, with path `/authorize`.
        - The pages are not cached and not shown in a frame.

        The choice of a means starts the approval. Approval and identification
        are one step, as in ETSI figure 3 step 9. DigiD (mock) is a stub that
        only checks the form of the BSN. Which means a Dutch ASI accepts is
        [Q-36](../traceability/open-questions.md#q-36). [Q-40](../traceability/open-questions.md#q-40) asks whether the citizen who logs in here is the
        same as the citizen who logged in at the QTSP.

## REQ-91: The citizen sees who asks what at which source before logging in {#req-91}

> For every authorization, the authorization server MUST show the citizen
> these facts before he logs in:
>
> - The QTSP that makes the request. The page MUST use the name from the
>   entry of the QTSP in the register of relying parties. A technical
>   client identifier alone is not enough.
> - The requested operation. This is verify, retrieve, or both.
> - The authentic source. The page MUST name the source for which the
>   token is valid.
>
> If the request names attributes ([REQ-103](#req-103)), the page MUST
> show them too. If the request names no attributes, the page MUST NOT
> name any.

| Case | Outcome |
|---|---|
| Registered QTSP | the legal name from the entry. A changed name shows after the next re-check (code). |
| Client from the configuration without a name | the `client_id` (code, demo glue) |
| Data service without a source name in the configuration | the authorization server does not start (code) |
| Request with `authorization_details` | the attributes, and what the QTSP gets to see (code) |
| Request without `authorization_details` | no attributes and no promise about them (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - eIDAS [article 45e(1)](https://eur-lex.europa.eu/eli/reg/2014/910/oj) ("at the request of the user"), with
          [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) clause 6.1.3.3, step 7 (informative).
        - The
          [FAPI 2.0 Security Profile](https://openid.net/specs/fapi-security-profile-2_0-final.html),
          to which ETSI clause 6.1.3.1 NOTE 3 refers. The profile asks for an
          informed decision of the end user. Its recommendation is to "provide
          end-users with all necessary information …, including the identity
          of the client and the scope of the authorization".
        - The requirement is also derived. It serves
          [P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/):
          without the name of the QTSP and of the source, the citizen does not
          know what he approves. If he does not see the source, a token for one
          source ([REQ-95](#req-95)) does not help him.
    - **Addressee**: GBO-delivered component: the authorization server.
    - **Evidence**: [ICTU/GBO-demo#525](https://github.com/ICTU/GBO-demo/issues/525), [#544](https://github.com/ICTU/GBO-demo/issues/544),
      [#547](https://github.com/ICTU/GBO-demo/issues/547), [PR #529](https://github.com/ICTU/GBO-demo/pull/529), [PR #545](https://github.com/ICTU/GBO-demo/pull/545),
      [PR #559](https://github.com/ICTU/GBO-demo/pull/559), [PR #591](https://github.com/ICTU/GBO-demo/pull/591). Code and tests:
        - The request page is in
          [`pages.go#L94-L123`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/pages.go#L94-L123).
        - The name from the entry is in
          [`registration.go#L185`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L185),
          and at the re-check in
          [`#L228-L244`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L228-L244).
        - The name and the source in the transaction are in
          [`service.go#L225-L229`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service.go#L225-L229)
          and [`#L286-L293`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service.go#L286-L293).
        - The source name is mandatory in
          [`main.go#L190-L210`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/main.go#L190-L210).
        - The tests are in [`login_test.go#L17-L58`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/login_test.go#L17-L58),
          [`style_test.go#L105-L163`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/style_test.go#L105-L163),
          [`registration_test.go#L67-L83`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L67-L83),
          [`#L244-L271`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/registration_test.go#L244-L271),
          and [`main_test.go#L5-L17`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/main_test.go#L5-L17).
    - **Related**: [REQ-88](#req-88), [REQ-89](#req-89), [REQ-90](#req-90),
      [REQ-95](#req-95), [REQ-102](#req-102), [REQ-103](#req-103),
      [Q-36](../traceability/open-questions.md#q-36).
    - **Notes**:
        - The page has other texts: why, what the QTSP learns, only this
          request, and where the citizen logs in. These texts are a text
          choice of the demo and are not a requirement.
        - The NL Wallet shows the authorization server and not the QTSP,
          because a fixed reader certificate cannot carry a name for each
          QTSP. The page and the purpose in that certificate explain the
          relation ([`provision.go#L109`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/provision.go#L109),
          [REQ-102](#req-102)).
        - The chosen safeguard is that the server does not start without a
          source name. In v0.9.0, the authorization server takes its data
          services and source names from `AZSP_RESOURCES` and not from the
          source descriptions. [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592) stays open.
        - This requirement absorbs the former REQ-96.

## REQ-92: The ASIP asks the source only for the fields of the requested attributes {#req-92}

> An ASIP that queries a source through the chain MUST ask the source
> only for the fields that the requested attributes need. This applies to
> each verify or retrieve request, for the citizen from the access token. The
> ASIP MUST refuse a request with an attribute that the data service does
> not deliver, before it asks the source anything.

| Case | Outcome |
|---|---|
| Verify with three attributes and a fragment | one query to the source, with the fields of each attribute once (code) |
| An attribute outside the catalogue next to a valid attribute | 404, and the ASIP does not ask the source (code) |
| An attribute for which the ASIP knows no fields | error, and the ASIP does not ask the source (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: derived. The requirement serves
      [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
      and [D-09](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
      (selective data request). The ASIP is a consumer of the source. If it
      asks more fields than the QTSP needs, it processes data without a
      purpose. [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) clause 4.3 leaves open how an ASIP
      that is "an intermediary acting on its behalf" queries its source.
    - **Addressee**: GBO-delivered component: the ASIP.
    - **Evidence**: [ICTU/GBO-demo#525](https://github.com/ICTU/GBO-demo/issues/525), [PR #527](https://github.com/ICTU/GBO-demo/pull/527),
      [PR #530](https://github.com/ICTU/GBO-demo/pull/530). Historical code and tests:
        - The fields for each attribute, and the one query, are in
          [`source.go#L37-L46`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source.go#L37-L46)
          and [`#L74-L108`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source.go#L74-L108).
        - The check against the catalogue comes first, in
          [`service.go#L110-L118`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service.go#L110-L118).
        - The tests are in [`service_test.go#L150-L199`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service_test.go#L150-L199),
          [`source_test.go#L122-L146`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source_test.go#L122-L146),
          [`#L186-L217`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source_test.go#L186-L217),
          and [`trace_test.go#L45-L81`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/trace_test.go#L45-L81).

        Code at v0.9.0: since steps 1 to 5 of [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592) (up to
        [PR #624](https://github.com/ICTU/GBO-demo/pull/624)), the ASIP derives one query from the `asi` description
        of the source. It does this in two steps:

        1. The ASIP checks that the description names every attribute
           ([`service.go#L238-L251`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L238-L251)).
        2. The ASIP makes one plan for all requested attributes
           ([`#L253-L268`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L253-L268),
           [`plan.go#L22-L35`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-mapping/plan.go#L22-L35)), with the BSN as a variable
           ([`source.go#L94`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/source.go#L94)).

        The tests are in [`source_test.go#L102`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/source_test.go#L102)
        and [`trace_test.go#L59`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/trace_test.go#L59).

    - **Related**: [REQ-08](authorization.md#req-08),
      [REQ-55](logging-audit.md#req-55), [REQ-60](logging-audit.md#req-60),
      [REQ-64](sources-identity.md#req-64), [REQ-94](#req-94), [Q-38](../traceability/open-questions.md#q-38),
      [ADR 0039](../decisions/0039-asi-source-described-attributes.md).
    - **Notes**:
        - The design uses one query per request. As a result, there is one
          FSC transaction and one decision of the PDP. The BSN is a variable
          and is not in the query text. The source enforces the limit itself
          with its own rule ([`asi0001.rego`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/asi/asi0001.rego)).
        - In v0.9.0, the source describes which fields belong to an
          attribute. It does this in the `asi` capability of its source
          metadata. GBO validates the description against its attribute
          catalogue ([`schemas/asi-attributes.json`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json)). The open points of
          that direction are in [Q-38](../traceability/open-questions.md#q-38) and
          [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592).

## REQ-93: A chain that does not answer is an error, not `Unknown` {#req-93}

> If the ASIP cannot reach the source, or the chain gives a server error,
> the ASIP MUST return 503. If the chain refuses the query, the ASIP MUST
> return 500. An example is a refusal by the PDP of the source. If the ASIP
> cannot read the answer of the source, it MUST also return 500. In all
> these cases, the ASIP MUST NOT return a verification result. This also
> excludes `Unknown`.

| Case | Outcome |
|---|---|
| Outway not reachable | 503 (code) |
| Outway answers with a 5xx (for example 502, source unreachable) | 503 (code) |
| The PDP of the source refuses (the Inway gives 401) | 500 (code) |
| The source answers with GraphQL errors, or with something other than JSON | 500 (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: derived. For verify, the requirement serves
      [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte). `Unknown` says that the source has no data
      ([ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-ASIP-6.1.1.2-04). If the ASIP reports a
      failure as `Unknown`, the QTSP gets a wrong verification result. The
      QTSP can then refuse the citizen, or let him fill in the value himself.
      Annex B has no 500 and no 503, so these codes are an addition.
    - **Addressee**: interface agreement: every ASIP. GBO-delivered component:
      the ASIP.
    - **Evidence**: [ICTU/GBO-demo#525](https://github.com/ICTU/GBO-demo/issues/525), [PR #527](https://github.com/ICTU/GBO-demo/pull/527).
      Historical code and tests:
        - The status codes are in
          [`handler.go#L353-L375`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L353-L375).
        - Unreachable or refused is in
          [`source.go#L211-L240`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source.go#L211-L240).
        - The addition to the contract is in
          [`completions.json#L76-L95`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/openapi/completions.json#L76-L95).
        - The tests are in [`source_test.go#L74-L97`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/source_test.go#L74-L97),
          [`brpsource/source_test.go#L148-L177`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/brpsource/source_test.go#L148-L177),
          and [`service_test.go#L201-L217`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service_test.go#L201-L217).

        Code at v0.9.0: the status codes are in
        [`handler.go#L362-L384`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L362-L384). Unreachable or
        refused is in
        [`source.go#L107-L138`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/source.go#L107-L138).
        The tests are in [`source_test.go#L141`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/source_test.go#L141)
        and [`graphqlsource/source_test.go#L157`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/source_test.go#L157).

    - **Related**: [REQ-60](logging-audit.md#req-60), [REQ-84](#req-84),
      [REQ-101](#req-101).
    - **Notes**: only unit tests show the 500 on a refusal by the PDP. The
      stack does not show it. A refusal by the chain is a fault in the setup
      and not a property of the citizen. Error messages name the
      `Fsc-Transaction-Id` and not the BSN ([REQ-60](logging-audit.md#req-60)).
      In v0.9.0, if the source has no up-to-date `asi` description, the ASIP
      also gives 503
      ([`source.go#L60-L68`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/source.go#L60-L68)).

## REQ-94: Every ASI response names the one authentic source responsible for it {#req-94}

> Every verify and retrieve response of the ASIP MUST name the ASIP
> (`provider`). If the ASIP is not itself the authentic source, the
> response MUST also name the responsible authentic source
> (`authenticSource`). It MUST name exactly one source. For that reason, an ASIP
> that serves several sources MUST limit each request to one source. An
> attribute of another source MUST give 404, and the ASIP MUST NOT ask
> any source anything.

| Case | Outcome |
|---|---|
| Data service with an authentic source behind the ASIP | `provider` and `authenticSource` in every response (code) |
| Data service of which the ASIP is itself the source | `provider`, no `authenticSource`. This is historical code, in unit tests only. In v0.9.0, the ASIP always takes `authenticSource` from the source description. |
| Attribute of another data service | 404, and the ASIP asks no source (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - Article 9(4) of Implementing Regulation (EU)
          [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj), as Implementing Regulation (EU)
          [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj) replaces it. The result "shall … specify the public
          sector body responsible for the authentic source". Where applicable,
          the result specifies instead "the public sector body designated to
          act on behalf of the authentic source".
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-ASIP-6.1.1.2-07, -08, and
          REQ-ASIP-6.1.2.2-04 (one `authenticSource`).
        - [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) ("de source holder (bronhouder) blijft juridisch en
          inhoudelijk verantwoordelijk").
        - [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: interface agreement: every ASIP. GBO-delivered component:
      the ASIP.
    - **Evidence**: [ICTU/GBO-demo#525](https://github.com/ICTU/GBO-demo/issues/525), [PR #529](https://github.com/ICTU/GBO-demo/pull/529).
      Historical code and tests:
        - The data services come from the configuration in
          [`dataservice.go#L52-L106`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/dataservice/dataservice.go#L52-L106)
          and [`main.go#L86-L105`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/main.go#L86-L105).
        - Each data service has a base URL, a contract, and records in
          [`handler.go#L89-L113`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L89-L113).
        - The source in the response is in
          [`#L37-L53`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L37-L53)
          and [`#L187-L192`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L187-L192).
        - The tests are in [`dataservices_test.go#L32-L48`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/dataservices_test.go#L32-L48),
          [`handler_test.go#L153-L159`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L153-L159),
          [`#L329-L349`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L329-L349),
          and [`service_test.go#L133-L148`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service_test.go#L133-L148).

        Code at v0.9.0: the data services are in
        [`dataservices.json`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/config/dataservices.json)
        and [`main.go#L115-L125`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/main.go#L115-L125). The ASIP takes `authenticSource`
        from the source description in
        [`handler.go#L304`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L304)
        and [`#L339`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L339). The tests are in
        [`dataservices_test.go#L35`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/dataservices_test.go#L35)
        and [`handler_test.go#L151-L155`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L151-L155).

    - **Related**: [REQ-83](#req-83), [REQ-84](#req-84), [REQ-95](#req-95),
      [REQ-99](#req-99), [F-89](../traceability/findings.md#f-89), [Q-37](../traceability/open-questions.md#q-37), [Q-38](../traceability/open-questions.md#q-38), [E3](../traceability/standards-feedback.md#e3),
      [ADR 0038](../decisions/0038-asi-data-service-per-source.md).
    - **Notes**: the design has one data service per source
      ([ADR 0038](../decisions/0038-asi-data-service-per-source.md)). Each data service has its own base URL, contract,
      catalogue, and token audience. The demo has one data service (`brp`,
      source `rvig`). A second data service exists only in unit tests. Whether
      an ASIP for several sources makes GBO an intermediary is [Q-37](../traceability/open-questions.md#q-37).

## REQ-95: An access token is valid only for the source the citizen saw {#req-95}

> An access token MUST be valid only for the authentic source that the
> citizen saw at the authorization ([REQ-91](#req-91)). An authorization
> request or a token request can name no data service, more than one, or an
> unknown one. The authorization server MUST then refuse it with
> `invalid_target`. The ASIP MUST refuse a token for another data service.

| Case | Outcome |
|---|---|
| One known `resource` | token with its base URL as `aud` (code) |
| No `resource`, two, or an unknown one | `invalid_target` (code) |
| Token request with another `resource` than the one of the code | `invalid_target` (code) |
| Token for data service A at data service B | 401 `invalid_token` (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: derived. The requirement serves eIDAS
      [article 45e(1)](https://eur-lex.europa.eu/eli/reg/2014/910/oj) ("at the request of the user") and
      [P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
      If a token is also valid for another source, the QTSP verifies data at a
      source that the citizen did not see. [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) does not
      specify the reach of a token for each data service.
    - **Addressee**: GBO-delivered component: the authorization server and
      the ASIP.
    - **Evidence**: [ICTU/GBO-demo#525](https://github.com/ICTU/GBO-demo/issues/525), [PR #529](https://github.com/ICTU/GBO-demo/pull/529). Code and tests:
        - The authorization server is in
          [`service.go#L201-L204`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service.go#L201-L204),
          [`#L255-L276`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service.go#L255-L276),
          and [`#L341-L343`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service.go#L341-L343).
        - The audience at the ASIP is in
          [`accesstoken.go#L148`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/accesstoken/accesstoken.go#L148),
          and for each data service in
          [`main.go#L102`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/main.go#L102).
        - The tests are in [`handler_test.go#L151-L182`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/handler_test.go#L151-L182)
          and [`dataservices_test.go#L15-L30`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/dataservices_test.go#L15-L30).
        - Code at v0.9.0: the audience for each data service is in
          [`main.go#L121`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/main.go#L121), tested in
          [`dataservices_test.go#L16`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/dataservices_test.go#L16).
    - **Related**: [REQ-86](#req-86), [REQ-87](#req-87), [REQ-91](#req-91),
      [REQ-94](#req-94), [REQ-99](#req-99), [REQ-103](#req-103), [F-89](../traceability/findings.md#f-89),
      [ADR 0038](../decisions/0038-asi-data-service-per-source.md).
    - **Notes**: the design allows exactly one `resource` for each
      authorization ([ADR 0038](../decisions/0038-asi-data-service-per-source.md)). As a result, a QTSP that needs
      attributes of two sources authorizes twice, with two interactions of the
      citizen. RFC 8707 §2.2 allows more resources in one authorization, with
      a token for each resource.

## REQ-99: The ASIP provides a discovery record for each attribute and data service, with a path to endpoint, contract, and authorization server {#req-99}

> For every data service, the ASIP MUST provide a `dataService` record
> according to ETSI TS 119 478 clause 5.3.3. It MUST provide one record for
> each attribute that the data service delivers. The record holds these
> items: the identifier of the attribute (`attributeIdentifier`), the
> endpoint of the data service (`endpointURI`), its contract
> (`endpointDescription`), and the provider (`provider`). The contract MUST
> name the same endpoint as server. The contract MUST also name the
> metadata of the authorization server ([REQ-100](#req-100)). From the record, a
> QTSP can then verify or retrieve without prior knowledge of the
> addresses of the ASIP.

| Case | Outcome |
|---|---|
| Data service `brp` with three attributes | three records, each with endpoint, contract, provider, and country. The records conform to the ETSI schema (code). |
| Record → contract | `servers` is the endpoint of the record. The contract names the metadata of the authorization server (code). |
| Unknown data service | no records, 404 (code) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) clause 5.3.3, REQ-DIP-5.3.3-03 (the content
          of the record). ETSI puts this requirement on the DIP.
        - ETSI figure 3, steps 2 to 5. In these steps, the QTSP finds the data
          service through the Discover Interface.
        - The requirement is also derived. It serves
          [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) ("aansluiting op relevante vertrouwenslijsten
          en catalogi") and
          [P-11](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/):
          without a record, a QTSP finds no Dutch data service for an
          attribute.
    - **Addressee**: GBO-delivered component: the ASIP. Interface agreement:
      the record and the contract.
    - **Evidence**: [ICTU/GBO-demo#533](https://github.com/ICTU/GBO-demo/issues/533), [PR #534](https://github.com/ICTU/GBO-demo/pull/534),
      [PR #535](https://github.com/ICTU/GBO-demo/pull/535). Code and tests:
        - The records for each data service are in
          [`handler.go#L104-L111`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L104-L111)
          and [`#L138-L156`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L138-L156).
        - A test checks the records against the ETSI schema
          ([`discovery_test.go#L62`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/discovery_test.go#L62)).
          Another test follows the path from record to contract
          ([`discovery_test.go#L101`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/discovery_test.go#L101)).
        - The stub of the DIP checks the records
          ([`directory.go#L101-L134`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-discovery-stub/directory.go#L101-L134))
          and finds them for each attribute
          ([`handler_test.go#L97`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-discovery-stub/handler_test.go#L97)).
        - The reference QTSP follows the record, the contract, and the
          metadata
          ([`qtsp.go#L119-L202`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/qtsp-reference/internal/qtsp/qtsp.go#L119-L202)).
        - Code at v0.9.0: the records follow the up-to-date description of
          the source. Without an up-to-date description, the ASIP gives 503
          ([`handler.go#L131-L165`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L131-L165)).
          The tests are in [`discovery_test.go#L66`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/discovery_test.go#L66),
          [`#L105`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/discovery_test.go#L105),
          and [`#L169`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/discovery_test.go#L169).
    - **Related**: [REQ-94](#req-94), [REQ-95](#req-95), [REQ-100](#req-100),
      [F-89](../traceability/findings.md#f-89), [Q-67](../traceability/open-questions.md#q-67).
    - **Notes**:
        - How the records get into the Data Service Directory of OOTS, and who
          registers them, is open ([Q-67](../traceability/open-questions.md#q-67)).
        - The demo offers the records for each data service at
          `/<dataservice>/dataservices`. A stub of the DIP fetches them.
        - In demo v0.9.0, the provider carries no `identifiers`.
          REQ-DIP-5.3.3-03-04-04 is only a recommendation, and there is no EU
          identifier type for an OIN.
        - The search of a QTSP through the Discover Interface is behavior of
          the QTSP itself (clause 5) and is no requirement on GBO.
        - The reference QTSP refuses a request with attributes of two data
          services before it contacts the authorization server. The reason is
          that a token is valid for one data service ([REQ-95](#req-95)).

## REQ-100: A data service contract names its authorization-server metadata at the location RFC 8414 prescribes {#req-100}

> The contract of a data service MUST name the URL of the metadata of its
> authorization server. That URL MUST be the location that RFC 8414 §3.1
> prescribes for the issuer: the suffix
> `/.well-known/oauth-authorization-server` between host and path of the
> issuer.

| Case | Outcome |
|---|---|
| Issuer `https://host` | `https://host/.well-known/oauth-authorization-server` (code) |
| Issuer with path `https://host/issuer1` | `https://host/.well-known/oauth-authorization-server/issuer1` (code) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-DIP-5.3.3-03-02-01. The contract "shall
          specify the corresponding metadata of the OAuth 2.0 based
          authorization server".
        - [RFC 8414](https://www.rfc-editor.org/rfc/rfc8414) §3.1 and §3.3.
        - [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) ("ETSI TS 119 478 V1.1.1 voor de inrichting van
          de ASI-provider").
    - **Addressee**: interface agreement: the contract of every ASIP.
      GBO-delivered component: the ASIP.
    - **Evidence**: [PR #534](https://github.com/ICTU/GBO-demo/pull/534), [PR #537](https://github.com/ICTU/GBO-demo/pull/537). Code and tests:
        - The contract is in
          [`contract.go#L102-L110`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/contract.go#L102-L110).
        - The URL is in
          [`asmetadata.go#L45-L53`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/asmetadata/asmetadata.go#L45-L53).
        - The tests are in [`asmetadata_test.go#L84`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/asmetadata/asmetadata_test.go#L84),
          [`#L103`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/asmetadata/asmetadata_test.go#L103)
          (issuer with a path), and
          [`discovery_test.go#L101`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/discovery_test.go#L101).
    - **Related**: [REQ-99](#req-99), [F-91](../traceability/findings.md#f-91), [Q-39](../traceability/open-questions.md#q-39),
      [Q-67](../traceability/open-questions.md#q-67), [E1](../traceability/standards-feedback.md#e1).
    - **Notes**: the extension `x-oauth-authorization-server` in the `oauth2`
      security scheme is a design choice. GBO chose this name itself, because
      ETSI gives no field ([E1](../traceability/standards-feedback.md#e1)). Until [Q-39](../traceability/open-questions.md#q-39) has a decision,
      each ASIP chooses for itself. RFC 8414 §3.3 already requires the client
      to check the `issuer` in the metadata against the URL. The reference
      QTSP does exactly this
      ([`qtsp.go#L196-L200`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/qtsp-reference/internal/qtsp/qtsp.go#L196-L200)).

## REQ-101: A retrieve for which the source lacks a requested attribute is not found and gives no partial result {#req-101}

> If the source has no value for a requested attribute, the ASIP MUST
> answer a retrieve request with 404, with the attribute in the reason. A
> retrieve MUST NOT give a partial result: a 200 MUST contain every
> requested attribute. Verify still gives `Unknown` ([REQ-84](#req-84)).

| Case | Outcome |
|---|---|
| The source has a value for every requested attribute | 200 with every attribute, sealed (code) |
| The source has no value for one attribute, also next to an attribute with a value | 404 without a seal. The reason names the attribute (code). |
| Attribute not in the catalogue of the data service | 404 ([REQ-94](#req-94)) (code) |
| Verify, the source has no value | `Unknown` ([REQ-84](#req-84)) (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design. The source is [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf)
      REQ-ASIP-6.1.2.2-06 ("404 … at least one of the requested attributes …
      was not found") and -02-01 ("one or more attribute objects"). GBO reads
      these requirements so that no value in the source also counts as not
      found.
    - **Addressee**: interface agreement: every ASIP. GBO-delivered component:
      the ASIP.
    - **Evidence**: [PR #541](https://github.com/ICTU/GBO-demo/pull/541), [PR #542](https://github.com/ICTU/GBO-demo/pull/542). Code and tests:
        - Historical code:
          [`service.go#L152-L158`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service.go#L152-L158)
          and [`handler.go#L366-L367`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L366-L367).
          The test for one and two attributes is in
          [`handler_test.go#L291-L319`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L291-L319).
        - Code at v0.9.0: [`service.go#L198-L236`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L198-L236)
          and [`handler.go#L375-L376`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L375-L376).
          The test is in [`handler_test.go#L291-L315`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L291-L315).
    - **Related**: [REQ-84](#req-84), [REQ-90](#req-90), [REQ-93](#req-93),
      [REQ-94](#req-94).
    - **Notes**: a missing value also tells something about the person, for
      example that he has no Dutch address. The citizen authorized the
      request himself ([REQ-90](#req-90)).

## REQ-102: The authorization server identifies the citizen with the EUDI wallet through OpenID4VP and asks only the PID attributes in its registration {#req-102}

> The authorization server of the ASI MUST be able to identify the citizen
> with the EUDI wallet through OpenID4VP. It MUST act as a registered
> wallet relying party of its own, and ask only the PID attributes that
> are in its registration. The PID MUST come from a trusted PID issuer and
> contain a BSN. A presentation of another type, or without a BSN, MUST
> NOT lead to an identification.

| Case | Outcome |
|---|---|
| PID `urn:eudi:pid:nl:1` with BSN, from a trusted issuer | identified. The BSN and the PID attributes go into the token ([REQ-86](#req-86)) (code). |
| PID without BSN, another type, another query ID, or no presentation | not identified (code) |
| Return on the same device with the session of another browser, or without a valid nonce | not identified (code) |
| Verifier not reachable | means not available. The transaction stays ([REQ-90](#req-90)) (code). |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-AZSP-6.1.3.1-02 and -03 ("with the
          EUDI-Wallet using the OpenID4VP protocol"), and clause 6.1.3.3,
          steps 8 to 10.
        - [eIDAS](https://eur-lex.europa.eu/eli/reg/2014/910/oj) article 5b(1) to (3). The relying party is registered
          and asks no other data than the registered data.
        - Implementing Regulation (EU) [2025/848](https://eur-lex.europa.eu/eli/reg_impl/2025/848/oj) article 8.
        - [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) ("OpenID4VP voor presentatie of verificatie
          waar relevant").
    - **Addressee**: GBO-delivered component: the authorization server of the
      ASI.
    - **Evidence**: [ICTU/GBO-demo#546](https://github.com/ICTU/GBO-demo/issues/546), [PR #550](https://github.com/ICTU/GBO-demo/pull/550),
      [PR #552](https://github.com/ICTU/GBO-demo/pull/552), [PR #573](https://github.com/ICTU/GBO-demo/pull/573). Code and tests:
        - The request for the PID is in
          [`client.go#L39-L48`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/client.go#L39-L48)
          and [`provision.go#L36-L40`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/provision.go#L36-L40).
        - The registration with only those attributes is in
          [`provision.go#L106-L112`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/provision.go#L106-L112)
          and [`#L189-L195`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/provision.go#L189-L195), tested in
          [`provision_test.go#L115-L117`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/provision_test.go#L115-L117).
        - The trusted issuers are in
          [`provision.go#L139-L150`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/provision.go#L139-L150).
        - The code accepts only a PID of the right type with a BSN, in
          [`client.go#L157-L175`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/client.go#L157-L175), tested in
          [`client_test.go#L174-L192`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/client_test.go#L174-L192).
        - Return on the same device works only for the session of this
          transaction and browser, in
          [`identification.go#L318-L341`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/identification.go#L318-L341).
          The tests are in [`wallet_test.go#L88`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/wallet_test.go#L88),
          [`#L123`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/wallet_test.go#L123),
          [`#L177`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/wallet_test.go#L177),
          and [`#L205`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/wallet_test.go#L205).
        - PR #552 records a run with the real NL Wallet (cross-device).
    - **Related**: [REQ-86](#req-86), [REQ-90](#req-90), [REQ-91](#req-91),
      [F-93](../traceability/findings.md#f-93), [F-94](../traceability/findings.md#f-94), [Q-36](../traceability/open-questions.md#q-36).
    - **Notes**:
        - The choice of verifier is a design choice of the demo. The verifier
          is the `verification_server` of nl-wallet v0.5.0. It checks the
          signature of the issuer and the binding to the wallet. Another
          verifier is allowed.
        - The reader certificate of the NL Wallet carries the registration
          (purpose and allowed attributes). In the demo, this certificate
          comes from a development CA and is not a registered access
          certificate.
        - The NL PID has no place of birth ([F-94](../traceability/findings.md#f-94)).
        - The wallet shows the authorization server and not the QTSP. The
          purpose in the registration explains the relation
          ([REQ-91](#req-91)).
        - The same-device route runs only in tests. A real run needs the ASI
          route on https in the simulation environment
          ([ICTU/GBO-demo#594](https://github.com/ICTU/GBO-demo/issues/594), [ICTU/GBO-demo#596](https://github.com/ICTU/GBO-demo/issues/596)).
        - Which means come next to the wallet is [Q-36](../traceability/open-questions.md#q-36).
        - The verifier accepts a PID whose revocation status cannot be
          established
          ([`config.go#L45`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/config.go#L45)).
          A sub-question of [Q-36](../traceability/open-questions.md#q-36) asks whether a PID with an unknown
          revocation status, or a revoked PID, can lead to an identification.

## REQ-103: An authorization can be bound to the requested attributes, and the ASIP then processes only those attributes {#req-103}

> An authorization request can name the attributes that the QTSP wants to
> verify or retrieve. The authorization server of the ASI MUST then check
> that these attributes belong to exactly the data service and the
> operations of the request. It MUST refuse an invalid list, show the
> attributes to the citizen, and put them unchanged in the access token.
> If the token carries such a list, the ASIP MUST refuse a request that
> names an attribute outside the list.
>
> A policy under article 9(5) of Implementing Regulation 2025/1569 can
> make the list mandatory
> ([Q-33](../traceability/open-questions.md#q-33)). Without such a policy,
> the authorization server MUST treat a request without a list as an
> authorization per operation according to ETSI TS 119 478. The catalogue
> of the data service is then the limit.

| Case | Outcome |
|---|---|
| No list | authorization per operation, a page without attributes, and a token without a list. The ASIP allows every attribute from the catalogue (code). |
| No list, list made mandatory | `invalid_request` (code) |
| The list is empty, of an unknown type, or for another data service. Or the list has other operations than the scope, no attributes, or invalid or duplicate attributes. | `invalid_request` (code) |
| Valid list | attributes on the page and unchanged in the token (code) |
| Token with a list, and the request names another attribute | 401 `insufficient_scope`. The reason names the attribute (code). |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - Implementing Regulation (EU) [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj) article 9(5). A member
          state can impose access control.
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) clause 6.1.3.2 binds only for each operation
          ([F-95](../traceability/findings.md#f-95)).
        - The requirement is also derived. It serves
          [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) ("uitgifte, verificatie en retrieval gebruiken
          passende authenticatie, autorisatie en logging") and
          [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
          Without a binding, the QTSP can ask every attribute from the
          catalogue with the same token, also when the citizen approved
          something else.
    - **Addressee**: GBO-delivered component: the authorization server and
      the ASIP. Interface agreement: with the QTSP.
    - **Evidence**: [PR #559](https://github.com/ICTU/GBO-demo/pull/559), [ICTU/GBO-demo#571](https://github.com/ICTU/GBO-demo/issues/571),
      [PR #572](https://github.com/ICTU/GBO-demo/pull/572). Code and tests:
        - The check at the authorization server is in
          [`authorization_details.go#L31-L79`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/authorization_details.go#L31-L79)
          and [`service.go#L205-L209`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service.go#L205-L209).
        - The page shows the attributes in
          [`pages.go#L109-L111`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/pages.go#L109-L111).
        - The token is in
          [`tokens.go#L70-L72`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/tokens.go#L70-L72).
        - The configuration that makes the list mandatory is in
          [`main.go#L109`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/main.go#L109).
        - The check at the ASIP is in
          [`accesstoken.go#L177-L197`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/accesstoken/accesstoken.go#L177-L197)
          and [`handler.go#L337-L347`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L337-L347).
        - The tests are in [`service_test.go#L85-L125`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service_test.go#L85-L125),
          [`#L151-L160`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/service_test.go#L151-L160),
          [`handler_test.go#L62`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/handler_test.go#L62),
          [`#L124`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/handler_test.go#L124),
          [`style_test.go#L145`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/httpapi/style_test.go#L145),
          [`token_test.go#L111`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L111),
          and [`#L233`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/token_test.go#L233).
        - Code at v0.9.0 for the ASIP:
          [`handler.go#L346-L356`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L346-L356).
    - **Related**: [REQ-86](#req-86), [REQ-87](#req-87), [REQ-91](#req-91),
      [F-95](../traceability/findings.md#f-95), [Q-33](../traceability/open-questions.md#q-33), [E5](../traceability/standards-feedback.md#e5),
      [ADR 0042](../decisions/0042-asi-attribute-token-binding.md).
    - **Notes**: the list is a design choice. It is one RFC 9396
      `authorization_details` of the provisional type
      `https://gbo.example/authorization-details/authentic-source-attributes`.
      It has these fields:
        - `locations`, equal to `resource`
        - `actions`, equal to the scope
        - `attribute_identifiers`, with 1 to 50 unique https URIs

        Only parties that know that type can use the binding. A QTSP that
        implements only ETSI connects without a list. In the demo,
        `AZSP_REQUIRE_AUTHORIZATION_DETAILS=true` makes the list mandatory.
        Whether the Netherlands imposes the binding is [Q-33](../traceability/open-questions.md#q-33). ETSI does
        not provide the binding ([E5](../traceability/standards-feedback.md#e5)).

## REQ-112: The ASIP offers the clause 6.1 interface {#req-112}

> The ASIP MUST offer the interface of ETSI TS 119 478 clause 6.1: verify
> and retrieve over HTTP, with authorization according to OAuth 2.0. Until
> [Q-64](../traceability/open-questions.md#q-64) decides otherwise, the ASIP does not offer the interface of
> clause 6.2 (ISO 15000).

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) REQ-ASIP-4.3-04. The ASIP chooses clause 6.1,
          clause 6.2, or both.
        - Annex IV of Implementing Regulation (EU) [2026/1735](https://eur-lex.europa.eu/eli/reg_impl/2026/1735/oj). For verify,
          it designates clause 6.1.1, or 6.2.3, or both.
        - "Afspraken en standaarden" of [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) ("ETSI TS 119 478
          V1.1.1 voor de inrichting van de ASI-provider").
    - **Addressee**: GBO-delivered component: the ASIP. Interface agreement.
    - **Evidence**: [PR #499](https://github.com/ICTU/GBO-demo/pull/499), [PR #540](https://github.com/ICTU/GBO-demo/pull/540), [PR #574](https://github.com/ICTU/GBO-demo/pull/574).
      The demo ASIP offers only clause 6.1
      ([`asi-route.md#L98`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/asi-route.md#L98)). The conformance matrix
      marks clause 6.2 as a group that is not applicable
      ([`etsi-ts-119478.yaml#L9-L11`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/etsi-ts-119478.yaml#L9-L11)).
      It marks REQ-ASIP-4.3-04 as passed
      ([`#L38-L42`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/etsi-ts-119478.yaml#L38-L42)).
    - **Related**: [F-80](../traceability/findings.md#f-80), [Q-64](../traceability/open-questions.md#q-64),
      [ADR 0037](../decisions/0037-asi-oauth-front-door.md).
    - **Notes**: this requirement is a choice within REQ-ASIP-4.3-04. The
      [profile](#asi-profile) records it. [Q-64](../traceability/open-questions.md#q-64) asks whether clause 6.2
      becomes necessary later, also for deferred responses.

## REQ-113: Fuzzy matching only on free text, with documented rules {#req-113}

> An ASIP that supports fuzzy matching (REQ-ASIP-6.1.1.1-10) MUST apply it
> only to free text, such as names and address lines. It MUST NOT apply it
> to dates, codes, and numbers. It MUST publish the rules that it applies. A
> QTSP then knows when it can get `MatchWithVariation`.

| Case | Outcome |
|---|---|
| A name that differs only in case, diacritics, hyphens, or white space | `MatchWithVariation` (code) |
| A date or code that differs only in this way, for example `1990-01-01` and `1990 01 01` | `NoMatch`. For dates, the demo does this since v0.9.0 (code). For codes, see the notes. |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design. The source is [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf)
      REQ-ASIP-6.1.1.1-10. It leaves fuzzy matching free. It names
      differences in transliteration, spaces, hyphens, and compounding "and
      similar orthographic variations". These differences fit text and do not
      fit a date or a code. ETSI prescribes no rules, and this requirement
      makes that stricter.
    - **Addressee**: interface agreement: every ASIP that offers fuzzy
      matching.
    - **Evidence**: [PR #499](https://github.com/ICTU/GBO-demo/pull/499). Code and tests:
        - Historical code: the rules are documented
          ([README `asi-provider`#L143](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/README.md#L143))
          and built
          ([`match.go#L110-L131`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/match.go#L110-L131)).
          The test is in [`handler_test.go#L119-L136`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L119-L136).
          At that commit, the demo normalized every string
          ([`match.go#L44-L48`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/match.go#L44-L48)).
        - Code at v0.9.0: since step 5 of [ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592)
          ([PR #624](https://github.com/ICTU/GBO-demo/pull/624)), a string with a `format` in the value schema
          matches exactly or not. An example is the birth date
          ([`match.go#L27-L54`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/match.go#L27-L54),
          [`asi-attributes.json`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json)). The rules are in the
          [README `asi-provider`#L158](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/README.md#L158). The test is in
          [`service_test.go#L330-L348`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service_test.go#L330-L348).
    - **Related**: [REQ-84](#req-84), [REQ-85](#req-85), [Q-38](../traceability/open-questions.md#q-38),
      [Q-70](../traceability/open-questions.md#q-70) (normalization for each kind of value),
      [ADR 0039](../decisions/0039-asi-source-described-attributes.md).
    - **Notes**:
        - The value schema of an attribute marks what free text is. The
          source metadata define this ([ICTU/GBO-demo#592](https://github.com/ICTU/GBO-demo/issues/592): "fuzzy matching
          follows the type", through `value_schema`). In v0.9.0, the marker
          is the JSON Schema `format`.
        - The demo still normalizes a code without a `format`. Nationality
          `nl` against `NL` gives `MatchWithVariation`. A postal code in
          another way of writing also gives `MatchWithVariation`. For codes,
          demo v0.9.0 does not meet the requirement.
        - The rules of the demo itself (ICAO Doc 9303, diacritics, hyphens,
          white space, case) are not a requirement.

## REQ-114: A request on behalf of another person gets 501 {#req-114}

> Until [Q-65](../traceability/open-questions.md#q-65) decides otherwise, the ASIP MUST NOT support verify and
> retrieve requests on behalf of another subject (`mandate`). It MUST
> answer them with 501, without asking the source anything.

| Case | Outcome |
|---|---|
| Verify with `mandate` | 501, and the ASIP does not ask the source (code) |
| Retrieve with `mandate` | 501, and the ASIP does not ask the source (code) |
| Malformed request with `mandate` | 400 comes first (code) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design. The source is [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf)
      REQ-ASIP-6.1.1.1-12, which leaves support of `mandate` free. The 501
      then follows from REQ-ASIP-6.1.1.1-13. ETSI leaves the content of
      `mandate` outside the specification (NOTE 3).
    - **Addressee**: GBO-delivered component: the ASIP. Interface agreement.
    - **Evidence**: [PR #499](https://github.com/ICTU/GBO-demo/pull/499), [PR #542](https://github.com/ICTU/GBO-demo/pull/542). Code and tests:
        - Historical code: the demo refuses before it asks the source
          ([`service.go#L107-L109`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service.go#L107-L109),
          [`#L140-L142`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service.go#L140-L142)),
          with 501
          ([`handler.go#L364-L365`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler.go#L364-L365)).
          The test is in [`handler_test.go#L190-L203`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L190-L203).
          The test for the order is in
          [`service_test.go#L90`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service_test.go#L90).
        - Code at v0.9.0: [`service.go#L133-L135`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L133-L135),
          [`#L205-L207`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L205-L207),
          and [`handler.go#L373-L374`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L373-L374).
          The test is in [`handler_test.go#L186-L199`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L186-L199).
    - **Related**: [REQ-112](#req-112),
      [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
      (representation), [Q-65](../traceability/open-questions.md#q-65).
    - **Notes**: this requirement is a choice within REQ-ASIP-6.1.1.1-12. The
      [profile](#asi-profile) records it. [Q-65](../traceability/open-questions.md#q-65) asks whether representation
      becomes necessary later, and where the evidence then comes from.

## REQ-115: The ASIP verifies attribute fragments {#req-115}

> The ASIP MUST support the verification of attribute fragments
> (REQ-ASIP-6.1.1.1-07, -08). The contract of every data service MUST
> describe which JSONPath expressions (RFC 9535) the ASIP accepts for a
> fragment.

| Case | Outcome |
|---|---|
| Fragment with an expression from the supported subset | `Match`, `MatchWithVariation`, or `NoMatch` (code) |
| Expression that selects nothing in the source value | `Unknown` (code) |
| Expression outside the subset | 400 (code). There is no decision whether this must be 400 or 501. |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design. [ETSI TS 119 478](https://www.etsi.org/deliver/etsi_ts/119400_119499/119478/01.01.01_60/ts_119478v010101p.pdf) leaves fragments free
      (REQ-ASIP-6.1.1.1-08-01). If the ASIP does not support fragments, it
      gives 501 (REQ-ASIP-6.1.1.1-09). With fragments, a QTSP can have one
      part of an attribute verified without sending the rest. An example is
      the town of an address.
    - **Addressee**: GBO-delivered component: the ASIP. Interface agreement.
    - **Evidence**: [ICTU/GBO-demo#608](https://github.com/ICTU/GBO-demo/issues/608) is not built in demo v0.9.0. The
      built part comes from [PR #499](https://github.com/ICTU/GBO-demo/pull/499). Code and tests:
        - Historical code: the demo supports a subset of JSONPath
          ([`match.go#L149-L210`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/match.go#L149-L210),
          [`service.go#L211-L233`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service.go#L211-L233)).
          The tests are in [`handler_test.go#L169-L188`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/httpapi/handler_test.go#L169-L188)
          and [`service_test.go#L82-L87`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service_test.go#L82-L87).
        - Code at v0.9.0: the subset is in
          [`match.go#L176-L187`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/match.go#L176-L187),
          and the fragment check is in
          [`service.go#L290-L317`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L290-L317).
          The test is in [`handler_test.go#L165-L184`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler_test.go#L165-L184).
        - The description in the contract is not built in demo v0.9.0. The
          subset is only in the
          [README `asi-provider`#L160](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/README.md#L160).
    - **Related**: [REQ-112](#req-112), [REQ-113](#req-113).
    - **Notes**:
        - The choice of subset is a choice for the contract and is no
          requirement.
        - The demo answers an expression outside its subset with 400
          ([`service.go#L220-L221`](https://github.com/ICTU/GBO-demo/blob/819f3eb7dc7469cd59665ca61be1aff497cecf63/services/asi-provider/internal/verification/service.go#L220-L221)).
          There is no decision whether an expression that the ASIP does not
          support gives 400 or 501.
        - In v0.9.0, a fragment can point to a member that the source
          description does not provide, or provides as a constant. That
          fragment gets `Unknown`, and the ASIP does not ask the source
          ([`service.go#L140-L161`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L140-L161)).

## Removed numbers

These requirement numbers are no longer in use:

- REQ-96: merged into [REQ-91](#req-91) (the request page names the source).
- REQ-98: removed. The content of rule ASI0001 follows from
  [REQ-48](authorization.md#req-48), [REQ-74](authorization.md#req-74),
  [REQ-97](authorization.md#req-97), [REQ-79](pseudonymization.md#req-79),
  and [REQ-17](authorization.md#req-17).
- REQ-104: removed. The QTSP identifies the citizen itself, as a duty of
  the QTSP under ETSI and eIDAS ([REQ-88](#req-88)). See also
  [F-93](../traceability/findings.md#f-93) and [Q-40](../traceability/open-questions.md#q-40).
- REQ-105: removed. The QTSP issues an attestation only to the citizen
  that it identified, as a duty of the QTSP under ETSI and eIDAS
  ([REQ-88](#req-88)).

