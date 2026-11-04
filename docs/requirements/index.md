# Requirements

A requirement in this technical design is a testable demand on what GBO
builds, or on the interfaces between GBO and other parties. It follows
from the design (GO, PSA, FR-DvTP), or the GBO team derived it from
building the demo. Each requirement states where it comes from.

The arc42 sections explain the design, and the
[architecture decisions](../decisions/index.md) record the choices. A
requirement states the need that a section or a decision serves. Each
arc42 page and each ADR ends with a traceability footer. The footer lists
the requirements that the page explains or depends on. The
[traceability pages](../traceability/index.md) link requirements to
findings, open questions, and demo increments.

## When something is a requirement {#norm}

A `REQ-NN` counts as a requirement only with these four properties:

1. **Testable**: MUST, MAY, or MUST NOT, with a result that you can
   observe.
2. **Sourced**: it names the passage in the design that it follows from.
   For a requirement derived from the demo, the source is the principle
   or capability that it serves, with one sentence about the reason.
3. **Addressed**: it is addressed to a component that GBO delivers, or to
   an interface agreement (see [Addressee](#addressee)).
4. **A need**: it describes the need and does not describe the chosen
   solution.

The test for a derived requirement is one question: *which principle or
capability breaks without this requirement?* If there is no answer, it is
no requirement.

### What is not a requirement

Three levels of items are no requirements, and each level lands in its
own place:

| Level | Example | Where it lands |
|---|---|---|
| Demo glue | mocks, seeds, provisioning, the fake DigiD | nowhere |
| Implementation detail | a switch, a design pattern, a library | in the code |
| Design decision | never cache the status, or keep keys for at most five minutes | an ADR, or a note on the requirement that it serves |

**Need or decision**: ask *can another solution meet the same need?* If
yes, the need is the requirement, and the chosen solution is a design
decision.

**When a design decision becomes an ADR**: a design decision becomes an
ADR only if all three conditions apply:

- There were real alternatives.
- Going back is expensive (an interface, a data model, or another party).
- Someone outside the team must know about it or agree to it.

If not, the decision is a note "design choice" on the requirement that it
serves. Related choices go into one ADR. The ADRs are in
[Architecture decisions](../decisions/index.md).

### Entry format

Each requirement entry has this format:

```
## REQ-NN — Title as a statement {#req-nn}

> The [component] MUST [testable demand].

| Case | Outcome |        (optional: what must hold, with the deny reason)
|---|---|

- **Source**: design — PSA S04, FR-34 criterion 1
             or: derived — serves PSA S01: why, in one sentence
- **Addressee**: GBO-delivered component | interface agreement | guideline for bronhouders
- **Evidence**: demo issue or PR, with a permalink to the test or the code;
               or: not built — issue
- **Related**: links only (REQ, F, Q, ADR)
- **Notes**: only what a builder needs; an open point as a link to the Q
- **Status**: draft | ready for review | approved | covered | withdrawn
```

The fields have these rules:

- **Source**: the value is `design` if the design already states or
  sharpens the requirement. The value is `derived` if the requirement
  comes from the demo. PSA and GO links go to the published site. FR-DvTP
  criteria are named without a link until the FRs are public. The
  archived reference architecture (v0.6.2) is no longer a source. The PSA
  passage replaces it.
- **Evidence**: the place where the demo tests the requirement: an issue
  or PR in gbo-demo, and a permalink to the test or the code. Later, test
  tags with coverage from CI will replace this field.
- **Related**: only references that work as links.
- **Notes**: limits, design choices, and open points. No history: the
  page describes the design as it is.

### Status {#status}

An entry has one of these statuses:

| Status | Meaning |
|---|---|
| draft | written by the analysis team |
| ready for review | meets this norm |
| approved | accepted in the review with the tech lead |
| covered | a test shows the requirement |
| withdrawn | an approved requirement that no longer applies. It stays, with the reason and the successor, because others can refer to it |
| candidate | a connection condition (AV) that is proposed and not set |

If a requirement was never approved and no longer holds, the GBO team
removes it and does not withdraw it. Nobody uses its number again. For
more information, see [Removed numbers](#removed-numbers).

### Addressee: a MUST is only about what GBO builds {#addressee}

The system is federative ([Q-02](../traceability/answered-questions.md#q-02)),
and [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
puts the bronhouder in control. So a requirement that prescribes how a
bronhouder configures its own PDP, PAP, or policy engine is no
requirement. Nobody can enforce it in practice. Each requirement names
its addressee:

- **GBO-delivered component**: software that GBO builds and delivers as a
  generic component or reference implementation. A MUST applies, because
  it is a demand on an artifact of GBO itself. Delivery does not mean
  operation: most of these components run at the source (behind the
  Inway: PEP and PDP, adapters, request mappers, gateways). The
  requirement binds the GBO build. It does not limit the freedom of a
  source to choose something else.
- **Interface agreement**: behavior at the outside that every participant
  must deliver, because it follows from system or legal demands. For
  example, you can trace which policy version a decision used. A MUST
  applies, but only to the observable result. It never applies to the
  internal configuration or the product.
- **Guideline for bronhouders**: the internal configuration at a source.
  At most SHOULD, with the reason, or a selection criterion for a product.

Three other namespaces hold what is not a requirement on GBO:

- **`RL-NN`**: guidelines for bronhouders, on
  [Policy management](authorization.md#policy-management). Matrix and findings can
  refer to them like a requirement, without the suggestion that they are
  one. Each guideline has a promotion rule: the open question that must
  be answered before it can become a requirement.
- **`AV-NN`**: candidate connection conditions, obligations for other
  participants, on [Connection conditions](admission.md#connection-conditions).
- **`BSNK-NN`**: preconditions that BSNk PP, an external facility,
  imposes on GBO, on [BSNk preconditions](pseudonymization.md#bsnk-preconditions).

If you write a requirement, do two checks:

1. *Does the MUST sentence name a product or an implementation form that
   GBO does not deliver*? If so, reword the sentence to the role (PAP,
   PDP, management API), and change the addressee. The use of a
   product in the demo is a demo choice. It belongs in the evidence.
2. *Does the requirement assume that GBO runs something?* That is almost
   never certain. It is open which facilities are really central
   ([Q-10](../traceability/answered-questions.md#q-10),
   [Q-02](../traceability/answered-questions.md#q-02)). The demo runs
   everything in one stack, and that proves nothing about it. Write the
   requirement on the artifact or on the interface.

### Organization of the pages

Topic pages are grouped by trajectory: Generic (needed for every
channel), DvTP, and EUDI. A requirement that belongs to one trajectory
only is on a topic page of that trajectory. If a requirement moves to
another page, its number does not change.

## All requirements {#all-requirements}

Every live number is in one of the following tables. The trajectory is Generic (needed for every channel), DvTP, or EUDI. The source is `design` if the design already states the requirement, and `derived` if it comes from building the demo.

### Requirements (REQ)

These requirements apply to GBO-delivered components and interface agreements:

| ID | Title | Trajectory | Topic page | Source (design/derived) | Status |
|---|---|---|---|---|---|
| [REQ-04](authorization.md#req-04) | The source delivers only after a positive decision by its PDP | Generic | [Authorization](authorization.md) | design | ready for review |
| [REQ-06](authorization.md#req-06) | A denial carries a machine-readable reason: coarse for the consumer, full for the operator | Generic | [Authorization](authorization.md) | design | ready for review |
| [REQ-08](authorization.md#req-08) | Source access delivers only the fields that the request selects | Generic | [Data minimization](authorization.md#data-minimization) | design | ready for review |
| [REQ-10](consent.md#req-10) | Consent covers a whole data set, and the citizen does not pick fields within a set | DvTP | [Consent (DvTP)](consent.md) | design | ready for review |
| [REQ-11](authorization.md#req-11) | A GBO component fetches source data from the source for each request and does not store it | Generic | [Data minimization](authorization.md#data-minimization) | design | ready for review |
| [REQ-12](consent.md#req-12) | A consent is bound to one consumer, one service, and a named data scope | DvTP | [Consent (DvTP)](consent.md) | design | draft |
| [REQ-14](consent.md#req-14) | After revocation, the chain denies every later request on that consent | DvTP | [Consent (DvTP)](consent.md) | design | ready for review |
| [REQ-17](authorization.md#req-17) | The PDP decides on every field that the source runs, and denies an uncertain field list | Generic | [Query enforcement](authorization.md#query-enforcement) | design | ready for review |
| [REQ-18](authorization.md#req-18) | The PDP decides on facts that it established itself, and never on what the consumer declares | Generic | [Authorization](authorization.md) | design | ready for review |
| [REQ-19](consent.md#req-19) | A consent has a finite validity, and after that the PDP denies | DvTP | [Consent lifecycle](consent.md#consent-lifecycle) | design | ready for review |
| [REQ-20](pseudonymization.md#req-20) | In the consent path the consumer gets no BSN in the proof or in the response | DvTP | [Pseudonymization](pseudonymization.md) | design | draft |
| [REQ-21](pseudonymization.md#req-21) | The source converts the value from the proof itself, only after a positive decision and without a central party | DvTP | [Pseudonymization](pseudonymization.md) | design | ready for review |
| [REQ-23](consent.md#req-23) | The consent register gets no BSN, not even temporarily | DvTP | [Consent roles](consent.md#consent-roles) | design | draft |
| [REQ-24](consent.md#req-24) | The citizen identity comes from the authentication service assertion at the required assurance level and not from client input | DvTP | [Consent roles](consent.md#consent-roles) | design | ready for review |
| [REQ-32](logging-audit.md#req-32) | Audit records are protected, complete, and stored apart from operational logs | Generic | [Decision audit](logging-audit.md#decision-audit) | design | ready for review |
| [REQ-37](consent.md#req-37) | A consent request names the consumer, the service, the requested data sets, and the return address | DvTP | [Consent initiation](consent.md#consent-initiation) | design | draft |
| [REQ-38](consent.md#req-38) | A logged-in citizen can view consents with status and revoke them | DvTP | [Citizen access](consent.md#citizen-access) | design | draft |
| [REQ-39](consent.md#req-39) | Only the consent backend can create, query, and revoke the consents of a citizen in the register | DvTP | [Citizen access](consent.md#citizen-access) | design | draft |
| [REQ-40](consent.md#req-40) | A citizen sees and revokes only their own consents | DvTP | [Citizen access](consent.md#citizen-access) | design | draft |
| [REQ-42](authorization.md#req-42) | The authorization request follows an open PEP-PDP profile, and the PEP passes the request on unchanged | Generic | [Authorization](authorization.md) | design | ready for review |
| [REQ-44](authorization.md#req-44) | A channel adapter translates protocol, and the decision on source data lies with the PDP of the source | Generic | [Authorization](authorization.md) | derived | ready for review |
| [REQ-45](eudi-issuance.md#req-45) | The source is queried only about the citizen from a verified PID disclosure | EUDI | [EUDI issuance](eudi-issuance.md) | design | draft |
| [REQ-46](sources-identity.md#req-46) | Every channel that calls a source on behalf of an external party does so through FSC, with a valid certificate | Generic | [Identity and trust](sources-identity.md#identity-trust) | design | ready for review |
| [REQ-48](authorization.md#req-48) | Every rule checks actor and scope itself, and a request passes only if no check denies | Generic | [Authorization](authorization.md) | design | ready for review |
| [REQ-55](logging-audit.md#req-55) | One trace ID per request across the whole chain, and the transaction ID can be linked to it | Generic | [Observability](logging-audit.md#observability) | design | ready for review |
| [REQ-57](eudi-issuance.md#req-57) | An attestation about someone other than the requester follows an agreed relation from the verified requester | EUDI | [EUDI issuance](eudi-issuance.md) | derived | draft |
| [REQ-58](eudi-issuance.md#req-58) | Every source holder has its own certificate set for issuance, and missing material fails | EUDI | [EUDI issuance](eudi-issuance.md) | design | ready for review |
| [REQ-59](logging-audit.md#req-59) | The decision record names the policy version that decided | Generic | [Decision audit](logging-audit.md#decision-audit) | design | ready for review |
| [REQ-60](logging-audit.md#req-60) | Logging contains no BSN that the processing does not need | Generic | [Decision audit](logging-audit.md#decision-audit) | design | ready for review |
| [REQ-61](admission.md#req-61) | Admission comes from a register and not from decision policy | Generic | [Admission and contracts](admission.md) | design | ready for review |
| [REQ-62](admission.md#req-62) | The admission decision on a contract is its own rule set, separate from request policy | Generic | [Admission and contracts](admission.md) | design | ready for review |
| [REQ-63](admission.md#req-63) | An automated refusal of a contract proposal is recoverable | Generic | [Admission and contracts](admission.md) | derived | draft |
| [REQ-64](sources-identity.md#req-64) | A GBO component works only with the service description the source publishes itself, after validation | Generic | [Source metadata](sources-identity.md#source-metadata) | design | ready for review |
| [REQ-65](sources-identity.md#req-65) | Only an explicit management action takes a source into use, and a valid contract is not enough | Generic | [Source metadata](sources-identity.md#source-metadata) | design | ready for review |
| [REQ-66](sources-identity.md#req-66) | Source metadata fails closed per source, ages within bounds, and can be rolled back | Generic | [Source metadata](sources-identity.md#source-metadata) | design | ready for review |
| [REQ-67](sources-identity.md#req-67) | The legal identity of a source holder comes from its certificate and not from configuration | Generic | [Identity and trust](sources-identity.md#identity-trust) | design | draft |
| [REQ-68](consent.md#req-68) | The PDP decides only on a consent whose origin, binding, and current status it establishes itself | DvTP | [Consent (DvTP)](consent.md) | design | draft |
| [REQ-69](pseudonymization.md#req-69) | The consent register stores the polymorphic values under its own reference and no encrypted values per party | DvTP | [Pseudonymization](pseudonymization.md) | design | ready for review |
| [REQ-71](logging-audit.md#req-71) | Every authorization decision is in an ADL-conformant decision record, and that record is the audit source | Generic | [Decision audit](logging-audit.md#decision-audit) | design | ready for review |
| [REQ-72](logging-audit.md#req-72) | A GBO component that processes personal data writes an LDV log record for each processing at its controller | Generic | [Processing logging](logging-audit.md#processing-logging) | design | ready for review |
| [REQ-74](authorization.md#req-74) | The authorization regime follows from the evidence a request carries | Generic | [Authorization](authorization.md) | derived | ready for review |
| [REQ-75](consent.md#req-75) | Consent status is available within a set propagation time, availability, and latency | DvTP | [Consent (DvTP)](consent.md) | design | draft |
| [REQ-76](consent.md#req-76) | The register gives consent status only to an authenticated, authorized PDP, over FSC, and records who asked | DvTP | [Consent (DvTP)](consent.md) | design | draft |
| [REQ-77](eudi-issuance.md#req-77) | An attestation gets the validity and revocation policy of the source holder | EUDI | [EUDI issuance](eudi-issuance.md) | design | draft |
| [REQ-78](eudi-issuance.md#req-78) | Issuance issues nested claims, with selective disclosure per element as the schema prescribes | EUDI | [EUDI issuance](eudi-issuance.md) | design | draft |
| [REQ-79](pseudonymization.md#req-79) | Under a consent the subject comes only from the proof | DvTP | [Pseudonymization](pseudonymization.md) | derived | ready for review |
| [REQ-80](pseudonymization.md#req-80) | The proof carries a value per party that only that party can read, and the recipient checks that the value is meant for it | DvTP | [Pseudonymization](pseudonymization.md) | design | ready for review |
| [REQ-81](pseudonymization.md#req-81) | Only the component that enforces the decision reaches the source gateway | DvTP | [Pseudonymization](pseudonymization.md) | derived | ready for review |
| [REQ-82](pseudonymization.md#req-82) | When consent is given, the consent service knows the OIN, the key version, and the BSN authorization of each source | DvTP | [Pseudonymization](pseudonymization.md) | derived | draft |
| [REQ-83](asi.md#req-83) | Every ASIP verification result is sealed | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-84](asi.md#req-84) | `Unknown` only means the source has no (complete) value | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-85](asi.md#req-85) | The verify response contains no value from the source | EUDI | [Authentic Source Interface](asi.md) | derived | draft |
| [REQ-86](asi.md#req-86) | The access token carries the citizen's identification data and the means used to identify him | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-87](asi.md#req-87) | The ASIP takes the citizen only from a valid token bound to the QTSP that covers the operation | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-88](asi.md#req-88) | Only a QTSP with the `QEAA_Provider` right in the register becomes a client | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-89](asi.md#req-89) | The right of a registered client is re-checked periodically | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-90](asi.md#req-90) | The citizen approves the request by logging in, or refuses | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-91](asi.md#req-91) | The citizen sees who asks what at which source before logging in | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-92](asi.md#req-92) | The ASIP asks the source only for the fields of the requested attributes | EUDI | [Authentic Source Interface](asi.md) | derived | ready for review |
| [REQ-93](asi.md#req-93) | A chain that does not answer is an error, not `Unknown` | EUDI | [Authentic Source Interface](asi.md) | derived | ready for review |
| [REQ-94](asi.md#req-94) | Every ASI response names the one authentic source responsible for it | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-95](asi.md#req-95) | An access token is valid only for the source the citizen saw | EUDI | [Authentic Source Interface](asi.md) | derived | ready for review |
| [REQ-97](authorization.md#req-97) | Every rule names the FSC services it applies to | Generic | [Authorization](authorization.md) | derived | ready for review |
| [REQ-99](asi.md#req-99) | The ASIP provides a discovery record for each attribute and data service, with a path to endpoint, contract, and authorization server | EUDI | [Authentic Source Interface](asi.md) | design | draft |
| [REQ-100](asi.md#req-100) | A data service contract names its authorization-server metadata at the location RFC 8414 prescribes | EUDI | [Authentic Source Interface](asi.md) | design | draft |
| [REQ-101](asi.md#req-101) | A retrieve for which the source lacks a requested attribute is not found and gives no partial result | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-102](asi.md#req-102) | The authorization server identifies the citizen with the EUDI wallet through OpenID4VP and asks only the PID attributes in its registration | EUDI | [Authentic Source Interface](asi.md) | design | ready for review |
| [REQ-103](asi.md#req-103) | An authorization can be bound to the requested attributes, and the ASIP then processes only those attributes | EUDI | [Authentic Source Interface](asi.md) | design | draft |
| [REQ-106](consent.md#req-106) | An integrator acts only with a registered mandate, and the consent binds the represented party | DvTP | [Consent (DvTP)](consent.md) | design | ready for review |
| [REQ-107](consent.md#req-107) | Consent can be given only after confirmation that the citizen saw the information | DvTP | [Consent (DvTP)](consent.md) | design | ready for review |
| [REQ-108](consent.md#req-108) | The citizen can export the overview of consents | DvTP | [Citizen access](consent.md#citizen-access) | design | ready for review |
| [REQ-109](consent.md#req-109) | Revocation is possible only for a valid consent | DvTP | [Citizen access](consent.md#citizen-access) | design | ready for review |
| [REQ-110](admission.md#req-110) | A suspended or departed consumer gets no more data, even with a valid consent | Generic | [Admission and contracts](admission.md) | design | draft |
| [REQ-111](consent.md#req-111) | What the citizen sees about the consumer, and the return address, come from the registration and not from the request | DvTP | [Consent initiation](consent.md#consent-initiation) | design | ready for review |
| [REQ-112](asi.md#req-112) | The ASIP offers the clause 6.1 interface | EUDI | [Authentic Source Interface](asi.md) | design | draft |
| [REQ-113](asi.md#req-113) | Fuzzy matching only on free text, with documented rules | EUDI | [Authentic Source Interface](asi.md) | design | draft |
| [REQ-114](asi.md#req-114) | A request on behalf of another person gets 501 | EUDI | [Authentic Source Interface](asi.md) | design | draft |
| [REQ-115](asi.md#req-115) | The ASIP verifies attribute fragments | EUDI | [Authentic Source Interface](asi.md) | design | draft |
| [REQ-116](eudi-issuance.md#req-116) | An attestation contains only what the source answered, per its mapping, and an answer that does not fit gives no attestation | EUDI | [EUDI issuance](eudi-issuance.md) | design | draft |
| [REQ-117](consent.md#req-117) | Before choosing, the citizen sees in plain language who asks what, for what, and for how long | DvTP | [Consent (DvTP)](consent.md) | design | draft |
| [REQ-118](consent.md#req-118) | If a service excludes delegation, an authorized representative cannot give consent for it | DvTP | [Consent (DvTP)](consent.md) | design | draft |
| [REQ-119](consent.md#req-119) | After every outcome the citizen returns to the consumer with that outcome | DvTP | [Consent initiation](consent.md#consent-initiation) | design | draft |
| [REQ-120](consent.md#req-120) | For every consent and after every revocation, the portal points the citizen to their rights at the consumer | DvTP | [Citizen access](consent.md#citizen-access) | design | draft |
| [REQ-121](consent.md#req-121) | Screen, initiation check, and reference policy follow the same data-set description | DvTP | [Consent (DvTP)](consent.md) | design | draft |
| [REQ-122](consent.md#req-122) | The citizen gets a confirmation of their choice | DvTP | [Consent (DvTP)](consent.md) | design | draft |
| [REQ-123](admission.md#req-123) | Every change to an admission, mandate, or activation is traceable | Generic | [Admission and contracts](admission.md) | design | draft |
| [REQ-124](eudi-issuance.md#req-124) | For every attestation, the versions of the mapping, the source schema, and the attestation schema are traceable | EUDI | [EUDI issuance](eudi-issuance.md) | design | draft |

### Guidelines for bronhouders (RL)

The guidelines apply to the internal configuration of a bronhouder, and each guideline has a promotion rule:

| ID | Title | Trajectory | Topic page | Source (design/derived) | Status |
|---|---|---|---|---|---|
| [RL-01](authorization.md#rl-01) | Deliver policy as a versioned bundle instead of baking it into the PDP | Generic | [Policy management](authorization.md#policy-management) | design | ready for review |
| [RL-02](authorization.md#rl-02) | Authorize the management API with its own policy set and deny on an empty store | Generic | [Policy management](authorization.md#policy-management) | derived | ready for review |
| [RL-03](authorization.md#rl-03) | Separate writing from publishing, and publish with a non-personal, short-lived identity | Generic | [Policy management](authorization.md#policy-management) | design | ready for review |
| [RL-04](authorization.md#rl-04) | Withdraw policy instead of deleting it, and reconcile the deployed set with version control | Generic | [Policy management](authorization.md#policy-management) | design | ready for review |
| [RL-05](authorization.md#rl-05) | Validate a bundle before activation, and fall back visibly to the last valid set | Generic | [Policy management](authorization.md#policy-management) | design | ready for review |

### Candidate connection conditions (AV)

The candidates are obligations for other participants, and each entry names the obliged party:

| ID | Title | Trajectory | Topic page | Source (design/derived) | Status |
|---|---|---|---|---|---|
| [AV-01](admission.md#av-01) | Consumer sends trace context and records the transaction ID | DvTP | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-02](admission.md#av-02) | Consumer records its processing according to LDV | DvTP | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-03](admission.md#av-03) | Consumer uses the consent service and BSNk PP | DvTP | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-04](admission.md#av-04) | Consumer has its own FSC peer with PKIoverheid certificate and OIN | DvTP | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-05](admission.md#av-05) | Consumer sends the consent proof unchanged | DvTP | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-06](admission.md#av-06) | Integrator is admitted separately and acts as processor | DvTP | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-07](admission.md#av-07) | Source holder publishes a machine-readable description for each data service | Generic | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-08](admission.md#av-08) | Source holder without its own endpoint provably agrees with a taken-over description | EUDI | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-09](admission.md#av-09) | Source holder keeps decryption keys of an older version while proofs for that version are valid | DvTP | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-10](admission.md#av-10) | Source holder logs every living data subject of a relation attestation | EUDI | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-11](admission.md#av-11) | Source holder tests its view for relation attestations | EUDI | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-12](admission.md#av-12) | Source holder as provider has a public validity and revocation policy | EUDI | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-13](admission.md#av-13) | Source holder gives the instruction to revoke an attestation | EUDI | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-14](admission.md#av-14) | Consumer has registered contact details for GDPR rights | DvTP | [Connection conditions](admission.md#connection-conditions) | — | candidate |
| [AV-15](admission.md#av-15) | Consumer declares an equivalent alternative at admission | DvTP | [Connection conditions](admission.md#connection-conditions) | — | candidate |

### BSNk PP preconditions (BSNK)

BSNk PP imposes these preconditions on GBO, and they have no status of their own:

| ID | Title | Trajectory | Topic page | Source (design/derived) | Status |
|---|---|---|---|---|---|
| [BSNK-01](pseudonymization.md#bsnk-01) | Only a recognized party can activate and transform | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-02](pseudonymization.md#bsnk-02) | Activation needs the BSN and check data | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-03](pseudonymization.md#bsnk-03) | A PI belongs to the requester and nobody else | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-04](pseudonymization.md#bsnk-04) | Transformation is possible only while the citizen is logged in | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-05](pseudonymization.md#bsnk-05) | At most four recipients per request | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-06](pseudonymization.md#bsnk-06) | The BSN Authorization List sets BSN or pseudonym | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-07](pseudonymization.md#bsnk-07) | The recipient is an OIN | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-08](pseudonymization.md#bsnk-08) | An encrypted value belongs to one key version | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-09](pseudonymization.md#bsnk-09) | The recipient gets its keys through an Access Service or Key Requester | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-10](pseudonymization.md#bsnk-10) | The party that activates has the inspection duty | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |
| [BSNK-11](pseudonymization.md#bsnk-11) | The interfaces are SOAP with PKIoverheid | DvTP | [BSNk preconditions](pseudonymization.md#bsnk-preconditions) | — | — |

## Removed numbers {#removed-numbers}

If a requirement was never approved and no longer holds, the GBO team removes it. Nobody uses its number again. Topic pages list their own removed numbers with the reason. Each removed number has a disposition and, where one exists, a successor:

| Number | Disposition | Successor |
|---|---|---|
| REQ-01 | removed | — |
| REQ-02 | merged into | [REQ-61](admission.md#req-61) |
| REQ-03 | removed | — |
| REQ-05 | merged into | [REQ-48](authorization.md#req-48) |
| REQ-07 | removed | — |
| REQ-09 | merged into | [REQ-17](authorization.md#req-17) |
| REQ-13 | removed | [REQ-68](consent.md#req-68), [REQ-18](authorization.md#req-18) |
| REQ-15 | merged into | [REQ-79](pseudonymization.md#req-79) |
| REQ-16 | merged into | [REQ-55](logging-audit.md#req-55) |
| REQ-22 | removed | pending [Q-49](../traceability/open-questions.md#q-49) |
| REQ-25 | removed | [REQ-79](pseudonymization.md#req-79), [REQ-17](authorization.md#req-17) |
| REQ-26 | removed | [REQ-79](pseudonymization.md#req-79), [REQ-17](authorization.md#req-17) |
| REQ-27 | removed | [REQ-79](pseudonymization.md#req-79), [REQ-17](authorization.md#req-17) |
| REQ-28 | merged into | [REQ-55](logging-audit.md#req-55) |
| REQ-29 | merged into | [REQ-60](logging-audit.md#req-60) |
| REQ-30 | never used | — |
| REQ-31 | merged into | [REQ-71](logging-audit.md#req-71) |
| REQ-33 | removed | — |
| REQ-34 | removed | — |
| REQ-35 | merged into | [REQ-40](consent.md#req-40) |
| REQ-36 | removed | — |
| REQ-41 | merged into | [REQ-14](consent.md#req-14) |
| REQ-43 | removed | — |
| REQ-47 | removed | — |
| REQ-49 | removed | — |
| REQ-50 | merged into | [REQ-18](authorization.md#req-18) |
| REQ-51 | removed | [REQ-44](authorization.md#req-44), [REQ-64](sources-identity.md#req-64) |
| REQ-52 | removed | a design decision, not a requirement (see [F-35](../traceability/findings-closed.md#f-35)) |
| REQ-53 | removed | [REQ-20](pseudonymization.md#req-20), [REQ-21](pseudonymization.md#req-21) (and [F-30](../traceability/findings-closed.md#f-30), [F-37](../traceability/findings-closed.md#f-37)) |
| REQ-54 | merged into | [REQ-55](logging-audit.md#req-55) |
| REQ-56 | removed | [REQ-74](authorization.md#req-74) (partly) |
| REQ-70 | removed | — |
| REQ-73 | removed | [AV-01](admission.md#av-01) |
| REQ-96 | merged into | [REQ-91](asi.md#req-91) |
| REQ-98 | removed | [REQ-48](authorization.md#req-48), [REQ-74](authorization.md#req-74), [REQ-97](authorization.md#req-97), [REQ-79](pseudonymization.md#req-79), [REQ-17](authorization.md#req-17) |
| REQ-104 | removed | [REQ-88](asi.md#req-88) (a duty of the QTSP under ETSI and eIDAS) |
| REQ-105 | removed | [REQ-88](asi.md#req-88) (a duty of the QTSP under ETSI and eIDAS) |
