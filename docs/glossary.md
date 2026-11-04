# Glossary

The glossary gives the English equivalents of the Dutch domain terms in
the TO and defines the GBO-specific terms. For the full begrippenlijst of
the GBO stelsel, see the
[GO begrippenlijst](https://ictu.github.io/GBO-GO/main/bijlage_begrippenlijst/).

## Domain terms (Dutch to English)

| Term | English | Meaning |
|---|---|---|
| Afnemer | Consumer | Organization that requests data from a bronhouder. |
| Betrokkene | Data subject | The person whom a processing is about (AVG and LDV term). |
| Bronhouder | Source holder | Organization responsible for an authentic register and its ontsluiting. |
| Bronontsluiting | Source access | The provision of register data through a standard interface. |
| Burger | Citizen | The data subject in GBO flows. |
| Dienstverlener | Service provider | Party, often private, that uses data to deliver a service to the citizen. In DvTP, the dienstverlener is the consumer. |
| Dienstencatalogus | Service catalog | Legally anchored register of the maximum scope that a consumer can ask for per use case. See [ADR-0008](decisions/0008-dienstencatalogus-ceiling.md). |
| Doelbinding | Purpose limitation | Processing of data is allowed only for the stated purpose. |
| Gegevensset | Data set | A named group of fields that a consent covers as a whole ([REQ-10](requirements/consent.md#req-10)). |
| Gegevensstroom | Data flow, trajectory | One of the GBO exchange routes (DvTP, EUDI issuance, ASI verification, Gov-to-Gov, and SDG-OOTS). |
| Grondslag | Legal basis | The legal ground for a processing or a provision of data. |
| Koppelvlak | Interface | A specified technical interface between parties or components. |
| Toestemming | Consent | The informed agreement of the citizen to a specific data exchange. |
| Toestemmingsportaal | Consent portal | Citizen-facing application to grant, view, and revoke consents. Its backend is the consent portal backend. |
| Toestemmingsregister | Consent register | Machine-readable registration of consents. It signs the consent proof and answers the consent status. |
| Verantwoordelijke | Controller | The party that decides on a processing (AVG). Under LDV, each controller keeps its own logbook. |
| Verwerking | Processing | Any operation on personal data (AVG term). |
| Wettelijke grondslag | Statutory basis | A grondslag set directly by law. |

## Abbreviations and system terms

| Term | Meaning |
|---|---|
| ADL | Authorization Decision Log. Logius standard for the record of an authorization decision. In GBO, the ADL is the authoritative record of every PDP decision ([ADR-0036](decisions/0036-adl-decision-record.md)). |
| ASIP | Authentic Source Interface Provider. The GBO service that offers verify and retrieve as specified in ETSI TS 119 478 clause 6.1. It calls the source over FSC ([ADR-0037](decisions/0037-asi-oauth-front-door.md)). |
| AuthZEN | OpenID standard for the evaluation interface from PEP to PDP. |
| AVG | Algemene verordening gegevensbescherming (GDPR). |
| AZSP | The ASI authorization server. It registers QTSPs, lets the citizen approve by logging in, and issues DPoP-bound access tokens. |
| BSN | Burgerservicenummer. Citizen identification number, restricted to authorized parties. |
| BSN authorization list | BSNk list (Autorisatielijst BSN) of the parties that are allowed to receive the BSN. A source on the list gets a VI in the consent proof. Other sources get only a VP. |
| BSNk PP | BSN-koppelregister polymorphic pseudonymization. Logius facility that turns a BSN into encrypted values per recipient. GBO uses it only at consent time ([ADR-0005](decisions/0005-bsnk-pp.md)). |
| Consent proof | The signed `gbo-consent+jwt` that the consent register issues. It carries an encrypted value per source (`encrypted_subject`), the scopes, and the consumer ([ADR-0032](decisions/0032-consent-proof.md)). |
| Decryption component | The component of a source that reads the VI or VP for that source with its own keys. The source gateway calls it after the allow decision. |
| Designated issuer | An FSC peer on the actor list of the EUDI rules. Only a designated issuer can ask for source data under the PID regime. |
| DIP | Discover Interface Provider. The party that publishes the data service records of ASIPs. The demo has a stub. |
| DPoP | Demonstrating Proof of Possession (RFC 9449). It binds an access token to a key of the client. |
| DvTP | Delen van gegevens via Toestemming met Private dienstverleners. The consent-based trajectory. |
| EP | Encrypted pseudonym. An older name for the VP. The TO uses VP. |
| EUDI wallet | European Digital Identity wallet (eIDAS2). |
| FSC | Federated Service Connectivity. The connectivity standard, with Inway, Outway, Manager, directory, and contracts. |
| FSC Manager | The FSC component of each peer that negotiates contracts and signs access tokens. It is different from the OpenFTV Manager. |
| FSC-Logging | Logius draft standard for the transaction log of FSC. It is the authoritative record of transport. |
| FTV / OpenFTV | Federatieve Toegangsverlening. The authorization framework that hosts the PDP. |
| GBO | Gemeenschappelijke Bronontsluiting. |
| Integrator | A software party that calls a source on behalf of a consumer, under an FSC delegated grant and a registered mandate ([ADR-0034](decisions/0034-integrator-delegation.md)). |
| LDV | Logboek Dataverwerkingen. Logius standard (v1.0.0) that records each processing in the logbook of its controller. Citizen access is one use of its read extension ([ADR-0026](decisions/0026-ldv-integration.md)). |
| Mandate (`acts_for`) | The registration in the admission register that an integrator acts for a provider and a rule. The PDP reads it at request time. |
| OIN | Organisatie-identificatienummer. Organization identifier, bound to PKI certificates. |
| OOTS | Once-Only Technical System. EU cross-border evidence exchange under the SDG-verordening. |
| OpenFTV Manager | The policy administration component of OpenFTV. It stores policies and serves bundles to the PDP. It is different from the FSC Manager. |
| OpenID4VCI / OpenID4VP | Protocols for credential issuance and presentation. |
| PAP | Policy Administration Point. It authors and distributes policies. |
| PBAC | Policy-based access control. |
| PDP | Policy Decision Point. It evaluates authorization requests. |
| Peer ID | The identifier of an FSC peer. It is different from the OIN of the organization ([REQ-67](requirements/sources-identity.md#req-67)). |
| PEP | Policy Enforcement Point. It enforces PDP decisions. In this design, the FSC Inway is the PEP. |
| PI | Polymorphic identity. BSNk value made for the requester (the consent portal) from the BSN. It stays with the requester: the register stores it under the `subject_ref`. Recipients get a VI made from it. |
| PID | Person Identification Data. The identity attestation in the EUDI wallet. |
| PIP | Policy Information Point. It supplies data to the PDP: the consent status and the admission register. |
| Placeholder | The value that a DvTP consumer puts in the query in place of the citizen: `consent:identity` or `consent:pseudonym`. The source gateway replaces it after the allow decision ([REQ-79](requirements/pseudonymization.md#req-79)). |
| PP | Polymorphic pseudonym. Like the PI, but for pseudonyms. Recipients get a VP made from it. |
| PuB-EAA | Public Body Electronic Attestation of Attributes. |
| QEAA / QTSP | QEAA is a Qualified Electronic Attestation of Attributes. QTSP is a Qualified Trust Service Provider. |
| `QEAA_Provider` | The entitlement in the national register of relying parties that a QTSP needs to become an ASI client. |
| QTSP reference client | `qtsp-reference`, the demo client that acts as the QTSP in the ASI route. It is not a GBO component. |
| Regime | The basis on which the PDP judges a request. The evidence in the request selects it ([ADR-0031](decisions/0031-regime-from-evidence.md)). With a consent proof, the consent regime applies. Without one, the PID regime applies. |
| SD-JWT VC | Selective-disclosure JWT verifiable credential format (`dc+sd-jwt`). |
| Source gateway | The component in front of a source API (`bron-sidecar`). After the allow decision, it decrypts the value for its own OIN ([ADR-0033](decisions/0033-gateway-decrypts-after-allow.md)). |
| `subject_ref` | The reference under which the consent service knows a citizen: a keyed HMAC of the BSN (route D). It is not a BSNk value. |
| VCT | Verifiable credential type identifier. It is published with `vct#integrity` over immutable Type Metadata. |
| VI | Encrypted identity. A BSN that BSNk encrypted for one recipient OIN and one key version. Only that recipient can read it. |
| VP | Encrypted pseudonym. A pseudonym that BSNk encrypted for one recipient OIN and one key version. |
| W3C Trace Context | The `traceparent` and `tracestate` headers. The trace ID in `traceparent` is the correlation key of the chain ([ADR-0035](decisions/0035-w3c-trace-context.md)). |

## Traceability terms

| Term | Meaning |
|---|---|
| BSNk precondition (BSNK-NN) | A fact about BSNk PP that the design must respect. It is not a requirement on GBO ([BSNk preconditions](requirements/pseudonymization.md#bsnk-preconditions)). |
| Connection condition (AV-NN) | A demand on a party that connects to GBO, not on GBO. The TO holds candidates for the management organization ([connection conditions](requirements/admission.md#connection-conditions)). |
| Finding (F-NN) | An observation from building the demo: a design gap, an exposed design choice, an implicit requirement or an erratum ([findings](traceability/findings.md)). |
| Guideline (RL-NN) | A recommendation to bronhouders, for example on policy management. Not a demand on GBO ([policy management](requirements/authorization.md#policy-management)). |
| Increment (SL-NN) | A demo increment: a bounded piece of demo work with its result ([increments](traceability/increments.md)). The ID keeps the old prefix SL. |
| Open question (Q-NN) | A question that the demo cannot answer, with the forum that must answer it and the working assumption until then ([open questions](traceability/open-questions.md)). |
| Quality scenario (QS-NN) | A testable scenario for a quality goal ([quality requirements](quality.md)). |
| Requirement (REQ-NN) | A testable demand on what GBO builds or on its interfaces ([requirements](requirements/index.md)). |

## Traceability

- Requirements: [REQ-10](requirements/consent.md#req-10),
  [REQ-67](requirements/sources-identity.md#req-67),
  [REQ-79](requirements/pseudonymization.md#req-79)
- Findings: [F-75](traceability/findings.md#f-75) (open)
- Open questions: none
- Demo increments: [SL-51](traceability/increments.md#sl-51) (done)
