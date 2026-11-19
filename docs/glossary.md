# Glossary

The TO is written in English. Each concept has one English term. On its
first use on a page, the term gets the Dutch name of the Globaal Ontwerp
in parentheses, for example "consent register (toestemmingsregister)".
After that, the page uses the English term only. Proper names stay as
they are: Gemeenschappelijke Bronontsluiting, Delen van gegevens via
Toestemming met Private dienstverleners, Globaal Ontwerp,
Projectstartarchitectuur, Technisch Ontwerp, MijnOverheid, DigiD, Logius,
BSN, Autorisatielijst BSN, Basisinrichting OOTS, Logboek Dataverwerkingen. One Dutch government
term also stays as it is, without a translation: bronhouder.

The following tables give each term, the Dutch name, its meaning, and the
words that the TO does not use for the same concept. The style linter
(`scripts/style_lint.py`) reports every word from a "Do not use" column
in running text. A Dutch name directly inside parentheses is allowed.
Code names, quotes from sources, and IDs are exempt. For the full
begrippenlijst of the GBO stelsel, see the
[GO begrippenlijst](https://ictu.github.io/GBO-GO/main/bijlage_begrippenlijst/).

## Building blocks and channels

These terms follow the [building block view](building-blocks/index.md):

| Term | Dutch (GO) | Meaning | Do not use |
|---|---|---|---|
| GBO Basis | GBO Basis | The part of GBO at every bronhouder: FSC, the PEP and the PDP, the source gateway, source configuration, and the records. It feeds every channel ([GBO Basis](building-blocks/gbo-basis/index.md)). | — |
| Channel | kanaal | A way in which GBO serves one kind of consumer. The three channels are DvTP, EUDI wallet, and OOTS. | trajectory |
| Route | — | One end-to-end flow through a channel: the DvTP route, the PuB-EAA route, the ASI route, the SDG-OOTS route, and the Gov-to-Gov route. | trajectory |
| Facility | voorziening | A shared function that GBO or another party provides, for example the consent facility. | voorziening |
| Consent facility | toestemmingsvoorziening | The GBO facility of the DvTP channel where the citizen gives, views, and revokes consent. It consists of the consent portal and the consent register ([Consent facility](building-blocks/dvtp/consent-service.md)). | toestemmingsvoorziening, consent service |
| Consent portal | toestemmingsportaal | The citizen-facing application of the consent facility (PSA S02). It has a frontend and a backend. The short form "portal backend" is allowed. | toestemmingsportaal |
| Consent register | toestemmingsregister | The register of consents (PSA S01). It signs the consent proof and answers the consent status. | toestemmingsregister |
| Pseudonymization facility | pseudonimiseervoorziening | BSNk PP: the Logius facility that the DvTP channel uses at consent time. | pseudonimiseervoorziening |
| PuB-EAA provider | PubEAA-voorziening | The GBO block of the EUDI wallet channel that issues an attestation from source data to the wallet ([PuB-EAA provider](building-blocks/eudi/pubeaa.md)). Legally, the bronhouder is the provider. | PubEAA |
| Issuance facility | — | The technical part of the PuB-EAA provider that GBO runs: the issuance server and the EUDI adapter ([ADR-0028](decisions/0028-pubeaa-productization.md)). | — |
| ASI | — | Authentic Source Interface: the interface of ETSI TS 119 478 through which a QTSP verifies or retrieves attributes at an authentic source (eIDAS article 45e). | — |
| ASI provider | ASI-provider | The GBO block of the EUDI wallet channel that offers the ASI. It consists of the ASIP and the ASI authorization server ([ASI provider](building-blocks/eudi/asi.md)). | — |
| OOTS adapter | OOTS-adapter | The GBO block of the OOTS channel that answers EU evidence requests. Design only ([OOTS channel](building-blocks/oots.md)). | — |
| Source gateway | — | The component in front of a source API (code name `bron-sidecar`). After the allow decision, it decrypts the value for its own OIN ([ADR-0033](decisions/0033-gateway-decrypts-after-allow.md)). | sidecar |
| Decryption component | — | The component of a source that reads the VI or VP for that source with its own keys. The source gateway calls it after the allow decision. | — |
| Admission register | toelatingsregister | The register of admitted participants and integrator mandates. The PDP pulls it as a PIP (code name `dvtp-onboarding-register`). | onboarding register |
| Source registry | — | The store of source descriptions: candidates, immutable releases, and the active release. | — |
| Source metadata | — | The description that a source publishes of its own services, at `/.well-known/gbo` ([Source configuration](building-blocks/gbo-basis/source-configuration.md)). | — |
| EUDI adapter | — | The component between the issuance server and the FSC chain. In the demo, its FSC peer is called "EDI issuer" (`edi-…`). | — |
| Wallet verifier | — | The nl-wallet verification server that the ASI authorization server uses for a login with the NL Wallet. | — |
| Integrator | integrator | A software party that calls a source on behalf of a consumer, under an FSC delegated grant and a registered mandate ([ADR-0034](decisions/0034-integrator-delegation.md)). | — |

## Domain terms

| Term | Dutch (GO) | Meaning | Do not use |
|---|---|---|---|
| Bronhouder | bronhouder | The government organization responsible for an authentic register and the access to it. The TO keeps this Dutch government term, also in English text, without translation. | source holder |
| Source | bron | A system of a bronhouder that answers queries. | — |
| Source access | (generieke) bronontsluiting | The part of GBO Basis that opens a source with one standard interface: the source gateway, the decryption component, and the GraphQL source API ([Source access](building-blocks/gbo-basis/source-access.md)). | bronontsluiting, generic source access |
| Citizen | burger | The data subject in GBO flows. | — |
| Consent | toestemming | The informed agreement of the citizen to a specific data exchange. | — |
| Consumer | afnemer | An organization that asks a bronhouder for data, in any channel. | afnemer |
| Service provider | dienstverlener | The private party that is the consumer in the DvTP channel. | dienstverlener |
| Controller | Verantwoordelijke | The party that decides on a processing (AVG). Under LDV, each controller keeps its own logbook. | — |
| Data subject | Betrokkene | The person whom a processing is about (AVG and LDV term). | — |
| Data set | gegevensset | A named group of fields that a consent covers as a whole ([REQ-10](requirements/consent.md#req-10)). | gegevensset |
| Service catalog | dienstencatalogus | The legally anchored register of the maximum scope that a consumer can ask for per use case. See [ADR-0008](decisions/0008-dienstencatalogus-ceiling.md). | dienstencatalogus |
| Purpose limitation | doelbinding | Processing of data is allowed only for the stated purpose. | — |
| Legal basis | grondslag | The legal ground for a processing or a provision of data. A legal basis set directly by law is a statutory basis (wettelijke grondslag). | grondslag |
| Interface | koppelvlak | A specified technical interface between parties or components. | koppelvlak |
| Interaction pattern | interactiepatroon | One of the patterns of the GO: A (EUDI wallet), B (OOTS), C (DvTP). | interactiepatronen |
| Processing | verwerking | Any operation on personal data (AVG term). | — |

## Consent, identity, and pseudonyms

| Term | Meaning | Do not use |
|---|---|---|
| Consent proof | The signed `gbo-consent+jwt` that the toestemmingsregister issues. It carries an encrypted value per source (`encrypted_subject`), the scopes, and the consumer ([ADR-0032](decisions/0032-consent-proof.md)). | — |
| Consent token | The same JWT as it travels in `X-GBO-Consent-Token`, before the PDP verified it. The evidence that selects the consent regime is a consent token. | — |
| Placeholder | The value that a dienstverlener puts in the query in place of the citizen: `consent:identity` or `consent:pseudonym`. The source gateway replaces it after the allow decision ([REQ-79](requirements/pseudonymization.md#req-79)). | — |
| Regime | The basis on which the PDP judges a request. The evidence in the request selects it ([ADR-0031](decisions/0031-regime-from-evidence.md)). With a consent token, the consent regime applies. Without one, the PID regime applies. | — |
| Designated issuer | An FSC peer on the actor list of the EUDI rules. Only a designated issuer can ask for source data under the PID regime. | — |
| Mandate (`acts_for`) | The registration in the admission register that an integrator acts for a consumer and a rule. The PDP reads it at request time. | — |
| BSN authorization list | The BSNk list (Autorisatielijst BSN) of the parties that are allowed to receive the BSN. A source on the list gets a VI in the consent proof. Other sources get only a VP. | — |
| PI | Polymorphic identity. A BSNk value made for the requester (the toestemmingsportaal) from the BSN. The toestemmingsregister stores it under the `subject_ref`. Recipients get a VI made from it. | — |
| PP | Polymorphic pseudonym. Like the PI, but for pseudonyms. Recipients get a VP made from it. | — |
| VI | Encrypted identity. A BSN that BSNk encrypted for one recipient OIN and one key version. Only that recipient can read it. | — |
| VP | Encrypted pseudonym. A pseudonym that BSNk encrypted for one recipient OIN and one key version. The BSNk specification calls it EP. | — |
| `subject_ref` | The reference under which the toestemmingsvoorziening knows a citizen: a keyed HMAC of the BSN (route D). It is not a BSNk value. | — |
| Peer ID | The identifier of an FSC peer. It is different from the OIN of the organization ([REQ-67](requirements/sources-identity.md#req-67)). | — |

## Records and tracing

| Term | Meaning | Do not use |
|---|---|---|
| Decision record | One ADL record: the authoritative record of a PDP decision ([ADR-0036](decisions/0036-adl-decision-record.md)). | — |
| Console decision log | The log of the policy engine that goes to Loki. It holds the detail per field, but it is observability, not audit. | — |
| LDV logbook | The logbook of one controller, with one record per processing ([ADR-0026](decisions/0026-ldv-integration.md)). | — |
| FSC txlog | The transaction log of an FSC peer (FSC-Logging): the authoritative record of transport. | — |
| W3C Trace Context | The `traceparent` and `tracestate` headers. The trace ID in `traceparent` is the correlation key of the chain ([ADR-0035](decisions/0035-w3c-trace-context.md)). | — |

## Abbreviations

| Term | Meaning |
|---|---|
| ADL | Authorization Decision Log. The Logius standard for the record of an authorization decision. In GBO, the ADL is the authoritative record of every PDP decision. |
| ASIP | Authentic Source Interface Provider. The GBO service that offers verify and retrieve as specified in ETSI TS 119 478 clause 6.1. It calls the source over FSC ([ADR-0037](decisions/0037-asi-oauth-front-door.md)). |
| AuthZEN | The OpenID standard for the evaluation interface from PEP to PDP. |
| AVG | Algemene verordening gegevensbescherming (GDPR). |
| AZSP | The ASI authorization server. It registers QTSPs, lets the citizen approve by logging in, and issues DPoP-bound access tokens. |
| BSN | Burgerservicenummer. The citizen identification number, restricted to authorized parties. |
| BSNk PP | BSN-koppelregister polymorphic pseudonymization. The Logius facility that turns a BSN into encrypted values per recipient. GBO uses it only at consent time ([ADR-0005](decisions/0005-bsnk-pp.md)). |
| DIP | Discover Interface Provider. The party that publishes the data service records of ASIPs. The demo has a stub. |
| DPoP | Demonstrating Proof of Possession (RFC 9449). It binds an access token to a key of the client. |
| DvTP | Delen van gegevens via Toestemming met Private dienstverleners. The consent-based channel. |
| EUDI wallet | European Digital Identity wallet (eIDAS2). |
| FSC | Federated Service Connectivity. The connectivity standard, with Inway, Outway, Manager, directory, and contracts. |
| FSC Manager | The FSC component of each peer that negotiates contracts and signs access tokens. It is different from the OpenFTV Manager. |
| FTV, OpenFTV | Federatieve Toegangsverlening. The authorization framework that hosts the PDP. |
| GBO | Gemeenschappelijke Bronontsluiting. |
| Gov-to-Gov | The route in which a government consumer gets data on a legal basis, without consent. Design only. |
| LDV | Logboek Dataverwerkingen. The Logius standard (v1.0.0) that records each processing in the logbook of its controller. |
| OIN | Organisatie-identificatienummer. The organization identifier, bound to PKI certificates. |
| OOTS | Once-Only Technical System. The EU cross-border evidence exchange under the SDG-verordening. |
| OpenFTV Manager | The policy administration component of OpenFTV. It stores policies and serves bundles to the PDP. It is different from the FSC Manager. |
| OpenID4VCI, OpenID4VP | Protocols for credential issuance and presentation. |
| PAP | Policy Administration Point. It authors and distributes policies. |
| PBAC | Policy-based access control. |
| PDP | Policy Decision Point. It evaluates authorization requests. |
| PEP | Policy Enforcement Point. It enforces PDP decisions. In this design, the FSC Inway is the PEP. |
| PID | Person Identification Data. The identity attestation in the EUDI wallet. |
| PIP | Policy Information Point. It supplies data to the PDP: the consent status and the admission register. |
| PuB-EAA | Public Body Electronic Attestation of Attributes. |
| QEAA | Qualified Electronic Attestation of Attributes. |
| QTSP | Qualified Trust Service Provider. In the ASI route, the QTSP is an OAuth client of the AZSP, not an FSC participant. |
| `QEAA_Provider` | The entitlement in the national register of relying parties that a QTSP needs to become an ASI client. |
| SD-JWT VC | The selective-disclosure JWT verifiable credential format (`dc+sd-jwt`). |
| VCT | Verifiable credential type identifier. It is published with `vct#integrity` over immutable Type Metadata. |

## Traceability terms

| Term | Meaning |
|---|---|
| BSNk precondition (BSNK-NN) | A fact about BSNk PP that the design must respect. It is not a requirement on GBO ([BSNk preconditions](requirements/pseudonymization.md#bsnk-preconditions)). |
| Connection condition (AV-NN) | A demand on a party that connects to GBO, not on GBO. The TO holds candidates for the management organization ([connection conditions](requirements/admission.md#connection-conditions)). |
| Demo increment (SL-NN) | A bounded piece of demo work with its result ([increments](traceability/increments.md)). The ID keeps the old prefix SL. |
| Finding (F-NN) | An observation from building the demo: a design gap, an exposed design choice, an implicit requirement, or an erratum ([findings](traceability/findings.md)). |
| Guideline (RL-NN) | A recommendation to bronhouders, for example on policy management. Not a demand on GBO ([policy management](requirements/authorization.md#policy-management)). |
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
