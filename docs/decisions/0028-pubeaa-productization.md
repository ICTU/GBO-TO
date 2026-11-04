# ADR-0028: PubEAA Provider productization

- Status: proposed
- Date: 2026-08-24, rewritten on 2026-11-02. The rewrite made the source holder (bronhouder) the PuB-EAA provider and GBO the technical issuance facility, and added the regulatory frame of F-81.
- Satisfies: [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte), [P-06](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [GO: PuB-EAA-uitgifte](https://ictu.github.io/GBO-GO/main/#uitgifte-van-attestaties-voor-de-eudi-wallet-pubeaa-uitgifte)
- Deliberation: reference architecture v0.6.2, gap 7 (archived and unpublished), [F-81](../traceability/findings.md#f-81), [F-82](../traceability/findings.md#f-82), [REQ-77](../requirements/eudi-issuance.md#req-77)
- Implemented in: demo grade. The issuance chain of [ADR-0018](0018-eudi-disclosure-issuance.md) works end to end with development CAs. [issuance_config.go#L166-L168](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_config.go#L166-L168) fixes the validity at 365 days.

## Context and problem statement

The government issues no PuB-EAAs. For this reason, the Netherlands
relies on commercial QTSPs for attestations from government sources. The
demo proves the issuance chain. Production status needs trust anchoring
and governance. The demo leaves these out on purpose.

The first version of this ADR made the shared GBO facility the PuB-EAA
provider that the member state notifies. That choice does not fit the
regulation or the GO:

- eIDAS article 3(46) names two possible issuers. One is the body that
  is responsible for the authentic source. The other is a public sector
  body that the member state designates on behalf of that body.
- The notification specification (EUDI TS2) assumes that the source holder
  is the provider. A party that issues on behalf of the source holder goes
  in the field `EEAIssuer`.
- The GO describes GBO as a technical, central, and optional issuance
  facility. Legally, GBO is not a PuB-EAA provider. The source holder stays
  legally responsible (PSA S11).

Since August 2026, PuB-EAA issuance also falls under the same standard as
QEAA issuance ([F-81](../traceability/findings.md#f-81)).

## Proposed decision

The proposal has seven parts:

1. Roles. Each source holder is the PuB-EAA provider of its attestations.
   GBO operates the technical issuance facility. GBO is probably the
   `EEAIssuer` in the notification of each source holder. The designation
   of GBO or the management organization under article 3(46) is an open
   decision ([Q-28](../traceability/open-questions.md#q-28)).
2. Conformity. The facility conforms to ETSI TS 119 471 with EN 319 401.
   Implementing Regulation 2026/1735 requires this for QEAA and PuB-EAA
   providers. Issuance follows OpenID4VCI as ETSI TS 119 472-3 specifies.
   The issuance checks the wallet instance attestation and the key
   attestation.
3. Certificates per source holder:
    - The facility seals the attestation in a QSCD, with a qualified seal
      certificate as ETSI TS 119 412-6 clause 8 specifies. The
      certificate names the authentic source and the legal basis (eIDAS
      article 45f(1)(b)).
    - Each registered service has its own access certificate and
      registration certificate.
    - The issuer registers as relying party with the entitlement
      `PUB_EAA_Provider`.
    - [ADR-0023](0023-identity-convergence.md) describes the roles.
4. Rulebook per type. Each Dutch attestation type gets a rulebook. The
   rulebook uses the template of the rulebooks catalogue.
5. Validity and revocation per type. The source holder sets them
   ([REQ-77](../requirements/eudi-issuance.md#req-77)):
    - If an attestation is valid for more than 24 hours, it carries a
      status reference.
    - The facility revokes the attestation on instruction of the
      source holder, and when the source data changes.
    - GBO only queries and gets no change signal
      ([F-82](../traceability/findings.md#f-82)). For this reason, each
      type chooses one of two forms: short-lived (less than 24 hours),
      or long-lived with a change feed from the source and revocation.
6. The callback gap of [ADR-0018](0018-eudi-disclosure-issuance.md) is
   closed with positive PID evidence and an authenticated callback
   ([REQ-45](../requirements/eudi-issuance.md#req-45)).
7. The facility is optional per source holder. Sources with capacity can
   run their own credential issuer.

## Consequences

- The legal responsibility for content, validity, and revocation stays
  with the source holder. GBO revokes technically, on instruction of the
  source holder ([AV-12](../requirements/admission.md#av-12),
  [AV-13](../requirements/admission.md#av-13)).
- Notification and registration happen per source holder. They do not
  happen once for GBO.
- Nobody tested the demo against ETSI TS 119 471, the certificate
  profile, or the checks of ETSI TS 119 472-3.
- The development CA of the demo stands in for all certificate roles at
  once. Production separates the roles.
- The central facility holds the private keys of the issuer and
  status-list certificates of every source. That needs a decision on key
  custody ([Q-17](../traceability/open-questions.md#q-17)).

## Open points

These points are open:

- Who holds and uses the seal and status-list keys of a source holder
  ([Q-17](../traceability/open-questions.md#q-17))? The options are the
  central facility, a remote signing service, or an HSM at the
  source holder.
- Who designates the Dutch PuB-EAA issuer, and who supervises
  ([Q-28](../traceability/open-questions.md#q-28))?
- On which trust list do PuB-EAA providers appear: a List of Trusted
  Entities or the trusted lists
  ([Q-30](../traceability/open-questions.md#q-30))? This point is open,
  and no fact settles it.
- Does every source answer get one seal, regardless of the channel
  ([Q-75](../traceability/open-questions.md#q-75))?
- The governance of the attestation schema per attestation type.

## Traceability

- Requirements: [REQ-45](../requirements/eudi-issuance.md#req-45),
  [REQ-58](../requirements/eudi-issuance.md#req-58),
  [REQ-77](../requirements/eudi-issuance.md#req-77),
  [AV-12](../requirements/admission.md#av-12),
  [AV-13](../requirements/admission.md#av-13)
- Findings: [F-66](../traceability/findings-closed.md#f-66) (closed),
  [F-81](../traceability/findings.md#f-81) (open),
  [F-82](../traceability/findings.md#f-82) (open)
- Open questions: [Q-17](../traceability/open-questions.md#q-17),
  [Q-28](../traceability/open-questions.md#q-28),
  [Q-30](../traceability/open-questions.md#q-30),
  [Q-75](../traceability/open-questions.md#q-75)
- Demo increments: [SL-26](../traceability/increments.md#sl-26)
