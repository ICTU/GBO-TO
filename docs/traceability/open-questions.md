# Open questions

An open question is a question that the demo cannot answer. It needs a
decision by the PSA, by a system forum (G5, Logius, the standards bodies),
or a legal assessment. Each entry names the forum, the options, and the
working assumption. The demo and this TO use the working assumption until
the forum decides the question. An architecture decision that waits for a
question has the status *proposed* in the [decision log](../decisions/index.md).

A question has one of four status values: *open*, *partly answered*,
*answered*, or *closed*. The register never reuses a question number. A
renumbered question keeps a history line with its old number.

### Q-01: Which pseudonym form does the system use? {#q-01}

- **Status**: partly answered

PSA P-04 asks that a consumer without a statutory power gets a citizen
identity that nobody can link outside its context. It is a legal question whether a private
consumer without a public task can connect to BSNk as a recipient. It is
also open whether an encrypted identity that the consumer cannot decrypt
counts as a processing of the BSN. The answer decides how the consumer
logs the citizen, gives access, and recognizes one citizen across
consents. The working assumption is that the consumer gets no pseudonym,
and the consent proof carries an encrypted value per source that each
source decrypts itself.

??? note "Options, working assumption and links"

    - **Forum**: PSA [B-07](https://ictu.github.io/GBO-PSA/main/vraagstukken/) (pseudonymous identity). Sub-question 1: Logius (BSNk management organization) and the Ministry of the Interior and Kingdom Relations (BZK). Sub-question 2: lawyer and BZK.
    - **Question**: PSA and GO set the direction of the form. PSA [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) says that a consumer without a statutory power gets "a party-specific identity or pseudonym" that cannot be linked outside its context. The [GO](https://ictu.github.io/GBO-GO/main/#toestemming-en-grondslag-als-afdwingbaar-autorisatiemechanisme) says the same for the private service provider (dienstverlener). Two sub-questions stay open:
        1. Is a private consumer without a public task allowed to connect to BSNk PP as a recipient? If so, on which legal basis (grondslag)?
        2. The consumer carries an encrypted identity for the source that the consumer cannot decrypt. Is that a processing of the BSN by the consumer?
    - **Answer so far**:
        - At BSNk, the recipient is the party (OIN). The service is not the recipient.
        - The consent proof carries an encrypted value per party. Each source decrypts its own value locally ([REQ-21](../requirements/pseudonymization.md#req-21), [REQ-80](../requirements/pseudonymization.md#req-80)).
        - The BSNk technical specifications v11.2 agree. The key belongs to the OIN and not to the FSC peer. Two peers with the same OIN share one encrypted value and one key.
        - A pseudonym per service needs a separate OIN ([BSNK-07](../requirements/pseudonymization.md#bsnk-07)).
    - **Why the demo cannot answer it**: Both sub-questions are legal questions under the BSN General Provisions Act (Wabb) and the GDPR. Technically, BSNk can do it. Every service provider with a PKIoverheid certificate gets keys for pseudonyms. BSNk also supports an OIN derived from a Chamber of Commerce (KvK) number (specification p. 23, p. 67). But the specification is written for service providers with a public task (p. 26). In the reading of the GBO team, a consumer without a public task falls outside it.
    - **Options**:
        - (a) No pseudonym for the consumer. The consumer then has no citizen identifier at all. This option affects three things:
            - the identifier that the consumer logs under ([Q-27](#q-27)),
            - the access of a citizen at the consumer,
            - the recognition of a citizen across consents ([F-76](findings.md#f-76)).
        - (b) An encrypted pseudonym (VP) from BSNk for the consumer. This option needs a yes on sub-question 1.
    - **Current working assumption**: The working assumption is option a:
        - The demo gives the consumer no pseudonym ([PR #469](https://github.com/ICTU/GBO-demo/pull/469)).
        - Since [PR #477](https://github.com/ICTU/GBO-demo/pull/477), the proof carries a VP for every source. For a source on the BSN Authorization List, it also carries an encrypted identity (VI). Thus sub-question 2 is already the practice of the demo.
        - [Issue #478](https://github.com/ICTU/GBO-demo/issues/478) tracks a pseudonym for the consumer. [Issue #377](https://github.com/ICTU/GBO-demo/issues/377) tracks a test against the real BSNk PP.
        - A point for the choice of form: with a pseudonym per recipient, the LDV `dataSubjectId` differs per controller (verantwoordelijke). Chain-wide citizen access can then search only by trace ID, from the own organization ([F-65](findings-closed.md#f-65)). This is a privacy property and not a defect.
    - **Related**: [F-65](findings-closed.md#f-65), [F-75](findings.md#f-75), [F-76](findings.md#f-76), [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-80](../requirements/pseudonymization.md#req-80), [BSNK-07](../requirements/pseudonymization.md#bsnk-07), [Q-26](#q-26) (recognition of the consent facility (toestemmingsvoorziening) at BSNk), [Q-27](#q-27), [ADR 0005](../decisions/0005-bsnk-pp.md), [ADR 0033](../decisions/0033-gateway-decrypts-after-allow.md).

### Q-08: What belongs in the LDV (processing log), and who holds the retention duty? {#q-08}

- **Status**: open

GBO builds and runs three components: the consent register (toestemmingsregister), the EUDI
adapter, and the issuance server. Each component records its own
processings in an LDV logbook, and the PDP records every decision in the
ADL. Nobody decided how
long these records stay, or who can read them. That is a legal and
supervision decision, and retention is harder because an ADL record
needs its sources to stay available. In the working assumption, the demo
keeps separate stores and a read-only role for the ADL, without a
retention policy or tamper evidence.

??? note "Options, working assumption and links"

    - **Forum**: management organization and privacy officer. PSA [S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid) ("agreements set retention, access, inspection and destruction explicitly"), [B-10](https://ictu.github.io/GBO-PSA/main/vraagstukken/).
    - **Question**: GBO builds and operates three components: the consent register, the eudi-adapter, and the issuance server. Which retention periods apply to the LDV and ADL records of these components? And who can read those records?
    - **Answer so far**:
        - The field schema is LDV plus ADL (PSA S09).
        - The ADL is the authoritative decision log ([PR #373](https://github.com/ICTU/GBO-demo/pull/373)). The policy version goes in `adl.core.policies` ([REQ-59](../requirements/logging-audit.md#req-59)).
        - Logius keeps three related logging standards with one trace ID: LDV, ADL, and FSC logging ([F-63](findings-closed.md#f-63)).
        - Each component records the events of its own responsibility, decentrally. This also applies on the wallet side (S09, B-10).
        - The citizen access model and central audit aggregation belong to B-10 and the open decisions of S09. This question does not cover them.
    - **Why the demo cannot answer it**: Retention periods and read access are a legal and supervision decision. Two points make retention harder:
        - The ADL source-reference model requires that a source stays available as long as a record that points to it exists.
        - LDV deliberately sets no access model for its read API. The access-control module of the API strategy is a candidate.
    - **Options**: None named. The management organization and the privacy officer give the periods and the access model as input.
    - **Current working assumption**:
        - The demo has separate stores and a SELECT-only reader role for the ADL.
        - The demo has no retention policy, no WORM storage, and no tamper evidence for ADL, LDV, or FSC transaction logs ([REQ-32](../requirements/logging-audit.md#req-32)).
        - The LDV field `processing_activity_id` needs a register of processing activities. In the demo, this register is a stand-in per logbook, without legal status. The real register is a dependency on the management organization ([REQ-72](../requirements/logging-audit.md#req-72)).
        - Since [PR #370](https://github.com/ICTU/GBO-demo/pull/370), the demo deviates on purpose from the S09 minimization norm ([REQ-60](../requirements/logging-audit.md#req-60)).
    - **Related**: [F-53](findings-closed.md#f-53), [F-54](findings.md#f-54), [F-63](findings-closed.md#f-63), [F-72](findings.md#f-72), [REQ-32](../requirements/logging-audit.md#req-32), [REQ-55](../requirements/logging-audit.md#req-55), [REQ-59](../requirements/logging-audit.md#req-59), [REQ-60](../requirements/logging-audit.md#req-60), [REQ-71](../requirements/logging-audit.md#req-71), [REQ-72](../requirements/logging-audit.md#req-72), [Q-25](#q-25), [Q-27](#q-27), [ADR 0026](../decisions/0026-ldv-integration.md), [ADR 0036](../decisions/0036-adl-decision-record.md).

### Q-13: Who sets the validity period of a consent? {#q-13}

- **Status**: open

The functional requirements give each service a default validity period
from the service catalog and let the citizen adjust it within bounds. It
is open whether the citizen really must be able to change the period,
and within which bounds. The choice is a policy and UX question under
the GDPR, which the demo can show but cannot decide. The demo deviates
from the requirements: the consumer sends the end date, and the citizen
cannot change the period. Without an end date, the consent register
uses one year.

??? note "Options, working assumption and links"

    - **Forum**: FR-DvTP owner, management organization (defaults and bounds in the service catalog), PSA [B-06](https://ictu.github.io/GBO-PSA/main/vraagstukken/) (consent in DvTP).
    - **Question**: Reopened on November 2, 2026.
        - FR-11 (FR-DvTP v0.9) says that the default period per service comes from the service catalog (FR-32). It also says that the citizen can adjust the period within the permitted bounds.
        - FR-05, criterion 5, says the same for the screen. Thus FR-05 and FR-11 agree.
        - It is open whether the citizen really must be able to adjust the period. The PSA capabilities only say that the portal shows the period to the citizen.

        Must the citizen be able to change the default validity period of a service? If so, within which bounds? The question which component enforces those bounds is [Q-62](#q-62), sub-question 1.

    - **Why the demo cannot answer it**: It is a policy and UX choice (GDPR art. 7). The demo can show each variant. It cannot decide which variant is lawful and wanted.
    - **Options**:
        - (a) A fixed default per service from the catalog. The citizen sees the period and does not change it.
        - (b) The citizen adjusts the period within bounds from the catalog, as the text of FR-11 says.
        - (c) The consumer sets the period in the request, within the catalog ceiling. No source names the consumer for this role. The demo does this in v0.9.0.
    - **Current working assumption**: No requirement says that the citizen adjusts the period ([REQ-19](../requirements/consent.md#req-19), [REQ-117](../requirements/consent.md#req-117), [register data model](../requirements/consent.md#consent-register)). The demo deviates from FR-11:
        - The consumer sends `valid_until` in the redirect context ([REQ-37](../requirements/consent.md#req-37)).
        - The portal turns this value into `validity_seconds` ([`PortaalConsent.tsx#L85`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L85)).
        - If there is no value, the register uses one year ([`consent-register/main.go#L51`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L51)).
        - The citizen cannot change the period.

        [Issue #380](https://github.com/ICTU/GBO-demo/issues/380) tracks the deviation. The issue also covers the adjust option that the demo removed earlier.

    - **Related**: FR-05, FR-11, FR-32, [F-11](findings-closed.md#f-11), [REQ-19](../requirements/consent.md#req-19), [REQ-37](../requirements/consent.md#req-37), [REQ-117](../requirements/consent.md#req-117), [Q-04](answered-questions.md#q-04), [Q-62](#q-62), [Q-76](#q-76) (per consent or per source).

### Q-14: Query enforcement model: how does the PDP model fields, recursion, and arguments? {#q-14}

- **Status**: open

The PSA speaks of pre-registered, selective data requests, and the GO
says that the service catalog holds the permitted requests per
application. The question is whether queries are fixed per application,
or whether a consumer can write its own queries within a schema that the
source publishes. The answer decides how rich the catalog gets and how
close GBO stays to iWlz (the data exchange of the Dutch Long-term Care Act). The working assumption rejects fixed queries
for DvTP, so the consumer writes its own query and the PDP decides every
field against an allowlist. If the field list is uncertain, the PDP
denies the request.

??? note "Options, working assumption and links"

    - **Forum**: PSA and GO authors, through [B-02](https://ictu.github.io/GBO-PSA/main/vraagstukken/) (API profile) and B-03 (service catalog). The technical enforcement model belongs in the GraphQL profile proposal for OpenFTV ([Q-16](answered-questions.md#q-16), [issue #331](https://github.com/ICTU/GBO-demo/issues/331)).
    - **Question**: [PSA S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting) says that the API supports "pre-registered, selective data requests". The GO says that the service catalog "contains the permitted data requests per application". Are the queries then fixed per application? Or is a different model sufficient, as follows:
        - The source publishes a (partial) schema per service.
        - The consumer writes its own queries within that schema.
        - The PDP validates each query against the schema (fields, nesting, arguments).
    - **Why the demo cannot answer it**: The demo can show each model. The meaning of S07 is for its authors to say. Three points are design and maintainability choices: which model applies per regime, how rich the catalog gets, and how close GBO stays to iWlz.
    - **Options**:
        - (A) The consumer picks one of a list of fixed query templates (iWlz, historically).
        - (B) The consumer writes its own query. The PDP parses it and checks each field against an allowlist (the demo).
        - (C) Schema directives say per field which policies run. A PEP preprocessor parses the query once and gives the PDP structured input (iWlz, present practice).
        - (D) The catalog fixes a maximum template or schema per scope. The query of the consumer must be a structural subset of it.
        - A middle form (findings review, September 21, 2026): the source publishes a (partial) schema with filter arguments. Per application, policy requires which paths are mandatory, and which filters with which fixed values. Policy does not look at content. The queries are then free, but the bounds for them are fixed. This form fits the GO and the iWlz network model. [Issue #425](https://github.com/ICTU/GBO-demo/issues/425) tests it for an attestation about another person ([REQ-57](../requirements/eudi-issuance.md#req-57)).
    - **Current working assumption**: The team does not want fixed queries for DvTP. The DvTP path uses model B. The PDP side builds the complete field list per the FTV GraphQL profile and decides every field separately. If the field list is uncertain, the PDP denies the request ([REQ-17](../requirements/authorization.md#req-17)). Since [SL-13](increments.md#sl-13), consent works at scope level, and that makes D a small next step. [SL-14](increments.md#sl-14) built a proof of concept for D.
    - **Related**: [REQ-17](../requirements/authorization.md#req-17), [REQ-57](../requirements/eudi-issuance.md#req-57), [F-74](findings.md#f-74), [Q-16](answered-questions.md#q-16), [SL-03a](increments.md#sl-03a), [SL-03b](increments.md#sl-03b), [ADR 0001](../decisions/0001-graphql-source-access.md), [ADR 0012](../decisions/0012-opa-graphql-parse.md).

### Q-17: EUDI issuance architecture: who owns the issuance server and the adapter? {#q-17}

- **Status**: open

GBO offers a central, optional facility that issues attestations for the
EUDI Wallet, and each bronhouder stays responsible for its
attestations. Can the facility hold the seal key of a bronhouder, or
must it call a signing facility under control of the bronhouder? It
is also open who holds the qualified seal certificate, which names the
authentic source, and the status-list certificate. Key custody and
certificate holding are legal and governance decisions. As a working
assumption, the demo uses one issuance server, a certificate set per
source, and keys in files, which decides nothing for production.

??? note "Options, working assumption and links"

    - **Forum**: BZK, the Dutch Authority for Digital Infrastructure (RDI), and bronhouders, with a legal review. PSA [B-13](https://ictu.github.io/GBO-PSA/main/vraagstukken/) and the open decisions of [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte), [issue #225](https://github.com/ICTU/GBO-demo/issues/225).
    - **Question**: The question became a key and seal question, with three parts:
        1. Can a central PuB-EAA facility hold and use the seal key material of a bronhouder? Or must sealing go through a signing facility that the bronhouder manages (remote signing, an HSM at the source)?
        2. Who holds the qualified seal certificate?
        3. Is the status-list certificate of the source or of the facility?
    - **Answer so far**:
        - The choice "one issuance server per bronhouder or one central server" is obsolete.
        - The [GO](https://ictu.github.io/GBO-GO/main/#uitgifte-van-attestaties-voor-de-eudi-wallet-pubeaa-uitgifte) gives GBO the technical role of a central, optional issuance facility: "GBO is not itself a PubEAA provider".
        - In PSA S11, the bronhouder stays legally and materially responsible.
        - The source publishes its own attestation schema and offer ([F-57](findings.md#f-57), [REQ-64](../requirements/sources-identity.md#req-64)).
        - Issuer and reader certificates are a set per source. If material is missing, issuance fails hard ([REQ-58](../requirements/eudi-issuance.md#req-58)).
        - Onboarding is [REQ-65](../requirements/sources-identity.md#req-65) and B-09.
        - The regime follows from the evidence and not from a flow field ([REQ-74](../requirements/authorization.md#req-74)).
    - **Why the demo cannot answer it**: Key custody and the holder of a qualified certificate are legal and governance decisions. The regulation makes them concrete:
        - Attestations: the seal on a PuB-EAA is created in a QSCD (ETSI TS 119 471, REQ-EAASP-7.5.3-02, through CIR 2026/1735). The seal uses a qualified certificate per ETSI TS 119 412-6 clause 8. That certificate names the authentic source and the legal basis (eIDAS art. 45f(1)(b)).
        - ASI results: from January 1, 2027, the public sector body or the designated intermediary seals them. It uses at least an advanced seal on a qualified seal certificate. A QSCD is not required there (CIR 2025/1569 art. 9(4), as amended by 2026/1735).
    - **Options**:
        - (a) The central facility holds the key of each bronhouder.
        - (b) Remote signing or an HSM under control of the bronhouder, which the facility calls.
    - **Current working assumption**: One issuance server with a certificate set per source. The demo keeps the keys in files at the facility. This choice decides nothing about production.
    - **Related**: [F-66](findings-closed.md#f-66), [F-80](findings.md#f-80), [F-81](findings.md#f-81), [REQ-58](../requirements/eudi-issuance.md#req-58), [Q-07](answered-questions.md#q-07), [Q-28](#q-28), [Q-32](#q-32), [Q-37](#q-37), [ADR 0028](../decisions/0028-pubeaa-productization.md), [ADR 0041](../decisions/0041-asi-seal-format.md).

### Q-18: EUDI flow security: phishing, certificate management, data processing in the adapter, PID verification {#q-18}

- **Status**: open

Can a bronhouder identify a citizen with a BSN from a verified EUDI
Wallet PID, with the legal status of a BSN from DigiD? If so, the chain
must show how the verified disclosure binds to the source query. This is
a national legal question, because eIDAS does not name the BSN and the
member state decides on the number. In the working assumption, the
issuance server verifies the PID but passes only plain attributes to the
adapter, without an authenticated callback. So nothing in the chain
binds the BSN of the source query to a verified PID.

??? note "Options, working assumption and links"

    - **Forum**: lawyer and BZK. PSA [B-08](https://ictu.github.io/GBO-PSA/main/vraagstukken/) (identity matching), [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte).
    - **Question**: The question is about a BSN from a verified PID disclosure (EUDI Wallet). Can a bronhouder use that BSN to identify the citizen in a source query, with the same legal status as a BSN from DigiD? If so, which binding between the verified disclosure and the query must the chain show ([issue #133](https://github.com/ICTU/GBO-demo/issues/133))?
    - **Answer so far**: The original question was split.
        - Presentation and combination of attestations by verifiers are outside GBO (GO pattern A).
        - The designation of the Dutch PID issuer is an external dependency.
        - The issuance server verifies the PID signature.
        - The security basis for the build covers phishing, certificate rotation and compromise, and trust-list use. It also covers data processing and logging in the adapter, state, and data freshness. See [REQ-77](../requirements/eudi-issuance.md#req-77) and the checklist in [issue #381](https://github.com/ICTU/GBO-demo/issues/381).
    - **Why the demo cannot answer it**: It is a national legal question.
        - eIDAS does not name the BSN. It requires that the PID "uniquely represents" the person (art. 5a(5)(f)). It forbids use that can be "tracked, linked or correlated" (art. 5a(16)(a)).
        - `personal_administrative_number` stays optional. The member state sets its policy in its eID scheme (CIR 2024/2977). CIR 2026/1731 did not change this.
        - Without a number, identity matching per CIR 2025/846 applies.
    - **Options**: For the legal part, the answer is yes or no. For the binding ([REQ-45](../requirements/eudi-issuance.md#req-45)), there are two options:
        - (a) The issuance server authenticates its callback to the adapter (mTLS or a signed request).
        - (b) The adapter verifies the SD-JWT disclosure itself.

        In both cases, the disclosure is bound to the request, and the PID trust list holds PID issuers only.

    - **Current working assumption**: The issuance server verifies the wallet presentation, but gives the adapter only plain attributes. The adapter does not authenticate that callback. Nothing in the chain binds the BSN of the source query to a verified PID disclosure. If a request carries no consent proof, it gets the PID regime ([REQ-74](../requirements/authorization.md#req-74), [F-70](findings.md#f-70)). [SL-25](increments.md#sl-25) (PID verification in the adapter) is a dropped demo increment.
    - **Related**: [F-70](findings.md#f-70), [REQ-45](../requirements/eudi-issuance.md#req-45), [REQ-74](../requirements/authorization.md#req-74), [REQ-77](../requirements/eudi-issuance.md#req-77), [Q-15](answered-questions.md#q-15), [Q-36](#q-36) (PID without BSN), [ADR 0018](../decisions/0018-eudi-disclosure-issuance.md), [ADR 0031](../decisions/0031-regime-from-evidence.md).

### Q-25: How can a reader find the step from the decision at the source to the consent log? {#q-25}

- **Status**: open

If the PDP of a source checks a consent status, the consent register
logs that check in its own LDV logbook. The PDP writes only an ADL
decision record, and the ADL has no field that points to another LDV
logbook. A reader who follows the standard links therefore cannot get
from the decision to the consent log. The question is how the ADL record
can point there, and the answer needs Logius or a design choice. The
working assumption accepts the gap: an auditor finds the register record
by a search on the trace ID.

??? note "Options, working assumption and links"

    - **Forum**: Logius (maintainers of ADL and LDV), [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid).
    - **Question**: The status check is a processing of the consent register. The register records it in its logbook under the trace of the request.
        - The caller is the PDP of the source. The PDP writes an ADL record and no LDV record ([F-63](findings-closed.md#f-63)).
        - Thus no LDV record at the source points to the consent logbook with `nextLogbookId`. The ADL has no equivalent. A reader who follows the standard route does not get to the consent logbook ([F-68](findings.md#f-68), point 2).
        - ADL 1.0.0 gives `adl.core.information` a reference per information source (PIP). That reference must be "sufficient to retrieve, on demand, the data … that affected the authorization decision".
        - That field is for rebuilding the input of the decision, in a free format. It does not mention LDV or `nextLogbookId`.
        - If a GBO profile uses the field as a pointer to an LDV logbook, that meaning is a GBO invention. Thus it does not close the gap.

        A PDP calls a PIP (the consent register). The register records that call itself as an LDV processing. How does the ADL record point to that LDV logbook, so that an LDV reader can follow the chain across the decision step? Is `adl.core.information` meant for this, or does a separate link field belong here, like `dpl.read.nextLogbookId`?

    - **Why the demo cannot answer it**: Option 1 adds a component that the design does not have. Option 2 changes the family of standards. Option 3 is a choice not to act. All three are design decisions. Option 2 needs Logius.
    - **Options**:
        - (1) Record the status query as a processing of the source, through a PIP adapter at the source. That adapter writes LDV with `nextLogbookId`. This option closes the gap with the means of the standard. It costs a component and a hop.
        - (2) Ask Logius how an ADL record points to the logbook of a PIP source.
        - (3) Accept the gap and document it. An auditor finds the status record through a search of the consent logbook by trace ID.
    - **Current working assumption**: Option 3. The record of the register is found by trace ID ([PR #371](https://github.com/ICTU/GBO-demo/pull/371)), with a verified caller ([issue #383](https://github.com/ICTU/GBO-demo/issues/383)). The demo log viewer shows the consent logbook as "reached without pointer".
    - **Related**: [F-63](findings-closed.md#f-63), [F-68](findings.md#f-68), [REQ-72](../requirements/logging-audit.md#req-72), [REQ-76](../requirements/consent.md#req-76), [Q-08](#q-08), [Q-23](answered-questions.md#q-23), [ADR 0026](../decisions/0026-ldv-integration.md), [ADR 0036](../decisions/0036-adl-decision-record.md).

### Q-26: Can the consent facility become a recognized BSNk party, and in which role? {#q-26}

- **Status**: open

In the design, the consent facility fetches an encrypted identity or
pseudonym per party from BSNk. BSNk serves only recognized parties, such
as means issuers and authorization services, and a consent facility is
none of these. The minister of BZK decides on recognition and its role.
Several practical points are open too, such as how the service
recognizes a citizen at a later login and how it gets the
Autorisatielijst BSN. The working assumption is that MijnOverheid passes
the BSN, and the service derives its own pseudonym under which it stores
the encrypted values.

??? note "Options, working assumption and links"

    - **Forum**: BZK and Logius (BSNk management organization). Also MijnOverheid for sub-questions 2, 3 and 5, and RvIG for sub-question 8. PSA [B-07](https://ictu.github.io/GBO-PSA/main/vraagstukken/), [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie).
    - **Question**: In the design of [issue #364](https://github.com/ICTU/GBO-demo/issues/364) the consent facility fetches an encrypted identity or an encrypted pseudonym per party from BSNk. Which part of the consent facility is the BSNk participant (register, portal backend, or both as one) is [Q-49](#q-49). Sub-questions:
        1. In which role can a consent facility be recognized: means issuer, authorization service (Machtigingsdienst), or a new role?
        2. Can the service be exempted from the check data at activation, because the citizen is already identified with DigiD at MijnOverheid ([BSNK-02](../requirements/pseudonymization.md#bsnk-02))?
        3. Does the login at MijnOverheid count as authentication by the service, as the specification requires before a transformation ([BSNK-04](../requirements/pseudonymization.md#bsnk-04))?
        4. How does the service appear in the overview of login means that the citizen sees in MijnOverheid ([BSNK-10](../requirements/pseudonymization.md#bsnk-10))?
        5. How does the service recognize the citizen at a later login? Can MijnOverheid pass an encrypted pseudonym for the service at login, as for the BSNk inspection register (Inzageregister)? Or can it pass a fixed reference of its own? If MijnOverheid passes the BSN itself, the service needs nothing else from MijnOverheid. The question then becomes whether MijnOverheid can legally pass the BSN.
        6. How does BSNk handle repeated activation for the same citizen? Does a stored PI stay usable when the service gets new keys?
        7. Who requests the keys at BSNk for sources and consumers? They do not talk to BSNk themselves ([BSNK-09](../requirements/pseudonymization.md#bsnk-09)). Can the service also become Key Requester, and which requirements apply?
        8. What does the BSN Authorization List look like in practice ([BSNK-06](../requirements/pseudonymization.md#bsnk-06))?
            - Known: RvIG manages the list. Logius publishes it per OIN as the Technical List BSN. The service must process it periodically and automatically. The service must not use it after its validity.
            - Not known: how Logius delivers it (file or service, signed or not, format). Also not known: how long an edition is valid and where that is stated. Further open points are how the service gets access, and how a source gets on the list (request to RvIG, lead time).
    - **Why the demo cannot answer it**:
        - Recognition is a decision of the minister of BZK (specification p. 24).
        - BSNk allows activation and transformation only to recognized parties: means issuer, authentication service, authorization service, or the eIDAS message service ([BSNK-01](../requirements/pseudonymization.md#bsnk-01)). A consent facility is none of these.
        - The specification names future roles, among them attribute services, without detail (p. 34).
        - The login cannot deliver the values. The citizen logs in at MijnOverheid, and the sources are known only at consent ([F-75](findings.md#f-75)).
        - The demo can show the behavior with a mock. It cannot decide the role or its conditions.
    - **Options**:
        - For sub-question 1: means issuer, authorization service, or a new role.
        - For sub-question 5, there are three options. The first is an encrypted pseudonym from MijnOverheid. The second is a fixed reference from MijnOverheid. The third is the BSN from MijnOverheid, with a pseudonym that the service derives itself (route D).
    - **Current working assumption**: Since October 5, 2026, MijnOverheid passes the BSN. The service derives its own pseudonym and stores PI and PP under it (route D, [ADR 0040](../decisions/0040-route-d-citizen-recognition.md), proposed, [BSNk preconditions](../requirements/pseudonymization.md#bsnk-preconditions)). The demo uses a BSNk mock. It reads the BSN Authorization List at the mock and uses a copy for at most one hour. The form and the period are assumptions ([PR #477](https://github.com/ICTU/GBO-demo/pull/477)).
    - **Related**: PSA [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), GO (central consent facility, BSNk PP mandatory for DvTP), [F-75](findings.md#f-75), [BSNK-01](../requirements/pseudonymization.md#bsnk-01), [BSNK-02](../requirements/pseudonymization.md#bsnk-02), [BSNK-04](../requirements/pseudonymization.md#bsnk-04), [BSNK-06](../requirements/pseudonymization.md#bsnk-06), [BSNK-09](../requirements/pseudonymization.md#bsnk-09), [BSNK-10](../requirements/pseudonymization.md#bsnk-10), [Q-01](#q-01), [Q-49](#q-49), [Q-50](#q-50), [ADR 0005](../decisions/0005-bsnk-pp.md), [ADR 0040](../decisions/0040-route-d-citizen-recognition.md).

### Q-27: Under what does a consumer without an identifier name the data subject in its processing log? {#q-27}

- **Status**: open

The consent proof carries the citizen only in values that sources can
read, so the consumer has no identifier for its LDV processing log. It
is open whether LDV accepts a reference to the legal basis as the data
subject. It is also open whether citizen access through the consents
meets the GDPR. In the working assumption, the consumer logs under the
consent ID. That ID is no pseudonym, so one citizen with two consents
shows as two data subjects.

??? note "Options, working assumption and links"

    - **Forum**: Sub-question 1: Logius and the LDV working group. Sub-question 2: lawyer or DPO. Variant 2 depends on [Q-01](#q-01). [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid).
    - **Question**: Since [SL-51](increments.md#sl-51) ([PR #469](https://github.com/ICTU/GBO-demo/pull/469)), the consent proof carries the citizen only in values that the sources can read. The consumer has no BSN, no PI, and no pseudonym. If the consumer logs its source calls per LDV ([AV-02](../requirements/admission.md#av-02)), `dpl.core.data_subject_id` must contain something. Two sub-questions follow:
        1. If the controller has no identifier of the data subject, can `dpl.core.data_subject_id` be a reference to the legal basis?
        2. Is it sufficient for the right of access that the citizen finds his processings at the consumer through his consents?
    - **Why the demo cannot answer it**:
        - Whether a reference to the legal basis is a valid `data_subject_id` is an interpretation of the LDV standard.
        - Whether access through the consent register is sufficient is a GDPR question.
        - Nobody checked whether the standard allows a record without a pseudonym of its own.
    - **Options**:
        - (1) The reference to the legal basis. The consumer holds no extra data. Citizen access goes through the consent register, which knows whose consents they are.
        - (2) A pseudonym for the consumer (a VP from BSNk). The consumer then logs under a pseudonym from its own space, as [REQ-72](../requirements/logging-audit.md#req-72) asks. It also recognizes the citizen across consents. This option needs a yes on [Q-01](#q-01) sub-question 1. The build is in [issue #478](https://github.com/ICTU/GBO-demo/issues/478).
        - (3) The own customer reference of the consumer, which it knows from its own process outside GBO. GBO cannot enforce or check it.
    - **Current working assumption**: Option 1. The demo consumer puts the consent ID in the field, with its own `data_subject_id_type` `consent-id` ([`logbook.go#L22`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/logbook/logbook.go#L22)). The consent ID is not a pseudonym. One citizen with two consents shows as two data subjects ([F-76](findings.md#f-76)).
    - **Related**: PSA [P-03, P-04, P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), FR-31, [F-68](findings.md#f-68), [F-76](findings.md#f-76), [REQ-72](../requirements/logging-audit.md#req-72), [AV-01](../requirements/admission.md#av-01), [AV-02](../requirements/admission.md#av-02), [Q-01](#q-01), [Q-08](#q-08), [Q-24](answered-questions.md#q-24), [ADR 0026](../decisions/0026-ldv-integration.md).

### Q-28: Who designates the PuB-EAA issuer and the ASI intermediary of the Netherlands, and who supervises? {#q-28}

- **Status**: open

A bronhouder can issue a PuB-EAA itself, or a public body that the
member state designates issues it on behalf of bronhouders. For
verification of attributes by QTSPs, the law also names a designated
intermediary. The question is whether the Netherlands designates GBO or
the management organization for one or both roles, and who supervises
PuB-EAA issuance. In the working assumption, the bronhouder is the
PuB-EAA provider and GBO runs the technical issuance facility. For
verification, the demo acts as the designated intermediary, but nobody
designated it.

??? note "Options, working assumption and links"

    - **Forum**: BZK (system responsibility), RDI (supervision of trust services). PSA [B-13, B-14](https://ictu.github.io/GBO-PSA/main/vraagstukken/), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte).
    - **Question**: The legal acts give the following background:
        - The bronhouder itself can issue a PuB-EAA. "A public sector body that is designated by the Member State" can also issue it on behalf of bronhouders (art. 3(46)).
        - For verification by QTSPs, Annex VI names "designated intermediaries recognized at national level".
        - CIR 2025/1569 art. 9(4), as amended by 2026/1735, lets "the designated intermediary recognized at national level" seal the result.
        - The member state notifies a PuB-EAA issuer with a conformity assessment report (art. 45f(3)).
        - The acts that the GBO team read do not name a supervisor of PuB-EAA issuers.

        Two sub-questions follow:

        1. Does the Netherlands designate GBO, or the management organization, as PuB-EAA issuer on behalf of bronhouders (eIDAS art. 3(46))? And as the nationally recognized intermediary for verification (eIDAS Annex VI, CIR 2025/1569 art. 9)?
        2. Which body supervises PuB-EAA issuance?

    - **Why the demo cannot answer it**: Designation and supervision are administrative decisions.
    - **Options**:
        - (a) GBO or the management organization gets a designation for both roles.
        - (b) GBO or the management organization gets a designation only for verification.
        - (c) No designation. Each bronhouder issues and verifies itself, and GBO supplies the technology.
    - **Current working assumption**: The bronhouder is the PuB-EAA provider, and GBO runs the technical issuance facility ([ADR 0028](../decisions/0028-pubeaa-productization.md)). For the ASI the demo acts as a designated intermediary ([Q-37](#q-37)). Neither is designated.
    - **Related**: [F-80](findings.md#f-80), [F-81](findings.md#f-81), [Q-17](#q-17), [Q-30](#q-30), [Q-31](#q-31), [Q-37](#q-37), [ADR 0028](../decisions/0028-pubeaa-productization.md), [ADR 0037](../decisions/0037-asi-oauth-front-door.md).

### Q-29: Is there a legal basis to verify attributes for private QTSPs, and does the ASI return the value on a match? {#q-29}

- **Status**: open

eIDAS lets a QTSP verify attributes at a source in accordance with Union
or national law, so the regulation creates no legal basis itself. From
January 1, 2027, the ASI can return the stored value on a match with
variation, which is more than a yes or no. An ETSI requirement makes
that value mandatory for fuzzy matching, which contradicts the optional
rule. It is open which Dutch legal basis applies, and whether the GBO
ASI does fuzzy matching and returns the value. In the working
assumption, the demo reports a match with variation but never returns
the stored value.

??? note "Options, working assumption and links"

    - **Forum**: A lawyer or DPO, and BZK. PSA [B-14](https://ictu.github.io/GBO-PSA/main/vraagstukken/), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte).
    - **Question**: Verification happens "at the request of the user, in accordance with Union or national law" (eIDAS art. 45e(1)). So the regulation does not create a legal basis itself. The UBO architecture states that no policy initiative is known for attribute verification by QTSPs.

        From January 1, 2027, CIR 2026/1735 lets the ASI return the value on `Match` or `MatchWithVariation`. With `MatchWithVariation`, the value is "the value of the attribute as stored in the authentic source". This return is optional, and it gives more than a yes or no answer. On `Match`, the source value gives no new information, because it equals the value of the QTSP. So sub-question 2 is about `MatchWithVariation`.

        Annex IV makes the value optional. But REQ-ASIP-6.1.1.1-10-01 still requires the value from an ASIP that supports fuzzy matching ([F-92](findings.md#f-92), [E2](standards-feedback.md#e2)). Three sub-questions are open:

        1. Which Dutch legal basis covers the verification of attributes from government sources for private QTSPs?
        2. Does the GBO ASI also return the value on a match, or only the result?
        3. Does the GBO ASI do fuzzy matching? If so, does it return the stored value with `MatchWithVariation`?

    - **Why the demo cannot answer it**: The legal basis and data minimization are legal trade-offs.
    - **Options**:
        - (a) Only the result, without `MatchWithVariation`.
        - (b) Only the result, with `MatchWithVariation`, and a report of the contradiction to ETSI and the Commission.
        - (c) The stored value with `MatchWithVariation`.
    - **Current working assumption**: Option b. The report to ETSI and the Commission is not sent. The demo ASIP gives `MatchWithVariation` and never returns the stored value ([`verification/service.go#L127-L128`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/service.go#L127-L128)). [REQ-85](../requirements/asi.md#req-85) stays draft until this question is decided.
    - **Related**: [F-80](findings.md#f-80), [F-92](findings.md#f-92), [REQ-85](../requirements/asi.md#req-85), [REQ-113](../requirements/asi.md#req-113), [E2](standards-feedback.md#e2), [Q-18](#q-18), [Q-36](#q-36), [Q-70](#q-70), [ADR 0037](../decisions/0037-asi-oauth-front-door.md).

### Q-30: On which trust list are PuB-EAA issuers: LoTE or the trusted lists? {#q-30}

- **Status**: open

Wallets and relying parties check the seal of a GBO attestation against
a trust list, and that list also goes into the attestation schema. The
EUDI specifications disagree on which list holds PuB-EAA issuers: a List
of Trusted Entities or the trusted lists. It is also open who manages
that list for the Netherlands. No decision exists, so a TO page that
names one list describes an assumption.

??? note "Options, working assumption and links"

    - **Forum**: BZK, through the EUDI cooperation group, and the operator of the Dutch trusted list. PSA [B-13](https://ictu.github.io/GBO-PSA/main/vraagstukken/), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte).
    - **Question**: EUDI technical specification TS2 lets the member state publish providers in LoTEs per ETSI TS 119 602. TS11 names "Lists of Trusted Lists" per ETSI TS 119 612 for PuB-EAAs. The ARF speaks of the PuB-EAA LoTE (§6.3.2).

        Wallets and relying parties validate the seal of a GBO attestation against this list. The list also sets the value in `trustedAuthorities` of the attestation schema.

        Is a PuB-EAA issuer published in a List of Trusted Entities (LoTE, ETSI TS 119 602) or in the trusted lists (ETSI TS 119 612)? Who manages that list for the Netherlands?

    - **Why the demo cannot answer it**: The specifications contradict each other.
    - **Options**:
        - (a) A LoTE per ETSI TS 119 602.
        - (b) The trusted lists per ETSI TS 119 612.
    - **Current working assumption**: There is no decision on the list. If a TO page names one list as fact, that page describes an assumption.
    - **Related**: [F-81](findings.md#f-81), [Q-28](#q-28), [ADR 0023](../decisions/0023-identity-convergence.md), [ADR 0028](../decisions/0028-pubeaa-productization.md).

### Q-31: Who registers the Dutch verification points in the catalogue of attributes? {#q-31}

- **Status**: open

The member state asks the EU to include its verification points in the
catalogue of attributes, which tells a QTSP how to use them. Each record
can carry a national code that tells Dutch sources apart if more than
one source delivers the same attribute. The question is who registers
the Dutch attributes and verification points, and who sets that national
coding scheme. Both are assignments that BZK makes. In the working
assumption, the demo has a local discovery stub and registers nothing in
the EU catalogue.

??? note "Options, working assumption and links"

    - **Forum**: BZK and the Dutch OOTS coordination. PSA [B-14](https://ictu.github.io/GBO-PSA/main/vraagstukken/), [S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte).
    - **Question**: Under CIR 2025/1569 art. 7(3) and 7(5), the member state asks for inclusion of the Annex VI attributes that rest on a public source. The request also describes how a QTSP uses the verification point.

        Per TS11, every attribute record has a `DataService` per source. A `DataService` holds the country, an optional `nationalSubID`, and the endpoint. The member state sets the coding scheme of `nationalSubID`. The catalogue runs on the SDG/OOTS infrastructure. TS11 has no management API for the catalogue. Two sub-questions are open:

        1. Who registers the attributes and verification points for the Netherlands?
        2. Who sets the coding scheme for `nationalSubID`? If more than one Dutch source delivers the same attribute, this scheme is necessary.

    - **Why the demo cannot answer it**: Registration and the national coding scheme are administrative choices. The route goes through OOTS, and OOTS is outside the scope of the demo.
    - **Options**: None named. Both answers are assignments that BZK makes.
    - **Current working assumption**: The demo has a local discovery stub with a record per attribute and data service ([REQ-99](../requirements/asi.md#req-99)). It registers nothing in the EU catalogue.
    - **Related**: [F-80](findings.md#f-80), [REQ-99](../requirements/asi.md#req-99), [Q-28](#q-28), [Q-67](#q-67) (Discover Interface).

### Q-32: In which format does an ASIP seal the verification result, so a QTSP can validate every ASIP the same way? {#q-32}

- **Status**: open

From January 1, 2027, every ASI verification result carries a seal, but
no rule fixes its format. A QTSP that verifies in several member states
must then implement the format of each ASIP separately. The question is
whether ETSI or an implementing act will fix a seal profile, or else
whether the Netherlands fixes one format for its ASIPs. In the working
assumption, the demo seals the response body with a detached JWS in a
header. That format is a demo choice, and the reference QTSP had to
implement it.

??? note "Options, working assumption and links"

    - **Forum**: For sub-question 1: ETSI ESI, and BZK through the EUDI cooperation group. For sub-question 2: BZK and the management organization.
    - **Question**: From January 1, 2027, the public sector body or the designated intermediary signs or seals every verification result (CIR 2025/1569 art. 9(4), as amended by 2026/1735). The signature or seal is at least advanced and rests on a qualified certificate. Recital 2 of 2026/1735 says that it "introduces the requirements for the signing and sealing of verification results". But these requirements only say who seals and at which level.

        Annex IV points to ETSI TS 119 478 clause 6.1.1, clause 6.2.3, or both, with changes on `attributeValue`. Annex IV says nothing about the seal. Clauses 6.1.1 and 6.1.2, and the OpenAPI of annex B, define no signature on the response.

        These points are fixed: that a seal is made, who makes it, at which level, and how to validate the certificate through the trusted lists. These points are open: the format (JAdES, CAdES, XAdES, or a plain JWS), the place (header, body, or envelope), and what exactly is signed.

        A QTSP that verifies at ASIPs in more than one member state must find and implement the format of each ASIP. An ASIP can describe its format in the OpenAPI that `endpointDescription` points to (REQ-DIP-5.3.3-03-02-01). But that OpenAPI is only documentation and is not an agreement. Two sub-questions are open:

        1. Will a next version of ETSI TS 119 478, or an implementing act, give a seal profile for the verification result?
        2. If not, does the Netherlands fix one format for its ASIPs? An example is JAdES baseline (ETSI TS 119 182-1) over the response body.

    - **Why the demo cannot answer it**: The format must apply to all ASIPs. That needs an agreement in ETSI, at EU level, or at national level. The demo can only make a proposal.
    - **Options**:
        - (a) A profile in ETSI TS 119 478.
        - (b) An implementing act.
        - (c) One national format, for example JAdES baseline.
        - (d) Each ASIP describes its own format in its OpenAPI.
    - **Current working assumption**: The demo ASIP seals the exact response body with a detached JWS in the header `X-JWS-Signature` (ES256, chain in `x5c`). This JWS is an addition to the ETSI OpenAPI ([PR #499](https://github.com/ICTU/GBO-demo/pull/499), [`handler.go#L414`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/handler.go#L414)). The format is a choice of the demo itself and is not JAdES. The reference QTSP had to implement this format. It accepts only a result with a valid seal ([PR #535](https://github.com/ICTU/GBO-demo/pull/535)). [ADR 0041](../decisions/0041-asi-seal-format.md) stays proposed until this question is decided.
    - **Related**: [REQ-83](../requirements/asi.md#req-83), [F-80](findings.md#f-80), [E4](standards-feedback.md#e4), [Q-17](#q-17) (who holds the seal certificate), [Q-28](#q-28), [Q-37](#q-37), [Q-39](#q-39) (same pattern), [Q-75](#q-75), [ADR 0041](../decisions/0041-asi-seal-format.md).

### Q-33: Does the Netherlands impose per-attribute authorization for ASI requests under art. 9(5)? {#q-33}

- **Status**: open

Under the ETSI standard, a QTSP gets a token per operation, and that
token is valid for every attribute while it lasts. The implementing
regulation lets a member state add controls, such as a binding of the
token to the attributes that the citizen came for. Such a binding limits
what a QTSP can request, but a QTSP that implements only ETSI fails on
it. The question is whether the Netherlands imposes this authorization
per attribute. In the working assumption, the binding is optional on
request of the QTSP, and a setting in the demo makes it mandatory.

??? note "Options, working assumption and links"

    - **Forum**: BZK, and a lawyer or DPO.
    - **Question**: ETSI TS 119 478 authorizes an ASI request per operation, with the scopes `verify` and `retrieve` (clause 6.1.3.2, figure 2). The QTSP puts the attributes to verify in the body of the request ("shall set out the attributes", art. 9(3)). The token does not hold them. So a token with scope `verify` is valid for every attribute while the token is valid.

        Art. 9(5) lets a member state impose "control mechanisms on the use of the verification methods", if the member state publishes them. The article adds: "taking into account … whether the authentic sources contain personal confidential or sensitive data".

        A binding of the token to the attributes that the user came for is such a mechanism. RFC 9396 `authorization_details` is one way to make this binding. The binding limits what a QTSP can request with one authorization, mainly on `/retrieve`. But the binding makes a Dutch ASIP stricter than ETSI. A QTSP that implements only ETSI fails on it.

        Does the Netherlands impose an authorization per attribute under CIR 2025/1569 art. 9(5)? Or is the authorization per operation of ETSI TS 119 478 sufficient?

    - **Why the demo cannot answer it**: Whether the Netherlands imposes a control beyond ETSI is a policy choice under art. 9(5).
    - **Options**:
        - (a) Per operation, as in ETSI.
        - (b) Per attribute, mandatory.
        - (c) Per attribute on request of the QTSP, with a setting that makes it mandatory.
    - **Current working assumption**: Option c. By default, the demo authorizes per operation. If the QTSP sends `authorization_details`, the token carries the attributes that the citizen saw on the consent screen. The ASIP then refuses other attributes ([REQ-103](../requirements/asi.md#req-103), [PR #559](https://github.com/ICTU/GBO-demo/pull/559)).

        [PR #572](https://github.com/ICTU/GBO-demo/pull/572) made the binding optional. The setting `AZSP_REQUIRE_AUTHORIZATION_DETAILS=true` makes it mandatory ([`main.go#L109`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/main.go#L109)). If a token does not cover the requested operation, the request gets 401 with `insufficient_scope`. The binding is an extension of ETSI with its own type ([F-95](findings.md#f-95)). [ADR 0042](../decisions/0042-asi-attribute-token-binding.md) stays proposed until this question is decided.

    - **Related**: [F-80](findings.md#f-80), [F-95](findings.md#f-95), [REQ-103](../requirements/asi.md#req-103), [E5](standards-feedback.md#e5), [Q-03](answered-questions.md#q-03), [Q-29](#q-29), [ADR 0042](../decisions/0042-asi-attribute-token-binding.md).

### Q-34: What happens to admitted QTSPs if the register is unreachable during a re-check, and how often is it checked? {#q-34}

- **Status**: open

The authorization server of the ASI checks the right of each registered
QTSP again at regular intervals in the register of relying parties. No
source says how often, or what happens when the register is unreachable.
With fail-open, a QTSP whose right was revoked during an outage stays
active, and with fail-closed, all QTSPs lose access. That trade-off
between availability and timely exclusion is a management and risk
choice. The working assumption is fail-open with a check every hour, and
the server refuses a new registration while the register is unreachable.

??? note "Options, working assumption and links"

    - **Forum**: The management organization and BZK.
    - **Question**: The authorization server of the ASI checks the right of each registered QTSP "again in regular intervals" in the register of relying parties (ETSI TS 119 478 clause 6.1.3.2, figure 2). No source says what happens if the register is unreachable at that moment. No source gives the interval either.

        With fail-open, QTSPs stay active during an outage. This also applies to a QTSP whose right was revoked during the outage. With fail-closed, the authorization server excludes all QTSPs during an outage. Two sub-questions are open:

        1. If the register is unreachable, is the behavior fail-open or fail-closed? If fail-open, after how much time does access close?
        2. At which interval does the authorization server check the right again? Or is a notification from the register on revocation sufficient?

    - **Why the demo cannot answer it**: The trade-off between availability of verification and timely exclusion of a party is a management and risk choice.
    - **Options**:
        - For an outage: (a) fail-open, (b) fail-closed, or (c) fail-open for a bounded time, then closed.
        - For the interval: (a) a periodic check, or (b) a notification from the register.
    - **Current working assumption**: Fail-open, with a check every hour by default ([`main.go#L101`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/main.go#L101), [`registration.go#L226-L240`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L226-L240), [PR #522](https://github.com/ICTU/GBO-demo/pull/522)). If the register is unreachable at a registration, the authorization server refuses with 503.
    - **Related**: [F-85](findings.md#f-85), [REQ-89](../requirements/asi.md#req-89), [Q-31](#q-31), [Q-35](#q-35), [Q-41](#q-41) (tokens after revocation).

### Q-35: Which identifier links a QTSP's access certificate to its register entry? {#q-35}

- **Status**: open

A QTSP registers at the ASI with a statement that it seals with its
certificate and that points to its entry in the register. The
authorization server must check that the entry belongs to the
certificate holder, so that no QTSP can present the entry of another.
Candidate identifiers are the EUID, the organization identifier with the
KvK number, and the OIN. The question is which identifier the
certificate and the entry share, and who sets it. In the working
assumption, the organization identifier of the certificate must equal
one of the identifiers of the entry.

??? note "Options, working assumption and links"

    - **Forum**: BZK, and the operator of the Dutch register of relying parties. The sources that the GBO team read do not designate this operator.
    - **Question**: A QTSP registers at the ASI with a software statement. The QTSP seals the statement with its certificate, and the statement holds the `registryURI` of its entry. The authorization server must establish that the entry belongs to the holder of the certificate. Otherwise, every QTSP with a valid certificate can present the entry of another QTSP.

        ETSI/EUDI TS5 names the EUID as the standard identifier in the register. A certificate carries an `organizationIdentifier`, often `NTRNL-` plus the KvK number. FSC and PKIoverheid work with the OIN.

        Which identifier is in the access certificate of a QTSP and also in its entry in the Dutch register? An authorization server needs this identifier to compare the two. Who sets this identifier?

    - **Why the demo cannot answer it**: The register and the certificate profile (ETSI TS 119 411-8) decide which identifier applies. The ASI does not decide it.
    - **Options**:
        - (a) The EUID.
        - (b) The `organizationIdentifier` with the KvK number.
        - (c) The OIN.
    - **Current working assumption**: The `organizationIdentifier` of the certificate must equal one of the identifiers of the entry ([REQ-88](../requirements/asi.md#req-88), [`registration.go#L211-L212`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L211-L212)).
    - **Related**: [F-85](findings.md#f-85), [REQ-88](../requirements/asi.md#req-88), [Q-07](answered-questions.md#q-07), [Q-31](#q-31), [Q-34](#q-34).

### Q-36: Which identification means does a Dutch ASI authorization server accept, and where does the identification data come from? {#q-36}

- **Status**: open

The ASI authorization server must identify the citizen, with the EUDI
Wallet or another procedure under the ETSI identity proofing standard.
It is open whether a Dutch server accepts the wallet, DigiD, or both.
DigiD gives only a BSN, so it is also open whether the server can fetch
the missing data from the BRP. In the working assumption, the demo
accepts both, and the token carries more data after a wallet login than
after DigiD. The demo refuses an identification without a BSN, which
excludes foreign PIDs, but it accepts a PID with unknown or revoked
status.

??? note "Options, working assumption and links"

    - **Forum**: BZK, and a lawyer or DPO. PSA [P-05](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S03](https://ictu.github.io/GBO-PSA/main/capabilities/#s03-burgeridentificatie-pseudonimisering).
    - **Question**:
        1. Does the authorization server of a Dutch ASI accept the EUDI Wallet, DigiD, or both?
        2. A means can deliver only part of the data. DigiD delivers only a BSN, and the NL PID has no place of birth. In that case, can the authorization server get the other identification data from the BRP? Or is the BSN sufficient as "the required identification data"?
        3. Does DigiD count for the Dutch ASI as a procedure per ETSI TS 119 461 use case 9.2.4? If so, at which level (Baseline or Extended LoIP)?
        4. If the revocation status of a PID cannot be determined, or if the PID is revoked, can the PID lead to an identification?
        5. Does the chain support a PID without a BSN through identity matching (PSA S03)? If so, where is that function?
    - **Why the demo cannot answer it**: Two points are legal and policy choices: which means are allowed, and whether the authorization server can get data from the BRP.

        The standards set these rules. The authorization server identifies the citizen (REQ-AZSP-6.1.3.1-02). It uses the EUDI Wallet over OpenID4VP, or "an alternative electronic identification procedure according to ETSI TS 119 461" (-03). It puts "the required identification data" in the token (-08).

        TS 119 461 V2.1.1 has use case 9.2.4, identity proofing by authentication with an eID means (p. 57). This use case contains these rules:

        - The means is at least eIDAS LoA substantial for Baseline LoIP, and high for Extended LoIP (COL-8.2.4-02X and -02A).
        - The identity proofing practice statement lists the accepted means (COL-8.2.4-01X).
        - All mandatory attributes of the context are collected and identify the person uniquely (COL-8.2.1-01A and -02).
        - A reliable register, such as a population register, can be extra evidence (USE-9.2.4-04).

        So DigiD at level Substantial or High seems to fit. Fetching the other data from the BRP also seems to fit. The GBO team did not check whether DigiD is notified under eIDAS, and at which level. The NL PID has no place of birth, the fifth mandatory attribute ([F-94](findings.md#f-94)).

    - **Options**:
        - For sub-question 1: (a) the EUDI Wallet, (b) DigiD, or (c) both.
        - For sub-question 2: (a) fetch the missing data from the BRP, or (b) the BSN alone is sufficient.
    - **Current working assumption**: The demo offers both: a DigiD mock and the NL Wallet ([REQ-102](../requirements/asi.md#req-102), [issue #544](https://github.com/ICTU/GBO-demo/issues/544), [issue #546](https://github.com/ICTU/GBO-demo/issues/546)). As a result, the token is asymmetric. With the wallet, the token carries the BSN and four PID attributes. With DigiD, it carries only the BSN and `acr`/`amr` ([REQ-86](../requirements/asi.md#req-86)).

        The wallet verifier accepts a PID whose revocation status is unknown or revoked. [REQ-45](../requirements/eudi-issuance.md#req-45), [REQ-86](../requirements/asi.md#req-86), and [REQ-102](../requirements/asi.md#req-102) refuse an identification without a BSN. This rule fits S03 ("only then can the source be queried"). But it excludes foreign PIDs and PIDs without a BSN.

    - **Related**: [F-86](findings.md#f-86), [F-88](findings.md#f-88), [F-94](findings.md#f-94), [REQ-45](../requirements/eudi-issuance.md#req-45), [REQ-86](../requirements/asi.md#req-86), [REQ-90](../requirements/asi.md#req-90), [REQ-102](../requirements/asi.md#req-102), [E7](standards-feedback.md#e7), [Q-18](#q-18), [Q-29](#q-29), [Q-40](#q-40).

### Q-37: What is GBO's role in the ASI: designated intermediary, technical supplier to bronhouders, or authentic source itself? {#q-37}

- **Status**: open

GBO builds one ASIP for several authentic sources, and the law allows an
ASIP to be the source itself or a designated intermediary. The question
is whether GBO becomes that designated intermediary, stays a technical
supplier to each bronhouder, or becomes an authentic source itself.
The role decides who seals the result and who answers for the
correctness of the data. The working assumption is the intermediary
model, which the GBO team saw as likely on October 14, 2026. The demo
names an authentic source for every data service and uses one seal for
all of them.

??? note "Options, working assumption and links"

    - **Forum**: BZK (system responsibility), the bronhouders, and a lawyer or DPO.
    - **Question**: GBO builds one ASIP for more than one authentic source ([F-89](findings.md#f-89)). The sources describe the role of an ASIP in these ways:

        - ETSI TS 119 478 says that the ASIP "can be an authentic source or an intermediary acting on its behalf" (clause 4.2).
        - CIR 2025/1569 art. 9(2) names "authentic sources or designated intermediaries recognized at national level".
        - Art. 9(4) lets the result name the source "or, where applicable, the public sector body designated to act on behalf of the authentic source".
        - 2026/1735 lets the source "or the designated intermediary" seal the result.
        - eIDAS art. 3(47) defines an authentic source as a system that "contains and provides" the data. That system is a primary source "or recognized as authentic in accordance with Union or national law".

        Does GBO (or the management organization) become the designated intermediary for ASI verification on behalf of the bronhouders? Or does each bronhouder stay ASIP itself, with GBO as technical supplier? Or is GBO itself recognized as an authentic source? In each case, who seals, and who answers for the correctness of the data?

    - **Why the demo cannot answer it**: The role follows from a designation and from the statutory responsibility for correctness. Those are administrative and legal decisions.
    - **Options**:
        - (X) GBO is the designated intermediary. `provider` is GBO, `authenticSource` is the bronhouder. GBO seals with one qualified seal of its own. This needs a national designation. The responsibility for correctness stays with the bronhouder.
        - (Y) Each bronhouder is ASIP itself, and GBO supplies the technology. `provider` is the bronhouder, there is no `authenticSource`, and each bronhouder seals itself. GBO is processor or technical service provider. GBO can possibly run one hosted service that has an identity and a seal per source.
        - (Z) GBO is itself the authentic source. `provider` is GBO, and there is no `authenticSource`. This needs statutory recognition of the GBO system as authentic. GBO then answers for data it does not manage, next to the base register that the law designates.
    - **Current working assumption**: Model X. In the team estimate of October 14, 2026, model X is likely and model Z is not. The demo has `provider` "GBO demo ASIP" ([`dataservices.json#L6`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/config/dataservices.json#L6)). In its source description, the demo names the BRP as authentic source by its legal name. The demo uses one seal.

        The provider is set per data service, but a seal per data service is not built. Since [issue #592](https://github.com/ICTU/GBO-demo/issues/592) step 5, every data service names an authentic source. So the demo does not allow a data service with the ASIP itself as source.

    - **Related**: [F-80](findings.md#f-80), [F-89](findings.md#f-89), [REQ-94](../requirements/asi.md#req-94), [E3](standards-feedback.md#e3), [Q-17](#q-17) (who holds the seal), [Q-28](#q-28) (who the Netherlands designates), [Q-32](#q-32) (seal format), [ADR 0037](../decisions/0037-asi-oauth-front-door.md), [ADR 0038](../decisions/0038-asi-data-service-per-source.md).

### Q-38: How does an authentic source connect to the ASIP: by code, by configuration, or by a description it publishes itself? {#q-38}

- **Status**: partly answered

The ASIP must turn a verification request into a query on the source.
One part is answered: the bronhouder manages the link between an
attribute and its own schema, in the metadata that it publishes. The
demo builds this: the ASIP derives one query per request from that
description, and the code adapter for the BRP is removed. Still open is
how many sources must connect and how fast, which is a management
choice. The GBO team estimates that code fits fewer than about ten
sources, and configuration or a published description fits tens of sources.

??? note "Options, working assumption and links"

    - **Forum**: The management organization, the bronhouders, and GBO architecture.
    - **Question**:
        1. How many sources must the ASIP open up, and how fast must a new source connect?
        2. Who manages the link between an attribute and the schema of the source: GBO in the ASIP, or the bronhouder in a published description?
    - **Answer so far**: Sub-question 2 is answered (October 27, 2026): the bronhouder manages the link, in its published description. The team chose option c. The source describes the attributes that it offers for verification in its source metadata. It does this as capability `asi`, next to `eudi`, in the same document. As a result, the ASIP becomes generic ([issue #592](https://github.com/ICTU/GBO-demo/issues/592)). The plan contains these choices:

        - Each attribute has a `selection`. The ASIP merges the selections of the requested attributes into one query ([REQ-92](../requirements/asi.md#req-92) still applies).
        - There is no field for fuzzy matching. The ASIP applies `MatchWithVariation` only to text values. The value schema shows which values are text. ETSI leaves fuzzy matching to the ASIP and defines it as orthographic variation.
        - Activation does not check that the policy of the source allows the fields of each selection. That check is a later step.

        On one point, the demo deviates from the plan of October 27, 2026. On that point, the demo applies. The plan said that the metadata only copies values (`gbo-simple-v1`) and that the source sets the value schema. The demo lets the source map its own fields onto each value with `pointer`, `join`, `const`, and `each`. GBO keeps the value schema per attribute identifier in [`schemas/asi-attributes.json`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json) until the EU catalogue of attributes provides it. [ADR 0039](../decisions/0039-asi-source-described-attributes.md) records this deviation.

    - **Why the demo cannot answer it**: Sub-question 1 depends on how many sources come, how fast they must connect, and who manages the link. That is a management and organization choice. In the team estimate of October 14, 2026, code with good tests fits fewer than about ten sources. Configuration or a description by the source fits tens of sources or fast onboarding.
    - **Options**:
        - (a) A code adapter per source, with a contract test against the schema of the source.
        - (b) Query and mapping as configuration in the ASIP.
        - (c) The source publishes query and mapping per attribute as metadata.
    - **Current working assumption**: Option c is built through issue #592 step 5. For each request, the ASIP derives one query from the `asi` capability of the source. The ASIP then builds the attributes from the answer. The BRP code adapter is removed. The discovery records list the attributes of the current description. If there is no current description, verify, retrieve, and discovery return 503.
    - **Related**: [F-89](findings.md#f-89), [REQ-64](../requirements/sources-identity.md#req-64), [REQ-92](../requirements/asi.md#req-92), [REQ-94](../requirements/asi.md#req-94), [Q-37](#q-37), [Q-70](#q-70), [Q-71](#q-71), [ADR 0016](../decisions/0016-source-owned-metadata.md), [ADR 0017](../decisions/0017-gbo-simple-v1.md), [ADR 0039](../decisions/0039-asi-source-described-attributes.md).

### Q-39: How does a data service contract name the authorization server, so a QTSP finds every ASIP the same way? {#q-39}

- **Status**: open

A QTSP finds a data service through the Discover Interface, and the
record points to an OpenAPI contract. The ETSI standard requires that
this contract names the OAuth authorization server, but OpenAPI has no
field for it. The question is whether ETSI will fix a way, or whether
the Netherlands sets one for its ASIPs. Without one shared way, a QTSP
cannot find every ASIP the same way. In the working assumption, the demo
uses its own extension in the security scheme, which no QTSP outside the
demo knows.

??? note "Options, working assumption and links"

    - **Forum**: For sub-question 1: ETSI ESI, and BZK through the EUDI cooperation group. For sub-question 2: BZK and the management organization.
    - **Question**: A QTSP finds a data service through the Discover Interface. The record points to the contract with `endpointDescription` ([REQ-99](../requirements/asi.md#req-99)). REQ-DIP-5.3.3-03-02-01 requires that the contract specifies the metadata of the OAuth authorization server. But OpenAPI 3.0 has no field there for an OAuth server (RFC 8414) ([F-91](findings.md#f-91)). Two sub-questions are open:

        1. Will a next version of ETSI TS 119 478 fix how the contract names the authorization server? Two examples are an extension in annex A or B, and the issuer in the record of the Discover Interface.
        2. If not, does the Netherlands fix one way for its ASIPs?

    - **Why the demo cannot answer it**: The field must be the same for all ASIPs in the EU. That needs an agreement in ETSI or at EU level.
    - **Options**:
        - (a) An extension in annex A or B of ETSI TS 119 478.
        - (b) The issuer in the Discover Interface record.
        - (c) A national convention.
    - **Current working assumption**: The demo uses the extension `x-oauth-authorization-server` in the `oauth2` security scheme. The extension holds the URL at the location of RFC 8414 §3.1 ([REQ-100](../requirements/asi.md#req-100), [PR #534](https://github.com/ICTU/GBO-demo/pull/534), [PR #537](https://github.com/ICTU/GBO-demo/pull/537), [`contract.go#L109`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/contract.go#L109)). The reference QTSP reads the extension and checks it against the issuer. This extension is a choice of the demo. A QTSP from outside the demo does not know it.
    - **Related**: [F-91](findings.md#f-91), [REQ-99](../requirements/asi.md#req-99), [REQ-100](../requirements/asi.md#req-100), [E1](standards-feedback.md#e1), [Q-32](#q-32) (same pattern), [Q-67](#q-67).

### Q-40: Must the citizen logging in at the QTSP provably be the same as the one logging in at the source's authorization server, and who checks? {#q-40}

- **Status**: open

The QTSP and the authorization server of the source each identify the
citizen, and no specification links the two identifications. The
question is whether the Netherlands requires that both are the same
person. If so, the source side can check it in the verification request,
or the authorization server can check it at login. It is also open
whether the QTSP can rely on the identification by the authorization
server. In the working assumption, the reference QTSP identifies the
citizen itself with wallet data and no BSN, but the check itself is not
built.

??? note "Options, working assumption and links"

    - **Forum**: BZK, a lawyer or DPO, and ETSI ESI for the feedback on the specification ([E6](standards-feedback.md#e6)).
    - **Question**: The QTSP identifies the citizen to whom it issues a QEAA (eIDAS art. 24(1)). The authorization server of the source identifies the citizen for the verification (REQ-AZSP-6.1.3.1-02). No specification links the two identifications ([F-93](findings.md#f-93)).

        CIR 2025/1569 art. 9(3) lets the verification request name the identification data of the subject. Art. 9(5) lets member states check that the QTSP acts at the request of a legitimate user. Three sub-questions are open:

        1. Does the Netherlands fix under art. 9(5) that the subject at the QTSP and at the authorization server is the same person?
        2. If so, does the source side check this through the verification request? In that case, the QTSP has its own identification data verified too. Or does the authorization server check it at login? In that case, the QTSP passes the data in advance.
        3. Can a QTSP use the identification by the authorization server as a "third party" in the sense of eIDAS art. 24(1a)? If so, the citizen logs in only once.

    - **Why the demo cannot answer it**: Three points are legal and policy choices:

        - whether the Netherlands imposes a check under art. 9(5)
        - which data the QTSP sends to the source side for this check
        - whether the QTSP can rely on the identification by the authorization server

        The demo can make each variant work, but it cannot make the choice.

    - **Options**:
        - (a) The QTSP identifies the citizen itself and has that data verified in the request.
        - (b) The QTSP passes its identification data to the authorization server before login.
        - (c) The QTSP relies on the data in the token. The team rejects option c. The token is meant for the ASIP, and the authorization server got the data for another purpose.
    - **Current working assumption**: The demo implements the team direction of October 19, 2026. The reference QTSP identifies the citizen itself before the verification ([issue #560](https://github.com/ICTU/GBO-demo/issues/560)). It uses name, given names, birth date, and nationalities from the wallet, and no BSN. So option a is possible, but the check itself is not built. Issuance to the wallet is the subject of [issue #549](https://github.com/ICTU/GBO-demo/issues/549). REQ-104 is removed, because it is a QTSP duty under ETSI and eIDAS (see [removed numbers](../requirements/index.md)).
    - **Related**: [F-93](findings.md#f-93), [E6](standards-feedback.md#e6), [REQ-88](../requirements/asi.md#req-88), [Q-36](#q-36) (identification means of the authorization server), [Q-37](#q-37) (who runs the ASIP and the authorization server).

### Q-41: What happens to the tokens of a QTSP whose right is revoked? {#q-41}

- **Status**: open

The authorization server checks the right of each QTSP again at
intervals, but the ETSI standard says nothing about tokens that it
already issued. The ASIP validates a token itself and does not ask the
authorization server. The question is whether a QTSP can use its token
after revocation until it expires, or whether the ASIP must learn of the
revocation. How fast a revocation takes effect is a management and risk
choice. In the working assumption, the server deactivates the client,
and issued tokens stay valid until they expire, at most 10 minutes.

??? note "Options, working assumption and links"

    - **Forum**: The management organization, BZK, and ETSI ESI for the feedback on the specification ([E10](standards-feedback.md#e10)).
    - **Question**: The authorization server re-checks the right of a registered QTSP in the register at intervals (ETSI TS 119 478 clause 6.1.3.2, figure 2). If the right lapses, the specification does not say what happens to tokens that are already issued. FAPI 2.0 §5.3.4 requires a resource server to check the revocation status of a token. The ASIP checks an RFC 9068 JWT itself and does not ask the authorization server. Two sub-questions are open:

        1. Can a QTSP use a token after its right is revoked, until the token expires? If so, for how long?
        2. If not, does the ASIP ask the authorization server for the status (introspection, RFC 7662)? Or does the ASIP keep its own list of revoked clients?

    - **Why the demo cannot answer it**: How fast a revoked right must take effect is a management and risk choice. The technique follows from that choice.
    - **Options**:
        - (a) Accept the token lifetime as the delay.
        - (b) Introspection by the ASIP.
        - (c) A shorter token lifetime.
        - (d) A list of revoked clients at the ASIP.
    - **Current working assumption**: If the right is revoked, the authorization server deactivates the client. Tokens that are already issued stay valid until they expire, at most 10 minutes. The demo records this as "not met, open" in its [security considerations](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/security-considerations.md) ([PR #574](https://github.com/ICTU/GBO-demo/pull/574)).
    - **Related**: [REQ-89](../requirements/asi.md#req-89), [F-84](findings.md#f-84), [F-85](findings.md#f-85), [Q-34](#q-34), [Q-66](#q-66), [E10](standards-feedback.md#e10).

### Q-42: When is a consent "retrieved", and how does the register learn that? {#q-42}

- **Status**: open

The functional requirements ask the consent register to record
whether and when a source first retrieved data under a consent. The
register cannot see a delivery, so the question is how it learns of one.
It is also open whether retrieved means a delivery or a use of the
consent. Each option changes what a source must build, from nothing to
an extra interface (koppelvlak) to the register. In the working assumption, the demo
shows no retrieved status, only Active, Expired, and Revoked.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead, and for option B also the bronhouders.
    - **Question**: FR-11 and FR-22 (FR-DvTP v0.9) require that the register records whether and when data was first retrieved under a consent. After the review of [F-19](findings.md#f-19), this information is a field in the register. The register does not derive it from the audit log. The open point is how the register learns of a successful delivery. It has three sub-questions:

        1. Does "retrieved" mean that data was delivered, or that a source used the consent?
        2. If the PDP denies after it requested the status, does the status change?
        3. For a consent that covers more than one source, is the status "retrieved" after the first delivery, or after all deliveries?

    - **Why the demo cannot answer it**: What "retrieved" means for the citizen, and what a source must build for it, is a design choice. This choice changes the connection conditions.
    - **Options**:
        - (A) The first status query by the PDP of a source. The register sees this query itself. But a query is not a delivery: the PDP can deny after it, or the source can fail.
        - (B) A message from the source after a successful delivery. This option is exact, but every source builds an extra interface to the register.
        - (C) Derive the status from the LDV chain. This option needs no extra interface, but it depends on [Q-08](#q-08) and [Q-25](#q-25).
    - **Current working assumption**: The demo shows no "retrieved" status. The overview shows the statuses Active, Expired, and Revoked ([issue #389](https://github.com/ICTU/GBO-demo/issues/389), open).
    - **Related**: [F-19](findings.md#f-19), [F-97](findings.md#f-97), [REQ-76](../requirements/consent.md#req-76), [Q-08](#q-08), [Q-25](#q-25), [Q-47](#q-47), [Q-48](#q-48).

### Q-43: For what purpose is a citizen's refusal recorded, and in which form? {#q-43}

- **Status**: partly answered

The functional requirements say that a refusal is recorded, but not
where, what, or for whom. The purpose decides the form: a refusal in the
citizen overview, a count per consumer as an abuse signal, or only a log
line. A record under the citizen is personal data and needs a retention
period. One point is answered: closing the window is no refusal, and
nothing happens then. In the working assumption, the demo returns the
citizen to the consumer with a denied status and records nothing.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead, a privacy officer or DPO for option a, and the management organization for option b.
    - **Question**: FR-DvTP v0.9, Flow A step A-13a, only says that the refusal is recorded. It does not say where, what, or for whom. The outcome (success, refusal, or error) already goes to the consumer in the return redirect (FR-14 criterion 3). That return needs no storage. Three sub-questions are open:

        1. Which purpose or purposes apply: a, b, c, or a combination?
        2. Is an abort (browser closed, time-out) a refusal or an outcome of its own?
        3. If a applies, can the citizen later change a refusal into a consent? Or does the consumer then start a new request?

    - **Answer so far**: Sub-question 2 is answered. Next to "agree", the citizen has only "refuse", as in FR-10 and Flow A-13a. There is no separate "abort" action. If the citizen closes the window or the session expires, nothing happens: no record and no return redirect. Sub-questions 1 and 3 stay open.
    - **Why the demo cannot answer it**: The purpose of the record is a design and privacy choice. The form follows from it.
    - **Options**:
        - (a) A record in the register with status "refused" under the citizen reference. The citizen sees it in the overview. This record is personal data, because it records that a consumer asked this citizen something. It needs a retention period.
        - (b) A count per consumer without the citizen, as an abuse signal for the management organization.
        - (c) Only a log line that accounts for the process.
    - **Current working assumption**: If the citizen refuses, the demo returns the citizen with `status=denied` and records nothing ([`PortaalConsent.tsx#L100-L106`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L100-L106)).
    - **Related**: [Q-08](#q-08) (retention), [Q-42](#q-42) (consent status), [Q-44](#q-44), [Q-63](#q-63).

### Q-44: What does the return redirect give back to the consumer, and how does the consent proof reach it? {#q-44}

- **Status**: partly answered

After every outcome, the consent portal (toestemmingsportaal) sends the citizen back to a
registered address of the consumer. On success, the signed consent proof
tells the consumer what is allowed, and on refusal or error a separate
outcome is necessary. It is open which outcomes the consumer must tell
apart, and whether the proof travels through the browser or as an
exchange code. One point is answered: an abort is no outcome, because a
citizen who closes the window does not return. In the working
assumption, the demo puts the proof in the URL fragment of the return
redirect.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead, and MijnOverheid for the redirect protocol.
    - **Question**: FR-14 requires a return redirect to a registered address after every outcome. The redirect carries the outcome (success, refusal, or error). On success, the signed proof binds the granted scopes, so the consumer knows what is allowed. On refusal or error, there is no proof, so a separate outcome is necessary. Two sub-questions are open:

        1. Which outcomes must the consumer tell apart: success, refusal, and error? On success, are the scopes in the proof sufficient? Or does the consumer also get the allowed data sets separately?
        2. Does the proof go through the browser (a), or through a code that the consumer exchanges (b)?

    - **Answer so far**: "Aborted" is not an outcome. There is no separate abort action ([Q-43](#q-43)), and a citizen who closes the window does not return. So the consumer cannot tell a citizen who stopped from a citizen who is still busy. Two points stay open: the set of outcomes for success, refusal, and error, and the transfer of the proof.
    - **Why the demo cannot answer it**: The set of outcomes is a design choice that every consumer must implement. The transfer depends on the redirect protocol (OIDC, PAR, or an own extension) and on the check of the return address ([issue #427](https://github.com/ICTU/GBO-demo/issues/427)).
    - **Options for the transfer**:
        - (a) The proof in the return redirect through the browser, as in demo v0.9.0. This option is simple. But the proof passes through the browser. Also, a URL has a limited length, and the proof carries a value per source.
        - (b) A short-lived code in the return redirect that the consumer exchanges for the proof over FSC (the OAuth authorization-code pattern). The proof does not touch the browser, but the consumer calls a service of the consent facility.
    - **Current working assumption**: The demo puts the signed proof in the URL fragment of the return redirect ([`PortaalBevestiging.tsx#L60`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalBevestiging.tsx#L60)). The demo deviates on one point. Next to "refuse", the consent screen has a "cancel" button. This button goes back to the login screen and does not return the citizen to the consumer ([`PortaalConsent.tsx#L108`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L108)). The plan in [issue #599](https://github.com/ICTU/GBO-demo/issues/599) is to remove this button.
    - **Related**: FR-14, FR-34 criterion 1, [REQ-37](../requirements/consent.md#req-37), [REQ-119](../requirements/consent.md#req-119), [Q-43](#q-43), [Q-60](#q-60), [Q-61](#q-61).

### Q-45: Does the consent facility enforce the minimal mandatory set, and who decides which sets are mandatory? {#q-45}

- **Status**: open

The functional requirements keep the minimal mandatory set always on,
but no source says whether the consent facility enforces it. It is also
open who decides which sets are mandatory, and what happens when a
consent lacks the mandatory set. The choice affects the service catalog
and the initiation request of the consumer. If the consent facility
enforces the set, both the UI and the backend enforce it. The demo has
no mandatory set and enforces none.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead, and the management organization (service catalog).
    - **Question**: FR-10 says that the minimal mandatory set is always on. Optional sets can be switched on or off. A citizen cannot consent to part of a set. No source says whether the consent facility enforces this. Three sub-questions are open:

        1. Does the consent facility enforce that every consent contains the mandatory set?
        2. Who decides which sets are mandatory? The description of FR-10 answers this in part. The consumer sets the composition of the mandatory set, within the legal ceiling of the service catalog (FR-32). It is open whether the consumer does this per request or once at setup. If per request, the initiation request ([REQ-37](../requirements/consent.md#req-37)) must name the mandatory sets.
        3. If the consent facility enforces the set and the mandatory set is missing, what happens? Does the service deny with an error to the consumer, or does something else happen?

    - **Why the demo cannot answer it**: A missing mandatory set can be an error, or a choice of the citizen with consequences for the consumer. That is a design choice. The decision on who sets "mandatory" affects the service catalog of the management organization. It also affects the initiation request of the consumer.
    - **Options**: See sub-questions 2 and 3.
    - **Current working assumption**: If the set is enforced, both the UI and the backend enforce it. The UI never enforces it alone. The demo has no mandatory set and enforces none.
    - **Related**: FR-10, FR-32, [REQ-10](../requirements/consent.md#req-10), [REQ-37](../requirements/consent.md#req-37), [Q-44](#q-44), [Q-69](#q-69).

### Q-46: Is the integrator in the consent proof, or only in the register? {#q-46}

- **Status**: open

An integrator acts on behalf of a consumer, with a mandate in the
admission register. The question is whether the consent proof must also
name the integrator, or whether that mandate is enough. With the
integrator in the proof, only that integrator can use it, but a change
of integrator makes running consents unusable. With only the mandate,
every registered integrator of that consumer can use the proof. In the
working assumption, the proof binds the consumer, and the PDP denies an
integrator without a mandate.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead, the management organization (onboarding of integrators), and PSA [B-19](https://ictu.github.io/GBO-PSA/main/vraagstukken/) (representation).
    - **Question**: Must the proof bind the integrator, or is the mandate in the register sufficient?
    - **Why the demo cannot answer it**: The demo shows that both options work. The necessary binding is a balance between abuse risk and manageability.
    - **Options**:
        - (a) The integrator is also in the proof. Then only that integrator can use the proof. But if the service provider changes integrator, running consents become unusable.
        - (b) Only the mandate in the register, as in demo v0.9.0. A change of integrator needs no action from the citizen. But every registered integrator of that service provider can use the proof.
    - **Current working assumption**: Option b. The proof binds the represented party (the service provider). The integrator has its own mandate per service provider and rule in the admission register. Without a mandate, the PDP denies with `INTEGRATOR_NOT_REGISTERED` ([`engine.rego#L253-L259`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L253-L259), [PR #464](https://github.com/ICTU/GBO-demo/pull/464), design from [F-73](findings-closed.md#f-73)). FR-DvTP v0.9 removed FR-06 (the citizen sees the integrator).
    - **Related**: FR-18, FR-37, [REQ-106](../requirements/consent.md#req-106), [AV-06](../requirements/admission.md#av-06), [F-73](findings-closed.md#f-73), [ADR 0034](../decisions/0034-integrator-delegation.md), [Q-44](#q-44), [Q-68](#q-68).

### Q-47: Which volumes must the chain handle, at start and later? {#q-47}

- **Status**: open

The chain needs volume figures for the consent register, the status
query, and the BSNk link, at start and after a few years. The figures
are citizens with a consent, new consents per day, and status queries
per second at average and peak. They matter because every request does
an online status query at the register without a cache, and every
consent costs a BSNk transformation per source. Who supplies the
estimate is open, and no figures exist. One demo measurement of the
status query gave 14.5 ms at the median and 82 ms at most.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead, the management organization, the service providers and bronhouders (expected use per use case), and BSNk (transformation capacity).
    - **Question**: Which volumes must the register, the status query, and the BSNk link handle, at start and after a few years? Who supplies the estimate? These figures are necessary for each moment:

        1. Citizens with at least one consent.
        2. New consents per day.
        3. Status queries per second, on average and at peak.

    - **Why the demo cannot answer it**: The demo runs with a few test citizens. Volumes come from the expected use per use case.
    - **Options**: None, because the figures are input. Every request does a status query online at the register, without a cache ([REQ-68](../requirements/consent.md#req-68)). So the register is in the critical path of every request. Every consent costs one BSNk transformation per source, in groups of at most four recipients ([BSNK-05](../requirements/pseudonymization.md#bsnk-05)).
    - **Current working assumption**: No figures exist. One demo measurement of the status query gave p50 14.5 ms and max 82 ms (note at [REQ-75](../requirements/consent.md#req-75)).
    - **Related**: [REQ-75](../requirements/consent.md#req-75), [REQ-68](../requirements/consent.md#req-68), [Q-05](answered-questions.md#q-05) (propagation time, which decides whether caching is allowed), [Q-42](#q-42), [Q-54](#q-54).

### Q-48: Does the register record when a consent was revoked? {#q-48}

- **Status**: open

The functional requirements ask for status insight for the citizen and
for a revocation that takes effect immediately. The question is whether
the consent register keeps the moment of revocation with the
consent, or whether the LDV log is enough. With the moment in the
register, the overview and the status query can show it, and otherwise
the portal must read the log. It is a choice about access and evidence.
In the working assumption, the register keeps only active or revoked,
and the moment is in the LDV record of the change.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead, and a privacy officer or DPO (citizen access).
    - **Question**: Must the register keep the moment of revocation with the consent, or is the LDV log sufficient? FR-22 asks for status insight for the citizen. FR-24 asks that revocation takes effect immediately.
    - **Why the demo cannot answer it**: The demo shows only "revoked". Whether the citizen or the source needs the moment is a choice about access and evidence. Technique does not decide it.
    - **Options**:
        - (a) Record the moment with the consent. The citizen sees it in the overview, and the status query can give it.
        - (b) Record the moment only in the LDV log. The register stays smaller, but the portal must read the log to show the moment.
    - **Current working assumption**: The register keeps only the status (active or revoked) per consent. The moment is in the LDV record of the change ([REQ-72](../requirements/logging-audit.md#req-72)). The register writes that record through an outbox, in the same transaction as the change.
    - **Related**: FR-22, FR-24, [REQ-68](../requirements/consent.md#req-68), [REQ-72](../requirements/logging-audit.md#req-72), [REQ-109](../requirements/consent.md#req-109), [Q-42](#q-42) (same question for another moment), [register data model](../requirements/consent.md#consent-register).

### Q-49: Are the consent register and the consent portal backend one system, and who is the BSNk participant? {#q-49}

- **Status**: open

The PSA describes the consent register and the consent portal
as capabilities and leaves their setup open. The question is whether the
register and the portal backend become one system or two, and which
party is the BSNk participant. The answer matters because a polymorphic
value must not leave the party that requested it. With two systems at
different parties, the register cannot store those values, and citizen
recognition needs another route. In the working assumption, the portal
backend requests the values at BSNk and the register stores them, under
one participant.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead, the management organization, and BZK and Logius (BSNk management organization) for the recognition. PSA [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie), [S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal).
    - **Question**: Do the register and the consent portal backend become one system or two? Which party is the BSNk participant? The PSA describes S01 and S02 as capabilities and does not describe them as systems. For S01, the PSA lists "central or federated setup" and "management organization" as open decisions.
    - **Why the demo cannot answer it**: The demo runs both as separate services under one operator. Which setup and which participant fit is a decision about management, recognition, and responsibility.
    - **Options**:
        - (a) One system, one BSNk participant.
        - (b) Two systems at one participant. That participant requests and stores.
        - (c) Two systems at different participants. Then the register must not store the polymorphic values, and citizen recognition must work differently. Route D ([ADR 0040](../decisions/0040-route-d-citizen-recognition.md)) then does not fit, and one of the routes A to C applies ([routes compared](../requirements/pseudonymization.md#routes-abc)).
    - **Current working assumption**: The demo follows option a or b. The portal backend is the requester at BSNk, and the register is storage ([REQ-23](../requirements/consent.md#req-23)). The register stores the polymorphic values that the portal requested ([REQ-69](../requirements/pseudonymization.md#req-69)). A polymorphic value does not leave the party that requested it ([BSNK-03](../requirements/pseudonymization.md#bsnk-03)).

        The earlier working assumption on the [BSNk preconditions](../requirements/pseudonymization.md#bsnk-preconditions) page made the register the recognized party. REQ-22 is removed until this question is decided (see [removed numbers](../requirements/index.md)). [ADR 0040](../decisions/0040-route-d-citizen-recognition.md) stays proposed until then.

    - **Related**: [REQ-23](../requirements/consent.md#req-23), [REQ-69](../requirements/pseudonymization.md#req-69), [BSNK-03](../requirements/pseudonymization.md#bsnk-03), [Q-26](#q-26), [Q-57](#q-57), [Q-58](#q-58), [register data model](../requirements/consent.md#consent-register).

### Q-50: How does the consent portal backend inside MijnOverheid get the verified citizen identity? {#q-50}

- **Status**: open

The citizen logs in at MijnOverheid, and the backend of the
consent portal runs inside it. The question is which evidence of
that login MijnOverheid can give to the backend, and how the backend
checks it. This matters because the backend must take the citizen
identity from a validated login assertion and never from client input.
MijnOverheid can pass a signed token, pass the BSN over an authenticated
channel, or pass the BSN encrypted for BSNk. Until someone decides, the
demo backend makes its own portal token after a mock login.

??? note "Options, working assumption and links"

    - **Forum**: MijnOverheid and the tech lead. PSA [S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal).
    - **Question**: Which evidence of the login can MijnOverheid give to the consent portal backend, and how does the backend check it? [REQ-24](../requirements/consent.md#req-24) requires that the backend takes the citizen identity from the validated assertion of the authentication service (FR-01 criterion 2). The backend must not take it from client input.

        GBO builds the UI inside MijnOverheid, and the citizen logs in there. The working assumption on the [BSNk preconditions](../requirements/pseudonymization.md#bsnk-preconditions) page is that MijnOverheid passes the BSN after login. That page does not say how. It is unknown whether a token of the authentication service is available at that moment.

    - **Why the demo cannot answer it**: The demo has no MijnOverheid. What is available there depends on the setup of MijnOverheid and on the agreements with Logius.
    - **Options**:
        - (a) MijnOverheid passes signed evidence of the login (a token or assertion) that the backend validates itself.
        - (b) MijnOverheid passes the BSN over an authenticated channel between systems. The backend trusts MijnOverheid as caller.
        - (c) MijnOverheid passes the BSN encrypted for BSNk, and the backend does not see the BSN. This option is an open design choice in [ADR 0040](../decisions/0040-route-d-citizen-recognition.md).
    - **Current working assumption**: In the demo, the backend makes its own portal token after a mock login.
    - **Related**: FR-01, PSA [P-05](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [REQ-24](../requirements/consent.md#req-24), [Q-26](#q-26) sub-question 3 (does the MijnOverheid login count as authentication for BSNk), [Q-44](#q-44), [Q-49](#q-49), [Q-59](#q-59), [Q-61](#q-61).

### Q-51: Must it be provable which information the citizen saw when giving consent? {#q-51}

- **Status**: open

When a citizen gives consent, the portal backend requires an
acknowledgment that the citizen saw the information. The question is
whether it must also be provable afterwards what that information was,
and where that evidence is kept. This matters because consent must be
informed and provable, and the GDPR requires that the controller can
show the consent. The existence of a consent proves the acknowledgment,
but it does not show the text. The demo records nothing extra, so in
effect only a versioned catalog can show what the citizen saw, and
nobody has decided this.

??? note "Options, working assumption and links"

    - **Forum**: A lawyer, a privacy officer or DPO, and the management organization (versions of catalog texts). PSA [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie).
    - **Question**: What must be provable afterwards about the information that the citizen saw, and where is it kept? Under [REQ-107](../requirements/consent.md#req-107), the backend refuses a consent without an acknowledgment that the citizen saw the information (FR-08). So the existence of a consent proves the acknowledgment. It does not prove what the citizen saw.

        GO/PSA function F2 requires that consent is "informed" and "provable". PSA S01 requires "evidence of the interaction" in the consent record. GDPR art. 7(1) requires that the controller can show the consent.

    - **Why the demo cannot answer it**: Whether the existence of the consent is sufficient evidence is a legal decision. The demo can build each option.
    - **Options**:
        - (a) Record with the consent the version of the information shown: the version of the catalog text, or a fingerprint of the text.
        - (b) Record nothing extra. The acknowledgment is implicit. If the catalog keeps versions, what was shown follows from the catalog at that moment.
        - (c) Keep the text shown.
    - **Current working assumption**: The demo records nothing extra, so option b applies in effect. There is no decision.
    - **Related**: FR-08, [REQ-107](../requirements/consent.md#req-107), [REQ-117](../requirements/consent.md#req-117), [REQ-121](../requirements/consent.md#req-121), [Q-08](#q-08), [Q-63](#q-63), [register data model](../requirements/consent.md#consent-register).

### Q-52: In which format does the citizen export the overview of consents? {#q-52}

- **Status**: open

The citizen can export the overview of consents. The question is which
format the export uses, and whether GBO follows what MijnOverheid uses
for export elsewhere. The requirement says "csv or pdf", which can mean
both formats or only one of them. The content is fixed: what the
overview shows, without the BSN or the name of the citizen. The demo has
no export, so there is no working assumption for the format.

??? note "Options, working assumption and links"

    - **Forum**: MijnOverheid and the tech lead.
    - **Question**: Which export format does MijnOverheid use, and does GBO follow it? FR-20 v0.9 criterion 3 says: "The overview can be exported in csv or pdf format." This sentence can mean both formats, or one of the two. The content is fixed: what the overview shows, without the BSN or the name of the citizen.
    - **Why the demo cannot answer it**: The format depends on the conventions of MijnOverheid, and the demo has no MijnOverheid.
    - **Options**:
        - (a) Follow what MijnOverheid uses for export in other places.
        - (b) Both formats: csv to process, and pdf to keep or share.
        - (c) One format.
    - **Current working assumption**: The demo has no export ([REQ-108](../requirements/consent.md#req-108) is not built).
    - **Related**: FR-01, FR-20, [REQ-108](../requirements/consent.md#req-108), [Q-50](#q-50), [Q-61](#q-61).

### Q-53: Within which time and by which mechanism does suspension of a consumer take effect? {#q-53}

- **Status**: open

When a consumer is suspended or terminated, it must lose its access in
time. The question is how fast that happens, by which mechanism, and who
revokes its FSC contract: the source or the management organization. An
expired or revoked consumer certificate must block access immediately,
but FSC checks revocation through a cache. It is also open whether the
citizen overview must show a consent at a suspended consumer as
something other than Active. In the demo, a suspended party gets no new
FSC contract, but it can still send requests with an existing contract.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead and the management organization. PSA [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel).
    - **Question**: PSA S04 requires that suspension or termination leads "in time" to revocation of access. [REQ-110](../requirements/admission.md#req-110) fixes the effect and leaves the consents as they are. Three sub-questions are open:

        1. Within which time must a suspension take effect, and by which mechanism? If the contract is revoked, who revokes it: the source or the management organization?
        2. If a consumer certificate expires or is revoked, access must be blocked "immediately" (FR-34 criterion 3). FSC refuses an expired or revoked certificate ([REQ-46](../requirements/sources-identity.md#req-46)). But open-fsc checks revocation with a cache, so the effect takes as long as that cache. As long as the initiation is not bound to the certificate ([Q-60](#q-60)), the consent process blocks through the status in the register ([REQ-111](../requirements/consent.md#req-111)). Does the same time limit apply as for a suspension?
        3. Must the overview of the citizen show a consent at a suspended consumer differently from "Active"? FR-30 criterion 3 asks that the status "trusted private service provider" is visible to the citizen. In demo v0.9.0, the citizen sees such a consent as Active, but the consumer cannot use it. A visible suspension affects the tone towards the consumer and the supervision.

    - **Why the demo cannot answer it**: The time limit is a management and supervision agreement. The mechanism depends on who manages the contracts.
    - **Options**:
        - (a) The source checks the admission status in the register on every request, as for an integrator in demo v0.9.0. This works immediately, but every source must call the register.
        - (b) If a consumer is suspended, its FSC contract is revoked. The source checks nothing extra. But an issued access token stays valid until it expires. After the suspension ends, a new contract is necessary.
    - **Current working assumption**: In the demo, a suspended party gets no new FSC contract. But it can still send requests with an existing contract.
    - **Related**: FR-31, FR-34, FR-36, [REQ-61](../requirements/admission.md#req-61), [REQ-110](../requirements/admission.md#req-110), [REQ-46](../requirements/sources-identity.md#req-46), [REQ-111](../requirements/consent.md#req-111), [Q-60](#q-60), [Q-62](#q-62).

### Q-54: Which durability and recovery requirements apply to the register storage? {#q-54}

- **Status**: open

The consent register is the only place that holds the consents and
the polymorphic values of a citizen. The question is which storage RINIS
offers, and which requirements apply for durability, acceptable loss,
recovery time and consistency after recovery. This matters because the
source denies when a consent is lost, while the consumer still holds a
valid consent proof. The demo register runs on Postgres when a database
is set, and in memory otherwise. If RINIS offers Postgres as a platform
service, Postgres is the obvious choice.

??? note "Options, working assumption and links"

    - **Forum**: RINIS, the tech lead, and the management organization. PSA [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie) (availability, integrity, and auditability by the operator).
    - **Question**: Which storage does RINIS offer? Which requirements apply for durability, RPO, RTO, and consistency after recovery? The register is the only place for the consents and the polymorphic values of a citizen. If a consent is lost, the status query fails and the source denies (fail closed, [REQ-68](../requirements/consent.md#req-68)). The citizen then no longer sees the consent, but the consumer has a valid proof.
    - **Why the demo cannot answer it**: The demo has no production platform. The guarantees come from the agreements with RINIS.
    - **Options**: None. This input is necessary:
        - the storage that RINIS offers
        - the acceptable loss (RPO)
        - the recovery time (RTO)
        - how the record and the issued proof agree again after recovery (a proof for a consent that is missing after recovery)
    - **Current working assumption**: If `DATABASE_URL` is set, the demo register runs on Postgres ([`postgres_store.go#L71-L75`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/postgres_store.go#L71-L75)). Otherwise, it runs in memory. If RINIS offers Postgres as a platform service, Postgres is the obvious choice.
    - **Related**: [REQ-68](../requirements/consent.md#req-68), [Q-47](#q-47), [Q-55](#q-55), [Q-63](#q-63), [register data model](../requirements/consent.md#consent-register).

### Q-55: Where is the signing key of the consent proof, and how is it rotated and retired? {#q-55}

- **Status**: open

The consent register signs every consent proof, and the PDPs of the
sources verify it with a public key. The question is where the signing
key is stored, how it rotates, and how it is revoked after a leak. It is
also open how the PDPs get the public keys. This matters because whoever
has the key can make proofs for every citizen and every consumer. With a
persistent store, the demo requires a fixed key from a file.

??? note "Options, working assumption and links"

    - **Forum**: The tech lead, RINIS (key storage), and the management organization.
    - **Question**: Where is the signing key? How is it rotated, and how is it revoked after a leak? How do the PDPs get the public keys?

        The register signs the proof (ES256). The PDPs of the sources verify the proof with the public key from a JWKS endpoint. They cache the key for five minutes. If a proof has an unknown `kid`, they fetch the key again ([REQ-68](../requirements/consent.md#req-68)). Whoever has the key can make proofs for every citizen and every consumer.

    - **Why the demo cannot answer it**: Key storage and key management belong to the platform and to operations. They are outside the scope of the demo.
    - **Options**: None. This input is necessary:
        - the storage (HSM, KMS, or other)
        - the rotation (overlap of old and new key, and the period)
        - the revocation after a leak (what happens to issued proofs)
        - the channel for the public keys to the PDPs (JWKS over FSC, or other)
    - **Current working assumption**: If the demo uses a persistent store, it requires a fixed key from a file ([`main.go#L84-L86`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L84-L86)).
    - **Related**: [REQ-68](../requirements/consent.md#req-68), [REQ-76](../requirements/consent.md#req-76) (status over FSC), [ADR 0032](../decisions/0032-consent-proof.md), [Q-54](#q-54), [Q-56](#q-56), [Q-62](#q-62).

### Q-56: How do citizen references follow a rotation of the portal HMAC key? {#q-56}

- **Status**: open

The consent portal recognizes a citizen by an HMAC of the BSN under
a secret key, and the register stores consents under that reference.
With a new key, the same BSN gives a different reference, so the portal
no longer finds the existing consents. The register cannot move them
itself, because it sees no BSN. The question is how often the key
rotates and how existing consents stay findable after a rotation. The
design uses one key and the demo has no migration, so a new key hides
older consents.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, and MijnOverheid for the case that citizen recognition works differently ([Q-26](#q-26) sub-question 5).
    - **Question**: How often does the HMAC key rotate, and why? How do existing consents stay findable after a rotation?

        The portal recognizes a citizen by an HMAC of the BSN under a secret key. The reference contains the key version ([ADR 0040](../decisions/0040-route-d-citizen-recognition.md)). The register stores consents and polymorphic values under that reference. With a new key, the same BSN gives a different reference. If nobody moves the existing consents, the portal no longer finds them. The register cannot move them itself, because it sees no BSN.

        Route D is a working assumption. There is no decision on it.

    - **Why the demo cannot answer it**: The demo knows one key. The choice depends on the key policy and on route D.
    - **Options**: The portal can handle a key rotation in one of three ways:
        - (a) Move the consents at the next login of the citizen. The portal computes both references and moves the consents.
        - (b) Keep both keys valid until all consents under the old key expire.
        - (c) Do not rotate, except after a leak. That case gets its own procedure.
    - **Current working assumption**: The design uses one key. A new `SUBJECT_REF_KEY` hides older consents. The demo has no migration.
    - **Related**: [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-69](../requirements/pseudonymization.md#req-69), [ADR 0040](../decisions/0040-route-d-citizen-recognition.md), [Q-26](#q-26), [Q-55](#q-55), [Q-57](#q-57).

### Q-57: Which protection do the stored polymorphic values get? {#q-57}

- **Status**: open

For each citizen, the consent register keeps the polymorphic
identity and pseudonym of the first activation. From these values, BSNk
makes an encrypted identity or an encrypted pseudonym for every party.
As a result, a party that has the values and can call the portal can
have values made for every source. The question is which protection the
values get: encryption with a key outside the database, access control
only, or both. The demo stores them unencrypted, in a table of their
own.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, security officer.
    - **Question**: Which protection do the PI and PP in the register get? Who can read them? For each citizen, the register keeps the PI and PP of the first activation ([REQ-69](../requirements/pseudonymization.md#req-69)). From these values, BSNk makes an encrypted identity (VI) or an encrypted pseudonym (VP) for every party. As a result, a party that has the values and can call the portal can have values made for every source. Only the portal reads them.
    - **Why the demo cannot answer it**: The protection follows from the risk assessment and the security baseline.
    - **Options**: The register can protect the values in one of three ways:
        - (a) Encryption in the database, with a key outside the database.
        - (b) Access control only (database and network).
        - (c) Both.
    - **Current working assumption**: The demo stores the values unencrypted, in a table of their own.
    - **Related**: [REQ-69](../requirements/pseudonymization.md#req-69), [BSNK-03](../requirements/pseudonymization.md#bsnk-03), [ADR 0040](../decisions/0040-route-d-citizen-recognition.md), [Q-49](#q-49) (who stores), [Q-55](#q-55), [Q-58](#q-58), [Q-63](#q-63).

### Q-58: Must the register authenticate the consent portal backend, or is network isolation enough? {#q-58}

- **Status**: open

The consent portal backend is the only caller that creates, reads
and revokes consents in the consent register. The question is
whether the register must authenticate that backend, for example with
mTLS or over FSC, or whether network isolation is enough. This matters
because a party that reaches the register directly can create or revoke
consents for every citizen. Network isolation alone requires that the
register and the backend run at one participant, in one environment. The
demo uses network isolation only, and the status query of the PDP has
its own listener over FSC.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, RINIS (network design).
    - **Question**: Does the register authenticate the consent portal backend? If so, how? The backend is the only caller of the register to create, read, and revoke consents. Citizens reach the register only through the backend ([REQ-39](../requirements/consent.md#req-39)). [REQ-76](../requirements/consent.md#req-76) requires authentication only for the status query by the PDP of the source. A party that reaches the register directly can create or revoke consents for every citizen.
    - **Why the demo cannot answer it**: The demo runs both components in one network, without authentication. The choice depends on the deployment.
    - **Options**: The register can rely on one of two protections:
        - (a) The register authenticates the backend, for example with mTLS or over FSC. The register also checks that only this caller can do these actions.
        - (b) Network isolation only. This option requires that the register and the backend run at one participant, in one environment ([Q-49](#q-49)).
    - **Current working assumption**: The demo uses option b. The status query has its own listener and goes over FSC ([REQ-76](../requirements/consent.md#req-76)).
    - **Related**: [REQ-39](../requirements/consent.md#req-39), [REQ-76](../requirements/consent.md#req-76), [Q-49](#q-49), [Q-57](#q-57).

### Q-59: Which security requirements apply to the portal UI inside MijnOverheid? {#q-59}

- **Status**: open

GBO builds the UI of the consent portal inside MijnOverheid. The
question is which security requirements apply to that UI, and which of
them MijnOverheid already imposes. Examples are a content security
policy, session management and protection against open redirects. The
return to the consumer is a redirect, so the portal must check the
return address. In the demo, only the frontend checks that address,
against a fixed list of origins.

??? note "Options, working assumption and links"

    - **Forum**: MijnOverheid, tech lead, security officer.
    - **Question**: Which security requirements apply to the UI inside MijnOverheid? Which of them does MijnOverheid already impose? GBO builds the UI of the consent portal inside MijnOverheid. Security requirements apply to this UI, for example a content security policy, session management, and protection against open redirects. The return to the consumer is a redirect, so the portal must check the return address ([issue #427](https://github.com/ICTU/GBO-demo/issues/427)).
    - **Why the demo cannot answer it**: The demo runs outside MijnOverheid.
    - **Options**: None. The necessary input is the requirements that MijnOverheid sets for contributions to its code base, and the additions that GBO must make.
    - **Current working assumption**: In the demo, only the frontend checks the return address. It checks against a fixed list of origins ([`useRedirectContext.ts#L11-L26`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/hooks/useRedirectContext.ts#L11-L26)).
    - **Related**: FR-04 (trusted government domain), FR-14, [REQ-24](../requirements/consent.md#req-24), [REQ-111](../requirements/consent.md#req-111), [Q-50](#q-50), [Q-61](#q-61).

### Q-60: If name, purpose, return address, and status come from the registration, must the origin of the initiation request be provable? {#q-60}

- **Status**: open

The functional requirements say that the initiation request of a
consumer must provably come from that service provider. The portal backend
takes name, purpose and return address from the registration, so a
forged request only gives a consent for the real consumer. A third party
can still start a request for a consumer that asked for nothing. The
question is whether that risk is acceptable, or whether the consumer
must sign the request or send it in advance over FSC. The demo passes
the context as query parameters, and its backend does not do these
checks.

??? note "Options, working assumption and links"

    - **Forum**: owner of FR-DvTP, tech lead, MijnOverheid (what the login can keep).
    - **Question**: Besides the checks of [REQ-111](../requirements/consent.md#req-111), is a provable origin of the initiation request necessary? If so, does the consumer sign the request in the URL, or send it in advance over FSC?

        FR-34 criterion 1 requires that the initiation request "provably comes from" the service provider. The criterion also requires verification of the request against the registered means of identification of the service provider. Under REQ-111, the backend takes name and purpose from the registration. The backend also checks the return address against the registered addresses, and it checks the status of the consumer. As a result, a forged request can only lead to a consent for the real consumer, with the correct name and for a registered scope. The return also goes to the address of that consumer.

        One risk remains: a third party can start a request on behalf of a consumer that asked for nothing. Only that consumer can use the proof ([REQ-68](../requirements/consent.md#req-68)).

    - **Why the demo cannot answer it**: Whether the residual risk is acceptable is a decision. The demo can build each option ([issue #427](https://github.com/ICTU/GBO-demo/issues/427)).
    - **Options**: The question has three options:
        - (a) Necessary, through a signed request in the URL. No FSC is necessary, but the content goes through the browser and MijnOverheid.
        - (b) Necessary, through a request that the consumer sends in advance over FSC. Only a reference goes through the browser (PAR, RFC 9126). This option needs an FSC service of the consent facility for consumers.
        - (c) Not necessary. Then FR-34 criterion 1 loses that part.

        For options a and b, the request or the reference must survive the MijnOverheid login (FR-13).

    - **Current working assumption**: The demo sends the context as query parameters. It keeps the context in the browser session during the mock login. The backend in demo v0.9.0 does not do the REQ-111 checks.
    - **Related**: FR-12, FR-13, FR-34, [REQ-37](../requirements/consent.md#req-37), [REQ-111](../requirements/consent.md#req-111), [Q-44](#q-44) (transfer of the proof, same options), [Q-50](#q-50), [Q-53](#q-53), [Q-61](#q-61).

### Q-61: What must MijnOverheid deliver or allow for the portal UI and the link to the consent facility? {#q-61}

- **Status**: open

GBO builds the UI of the consent portal as a contribution to the
MijnOverheid code base. Several requirements therefore depend on what
MijnOverheid delivers or allows. This question collects the points
without a question of their own, so that one meeting can discuss them
all. They include the interface to the portal backend, the redirect
protocol, the request context across the login, and ownership of the UI.
Others are accessibility, house style, the switch to the apps, and
delegation. There is no working assumption apart from the imitated shell
in which the demo runs the portal.

??? note "Options, working assumption and links"

    - **Forum**: MijnOverheid (Logius), tech lead, PSA [S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal).
    - **Question**: GBO builds the UI of the consent portal as a contribution to the MijnOverheid code base. The citizen logs in there. As a result, several requirements depend on what MijnOverheid delivers. Some of them have their own question: the verified citizen identity ([Q-50](#q-50)), the UI security requirements ([Q-59](#q-59)), and the export format ([Q-52](#q-52)). [Q-60](#q-60) covers what the login can keep for a signed or pre-sent request. This question collects the other requirements, so that one meeting can discuss them all:
        1. **Interface**: which form does the link between MijnOverheid and the consent portal backend get? How does this link relate to the interface DelenVanMijnGegevens?
        2. **Redirect protocol**: do initiation and return follow an existing protocol (OIDC, PAR), or a separate agreement?
        3. **Contributions**: on which stack does the GBO UI go into MijnOverheid? Which review and release process applies, who owns the UI, and who fixes bugs in production?
        4. **Context across the login (FR-13)**: how does the request of the consumer stay available while the citizen logs in?
        5. **Accessibility and house style**: which accessibility standard applies to the whole UI, and who checks it? Which house style or component library does MijnOverheid prescribe?
        6. **Web and app (FR-15)**: how does the switch to the DigiD app or the MijnOverheid app work? How does the citizen go back to the app of the consumer?
        7. **Delegation (FR-02)**: does MijnOverheid pass on that the citizen acts on behalf of another person? In that case, who blocks: MijnOverheid or the consent facility?
    - **Why the demo cannot answer it**: The demo has no MijnOverheid. The portal runs in an imitated shell.
    - **Options**: Each sub-question has its own options.
    - **Current working assumption**: None, apart from the demo shell.
    - **Related**: FR-02, FR-04, FR-13, FR-15, [Q-44](#q-44), [Q-50](#q-50), [Q-52](#q-52), [Q-59](#q-59), [Q-60](#q-60), [Q-73](#q-73).

### Q-62: What must the management organization record or deliver for the consent process? {#q-62}

- **Status**: open

Several parts of the consent screen and the overview depend on data or
processes of the management organization. This question collects them in
one place. They are the validity limits per service, the privacy officer
per consumer, the voluntariness text, the owner of the texts, and the
support contact. The incident processes for a failure of BSNk,
MijnOverheid or the register, and for a compromised key, are also open.
Until the management organization provides these, the demo uses fixed
configuration values.

??? note "Options, working assumption and links"

    - **Forum**: management organization, tech lead.
    - **Question**: Several requirements on the consent screen and the overview depend on data or processes that the management organization must provide. This question collects these requirements:
        1. **Validity limits (FR-11, FR-32)**: when a consent is recorded, which component enforces the limits per service? Where are the limits kept?
        2. **GDPR reference (FR-25)**: where do the contact details of the privacy officer per consumer come from? How do these details reach the portal?
        3. **Voluntariness (FR-36)**: which text does the screen show? Where does the alternative per consumer come from, and who receives complaints?
        4. **Texts**: who owns the B1 texts and the legal texts? How is the B1 level checked, and do all texts come from the catalog?
        5. **Support (FR-04)**: which contact option does the page show?
        6. **Incidents**: which process applies if BSNk, MijnOverheid, or the register fails? Which process applies if a key is compromised ([Q-55](#q-55), [Q-56](#q-56))?
    - **Why the demo cannot answer it**: The demo has no management organization. The demo fixes the values in configuration.
    - **Options**: Each sub-question has its own options.
    - **Current working assumption**: The demo uses fixed configuration values.
    - **Related**: FR-04, FR-11, FR-25, FR-32, FR-36, [AV-14](../requirements/admission.md#av-14), [AV-15](../requirements/admission.md#av-15), [Q-13](#q-13) (reopened: can the citizen change the default validity of the service?), [Q-51](#q-51), [Q-53](#q-53).

### Q-63: How long are consents, polymorphic values and citizen references kept? {#q-63}

- **Status**: open

The consent register keeps a record per consent, and the polymorphic
values per citizen under a reference. The question is how long it keeps
expired or revoked consents, the values of a citizen without a running
consent, and empty references. It is also open how long the citizen sees
old consents, and whether the citizen can ask to delete them. Retention
and deletion must follow legal and audit requirements, so this is a
legal decision. The demo keeps expired and revoked consents without a
time limit.

??? note "Options, working assumption and links"

    - **Forum**: lawyer, privacy officer or DPO, management organization, PSA [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie).
    - **Question**: PSA S01 requires that retention periods and deletion follow legal and audit requirements. [Q-08](#q-08) covers only the LDV, so this question covers the register. The register keeps the record per consent, and the PI and PP per citizen under a reference ([register data model](../requirements/consent.md#consent-register)). The question has four parts:
        1. How long does the register keep an expired or revoked consent? How long does the citizen see it in the overview?
        2. How long does the register keep the PI and PP of a citizen without a running consent?
        3. If nothing is stored under a citizen reference any more, what happens to that reference?
        4. Can the citizen ask for the deletion of expired or revoked consents?
    - **Why the demo cannot answer it**: Retention periods are a legal decision.
    - **Options**: None. The necessary input is a period per data item, and a rule for the end of the period.
    - **Current working assumption**: The demo keeps expired and revoked consents without a time limit.
    - **Related**: FR-20 (overview with consents that expired or were revoked a short time ago), [Q-08](#q-08), [Q-43](#q-43) (refusals), [Q-51](#q-51), [Q-54](#q-54), [Q-57](#q-57).

### Q-64: Must a Dutch ASIP also offer clause 6.2 (ISO 15000) besides clause 6.1, and with it deferred responses? {#q-64}

- **Status**: open

ETSI TS 119 478 lets an ASIP choose between clause 6.1 (HTTP and OAuth)
and clause 6.2 (ISO 15000). Only clause 6.2 has a deferred response, for
a source that cannot answer immediately. The question is whether a Dutch
ASIP must also offer clause 6.2, and whether such slow sources exist. If
so, it is open whether clause 6.2 can run over the eDelivery of the
Basisinrichting OOTS. The working assumption is clause 6.1 only, which
is synchronous.

??? note "Options, working assumption and links"

    - **Forum**: PSA/GO authors, bronhouders, BZK, PSA [S08](https://ictu.github.io/GBO-PSA/main/capabilities/#s08-oots-adapter), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte).
    - **Question**: REQ-ASIP-4.3-04 (ETSI TS 119 478) lets an ASIP choose between two interfaces: the clause 6.1 interface (HTTP and OAuth) and the clause 6.2 interface (ISO 15000). For verify, Annex IV of CIR 2026/1735 designates clause 6.1.1, clause 6.2.3, or both. Only clause 6.2 has a deferred response (6.2.3.2.3, 6.2.4.3.3), for a source that cannot answer immediately. Clause 6.1 is synchronous. The question has three parts:
        1. Is clause 6.1 sufficient, or must a Dutch ASIP also offer clause 6.2?
        2. Are there sources that cannot answer immediately, so that they need a deferred response?
        3. If the answer to 1 or 2 is yes, can clause 6.2 run over the eDelivery of the Basisinrichting OOTS?
    - **Why the demo cannot answer it**: It depends on the QTSPs that will use the ASI, on the sources that cannot answer immediately, and on what GBO already has for eDelivery. PSA S08 places AS4/eDelivery at the side of the Basisinrichting OOTS.
    - **Options**: The ASIP can offer one of two sets of interfaces:
        - (a) Clause 6.1 only.
        - (b) Clause 6.1 and clause 6.2.
    - **Current working assumption**: Clause 6.1 only, synchronous ([REQ-112](../requirements/asi.md#req-112)). For the ASI profile, see the [ASI requirements page](../requirements/asi.md).
    - **Related**: [REQ-112](../requirements/asi.md#req-112), [F-80](findings.md#f-80), [ADR 0037](../decisions/0037-asi-oauth-front-door.md), [Q-79](#q-79).

### Q-65: Must the ASI support requests on behalf of another person (representation)? {#q-65}

- **Status**: open

With a mandate request, a QTSP asks the ASI for attributes of a subject
while another person acts on behalf of that subject. ETSI makes support
optional and leaves the details out of the specification. The question
is whether the ASI must support such requests, and if so, whether the
authorization server or the ASIP checks the evidence of representation.
Support needs a legal basis, a source for the representation and an
agreement on who checks it. The working assumption is no support, and
the ASI answers such a request with status 501.

??? note "Options, working assumption and links"

    - **Forum**: BZK, lawyer, PSA/GO authors, PSA [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte).
    - **Question**: REQ-ASIP-6.1.1.1-12 leaves an ASIP free to support requests with `mandate`. With such a request, the QTSP asks for attributes of a subject, and another person acts on behalf of that subject. ETSI leaves the details of `mandate` out of the specification (NOTE 3 at REQ-ASIP-6.1.1.1-13). The question has two parts:
        1. Must the ASI support requests on behalf of another person?
        2. If so, where does the evidence of the representation come from? Does the authorization server or the ASIP check it?
    - **Why the demo cannot answer it**: Representation needs a legal basis, a source for the representation, and an agreement on who checks it. PSA S04 lists the governance of representation as an open point.
    - **Options**: The ASI can handle representation in one of three ways:
        - (a) No support.
        - (b) Support, with the check at the authorization server.
        - (c) Support, with the check at the ASIP.
    - **Current working assumption**: The ASI does not support representation. Such a request gets 501 ([REQ-114](../requirements/asi.md#req-114)).
    - **Related**: [REQ-114](../requirements/asi.md#req-114), [Q-73](#q-73).

### Q-66: Which security profile does the authorization server of a Dutch ASIP get? {#q-66}

- **Status**: open

ETSI lets the authorization server of an ASIP choose its client
authentication (mTLS, private_key_jwt or both) and its token binding
(mTLS or DPoP). It also leaves open whether the server fully follows
FAPI 2.0 with PAR. The question is which profile the Dutch ASIP picks. A
profile stricter than ETSI excludes QTSPs that implement only ETSI, and
a QTSP that serves several member states must support every variant. The
demo uses private_key_jwt and DPoP without PAR, as a demo choice without
a decision.

??? note "Options, working assumption and links"

    - **Forum**: management organization, security officer, PSA/GO authors.
    - **Question**: ETSI TS 119 478 lets the authorization server choose in two places. For client authentication, the server can choose mTLS, `private_key_jwt`, or both (REQ-AZSP-6.1.3.1-05). For token binding, it can choose mTLS or DPoP (REQ-AZSP-6.1.3.1-06). The QTSP uses what the authorization server chooses (REQ-TSP-6.1.3.1-02 and -03). The QTSP reads the choice from the metadata of the server (RFC 8414: `token_endpoint_auth_methods_supported`, and `dpop_signing_alg_values_supported` or `tls_client_certificate_bound_access_tokens`).

        ETSI also leaves open whether the server fully follows FAPI 2.0 (for example PAR). REQ-AZSP-6.1.3.4-01 only asks to take FAPI 2.0 "into account". The question has three parts:
        1. Which client authentication: mTLS, `private_key_jwt`, or both?
        2. Which token binding: mTLS or DPoP?
        3. Does the authorization server fully follow FAPI 2.0, with PAR, or only ETSI?

    - **Why the demo cannot answer it**: The profile is a balance between security and the threshold for QTSPs. A profile stricter than ETSI excludes QTSPs that implement only ETSI. A QTSP that connects to ASIPs in several member states must support every variant. The form of the QTSP access certificates also matters, because a QTSP can use them as mTLS client certificate ([Q-35](#q-35)).
    - **Options**: The sub-questions give the options.
    - **Current working assumption**: The demo uses `private_key_jwt` and DPoP, without PAR. This is a demo choice, and there is no decision on it ([F-84](findings.md#f-84)). The demo [security considerations](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/security-considerations.md) explain the trade-off.
    - **Related**: [F-84](findings.md#f-84), [F-96](findings.md#f-96), [Q-35](#q-35), [Q-41](#q-41), [E8](standards-feedback.md#e8), [E9](standards-feedback.md#e9), and the ASI profile on the [ASI requirements page](../requirements/asi.md).

### Q-67: How do Dutch data services get into the Discover Interface, and who registers them? {#q-67}

- **Status**: open

A QTSP uses the Discover Interface to find, per attribute, the data
service that verifies it. ETSI intends this interface for the OOTS
common services of the European Commission, such as the Data Service
Directory. No document describes how a Dutch ASIP registers its data
services there, or whether this goes through the Basisinrichting OOTS.
The question is where QTSPs find the Dutch data services, and who
registers them. The demo has a stub for the Discover Interface, and the
ASIP publishes the records itself.

??? note "Options, working assumption and links"

    - **Forum**: BZK, operator of the Basisinrichting OOTS, PSA/GO authors, PSA [B-14](https://ictu.github.io/GBO-PSA/main/vraagstukken/), [S08](https://ictu.github.io/GBO-PSA/main/capabilities/#s08-oots-adapter), [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte).
    - **Question**: ETSI TS 119 478 clause 5 describes the Discover Interface. For each attribute, a QTSP uses this interface to find the data service that verifies the attribute. The requirements apply to the Discover Interface Provider (DIP), a role next to the ASIP. Clauses 4.2 and 5.1 intend the Discover Interface for the OOTS common services that the European Commission operates. These services are the Semantic Repository for attributes, and the Data Service Directory for sources and their data services.

        CIR 2025/1569 art. 10(2) lets the Commission reuse these services for the catalogue of attributes. No document describes how a Dutch ASIP registers its data services there, or whether this goes through the Basisinrichting OOTS. The question has two parts:
        1. Does a QTSP find the Dutch data services in the OOTS Data Service Directory, or in a Discover Interface of its own?
        2. Who registers a data service there? Does this go through the Basisinrichting OOTS?

    - **Why the demo cannot answer it**: Registration in the Data Service Directory is an agreement with the Commission and within the OOTS system.
    - **Options**: A QTSP can find the Dutch data services in one of two places:
        - (a) The OOTS Data Service Directory.
        - (b) A Discover Interface of its own.
    - **Current working assumption**: The demo has a DIP stub. The ASIP publishes the records itself ([REQ-99](../requirements/asi.md#req-99)).
    - **Related**: [REQ-99](../requirements/asi.md#req-99), [REQ-100](../requirements/asi.md#req-100), [Q-31](#q-31), [Q-37](#q-37), [Q-39](#q-39), [Q-71](#q-71), [Q-79](#q-79).

### Q-68: Can policy read the FSC Peer ID as the OIN of the consumer, or must that link come from the register? {#q-68}

- **Status**: open

In FSC, the Peer ID of a party is the serial number of its certificate,
and with PKIoverheid that value is the OIN. The question is whether
policy can treat "Peer ID = OIN" as a system rule, or must get the link
between peer and organization from the admission register. The register
is necessary when one peer acts for several organizations, as with
hosting or an integrator, or when an organization changes certificate.
The working assumption is the system rule: the DvTP policy compares the
Peer ID directly with the consumer OIN in the consent.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, management organization (certificate profile and register), PSA [S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel).
    - **Question**: Is "Peer ID = OIN" a system rule that policy can build on? Or must the link between peer and organization come from the admission register? In FSC, the Peer ID is the `serialNumber` of the FSC certificate. With a PKIoverheid certificate, that value is the OIN. PSA S04 requires that the setup "links the technical identity to the admitted legal organization and role". [REQ-67](../requirements/sources-identity.md#req-67) fixes this link only for the bronhouder side.
    - **Why the demo cannot answer it**: In the demo, every peer is one organization with an OIN as Peer ID, so both options behave the same.
    - **Options**: The link between peer and organization can come from one of two places:
        - (a) Peer ID = OIN as a system rule. The certificate profile guarantees this rule, and policy can read the Peer ID as OIN.
        - (b) The admission register records the OIN of the organization per peer. Policy compares the consent with that OIN. If one peer acts for more than one organization (hosting, integrator), option b is necessary. The same applies if an organization changes certificate.
    - **Current working assumption**: Option a. The DvTP policy compares the represented party (a Peer ID) directly with the consumer OIN in the consent ([`dvtp_helper.rego#L62-L65`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvtp_helper.rego#L62-L65)).
    - **Related**: FR-33, FR-34, [REQ-61](../requirements/admission.md#req-61), [REQ-67](../requirements/sources-identity.md#req-67), [REQ-106](../requirements/consent.md#req-106), [ADR 0034](../decisions/0034-integrator-delegation.md), [Q-06](answered-questions.md#q-06), [Q-07](answered-questions.md#q-07), [Q-46](#q-46).
    - **History**: this question had the number Q-64 before.

### Q-69: Must the consent proof bind the purpose, so that the PDP checks it? {#q-69}

- **Status**: open

A consent binds one consumer, one service with its purpose, and at least
one data set. The purpose is in the register record, but the consent
proof does not carry it, so the PDP does not check it. The question is
whether the proof must bind the purpose or service, and whether the PDP
must check the admission of the consumer for it. The demo has one
service per data set, so the difference is not visible there. The
working assumption is that the service follows from the data set only.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, management organization (catalog).
    - **Question**: [REQ-12](../requirements/consent.md#req-12) binds a consent to one consumer, one service with its purpose, and at least one data set. The purpose is in the register record, but the proof does not contain it. As a result, the PDP does not check the purpose. FR-17 criterion 1 names the purpose at retrieval. The question has two parts:
        1. Must the proof bind the purpose or the service? Or is the data set sufficient until the catalog exists?
        2. At the source request, does the PDP also check that the consumer is admitted for the service (FR-16 criterion 2)? At initiation, the consent portal backend already checks this ([REQ-111](../requirements/consent.md#req-111)). To do this check, the PDP must know the service. That depends on the same choice: the service in the proof, or in the contract.
    - **Why the demo cannot answer it**: The demo has one service per data set, so the difference is not visible.
    - **Options**: The PDP can learn the service in one of three ways:
        - (a) The proof carries the service or the purpose. The PDP denies a request that does not belong to that service.
        - (b) The service follows from the data set. The purpose stays a data item of the register and the screen.
        - (c) The service follows from the FSC contract. This option requires a catalog that links services to contracts ([issue #382](https://github.com/ICTU/GBO-demo/issues/382)).
    - **Current working assumption**: Option b. The service follows only from the data set. The register gets the purpose from the redirect as `use_case` ([`PortaalConsent.tsx#L86`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/pages/PortaalConsent.tsx#L86)).
    - **Related**: FR-09, FR-16, FR-17, [REQ-12](../requirements/consent.md#req-12), [REQ-68](../requirements/consent.md#req-68), [REQ-111](../requirements/consent.md#req-111), [ADR 0032](../decisions/0032-consent-proof.md), [Q-45](#q-45).

### Q-70: Which normalization applies in fuzzy matching per kind of value, and who sets it? {#q-70}

- **Status**: open

The ASI allows fuzzy matching only for free text, to accept spelling
variations, and excludes dates, codes and numbers. The demo normalizes
white space, case, hyphens and diacritics, but not every kind of value
tolerates all of these rules. The question is whether the rules differ
per kind of value, and who sets that kind: the ASIP, the source or the
EU catalogue. In the demo, every string without a format gets the full
normalization. Postal code and country code have no format, so they get
it too, and that conflicts with the requirement.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, PSA/GO authors (ASI profile).
    - **Question**: [REQ-113](../requirements/asi.md#req-113) limits fuzzy matching to free text. It excludes dates, codes, and numbers. ETSI TS 119 478 REQ-ASIP-6.1.1.1-10 names "orthographic variations" and leaves the rules free. The demo normalization has three rules: equal white space and case, equal hyphens, and removal of diacritics with transliteration per ICAO 9303.

        Not every kind of value tolerates all three rules. For a name, all three rules fit. A postal code that differs only in a space or in case (`1234AB` and `1234 ab`) is clearly the same value. For a country code, case folding is the most that fits. The question has three parts:
        1. Does the normalization apply per kind of value? Which rules belong to postal codes and to codes?
        2. Who sets the kind of value: the ASIP, the source, or the EU catalogue of attributes?
        3. Must REQ-113 then exclude codes, or name the rules per kind of value?

    - **Why the demo cannot answer it**: What counts as the same value is an agreement between ASIP and QTSP. The QTSP must know in which cases it gets `MatchWithVariation`. The demo cannot make that agreement.
    - **Options**: The normalization can follow one of four rule sets:
        - (a) One normalization for every string without `format`.
        - (b) Normalization per kind of value. Names get the full normalization. Postal codes get only the white space and case rule. Codes get no normalization, or only the case rule. The ASIP sets the kind per attribute identifier.
        - (c) As option b, but the source gives the kind in `value_schema`, for example with `format`.
        - (d) The rules that the EU catalogue of attributes sets per attribute. This option needs the catalogue to exist ([Q-38](#q-38)).
    - **Current working assumption**: Option a. Since demo [issue #592](https://github.com/ICTU/GBO-demo/issues/592) steps 1 to 5 ([PR #624](https://github.com/ICTU/GBO-demo/pull/624)), the source describes its attributes. The ASIP takes the rule from `value_schema`.

        A string with a `format` matches exactly, for example the birth date (`format: date`). Every string without a `format` gets the full normalization ([`match.go#L31-L49`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/match.go#L31-L49), [`match.go#L137-L158`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/verification/match.go#L137-L158)). Postal code and country code have no `format` ([`asi-attributes.json#L44-L55`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json#L44-L55)). As a result, they also get the full normalization. This conflicts with REQ-113.

    - **Related**: [REQ-113](../requirements/asi.md#req-113), [REQ-84](../requirements/asi.md#req-84), [REQ-85](../requirements/asi.md#req-85), [F-92](findings.md#f-92), [ADR 0039](../decisions/0039-asi-source-described-attributes.md), [Q-29](#q-29), [Q-38](#q-38), [Q-71](#q-71), [E2](standards-feedback.md#e2).

### Q-71: Which form do address and name get as attributes, until the EU catalogue of attributes fixes it? {#q-71}

- **Status**: open

The ASIP compares an attribute in the form of a schema from the EU
catalogue of attributes. Until that catalogue has schemas, GBO sets the
schema per attribute, and each source maps its own fields to it. The BRP
splits house number and surname into parts, while the amended PID puts
the house number into the street. The question is which form address and
name get, and who registers the Dutch attributes in the catalogue. The
working assumption keeps a separate house number with letter and
addition, and puts the surname prefix (`voorvoegsel`) in the family name.

??? note "Options, working assumption and links"

    - **Forum**: BZK (registration in the catalogue), BRP bronhouder, PSA/GO authors (ASI profile).
    - **Question**: The ASIP compares an attribute as a JSON object. The object has the form of the JSON Schema that is registered for the attribute in the catalogue of attributes (ETSI TS 119 478 REQ-ASIP-6.1.1.1-06-02-01). As long as the catalogue has no schemas, GBO sets the schema per attribute identifier itself. In its source metadata, the source then describes how it maps its fields to that schema.

        The BRP splits the house number into the number (`huisnummer`), the letter (`huisletter`), and the addition (`huisnummertoevoeging`). It splits the surname into the prefix (`voorvoegsel`) and the main name (`geslachtsnaam`). The PID divides the address differently. CIR 2024/2977 first had a `resident_house_number` "including any affix or suffix". Since the amendment 2026/1731, that field is gone, and `resident_street` is "including the house number and any affix or suffix thereof".

        CIR 2025/1569 art. 7(5)(g) asks for the catalogue only "the data type of the attribute". Art. 7(3) lets the member state register the attributes of eIDAS Annex VI itself. The question has three parts:
        1. Which form does the address get: (a), (b), or (c)? Which separator goes between house number, letter, and addition?
        2. Does the name put the prefix (`voorvoegsel`) in `family_name`, or in a separate field?
        3. Who registers the Dutch Annex VI attributes in the catalogue? Does the GBO schema then follow that registration?

    - **Why the demo cannot answer it**: The form must fit what QTSPs in other member states send. In the end, it must fit what the Netherlands registers in the catalogue. The demo can only pick a form.
    - **Options for the address**: The address can have one of three forms:
        - (a) As the PID after the amendment 2026/1731: street with house number, postal code, city, and country.
        - (b) As the demo: street, house number with letter and addition, postal code, city, and country. This form follows the original PID.
        - (c) As the BRP: `huisnummer`, `huisletter`, and `huisnummertoevoeging` as separate fields.
    - **Current working assumption**: Option b. For the name, the prefix (`voorvoegsel`) and the main name (`geslachtsnaam`) go together in `family_name` ([`asi-attributes.json#L44-L55`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json#L44-L55)). Since demo [issue #592](https://github.com/ICTU/GBO-demo/issues/592), the BRP source joins the parts in the `asi` mapping of its own source metadata. The source uses a space as separator ([`gbo-source-metadata.json#L219-L280`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/config/gbo-source-metadata.json#L219-L280)). Since that issue, the ASIP has no BRP adapter in code.
    - **Related**: [REQ-113](../requirements/asi.md#req-113), [ADR 0039](../decisions/0039-asi-source-described-attributes.md), [F-94](findings.md#f-94), [Q-31](#q-31), [Q-38](#q-38), [Q-67](#q-67), [Q-70](#q-70) (normalization: whether "12a" and "12 a" match).

### Q-72: Do GBO components write attributes outside the LDV core, and if so under which extension? {#q-72}

- **Status**: open

LDV allows attributes outside its core only within an approved
extension. Several GBO components write local GBO attributes, such as
the consent ID and attestation claims, and that extension has no
approval. As a result, the demo does not log according to LDV. The
question is whether the core is enough, or whether GBO must submit an
extension to Logius for the consent ID that citizen access needs. The
starting point is core only, but the demo still writes the local
attributes.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, and Logius for option 2.
    - **Question**: Is the LDV core sufficient (option 1)? If citizen access needs the consent ID, is an extension at Logius (option 2) necessary only for that attribute? LDV allows an attribute outside `dpl.core` only within an approved extension ([LDV, `attributes`](https://logius-standaarden.github.io/logboek-dataverwerkingen/#attributes)). In demo v0.9.0, the consent register, the consent portal backend, and the EUDI adapter write `dpl.gbo.*` attributes. Examples are the consent ID, `sourceId`, `typeId`, the attestation claims, and the reason for pseudonymization. That extension is local and has no approval, so the demo does not meet [REQ-72](../requirements/logging-audit.md#req-72) ("according to Logboek Dataverwerkingen").
    - **Why the demo cannot answer it**: The demo writes the attributes because it can. Whether they are necessary, and whether an extension gets approved, is a choice about conformance and an agreement with the operator of the standard.
    - **Options**: The GBO components can handle the extra attributes in one of three ways:
        - (1) Core only: the GBO components write no `dpl.gbo.*`. What is necessary follows from the processing activity, the status, or `data_subject_id_type`.
        - (2) Submit a GBO extension to Logius (extension template) for the attributes that add something, such as the consent ID for citizen access. The components write these attributes only after approval. Until then, option 1 applies.
        - (3) Accept the deviation and record it as a note at REQ-72 ("LDV core with local extension").
    - **Current working assumption**: The starting point is option 1. The demo still writes `dpl.gbo.*` ([`consent-register/main.go#L468`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L468), [`portal.go#L170`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L170), [`ldv_issuance.go#L173-L177`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/ldv_issuance.go#L173-L177)). [`ldv-client/client.go#L44-L50`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/client.go#L44-L50) describes the local extension.
    - **Related**: [REQ-72](../requirements/logging-audit.md#req-72), [F-64](findings-closed.md#f-64), [ADR 0026](../decisions/0026-ldv-integration.md), [Q-08](#q-08).
    - **History**: this question had the number Q-70 before.

### Q-73: Whose consent is a consent given by an authorized representative, and what does the register record? {#q-73}

- **Status**: open

If a service allows delegation, an authorized representative can give
consent for another person. The requirements assume one person, who logs
in, sees only their own consents, and gets polymorphic values while
logged in. The question is in whose name the consent is, whether the
register records the representative, and who can see and revoke the
consent. It is also open whether BSNk can make a value for the
represented person during the login of the representative. There is no
working assumption, because the demo has no mandates.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, lawyer, MijnOverheid and Logius (mandates), BZK and Logius (BSNk), PSA [B-19](https://ictu.github.io/GBO-PSA/main/vraagstukken/).
    - **Question**: If the legal basis of the service does not exclude delegation, FR-02 criterion 4 (FR-DvTP v0.9) lets an authorized representative give consent. Criterion 3 says that "the citizen" is then the representative. The requirements assume one person. The identity comes from the login ([REQ-24](../requirements/consent.md#req-24)), and the citizen sees only their own consents ([REQ-40](../requirements/consent.md#req-40)). The register knows the citizen under one reference, with the polymorphic values of that citizen ([REQ-69](../requirements/pseudonymization.md#req-69)). BSNk transforms only while the citizen is logged in ([BSNK-04](../requirements/pseudonymization.md#bsnk-04)).

        For a mandate service, BSNk requires that the mandate is registered. With a mandate, the data belongs to the represented person, while the representative is logged in. If a service excludes delegation, the consent facility refuses ([REQ-118](../requirements/consent.md#req-118)). This question is about the services that allow delegation. The question has four parts:
        1. In whose name is the consent: the represented person or the representative?
        2. Does the register record that a representative gave the consent, and which representative?
        3. Who sees the consent in the overview, and who can revoke it?
        4. On the login of the representative, can the consent facility have BSNk make a value for the represented person? Or does that need another role ([Q-26](#q-26))?

    - **Why the demo cannot answer it**: The demo has no mandates. Who the data subject is, and who can view and revoke the consent, is a legal choice.
    - **Options**: The consent facility can handle a representative in one of three ways:
        - (a) The consent is in the name of the represented person. The register records the representative with it, and both persons see the consent.
        - (b) The consent is in the name of the represented person. The representative appears only in the LDV log.
        - (c) Allow delegation for no service, until a service asks for it.
    - **Current working assumption**: None. The demo has no mandates.
    - **Related**: FR-02, FR-20, FR-23, [REQ-118](../requirements/consent.md#req-118), [REQ-24](../requirements/consent.md#req-24), [REQ-40](../requirements/consent.md#req-40), [REQ-69](../requirements/pseudonymization.md#req-69), [BSNK-04](../requirements/pseudonymization.md#bsnk-04), [Q-26](#q-26), [Q-61](#q-61) sub-question 7, [Q-65](#q-65).
    - **History**: this question had the number Q-71 before.

### Q-74: Does GBO build the registration and onboarding facility for service providers, or the management organization? {#q-74}

- **Status**: open

Three requirements describe a facility where a service provider logs in
with eHerkenning, applies with supporting documents, and gets its
certificate checked. GBO builds the admission register, but that
register knows only FSC Peer IDs and has no accounts or certificates. In
this design, the registration and review process is with the management
organization. The question is whether that organization builds or buys
the facility, or GBO builds a self-service flow on top of the register.
There is no working assumption, because the demo loads its participants
into the register in advance.

??? note "Options, working assumption and links"

    - **Forum**: tech lead.
    - **Question**: Three requirements describe a facility where a service provider registers and manages its connection:
        - FR-03: login with eHerkenning or another recognized means. Onboarding functions are available only after authentication.
        - FR-29: start an application after login, with supporting documents.
        - FR-33 criterion 2: at registration, check validity, revocation status, and issuer of the certificate.

        GBO builds the admission register ([REQ-61](../requirements/admission.md#req-61)). That register is keyed on the FSC Peer ID. It sees no certificate and has no accounts. In this design, the registration and review process is with the management organization ([Q-22](answered-questions.md#q-22)).

    - **Why the demo cannot answer it**: The demo has no registration process. Participants are in the register in advance. Who builds the facility is a decision about the division of roles in the build phase.
    - **Options**: The facility can come from one of two parties:
        - (a) The management organization builds or buys the registration and onboarding facility. GBO delivers the admission register with its management interface.
        - (b) GBO builds the registration and review flow on top of the admission register, as self-service for service providers. With option b, FR-03, FR-29, and FR-33 criterion 2 become requirements on that component.
    - **Current working assumption**: None. The demo register has its participants loaded in advance.
    - **Related**: FR-03, FR-29, FR-30, FR-33, [REQ-61](../requirements/admission.md#req-61), [REQ-123](../requirements/admission.md#req-123), [Q-06](answered-questions.md#q-06), [Q-22](answered-questions.md#q-22).
    - **History**: this question had the number Q-72 before.

### Q-75: Does every source response get one seal, regardless of channel (DvTP, EUDI, ASI)? {#q-75}

- **Status**: open

The functional requirements ask the bronhouder to seal all outgoing
data sets with a qualified electronic seal, without naming the standard.
In the ASI, the ASIP already seals every result, and in issuance the
attestation carries the seal of the issuer. A DvTP source response has
no seal, and FSC mTLS protects only the transport. The question is
whether every response gets one seal, which level and format apply, who
holds the key, and what happens when sealing fails. The starting point
is one seal for every channel, and in the demo only the ASI seals.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, owner of FR-DvTP, bronhouders.
    - **Question**: FR-27 requires that the bronhouder seals all outgoing data sets with a qualified electronic seal. The seal makes origin and integrity provable (criterion 1). The seal must meet "applicable system standards" (criterion 2), but FR-27 does not name the standard.

        In the ASI, the ASIP already seals every verification result ([REQ-83](../requirements/asi.md#req-83)). [Q-32](#q-32) covers the format. In issuance, the attestation carries the seal of the issuer ([Q-17](#q-17)).

        For a source response in DvTP, no seal exists. FSC mTLS protects only the transport between peers. It does not protect the response after the consumer receives it, or after an integrator passes it on. The question has three parts:
        1. Does every source response get one seal regardless of channel (a), a form per channel (b), or no seal (c)?
        2. If so, which seal applies: qualified, or advanced with a PKIoverheid certificate? Which format applies, under which system standard (FR-27 criterion 2)? Who holds the key: the source, or a GBO component that seals on behalf of the source?
        3. If sealing fails, what happens: no delivery, or delivery without a seal?

    - **Why the demo cannot answer it**: The demo can build each option. Which level is necessary, in which format, and who holds the key, is a choice about trust and management.
    - **Options**: The source responses can get one of three kinds of protection:
        - (a) One seal on every source response, regardless of channel. This option fits the ASI, where the ASIP already seals every response.
        - (b) A separate form per channel.
        - (c) No seal. FSC mTLS and the transaction log are sufficient, and FR-27 then applies to the transport only.
    - **Current working assumption**: Option a is the starting point. In the demo, only the ASI seals.
    - **Related**: FR-18 (integrator as processor), FR-27, [REQ-08](../requirements/authorization.md#req-08), [REQ-46](../requirements/sources-identity.md#req-46), [REQ-83](../requirements/asi.md#req-83), [AV-06](../requirements/admission.md#av-06), [ADR 0041](../decisions/0041-asi-seal-format.md), [Q-17](#q-17), [Q-32](#q-32).
    - **History**: this question had the number Q-73 before.

### Q-76: Does the validity period apply per consent or per source within the consent? {#q-76}

- **Status**: open

The functional requirements give each consent rule its own validity
period per source, while the register and the proof know one valid-until
per consent. The question is which of the two levels applies. A validity
per source changes the screen, gives the proof a valid-until per source,
and lets a consent expire for one source only. The demo calls one source
per consent, so the difference is not visible. The working assumption is
one validity per consent, equal to the expiry time of the proof.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, owner of FR-DvTP, management organization (duration per service in the catalog).
    - **Question**: Must a consent have a separate validity per source? Or does one validity apply to the whole consent? FR-38 criterion 2 lets each consent rule refer to "(bronhouder, data element, validity period)". So FR-38 has a validity per source. [REQ-19](../requirements/consent.md#req-19) and the [register data model](../requirements/consent.md#consent-register) know one valid-until per consent. The proof has one expiry time, equal to that valid-until.
    - **Why the demo cannot answer it**: Under one consent, the demo calls one source, so the difference is not visible.
    - **Options**: The validity can apply at one of two levels:
        - (a) One validity per consent, as in REQ-19. FR-38 must then change.
        - (b) A validity per source within one consent. This option affects the screen, which shows the duration per source. It affects the proof, which has a valid-until per source, and the PDP of each source checks its own valid-until. It also affects the status: a consent can be expired for one source and not for another.
    - **Current working assumption**: Option a: one validity per consent. The proof `exp` equals the valid-until.
    - **Related**: FR-11, FR-38, [REQ-19](../requirements/consent.md#req-19), [REQ-38](../requirements/consent.md#req-38), [REQ-68](../requirements/consent.md#req-68), [REQ-117](../requirements/consent.md#req-117), [Q-13](#q-13).
    - **History**: this question had the number Q-74 before.

### Q-77: What is a change of a consent: a new consent or an amendment of the existing one? {#q-77}

- **Status**: open

The PSA asks the consent register to support granting, change,
revocation and expiry of a consent, but no requirement covers change.
The consent proof binds the data sets and the validity, so a change also
affects the proof that the consumer holds. The question is which changes
the citizen can make, who starts them, and whether the consumer then
gets a new proof. The options range from no change, through restrictions
only, to a new consent that replaces the old one. The working assumption
is no change: the citizen revokes, and the consumer starts a new
request.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, PSA [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie).
    - **Question**: PSA S01 requires that the register supports "granting, change, revocation and expiry". [REQ-12](../requirements/consent.md#req-12), [REQ-14](../requirements/consent.md#req-14), [REQ-19](../requirements/consent.md#req-19), and [REQ-109](../requirements/consent.md#req-109) cover granting, revocation, and expiry. No requirement and no FR covers change. FR-DvTP v0.9 knows only giving and revoking.

        The proof binds the sets and the validity ([REQ-68](../requirements/consent.md#req-68)). As a result, a change also affects the proof that the consumer already has. The question has two parts:
        1. Which changes must the citizen be able to make? Who starts them: the citizen in the overview, or the consumer with a new request?
        2. Does the consumer get a new proof after a change?

    - **Why the demo cannot answer it**: What the citizen can change, and what the consumer notices of it, is a design choice. This choice has consequences for the proof and the return redirect.
    - **Options**: The register can support a change in one of three ways:
        - (a) No change. The citizen revokes, and the consumer starts a new request.
        - (b) The citizen can only restrict: switch off an optional set, or shorten the validity. The restriction takes effect through the status query, and the consumer keeps the existing proof.
        - (c) A change makes a new consent with a new proof, and revokes the old consent.
    - **Current working assumption**: Option a. The demo has no change function.
    - **Related**: [REQ-12](../requirements/consent.md#req-12), [REQ-14](../requirements/consent.md#req-14), [REQ-19](../requirements/consent.md#req-19), [REQ-68](../requirements/consent.md#req-68), [REQ-109](../requirements/consent.md#req-109), [Q-13](#q-13), [Q-44](#q-44).
    - **History**: this question had the number Q-75 before.

### Q-78: How does the reference policy show that it is not tied to one policy language or engine? {#q-78}

- **Status**: open

The PSA requires that policy is product-independent and not tied to one
policy language or engine. The reference policy of GBO uses one language
for one engine. A source with another PDP cannot take it over or show
equal decisions. The question is how GBO shows independence: rules as
data, a shared decision test set, or one open language with an exit
path. There is no decision, and the demo has one engine and one policy
language.

??? note "Options, working assumption and links"

    - **Forum**: tech lead, PSA [S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie), [S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie).
    - **Question**: Which option does GBO follow for its reference policy? Does the requirement also apply to policy that a bronhouder writes itself, or only as a guideline (RL)? PSA S05 requires that "the interface and the policy are product-independent". S06 requires that policy is "not tied to one specific policy language or implementation" (see also [P-09](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)). [REQ-42](../requirements/authorization.md#req-42) covers the interface.

        The reference policy that GBO delivers is in one policy language, for one engine. A source that chooses another PDP cannot take this policy over. That source also cannot show that its decisions are the same.

    - **Why the demo cannot answer it**: The demo runs one engine. Only a second engine can show whether the policy is portable.
    - **Options**: GBO can show the independence in one of three ways:
        - (a) The content of the rules (service, actor, sets, fields, regime) as data, apart from the engine code, with a thin layer per engine.
        - (b) A decision test set apart from the engine, which every PDP must pass, next to the policy in one language. Each test maps an AuthZEN request to the expected decision and reason.
        - (c) Accept one open policy language as sufficient, with a recorded exit path ([D-13](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)).
    - **Current working assumption**: No decision. The demo has one engine and one policy language.
    - **Related**: [REQ-42](../requirements/authorization.md#req-42), [RL-01](../requirements/authorization.md#rl-01), [ADR 0021](../decisions/0021-central-pap-signed-bundles.md), [Q-16](answered-questions.md#q-16), [Q-21](answered-questions.md#q-21).
    - **History**: this question had the number Q-76 before.

### Q-79: Does GBO build the OOTS adapter, or does the OOTS-V operator extend its facility with the GBO interface? {#q-79}

- **Status**: open

The PSA lets an OOTS adapter connect to the national interface of
OOTS-V, and OOTS requests use the same authorization and logging as
other requests. The question is whether GBO builds that adapter, or the
OOTS-V operator extends its facility with the GBO interface. The choice
decides the route to the source, the regime and evidence for OOTS, and
the versioned mapping to OOTS-EDM. The PDP knows only the consent and
PID regimes, so it denies an OOTS request without its own evidence.
There is no working assumption, because the demo has no OOTS route.

??? note "Options, working assumption and links"

    - **Forum**: BZK and OOTS coordination, tech lead, PSA [B-12](https://ictu.github.io/GBO-PSA/main/vraagstukken/), [S08](https://ictu.github.io/GBO-PSA/main/capabilities/#s08-oots-adapter), [S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus).
    - **Question**: Does GBO build the OOTS adapter, or does the OOTS-V operator extend its facility with the GBO interface? Where is the boundary between OOTS-V and the mapping function?

        PSA S08 lets the OOTS adapter connect to the national interface of OOTS-V. OOTS requests use the same generic authorization and logging as other data requests. Bronhouders do not depend on AS4/eDelivery. The Basisinrichting OOTS stays responsible for transport, discovery, and the European process interaction. If the bronhouder configures a mapping, a central mapping function translates to OOTS-EDM.

        Who builds the adapter is an open decision of S08. This design has no OOTS requirement. Three items depend on the choice:
        - The route of an OOTS request to the source.
        - The regime and the evidence for OOTS. [REQ-74](../requirements/authorization.md#req-74) knows only the consent regime and the PID regime. As a result, the PDP denies an OOTS request without its own evidence.
        - The mapping to OOTS-EDM with traceable versions, as [REQ-124](../requirements/eudi-issuance.md#req-124) requires for issuance.

    - **Why the demo cannot answer it**: The demo does not touch OOTS.
    - **Options**: The OOTS adapter can come from one of two parties:
        - (a) GBO builds the OOTS adapter, behind the national interface of OOTS-V.
        - (b) The OOTS-V operator extends its facility with the GBO interface. GBO delivers only the generic source access.
    - **Current working assumption**: None. The demo has no OOTS route.
    - **Related**: [REQ-04](../requirements/authorization.md#req-04), [REQ-44](../requirements/authorization.md#req-44), [REQ-46](../requirements/sources-identity.md#req-46), [REQ-74](../requirements/authorization.md#req-74), [REQ-124](../requirements/eudi-issuance.md#req-124), [ADR 0031](../decisions/0031-regime-from-evidence.md), [ADR 0020](../decisions/0020-as4-bridge-for-oots.md), [Q-64](#q-64), [Q-67](#q-67).
    - **History**: this question had the number Q-77 before.

### Q-83: Which authorization server identifies the citizen when an attestation is issued with the authorization code flow? {#q-83}

- **Status**: open

In the authorization code flow, an authorization server identifies the
citizen and records consent, instead of the citizen sharing the PID with
the issuer. HAIP 1.0 requires this flow, while ETSI TS 119 472-3 asks an
issuer to offer at least one of the two flows. OpenID4VCI 1.0 leaves open
how the authorization server identifies the citizen, and ETSI TS 119 478
covers only verification for QTSPs. GBO already plans an authorization
server for the ASI that identifies the citizen and shows a request page
per source. The question is which authorization server identifies the
citizen if GBO offers this flow. It also asks what that means for the
requirements that assume only a PID disclosure.

??? note "Options, working assumption and links"

    - **Forum**: tech lead. PSA [S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte).
    - **Question**: [HAIP 1.0](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html) section 4 says that the wallet and the credential issuer must support the authorization code flow. [ETSI TS 119 472-3](https://www.etsi.org/deliver/etsi_ts/119400_119499/11947203/01.01.01_60/ts_11947203v010101p.pdf), which Implementing Regulation (EU) 2026/1731 applies to the issuance interface, asks the wallet to support both flows (GEN-REQ-4.1-03). It asks an issuer to implement at least one of them (GEN-REQ-4.1-04). [OpenID4VCI 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) section 3 leaves the authentication of the citizen to the authorization server. One example the specification gives is a credential presentation.

        1. Which authorization server identifies the citizen and records consent for issuance with the authorization code flow?
        2. If the authorization server of the ASI also serves issuance: which clients and resources does it accept? [REQ-88](../requirements/asi.md#req-88) and [REQ-89](../requirements/asi.md#req-89) admit only clients with the entitlement `QEAA_Provider`.
        3. [REQ-45](../requirements/eudi-issuance.md#req-45) takes the subject of a source query only from a verified PID disclosure. Which identification replaces it in this flow, and which identification means count ([Q-36](#q-36))?

    - **Why the demo cannot answer it**: It is a choice about components and responsibilities: which party identifies the citizen and records consent for issuance. The demo can build each option, but cannot choose between them.
    - **Options**:
        - (a) The issuer has its own authorization server, with its own login.
        - (b) The authorization server of the ASI is also the authorization server of the issuer. The wallet sends its authorization request and token request there.
        - (c) The issuer keeps its own authorization server toward the wallet, and is an OAuth client of the authorization server of the ASI. The citizen logs in and consents there. This is the proposal: one place where the citizen logs in and consents per source, in the same pattern as ETSI TS 119 478.
    - **Current working assumption**: None. The TO describes issuance only after a PID disclosure ([ADR 0018](../decisions/0018-eudi-disclosure-issuance.md)).
    - **Related**: [Q-28](#q-28), [Q-36](#q-36), [Q-37](#q-37), [REQ-45](../requirements/eudi-issuance.md#req-45), [REQ-88](../requirements/asi.md#req-88), [REQ-89](../requirements/asi.md#req-89), [REQ-91](../requirements/asi.md#req-91), [ADR 0018](../decisions/0018-eudi-disclosure-issuance.md), [ADR 0037](../decisions/0037-asi-oauth-front-door.md).
