# Answered questions

These questions have an answer, or they are closed. Each entry gives the answer and where it landed. The questions that are still open are on [Open questions](open-questions.md).

### Q-02: Central authorization server or distributed PDP (per source holder)? {#q-02}

- **Status**: answered
- **Question**: Does one central PDP decide for all sources, or does each source holder (bronhouder) run its own PDP?
- **Answer**: Decentral, at the source holder. The [GO table of provisions](https://ictu.github.io/GBO-GO/main/#overzicht-voorgestelde-oplossing) places the source access API, the PEP, PDP, and PAP, and the FSC Inway at the source holder. If responsibilities and availability are assured, [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie) allows a PDP per source holder or a shared PDP. [B-04](https://ictu.github.io/GBO-PSA/main/vraagstukken/) allows several variants under one PEP-PDP interface. The B-04 owners (bronhouders, FDS/GDI) set the conditions for a shared PDP. GBO does not set them.
- **Landed in**: [ADR 0004](../decisions/0004-federated-authorization.md), [REQ-04](../requirements/authorization.md#req-04). As a shortcut, the demo runs one shared PDP behind both Inways. [SL-44](increments.md#sl-44) shows that each source can run its own PDP with bundle distribution.

### Q-03: Atomic consent or field level: what is lawful and understandable? {#q-03}

- **Status**: answered
- **Question**: Does the citizen consent per field, or per indivisible data set?
- **Answer**: Per data set. In the GO, consent applies to a specific purpose, consumer, and data set. FR-10 (FR-DvTP v0.9) puts consent at set level, with "1 scope = 1 record". The citizen switches an optional set on or off as a whole. The demo portal switches per scope and conforms. FR-10 also adds a fixed minimal mandatory set, which is [Q-45](open-questions.md#q-45) and [issue #382](https://github.com/ICTU/GBO-demo/issues/382).
- **Landed in**: [REQ-10](../requirements/consent.md#req-10), [F-03](findings-closed.md#f-03).

### Q-04: Is consent single-use or repeatable within a validity period? {#q-04}

- **Status**: answered
- **Question**: Is a consent valid for one retrieval, or can the consumer use it again until it expires?
- **Answer**: Repeatable. In FR-11 (FR-DvTP v0.9), every consent has a configurable validity period. Within that period, the consumer can use the consent again. Single use is no longer an option.
- **Landed in**: [REQ-19](../requirements/consent.md#req-19), [F-04](findings-closed.md#f-04). The question who sets the period is [Q-13](open-questions.md#q-13).

### Q-05: Who is authoritative for revocation and expiry, and what is the propagation SLA? {#q-05}

- **Status**: answered
- **Question**: Which party is authoritative for revocation and expiry? How much time can a revocation take to reach the decision?
- **Answer**: The central consent register (toestemmingsregister) is authoritative (GO, [B-06](https://ictu.github.io/GBO-PSA/main/vraagstukken/)). Revocation has direct effect. The authorization chain calls the register as PIP when the data request arrives ([PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie), S02 "without undue delay", FR-11 v0.9 "real-time"). The demo conforms: the PDP calls for the status per request, without a cache ([PR #371](https://github.com/ICTU/GBO-demo/pull/371)). The proof travels signed, but its status stays online ([F-61](findings-closed.md#f-61)).
- **Landed in**: [REQ-68](../requirements/consent.md#req-68), [ADR 0032](../decisions/0032-consent-proof.md). The figures (propagation time, availability, latency) are a design requirement in [REQ-75](../requirements/consent.md#req-75).

### Q-06: Authentication means for private parties: eHerkenning, PKI certificate, or both? {#q-06}

- **Status**: answered
- **Question**: With which means does a private party authenticate: eHerkenning, a PKI certificate, or both?
- **Answer**: Both, with separate roles.
    - FR-03 (FR-DvTP v0.9): people use eHerkenning, at onboarding and for management.
    - FR-33 and FR-34: systems use an organization identification means from a recognized issuer, linked to OIN or KvK.
    - [PSA S04](https://ictu.github.io/GBO-PSA/main/capabilities/#s04-organisatie-authenticatie-vertrouwensstelsel): organizations and systems use recognized identifiers and certificates.
    - The demo conforms for systems. The legal identity comes from the validated certificate ([F-60](findings-closed.md#f-60)).
    - The origin of source metadata fetched outside FSC is a design matter and no question for the PSA ([F-71](findings.md#f-71)).
- **Landed in**: [REQ-67](../requirements/sources-identity.md#req-67), [REQ-64](../requirements/sources-identity.md#req-64), [ADR 0023](../decisions/0023-identity-convergence.md). The identifier and the issuer are [Q-07](#q-07).

### Q-07: PKIoverheid scope as trust anchor (also EUDI Access CA?) {#q-07}

- **Status**: answered
- **Question**: Is PKIoverheid the one trust anchor for both FDS and EUDI, including the EUDI Access CA?
- **Answer**: The question is answered or no longer applies, as follows:
    - On the FDS side, systems authenticate with PKIoverheid certificates ([GO](https://ictu.github.io/GBO-GO/main/), PSA S04).
    - The seal on an attestation follows the eIDAS framework. It uses a qualified seal certificate from a QTSP, checked against the EU trusted lists ([F-66](findings-closed.md#f-66)).
    - Access certificates (ETSI TS 119 411-8) only authenticate a provider or relying party to the wallet. They do not sign attestations.
    - GO and PSA no longer pursue one infrastructure for FDS and EUDI.
    - Issuer and reader certificates are a set per source. The reason is that the legal identity and the display name depend on the signing certificate ([issue #225](https://github.com/ICTU/GBO-demo/issues/225)).
    - The Access CA is a dependency on the Dutch EUDI governance.
    - The open key and seal question moved to [Q-17](open-questions.md#q-17).
- **Landed in**: [REQ-58](../requirements/eudi-issuance.md#req-58), [F-66](findings-closed.md#f-66), [ADR 0023](../decisions/0023-identity-convergence.md). For a private consumer, the choice is OIN or KvK. The GO names the OIN. The link between the identifiers is an open decision in S04.

### Q-09: How does the FSC grant (org permission) relate to consent (legal basis)? Can one be missing? {#q-09}

- **Status**: answered
- **Question**: Are organization permission (the FSC grant) and legal basis (consent) separate checks, and must both always be present?
- **Answer**: Yes, there are two separate, cumulative checks:
    - Admission: PSA S04 ("participation requires a prior admission decision") and FR-16 (FR-DvTP v0.9).
    - Legal basis: [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie), FR-17, and the GO.

    The demo conforms ([SL-05](increments.md#sl-05), [SL-45](increments.md#sl-45)). The governance part is [Q-22](#q-22) and [B-09](https://ictu.github.io/GBO-PSA/main/vraagstukken/).

- **Landed in**: [REQ-61](../requirements/admission.md#req-61), [REQ-62](../requirements/admission.md#req-62), [REQ-74](../requirements/authorization.md#req-74).

### Q-10: Which functions must really be central, and which are decentral at each source holder? {#q-10}

- **Status**: answered
- **Question**: Which provisions run centrally, and which run at each source holder?
- **Answer**: The [GO table of provisions](https://ictu.github.io/GBO-GO/main/#overzicht-voorgestelde-oplossing) gives the answer:
    - The PEP, PDP, and PAP and the source access are decentral, at the source holder.
    - The consent facility (toestemmingsvoorziening) is central and mandatory for DvTP ("needs a statutory basis").
    - BSNk PP is mandatory for DvTP (Logius).
    - PuB-EAA issuance, the ASI provider, and the OOTS adapter are optional central connection provisions.
    - Operators "still to be decided" fall under [B-17 and B-06](https://ictu.github.io/GBO-PSA/main/vraagstukken/).
    - Funding is outside this analysis.
- **Landed in**: [ADR 0004](../decisions/0004-federated-authorization.md), [Q-02](#q-02). In the demo, the register and BSNk are central, which conforms. The PDP is shared as a shortcut. The demo removed `sector-pip` ([issue #378](https://github.com/ICTU/GBO-demo/issues/378)).

### Q-11: Transformation between source schema and canonical model: where and how? {#q-11}

- **Status**: answered
- **Question**: Where and how is a source schema transformed to a canonical model?
- **Answer**: There is no central canonical model.
    - [GO F4](https://ictu.github.io/GBO-GO/main/#f4-semantiek-eenheid-van-taal) gives a shared concept framework (NL-SBB, MIM, RDF/SKOS, DCAT-AP-NL) and "the canonical data models of source holders".
    - In [PSA S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus), mappings are explicit and traceable. Source holders and domains own their models.
    - For EUDI, the source supplies its own mapping ([F-57](findings.md#f-57)).
    - For OOTS, there is an optional shared mapping facility (GO, B-12).
    - Ownership of the semantics falls under [B-11](https://ictu.github.io/GBO-PSA/main/vraagstukken/).
    - One point is open for a check. S10 requires that every data service refers to a managed schema and concept framework. That includes the service description of the source (`/.well-known/gbo`).
- **Landed in**: [ADR 0024](../decisions/0024-canonical-semantic-models.md), [REQ-64](../requirements/sources-identity.md#req-64), [F-57](findings.md#f-57).

### Q-12: Role of integrators: pass-through, and can they see data? {#q-12}

- **Status**: answered
- **Question**: Is an integrator only a pass-through, and can it see the data?
- **Answer**:
    - FR-DvTP v0.9 removes FR-06. The citizen gets no information about the integrator.
    - FR-18: the integrator is a processor for the service provider (dienstverlener). It can view and edit data as far as the assignment needs. It does so under a processing agreement and without persistent storage.
    - FR-37: the integrator has its own onboarding and its own organization identification means. It also has a registration in the service catalog per service provider and use case.
    - For more information, see PSA S04, S05, and [B-19](https://ictu.github.io/GBO-PSA/main/vraagstukken/).
    - The consequence for the actor binding of consent was [F-73](findings-closed.md#f-73). The demo tested it with FSC delegation ([issue #379](https://github.com/ICTU/GBO-demo/issues/379)).
- **Landed in**: [REQ-106](../requirements/consent.md#req-106), [AV-06](../requirements/admission.md#av-06), [ADR 0034](../decisions/0034-integrator-delegation.md). Follow-up: [Q-46](open-questions.md#q-46).

### Q-15: How does the Manager decide which access-basis path applies to a (consumer x scope) combination? {#q-15}

- **Status**: answered
- **Question**: Which mechanism selects the access-basis path (consent or legal basis) for a request?
- **Answer**: The premise ("the Manager selects the path") lapsed.
    - The regime follows from the evidence that the request carries. A consent token opens the consent regime. Without a consent token, the PID regime applies ([PR #363](https://github.com/ICTU/GBO-demo/pull/363)).
    - The GO and [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie) check the legal basis in policy.
    - An admission question remains: who is on the actor list of the PID regime? That is a register fact ([Q-22](#q-22)).
    - Positive PID evidence is [F-70](findings.md#f-70), [issue #133](https://github.com/ICTU/GBO-demo/issues/133), and [Q-18](open-questions.md#q-18).
    - Grants carry no properties any more. The demo removed `subject_id_type` ([issue #473](https://github.com/ICTU/GBO-demo/issues/473)).
- **Landed in**: [REQ-74](../requirements/authorization.md#req-74), [ADR 0031](../decisions/0031-regime-from-evidence.md) (supersedes [ADR 0030](../decisions/0030-grant-properties.md)), [F-70](findings.md#f-70).

### Q-16: AuthZEN/OpenFTV conformity: which profile does GBO follow, and is GBO at the working-group table? {#q-16}

- **Status**: answered
- **Question**: Which PEP-PDP profile does GBO follow, and does GBO take part in the OpenFTV working group?
- **Answer**:
    - GBO takes part in the OpenFTV working group and prepares a proposal for a GraphQL profile ([B-02](https://ictu.github.io/GBO-PSA/main/vraagstukken/), [issue #331](https://github.com/ICTU/GBO-demo/issues/331)).
    - The conformity level is the NLGov AuthZEN profile (GO, [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)).
    - The demo conforms on the wire protocol through OpenFTV v0.1.0 ([PR #337](https://github.com/ICTU/GBO-demo/pull/337)). In demo v0.9.0, only the GraphQL mapping is patched.
    - The profile variant and the choice "purist or pragmatic" belong in the proposal.
    - The mapping of DvTP fields onto AuthZEN is the open S05 decision on the definitive GBO profile. [Q-14](open-questions.md#q-14) is input for it.
    - The standardization route for grant properties lapsed ([PR #363](https://github.com/ICTU/GBO-demo/pull/363), [issue #364](https://github.com/ICTU/GBO-demo/issues/364)).
- **Landed in**: [REQ-42](../requirements/authorization.md#req-42), [ADR 0002](../decisions/0002-opa-rego-authzen.md).

### Q-19: Where do adapter parameters come from? Boundary of the thin adapter and catalog coupling {#q-19}

- **Status**: answered
- **Question**: Where do the query parameters that a channel adapter sends to a source come from?
- **Answer**: From the source, for both branches.
    - EUDI: the source publishes the query, the declared parameters, the mapping, the attestation schema, and the offer in `/.well-known/gbo`. GBO validates and activates them ([SL-46](increments.md#sl-46), [PR #224](https://github.com/ICTU/GBO-demo/pull/224)). The adapter has no use-case knowledge. The demo removed the use-case catalog on the GBO side.
    - DvTP: FR-32 (FR-DvTP v0.9) sets up a statutory service catalog with the legal ceiling per use case. The operator of the DvTP service makes the catalog with the sector representative and manages it. The catalog links data sets to service providers and marks each set mandatory, optional, or minimal.
    - [B-03](https://ictu.github.io/GBO-PSA/main/vraagstukken/): content management is federated, and findability is central. For more information, see PSA S07.
    - The consequence is [F-74](findings.md#f-74): DvTP takes the scope from the demand side, and EUDI takes it from the supply side ([issue #382](https://github.com/ICTU/GBO-demo/issues/382)).
- **Landed in**: [REQ-64](../requirements/sources-identity.md#req-64), [REQ-44](../requirements/authorization.md#req-44), [ADR 0016](../decisions/0016-source-owned-metadata.md), [ADR 0008](../decisions/0008-dienstencatalogus-ceiling.md).

### Q-20: SD-JWT VC claim shape for related-person data: flat display strings or structured objects? {#q-20}

- **Status**: closed
- **Question**: Does an attestation carry related-person data (for example, the parents on a death certificate) as flat display strings or as structured claims?
- **Answer**: The question became a schema choice per attestation type. It is no longer a system question.
    - In PSA S11, attestations follow an agreed attestation rulebook and schema.
    - The GO has attestation schemas per use case.
    - The schema comes from the source ([REQ-64](../requirements/sources-identity.md#req-64)).
    - ARF [ARB_30](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#ARB_30) lets the rulebook state the selective disclosure of nested properties and list elements. Each one MUST, MAY, or MUST NOT be selectively disclosable. Issuance must be able to follow the rulebook.
    - [Issue #381](https://github.com/ICTU/GBO-demo/issues/381), row 13, tests nested claims in the NL Wallet.
- **Landed in**: [REQ-78](../requirements/eudi-issuance.md#req-78), [F-47](findings.md#f-47).

### Q-21: Who can manage and publish the policy of a source holder, and how is that authority set federatively? {#q-21}

- **Status**: answered
- **Question**: Who sets the authorization policy for DvTP: a central Policy Authority (FR-39) or the source holder (GO)? Who can manage and publish it?
- **Answer**: Policy management stays with each source holder.
    - PAP and PDP are at the source holder, as the GO says ([issue #426](https://github.com/ICTU/GBO-demo/issues/426), closed as not planned, October 28, 2026).
    - The policy guidelines stay guidelines. They do not become requirements.
    - Publication control is a norm in [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie). It covers the owner, the approver, the effective date, the change history, tests before publication, and an emergency and rollback procedure.
    - The text of FR-39 (central Policy Authority, signed bundles) is outdated. FR-DvTP needs a change to this text.
    - Authority over policy lies with competent public parties ([B-05](https://ictu.github.io/GBO-PSA/main/vraagstukken/)).
- **Landed in**: [ADR 0021](../decisions/0021-central-pap-signed-bundles.md) (rewritten: "Policy management and distribution per source holder"), [RL-01](../requirements/authorization.md#rl-01) to [RL-05](../requirements/authorization.md#rl-05), [F-09](findings-closed.md#f-09), [F-51](findings.md#f-51), [F-52](findings.md#f-52).

### Q-22: Who runs the admission register, on which grounds, and what legal protection has a refused party? {#q-22}

- **Status**: answered
- **Question**: The question has four parts:
    1. Who keeps the admission register?
    2. On which grounds does a party get admission?
    3. What legal protection does a refused party get?
    4. At which granularity is admission given?
- **Answer**:
    - Register: the operator of the DvTP service keeps the register (FR-30, FR-DvTP v0.9). The system framework (FDS gatekeeper, draft) follows from [B-09](https://ictu.github.io/GBO-PSA/main/vraagstukken/).
    - Grounds: [PSA P-16](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) ("objective, proportionate and verifiable; the permitted service, legal basis and data request are registered in advance") and FR-30 (selection criteria, connection conditions).
    - Granularity: per service (P-16, FR-32), through the catalog and the consent registration ([issue #382](https://github.com/ICTU/GBO-demo/issues/382)).
    - Legal protection: procedural, at the management organization and B-09. The technical part is [REQ-63](../requirements/admission.md#req-63).
    - The actor list of the PID regime is a register fact. It must stay disjoint from the DvTP consumers ([REQ-74](../requirements/authorization.md#req-74), [F-70](findings.md#f-70)).
    - Demo gap: FR-30 criterion 3 (status "trusted" visible to the citizen) is missing.
- **Landed in**: [REQ-61](../requirements/admission.md#req-61), [REQ-62](../requirements/admission.md#req-62), [REQ-63](../requirements/admission.md#req-63), candidate [connection conditions](../requirements/admission.md#connection-conditions), [F-55](findings-closed.md#f-55), [F-56](findings-closed.md#f-56), [ADR 0015](../decisions/0015-contract-acceptance-by-policy.md).

### Q-23: Through which interface does a source get the consent status, and how does the register know who asks? {#q-23}

- **Status**: closed
- **Question**: The PDP of a source calls the register for the consent status across an organization boundary. Over which interface does it do this, and how does the register authenticate the caller?
- **Answer**: [PSA S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie) sets the norm: only the citizen and authorized components have access to consent. The interface and the caller identity are a design decision for the GBO team, as builders of the register. The GO gives FSC as the direction. In demo v0.9.0, the status query goes over FSC. Thus the register records the verified FSC peer as the processor in LDV ([issue #383](https://github.com/ICTU/GBO-demo/issues/383)). The trade-off between a query per request and a status list is at [REQ-75](../requirements/consent.md#req-75).
- **Landed in**: [REQ-76](../requirements/consent.md#req-76), [REQ-75](../requirements/consent.md#req-75), [ADR 0032](../decisions/0032-consent-proof.md).

### Q-24: Must a private consumer record its processing according to LDV? {#q-24}

- **Status**: closed
- **Question**: Must a private consumer, which LDV does not bind, record its processing so that a reader can follow a chain from its start?
- **Answer**: The minimum is normative: the consumer sends W3C Trace Context and records the transaction ID. In [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid), every data request gets a request identifier that is usable across the whole chain. Full LDV at the private consumer is a candidate connection condition. FR-31 (FR-DvTP v0.9) puts the chain audit at the service. The LDV records of the status queries at the register form that chain-wide index. This is true only while the PDP calls for the status per request ([REQ-75](../requirements/consent.md#req-75), [F-68](findings.md#f-68)).
- **Landed in**: [AV-01](../requirements/admission.md#av-01) (minimum), [AV-02](../requirements/admission.md#av-02) (full LDV, candidate), [F-68](findings.md#f-68).

