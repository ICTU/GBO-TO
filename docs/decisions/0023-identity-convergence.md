# ADR-0023: Organization identity from the certificate, and separate EUDI certificate roles

- Status: accepted (part A, organization identity), proposed (part B, EUDI certificate roles)
- Date: 2026-08-24, rewritten on 2026-11-02 for gbo-demo v0.9.0. The rewrite split the ADR into organization identity and EUDI certificate roles, and moved the BSNk production part out.
- Satisfies: [P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) (trust through recognized admission and trust anchors), [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte), [F1](https://ictu.github.io/GBO-PSA/main/generieke-functies/#f1-identiteit-vertrouwen)
- Deliberation: reference architecture v0.6.2, gap 2 and trust model comparison (archived and unpublished), [F-60](../traceability/findings-closed.md#f-60), [F-66](../traceability/findings-closed.md#f-66), [F-81](../traceability/findings.md#f-81), [SL-49](../traceability/increments.md#sl-49), and demo [PR #242](https://github.com/ICTU/GBO-demo/pull/242), [PR #247](https://github.com/ICTU/GBO-demo/pull/247), [PR #321](https://github.com/ICTU/GBO-demo/pull/321)
- Implemented in:
    - Part A: the OIN and the name come from the certificate in [development_ca_provider.go#L280-L288](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/development_ca_provider.go#L280-L288). The refusal of a set without OIN or name is in [source-registry/onboarding/service.go#L293-L297](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L293-L297). The Peer ID is separate from the OIN in [source_configuration.go#L35-L44](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_configuration.go#L35-L44).
    - Part B: not implemented. One development CA stands in for every role ([issuance_config.go#L159-L180](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_config.go#L159-L180)).

## Context and problem statement

The first version of this ADR had one goal: a single "converged" trust
and identity story. That story had three parts:

- PKIoverheid as the basis for all certificates.
- One common anchor for all organization identifiers.
- The production BSNk PP.

GO and PSA dropped that goal. P-07 does not name PKI any more
([Q-07](../traceability/answered-questions.md#q-07)). Two separate questions
remain.

Question A is: who is this organization? The demo had three identity
carriers side by side: the FSC Peer ID, a configured OIN, and the
certificate. One field mixed two identities, and the runtime held CA
private keys ([F-60](../traceability/findings-closed.md#f-60)). Simulation Peer
IDs are not OINs (`0000009950HYPBV00000`).

Question B is: which certificates does EUDI issuance need? The analysis
first confused the PuB-EAA seal and the access CA with PKIoverheid
([F-66](../traceability/findings-closed.md#f-66)). Since August 2026, PuB-EAA
issuance falls under ETSI TS 119 471. That standard has its own
registration and certificate profile
([F-81](../traceability/findings.md#f-81)).

The BSNk production part of the first version is not in this ADR.
[ADR-0005](0005-bsnk-pp.md) covers pseudonymization.
[ADR-0040](0040-route-d-citizen-recognition.md) covers citizen
recognition and the BSNk participant.

## Decision

### Part A: organization identity (accepted)

The decision for organization identity has five parts:

1. The legal identity of a bronhouder (OIN and organization name) comes
   from its verified certificate material. It does not come from
   configuration ([REQ-67](../requirements/sources-identity.md#req-67)).
   The OIN is the 20-digit `serialNumber`. The name is exactly one `O`
   attribute.
2. GBO refuses a configured OIN or name that differs from the
   certificate. GBO also refuses a certificate without a 20-digit OIN,
   or without exactly one organization name.
3. The configuration holds the FSC Peer ID separately from the OIN
   (`provider_peer_id`). One peer can offer services of more than one
   bronhouder.
4. The runtime gets leaf material and public CA certificates, never CA
   private keys. A separate privileged command does the provisioning.
5. FSC participants use PKIoverheid certificates
   ([ADR-0003](0003-fsc-connectivity.md)).

### Part B: EUDI certificate roles (proposed)

GBO issues attestations for a bronhouder. Each such bronhouder needs its
own certificates, one per role. One certificate never fills two roles.
The roles are as follows:

| Role | Purpose | Issued by | Trust anchor |
|---|---|---|---|
| Organization or system certificate | mTLS for FSC, and organization identity (OIN, name) | PKIoverheid | PKIoverheid root |
| Access certificate | Authenticates the issuer to the wallet (OpenID4VCI) | An access CA (ETSI TS 119 411-8) | The access CA that the member state notified |
| Registration certificate | Proves the registration of the service, one per registered service (since Implementing Regulation (EU) 2026/1730) | A provider of registration certificates that the member state appoints | Published by the member state |
| Qualified certificate for electronic seal | Seals the PuB-EAA. The profile is ETSI TS 119 412-6 clause 8. It names the authentic source and the legal basis (eIDAS art. 45f(1)(b)). The key is in a QSCD | A QTSP | Open: [Q-30](../traceability/open-questions.md#q-30) |
| Status-list certificate | Signs the status list for revocation | Open: [Q-17](../traceability/open-questions.md#q-17) | Open |

PKIoverheid is not an EUDI access CA. It is also not the seal
infrastructure for PuB-EAAs. An access CA issues access certificates
only, and it never signs attestations.
[REQ-58](../requirements/eudi-issuance.md#req-58) makes the certificate
set per source fail-hard ([ADR-0016](0016-source-owned-metadata.md)).

## Consequences

- An attestation and a decision record name the bronhouder with an
  identity that an operator cannot fill in freely.
- Consents are bound to the identity of the consumer. If that identity
  changes, the consents become unusable. The migration in
  [PR #244](https://github.com/ICTU/GBO-demo/pull/244) and
  [PR #277](https://github.com/ICTU/GBO-demo/pull/277) showed that the
  binding is real.
- In the default demo onboarding, the demo publishes RvIG through the
  Belastingdienst peer with the Belastingdienst OIN. That is a demo
  shortcut, so it does not show one OIN per bronhouder. The certificate
  sets still differ per source.
- The demo development CA stands in for all EUDI roles at once.
  Production separates the roles.
- The choice of the party that operates the Dutch access CA depends on
  Dutch EUDI governance. That choice is outside the decision scope of
  GBO.

## Open points

These points are open:

- Can policy read the FSC Peer ID of a consumer as its OIN, or must
  policy take that link from the register
  ([Q-68](../traceability/open-questions.md#q-68))?
- On which trust list do PuB-EAA providers appear: a List of Trusted
  Entities (ETSI TS 119 602) or the trusted lists (ETSI TS 119 612)? The
  specifications contradict each other
  ([Q-30](../traceability/open-questions.md#q-30)).
- Who holds the keys of the seal and status-list certificates: the
  bronhouder, or the central issuance facility
  ([Q-17](../traceability/open-questions.md#q-17))?
- How does the migration from the self-generated CAs of the demo work?

## Traceability

- Requirements: [REQ-46](../requirements/sources-identity.md#req-46),
  [REQ-58](../requirements/eudi-issuance.md#req-58),
  [REQ-67](../requirements/sources-identity.md#req-67)
- Findings: [F-60](../traceability/findings-closed.md#f-60) (closed),
  [F-66](../traceability/findings-closed.md#f-66) (closed),
  [F-81](../traceability/findings.md#f-81) (open)
- Open questions: [Q-06](../traceability/answered-questions.md#q-06),
  [Q-07](../traceability/answered-questions.md#q-07),
  [Q-17](../traceability/open-questions.md#q-17),
  [Q-30](../traceability/open-questions.md#q-30),
  [Q-68](../traceability/open-questions.md#q-68)
- Demo increments: [SL-34a](../traceability/increments.md#sl-34a),
  [SL-49](../traceability/increments.md#sl-49)
