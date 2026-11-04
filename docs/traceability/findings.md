# Findings

A finding records what the demo build showed about the design. A finding
is one of these four types:

- An implicit requirement.
- An assumption that the build made visible.
- A gap.
- An error in a source.

Each finding records four items:

- Its trigger: a [demo increment](increments.md) or a demo PR.
- The observation.
- Why the observation matters for the GO, the PSA, or the FR-DvTP.
- Where it landed: a [requirement](../requirements/index.md), an
  [architecture decision](../decisions/index.md), a risk, or an
  [open question](open-questions.md).

A finding has one of these status values:

- open: the design has no answer to the finding.
- closed: the design or a review answered the finding.
- resolved in demo: the demo changed, and the finding no longer applies.
- superseded.
- premise lapsed.

Finding numbers are never reused. F-01, F-05, F-10, F-12, F-13, F-33, and
F-48 do not exist.

For the open findings per PSA theme, see
[Summary for the PSA](#summary-for-the-psa).

### F-19: The register does not record the consent-use event ("first used"), so the FR-22 usage status cannot be shown {#f-19}

- **Status**: open

The consent detail page shows when the citizen gave a consent, when a
service provider (dienstverlener) first used it, and when it ended. The
consent register (toestemmingsregister) keeps only the start and end dates, so the demo
cannot show the first use. FR-11 and FR-22 require that the register
itself records whether and when data was first retrieved. The open point
is how the register learns of a successful delivery at the source. Three
options exist: the first status lookup by a PDP, a report from the
source after delivery, or derivation from the LDV chain.

??? note "Evidence, impact and proposal"

    - **Type**: capability gap
    - **Trigger**: [SL-06b](increments.md#sl-06b). The consent detail page shows a history with issued, first used, and revoked or expired.
    - **Observation**: the register keeps `created_at` and `valid_until`, but no use event ([`consent-register/main.go#L36-L46`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-register/main.go#L36-L46)). The decision logs hold `consent_id` per allow. These logs are a query log and hold no consent state. The demo shows only issued and revoked or expired.
    - **Why it matters**: FR-11 v0.9 and FR-22 v0.9 require that the consent register records whether and when data was first retrieved. So the first use is a field in the register. The register does not derive it from the audit log. Single use no longer applies ([Q-04](answered-questions.md#q-04)), so this finding does not depend on Q-04 any more.
    - **Proposal**: the open point is how the register learns of a successful delivery at the source. [Q-42](open-questions.md#q-42) gives three options:
        - (A) The first status query by a PDP.
        - (B) A report from the source after delivery. Option B adds an interface per source.
        - (C) Derivation from the LDV chain. Option C depends on [Q-08](open-questions.md#q-08) and [Q-25](open-questions.md#q-25).

        The build choice waits in demo issue [#389](https://github.com/ICTU/GBO-demo/issues/389).

    - **Related**: [REQ-76](../requirements/consent.md#req-76), [REQ-14](../requirements/consent.md#req-14), [Q-42](open-questions.md#q-42), [Q-25](open-questions.md#q-25), [Q-08](open-questions.md#q-08), [F-97](#f-97) (FR-22 to FR-24 name the statuses differently).

### F-47: Wallet credential where the subject of the claim differs from the discloser {#f-47}

- **Status**: open

In the death certificate case, a surviving partner discloses her own PID
and gets a credential about her deceased partner. The source decides
which marriage and partner apply, and the PDP sees only the output
fields, so policy cannot check the relation. The PSA assumes that a
citizen gets credentials about himself or herself only. The proposal is
that the source publishes the relation as filter arguments in its
schema, and policy requires fixed values for them. What a filter cannot
express stays a tested property of the source, marked in its service
description.

??? note "Evidence, impact and proposal"

    - **Type**: implicit requirement / architectural variant
    - **Trigger**: [SL-43](increments.md#sl-43) (death certificate, [PR #125](https://github.com/ICTU/GBO-demo/pull/125)). A surviving partner discloses her own PID and gets a credential about her deceased partner.
    - **Observation**: the query is a source-owned view, `akteVanOverlijden(bsn)`. The source picks the marriage and the deceased partner ([`brp-graphql-server/main.go#L671-L679`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/main.go#L671-L679)). The PDP sees only the flat output fields. It cannot inspect how the source walks the relation ([`eud0002.rego#L7-L11`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0002.rego#L7-L11)).
    - **Why it matters**: the PSA assumes self-disclosure ([PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)). Issuance about a related person changes who can receive a credential about whom. If only the source knows the relation, policy cannot check it.
    - **Proposal**: the rewritten [REQ-57](../requirements/eudi-issuance.md#req-57) takes this approach:
        - The preferred option: the source publishes the relation as filter arguments in its schema.
        - Policy then requires the path and the filters with fixed values, without looking at the content. The iWlz network model works this way.
        - What a filter cannot express stays a tested invariant of the source. The service description marks it. Demo issue [#425](https://github.com/ICTU/GBO-demo/issues/425) holds the test (not built).
        - Authorized representatives are out of scope. A mandate is representation, not a registration fact (PSA B-19).
    - **Related**: [REQ-57](../requirements/eudi-issuance.md#req-57), [REQ-116](../requirements/eudi-issuance.md#req-116), [AV-10](../requirements/admission.md#av-10), [AV-11](../requirements/admission.md#av-11), [Q-14](open-questions.md#q-14), [Q-20](answered-questions.md#q-20), [F-57](#f-57).

### F-51: The PDP protects its own management endpoints with the decision policy {#f-51}

- **Status**: open

The PDP protects its own management endpoints with the policy that
decides on requests for citizen data. That policy refuses everything
except GBO data requests, so a push of policy bundles from the PAP
fails. The demo therefore lets the PDP pull its bundles at start-up,
which meets the PSA. The weak point is in the implementation: every rule
that allows management sits in the policy for citizen data. The proposal
is a separate authorization path for management, as a guideline for
bronhouders, because each source keeps its own PAP and PDP.

??? note "Evidence, impact and proposal"

    - **Type**: exposed design choice (management plane versus decision plane)
    - **Trigger**: [SL-44](increments.md#sl-44) tried to push bundles from the PAP to the PDP.
    - **Observation**:
        - The PDP authorizes its own management endpoints with the policy set that decides data requests (`package authz`).
        - That policy refuses anything that is not a GBO data request, so a push gets 403.
        - For push to work, the decision policy needs a rule that opens the management API of the PDP. The demo therefore pulls at start-up (`targets: []`, [`gbo-pdp.yaml#L18-L32`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/bundles/gbo-pdp.yaml#L18-L32)).
        - While its policy store is empty, the engine also installs a no-auth mode.
        - On the Manager side, the bundle pull needs its own Cedar policy since OpenFTV v0.1.0 ([`pdp-bundle.cedar`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/authz/pdp-bundle.cedar)).
    - **Why it matters**: every rule that allows management sits in the policy that decides on citizen data. Pull meets [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie), which asks only that a component reliably gets a valid policy version. The GO and the PSA have no gap here. The gap is in the implementation.
    - **Proposal**: a PDP needs a separate authorization path for management. Then push works without a wider decision policy ([RL-02](../requirements/authorization.md#rl-02)). The point was reported to the OpenFTV maintainers. [Q-21](answered-questions.md#q-21) keeps PAP and PDP at each source. RL-02 therefore stays a guideline for bronhouders and is no requirement.
    - **Related**: [RL-02](../requirements/authorization.md#rl-02), [F-09](findings-closed.md#f-09), [F-52](#f-52), [Q-21](answered-questions.md#q-21), [ADR-0021](../decisions/0021-central-pap-signed-bundles.md).

### F-52: The policy store is cumulative and cannot delete, and one duplicate package breaks every decision {#f-52}

- **Status**: open

The PDP compiles all its policies as one set. In the demo, one stale
policy with a duplicate package name made every request fail with a
server error instead of a deny. The policy store also cannot delete a
policy, so an operator can only retire it. Faults of the same class came
back three times, for example a policy that did not compile but showed
as loaded. The proposal is to validate a policy set before activation
and to fall back visibly to the last valid set, as the PSA asks.

??? note "Evidence, impact and proposal"

    - **Type**: gap (availability and lifecycle)
    - **Trigger**: [SL-44](increments.md#sl-44) ([PR #208](https://github.com/ICTU/GBO-demo/pull/208)). A stale policy declared the same Rego package as an existing rule.
    - **Observation**:
        - The PDP compiles the policy set as a whole. One bad module caused HTTP 500 on every request. The PDP returned no deny.
        - Upstream, a delete fails on a foreign key to the audit trail. The way out is to retire the policy: remove the bundle tag ([`seed-openftv-manager.py#L116-L122`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/scripts/seed-openftv-manager.py#L116-L122)).
        - The same class of fault came back three times:
            - Non-Rego files silently dropped policies ([PR #228](https://github.com/ICTU/GBO-demo/pull/228)).
            - A PDP looked healthy but got 403 on every bundle fetch ([PR #337](https://github.com/ICTU/GBO-demo/pull/337)).
            - A module that does not compile is reported as loaded, while the old policy keeps deciding (demo issue [#151](https://github.com/ICTU/GBO-demo/issues/151)).
        - As a local safety net, `make policy-check` runs before every PDP start ([PR #372](https://github.com/ICTU/GBO-demo/pull/372), [`Makefile#L92`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L92)). Reconciliation with git is built. Validation and fallback at activation are not built.
    - **Why it matters**: the policy set is one availability object. One bad rule affects the whole authorization decision. [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie) sets the norm: tests before publication, a controlled fallback, and a rollback procedure. Source metadata already has this lifecycle ([F-59](findings-closed.md#f-59)).
    - **Proposal**: [RL-04](../requirements/authorization.md#rl-04) (retire, reconcile) and [RL-05](../requirements/authorization.md#rl-05) (validate before activation, visible fallback to the last valid set). The point was reported to the OpenFTV maintainers. [Q-21](answered-questions.md#q-21) puts PAP and PDP at each source. Bundle scoping per policy owner therefore matters only where sources share a PDP.
    - **Related**: [RL-04](../requirements/authorization.md#rl-04), [RL-05](../requirements/authorization.md#rl-05), [REQ-66](../requirements/sources-identity.md#req-66), [F-09](findings-closed.md#f-09), [F-51](#f-51), [F-59](findings-closed.md#f-59), [Q-21](answered-questions.md#q-21), [ADR-0021](../decisions/0021-central-pap-signed-bundles.md).

### F-54: Log masking in the policy engine is inert, so the BSN-free decision log depended on input construction {#f-54}

- **Status**: open

The policy engine loads a masking rule for its decision log but never
applies it, so BSN values reached the log in clear text. The demo then
replaced the BSN with a pseudonym in the PDP input, until it removed
that step on purpose. In demo v0.9.0, the EUDI and ASI routes put the
plain BSN in the PDP input and in the logs. The proposal keeps
identifiers out of the PDP input when the input is built. Masking stays
allowed only as a second line, with a continuous test on real log
output.

??? note "Evidence, impact and proposal"

    - **Type**: replaced assumption
    - **Trigger**: the harvest of [SL-44](increments.md#sl-44). The masking rule from [SL-29](increments.md#sl-29) did not exist any more.
    - **Observation**:
        - In the OpenFTV PDP, a `system.log` masking rule loads. The decision-log plugin never applies it (demo issue [#149](https://github.com/ICTU/GBO-demo/issues/149)). Values reached Loki in clear text. Bundle distribution does not change this.
        - The PDP mapper then carried the guarantee: it turned the wallet BSN into a PI before evaluation.
        - [PR #370](https://github.com/ICTU/GBO-demo/pull/370) removed that step on purpose. In demo v0.9.0, the EUDI and ASI routes put the plain BSN in the PDP input, the ADL, and the console log ([`CHANGELOG.md#L598-L602`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/CHANGELOG.md#L598-L602)). The DvTP path carries only a placeholder.
    - **Why it matters**: [PSA P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) and [S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid) ask for minimal logging. From the outside, a masking rule that does not work looks the same as one that works. The EUDI and ASI routes do not meet REQ-60.
    - **Proposal**: demo issue [#368](https://github.com/ICTU/GBO-demo/issues/368) decides between masking and transforming first. [REQ-60](../requirements/logging-audit.md#req-60) prefers minimization at input construction. Masking is allowed only as a second line, with a continuous test on real log output. [ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md) (proposed) records this choice.
    - **Related**: [REQ-60](../requirements/logging-audit.md#req-60), [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-71](../requirements/logging-audit.md#req-71), [F-37](findings-closed.md#f-37), [F-30](findings-closed.md#f-30), [ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md).

### F-57: The source owns its service description, and GBO validates and activates it {#f-57}

- **Status**: open

Each source publishes one service description that names its data
service, query, parameters, mapping, attestation schema, and offer. GBO
finds the source through its valid contracts, validates the description,
and activates it in one step. The issuance configuration and the offers
in the frontend come from this description, so a source can join without
a change in GBO code. For the EUDI branch, this design gives the GO
service catalogue a concrete form, which the bronhouder manages with a
common profile. Three points stay open: a link to the DCAT-AP-NL
description, central findability, and a conflict with the wish for no
fixed DvTP queries.

??? note "Evidence, impact and proposal"

    - **Type**: directional design choice
    - **Trigger**: [SL-46](increments.md#sl-46) ([PR #219](https://github.com/ICTU/GBO-demo/pull/219), [PR #224](https://github.com/ICTU/GBO-demo/pull/224)). Before this demo increment, every added source, attestation type, or year needed a change in GBO code or in a GBO catalog file.
    - **Observation**:
        - Each source publishes one document at `/.well-known/gbo` ([`source_configuration.go#L15`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_configuration.go#L15)). The document holds the data service name, endpoint, query, parameters, mapping, attestation schema, and offer.
        - The reconciler finds sources through valid contracts. It validates schema, origin, version, validity, and contract binding. Then it activates the document atomically.
        - The issuance configuration and the frontend offers are generated from this document.
        - Two sources (BD, BRP) use the same path, without fallback.
    - **Why it matters**: the GO has two catalogs: a data catalog that follows DCAT-AP-NL, and a service catalog. The service catalog lists the allowed data requests. It is "managed federatively with a common profile and central findability", and the bronhouder manages it ([GO §6](https://ictu.github.io/GBO-GO/main/#6-impact-op-betrokken-partijen)). `/.well-known/gbo` is that service catalog, and the validation profile of the reconciler is the common profile. This design gives [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) a concrete form. It answers [Q-19](answered-questions.md#q-19) for the EUDI branch.
    - **Proposal**: keep [REQ-64](../requirements/sources-identity.md#req-64). Three points stay open:
        1. The description does not refer to the DCAT-AP-NL description of the data set or data service. This point is an addition to REQ-64.
        2. Central findability is missing. It belongs with the catalog of the management organization.
        3. "Allowed data requests per application" conflicts with the wish for no fixed DvTP queries ([Q-14](open-questions.md#q-14)).

        The demo proves the approach on the EUDI branch. [F-74](#f-74) covers DvTP. Semantics stay out of scope: a source-owned mapping is not a canonical model ([Q-11](answered-questions.md#q-11)). The form of the document is the input of the demo to the open PSA S10 decision.

    - **Related**: [REQ-64](../requirements/sources-identity.md#req-64), [REQ-65](../requirements/sources-identity.md#req-65), [REQ-66](../requirements/sources-identity.md#req-66), [AV-07](../requirements/admission.md#av-07), [F-21](findings-closed.md#f-21), [F-23](findings-closed.md#f-23), [F-71](#f-71), [F-74](#f-74), [Q-11](answered-questions.md#q-11), [Q-14](open-questions.md#q-14), [Q-19](answered-questions.md#q-19), [Q-38](open-questions.md#q-38), [ADR-0016](../decisions/0016-source-owned-metadata.md).

### F-68: A chain read goes forward only, and in DvTP the chain starts at a party that LDV does not bind {#f-68}

- **Status**: open

A chain read in LDV starts at the party that started the processing and
follows pointers forward to each next logbook. In DvTP, a private
consumer starts the processing, and LDV does not bind that party, so
nobody knows which sources one processing touched. The PDP at the source
also writes only decision records, so no record at the source points to
the consent logbook. The proposal uses the consent register as an
index: every retrieval leads to a status lookup there, and the register
logs each lookup. The step from the source to the register is open with
Logius.

??? note "Evidence, impact and proposal"

    - **Type**: design gap
    - **Trigger**: demo issue [#365](https://github.com/ICTU/GBO-demo/issues/365). The chain view in the developer portal knew a chain only because all logbooks were in its configuration. No record in the DvTP flow carried `dpl.read.nextLogbookId`.
    - **Observation**:
        - The LDV read extension always starts at the application that started the processing. From there, it follows `nextLogbookId`. A caller of another party records the read API of that party. `dpl.core.foreign_operation.processor` names the caller, but it gives no route back.
        - Point 1 is the start of the chain. In DvTP, a private consumer starts the processing. LDV is meant for organizations with a public task. Without the records of the consumer, no one knows which sources one processing touched.
        - Point 2 is the step from the source to the register. The PDP at the source does the status lookup. A PDP writes ADL records only ([F-63](findings-closed.md#f-63)). The ADL has no equivalent of `nextLogbookId`, so no record at the source points to the consent logbook.
        - In demo v0.9.0 ([PR #366](https://github.com/ICTU/GBO-demo/pull/366)), the consumer has its own logbook with `nextLogbookId` per source call. The chain view starts at the start logbooks and follows the pointers. It shows the consent logbook as "reached without pointer".
    - **Why it matters**: [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid), FR-20, and FR-31 ask for a chain audit and citizen access. If nobody can follow a chain, nobody can audit it.
    - **Proposal**:
        - Point 1 has an outcome without the private consumer. FR-31 v0.9 puts the chain audit at the facility. Every retrieval at any source leads to a status lookup at the register, with trace, `consent_id`, and consumer. The register logs each lookup as an LDV processing.
        - As long as the status is fetched per request, these records form a chain-wide index ([REQ-75](../requirements/consent.md#req-75)). Since demo issue [#383](https://github.com/ICTU/GBO-demo/issues/383), the caller of the lookup is verified over FSC ([REQ-76](../requirements/consent.md#req-76)).
        - From the consumer, the minimum is trace context ([AV-01](../requirements/admission.md#av-01)). LDV for the consumer is a candidate ([AV-02](../requirements/admission.md#av-02)). [Q-24](answered-questions.md#q-24) is closed.
        - Point 2 is open with Logius: [Q-25](open-questions.md#q-25).
        - [REQ-64](../requirements/sources-identity.md#req-64): if the source does not publish its read API, a caller cannot fill `nextLogbookId`.
    - **Related**: [F-65](findings-closed.md#f-65), [F-76](#f-76), [REQ-72](../requirements/logging-audit.md#req-72), [REQ-75](../requirements/consent.md#req-75), [REQ-76](../requirements/consent.md#req-76), [AV-01](../requirements/admission.md#av-01), [AV-02](../requirements/admission.md#av-02), [Q-24](answered-questions.md#q-24), [Q-25](open-questions.md#q-25), [ADR-0026](../decisions/0026-ldv-integration.md), [ADR-0036](../decisions/0036-adl-decision-record.md).

### F-70: The regime follows from the proof, but only consent is positive proof: the PID regime comes from not sending something {#f-70}

- **Status**: open

The PDP picks the rules from the evidence in a request. A consent proof
is positive evidence: it is signed, and the PDP checks it. The PID regime
has no evidence of its own. A request ends up there because it carries no
consent proof. So the only guard on that regime is a short list of
callers, and the adapter does not check who calls it. The design needs a
verified PID as positive evidence for this regime.

??? note "Evidence, impact and proposal"

    - **Type**: exposed design choice and design gap
    - **Trigger**: [PR #363](https://github.com/ICTU/GBO-demo/pull/363) (closes demo issue [#334](https://github.com/ICTU/GBO-demo/issues/334)) removed `flow` as a grant property and as authorization input. [PR #370](https://github.com/ICTU/GBO-demo/pull/370) and [PR #371](https://github.com/ICTU/GBO-demo/pull/371) completed the change: the policy reads the proof itself.
    - **Observation**:
        - One signal sets the regime: a consent token in the request, verified or not. With a token, the consent regime applies. Without one, the PID regime applies ([`engine.rego#L168-L175`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L168-L175)). The policy ignores a `pip.consent` that comes from outside.
        - A request cannot carry evidence for both regimes. For this reason, the earlier `AMBIGUOUS_EVIDENCE` rule is gone. The deny reason comes from the rule that got furthest through its own steps.
        - The only control on the PID regime is the list of designated issuers per EUDI rule ([`eudi_helper.rego#L13-L24`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eudi_helper.rego#L13-L24)). If a consumer OIN is on that list, that consumer can skip consent by leaving out the token.
        - A test requires the issuer list to be disjoint from the DvTP consumers ([`engine_test.rego#L371`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L371)). The test knows only the local consumers. The simulation consumer (`0000009950HYPBV00000`) is not in the test. For that consumer, disjointness rests on inspection, and no test covers it.
        - The PID step checks only that there is no consent token and that the query names a citizen. A comment in the code says so: "The PID itself is not verified here; the adapter trusts the disclosure." The adapter does not authenticate the callback from the issuance server (demo issue [#133](https://github.com/ICTU/GBO-demo/issues/133), open).
    - **Why it matters**: the DvTP regime rests on a signed artifact that the PDP verifies ([REQ-68](../requirements/consent.md#req-68)). The EUDI regime rests on an identifier whose origin no one in the chain checks. The design must say what the evidence for the EUDI legal basis is. If it does not, the regime stays defined as "no consent proof". Since PR #363, a place on the PID actor list is an admission decision with authorization weight ([Q-22](answered-questions.md#q-22)).
    - **Proposal**: [REQ-74](../requirements/authorization.md#req-74) and [ADR-0031](../decisions/0031-regime-from-evidence.md) record the choice. The structural fix is positive PID evidence. That evidence is made where the wallet presentation is verified, and it is bound to the subject of the source query ([REQ-45](../requirements/eudi-issuance.md#req-45), demo issues [#133](https://github.com/ICTU/GBO-demo/issues/133) and [#381](https://github.com/ICTU/GBO-demo/issues/381)). [Q-18](open-questions.md#q-18) covers the legal status of the BSN from the PID. Until then, test the disjointness in each environment as well as locally.
    - **Related**: [F-62](findings-closed.md#f-62), [F-90](findings-closed.md#f-90), [REQ-45](../requirements/eudi-issuance.md#req-45), [REQ-48](../requirements/authorization.md#req-48), [REQ-68](../requirements/consent.md#req-68), [REQ-74](../requirements/authorization.md#req-74), [Q-15](answered-questions.md#q-15), [Q-18](open-questions.md#q-18), [Q-22](answered-questions.md#q-22), [ADR-0031](../decisions/0031-regime-from-evidence.md).

### F-71: A source without its own metadata endpoint: the operator takes over its service description {#f-71}

- **Status**: open

Some sources publish only their data service and no service description
of their own. For such a source, the demo lets the operator keep the
description in a directory. The operator then decides the query, the
mapping, and the wallet claims for the product of another party. Four
bounds stay in place, among them the pinned contract and the check of
the OIN against the certificate. The design allows this only as an
exception, with the recorded agreement of the bronhouder as first
condition, and that condition is not built.

??? note "Evidence, impact and proposal"

    - **Type**: exposed design choice (exception to [F-57](#f-57))
    - **Trigger**: [PR #318](https://github.com/ICTU/GBO-demo/pull/318). An external source in the simulation published only its GraphQL service on FSC. It did not publish `/.well-known/gbo`. With one transport for both legs, the demo had no way to connect such a source.
    - **Observation**:
        - In demo v0.9.0, metadata and data each have their own transport. A `file` transport reads the description from a directory that the operator keeps ([`reconcile_command.go#L192`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/reconcile_command.go#L192), `--metadata-dir`). The registry reports per leg whether its transport is authenticated.
        - The demo README states this openly. The operator who keeps the file takes over the description of the product of another party. That operator must record who agreed to it ([`source-metadata/README.md#L17-L22`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/source-metadata/README.md#L17-L22)).
        - Four bounds stay in place:
            - the peer ID from the own configuration
            - the grant hash that pins the contract
            - the OIN check against the certificate
            - promotion as a separate step
    - **Why it matters**: [F-57](#f-57) and [REQ-64](../requirements/sources-identity.md#req-64) put the description at the source ([PSA P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)). Whoever controls the document decides the query, the mapping, and the wallet claims. With `file` transport, the operator controls the document. The origin check then falls back to the OIN in the certificate.
    - **Proposal**: the design is in [REQ-64](../requirements/sources-identity.md#req-64), as an exception clause, and in [AV-08](../requirements/admission.md#av-08). Its first condition is the recorded agreement of the bronhouder. That condition is not built. Demo issue [#221](https://github.com/ICTU/GBO-demo/issues/221) (open) covers the trust model per transport, including an unsecured variant. According to the [Q-06](answered-questions.md#q-06) review, this is no governance question.
    - **Related**: [F-57](#f-57), [F-58](findings-closed.md#f-58), [REQ-64](../requirements/sources-identity.md#req-64), [REQ-65](../requirements/sources-identity.md#req-65), [AV-08](../requirements/admission.md#av-08), [Q-06](answered-questions.md#q-06), [ADR-0016](../decisions/0016-source-owned-metadata.md).

### F-72: The decision record can carry only what the consumer also gets to see {#f-72}

- **Status**: open

The ADL is the audit record of every decision. It stores the answer that
the PDP gives to the consumer, and nothing else. That answer is
deliberately coarse, so the ADL is coarse too: it holds no reason per
field and no consent status. A supervisor can therefore reconstruct only
what the consumer was allowed to know, and nobody can replay a decision
from the record.

??? note "Evidence, impact and proposal"

    - **Type**: exposed design choice
    - **Trigger**: [PR #373](https://github.com/ICTU/GBO-demo/pull/373) (closes demo issue [#332](https://github.com/ICTU/GBO-demo/issues/332)) made the ADL the audit source. The change had to choose how decision detail gets into the ADL.
    - **Observation**:
        - OpenFTV reads only `allow` and `reason` from the policy. `reason` becomes `reason_user.en` in the AuthZEN answer. The ADL stores that answer unchanged ([`policies/authz.rego#L42-L48`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/authz.rego#L42-L48)). Per-field detail and the step trace are only in the console log of the engine, and that log is observability.
        - Detail in `reason_admin` does not solve this. The FSC Inway returns the reason to the consumer, so everything in it reaches a private party. Since [PR #375](https://github.com/ICTU/GBO-demo/pull/375), the service provider backend filters which reason code the citizen sees. In demo v0.9.0, the Inway drops the reason (OpenFSC #308).
        - The ADL records show `policies: 0`, so they hold no policy version ([REQ-59](../requirements/logging-audit.md#req-59)).
        - Behind the Inway, the ADL record has its own trace and no `adl.fsc.transaction_id` (demo issue [#369](https://github.com/ICTU/GBO-demo/issues/369), open).
    - **Why it matters**: in this design, the AuthZEN answer is both the audit record and the error message to the consumer. What a supervisor must reconstruct is then limited to what the consumer is allowed to know ([PSA P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid), FR-31). Since [PR #371](https://github.com/ICTU/GBO-demo/pull/371), the policy fetches the consent status during evaluation. If the record does not hold that answer, nobody can replay the decision ([F-61](findings-closed.md#f-61)).
    - **Proposal**: ADL 1.0.0 already has a channel next to the answer. ADL does not ask for per-field detail. It replays a decision from the request, policy, information, and configuration, and it prefers references to copies. Ask OpenFTV to fill `adl.core.policies` (`0` in demo v0.9.0), `adl.core.information` (the consent register answer), and, where possible, `adl.core.configuration`. [REQ-71](../requirements/logging-audit.md#req-71) holds the corrected requirement. Personal data in the record (demo issue [#368](https://github.com/ICTU/GBO-demo/issues/368)) is a separate point (see [ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md)).
    - **Related**: [F-53](findings-closed.md#f-53), [F-54](#f-54), [F-61](findings-closed.md#f-61), [F-63](findings-closed.md#f-63), [REQ-06](../requirements/authorization.md#req-06), [REQ-59](../requirements/logging-audit.md#req-59), [REQ-71](../requirements/logging-audit.md#req-71), [Q-08](open-questions.md#q-08), [ADR-0036](../decisions/0036-adl-decision-record.md), [ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md).

### F-74: DvTP scope comes from the demand side, EUDI scope from the supply side, and the intersection is what is technically allowed {#f-74}

- **Status**: open

For EUDI, the source publishes its offer, and GBO validates and
activates it. For DvTP, FR-32 describes a statutory service catalogue
that sets a legal ceiling per use case, from the demand side. What a
DvTP consumer can request is the intersection of the source offer and
that ceiling, and no GO, PSA, or FR text names it. In the demo, the DvTP
scopes are spread over policy, portal, and field map. The proposal is
one DvTP catalogue as the single source for scopes, fields, and portal
text, with a check of the intersection at activation.

??? note "Evidence, impact and proposal"

    - **Type**: exposed design choice
    - **Trigger**: a review of [Q-19](answered-questions.md#q-19) against FR-DvTP v0.9 (September 16, 2026).
    - **Observation**:
        - For EUDI, the source publishes its offer, and GBO validates and activates it ([F-57](#f-57), [REQ-64](../requirements/sources-identity.md#req-64)).
        - For DvTP, FR-32 v0.9 describes a statutory service catalogue. Per use case, the catalogue sets the legal ceiling of what can be requested. The sector need defines the catalogue, and the operator of the DvTP facility keeps it. Data sets link to service providers. Each data set is marked mandatory, optional, or minimal.
        - FR-38 v0.9, criterion 5, limits the scope of a request to that ceiling. The demand side is therefore normative.
        - In the demo, the DvTP scopes are spread over policy, portal, and field map ([F-17](findings-closed.md#f-17)).
    - **Why it matters**: what a DvTP consumer can request is the intersection of the source offer (its schema, [Q-14](open-questions.md#q-14)) and the legal ceiling per use case. [REQ-64](../requirements/sources-identity.md#req-64) covers only the supply side. No GO, PSA, or FR text names the intersection ([PSA S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus), B-03, FR-10 v0.9).
    - **Proposal**: one DvTP catalogue per FR-32, as the single source for scopes, fields, portal text, and the link to service providers. At activation, an intersection check runs. Demo issue [#382](https://github.com/ICTU/GBO-demo/issues/382) (open) and [REQ-121](../requirements/consent.md#req-121) cover this proposal. A schema with enforceable filters (demo issue [#425](https://github.com/ICTU/GBO-demo/issues/425)) is one form for the ceiling ([Q-14](open-questions.md#q-14)). The intersection is a proposal for the GO (PSA B-03).
    - **Related**: [F-17](findings-closed.md#f-17), [F-47](#f-47), [F-57](#f-57), [F-78](#f-78), [REQ-10](../requirements/consent.md#req-10), [REQ-64](../requirements/sources-identity.md#req-64), [REQ-121](../requirements/consent.md#req-121), [Q-14](open-questions.md#q-14), [Q-19](answered-questions.md#q-19), [Q-45](open-questions.md#q-45), [ADR-0008](../decisions/0008-dienstencatalogus-ceiling.md).

### F-75: The BSNk design fits the specification, but the consent facility can fetch the values only as a recognized party {#f-75}

- **Status**: open

BSNk polymorphic pseudonymization is mandatory for DvTP. A check against
the BSNk specifications showed that the design fits on five points and
keeps BSNk out of the request path. One point does not fit: only a
recognized BSNk party can activate and transform values. The citizen
logs in at MijnOverheid before the sources are known, so the login
cannot deliver the values. The remaining work is administrative and
legal: the consent facility (toestemmingsvoorziening) must become a recognized party, and someone
must decide who the BSNk participant is.

??? note "Evidence, impact and proposal"

    - **Type**: assumption (checked), with one gap
    - **Trigger**: the BSNk technical specifications v11.2 (December 2025) and the decryption component documentation, read next to the design in demo issue [#364](https://github.com/ICTU/GBO-demo/issues/364) (September 30, 2026).
    - **Observation**:
        - Five parts of the design fit the specification:
            - An encrypted value per party in the proof is the recipient-specific BSNk form, per OIN ([BSNK-07](../requirements/pseudonymization.md#bsnk-07)).
            - The choice between identity and pseudonym by authorization is a lookup in the BSN authorization list (Autorisatielijst BSN) ([BSNK-06](../requirements/pseudonymization.md#bsnk-06)).
            - Transformation happens when the citizen gives consent, the only time when BSNk allows it ([BSNK-04](../requirements/pseudonymization.md#bsnk-04)).
            - Local decryption at the source, after the PDP, is what every BSNk recipient does ([BSNK-09](../requirements/pseudonymization.md#bsnk-09)).
            - The design makes no BSNk call at query time, so BSNk stays out of the query path.
        - One part does not fit: only a recognized party is allowed to activate and transform ([BSNK-01](../requirements/pseudonymization.md#bsnk-01)). The login cannot deliver the values, because the citizen logs in at MijnOverheid before the sources are known.
        - Three earlier assumptions were wrong:
            - A polymorphic identity is specific to the requester, not to the recipient ([BSNK-03](../requirements/pseudonymization.md#bsnk-03)).
            - The closing key comes from BSNk, not from the recipient.
            - PI and PP do not have the same starting point.
        - The demo built three parts on the BSNk mock ([SL-51](increments.md#sl-51), [PR #469](https://github.com/ICTU/GBO-demo/pull/469), [PR #477](https://github.com/ICTU/GBO-demo/pull/477)):
            - an encrypted pseudonym for every source
            - an encrypted identity only for a source on the BSN authorization list
            - requests of at most four parties ([BSNK-05](../requirements/pseudonymization.md#bsnk-05))
        - The spike on the real BSNk PP (demo issue [#377](https://github.com/ICTU/GBO-demo/issues/377)) closed on October 21, 2026. Its result: the mock follows the BSNk interface and rules. Real activation, transport, key handling, and the agreement for private recipients wait for pre-production access.
    - **Why it matters**: [PSA P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie), B-07, and GO §5 make BSNk PP mandatory for DvTP. Nothing technical blocks the design. The remaining work is administrative and legal. The consent facility must become a recognized BSNk party, in a role that BSNk was not written for.
    - **Proposal**: use [BSNK-01 to BSNK-11](../requirements/pseudonymization.md#bsnk-preconditions) as the check for each build step and for the trial with the real BSNk PP. Submit the recognition question ([Q-26](open-questions.md#q-26)). Decide who the BSNk participant is ([Q-49](open-questions.md#q-49), [ADR-0040](../decisions/0040-route-d-citizen-recognition.md), proposed). Two points stay open in the demo: a pseudonym for the consumer (demo issue [#478](https://github.com/ICTU/GBO-demo/issues/478)), and how the BSN authorization list is delivered in practice ([Q-26](open-questions.md#q-26)).
    - **Related**: [F-76](#f-76) to [F-79](#f-79), [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-69](../requirements/pseudonymization.md#req-69), [REQ-80](../requirements/pseudonymization.md#req-80), [Q-01](open-questions.md#q-01), [Q-26](open-questions.md#q-26), [Q-49](open-questions.md#q-49), [ADR-0005](../decisions/0005-bsnk-pp.md), [ADR-0040](../decisions/0040-route-d-citizen-recognition.md).

### F-76: The consumer has no citizen identifier, so what it records about "this person" depends on the consent {#f-76}

- **Status**: open

The service provider never learns who the citizen is. It holds a consent
proof and names the citizen with a placeholder. This goes further than
"no BSN for private parties", and it has side effects. The service provider
logs under the consent ID, so one citizen with two consents is two
people in its logbook. It cannot tell that two consents come from the
same person, and it can answer a request for access only through the
consents.

??? note "Evidence, impact and proposal"

    - **Type**: exposed design choice
    - **Trigger**: [SL-51](increments.md#sl-51) ([PR #469](https://github.com/ICTU/GBO-demo/pull/469)). The proof carries an encrypted identity per source instead of a PI. The consumer cannot read it. A pseudonym of its own (VP) for the consumer is optional in the design. It is not built (demo issue [#478](https://github.com/ICTU/GBO-demo/issues/478)).
    - **Observation**:
        - The consumer reads only `consent_id` and `scopes` from the proof. It names the subject with a placeholder.
        - Its logbook names the data subject by the consent ID, under the subject type `consent-id` ([`logbook.go#L22`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/logbook/logbook.go#L22)).
        - In one query chain, the same citizen is `c-…` at the consumer, `LP-…` at the source, and `EP-…` at the consent register (seen in the running demo, September 30, 2026).
    - **Why it matters**: [PSA P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) says "BSN-free for private consumers". This design goes further: the consumer is identifier-free. The design does not name three effects of this choice:
        1. Logging: [REQ-72](../requirements/logging-audit.md#req-72) asks for a pseudonym from the own space of the controller. The consumer has none. A consent ID is no pseudonym. One citizen with two consents is two data subjects in the consumer logbook.
        2. Access: if a citizen asks the consumer what it processed about them, the consumer can find that citizen only through their consents. The consent register translates the citizen to consents (FR-31, [F-68](#f-68)).
        3. Recognition: through GBO, the consumer cannot tell that two consents are from the same person. That is data minimization ([PSA P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)), but it is a design choice. With a VP, the consumer can tell, and it then has a pseudonym to log under.
    - **Proposal**: add a rule to [REQ-72](../requirements/logging-audit.md#req-72) for a party without an identifier of the data subject. That party logs under the reference to the legal basis, with its own `data_subject_id_type`. Submit the question whether that rule fits LDV ([Q-27](open-questions.md#q-27)). Make "VP for the consumer or not" an explicit design choice, with these three effects ([Q-01](open-questions.md#q-01)).
    - **Related**: [F-69](findings-closed.md#f-69), [F-75](#f-75), [F-77](#f-77), [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-72](../requirements/logging-audit.md#req-72), [AV-02](../requirements/admission.md#av-02), [Q-01](open-questions.md#q-01), [Q-27](open-questions.md#q-27).

### F-77: The PDP checks that the subject comes from the proof, and no longer who the subject is {#f-77}

- **Status**: open

The PDP used to compare the citizen in the query with the citizen in the
consent. Now the query carries a placeholder, and the proof carries a
value that the PDP cannot read. The PDP checks only that the citizen
comes from the proof. A rule can therefore never depend on a property of
the citizen, and one request can be about one citizen only.

??? note "Evidence, impact and proposal"

    - **Type**: exposed design choice (replaces the subject binding of the removed REQ-27)
    - **Trigger**: [SL-51](increments.md#sl-51) ([PR #469](https://github.com/ICTU/GBO-demo/pull/469)). Before this demo increment, the policy compared the PI in the query with the PI in the proof. After it, the query has a placeholder, and the proof has a value that the PDP cannot read.
    - **Observation**:
        - Since [PR #476](https://github.com/ICTU/GBO-demo/pull/476), two placeholders exist, one for each form that an API takes: `consent:identity` (the BSN) and `consent:pseudonym` (the source's own pseudonym) ([`lib.rego#L49-L53`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L49-L53)). Each rule names the placeholders that it accepts. The PDP denies any other value with `CONSTRAINT_MISMATCH`, before the request reaches the source.
        - Without a verified proof, a placeholder stands for nobody. A value from the request itself does not change that.
        - The PDP denies a literal BSN with `CONSTRAINT_MISMATCH`, also when the proof is valid.
        - The PDP sees only the placeholder in the query.
    - **Why it matters**: the binding of the query to the legal basis ([PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)) changed from a comparison into a construction. The only subject that the source can fill in is the subject from the proof. This change has four effects:
        1. The PDP has no subject-dependent policy, because it does not know who the person is. If a policy depends on a property of the citizen, it must get that property from the proof. Otherwise it must run at the source after the substitution.
        2. A request has one subject: one placeholder per form and one citizen per consent. A question about two persons (partner, child) does not fit. This point stays open. Demo issue [#473](https://github.com/ICTU/GBO-demo/issues/473) closed without a solution for it.
        3. Substitution works only on variables. If the query text holds a literal placeholder, that placeholder passes the PDP, and nothing replaces it. This fails closed: the source finds no one.
        4. The decision log has no identifier, but it holds the proof with the encrypted value. In the demo, that value is readable because the mock does not encrypt (demo issue [#368](https://github.com/ICTU/GBO-demo/issues/368)).
    - **Proposal**: [REQ-79](../requirements/pseudonymization.md#req-79) holds the requirement. Record in [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md) that, under a consent, the binding is the rule "the subject comes from the proof". The binding is no comparison of identifiers. Point 2 needs a design decision.
    - **Related**: [F-44](findings-closed.md#f-44), [F-76](#f-76), [F-79](#f-79), [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-79](../requirements/pseudonymization.md#req-79), [REQ-80](../requirements/pseudonymization.md#req-80), [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md).

### F-78: The proof freezes at consent: parties, key versions, and proof form are fixed for the whole validity period {#f-78}

- **Status**: open

At consent, the portal makes an encrypted value for each source, with
the OIN and the key version of that source. The consent proof therefore
fixes the parties, the key versions, the BSN authorization, and the
proof form for its whole validity period. An added party needs another
consent from the citizen. A changed OIN or proof form can break
outstanding proofs, and a consent can be valid for months. The proposal
adds the OIN, the key version, and the BSN authorization per party to
the service catalogue, and gives the proof a version.

??? note "Evidence, impact and proposal"

    - **Type**: design gap
    - **Trigger**: [SL-51](increments.md#sl-51) ([PR #469](https://github.com/ICTU/GBO-demo/pull/469)). To make the values, the portal must know an OIN and a key version per source. No part of the chain holds these values, so they became configuration.
    - **Observation**:
        - The portal gets the sources as `<OIN>@<key set version>` from an environment variable. Without at least one source, the portal gives no consent ([`consent-portal-backend/main.go#L154-L173`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/main.go#L154-L173)).
        - The source keeps its keys as files at the source gateway. In the demo, the keys are in the image.
        - Since [PR #477](https://github.com/ICTU/GBO-demo/pull/477), the portal reads the BSN authorization from the BSN authorization list of BSNk instead of from configuration ([`portal.go#L38`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/consent-portal-backend/consent/portal.go#L38)). The authorization is therefore a snapshot too. If a source joins the list after the consent, that consent holds only a pseudonym for the source.
        - A proof in an older form is denied with `CONSENT_CONTEXT_INVALID`. The proof form changed twice (PR #469, PR #477). Each time, older proofs stopped working.
    - **Why it matters**: [BSNK-04](../requirements/pseudonymization.md#bsnk-04) (transformation only while the citizen is present) makes the proof a snapshot. After each later change, either the old proof keeps working, or the citizen gives a new consent. Each kind of change has its own effect:
        1. A new party needs a new consent (demo issue [#382](https://github.com/ICTU/GBO-demo/issues/382)).
        2. A new certificate at a source gives a new key version. While proofs for the old keys are valid, the source keeps those keys ([BSNK-08](../requirements/pseudonymization.md#bsnk-08), [AV-09](../requirements/admission.md#av-09)). The register must know the new version before the next consent (demo issue [#467](https://github.com/ICTU/GBO-demo/issues/467)).
        3. If a source gets a different OIN, the proof stops working for that source.
        4. If the PDP and the source do not keep the old form, a different proof form makes all outstanding proofs lapse. FR-11 allows months of validity, and the proof has no version.
        - The proof keys values on the OIN, while FSC knows parties by the Peer ID ([F-60](findings-closed.md#f-60), [Q-68](open-questions.md#q-68)). For each party of a service, the register must know the OIN, the key version, and the BSN authorization ([BSNK-06](../requirements/pseudonymization.md#bsnk-06)). The service catalogue (FR-32, [F-74](#f-74)) does not carry these values.
    - **Proposal**: [REQ-82](../requirements/pseudonymization.md#req-82) holds the requirement. Extend the service catalogue with the OIN, the key version, and the BSN authorization per party. Give the proof a version. Record how long an old version stays valid. [Q-77](open-questions.md#q-77) covers what counts as a change of a consent.
    - **Related**: [F-60](findings-closed.md#f-60), [F-74](#f-74), [F-75](#f-75), [REQ-82](../requirements/pseudonymization.md#req-82), [AV-09](../requirements/admission.md#av-09), [Q-68](open-questions.md#q-68), [Q-76](open-questions.md#q-76), [Q-77](open-questions.md#q-77), [ADR-0032](../decisions/0032-consent-proof.md).

### F-79: "After the decision" holds only if nothing but the Inway reaches the source gateway {#f-79}

- **Status**: open (the demo fixes it for Docker Compose. The roll-out outside Compose and the nonce are open.)

The source gateway decrypts the citizen from the consent proof and does
not check the proof again. That is safe only when every request at the
gateway has passed the PDP first. In an early demo version a consumer
was able to reach the gateway directly and skip the PDP. The demo now isolates
the gateway on its own networks. Every production deployment needs the
same isolation, and a nonce can bind a value to one consent as a second
guard.

??? note "Evidence, impact and proposal"

    - **Type**: design gap (security)
    - **Trigger**: [SL-51](increments.md#sl-51) ([PR #469](https://github.com/ICTU/GBO-demo/pull/469)). The substitution runs in the source gateway behind the Inway. A plugin in the Inway after the authorization needs a custom Inway build (demo issue [#364](https://github.com/ICTU/GBO-demo/issues/364)). A review of PR #469 showed that consumers were able to reach the source gateway without the Inway.
    - **Observation**:
        - The source gateway reads the proof without a signature check. It relies on the PDP that checked the same request ([`substitution.go#L105-L107`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/substitution/substitution.go#L105-L107)). The source gateway does check two things: the proof has a value for its own OIN, and the BSNk-signed value names that OIN as recipient.
        - Before the fix, consumers shared networks with the source gateways, and the source gateways published a port. A consumer with a real proof was able to send any query to the source gateway directly. The source gateway decrypted the identity and passed the query on. The checks on scope, fields, actor, and revocation did not run.
        - The fix: the source gateways publish no port. Each source gateway is only on a network with the Inways of the source and on a network with the service behind the source ([`docker-compose.yml#L829-L836`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L829-L836)). A check on October 5, 2026 showed that consumer networks and the host cannot reach the source gateways. The Inways can reach them.
    - **Why it matters**:
        - The rule "only after a positive decision" ([REQ-21](../requirements/pseudonymization.md#req-21)) depends on the deployment. The source gateway alone cannot make it true.
        - A signature check in the source gateway does not help. A consumer holds real proofs, so a direct call with a real proof passes the check and still skips the PDP.
        - Only two measures help: isolation, or a proof of the decision that is bound to the request. The Inway does not pass such a proof on.
        - A BSNk value is bound to a recipient. It is not bound to a consent, and it has no end date. A nonce can bind it to one consent as a second line of defense ([PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)).
    - **Proposal**: [REQ-81](../requirements/pseudonymization.md#req-81) says that only the component that enforces the decision reaches the source gateway. Outside Compose, this needs a NetworkPolicy or an equivalent measure. Add the nonce as a second line of defense ([BSNk preconditions](../requirements/pseudonymization.md#bsnk-preconditions)). The nonce is not built. Both measures are open design points from demo issue [#473](https://github.com/ICTU/GBO-demo/issues/473).
    - **Related**: [F-37](findings-closed.md#f-37), [F-77](#f-77), [REQ-21](../requirements/pseudonymization.md#req-21), [REQ-68](../requirements/consent.md#req-68), [REQ-81](../requirements/pseudonymization.md#req-81), [Q-14](open-questions.md#q-14), [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md).

### F-80: Since 2026 the ASI has a statutory interface and a seal obligation, but the authorization part stays a free choice {#f-80}

- **Status**: open

Since August 2026, EU law requires an authentic source interface (ASI)
for the verification of attributes. From January 1, 2027, the interface
must follow ETSI TS 119 478, and the source or a designated intermediary
must seal every result. The ETSI part on authorization is not
designated, so the member state chooses how the citizen is identified
and how the request is authorized. The GO and the PSA do not say that
verification is a legal obligation or that every result needs a seal.
The demo seals results with a development certificate, and who seals, in
which format, and who is the intermediary stay open.

??? note "Evidence, impact and proposal"

    - **Type**: external requirement (regulation)
    - **Trigger**: a reading of the 34 EUDI implementing acts (October 5 to 6, 2026), and then of the ARF v3.0.0 and its technical specifications.
    - **Observation**:
        - CIR (EU) 2025/1569, art. 9, applies from August 19, 2026. It requires an access point, attributes plus identification data in the request, and a result that says whether the attribute is verified.
        - CIR (EU) 2026/1735 adds art. 9(2a): the mechanism follows Annex IV. Annex IV designates ETSI TS 119 478 V1.1.1 clause 6.1.1 (verify over HTTP), clause 6.2.3 (verify over ISO 15000), or both.
        - The same act replaces art. 9(4): the result "shall be signed or sealed" by the public sector body or the designated intermediary. The minimum is an advanced signature or seal on a qualified certificate. On `Match` or `MatchWithVariation`, the result can contain the value.
        - Art. 9(2a) and 9(4) apply from January 1, 2027.
        - Annex IV does not designate clause 6.1.3 (the OAuth authorization server, with the identification data in a JWT token) or clause 5 (discover). CIR 2026/1735 also declares ETSI TS 119 471 clause 4.2.2.2 not applicable. As a result, QTSPs verify only through art. 9.
        - The ARF (QTSPAS_02) asks the source or intermediary to establish on each request that the requester is a QTSP that issues QEAAs. The ARF gives an example: "for example by means of a lookup in the QTSP Trusted List". The verification point is registered in the catalogue of attributes, as a `DataService` per source.
        - Demo state ([SL-28](increments.md#sl-28)): the ASIP seals every successful result with a detached JWS over the body, with the chain in `x5c` ([REQ-83](../requirements/asi.md#req-83), [PR #499](https://github.com/ICTU/GBO-demo/pull/499), [`seal.go`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/seal/seal.go)). The certificate is a development certificate. It is not qualified. The authorization follows clause 6.1.3 ([REQ-86](../requirements/asi.md#req-86) to [REQ-89](../requirements/asi.md#req-89)).
    - **Why it matters**: the GO and [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) (B-14) name an ASI provider per ETSI TS 119 478. They do not say that the verify part becomes a legal obligation, or that every result must be sealed. The member state chooses how the citizen is identified and how the request is authorized.
    - **Proposal**:
        - Add three points to PSA S11 and B-14. First, the verify interface follows ETSI clause 6.1.1, clause 6.2.3, or both. Second, every result is sealed with a qualified seal certificate. Third, the authorization is a free choice.
        - The demo choice for the authorization is [ADR-0037](../decisions/0037-asi-oauth-front-door.md) (clause 6.1 only, [REQ-112](../requirements/asi.md#req-112), [Q-64](open-questions.md#q-64)).
        - The seal is open: who seals ([Q-17](open-questions.md#q-17)) and in which format ([Q-32](open-questions.md#q-32), [ADR-0041](../decisions/0041-asi-seal-format.md), proposed).
        - Three more points are open: who is designated as intermediary ([Q-28](open-questions.md#q-28)), whether the value is returned ([Q-29](open-questions.md#q-29)), and who registers the verification points ([Q-31](open-questions.md#q-31)).
    - **Related**: [F-84](#f-84) to [F-87](#f-87), [REQ-83](../requirements/asi.md#req-83), [REQ-112](../requirements/asi.md#req-112), [Q-17](open-questions.md#q-17), [Q-28](open-questions.md#q-28), [Q-29](open-questions.md#q-29), [Q-31](open-questions.md#q-31), [Q-32](open-questions.md#q-32), [E4](standards-feedback.md#e4), [ADR-0037](../decisions/0037-asi-oauth-front-door.md), [ADR-0041](../decisions/0041-asi-seal-format.md).

### F-81: Since August 2026 PuB-EAA issuance falls under the same standard as QEAA issuance, with designation, registration, and its own certificate profile {#f-81}

- **Status**: open (the demo is not checked against it)

Since August 2026, EU law puts PuB-EAA issuance under the same standard
as QEAA issuance. The issuer is the bronhouder itself or a public sector
body that the member state designates. The issuer needs a qualified seal
certificate with a fixed profile, a notification by the member state,
and a registration as relying party. For GBO, this probably means one
notification per bronhouder, with GBO as the party that issues on its
behalf. The demo is not checked against the standard, and none of the acts in this reading says
who designates the issuer or who supervises.

??? note "Evidence, impact and proposal"

    - **Type**: external requirement (regulation)
    - **Trigger**: a reading of the EUDI implementing acts (October 5 to 6, 2026) and the ARF v3.0.0.
    - **Observation**:
        - **Who can issue**: eIDAS art. 3(46) names two options. The issuer is the bronhouder itself, or "a public sector body that is designated by the Member State" on behalf of bronhouders.
        - **Certificate**: the qualified certificate under the seal names the authentic source and the legal basis (eIDAS art. 45f(1)(b)). The profile is ETSI TS 119 412-6 clause 8, QcType `id-etsi-qct-eidaspsbeaa` (CIR 2026/1731).
        - **Standard**: CIR 2026/1735 replaces Annex I of 2025/1569 with ETSI TS 119 471 V1.1.1 and EN 319 401 V3.2.1, for QEAA and PuB-EAA providers. This change applies from entry into force (calculated: August 11, 2026). The provider makes the attestation seal in a QSCD.
        - **Notification and registration**: the member state notifies the issuer with a conformity assessment report (eIDAS art. 45f(3)). The issuer registers as relying party with the entitlement `PUB_EAA_Provider` (CIR 2025/848, Annex I, point 12(d)). The issuer has an access certificate. Since CIR 2026/1730, it also has a registration certificate.
        - **Protocol**: OpenID4VCI per ETSI TS 119 472-3, with checks on the wallet instance attestation and the key attestation (CIR 2026/1731).
        - ARF technical specification TS2 assumes that the bronhouder is the PuB-EAA provider. A party that issues on behalf of the bronhouder goes in the field `EEAIssuer`. For GBO, that probably means one notification per bronhouder, with GBO as `EEAIssuer`.
        - The intermediary model of TS5 applies only to relying parties. It does not apply to issuance.
        - Under the ARF technical specifications, each registered service needs its own access and registration certificate (Reg_10a, Reg_10c). Each Dutch attestation type needs a rulebook.
    - **Why it matters**: the demo issues through the nl-wallet issuance server and the EUDI adapter, with a certificate set per source ([REQ-58](../requirements/eudi-issuance.md#req-58)). That fits art. 45f(1)(b). The demo is not checked against TS 119 471, the certificate profile, or the checks of TS 119 472-3. None of the acts in this reading says who designates the issuer and who supervises.
    - **Proposal**: add the designation (art. 3(46)) and the standard (TS 119 471) to PSA B-13. [Q-28](open-questions.md#q-28) covers designation and supervision. [Q-30](open-questions.md#q-30) covers the trust list for PuB-EAA issuers. The check of the demo against TS 119 471 and TS 119 472-3 is completion work.
    - **Related**: [F-50](findings-closed.md#f-50), [F-66](findings-closed.md#f-66), [F-82](#f-82), [REQ-58](../requirements/eudi-issuance.md#req-58), [Q-17](open-questions.md#q-17), [Q-28](open-questions.md#q-28), [Q-30](open-questions.md#q-30), [ADR-0028](../decisions/0028-pubeaa-productization.md).

### F-82: An issuer must track changes in the source, but GBO only supports queries {#f-82}

- **Status**: open

The ARF requires that a provider revokes an attestation when an
attribute value in the source changes. The rule applies to revocable
attestations that are valid for 24 hours or more. GBO supports only
queries, and in the demo the source sends no change notifications. A
provider of long-lived attestations therefore needs a notification
stream from the source. The proposal is a choice per attestation type:
short-lived attestations that the provider issues again often, or
long-lived attestations with change notifications from the source.

??? note "Evidence, impact and proposal"

    - **Type**: external requirement (ARF)
    - **Trigger**: a reading of the ARF v3.0.0 (October 6, 2026).
    - **Observation**: ARF VCR_09 says that a provider "SHALL revoke that PID or attestation if the value of one or more of the attributes … was changed". This rule applies to a revocable attestation that is valid for 24 hours or more. An attestation that is valid for less than 24 hours does not have to be revocable. If an authentic source sets the value, "the Provider is responsible for ensuring that this third party notifies them about such changes".
    - **Why it matters**: GBO is designed for queries. In the demo, the adapter fetches the data from the source at issuance. The source sends no change notifications. A provider of long-lived PuB-EAAs needs such a notification stream. The alternative is short-lived attestations (less than 24 hours) that the provider issues again often.
    - **Proposal**: add a choice per attestation type to [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte) and B-13. The two options are short-lived attestations that the provider issues again often, or long-lived attestations with a change notification stream from the source. The ARF is not binding, but the requirement follows from the duty to revoke on changed data. [REQ-77](../requirements/eudi-issuance.md#req-77), [AV-12](../requirements/admission.md#av-12), and [AV-13](../requirements/admission.md#av-13) cover the validity and revocation policy per bronhouder.
    - **Related**: [F-81](#f-81), [REQ-77](../requirements/eudi-issuance.md#req-77), [AV-12](../requirements/admission.md#av-12), [AV-13](../requirements/admission.md#av-13), [ADR-0018](../decisions/0018-eudi-disclosure-issuance.md).

### F-83: Approval in the wallet is not a legal basis, so the EUDI route and DvTP consent cannot lean on each other {#f-83}

- **Status**: open

The ARF states that approval in the wallet is never a lawful ground for
processing by the relying party. In DvTP, the consent of the citizen is
the legal basis for delivery to a private party. In the EUDI route, the
citizen chooses only what to present. A consumer that uses both routes
therefore needs its own legal basis for the wallet route. The proposal
separates the terms in the GO and the PSA: consent is a registered,
revocable legal basis, and approval is a choice per presentation.

??? note "Evidence, impact and proposal"

    - **Type**: exposed assumption
    - **Trigger**: a reading of the ARF v3.0.0 (October 6, 2026).
    - **Observation**:
        - ARF §6.6.3.5.1 is explicit about "User approval to present data from their Wallet Unit". Under no circumstances is this approval "lawful grounds for the processing of personal data by the Relying Party or any other entity".
        - A relying party must have its own ground under GDPR art. 6.
        - eIDAS art. 5b(9) and ARF §2.5.1 add a second rule. If the law does not require identification, a relying party cannot refuse a pseudonym.
    - **Why it matters**: in DvTP, the consent of the citizen is the legal basis for delivery to a private party ([PSA P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/), [S01](https://ictu.github.io/GBO-PSA/main/capabilities/#s01-toestemmingsregistratie)). In the EUDI route, the citizen chooses in the wallet what to present. The ARF explicitly says that this choice is something else. A consumer that can get data through DvTP and through the wallet needs its own legal basis for the wallet route. No single "consent" covers both routes. The same holds for the ASI: the citizen approves by logging in per request, and that approval is no stored, revocable consent ([REQ-90](../requirements/asi.md#req-90)).
    - **Proposal**: separate the two terms in the GO and the PSA. Consent in DvTP is the legal basis, registered and revocable. Approval in the wallet is the choice of the citizen per presentation, and it is no legal basis.
    - **Related**: [F-70](#f-70), [REQ-68](../requirements/consent.md#req-68), [REQ-90](../requirements/asi.md#req-90), [ADR-0032](../decisions/0032-consent-proof.md).

### F-84: ETSI leaves the security profile of the ASI authorization server open, and conflicts on two points with the norms it refers to {#f-84}

- **Status**: open

ETSI leaves the security profile of the ASI authorization server largely
open. It gives a choice for client authentication and for token binding,
and it only asks to take the FAPI 2.0 profile into account. On two
points, ETSI conflicts with the norms that it refers to: pushed
authorization requests and the RS256 algorithm. A QTSP that verifies at
several ASI providers must therefore implement a different profile for
each authorization server. The proposal is one fixed profile for Dutch
ASI providers in the PSA, and a report of the two conflicts to ETSI.

??? note "Evidence, impact and proposal"

    - **Type**: open design choice
    - **Trigger**: [SL-28](increments.md#sl-28), the authorization server of the ASIP mock (demo issue [#503](https://github.com/ICTU/GBO-demo/issues/503)).
    - **Observation**:
        - REQ-AZSP-6.1.3.1-05 and -06 give a choice per mechanism. Client authentication uses mTLS or `private_key_jwt`. Token binding uses mTLS or DPoP. The demo chose `private_key_jwt` and DPoP.
        - REQ-AZSP-6.1.3.4-01 only asks to take the FAPI 2.0 Security Profile "into account". NOTE 3 at the PKCE requirement refers to FAPI clause 5.3.2.2, which requires pushed authorization requests (PAR, RFC 9126). ETSI does not require PAR. The demo does not offer PAR, because a server that requires PAR refuses QTSPs that implement only ETSI.
        - REQ-AZSP-6.1.3.1-08 makes RFC 9068 §2.1 mandatory. RFC 9068 §2.1 requires resource servers to support RS256. FAPI 2.0 allows only PS256, ES256, and EdDSA. The authorization server signs with ES256. The ASIP also accepts RS256.
        - [PR #574](https://github.com/ICTU/GBO-demo/pull/574) weighed RFC 9700 and FAPI 2.0 item by item ([`conformance/security-considerations.md`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/security-considerations.md)). The absence of PAR and the support for RS256 are deliberate demo choices. Two points stay open: `iss` in the authorization response ([F-96](#f-96)) and tokens after a right is revoked ([Q-41](open-questions.md#q-41)).
    - **Why it matters**: a QTSP that verifies at ASIPs in several member states, or at several Dutch ASIPs, must implement a different profile per authorization server. The GO and the PSA do not name the authorization. [F-80](#f-80) found that the member state is free to choose it.
    - **Proposal**: fix one profile for Dutch ASIPs in the PSA (S11, B-14). The profile names the client authentication, the token binding, and whether PAR is required ([Q-66](open-questions.md#q-66)). Send the two conflicts to ETSI ([E8](standards-feedback.md#e8)).
    - **Related**: [F-80](#f-80), [F-96](#f-96), [REQ-87](../requirements/asi.md#req-87), [Q-41](open-questions.md#q-41), [Q-66](open-questions.md#q-66), [E8](standards-feedback.md#e8), [E10](standards-feedback.md#e10), [ADR-0037](../decisions/0037-asi-oauth-front-door.md).

### F-85: The admission of QTSPs depends on a register and a certificate profile that do not exist {#f-85}

- **Status**: open

Before an ASI authorization server admits a QTSP, it looks up the right
of the QTSP in the national register of relying parties. That register
and its API do not exist. No text says which identifier links the QTSP
certificate to its register entry, and ETSI does not say what happens
when the register is unreachable. The demo uses a stub register and test
certificates, and it keeps a client active when the register is
unreachable. The proposal fixes the link between certificate and entry
and the behavior during an outage.

??? note "Evidence, impact and proposal"

    - **Type**: external dependency
    - **Trigger**: [SL-28](increments.md#sl-28), dynamic client registration ([PR #522](https://github.com/ICTU/GBO-demo/pull/522)).
    - **Observation**:
        - ETSI clause 6.1.3.2, figure 2: the authorization server looks up the right of the QTSP in the national register of relying parties (CIR 2025/848). It finds the entry through the `registryURI` in the software statement of the QTSP. It checks the right "again in regular intervals".
        - The right is `QEAA_Provider` (CIR 2025/848, Annex I, point 12). ETSI/EUDI TS5 lists it as `https://uri.etsi.org/19475/Entitlement/QEAA_Provider`, but an example in TS5 uses `http://data.europa.eu/eudi/entitlement/...`.
        - No text says which identifier links the QTSP certificate to its register entry. TS5 names the EUID as default. A seal certificate carries an `organizationIdentifier` such as `NTRNL-...`. The demo requires that the `organizationIdentifier` is one of the identifiers of the entry ([`registration.go#L212`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L212)).
        - The WRPAC profile (ETSI TS 119 411-8) was not read for this finding.
        - ETSI does not say what the server does if the register is unreachable during a re-check. In that case, the demo keeps the client active (fail-open, a demo choice: [`registration.go#L222-L228`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/registration.go#L222-L228)).
        - The demo uses a stub register file and test certificates from the development CA ([REQ-88](../requirements/asi.md#req-88), [REQ-89](../requirements/asi.md#req-89)).
    - **Why it matters**: the ASI can admit QTSPs only when two things exist: the national register with its API, and a fixed link between certificate and entry ([PSA P-07](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)).
    - **Proposal**: fix the link between certificate and entry ([Q-35](open-questions.md#q-35)) and the behavior when the register is unreachable ([Q-34](open-questions.md#q-34)). Report the URI conflict in TS5.
    - **Related**: [F-80](#f-80), [F-87](#f-87), [REQ-88](../requirements/asi.md#req-88), [REQ-89](../requirements/asi.md#req-89), [Q-34](open-questions.md#q-34), [Q-35](open-questions.md#q-35), [Q-41](open-questions.md#q-41), [ADR-0037](../decisions/0037-asi-oauth-front-door.md).

### F-86: ETSI requires the identification data in the token, and without encryption the QTSP reads the BSN {#f-86}

- **Status**: open

ETSI requires that the access token of the ASI carries the
identification data of the citizen, and it rejects token introspection.
The QTSP holds that token. In the demo, the token carries the BSN in
readable form, together with the name, birth date, and nationality.
Without encryption, the QTSP therefore processes the BSN, while the DvTP
route never sends a readable BSN as a field. The proposal is that only
the ASI provider can read the identification data, for example through a
claim that is encrypted for the provider.

??? note "Evidence, impact and proposal"

    - **Type**: conflict with a principle
    - **Trigger**: [SL-28](increments.md#sl-28), the access token of the authorization server (demo issue [#503](https://github.com/ICTU/GBO-demo/issues/503)).
    - **Observation**:
        - REQ-AZSP-6.1.3.1-08 requires JWT tokens "which shall contain the required identification data of the user". NOTE 6 rejects token introspection, because it does not meet art. 9(3) of CIR 2025/1569.
        - RFC 9068 §6 names encryption of the token or of sensitive claims as a privacy measure.
        - The demo carries the BSN readable in the claim `https://gbo.example/claims/bsn` ([`tokens.go#L29`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/tokens.go#L29)). Since demo issue [#523](https://github.com/ICTU/GBO-demo/issues/523), the token also carries the mandatory PID attributes that the identification means supplies ([REQ-86](../requirements/asi.md#req-86)). Demo issue [#595](https://github.com/ICTU/GBO-demo/issues/595) covers the protection and is open.
    - **Why it matters**: in the DvTP route, no readable BSN travels as a field ([REQ-20](../requirements/pseudonymization.md#req-20), [REQ-21](../requirements/pseudonymization.md#req-21)). In the ASI route, the QTSP holds the token. Without encryption, the QTSP processes the BSN ([PSA P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)). It also processes the name, birth date, and nationality from the identification. The QTSP often has those data from the citizen already, but the proposal covers the whole claim set. The same question applies to the encrypted identity that a consumer sends on ([Q-01](open-questions.md#q-01)).
    - **Proposal**: record in the PSA (S11) that only the ASIP can read the identification data in the token. One way is a claim that is encrypted for the ASIP. Send the gap to ETSI ([E7](standards-feedback.md#e7)).
    - **Related**: [F-88](#f-88), [F-93](#f-93), [REQ-20](../requirements/pseudonymization.md#req-20), [REQ-86](../requirements/asi.md#req-86), [Q-01](open-questions.md#q-01), [Q-36](open-questions.md#q-36), [E7](standards-feedback.md#e7).

### F-87: In the ASI route the QTSP is not an FSC participant, and the generic chain starts behind the ASIP {#f-87}

- **Status**: open

The earlier design assumed that a QTSP verifies through FSC as an OIN
holder. Under the designated ETSI route, the QTSP talks to the ASI
provider over HTTP as an OAuth client, and FSC has no part in admission.
The generic GBO chain starts behind the ASI provider, which is the actor
towards the source. The source sees neither the QTSP nor the citizen,
and the citizen cannot see QTSP verifications in any logbook. Open
points are which data about the QTSP the provider passes into the chain,
and how the source gets proof of the citizen.

??? note "Evidence, impact and proposal"

    - **Type**: replaces an assumption
    - **Trigger**: [SL-28](increments.md#sl-28). The earlier design assumed a QTSP that verifies through an FSC Outway as an OIN holder.
    - **Observation**:
        - ETSI TS 119 478 clause 6.1 is the designated route since CIR 2026/1735. In this route, the QTSP talks to the ASIP over HTTP as an OAuth client. It uses a token from the authorization server of the ASIP (clause 6.1.3). Admission runs through the register of relying parties and the QTSP certificate ([F-85](#f-85)). FSC has no part in admission. The demo builds it that way ([REQ-86](../requirements/asi.md#req-86) to [REQ-88](../requirements/asi.md#req-88)).
        - The chain behind the ASIP exists (demo issue [#525](https://github.com/ICTU/GBO-demo/issues/525)). The ASIP is an FSC peer of its own (`…1200`) with a contract for the BRP service. The ASIP is the actor in the chain: rule ASI0001 gives the ASIP peer the fields behind its attributes, on `brp` only ([`asi0001.rego`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/asi/asi0001.rego)).
        - The ASIP passes nothing about the QTSP into the chain. The source sees the ASIP. It does not see the QTSP or the citizen, and it relies on the ASIP for the check of the token.
        - The ASIP writes no LDV records, although it is a GBO-delivered component under [REQ-72](../requirements/logging-audit.md#req-72).
        - The PDP input and the decision log hold the BSN on ASI requests too ([REQ-60](../requirements/logging-audit.md#req-60), demo issue [#368](https://github.com/ICTU/GBO-demo/issues/368)).
    - **Why it matters**: the ASI is a front door with its own trust model ([PSA P-14](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)). The generic chain stays reusable, with the ASIP as its actor instead of the QTSP. The citizen cannot see QTSP verifications in any logbook.
    - **Proposal**: [ADR-0037](../decisions/0037-asi-oauth-front-door.md) records the front door. Describe it the same way in the GO and the PSA (S11, B-14). Decide which data about the QTSP the ASIP passes into the chain, for policy and for processing logging. Proof of the citizen at the source (the encrypted BSN of part 9 of the demo epic) is open. [ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md) (proposed) keeps the BSN out of the PDP input.
    - **Related**: [F-85](#f-85), [F-90](findings-closed.md#f-90), [REQ-60](../requirements/logging-audit.md#req-60), [REQ-72](../requirements/logging-audit.md#req-72), [REQ-88](../requirements/asi.md#req-88), [REQ-92](../requirements/asi.md#req-92), [REQ-97](../requirements/authorization.md#req-97), [ADR-0029](../decisions/0029-authentic-source-interface.md) (superseded), [ADR-0037](../decisions/0037-asi-oauth-front-door.md), [ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md).

### F-88: An identification means must deliver the mandatory identification data, or the data must come from elsewhere {#f-88}

- **Status**: open

ETSI requires the mandatory identification data of the citizen in the
ASI token. The wallet PID delivers these data except the place of birth,
but DigiD delivers only a BSN. If the Netherlands accepts such a means,
the authorization server fetches the other data from the BRP, or the
token holds only the BSN. The first option makes the server a BRP
consumer, and the second needs a reading of "required identification
data". The proposal is to record in the PSA which identification means
the server accepts and which data the token carries for each means.

??? note "Evidence, impact and proposal"

    - **Type**: open design choice
    - **Trigger**: [SL-28](increments.md#sl-28), request page and PID claims (demo issue [#523](https://github.com/ICTU/GBO-demo/issues/523)). DigiD came up as a second login route next to the wallet.
    - **Observation**:
        - REQ-AZSP-6.1.3.1-08 requires "the required identification data of the user" in the token. REQ-AZSP-6.1.3.1-03 allows the EUDI wallet over OpenID4VP "or an alternative electronic identification procedure according to ETSI TS 119 461".
        - The wallet PID has the mandatory attributes, except place of birth ([F-94](#f-94)). The demo copies them one to one ([REQ-86](../requirements/asi.md#req-86), [REQ-102](../requirements/asi.md#req-102)).
        - DigiD supplies only a BSN. In demo v0.9.0, a DigiD mock is available next to the wallet, with only the BSN in the token (demo issue [#544](https://github.com/ICTU/GBO-demo/issues/544)).
        - The other variant is not built: an authorization server that fetches the other data from the BRP. ETSI TS 119 461 allows this variant. With an eID means, a reliable register such as a population register can be supplementary evidence (USE-9.2.4-04 and its note).
    - **Why it matters**: if the Netherlands accepts a means that supplies only a BSN, two options remain. The authorization server must fetch the other data itself, or the token carries only the BSN. The first option makes the authorization server a BRP consumer. The second option needs a reading of "required identification data" ([PSA P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)).
    - **Proposal**: record in the PSA (S11) which identification means the authorization server of a Dutch ASI accepts. Also record which identification data the token carries for each means ([Q-36](open-questions.md#q-36)).
    - **Related**: [F-86](#f-86), [F-94](#f-94), [REQ-86](../requirements/asi.md#req-86), [REQ-102](../requirements/asi.md#req-102), [Q-36](open-questions.md#q-36).

### F-89: ETSI lets a response name one authentic source, so an ASIP for several sources offers one data service per source {#f-89}

- **Status**: open

In ETSI, a response of the ASI can name only one authentic source. GBO
builds one ASI provider for several sources, so one verify request with
attributes from two sources does not fit one response. The demo
therefore offers one data service per source, each with its own
contract, catalogue entry, and token audience. A token is valid for one
data service, so attributes from two sources need two authorizations and
two citizen interactions. The proposal records this layout in the PSA
and reports the gap to ETSI.

??? note "Evidence, impact and proposal"

    - **Type**: open design choice
    - **Trigger**: [SL-28](increments.md#sl-28), part 4 of the demo epic (demo issue [#525](https://github.com/ICTU/GBO-demo/issues/525)). GBO builds one ASIP for several authentic sources.
    - **Observation**:
        - REQ-ASIP-6.1.1.2-08 and REQ-ASIP-6.1.2.2-04 apply "if and only if the ASIP is different from the authentic source". In that case, the response has one `authenticSource`. The schema makes it a single object. CIR 2025/1569 art. 9(4) requires the result to name the responsible source, or the body that acts for it.
        - The Data Service Directory describes a `dataService` per attribute, with `endpointURI` and `provider` (REQ-DIP-5.3.3-03). One verify request with attributes of two sources does not fit one response.
        - The demo offers one data service per source under `/<dataservice>/authsrc-api`. Each data service has its own contract, catalogue entry, and token audience ([REQ-94](../requirements/asi.md#req-94), [REQ-95](../requirements/asi.md#req-95), [PR #529](https://github.com/ICTU/GBO-demo/pull/529), [`config/dataservices.json`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/config/dataservices.json)).
        - The reference QTSP follows this layout. It picks the data service that delivers all requested attributes. If no data service delivers all of them, the QTSP refuses the request before the authorization server and advises to split it ([REQ-99](../requirements/asi.md#req-99), [PR #535](https://github.com/ICTU/GBO-demo/pull/535)).
    - **Why it matters**: a token is valid for one data service. Attributes from two sources need two authorizations, with two citizen interactions. [Q-37](open-questions.md#q-37) asks whether one ASIP for several sources makes GBO an intermediary, or whether each bronhouder stays ASIP. The data-service layout fits both answers.
    - **Proposal**: the demo choice is [ADR-0038](../decisions/0038-asi-data-service-per-source.md) (accepted). Record three points in the PSA (S11, B-14): one data service per authentic source, the source in each response, and one token per data service. A possible improvement is several sources in one authorization (RFC 8707 §2.2, one token per resource). Send the gap to ETSI ([E3](standards-feedback.md#e3)).
    - **Related**: [REQ-91](../requirements/asi.md#req-91), [REQ-94](../requirements/asi.md#req-94), [REQ-95](../requirements/asi.md#req-95), [REQ-99](../requirements/asi.md#req-99), [Q-37](open-questions.md#q-37), [E3](standards-feedback.md#e3), [ADR-0038](../decisions/0038-asi-data-service-per-source.md).

### F-91: ETSI requires the authorization-server metadata in the contract, but gives no field for it {#f-91}

- **Status**: open

ETSI requires that the contract of an ASI data service names the
metadata of its OAuth authorization server. The OpenAPI format has no
field for that metadata: its OAuth fields hold single URLs, and its
OpenID field points to another kind of server. The demo uses its own
extension field with the standard metadata URL. Without a fixed field,
each ASI provider picks its own way, and a QTSP in several member states
must learn each way. The proposal is to ask ETSI and, until ETSI
answers, to describe the demo extension in the PSA as the Dutch choice.

??? note "Evidence, impact and proposal"

    - **Type**: open point in the specification
    - **Trigger**: [SL-28](increments.md#sl-28), part 6 of the demo epic (demo issue [#533](https://github.com/ICTU/GBO-demo/issues/533), [PR #534](https://github.com/ICTU/GBO-demo/pull/534)). The reference QTSP must find the authorization server from the Discover Interface record.
    - **Observation**:
        - REQ-DIP-5.3.3-03-02-01 requires that the contract that `endpointDescription` points to specifies the OAuth authorization-server metadata.
        - The OpenAPI 3.0 `oauth2` security scheme has only `authorizationUrl`, `tokenUrl`, and `refreshUrl`. The `openIdConnect` type has `openIdConnectUrl`, but that URL points to OpenID Connect Discovery. The clause 6.1.3 server is an OAuth server with RFC 8414 metadata. It is no OpenID provider. As a result, no field exists for the metadata, which includes `registration_endpoint` for RFC 7591 and `jwks_uri`.
        - The demo uses the extension `x-oauth-authorization-server`, with the URL at the RFC 8414 §3.1 location ([REQ-100](../requirements/asi.md#req-100), [`contract.go#L109`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/httpapi/contract.go#L109)).
    - **Why it matters**: without a fixed field, each ASIP chooses its own way. A QTSP that verifies in several member states must find out the way of each ASIP. The seal format has the same pattern ([Q-32](open-questions.md#q-32)).
    - **Proposal**: submit the question to ETSI ESI ([Q-39](open-questions.md#q-39), [E1](standards-feedback.md#e1)). Until ETSI answers, describe the demo extension in the PSA (S11) as the Dutch choice.
    - **Related**: [F-84](#f-84), [REQ-99](../requirements/asi.md#req-99), [REQ-100](../requirements/asi.md#req-100), [Q-32](open-questions.md#q-32), [Q-39](open-questions.md#q-39), [Q-67](open-questions.md#q-67), [E1](standards-feedback.md#e1).

### F-92: Annex IV of CIR 2026/1735 makes the value optional, but keeps the requirement for fuzzy matching {#f-92}

- **Status**: open

An EU implementing act makes the attribute value optional in a positive
ASI result. It keeps an ETSI rule that an ASI provider with fuzzy
matching must return the stored value. The demo does fuzzy matching and
returns no value, so a literal reading says that the demo does not meet
that rule. If the rule stays, a Dutch ASI provider must choose: return
the stored value on a fuzzy match, or do no fuzzy matching. The proposal
adds this choice to the open question whether the ASI returns the value,
and reports the point to ETSI.

??? note "Evidence, impact and proposal"

    - **Type**: contradiction in the source text
    - **Trigger**: [SL-28](increments.md#sl-28), part 6c of the demo epic ([PR #540](https://github.com/ICTU/GBO-demo/pull/540)). The conformance matrix reads ETSI TS 119 478 as amended by Annex IV of CIR (EU) 2026/1735.
    - **Observation**:
        - Annex IV makes `attributeValue` optional on `Match` and `MatchWithVariation` (REQ-ASIP-6.1.1.2-04-01 to -03, and -06-04-01 to -03 for fragments).
        - Annex IV does not amend REQ-ASIP-6.1.1.1-10-01. Under that requirement, an ASIP that supports fuzzy matching "shall return the attribute value … stored in the authentic source".
        - The demo does fuzzy matching (`MatchWithVariation`, after transliteration and normalization) and returns no value ([REQ-85](../requirements/asi.md#req-85), [REQ-113](../requirements/asi.md#req-113)). Read literally, the demo does not meet 10-01. The matrix marks that requirement `failing` ([`etsi-ts-119478.yaml#L132-L135`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/etsi-ts-119478.yaml#L132-L135)).
    - **Why it matters**: [REQ-85](../requirements/asi.md#req-85) chooses data minimization on the basis of Annex IV. If 10-01 stays, a Dutch ASIP must choose one of two options. It returns the stored value on `MatchWithVariation`, or it does no fuzzy matching (only `Match` or `NoMatch`).
    - **Proposal**: add this point as a sub-question to [Q-29](open-questions.md#q-29). The choice between the two options belongs to the question whether the ASI returns the value. Send the point to ETSI ([E2](standards-feedback.md#e2)).
    - **Related**: [REQ-84](../requirements/asi.md#req-84), [REQ-85](../requirements/asi.md#req-85), [REQ-113](../requirements/asi.md#req-113), [Q-29](open-questions.md#q-29), [Q-70](open-questions.md#q-70), [E2](standards-feedback.md#e2).

### F-93: Nothing links the citizen who logs in at the QTSP to the citizen who logs in at the source's authorization server {#f-93}

- **Status**: open

The QTSP identifies the citizen to whom it issues an attestation, and
the authorization server of the source identifies the citizen again for
the token. Nothing links these two identifications. A QTSP can therefore
issue an attestation with the data of person B to person A, for example
when B scans the QR code. The QTSP cannot compare the two itself,
because it must not receive the BSN and the token is opaque to it. The
proposal is a Dutch check: the QTSP sends its own identification data in
the request or to the authorization server for comparison.

??? note "Evidence, impact and proposal"

    - **Type**: open point in the specification
    - **Trigger**: [SL-28](increments.md#sl-28), part 7 of the demo epic (demo issue [#546](https://github.com/ICTU/GBO-demo/issues/546), [PR #550](https://github.com/ICTU/GBO-demo/pull/550), [PR #552](https://github.com/ICTU/GBO-demo/pull/552)). Work on issuance to the wallet (demo issue [#549](https://github.com/ICTU/GBO-demo/issues/549)) showed that the chain has two identifications of the citizen, with no link between them.
    - **Observation**:
        - eIDAS art. 24(1): a QTSP that issues a QEAA verifies the identity of the person it issues to. Paragraph 1a(a) names the EUDI wallet for that, "directly or by means of a third party". Annex V(c): the QEAA identifies the subject without ambiguity.
        - ETSI TS 119 478 clause 6.1.3.3 (figure 3): only the authorization server identifies the citizen (REQ-AZSP-6.1.3.1-02), and that data goes into the token. The clause does not describe identification by the QTSP. No requirement links the two identifications, and the security requirements of 6.1.3.4 do not link them either.
        - CIR 2025/1569 art. 9(3): the request "shall set out the attributes and the identification data of the subject". In ETSI, the token carries these data. The QTSP does not supply them. Art. 9(5): member states can impose checks that the QTSP "is acting at the request of a legitimate user".
        - Demo state: in demo v0.9.0, the reference QTSP identifies the citizen itself before the verification, with the NL Wallet or test data (demo issue [#560](https://github.com/ICTU/GBO-demo/issues/560)). Issuance to the wallet ([PR #570](https://github.com/ICTU/GBO-demo/pull/570)) links to the QTSP login only through names, birth date, and nationalities. Demo issue #549 closed without a check between the two logins.
        - On the same device, the wallet returns the browser with a nonce. The authorization server accepts that return only in the browser of the transaction ([PR #573](https://github.com/ICTU/GBO-demo/pull/573)). The QR-code route stays available: another phone can scan the code and complete the session.
    - **Why it matters**: without a link, a QTSP can issue an attestation with the data of person B to person A. This can happen, for example, when B scans the QR code. The QTSP cannot compare the identifications itself, for two reasons. It must not receive the BSN. Also, RFC 6749 and RFC 9068 treat the access token as opaque to the client.
    - **Proposal**: the Netherlands fixes a check under art. 9(5), in one of two variants:
        1. The QTSP puts the identification data from its own identification in the request, as art. 9(3) says literally, and has them verified too. `Match` then means that the citizen at the authorization server has the same name and birth date. Since demo issue #560, the QTSP has these data at request time. The check is not built.
        2. The QTSP gives the data to the authorization server (like `login_hint`), and the server refuses on a mismatch.
        - Decide in [Q-40](open-questions.md#q-40). Send the gap to ETSI ([E6](standards-feedback.md#e6)).
    - **Related**: [F-86](#f-86), [F-88](#f-88), [REQ-86](../requirements/asi.md#req-86), [REQ-88](../requirements/asi.md#req-88), [REQ-90](../requirements/asi.md#req-90), [REQ-102](../requirements/asi.md#req-102), [Q-40](open-questions.md#q-40), [E6](standards-feedback.md#e6).

### F-94: The NL PID has no place of birth, while the implementing regulation makes it mandatory {#f-94}

- **Status**: open

EU law makes five PID attributes mandatory, among them the place of
birth. The NL Wallet PID has no place of birth, so the authorization
server asks for four of the five attributes plus the BSN. If the
Netherlands reads "required identification data" as the mandatory PID
attributes, a token from the NL Wallet cannot meet the requirement. The
check covered only the metadata of the development environment, so the
content of the production PID is unknown. The proposal asks the NL
Wallet team about a place of birth, and records in the PSA the minimum
data in the token.

??? note "Evidence, impact and proposal"

    - **Type**: deviation between source text and implementation
    - **Trigger**: [SL-28](increments.md#sl-28), part 7 of the demo epic (demo issue [#546](https://github.com/ICTU/GBO-demo/issues/546), [PR #552](https://github.com/ICTU/GBO-demo/pull/552)). The authorization server asks for the PID attributes that the token must carry ([REQ-86](../requirements/asi.md#req-86)).
    - **Observation**:
        - CIR (EU) 2024/2977, table 1, makes `family_name`, `given_name`, `birth_date`, `birth_place`, and `nationality` mandatory.
        - The nl-wallet v0.5.0 PID type metadata for `urn:eudi:pid:nl:1` has no place of birth. The base type `urn:eudi:pid:1` has no place of birth either.
        - As a result, the authorization server asks for four of the five mandatory attributes, plus the BSN ([`provision.go#L40`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/walletverifier/provision.go#L40)). The run with the real NL Wallet delivered those four.
        - The metadata in the vendor checkout describes the development environment. The content of the production PID was not checked.
    - **Why it matters**: REQ-AZSP-6.1.3.1-08 requires "the required identification data" in the token. CIR 2025/1569 art. 9(3) requires the identification data of the subject. If the Netherlands reads that as the mandatory PID attributes, a token from the NL Wallet cannot meet the requirement. This holds as long as the NL PID has no place of birth. The finding also raises a question about the PID itself: does the NL PID meet table 1?
    - **Proposal**: ask the NL Wallet team whether the NL PID gets a place of birth. Record in the PSA (S11) which identification data the token carries at least, with and without place of birth ([Q-36](open-questions.md#q-36)).
    - **Related**: [F-88](#f-88), [REQ-86](../requirements/asi.md#req-86), [REQ-102](../requirements/asi.md#req-102), [Q-36](open-questions.md#q-36).

### F-95: ETSI binds an ASI token only per operation, so a binding per attribute needs its own extension {#f-95}

- **Status**: open

ETSI defines only the scopes verify and retrieve for an ASI token, so a
token covers an operation and names no attributes. The citizen then
approves an operation, and the approval does not name the requested
data. The demo binds the token to attributes with an extension type of
its own, and makes this binding optional. Only parties that know the
type can use the binding, and a QTSP from another member state does not
know it. If the open question decides so, the PSA records the binding as
the Dutch choice, and the type goes to ETSI.

??? note "Evidence, impact and proposal"

    - **Type**: open point in the specification
    - **Trigger**: [SL-28](increments.md#sl-28), part 11 of the demo epic (demo issue [#547](https://github.com/ICTU/GBO-demo/issues/547), [PR #559](https://github.com/ICTU/GBO-demo/pull/559)). The request page had to show which attributes the QTSP asks for.
    - **Observation**:
        - ETSI TS 119 478 defines the scopes `verify` and `retrieve` (clause 6.1.3.2). It defines no binding of the token to attributes. Only the request to the ASIP names the attributes that the QTSP asks for.
        - The demo uses RFC 9396 `authorization_details` with its own provisional type, `https://gbo.example/authorization-details/authentic-source-attributes` ([`authorization_details.go#L15`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-authorization-server/internal/authorization/authorization_details.go#L15)). The authorization server checks the attributes, shows them, and puts them in the token. The ASIP refuses other attributes ([REQ-103](../requirements/asi.md#req-103)).
        - Since [PR #572](https://github.com/ICTU/GBO-demo/pull/572) (demo issue [#571](https://github.com/ICTU/GBO-demo/issues/571)), the binding is optional. Without the detail, the token is per operation, as in ETSI. A QTSP that implements only ETSI can then connect. A configuration value (`AZSP_REQUIRE_AUTHORIZATION_DETAILS`) makes the detail mandatory.
    - **Why it matters**: without a binding, the citizen approves an operation. The approval does not name the requested data. With a type of its own, the binding works only between parties that know the type. A QTSP from another member state does not know it.
    - **Proposal**: if [Q-33](open-questions.md#q-33) decides so, record the per-attribute binding in the PSA (S11) as the Dutch choice. The demo choice is [ADR-0042](../decisions/0042-asi-attribute-token-binding.md) (proposed). Send the type to ETSI ([E5](standards-feedback.md#e5)), so that a next version of the standard fixes it.
    - **Related**: [F-84](#f-84), [REQ-91](../requirements/asi.md#req-91), [REQ-103](../requirements/asi.md#req-103), [Q-33](open-questions.md#q-33), [E5](standards-feedback.md#e5), [ADR-0042](../decisions/0042-asi-attribute-token-binding.md).

### F-96: ETSI does not name RFC 9207, so a QTSP that verifies at several ASIPs has no defense against mix-up {#f-96}

- **Status**: open

An OAuth client that talks to more than one authorization server needs a
defense against mix-up attacks. RFC 9700 prefers the issuer parameter in
the authorization response, and FAPI 2.0 requires the server to return
it. ETSI only asks to take both into account, and the demo does not
return the parameter. A QTSP talks to one authorization server per ASI
provider, which is exactly the case where RFC 9700 makes the defense
mandatory. The proposal is that a Dutch ASI authorization server returns
the issuer parameter and that the QTSP checks it.

??? note "Evidence, impact and proposal"

    - **Type**: open point in the specification
    - **Trigger**: [SL-28](increments.md#sl-28), part 8 of the demo epic ([PR #574](https://github.com/ICTU/GBO-demo/pull/574)): the item-by-item review of RFC 9700 and the FAPI 2.0 Security Profile.
    - **Observation**:
        - RFC 9700 §2.1 requires a defense against mix-up for a client that talks to more than one authorization server. The preferred defense is the `iss` parameter in the authorization response (RFC 9207). FAPI 2.0 §5.3.2.2 requires the server to return `iss`.
        - ETSI TS 119 478 clause 6.1.3.4 only asks to take both "into account" and does not name RFC 9207. Clause 6.1.3.1 does not require it.
        - The demo returns `code` and `state`, without `iss`. The metadata does not announce `authorization_response_iss_parameter_supported` ([`security-considerations.md#L23`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/conformance/security-considerations.md#L23)).
    - **Why it matters**: a QTSP talks to one authorization server per ASIP. In the EU, that is one server per member state or per source. RFC 9700 makes the defense mandatory for exactly this case. Without `iss`, the QTSP must tell servers apart with its own redirect URI per server (RFC 9700 §4.4.2). That method is a choice of each QTSP. It is part of the profile that ETSI leaves open ([F-84](#f-84)).
    - **Proposal**: record in the PSA (S11, B-14) that a Dutch ASI authorization server returns `iss` per RFC 9207, and that a QTSP checks it ([Q-66](open-questions.md#q-66)). Send the point to ETSI ([E9](standards-feedback.md#e9)), so that clause 6.1.3 includes it. The return of `iss` is not built in demo v0.9.0.
    - **Related**: [F-84](#f-84), [Q-66](open-questions.md#q-66), [E9](standards-feedback.md#e9), [ADR-0037](../decisions/0037-asi-oauth-front-door.md).

### F-97: FR-22 to FR-24 name the same statuses with different words, and the rationale of FR-23 contradicts its criteria {#f-97}

- **Status**: open

FR-22 to FR-24 of FR-DvTP use different words for the same consent
statuses. One rationale uses "Openstaand" (pending) next to "Actief"
(active). A revoked consent is "Geannuleerd" (cancelled) in one place and
"ingetrokken" (revoked) in another. The rationale of FR-23 allows
revocation only while the status is "Open", but its criteria also allow
it after retrieval. Builders and reviewers therefore get two readings of
one rule. The proposal is one set of terms, with "Ingetrokken" for a
revoked consent, and a rationale that matches the criteria.

??? note "Evidence, impact and proposal"

    - **Type**: contradiction in the source (FR-DvTP v0.9)
    - **Trigger**: a review of the decision points for the build phase, track B (October 27, 2026).
    - **Observation**:
        - FR-22, criterion 1, names the statuses active ("Actief"), retrieved and still valid ("Opgehaald (nog geldig)"), expired ("Verlopen"), and cancelled ("Geannuleerd"). The rationale of FR-22 uses "Openstaand" for the same status.
        - FR-23 names the action revoke ("Intrekken") and the outcome "Geannuleerd". FR-24 uses "ingetrokken".
        - The rationale of FR-23 says that revocation is possible only when the status is "Open". FR-23, criterion 1, and FR-24, criterion 1, also allow revocation after "Opgehaald", while the consent is valid.
    - **Why it matters**: builders and reviewers get two readings of one rule. The demo shows "Actief", "Verlopen", and "Ingetrokken" ([`StatusChip.tsx#L4-L6`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/toestemmingsportaal-frontend/src/components/consent-detail/StatusChip.tsx#L4-L6)). "Opgehaald" is missing, because no decision exists on when a consent counts as retrieved ([Q-42](open-questions.md#q-42), [F-19](#f-19)).
    - **Proposal**: use one set of terms in FR-DvTP: "Actief", "Opgehaald (nog geldig)", "Verlopen", and "Ingetrokken". The last term matches the action "Intrekken". Make the FR-23 rationale match the criteria: revocation is possible on "Actief" and "Opgehaald". The choice for the build (October 27, 2026) is "Actief" for the first status and "Ingetrokken" for a revoked consent ([REQ-109](../requirements/consent.md#req-109)).
    - **Addressee**: owner of FR-DvTP.
    - **Related**: [F-19](#f-19), [REQ-38](../requirements/consent.md#req-38), [REQ-109](../requirements/consent.md#req-109), [Q-42](open-questions.md#q-42), [Q-48](open-questions.md#q-48).

### F-98: FR-DvTP v0.9 contradicts decisions and its own criteria on four points, and PSA S02 is ambiguous on one point {#f-98}

- **Status**: open

FR-DvTP v0.9 conflicts with decisions or with its own criteria on four
points, and the PSA is ambiguous on one point. FR-39 and FR-26 put
policy and a first check at a central place, while the decisions keep
PAP and PDP at each bronhouder. FR-25 assumes that revocation ends at
retrieval, and FR-35 describes register contents that differ from the
chosen design. The PSA calls pseudonymization "transparent" to the
citizen, which can mean invisible or explained. The FR-DvTP owner must
make four changes and the PSA authors must fix the meaning, so that
builders do not get two conflicting sources.

??? note "Evidence, impact and proposal"

    - **Type**: contradiction in the source
    - **Trigger**: a design round compared FR-DvTP v0.9 and the PSA with the requirements (November 2, 2026).
    - **Observation**:
        - **FR-39** puts the authorization policy at a central policy authority. Its criteria cover centrally managed, sealed bundles (criteria 1 and 2), an RFC process (3), and governance of the authority (4). Criterion 5 puts the mapping of the service catalogue to scopes in that central policy. The decision in demo issue [#426](https://github.com/ICTU/GBO-demo/issues/426) replaced this model ([Q-21](answered-questions.md#q-21), closed October 28, 2026). Under that decision, policy management stays at each source, PAP and PDP sit at the bronhouder, and [RL-01 to RL-05](../requirements/authorization.md#policy-management) stay guidelines. Criterion 5 then belongs in the service description ([REQ-121](../requirements/consent.md#req-121)) instead of a central policy.
        - **FR-26**, dependency 2, says: "the bronhouder receives a request only after the central authorization component (FR-17) did the first check". That conflicts with [Q-02](answered-questions.md#q-02) (PEP, PDP, and PAP decentral at the bronhouder) and with [REQ-04](../requirements/authorization.md#req-04) and [REQ-68](../requirements/consent.md#req-68): the PDP of the source does the check. The FR-26 criteria themselves are covered.
        - **FR-25** applies the pointer to GDPR rights only "when a consent can no longer be cancelled technically (because the data is retrieved)". Its dependency says "only activated when FR-24 is active (revocation no longer possible)". But FR-23 and FR-24, criterion 1, allow revocation after retrieval while the consent is valid ([REQ-109](../requirements/consent.md#req-109)). For that reason, [REQ-120](../requirements/consent.md#req-120) shows the pointer with every consent and after every revocation.
        - **FR-35**, criterion 1, says: "only a party-specific identifier in place of the BSN and the consent proof are recorded". The design chooses otherwise on purpose ([REQ-69](../requirements/pseudonymization.md#req-69), [consent register data model](../requirements/consent.md#consent-register), route D in [ADR-0040](../decisions/0040-route-d-citizen-recognition.md)). The register keeps the polymorphic PI and PP under its own reference. It keeps no party-specific values, and it signs the proof without keeping it. Both approaches keep no BSN, but they record different data.
        - **PSA S02** says: "pseudonymization and technical identifiers are transparent to the citizen. The interface does not present them as a choice of content." The second part is clear and is in [REQ-117](../requirements/consent.md#req-117). "Transparent" can mean two things: the citizen sees nothing of it, or the interface explains it to the citizen ([PSA P-13](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)).
    - **Why it matters**: the requirements follow the decisions ([Q-02](answered-questions.md#q-02), [Q-21](answered-questions.md#q-21)) and the chosen design (route D). If the FR-DvTP text stays, builders and reviewers get two conflicting sources. The S02 UI requirement stays incomplete until the meaning of "transparent" is fixed.
    - **Proposal**:
        - The owner of FR-DvTP must make four changes:
            - Rewrite FR-39 to policy at the bronhouder, with the catalogue-to-set mapping in the service description.
            - Make FR-26 dependency 2 refer to the PDP of the source instead of a central authorization component.
            - Detach FR-25 from "revocation no longer possible". Apply it to every consent and after a revocation.
            - Make FR-35, criterion 1, describe what the register really keeps: its own reference with PI and PP, no party-specific values, and not the proof.
        - The PSA authors must fix in [S02](https://ictu.github.io/GBO-PSA/main/capabilities/#s02-toestemmingsportaal) whether "transparent" means invisible or explained.
    - **Addressee**: owner of FR-DvTP, and the PSA authors (S02).
    - **Related**: [F-06](findings-closed.md#f-06), [F-09](findings-closed.md#f-09), [F-97](#f-97), [REQ-04](../requirements/authorization.md#req-04), [REQ-68](../requirements/consent.md#req-68), [REQ-69](../requirements/pseudonymization.md#req-69), [REQ-109](../requirements/consent.md#req-109), [REQ-117](../requirements/consent.md#req-117), [REQ-120](../requirements/consent.md#req-120), [REQ-121](../requirements/consent.md#req-121), [RL-01](../requirements/authorization.md#rl-01), [RL-05](../requirements/authorization.md#rl-05), [Q-02](answered-questions.md#q-02), [Q-21](answered-questions.md#q-21), [ADR-0021](../decisions/0021-central-pap-signed-bundles.md), [ADR-0040](../decisions/0040-route-d-citizen-recognition.md).

## Summary for the PSA

The demo shows that the generic chain works end to end for three routes: DvTP, EUDI issuance, and the Authentic Source Interface (ASI). The following sections group the open findings per theme (state of November 2, 2026) and name what the PSA must decide.

An earlier version of this summary named six open design knots. All six are closed: [F-02](findings-closed.md#f-02), [F-03](findings-closed.md#f-03), [F-04](findings-closed.md#f-04), [F-06](findings-closed.md#f-06), [F-07](findings-closed.md#f-07), and [F-08](findings-closed.md#f-08). The requirements and ADRs cover PDP placement, consent atomicity, the consent lifecycle, the fourth validation point, LDV, and mTLS on FSC.

In total, 34 findings are open. The review of September 21, 2026 closed 28 of 39 findings and kept 11 open. After that review, 24 findings were added, and the demo resolves one of them. [F-54](#f-54) is open again, and [ADR-0021](../decisions/0021-central-pap-signed-bundles.md) closed [F-09](findings-closed.md#f-09).

### Policy management

- **Closed**: [F-09](findings-closed.md#f-09) (signing only across an organization boundary, [ADR-0021](../decisions/0021-central-pap-signed-bundles.md)).
- **Open**: [F-51](#f-51) (management endpoints behind the decision policy), [F-52](#f-52) (cumulative store), and [F-98](#f-98) (FR-39 still describes a central policy authority).
- **Decided**: policy management stays at each source. PAP and PDP sit at the bronhouder ([Q-21](answered-questions.md#q-21)). [RL-01 to RL-05](../requirements/authorization.md#policy-management) are guidelines for bronhouders.
- **PSA to decide**: whether bundle signing is required when a bundle crosses an organization boundary ([ADR-0021](../decisions/0021-central-pap-signed-bundles.md)).

### Consent and its lifecycle

- **Open**: [F-19](#f-19) (no "retrieved" status), [F-74](#f-74) (scope is the intersection of legal ceiling and source offer), [F-78](#f-78) (the proof freezes at consent), and [F-97](#f-97) and [F-98](#f-98) (FR-DvTP contradictions).
- **Decided**: the legal basis travels as a signed proof. The status is checked online and fails closed ([F-61](findings-closed.md#f-61), [ADR-0032](../decisions/0032-consent-proof.md)). An integrator connects under FSC delegation, and the consent binds the represented party ([F-73](findings-closed.md#f-73), [ADR-0034](../decisions/0034-integrator-delegation.md)).
- **PSA to decide**:
    1. When a consent counts as retrieved, and how the register learns it ([Q-42](open-questions.md#q-42)).
    2. A DvTP catalogue per FR-32 as the single source for scopes, with an intersection check at activation (B-03, [REQ-121](../requirements/consent.md#req-121)).
    3. A version for the proof, and how long an old version stays valid ([REQ-82](../requirements/pseudonymization.md#req-82)).
    4. What "transparent" means in S02 ([F-98](#f-98)).

### Authorization regime

- **Open**: [F-70](#f-70). The regime follows from the proof ([ADR-0031](../decisions/0031-regime-from-evidence.md)), but only consent is positive proof. The PID regime rests on an actor list and an unverified BSN.
- **PSA to decide**: what the evidence for the EUDI legal basis is ([REQ-45](../requirements/eudi-issuance.md#req-45), [Q-18](open-questions.md#q-18)). The demo resolves the binding of rules to services ([F-90](findings-closed.md#f-90)), and this binding is a proposal for S05.

### Pseudonymization and BSNk

- **Open**: [F-75](#f-75) (the consent facility must be a recognized BSNk party), [F-76](#f-76) (the consumer has no citizen identifier), [F-77](#f-77) (one subject per request), and [F-79](#f-79) (only the Inway reaches the source gateway, with the roll-out outside Compose and the nonce open).
- **Decided in the TO**: the source gateway decrypts its own value after the allow ([ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md)). Route D for citizen recognition is proposed ([ADR-0040](../decisions/0040-route-d-citizen-recognition.md)).
- **PSA to decide**:
    1. Recognition of the consent facility at BSNk, and who the BSNk participant is ([Q-26](open-questions.md#q-26), [Q-49](open-questions.md#q-49)).
    2. Whether the consumer gets a pseudonym (VP), with its effects on logging, access, and recognition ([Q-01](open-questions.md#q-01)).
    3. Queries about more than one person.

### Admission and service descriptions

- **Open**: [F-57](#f-57) (the source owns its description, but the DCAT-AP-NL reference and central findability are missing), and [F-71](#f-71) (an operator takes over a description, and the recorded agreement of the bronhouder is not built).
- **Decided**: admission is a register entry instead of a policy rule ([F-55](findings-closed.md#f-55)).
- **PSA to decide**: accept or reject the role split "the source publishes, GBO validates and activates" (S10), and decide where central findability lives.

### Audit and logging

- **Open**: [F-54](#f-54) (BSN in both decision logs on the EUDI and ASI routes), [F-68](#f-68) (no route from the ADL at the source to the consent logbook), [F-72](#f-72) (the ADL lacks policy version, consent status answer, and configuration), and [F-76](#f-76) (what the consumer logs under).
- **Decided**: three standards give three records. ADL is for decisions ([ADR-0036](../decisions/0036-adl-decision-record.md)), LDV is per controller ([ADR-0026](../decisions/0026-ldv-integration.md)), and FSC-Logging is for transport. W3C Trace Context is the correlation key ([ADR-0035](../decisions/0035-w3c-trace-context.md)). The register index covers the chain start ([F-68](#f-68) point 1).
- **PSA to decide**: keep identifiers out of the PDP input instead of masking logs ([ADR-0043](../decisions/0043-identifiers-out-of-pdp-input.md), proposed). The questions to Logius ([Q-25](open-questions.md#q-25), [Q-27](open-questions.md#q-27)) and to OpenFTV (fill the ADL fields) need an owner.

### EUDI issuance

- **Open**: [F-47](#f-47) (attestation about a related person), [F-81](#f-81) (designation, TS 119 471, and the certificate profile), [F-82](#f-82) (an issuer must track source changes), and [F-83](#f-83) (wallet approval is no legal basis).
- **PSA to decide**:
    1. Who designates the PuB-EAA issuer and who supervises ([Q-28](open-questions.md#q-28)). Add art. 3(46) and TS 119 471 to B-13.
    2. Per attestation type: short-lived, or long-lived with a change notification stream from the source.
    3. Separate the terms "consent" (DvTP) and "approval" (wallet) in the GO and the PSA.
    - The relation in a related-person attestation is enforced through schema filters instead of source code ([REQ-57](../requirements/eudi-issuance.md#req-57)).

### Authentic Source Interface

- **Open**: [F-80](#f-80), [F-84](#f-84) to [F-89](#f-89), and [F-91](#f-91) to [F-96](#f-96).
- **Decided in the TO**: the ASI is an OAuth front door per ETSI TS 119 478 clause 6.1, and the QTSP is not an FSC participant ([ADR-0037](../decisions/0037-asi-oauth-front-door.md)). Each source has one data service, with one token per data service ([ADR-0038](../decisions/0038-asi-data-service-per-source.md)). The source describes its ASI attributes ([ADR-0039](../decisions/0039-asi-source-described-attributes.md)). Two ADRs are proposed: the seal format ([ADR-0041](../decisions/0041-asi-seal-format.md)) and the optional per-attribute binding ([ADR-0042](../decisions/0042-asi-attribute-token-binding.md)).
- **PSA to decide** (S11, B-14): Annex IV and the seal duty apply from January 1, 2027. The PSA must decide five points:
    1. The role of GBO and the designated intermediary ([Q-37](open-questions.md#q-37), [Q-28](open-questions.md#q-28)), and who holds the qualified seal certificate ([Q-17](open-questions.md#q-17), [Q-32](open-questions.md#q-32)).
    2. One security profile for Dutch authorization servers, including `iss` per RFC 9207 ([Q-66](open-questions.md#q-66), [F-84](#f-84), [F-96](#f-96)).
    3. The accepted identification means, and identification data in the token that only the ASIP can read ([Q-36](open-questions.md#q-36), [F-86](#f-86), [F-88](#f-88), [F-94](#f-94)).
    4. A check that links the QTSP login to the login at the authorization server ([Q-40](open-questions.md#q-40), [F-93](#f-93)), and per-attribute binding under art. 9(5) ([Q-33](open-questions.md#q-33)).
    5. Whether the ASI returns the value on a match, and fuzzy matching ([Q-29](open-questions.md#q-29), [F-92](#f-92)). Also the register and the certificate link for QTSP admission ([Q-34](open-questions.md#q-34), [Q-35](open-questions.md#q-35)).
    - The specification gaps go to ETSI ESI: [E1 to E10](standards-feedback.md). The sender is not decided.

### Source texts

- **Open**: [F-97](#f-97) and [F-98](#f-98). The owner of FR-DvTP makes FR-22 to FR-26, FR-35, and FR-39 match the decisions. The PSA authors fix the meaning of "transparent" in S02.
