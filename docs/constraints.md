# Constraints

Four sources set the constraints for this design: the PSA, the law, the
GDI standards, and the functional requirements for DvTP. Each constraint
links to its normative text, and the TO does not restate that text. If a
design element conflicts with a constraint, one of these records the
conflict:

- an entry in [Risks and technical debt](risks.md),
- a [finding](traceability/findings.md),
- an [architecture decision](decisions/index.md).

## Architecture principles (PSA)

The 16 architectuurprincipes of the PSA bind this design. The PSA page
has no anchor per principle. For this reason, each link opens the
[principles page](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
The following principles constrain the technical design most directly:

| ID | Principle | Bearing on the TO |
|---|---|---|
| [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | Legal basis before exchange | Before data flows, the PDP judges every request under a regime. The evidence in the request selects the regime ([ADR-0031](decisions/0031-regime-from-evidence.md)). |
| [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | Minimal data processing | The PDP decides on each field of the GraphQL query ([REQ-17](requirements/authorization.md#req-17)). |
| [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | BSN-free for private consumers | In DvTP, the consumer holds no citizen identifier. After the allow decision, the source decrypts its own value ([ADR-0033](decisions/0033-gateway-decrypts-after-allow.md)). See [Pseudonymization](concepts/pseudonymization.md). |
| [P-06](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | Support for the EUDI wallet | The PSA treats this principle as a hook outside version 1. The demo still proves EUDI issuance and ASI verification. |
| [P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | Trust through recognized admission and trust anchors (until September 2026: "trust framework based on PKI") | Every FSC connection uses mTLS with PKI certificates. Admission comes from a register ([REQ-61](requirements/admission.md#req-61)). The legal identity comes from the certificate ([REQ-67](requirements/sources-identity.md#req-67)). See [Identity and trust](concepts/identity-trust.md). |
| [P-09](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | Open standards and vendor independence | The design uses FSC, AuthZEN, OpenID4VCI and OpenID4VP, GraphQL, OPA, LDV, W3C Trace Context, and OAuth 2.0. |
| [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | Data sovereignty: the bronhouder keeps control | Sources own their schema, service description, decryption keys, and policy. PAP and PDP are at the bronhouder ([ADR-0021](decisions/0021-central-pap-signed-bundles.md)). |
| [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | Logging and non-repudiation | The design has three authoritative records, one per Logius standard. The ADL holds the authorization decisions ([ADR-0036](decisions/0036-adl-decision-record.md)). The LDV logbook of each controller holds the processings ([ADR-0026](decisions/0026-ldv-integration.md)). FSC-Logging holds the transport. The W3C trace ID joins the three records, and the FSC transaction ID is recorded next to it ([ADR-0035](decisions/0035-w3c-trace-context.md)). See [Logging, audit and traceability](concepts/logging.md). |
| [P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | Transparency and access for the citizen | The citizen views and revokes consents ([REQ-38](requirements/consent.md#req-38)). Each controller can answer an access request from its LDV logbook. |
| [P-14](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) | Separation of generic and specific functions | GBO has one generic chain. Route-specific adapters are at the edge ([REQ-44](requirements/authorization.md#req-44)). |

For the full list (P-01 to P-16) and the status of each principle in the
demo, see the [matrix](traceability/matrix.md#architecture-principles).

## Design principles (PSA)

The 14 ontwerpprincipes govern how the GBO components are built. Each
link opens the
[design principles page](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/).
The following design principles constrain the TO most directly:

| ID | Principle | Bearing on the TO |
|---|---|---|
| [D-01](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/) | Decentral where possible, central where necessary | Each bronhouder has its own PDP and PAP. Each provider issues its own tokens. GBO has central components only where they are necessary: the toestemmingsvoorziening and the admission register. |
| [D-03](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/) | Use national generic facilities (GDI) unless | GBO reuses FSC, FTV, BSNk PP, DigiD, and PKIoverheid and does not rebuild them. The demo mocks DigiD, BSNk, and MijnOverheid. |
| [D-07](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/) | Open source unless | All GBO components and the demo are open source (EUPL). |
| [D-08](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/) | Comply or explain: mandatory open standards | A deviation from a mandated standard is an explicit ADR or risk. |
| [D-09](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/) | API-first | All koppelvlakken are specified APIs. See [Context and scope](context.md). |
| [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/) | Least privilege | Authorization is closed-world: without a rule, there is no access. Only the FSC Inway reaches the source gateway ([REQ-81](requirements/pseudonymization.md#req-81)). |
| [D-13](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/) | Standardize where possible, make exceptions explicit | Exceptions to a standard are visible in the data and in the ADR log. An example is the `file` metadata transport ([AV-08](requirements/admission.md#av-08)). |

For the full list (D-01 to D-14), see the
[matrix](traceability/matrix.md#design-principles).

## Requirements

The [requirements](requirements/index.md) state testable demands on what
GBO builds and on the interfaces between GBO and other parties. Each
requirement names its source. The source is a passage in the GO, the PSA,
or FR-DvTP, or a principle for which a demo finding showed the need. The
arc42 sections explain how the design meets the requirements. The status
of each requirement is one of these words: draft, ready for review,
approved, covered, or withdrawn.

The requirements page also lists the guidelines for bronhouders
([RL-01 to RL-05](requirements/authorization.md#policy-management)). A guideline is a
recommendation for bronhouders. It puts no demand on GBO.

## Connection conditions (candidates)

Some demands fall on the parties that connect to GBO, and GBO itself does
not carry them. The TO collects these demands as candidate connection
conditions ([AV-01 to AV-15](requirements/admission.md#connection-conditions)).
They are input for the management organization, which sets the real
connection conditions
([PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)).

The candidates apply to three types of party:

| Party | Candidates |
|---|---|
| Consumer | [AV-01](requirements/admission.md#av-01) trace context, [AV-02](requirements/admission.md#av-02) LDV, [AV-03](requirements/admission.md#av-03) toestemmingsvoorziening and BSNk PP, [AV-04](requirements/admission.md#av-04) own FSC peer. [AV-05](requirements/admission.md#av-05) proof sent unchanged, [AV-14](requirements/admission.md#av-14) contact details for GDPR rights, [AV-15](requirements/admission.md#av-15) equivalent alternative. |
| Integrator | [AV-06](requirements/admission.md#av-06) admitted separately, acts as processor |
| Bronhouder | [AV-07](requirements/admission.md#av-07) to [AV-13](requirements/admission.md#av-13): service description, consent to a taken-over description, old decryption keys, LDV for relation attestations, and validity and revocation policy |

## BSNk preconditions

BSNk PP sets preconditions that the DvTP design must respect
([BSNK-01 to BSNK-11](requirements/pseudonymization.md#bsnk-preconditions)). These
preconditions are facts about an external facility. They are not
requirements on GBO. Three of them shape the design most:

- Transformation is possible only while the citizen is logged in
  ([BSNK-04](requirements/pseudonymization.md#bsnk-04)). As a result,
  the toestemmingsvoorziening makes all values at consent time, and the proof
  freezes at consent ([F-78](traceability/findings.md#f-78)).
- Only a recognized party can activate and transform
  ([BSNK-01](requirements/pseudonymization.md#bsnk-01)). It is open
  whether the toestemmingsvoorziening can be such a party
  ([Q-26](traceability/open-questions.md#q-26),
  [Q-49](traceability/open-questions.md#q-49)).
- The interfaces are SOAP with PKIoverheid
  ([BSNK-11](requirements/pseudonymization.md#bsnk-11)). The demo mock
  offers the same operations as JSON.

How the register finds a returning citizen is an open design choice. The
working assumption is
[route D](requirements/pseudonymization.md#route-d)
([ADR-0040](decisions/0040-route-d-citizen-recognition.md), proposed).

## Functional requirements DvTP (FR-DvTP v0.9)

FR-DvTP v0.9 contains the functional requirements FR-01 to FR-39 for the
DvTP route. The document is not public. For this reason, the TO
names a criterion without a link, for example "FR-34, criterion 1". The
[matrix](traceability/matrix.md#fr-dvtp) gives the demo status per FR.

FR-DvTP v0.9 has known contradictions. If the text and a decision
conflict, the requirements follow the decision. The known contradictions
are:

- FR-22 to FR-24 name the same consent statuses with different words.
  The rationale of FR-23 contradicts its criteria
  ([F-97](traceability/findings.md#f-97)).
- FR-39 puts policy at a central authority, and FR-26 puts it at a
  central authorization component. FR-25 ties the GDPR pointer to
  "revocation no longer possible". FR-35 describes a register content
  that the design does not use ([F-98](traceability/findings.md#f-98)).

## Legal and regulatory constraints

The PSA groups its principles by legal kader. The following kaders
constrain this design:

| Constraint | Source | Bearing on the TO |
|---|---|---|
| AVG (GDPR) | [PSA architectuurprincipes](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), kader 1 | Data minimization, doelbinding, and grondslag. Each controller (Verantwoordelijke) logs its own processing ([ADR-0026](decisions/0026-ldv-integration.md)). |
| Wdo and PKIoverheid | PSA kader 3 | Organization identity through PKI certificates and the OIN. |
| eIDAS2 and ARF | PSA kader 4 | EUDI wallet support. Article 45e: the Authentic Source Interface ([ADR-0037](decisions/0037-asi-oauth-front-door.md)). |
| eIDAS implementing regulations of 2026 (ASI) | CIR (EU) 2025/1569 art. 9, CIR (EU) 2026/1735 Annex IV | Art. 9 applies from August 19, 2026. From January 1, 2027, the verify interface follows ETSI TS 119 478 clause 6.1.1, clause 6.2.3, or both. From that date, every result is sealed. The authorization part stays a national choice ([F-80](traceability/findings.md#f-80)). |
| eIDAS implementing regulations of 2026 (PuB-EAA) | CIR (EU) 2026/1735 (ETSI TS 119 471), CIR (EU) 2026/1731 (ETSI TS 119 412-6, TS 119 472-3), CIR (EU) 2026/1730, and CIR (EU) 2025/848 | PuB-EAA issuance falls under the same standard as QEAA issuance. The issuer needs designation and a registration with entitlement `PUB_EAA_Provider`. It also needs an access certificate, a registration certificate, and a qualified seal certificate with its own profile ([F-81](traceability/findings.md#f-81), [Q-28](traceability/open-questions.md#q-28)). |
| BSN legislation (Wabb) | PSA kader 6 | Private parties must not process the BSN. This rule drives pseudonymization and the BSN exception for the QTSP ([F-86](traceability/findings.md#f-86)). |
| SDG-verordening (EU 2018/1724) | [GO interactiepatronen](https://ictu.github.io/GBO-GO/main/#3-interactiepatronen) | The OOTS connection over AS4 is an obligation under EU law, and GBO has no choice in it ([ADR-0020](decisions/0020-as4-bridge-for-oots.md)). |

## Standards

The capabilities chapter of the PSA lists the afspraken, standards, and
voorzieningen per capability, with their gaps. See
[capabilities S01 to S11](https://ictu.github.io/GBO-PSA/main/capabilities/).
The design builds directly on the following standards:

- Connectivity and authorization: OpenFSC, OpenFTV with OpenID AuthZEN
  1.0 and the FTV GraphQL profile, OPA/Rego, GraphQL, and PKIoverheid.
- Pseudonymization: BSNk PP.
- EUDI issuance: OpenID4VCI, OpenID4VP, and SD-JWT VC.
- ASI verification: ETSI TS 119 478, OAuth 2.0 with PKCE, DPoP
  (RFC 9449), and JWT access tokens (RFC 9068). ASI verification also
  uses dynamic client registration (RFC 7591), authorization server
  metadata (RFC 8414), resource indicators (RFC 8707), rich authorization
  requests (RFC 9396), and problem details (RFC 9457).
- Logging and traceability: LDV 1.0.0 (Logboek Dataverwerkingen),
  ADL (Authorization Decision Log), FSC-Logging (draft), W3C Trace
  Context, and OpenTelemetry.

If the demo deviates from a standard that the PSA names, a risk entry
records the deviation. For example, the demo uses Rego instead of ODRL as
policy language ([R16](risks.md#r16)).

## Traceability

- Requirements: [REQ-17](requirements/authorization.md#req-17),
  [REQ-38](requirements/consent.md#req-38),
  [REQ-44](requirements/authorization.md#req-44),
  [REQ-61](requirements/admission.md#req-61),
  [REQ-67](requirements/sources-identity.md#req-67),
  [REQ-81](requirements/pseudonymization.md#req-81),
  [RL-01](requirements/authorization.md#rl-01) to
  [RL-05](requirements/authorization.md#rl-05),
  [AV-01](requirements/admission.md#av-01) to
  [AV-15](requirements/admission.md#av-15),
  [BSNK-01](requirements/pseudonymization.md#bsnk-01),
  [BSNK-04](requirements/pseudonymization.md#bsnk-04),
  [BSNK-11](requirements/pseudonymization.md#bsnk-11)
- Findings: [F-78](traceability/findings.md#f-78) (open),
  [F-80](traceability/findings.md#f-80) (open),
  [F-81](traceability/findings.md#f-81) (open),
  [F-86](traceability/findings.md#f-86) (open),
  [F-97](traceability/findings.md#f-97) (open),
  [F-98](traceability/findings.md#f-98) (open)
- Open questions: [Q-26](traceability/open-questions.md#q-26) (open),
  [Q-28](traceability/open-questions.md#q-28) (open),
  [Q-49](traceability/open-questions.md#q-49) (open)
- Demo increments: [SL-28](traceability/increments.md#sl-28) (done),
  [SL-51](traceability/increments.md#sl-51) (done)
