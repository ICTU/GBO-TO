# Identity and trust

GBO must know which organization it deals with, and which certificate the
chain uses for which purpose. The design keeps two questions apart:

- Who is this organization? This is the legal identity (OIN and name) and
  the technical identity on FSC.
- Which certificates does EUDI need? These are the trust roles of
  attestation issuance and of the Authentic Source Interface.

The capabilities are
[S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
and [F1](https://ictu.github.io/GBO-PSA/main/generieke-functies/#f1-identiteit-vertrouwen),
under [P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
(trust through recognized admission and trust anchors). These decisions
apply:

- [ADR-0003](../decisions/0003-fsc-connectivity.md): FSC for all
  connectivity.
- [ADR-0023](../decisions/0023-identity-convergence.md): part A,
  organization identity (accepted), and part B, EUDI certificate roles
  (proposed).
- [ADR-0028](../decisions/0028-pubeaa-productization.md): PuB-EAA
  productization (proposed).

For the requirements, see
[Identity, trust and transport](../requirements/sources-identity.md#identity-trust).

Authorization per request is a separate layer. FSC establishes the
organization, but this tells nothing about what the organization can do in
one request. For more information, see [Authorization](authorization.md).

## Three identity carriers

An organization in the chain has three identifiers
([F-60](../traceability/findings-closed.md#f-60)):

| Carrier | What it identifies | Source |
|---|---|---|
| FSC Peer ID | the FSC peer: the system that sends or receives FSC traffic | `subject.serialNumber` of the FSC certificate |
| OIN | the legal organization (bronhouder, consumer) | `serialNumber` of the organization's certificate |
| Organization name | the legal name that a wallet or a record shows | exactly one `O` attribute of the same certificate |

If the bronhouder runs its own peer, its Peer ID is its OIN. In other cases,
the two values can differ. One peer can offer services of more than one
bronhouder. Simulation Peer IDs are not OINs, for example
`0000009950HYPBV00000`. Until [SL-49](../traceability/increments.md#sl-49)
([PR #242](https://github.com/ICTU/GBO-demo/pull/242)), the demo used one
field for both values. In demo v0.9.0, the source configuration keeps
`provider_peer_id` as a separate field
([`source_configuration.go#L35-L44`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_configuration.go#L35-L44)).

It is open whether policy can read the Peer ID of a consumer as its OIN.
The alternative is that policy takes that link from the admission register
([Q-68](../traceability/open-questions.md#q-68)).

## The legal identity comes from the certificate

A GBO component can put the OIN or name of a bronhouder in an attestation
or a decision record. The component takes that value from verified
certificate material. A value that an operator can fill in freely is never
the source ([REQ-67](../requirements/sources-identity.md#req-67),
[ADR-0023](../decisions/0023-identity-convergence.md), part A).

The certificate content decides the result:

| Certificate | Result |
|---|---|
| 20-digit OIN in `serialNumber`, exactly one organization name | The OIN and the name come from the certificate |
| The configured OIN or name differs from the certificate | Refused: the component does not load the set |
| No 20-digit OIN, or not exactly one organization name | Refused (`CERTIFICATE_SET_INVALID`) |

The rule is in
[`development_ca_provider.go#L280-L288`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/development_ca_provider.go#L280-L288)
and
[`source-registry/onboarding/service.go#L293-L297`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L293-L297).
The source document also names its `source_oin`. This value must equal the
OIN in the certificate set. If it differs, the onboarding refuses the
document ([Source onboarding](source-onboarding.md)). The issuer name, the
description, and the logo that the wallet shows also come from the
certificate ([PR #321](https://github.com/ICTU/GBO-demo/pull/321)).

This rule has these consequences:

- The runtime gets leaf material and public CA certificates, but never CA
  private keys. Provisioning is a separate privileged command.
- Consents are bound to the identity of the consumer. If that identity
  changes, the consents become unusable. The migration in
  [PR #244](https://github.com/ICTU/GBO-demo/pull/244) and
  [PR #277](https://github.com/ICTU/GBO-demo/pull/277) showed this.
- In the default demo onboarding, the Belastingdienst peer publishes RvIG
  with the Belastingdienst OIN. This is a demo shortcut, and it does not
  show one OIN per bronhouder. The certificate sets still differ per
  source.

## Every channel goes through FSC

Every channel that calls a source for an external party goes through FSC,
with a valid certificate
([REQ-46](../requirements/sources-identity.md#req-46),
[ADR-0003](../decisions/0003-fsc-connectivity.md)). DvTP, EUDI issuance,
and the ASIP each call through their own Outway. FSC traffic is mTLS
between peers. The Manager of the provider issues the access token with the
grant hash of the contract.

FSC refuses a connection with an expired or revoked certificate. open-fsc
checks revocation with a CRL cache. An operator can switch off this cache
per Inway, Outway, and Manager. The requirement forbids this. The demo does
not check this behavior. It is open within which time a revocation must
take effect ([Q-53](../traceability/open-questions.md#q-53)).

## Private parties

A private consumer authenticates in two ways, with separate roles
([Q-06](../traceability/answered-questions.md#q-06), answered):

- People use eHerkenning at onboarding and for management (FR-03).
- Systems use an organization certificate from a recognized issuer, linked
  to the OIN or the KvK number (FR-33, FR-34).

The candidate connection condition has two parts
([AV-04](../requirements/admission.md#av-04)):

- A private consumer runs its own FSC peer with a PKIoverheid certificate.
- The private consumer uses the OIN as its legal identity.

FR-33 allows an OIN or a KvK number. The link between OIN, KvK, and eIDAS
identifiers is an open S04 decision. The trust framework for private
parties as a whole is PSA decision B-09 in the
[besluitregister](https://ictu.github.io/GBO-PSA/main/vraagstukken/#besluitregister).

An integrator connects under FSC delegation. The consent binds the party
that the integrator represents
([ADR-0034](../decisions/0034-integrator-delegation.md)). The consent does
not bind the integrator.

## The PKIoverheid question

The first version of [ADR-0023](../decisions/0023-identity-convergence.md)
aimed at one infrastructure, with PKIoverheid as the anchor for all
certificates, including EUDI. GO and PSA no longer follow that ambition
([Q-07](../traceability/answered-questions.md#q-07), answered). The roles are
separate:

- PKIoverheid is the Dutch PKI for mTLS, FSC, and organization identity.
- A PuB-EAA carries a qualified electronic seal, from a certificate that a
  QTSP issues. Neither PKIoverheid nor an access CA seals it
  ([F-66](../traceability/findings-closed.md#f-66)).
- An access CA issues access certificates only (ETSI TS 119 411-8). An
  access certificate authenticates an issuer or relying party to the
  wallet. It never signs attestations.

Dutch EUDI governance decides which party operates the Dutch access CA.
This is a dependency outside the decision scope of GBO.

## EUDI issuance: a certificate set per source

The issuance facility keeps a certificate set per bronhouder. The set has
issuer, reader (access), and status-list certificates. The facility never
signs with the set of another bronhouder
([REQ-58](../requirements/eudi-issuance.md#req-58)). The issuer name and
the purpose that the wallet shows are bound to these certificates. A
fallback to the set of another source made the wallet show the wrong issuer
([F-50](../traceability/findings-closed.md#f-50)).

A missing or incomplete set blocks only that source. For the failure cases,
see [Source onboarding](source-onboarding.md#a-certificate-set-per-source).

## EUDI trust roles

GBO issues attestations for bronhouders. Each of these bronhouders needs
its own certificate per role, and one certificate never fills two roles
([ADR-0023](../decisions/0023-identity-convergence.md), part B, proposed,
[F-81](../traceability/findings.md#f-81)). The roles are as follows:

| Role | Purpose | Issued by | Trust anchor |
|---|---|---|---|
| Organization or system certificate | mTLS for FSC, and the OIN and name | PKIoverheid | PKIoverheid root |
| Access certificate | Authenticates the issuer to the wallet (OpenID4VCI) | An access CA (ETSI TS 119 411-8) | The access CA that the member state notifies |
| Registration certificate | Proves the registration, per registered service (since Implementing Regulation (EU) 2026/1730) | A provider that the member state appoints | Published by the member state |
| Qualified certificate for electronic seal | Seals the PuB-EAA. Profile ETSI TS 119 412-6 clause 8. Names the authentic source and the legal basis. Key in a QSCD | A QTSP | Open ([Q-30](../traceability/open-questions.md#q-30)) |
| Status-list certificate | Signs the status list for revocation | Open ([Q-17](../traceability/open-questions.md#q-17)) | Open |

[ADR-0028](../decisions/0028-pubeaa-productization.md) sets the roles and
responsibilities around these certificates:

- Each bronhouder is the PuB-EAA provider of its attestations. GBO operates
  the technical issuance facility. GBO is probably the `EEAIssuer` in the
  notification of each bronhouder. It is open who designates the Dutch
  PuB-EAA issuer, and who supervises
  ([Q-28](../traceability/open-questions.md#q-28)).
- The issuer registers as relying party with the entitlement
  `PUB_EAA_Provider`.
- It is open on which trust list PuB-EAA providers appear. The options are
  a List of Trusted Entities (ETSI TS 119 602) or the trusted lists
  (ETSI TS 119 612). The specifications contradict each other
  ([Q-30](../traceability/open-questions.md#q-30)). No decision exists for
  either list.
- It is open who holds the seal and status-list keys. The options are the
  central facility, a remote signing service, or an HSM at the bronhouder
  ([Q-17](../traceability/open-questions.md#q-17)). In the demo, the
  central issuance server holds them.

To verify the PID that the wallet discloses, the issuance server also
trusts PID issuers. Its list of PID trust anchors holds these CAs
([`issuance_server.toml.example#L3-L9`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/config/issuance_server.toml.example#L3-L9),
[`issuance_release.go#L120-L121`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_release.go#L120-L121)):

- The BZK pre-production PID issuer CA.
- The GBO development issuer CA.
- The issuer CA of every source.

That list is too broad. It must hold PID-provider anchors only. The
callback from the issuance server to the adapter has no caller
authentication ([REQ-45](../requirements/eudi-issuance.md#req-45),
[ADR-0018](../decisions/0018-eudi-disclosure-issuance.md)).

## ASI trust roles

In the ASI route, the QTSP is not an FSC participant. The chain on FSC
starts behind the ASIP ([F-87](../traceability/findings.md#f-87)). Two
trust points apply:

- Admission of a QTSP: only a QTSP with the `QEAA_Provider` right in the
  register becomes a client of the ASIP
  ([REQ-88](../requirements/asi.md#req-88)). That register and the
  certificate profile do not exist in demo v0.9.0
  ([F-85](../traceability/findings.md#f-85)). It is open which identifier
  links the access certificate of a QTSP to its register entry
  ([Q-35](../traceability/open-questions.md#q-35)).
- The seal on a result: the ASIP seals every verification result
  ([REQ-83](../requirements/asi.md#req-83)). The format is open
  ([Q-32](../traceability/open-questions.md#q-32),
  [ADR-0041](../decisions/0041-asi-seal-format.md)). The demo seals with a
  development certificate. This certificate is not a qualified seal
  certificate.

[ADR-0037](../decisions/0037-asi-oauth-front-door.md) describes the ASI
front door.

## Demo PKI and production

The demo generates its own trust anchors. Git ignores the private keys, and
the demo generates them again for each checkout.

The demo and production use different PKI parts:

| Area | Demo | Production |
|---|---|---|
| FSC group root | A self-hosted CA: cfssl with a root and intermediate CA (`GBO-DEMO Root CA`) ([`fsc-infra/pki/generate-root-ca.sh`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/pki/generate-root-ca.sh)) | PKIoverheid |
| FSC certificate requests | The FSC `ca-certportal` in front of cfssl ([`fsc-infra/docker-compose.yml#L60-L72`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L60-L72)) | The PKIoverheid issuance process of each organization |
| Organization certificates | Per organization, a group certificate with `serialNumber` = OIN, and internal mTLS certificates ([`bootstrap-bd-mock.sh#L48`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/pki/bootstrap-bd-mock.sh#L48)) | PKIoverheid certificates of each organization |
| PDP AuthZEN endpoint | A self-signed certificate that the Inways pin as CA ([`generate-pdp-cert.sh`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/pki/generate-pdp-cert.sh)) | An organization certificate |
| EUDI issuer and reader CAs | Two pre-provisioned development CAs. The demo never generates them, and onboarding stops without them ([`Makefile#L268-L272`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L268-L272)) | A QTSP for the seal, an access CA, and a registration certificate provider |
| Source leaf certificates | The development CA provider mints source-bound issuer, reader, and status-list leafs, under a separate privileged command ([`Makefile#L326-L336`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L326-L336)) | Issued per bronhouder, per role |
| ASIP seal and QTSP client certificates | From the same development CAs ([`Makefile#L276-L283`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L276-L283), [`#L320-L324`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L320-L324)) | A qualified seal certificate, and access certificates of admitted QTSPs |
| PID trust anchor | The BZK pre-production PID issuer CA | The notified PID providers |

In the demo, the development CA fills all EUDI roles at the same time.
Production separates the roles. The demo is not tested against these
standards ([F-81](../traceability/findings.md#f-81)):

- ETSI TS 119 471.
- The certificate profile.
- The checks of ETSI TS 119 472-3.

## Open points

These points about identity and trust are open:

- Can policy read the Peer ID of a consumer as its OIN
  ([Q-68](../traceability/open-questions.md#q-68))?
- The trust list for PuB-EAA providers
  ([Q-30](../traceability/open-questions.md#q-30)).
- Custody of the seal and status-list keys
  ([Q-17](../traceability/open-questions.md#q-17)).
- Designation of the Dutch PuB-EAA issuer, and supervision
  ([Q-28](../traceability/open-questions.md#q-28)).
- The identifier between a QTSP access certificate and its register entry
  ([Q-35](../traceability/open-questions.md#q-35)).
- The time limit for a revocation to take effect
  ([Q-53](../traceability/open-questions.md#q-53)).
- The trust framework for private parties (PSA B-09).
- Migration from the self-generated demo CAs.

## Traceability

- Requirements: [REQ-45](../requirements/eudi-issuance.md#req-45),
  [REQ-46](../requirements/sources-identity.md#req-46),
  [REQ-58](../requirements/eudi-issuance.md#req-58),
  [REQ-67](../requirements/sources-identity.md#req-67),
  [REQ-83](../requirements/asi.md#req-83),
  [REQ-88](../requirements/asi.md#req-88),
  [AV-04](../requirements/admission.md#av-04)
- Findings: [F-50](../traceability/findings-closed.md#f-50) (closed),
  [F-60](../traceability/findings-closed.md#f-60) (closed),
  [F-66](../traceability/findings-closed.md#f-66) (closed),
  [F-81](../traceability/findings.md#f-81) (open),
  [F-85](../traceability/findings.md#f-85) (open),
  [F-87](../traceability/findings.md#f-87) (open)
- Open questions: [Q-06](../traceability/answered-questions.md#q-06) (answered),
  [Q-07](../traceability/answered-questions.md#q-07) (answered),
  [Q-17](../traceability/open-questions.md#q-17) (open),
  [Q-28](../traceability/open-questions.md#q-28) (open),
  [Q-30](../traceability/open-questions.md#q-30) (open),
  [Q-32](../traceability/open-questions.md#q-32) (open),
  [Q-35](../traceability/open-questions.md#q-35) (open),
  [Q-53](../traceability/open-questions.md#q-53) (open),
  [Q-68](../traceability/open-questions.md#q-68) (open)
- Demo increments: [SL-34a](../traceability/increments.md#sl-34a) (done),
  [SL-34c](../traceability/increments.md#sl-34c) (done),
  [SL-49](../traceability/increments.md#sl-49) (done)
- Decisions: [ADR-0003](../decisions/0003-fsc-connectivity.md),
  [ADR-0023](../decisions/0023-identity-convergence.md),
  [ADR-0028](../decisions/0028-pubeaa-productization.md) (proposed)
