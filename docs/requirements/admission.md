# Admission and connection requirements

These requirements cover who can connect to a source. The first part holds requirements on the admission register and the contract decision. The second part holds candidate connection conditions for the parties that connect. For the design, see [Admission of parties](../building-blocks/gbo-basis/authorization.md#admission-of-parties).

This page has the following parts:

- [Admission register and contracts](#admission)
- [Connection conditions (candidates)](#connection-conditions)

## Admission register and contracts {#admission}

The admission requirements cover the step before a request. They answer
three questions: can this party connect, to which bronhouder, and who
decides that. The requirements are generic. They apply to every party that
connects through FSC: in DvTP, EUDI issuance, and the ASI route.
[Authorization](authorization.md) covers the authorization of one request.

Admission is a registration and is not a policy rule. An automatic "no"
stays reversible ([F-55](../traceability/findings-closed.md#f-55)). The contract
proposal that the PDP judges is thin. It tells who connects, but it does
not tell to what ([F-56](../traceability/findings-closed.md#f-56)). The
governance side (who runs the register, and which legal protection a
refused party has) is in [Q-22](../traceability/answered-questions.md#q-22).
The design decision is
[ADR 0015](../decisions/0015-contract-acceptance-by-policy.md).
### REQ-61: Admission comes from a register and not from decision policy {#req-61}

> The admission of a participant MUST come from a participant register
> that the PDP consults as an information source. Admission covers whether
> a party is allowed to connect, to which bronhouder, and whether that
> admission is active. If a party is not actively admitted there to the
> bronhouder, it MUST NOT get a new contract. It MUST be possible to add,
> suspend, extend, or withdraw an admission without a change of decision
> policy and without a restart of the PDP. The reference policy MAY
> co-sign only for grants that the admission decision covers. These grants
> are a service connection, or a delegated service connection with a
> registered representation ([REQ-106](consent.md#req-106)).

| Case | Outcome |
|---|---|
| Party actively admitted to this bronhouder | contract co-signed |
| Party not in the register | refused: `PARTY_NOT_IN_REGISTRY` |
| Party suspended | refused: `PARTY_NOT_ACTIVE` |
| Party admitted, but not to this bronhouder | refused: `SOURCE_NOT_ALLOWED` |
| Register gives no data | refused: `ADMISSION_REGISTER_UNAVAILABLE` |
| Proposal with another kind of grant, with both kinds at the same time, or without a grant | refused: `GRANT_TYPE_NOT_ALLOWED`. The proposal stays pending (code) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
          ("deelname vereist een voorafgaande toelatingsbeslissing", facility "deelnemersregister").
        - [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
          (the PDP consults the participant status, among other sources).
        - FR-30 criteria 1 and 2, and FR-16 criterion 2.
        - [P-16](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the admission register, its
      link to the PDP, and the reference policy for co-signing.
    - **Evidence**: [PR #239](https://github.com/ICTU/GBO-demo/pull/239),
      [PR #228](https://github.com/ICTU/GBO-demo/pull/228). Code and tests:
        - The
          [register](https://github.com/ICTU/GBO-demo/tree/v0.9.0/services/dvtp-onboarding-register)
          and the
          [PIP link](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/pip-pull/dvtp-onboarding.yaml#L1-L31).
        - The refusals are in
          [`autosign.rego#L166-L175`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L166-L175),
          tested in
          [`autosign_test.rego#L126-L141`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign_test.rego#L126-L141).
        - [PR #579](https://github.com/ICTU/GBO-demo/pull/579): the policy
          tells a missing register apart from an empty register in
          [`autosign.rego#L50-L52`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L50-L52),
          tested in
          [`autosign_test.rego#L86-L99`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign_test.rego#L86-L99).
    - **Related**: [REQ-62](#req-62), [REQ-106](consent.md#req-106),
      [REQ-110](#req-110), [F-55](../traceability/findings-closed.md#f-55),
      [Q-22](../traceability/answered-questions.md#q-22),
      [Q-68](../traceability/open-questions.md#q-68),
      [ADR 0015](../decisions/0015-contract-acceptance-by-policy.md).
    - **Notes**:
        - The register uses the FSC Peer ID as key. It is thin: name, active,
          admitted sources, and mandates.
        - The register has no accounts. Whoever can reach the management
          interface locally is administrator.
        - Production needs administrator authentication and a shielded or
          mTLS-protected pull endpoint. The form of the data does not change
          for that.
        - The register deactivates a participant and does not delete it.
        - The pull replaces entities but does not remove them. So a record that
          disappears leaves the old admission in place.

### REQ-62: The admission decision on a contract is its own rule set, separate from request policy {#req-62}

> A separate rule set MUST decide whether a contract proposal gets a
> co-signature. This rule set MUST stay apart from the policy that decides
> on single requests. The two MUST NOT share rules or deny reasons. They
> MAY read the same admission data from the register.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design.
      [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
      ("de inrichting behandelt technische identiteit en toelatingsstatus apart van de rol en bevoegdheid in een concrete interactie").
    - **Addressee**: GBO-delivered component: the reference policy.
    - **Evidence**: [PR #228](https://github.com/ICTU/GBO-demo/pull/228). The
      rule set is its own package without an import, in
      [`autosign.rego#L1-L10`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L1-L10).
      The request policy reads the same register for the mandate in
      [`engine.rego#L253-L267`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L253-L267)
      ([PR #464](https://github.com/ICTU/GBO-demo/pull/464)).
    - **Related**: [REQ-61](#req-61), [REQ-106](consent.md#req-106),
      [F-52](../traceability/findings.md#f-52),
      [F-55](../traceability/findings-closed.md#f-55),
      [F-56](../traceability/findings-closed.md#f-56),
      [ADR 0015](../decisions/0015-contract-acceptance-by-policy.md).
    - **Notes**:
        - Design choice: the contract decision runs as an AuthZEN evaluation
          through the same PDP as the requests
          ([`fsc-infra/docker-compose.yml#L701`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L701),
          [`#L773`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L773)).
          So both decisions are in the same decision log.
        - The FSC Manager selects the policy on
          `doelbinding = "auto_sign_contract"`. A renamed package switches the
          policy off without a signal, and every contract stays pending
          ([F-52](../traceability/findings.md#f-52)).
        - The proposal names no service and no direction of delegation. So the
          decision is about who connects. It does not cover what the party
          connects to ([F-56](../traceability/findings-closed.md#f-56)).

### REQ-63: An automated refusal of a contract proposal is recoverable {#req-63}

> An automated negative decision on a contract proposal MUST leave the
> proposal pending. A final refusal MUST be a separate, deliberate
> action. After a correction of the admission data, the submitting party
> MUST be able to submit again without an action of the other party. The new
> submission MUST get a new assessment.

| Case | Outcome |
|---|---|
| Policy refuses the proposal | the proposal stays pending, no co-signature |
| Admission corrected, proposal submitted again | new assessment, co-signed if allowed |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: derived. The requirement serves
      [P-16](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) and
      [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel).
      An automatic "no" that nobody can correct turns an error in the register
      into an exclusion.
    - **Addressee**: interface agreement: the observable behavior of the
      admission process.
    - **Evidence**: [PR #228](https://github.com/ICTU/GBO-demo/pull/228),
      tested by hand. The co-signature follows only on allow, in
      [`autosign.rego#L3-L5`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L3-L5).
      No automated test.
    - **Related**: [REQ-61](#req-61), [F-55](../traceability/findings-closed.md#f-55),
      [Q-22](../traceability/answered-questions.md#q-22),
      [ADR 0015](../decisions/0015-contract-acceptance-by-policy.md).
    - **Notes**: in the FSC Manager in use, this is product behavior. A
      refusal by the PDP leaves the proposal at *proposed*. A new submission
      is a new proposal with a new contract hash. So the requirement binds the
      configuration: do not configure an automatic refusal.
      [Q-22](../traceability/answered-questions.md#q-22) covers the procedural
      side (reasons, objection).

### REQ-110: A suspended or departed consumer gets no more data, even with a valid consent {#req-110}

> If a consumer is suspended or terminated, it MUST receive no more data
> within a set period, even with a valid consent. A suspension or
> termination MUST NOT change any consent. After a suspension ends, the
> existing consents MUST be usable again.

| Case | Outcome |
|---|---|
| Active consumer, valid consent | allowed |
| Consumer suspended | denied within the period, consent unchanged |
| Suspension ended | allowed again, without a new consent |
| Consumer terminated | denied |
| Consent expires during the suspension | expires as always |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design.
      [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
      ("schorsing of beëindiging leidt tijdig tot intrekking van de toegang"),
      made stricter: the consent does not change. Also FR-31 criterion 2 and
      FR-36 criterion 4.
    - **Addressee**: interface agreement between source and management
      organization: who closes the access, and how fast. The consent function
      does not need to do anything.
    - **Evidence**: not built. The demo issue follows after
      [Q-53](../traceability/open-questions.md#q-53). Partly built: a
      suspended party gets no new contract
      ([`autosign.rego#L172`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L172)).
      At a request, the policy checks only the status of an integrator
      ([`engine.rego#L263`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L263)).
      So a suspended consumer with an existing contract can still call the
      source.
    - **Related**: [REQ-61](#req-61), [REQ-106](consent.md#req-106),
      [REQ-123](#req-123), [Q-53](../traceability/open-questions.md#q-53).
    - **Notes**:
        - The requirement fixes the effect and leaves the mechanism open. A
          status check at every request meets it, and so does the withdrawal
          of the FSC contract. With the withdrawal, an issued access token
          stays valid until it expires. A new contract is then necessary after
          the suspension ends. The deny reason depends on the mechanism
          ([Q-53](../traceability/open-questions.md#q-53)).
        - In the demo, a status change in the register reaches the PDP within
          the pull interval of 5 s
          ([`dvtp-onboarding.yaml#L9`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/pip-pull/dvtp-onboarding.yaml#L9)).
        - A suspension or departure does not revoke the consents. The citizen
          sees them as Active while the party cannot use them.
        - A consumer with a new OIN is a new party. Old consents become
          unusable and do not move to the new party.
        - New consent requests of a suspended consumer belong to the check of
          the initiator
          ([ICTU/GBO-demo#427](https://github.com/ICTU/GBO-demo/issues/427)).

### REQ-123: Every change to an admission, mandate, or activation is traceable {#req-123}

> A GBO-delivered component that records who is allowed to take part, or
> what is in use, MUST record every change of that data. The record MUST
> hold who made the change, when it took effect, what changed, and the
> value before and after. This covers the admission register (admissions
> and mandates), the activation of sources in issuance, and the client
> registration of the ASI authorization server. A change MUST be possible
> only for an authenticated, authorized administrator, or for a check that
> the component runs itself. The component MUST protect the record in the
> same way as the audit records of [REQ-32](logging-audit.md#req-32).

| Case | Outcome |
|---|---|
| Administrator suspends a party | record: administrator, moment, active → suspended |
| Change without an authenticated, authorized administrator | refused, nothing changed |
| Client deactivated after a re-check ([REQ-89](asi.md#req-89)) | record with the re-check as actor |
| Source activated or rolled back ([REQ-65](sources-identity.md#req-65), [REQ-66](sources-identity.md#req-66)) | record with the version before and after |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
          ("iedere component legt de gebeurtenissen vast die voor zijn verantwoordelijkheid relevant zijn",
          "maatregelen beschermen loggegevens tegen ongeautoriseerde wijziging en verwijdering").
        - [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
          ("schorsing of beëindiging leidt tijdig tot intrekking van de toegang").
        - [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
          ("beheerrechten zijn beperkt, tijdelijk en aantoonbaar toegekend").
        - [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the admission register, the
      activation in the EUDI adapter, and the authorization server of the ASI.
    - **Evidence**: not built. The register has no accounts (notes of
      [REQ-61](#req-61)).
    - **Related**: [REQ-61](#req-61), [REQ-110](#req-110),
      [REQ-65](sources-identity.md#req-65), [REQ-66](sources-identity.md#req-66),
      [REQ-88](asi.md#req-88), [REQ-89](asi.md#req-89),
      [REQ-32](logging-audit.md#req-32),
      [Q-53](../traceability/open-questions.md#q-53),
      [Q-74](../traceability/open-questions.md#q-74).
    - **Notes**:
        - These records are data about organizations. They are no LDV
          processing of a data subject.
        - How the administrator authenticates is a choice of the
          configuration. The requirement asks only that a change can be
          attributed to an authorized person or to a check.
        - The component does not delete a record ([REQ-61](#req-61):
          deactivate, do not delete).
        - Without this record, nobody can test [REQ-110](#req-110) ("within a
          set period"), because nobody knows when a suspension took effect.

## Connection conditions (candidates) {#connection-conditions}

The demo asks participants for certain behavior to make the chain work.
The TO records these demands as candidate connection conditions (AV-NN).
They cover every channel: GBO Basis, DvTP, and EUDI. None of them is an
approved condition.

[PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
names "aansluitvoorwaarden per deelnemersgroep" as an agreement that is
still open. FR-30 lets the operator of the DvTP facility check selection
criteria and connection conditions. The framework falls under PSA open
decision [B-09](https://ictu.github.io/GBO-PSA/main/vraagstukken/#besluitregister).

### Why the items are candidates and not requirements

A connection condition puts an obligation on a party that is not GBO. The
management organization sets the condition. GBO does not. For that reason,
each item is a candidate, written as SHOULD. Each candidate has its basis
in the demo, the PSA, or the FR, as input for the decision. A candidate can
refer to a requirement (REQ) that enforces the same behavior on the GBO
side.

The connection conditions name three participant groups: private
consumer, integrator, and bronhouder. Each channel puts its candidates
on one of these groups:

| Channel | Obliged party | Candidates |
|---|---|---|
| All channels | bronhouder | [AV-07](#av-07) |
| DvTP | private consumer | [AV-01](#av-01), [AV-02](#av-02), [AV-03](#av-03), [AV-04](#av-04), [AV-05](#av-05), [AV-14](#av-14), [AV-15](#av-15) |
| DvTP | integrator | [AV-06](#av-06) |
| DvTP | bronhouder | [AV-09](#av-09) |
| EUDI | bronhouder | [AV-08](#av-08), [AV-10](#av-10), [AV-11](#av-11), [AV-12](#av-12), [AV-13](#av-13) |

### AV-01: Consumer sends trace context and records the transaction ID {#av-01}

> A private consumer SHOULD send W3C Trace Context with every call to a
> source, and SHOULD record the `Fsc-Transaction-Id`.

- **Status**: candidate, normative minimum according to S09

??? note "Source, evidence and notes"

    - **Obliged party**: private consumer
    - **Channel**: DvTP
    - **Source**: [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
      (a request identifier across the whole chain) and
      [Q-24](../traceability/answered-questions.md#q-24). This candidate replaces
      the removed REQ-73.
    - **Related**: [REQ-55](logging-audit.md#req-55)

### AV-02: Consumer records its processing according to LDV {#av-02}

> A private consumer SHOULD record its processing according to LDV, with
> `dpl.read.nextLogbookId` for each call to a source.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: private consumer
    - **Channel**: DvTP
    - **Source**: the LDV read extension (the chain starts at the application
      that started the processing),
      [F-68](../traceability/findings.md#f-68), and
      [Q-24](../traceability/answered-questions.md#q-24) option 3. The demo does
      this ([PR #366](https://github.com/ICTU/GBO-demo/pull/366)).
    - **Related**: [REQ-72](logging-audit.md#req-72),
      [REQ-75](consent.md#req-75)
    - **Notes**: LDV does not bind private parties itself. The chain-wide
      starting point can also come from the records of the register
      ([REQ-75](consent.md#req-75)).

### AV-03: Consumer uses the toestemmingsvoorziening and BSNk PP {#av-03}

> A private consumer that takes part in DvTP SHOULD use the central
> consent function and BSNk PP.

- **Status**: candidate, already in the GO

??? note "Source, evidence and notes"

    - **Obliged party**: private consumer
    - **Channel**: DvTP
    - **Source**: the table of facilities in the
      [GO](https://ictu.github.io/GBO-GO/main/) (section 5): "Een private dienstverlener die deelneemt, moet de toestemmingsvoorziening en BSNk PP gebruiken en aan de aansluitvoorwaarden voldoen."

### AV-04: Consumer has its own FSC peer with PKIoverheid certificate and OIN {#av-04}

> A private consumer SHOULD connect with its own FSC peer, with a
> PKIoverheid certificate, and SHOULD use the OIN as its legal identity.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: private consumer
    - **Channel**: DvTP
    - **Source**: FR-33 and FR-34 (v0.9), the
      [GO](https://ictu.github.io/GBO-GO/main/) (S04 building blocks
      PKIoverheid and OIN),
      [Q-06](../traceability/answered-questions.md#q-06), and
      [Q-07](../traceability/answered-questions.md#q-07).
    - **Related**: [REQ-67](sources-identity.md#req-67)
    - **Notes**: FR-33 (v0.9) allows an OIN or a KvK number. The link between
      identifiers is an open decision in S04.

### AV-05: Consumer sends the consent proof unchanged {#av-05}

> A private consumer SHOULD send the consent proof unchanged, including the
> identifier of the citizen as it is in the proof.

- **Status**: candidate, depends on the outcome of #377

??? note "Source, evidence and notes"

    - **Obliged party**: private consumer
    - **Channel**: DvTP
    - **Source**: [REQ-68](consent.md#req-68) (the policy binds the query
      subject to the proof). With a real BSNk, a PI is randomized. So only the
      exact value binds
      ([ICTU/GBO-demo#377](https://github.com/ICTU/GBO-demo/issues/377),
      consequence 1).
    - **Related**: [REQ-68](consent.md#req-68),
      [REQ-80](pseudonymization.md#req-80)
    - **Notes**: from demo increment
      [SL-51](../traceability/increments.md#sl-51) on, the proof carries an
      encrypted value for each source
      ([REQ-80](pseudonymization.md#req-80)). The query names the subject only
      with a placeholder.

### AV-06: Integrator is admitted separately and acts as processor {#av-06}

> An integrator SHOULD be admitted separately, with its own organization
> identity means. It SHOULD have a processing agreement with the
> dienstverlener, and SHOULD NOT store personal data persistently. It
> SHOULD have a registration for each dienstverlener and use case.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: integrator
    - **Channel**: DvTP
    - **Source**:
        - FR-18 and FR-37 (v0.9).
        - [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel)
          and [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie),
          [B-19](https://ictu.github.io/GBO-PSA/main/vraagstukken/#besluitregister).
        - [F-73](../traceability/findings-closed.md#f-73).
        - [ICTU/GBO-demo#379](https://github.com/ICTU/GBO-demo/issues/379).
    - **Related**: [REQ-106](consent.md#req-106) (the technical side: binding
      and mandate), [REQ-61](admission.md#req-61),
      [ADR 0034](../decisions/0034-integrator-delegation.md)

### AV-07: Bronhouder publishes a machine-readable description for each data service {#av-07}

> A bronhouder SHOULD publish a machine-readable and versionable
> description at the fixed location. It SHOULD publish one for each data
> service and for every data flow in which it offers that service. The
> description contains the schema and its version, a reference to the
> concept framework, the error messages, and the availability
> properties. It also contains quality properties and provenance
> information. It also holds the mappings that the bronhouder fixes for that flow, and the URL
> of the LDV read API of its logbook. Where possible, the description
> SHOULD refer to managed objects (the service in the catalog, the schema,
> the mapping) instead of repeating them.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: bronhouder
    - **Channel**: all channels
    - **Source**:
        - [PSA S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting)
          ("gepubliceerde informatie beschrijft schema's, versies, foutmeldingen en beschikbaarheidskenmerken").
        - [PSA S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus)
          ("verwijst naar een beheerd schema en begrippenkader",
          "machineleesbaar en versieerbaar",
          "kwaliteitskenmerken en herkomstinformatie",
          "verwijst waar mogelijk naar beheerde objecten").
        - [F-68](../traceability/findings.md#f-68).
    - **Related**: [REQ-64](sources-identity.md#req-64)
    - **Notes**: the candidate applies to every data flow: DvTP, EUDI
      issuance, ASI, and OOTS.

### AV-08: Bronhouder without its own endpoint provably agrees with a taken-over description {#av-08}

> A bronhouder that publishes no metadata endpoint of its own SHOULD
> provably agree with the service description that the operator keeps on
> its behalf.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: bronhouder
    - **Channel**: EUDI
    - **Source**: [F-71](../traceability/findings.md#f-71) and the exception
      in [REQ-64](sources-identity.md#req-64).
    - **Related**: [REQ-64](sources-identity.md#req-64)

### AV-09: Bronhouder keeps decryption keys of an older version while proofs for that version are valid {#av-09}

> A bronhouder SHOULD keep the keys with which it decrypts the values in a
> consent proof. It SHOULD keep a key version as long as valid proofs made
> with that key version exist.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: bronhouder
    - **Channel**: DvTP
    - **Source**: [REQ-82](pseudonymization.md#req-82) and
      [BSNK-08](pseudonymization.md#bsnk-08) (an encrypted value belongs to
      one key version).
    - **Related**: [REQ-82](pseudonymization.md#req-82),
      [F-78](../traceability/findings.md#f-78)

### AV-10: Bronhouder logs every living data subject of a relation attestation {#av-10}

> An attestation can hold data about someone other than the requester. For
> such an attestation, a bronhouder SHOULD record in its processing log
> every living data subject whose data it supplies. A record of the
> requester alone is not enough.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: bronhouder
    - **Channel**: EUDI
    - **Source**: [REQ-57](eudi-issuance.md#req-57) and
      [REQ-72](logging-audit.md#req-72).
    - **Related**: [REQ-57](eudi-issuance.md#req-57),
      [REQ-72](logging-audit.md#req-72)

### AV-11: Bronhouder tests its view for relation attestations {#av-11}

> A bronhouder can supply a relation (for example a marriage) through a
> view of its own. It SHOULD then prove with tests that this view returns
> only the relation of the identified citizen.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: bronhouder
    - **Channel**: EUDI
    - **Source**: [REQ-57](eudi-issuance.md#req-57).
    - **Related**: [REQ-57](eudi-issuance.md#req-57)

### AV-12: Bronhouder as provider has a public validity and revocation policy {#av-12}

> A bronhouder that has attestations issued SHOULD have a written and
> public policy for validity and revocation. It SHOULD publish the validity
> period for each attestation type in its configuration.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: bronhouder
    - **Channel**: EUDI
    - **Source**: Implementing Regulation (EU)
      [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj),
      article 4(1), [REQ-77](eudi-issuance.md#req-77), and
      [REQ-64](sources-identity.md#req-64).
    - **Related**: [REQ-77](eudi-issuance.md#req-77),
      [REQ-64](sources-identity.md#req-64)

### AV-13: Bronhouder gives the instruction to revoke an attestation {#av-13}

> If the data in an issued attestation is no longer correct, a bronhouder
> SHOULD tell the issuance function that the attestation must be revoked.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: bronhouder
    - **Channel**: EUDI
    - **Source**: Implementing Regulation (EU)
      [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj),
      article 4(2) and 4(3), and [REQ-77](eudi-issuance.md#req-77).
    - **Related**: [REQ-77](eudi-issuance.md#req-77),
      [F-82](../traceability/findings.md#f-82)
    - **Notes**: it is open who detects a change in the source:
      [Q-17](../traceability/open-questions.md#q-17).

### AV-14: Consumer has registered contact details for GDPR rights {#av-14}

> A private consumer SHOULD have contact details registered at its
> admission, where the citizen can exercise their GDPR rights. A consumer
> without those details SHOULD NOT be admitted.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: private consumer
    - **Channel**: DvTP
    - **Source**:
        - FR-25 criterion 2 (contact details "vastgelegd tijdens onboarding/configuratie").
        - [REQ-120](consent.md#req-120) (the portal shows them with
          every consent and after a revocation).
        - [Q-62](../traceability/open-questions.md#q-62) sub-question 2.
    - **Related**: [REQ-120](consent.md#req-120),
      [REQ-61](admission.md#req-61)

### AV-15: Consumer declares an equivalent alternative at admission {#av-15}

> At its admission, a private consumer SHOULD declare provably that it
> offers an equivalent alternative next to the digital consent route. It
> SHOULD also declare that a refusal of consent gives the citizen no
> disadvantage. It SHOULD describe that alternative so that the consent
> screen can name it.

- **Status**: candidate

??? note "Source, evidence and notes"

    - **Obliged party**: private consumer
    - **Channel**: DvTP
    - **Source**:
        - FR-36 criteria 1 and 2.
        - [PSA S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal)
          ("de inrichting biedt een gelijkwaardig alternatief als wetgeving of beleid dat vereist").
        - [REQ-117](consent.md#req-117) (the screen names the alternative).
        - [Q-62](../traceability/open-questions.md#q-62) sub-question 3.
    - **Related**: [REQ-117](consent.md#req-117)

