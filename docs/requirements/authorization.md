# Authorization and data access requirements

These requirements cover how GBO Basis decides on a request. They cover the PEP, the PDP and the rules, the enforcement of the query, and the data that the source returns. They also cover how the policy itself is managed. For the design, see [Authorization in GBO Basis](../building-blocks/gbo-basis/authorization.md).

This page has the following parts:

- [PEP, PDP and PIP](#authorization)
- [Query enforcement requirements](#query-enforcement)
- [Data minimization requirements](#data-minimization)
- [Policy management guidelines](#policy-management)

## PEP, PDP and PIP {#authorization}

The requirements on this page cover the authorization of one request at a
source. They apply to the PEP, the PDP of the source, and the information
sources (PIP) that the PDP consults. The requirements are generic: they
apply to DvTP, EUDI issuance, and the ASI route.
[Admission](admission.md) covers the admission of a party before any
request. [Query enforcement](authorization.md#query-enforcement) covers the decision
per field of a query.

### Rule set in the demo

The demo (v0.9.0) uses the FSC Inway as the PEP and OpenFTV with OPA as
the PDP. The reference policy is plain Rego under
[`policies/gbo/`](https://github.com/ICTU/GBO-demo/tree/v0.9.0/policies/gbo).
Each rule declares its regime and the FSC services that it applies to
([REQ-74](#req-74), [REQ-97](#req-97)). Each rule also states its own
reasons to deny ([REQ-48](#req-48)). The reference policy has five rules:

| Rule | Regime | FSC service | What it grants |
|---|---|---|---|
| DVT0001 | consent | `bri` | income declaration fields under a consent |
| LVG0001 | consent | `lvg` | ownership check at the LVG source |
| EUD0001 | PID | `bri` | income declaration to the wallet |
| EUD0002 | PID | `brp` | death certificate to the wallet |
| ASI0001 | PID | `brp` | BRP fields for the ASIP |
### REQ-04: The source delivers only after a positive decision by its PDP {#req-04}

> Every request to a source MUST pass a PEP that consults the PDP of the
> source. The PEP MUST let the request through only after a positive
> decision. What is behind the PEP (source gateway, source service) MUST
> NOT be reachable for a consumer by another route. If no decision comes,
> the request MUST be denied.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
      [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
      ("iedere gegevensvraag doorloopt een PEP-PDP-keten", "een PEP weigert
      standaard bij ontbrekende of onbetrouwbare beslisinformatie"), and
      FR-26 criteria 1 and 3.
    - **Addressee**: interface agreement. The requirement applies to every
      source that connects through GBO.
      [REQ-81](pseudonymization.md#req-81) works it out for the source
      gateway that GBO delivers.
    - **Evidence**: every Inway sends every request as an AuthZEN question to
      the PDP
      ([`fsc-infra/docker-compose.yml#L769-L775`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L769-L775),
      [`#L957-L959`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L957-L959),
      [PR #60](https://github.com/ICTU/GBO-demo/pull/60)). The source gateways
      are only on a network with the Inways
      ([`docker-compose.yml#L829-L836`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L829-L836),
      [PR #469](https://github.com/ICTU/GBO-demo/pull/469)). No test exists.
    - **Related**: [REQ-81](pseudonymization.md#req-81), [REQ-21](pseudonymization.md#req-21),
      [REQ-42](#req-42), [F-35](../traceability/findings-closed.md#f-35),
      [ADR 0002](../decisions/0002-opa-rego-authzen.md),
      [ADR 0033](../decisions/0033-gateway-decrypts-after-allow.md).
    - **Notes**: design choice: the FSC Inway is the PEP, with the PDP as
      AuthZEN endpoint. There is no separate PEP service. The isolation of the
      gateway exists only in compose. In Kubernetes, the isolation needs a
      NetworkPolicy or an equivalent control.

### REQ-06: A denial carries a machine-readable reason: coarse for the consumer, full for the operator {#req-06}

> The PDP MUST give a machine-readable reason for every denial. The consumer MUST get only a code that tells that the request was denied and in which class. That code MUST NOT reveal which field was denied, whether a field exists, or which check failed. For the operator of the source, the record MUST show which rules decided on each denied field, and with which reasons. The most fundamental reason MUST come first. A fault on the side of the source MUST appear to the consumer as a normal access denial.

| Case | Outcome |
|---|---|
| Field is outside the rule | consumer: `FIELD_NOT_PERMITTED`. Operator: per field the rule and the reason, for example `YEAR_NOT_COVERED`. |
| Query cannot be verified | consumer: `COVERAGE_UNVERIFIABLE` with a subcode. For `INVALID_QUERY`, the consumer gets `FIELD_NOT_PERMITTED`. |
| Register unreachable, rule cannot be evaluated | consumer: `ACCESS_DENIED`. Operator: `PIP_UNAVAILABLE` or `CONFIG_ERROR` with trace. |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
      [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
      ("logging legt de beleidsversie, relevante context en beslissing vast"),
      [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid),
      and [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
      The consumer codes follow the
      [FTV GraphQL profile for AuthZEN](https://github.com/VNG-Realisatie/ftv/blob/3da8a3378a8b729f39bda09a4c7440b77a0a3457/static/documents/20260928-ftv-graphql-profile.html)
      ("Decision and Error Transport", "Security Considerations").
    - **Addressee**: GBO-delivered component: the reference engine of the
      PDP. Interface agreement: the consumer codes.
    - **Evidence**: [PR #488](https://github.com/ICTU/GBO-demo/pull/488)
      gives this evidence:
        - The consumer code is in
          [`engine.rego#L95-L118`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L95-L118).
        - The detail per field is in
          [`#L56-L68`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L56-L68).
        - The order is in
          [`#L321-L344`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L321-L344).
        - The tests are
          [`engine_test.rego#L11`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L11)
          and
          [`#L29`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L29).
        - If a rule cannot be evaluated, the field is denied
          ([`engine.rego#L18-L23`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L18-L23))
          with `CONFIG_ERROR` / `RULE_NOT_EVALUABLE`
          ([`#L77-L79`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L77-L79)).
          The test is
          [`engine_test.rego#L784-L791`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L784-L791).
    - **Related**: [REQ-32](logging-audit.md#req-32), [REQ-71](logging-audit.md#req-71),
      [REQ-74](#req-74), [F-72](../traceability/findings.md#f-72).
    - **Notes**: in demo v0.9.0, the detail per field reaches only the
      console decision log of the engine (observability). The ADL records
      only the consumer code
      ([`authz.rego#L42-L51`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/authz.rego#L42-L51)).
      Design choice: the order is first the proof, then the state of the
      consent, then the question, then the caller.

### REQ-18: The PDP decides on facts that it established itself, and never on what the consumer declares {#req-18}

> The PDP MUST decide on facts that it verified itself or fetched from a trusted source. The PDP MUST take the caller and the service from the transport token that the source signed. It MUST take the consent from a proof whose signature and status the PDP checks itself. It MUST take the admission from the register.

> What the consumer sends (header, body, query argument) MUST state only what is asked. It MUST NOT carry a decision without that own check. The PDP MUST ignore decision information that arrives in the question as a ready-made fact.

| Case | Outcome |
|---|---|
| Consent record sent in the question, no token | ignored. The PID regime applies, and the placeholder names nobody: `PID_NOT_PRESENT`. |
| Register gives no status | denied: `CONSENT_STATUS_UNAVAILABLE` |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
      [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
      ("de PDP kan relevante informatiebronnen raadplegen", "een PEP weigert
      standaard bij ontbrekende of onbetrouwbare beslisinformatie"), FR-16
      criterion 1, and FR-17 criterion 1.
    - **Addressee**: GBO-delivered component: the reference PDP (mapper and
      policy).
    - **Evidence**: the PDP ignores a consent that is sent in the question
      ([`dvtp_helper.rego#L6-L9`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvtp_helper.rego#L6-L9),
      test [`engine_test.rego#L54`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L54)).
      The policy checks the token and the status itself
      ([`consent.rego#L169-L186`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L169-L186),
      [`#L270-L280`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L270-L280),
      [PR #371](https://github.com/ICTU/GBO-demo/pull/371)). The service and
      the caller come from the token
      ([`ftvgraphql.go#L30-L33`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/mapper/ftvgraphql.go#L30-L33),
      [`lib.rego#L55-L72`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L55-L72)).
      Since [PR #580](https://github.com/ICTU/GBO-demo/pull/580), a declared
      scope header does not count.
    - **Related**: [REQ-68](consent.md#req-68), [REQ-61](admission.md#req-61),
      [REQ-79](pseudonymization.md#req-79), [REQ-74](#req-74),
      [REQ-45](eudi-issuance.md#req-45), [F-32](../traceability/findings-closed.md#f-32),
      [ADR 0032](../decisions/0032-consent-proof.md).
    - **Notes**: in demo v0.9.0, the BSN in the PID regime is a statement of
      the adapter. The PID is not verified
      ([ICTU/GBO-demo#133](https://github.com/ICTU/GBO-demo/issues/133),
      [REQ-45](eudi-issuance.md#req-45)). The fetched consent is not in the
      question. For that reason, the PDP adds it to its answer, for the
      decision record
      ([`engine.rego#L25-L29`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L25-L29)).

### REQ-42: The authorization request follows an open PEP-PDP profile, and the PEP passes the request on unchanged {#req-42}

> The question from PEP to PDP MUST follow the AuthZEN NLGov profile. In that profile, the caller is the subject, the request is the action and the resource, and the transport context is the context. The PEP MUST pass the request on unchanged (for GraphQL: the raw body). The PEP MUST NOT interpret or add to the request. The PDP side decides which data the request asks for.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
      [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
      ("gestandaardiseerd vocabulaire voor subject, actie, resource en
      context", "de interface en het beleid zijn productonafhankelijk",
      agreement: AuthZEN NLGov profile).
    - **Addressee**: interface agreement: PEP to PDP. GBO-delivered
      component: the mapper on the PDP side.
    - **Evidence**: the Inway sends the body
      ([`fsc-infra/docker-compose.yml#L773-L775`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L773-L775)).
      The mapper reads the question and does not change it
      ([`ftvgraphql.go#L11-L13`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/mapper/ftvgraphql.go#L11-L13),
      [`#L89-L103`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/mapper/ftvgraphql.go#L89-L103)).
      The changes are in [PR #482](https://github.com/ICTU/GBO-demo/pull/482)
      and [PR #484](https://github.com/ICTU/GBO-demo/pull/484).
    - **Related**: [REQ-04](#req-04), [REQ-17](authorization.md#req-17),
      [REQ-18](#req-18), [Q-16](../traceability/answered-questions.md#q-16),
      [ADR 0002](../decisions/0002-opa-rego-authzen.md).
    - **Notes**: design choice: for GraphQL, the demo follows the FTV GraphQL
      profile for AuthZEN. The profile work continues upstream. The Inway
      sends the body only with `Content-Type: application/json`. Without a
      body, the mapper fails closed.

### REQ-44: A channel adapter translates protocol, and the decision on source data lies with the PDP of the source {#req-44}

> A channel adapter that GBO delivers MUST do only protocol translation and pass the request on. It MUST NOT decide which data of the source a party gets. It MUST NOT fetch or add decision information (consent, admission, designation) itself. It MUST NOT carry knowledge of a source or use case in code. Checks that belong to the channel protocol itself (wallet session, access token of the channel) stay with the channel.

> A channel adapter MUST query the source through the source access that the source offers for all GBO interaction patterns. It MUST NOT ask a source for a channel-specific koppelvlak.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: derived. The requirement serves
      [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) and
      [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie).
      If the adapter takes part in the decision, the policy of the source
      does not alone decide what a party gets. The single koppelvlak follows
      from the design:
      [PSA S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting)
      ("een bronhouder gebruikt voor de GBO-interactiepatronen één logisch
      koppelvlak") and
      [P-06 and P-08](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: channel adapters (in demo
      v0.9.0, the EUDI adapter).
    - **Evidence**: the query and the mapping come from the source metadata,
      with no source-specific query
      ([`eudi-adapter/main.go#L16-L21`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L16-L21),
      [PR #219](https://github.com/ICTU/GBO-demo/pull/219)). The adapter does
      not fetch consent. The PDP judges
      ([`#L10-L14`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L10-L14)).
      No test exists.
    - **Related**: [REQ-64](sources-identity.md#req-64),
      [REQ-45](eudi-issuance.md#req-45), [F-31](../traceability/findings-closed.md#f-31),
      [Q-17](../traceability/open-questions.md#q-17).
    - **Notes**: the adapter takes the BSN from the PID disclosure and does not
      check the signature
      ([`#L23-L24`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L23-L24)).
      That gap falls under [REQ-45](eudi-issuance.md#req-45) and is no
      decision of the adapter. This requirement and
      [REQ-64](sources-identity.md#req-64) cover the removed REQ-51.

### REQ-48: Every rule checks actor and scope itself, and a request passes only if no check denies {#req-48}

> Every rule of the PDP MUST check the actor and the scope of the request
> itself, in every regime. The actor MUST NOT follow only from the
> existence of an FSC contract or connection. The scope (fields and filters
> such as tax years) MUST NOT be taken from what an adapter or consumer
> declares. A field MUST be allowed only if a rule about it has no reason
> to deny on any check. The request MUST be allowed only if every requested
> field is allowed. A policy set MUST enforce with a test that every rule
> has its own actor check.

| Case | Outcome |
|---|---|
| Consent given to another party | denied: `CONSENT_ACTOR_MISMATCH` |
| Year outside the consent, or no year filter | denied: `YEAR_NOT_COVERED` |
| PID regime, caller is not a designated issuer | denied: `ACTOR_NOT_ALLOWED` |
| PID regime, year outside the rule | denied: `YEAR_NOT_ALLOWED` |
| ASI rule, caller is not the ASIP | denied: `ACTOR_NOT_ALLOWED` |
| Integrator without a mandate for this rule | denied: `INTEGRATOR_NOT_REGISTERED` |
| One field denied, the rest allowed | the whole request denied |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
      [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
      (a check against identity, service, grondslag, and data scope, with the
      acting and the represented party, and allow or deny per field),
      [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/), FR-16
      criteria 2 and 3, and FR-17 criteria 2 and 3.
    - **Addressee**: GBO-delivered component: the reference engine and the
      rules of the PDP.
    - **Evidence**: the actor-check test is not built:
      [ICTU/GBO-demo#604](https://github.com/ICTU/GBO-demo/issues/604).
      [PR #507](https://github.com/ICTU/GBO-demo/pull/507) and
      [PR #464](https://github.com/ICTU/GBO-demo/pull/464) built these parts:
        - all fields
          ([`engine.rego#L36-L41`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L36-L41)),
          the first rule without a reason
          ([`#L290-L293`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L290-L293)),
          and the mandate
          ([`#L246-L267`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L246-L267))
        - DVT0001
          ([`dvt0001.rego#L59-L68`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L59-L68),
          [`#L82-L96`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L82-L96))
        - EUD0001
          ([`eud0001.rego#L45-L75`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0001.rego#L45-L75),
          [`eudi_helper.rego#L13-L24`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eudi_helper.rego#L13-L24))
        - the tests [`dvt0001_test.rego#L84`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L84),
          [`eud0001_test.rego#L65`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0001_test.rego#L65),
          and
          [`engine_test.rego#L315`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L315)
        - the years, tested with a literal list, a schema default, null, and
          a variable in
          [`dvt0001_test.rego#L162-L202`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L162-L202)
        - the denial of a field without a decision, which is not left out
          ([PR #519](https://github.com/ICTU/GBO-demo/pull/519),
          [`engine.rego#L18-L23`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L18-L23),
          tested in [`engine_test.rego#L775-L791`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L775-L791))
        - a consent without scopes, which covers no year
          ([`dvt0001_test.rego#L183-L187`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001_test.rego#L183-L187))
    - **Related**: [REQ-97](#req-97), [REQ-74](#req-74),
      [REQ-106](consent.md#req-106), [F-56](../traceability/findings-closed.md#f-56),
      [ADR 0034](../decisions/0034-integrator-delegation.md).
    - **Notes**:
        - Contract proposals are co-signed without a check of the grant
          content ([F-56](../traceability/findings-closed.md#f-56)). This
          requirement is the compensating control. A rule without its own
          actor check, or an actor list derived from the contract, reopens
          that decision.
        - In demo v0.9.0, designated issuers and allowed years are fixed in
          the rules. With more parties or years, they belong in a register
          ([REQ-61](admission.md#req-61)).
        - The test that checks every rule for its own actor check does not
          exist (#604).

### REQ-74: The authorization regime follows from the evidence a request carries {#req-74}

> The regime under which the PDP judges a request MUST follow from the
> proof that the request carries. It MUST NOT follow from a property that
> only names the regime (no header, contract property, or claim). Only the
> rules of that regime MAY judge the request, so the deny reason comes from
> that regime. If a request carries more than one consent proof, it MUST be
> denied. If the absence of proof opens a regime, the actors of that regime
> MUST be disjoint from the actors under another regime. A test MUST
> enforce this for every environment in which the policy runs.

| Case | Outcome |
|---|---|
| Consent token present, valid or not | consent regime. Only DVT0001 and LVG0001 judge. |
| No consent token | PID regime. Only EUD0001, EUD0002, and ASI0001 judge. |
| Two consent tokens | denied: `CONSENT_CONTEXT_INVALID` |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: derived. The requirement serves
      [P-01](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/) and
      [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie).
      A consumer that can name its regime chooses the grondslag that it is
      judged on.
    - **Addressee**: GBO-delivered component: the reference engine and the
      source gateway. Interface agreement: which proof opens which regime.
    - **Evidence**: [PR #363](https://github.com/ICTU/GBO-demo/pull/363),
      [PR #486](https://github.com/ICTU/GBO-demo/pull/486), and
      [PR #371](https://github.com/ICTU/GBO-demo/pull/371) give this evidence:
        - The regime and the active rules are in
          [`engine.rego#L173-L181`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L173-L181).
        - The check for two tokens is in
          [`consent.rego#L44-L62`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L44-L62).
        - The tests are
          [`engine_test.rego#L227-L238`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L227-L238)
          and
          [`consent_test.rego#L438`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent_test.rego#L438).
          The disjointness test is
          [`engine_test.rego#L366-L376`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L366-L376).
        - The source gateway acts on the same proof
          ([`bron-sidecar/main.go#L185-L188`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/main.go#L185-L188)).
    - **Related**: [REQ-18](#req-18), [REQ-48](#req-48), [REQ-06](#req-06),
      [REQ-79](pseudonymization.md#req-79), [REQ-45](eudi-issuance.md#req-45),
      [F-70](../traceability/findings.md#f-70),
      [Q-15](../traceability/answered-questions.md#q-15),
      [ADR 0031](../decisions/0031-regime-from-evidence.md).
    - **Notes**:
        - The PID regime has no positive proof, only the absence of a consent
          token ([ICTU/GBO-demo#133](https://github.com/ICTU/GBO-demo/issues/133)).
          For that reason, the last two sentences of the requirement are
          necessary.
        - The disjointness test knows only the local consumers. For the
          simulation, it gives no guarantee.
        - With positive PID evidence ([REQ-45](eudi-issuance.md#req-45)),
          these two sentences lapse.
        - Grants carry no properties.
          [PR #363](https://github.com/ICTU/GBO-demo/pull/363) removed `flow`,
          and [PR #475](https://github.com/ICTU/GBO-demo/pull/475) removed
          `subject_id_type`.

### REQ-97: Every rule names the FSC services it applies to {#req-97}

> A rule of the PDP MUST name the FSC services that it applies to. The PDP MUST count a rule only on a request for one of those services. The service in the transport token that the source signed decides this. A rule MUST NOT allow fields on another service that happen to have the same key (`Type.field`). This prohibition also applies to a root field alone. A policy set MUST enforce with a test that every rule names its services.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: derived. The requirement serves
      [PSA S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting)
      ("iedere gegevensvraag verwijst eenduidig naar een dienst") and
      [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie).
      A field key is unique only within one schema. Without a service
      binding, a rule for one source gives access to another source.
    - **Addressee**: GBO-delivered component: the reference engine and the
      rules of the PDP.
    - **Evidence**: [ICTU/GBO-demo#525](https://github.com/ICTU/GBO-demo/issues/525)
      and [PR #527](https://github.com/ICTU/GBO-demo/pull/527) give this
      evidence:
        - The service binding is in
          [`engine.rego#L183-L192`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L183-L192).
        - The service comes from the token
          ([`ftvgraphql.go#L30-L33`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/mapper/ftvgraphql.go#L30-L33)).
        - [`engine_test.rego#L471-L480`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L471-L480)
          tests a root field alone.
        - [`#L497-L501`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L497-L501)
          tests that every rule names its services.
    - **Related**: [REQ-17](authorization.md#req-17), [REQ-48](#req-48),
      [REQ-74](#req-74), [F-90](../traceability/findings-closed.md#f-90).
    - **Notes**: a PDP that serves one source with one schema does not have
      the collision. The requirement stays for a PDP that serves more services,
      as in the demo.

### Removed numbers

These numbers are removed or merged into another requirement:

- REQ-05 (several independent authorization axes): merged into [REQ-48](#req-48).
- REQ-07 (policy as code, apart from the services): removed.
- REQ-33 (sector grant check at token issuance, Manager role): removed.
- REQ-34 (token binding at service call, Inway role): removed.
- REQ-36 (untrusted catalog index for scope-dependent requests): removed.
- REQ-43 (access basis from validated component identity): removed.
- REQ-47 (plural organization permissions on one service): removed.
- REQ-49 (FSC Inway forwards the body unchanged, no token-derived fields): removed.
- REQ-50 (trust classification of transport context by header prefix): merged into [REQ-18](#req-18).
- REQ-52 (AuthZEN endpoint directly behind the FSC Inway): removed. [ADR 0002](../decisions/0002-opa-rego-authzen.md) records the decision.
- REQ-53 (data transformation after authorization in a gateway): removed. For more information, see [REQ-20](pseudonymization.md#req-20), [REQ-21](pseudonymization.md#req-21), [F-30](../traceability/findings-closed.md#f-30), and [F-37](../traceability/findings-closed.md#f-37).
- REQ-56 (dispatch per contract by grant properties): removed. [REQ-74](#req-74) partly replaces it.
- REQ-70 (grant properties in a Group extension): removed.

## Query enforcement requirements {#query-enforcement}

The query enforcement requirement covers how the PDP decides on a GraphQL
query: field by field, against the schema that the source runs. The
requirement is generic. It applies to DvTP, EUDI issuance, and the ASI
route. The PEP passes the query on unchanged
([REQ-42](authorization.md#req-42)). The PDP side parses it according to
the FTV GraphQL profile for AuthZEN.

### REQ-17: The PDP decides on every field that the source runs, and denies an uncertain field list {#req-17}

> The PDP MUST determine the requested fields as the source will run
> them, against the schema of the called service. The PDP MUST decide on
> each field separately. The PDP MUST deny a field for which no rule
> applies. If it is not certain that the field list is complete and
> correct, the PDP MUST deny the whole request.

> The schema on which the PDP decides MUST have the same definition in
> every type, field, and argument as the schema that the source runs. The
> PDP MUST NOT add annotations other than those that the profile allows,
> such as authorization directives. A difference MUST be found before the PDP or
> the source goes into use with that difference.

> The source gateway that GBO delivers MUST refuse a request that is not
> in the form that the PDP judges. Thus the source runs nothing that the
> PDP did not decide. The PDP MUST be able to allow only a read query. The
> PDP MUST deny a request that changes data or opens a subscription, also
> if a rule covers its fields.

| Case | Outcome |
|---|---|
| Query cannot be parsed or is not valid against the schema | denied: `COVERAGE_UNVERIFIABLE` / `INVALID_QUERY`. The consumer sees `FIELD_NOT_PERMITTED` |
| Schema differs from the pinned schema of the service | denied: `CONFIG_ERROR` / `SCHEMA_MISMATCH` |
| A field without a rule (also introspection) | denied: `NO_APPLICABLE_RULE`. The whole request is denied |
| Source runs a schema that differs from the schema of the PDP (other type, extra argument or default, other member or enum value) | not taken into use: the check fails and names the element |
| Request reaches the source gateway in another form than the PDP judges (other path, a method other than POST, query string, other media type, `Content-Encoding` or `Upgrade`) | refused by the gateway, nothing decrypted (code) |
| Mutation or subscription | denied: `OPERATION_NOT_SUPPORTED`. The consumer sees that code (code) |
| Request without a data field (only `__typename`) | denied: `NO_DATA_FIELDS`. The consumer sees that code (code) |
| Every field allowed by a rule | allowed |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie)
          ("de beslissing kan afzonderlijke gegevens of velden toestaan of weigeren",
          "een PEP weigert standaard bij ontbrekende of onbetrouwbare beslisinformatie").
        - The additional requirements for the source access API in the
          [design principles](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
          ("een afnemer kan alleen vooraf toegestane gegevensvragen uitvoeren").
        - [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)
          and [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/).
        - [FTV GraphQL profile for AuthZEN](https://github.com/VNG-Realisatie/ftv/blob/3da8a3378a8b729f39bda09a4c7440b77a0a3457/static/documents/20260928-ftv-graphql-profile.html),
          "Transport subset" (guarantee H1) and "Ownership and drift"
          (guarantee H3).
    - **Addressee**: GBO-delivered components: the request mapper and the
      reference policy of the PDP, and the source gateway.
    - **Evidence**: [PR #480](https://github.com/ICTU/GBO-demo/pull/480),
      [PR #482](https://github.com/ICTU/GBO-demo/pull/482). Code and tests:
        - The deny on an uncertain list is in
          [`engine.rego#L129-L138`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L129-L138).
          The closed world for each field is in
          [`#L282-L284`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L282-L284).
          The tests are in [`engine_test.rego#L117-L130`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L117-L130),
          [`#L172-L186`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L172-L186),
          and [`mapper_test.go#L181-L182`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/mapper_test.go#L181-L182).
        - The subcodes of the mapper for an uncertain list are in
          [`mapper.go#L27-L43`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/mapper.go#L27-L43),
          tested in [`mapper_test.go#L19`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/mapper_test.go#L19)
          (transport) and [`#L60`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/mapper_test.go#L60)
          (body). Only a query operation passes
          ([`mapper.go#L193-L195`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/mapper.go#L193-L195)).
        - Schema equality: [PR #495](https://github.com/ICTU/GBO-demo/pull/495),
          [PR #496](https://github.com/ICTU/GBO-demo/pull/496). The comparison
          is in
          [`drift.go#L13-L18`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/drift.go#L13-L18),
          tested in [`drift_test.go#L49`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/drift_test.go#L49).
          CI enforces it
          ([`ci.yml#L184-L195`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/.github/workflows/ci.yml#L184-L195)).
        - Transport form at the source gateway:
          [`bron-sidecar/transport.go#L9-L52`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/transport.go#L9-L52).
    - **Related**: [REQ-08](authorization.md#req-08),
      [REQ-42](authorization.md#req-42), [REQ-97](authorization.md#req-97),
      [F-90](../traceability/findings-closed.md#f-90),
      [Q-14](../traceability/open-questions.md#q-14),
      [Q-16](../traceability/answered-questions.md#q-16).
    - **Notes**:
        - Design choice: the PEP (FSC Inway) passes the body on without
          parsing. The PDP parses it according to the FTV GraphQL profile.
          Thus no PEP needs to know GraphQL.
        - The consumer does not learn which field was denied, or whether an
          unknown field exists. Thus the consumer cannot probe the schema.
        - In the demo, policy and sources are in one repository. So one check
          covers both sides of schema equality.
        - The FTV GraphQL profile ("Ownership and drift") runs the check in
          two places:
            - In the pipeline of the policy bundle, before the rollout of a
              bundle.
            - In the pipeline of the source, before a schema change goes live.
              For a source with its own release cycle, this part belongs to
              the bronhouder.

### Removed numbers

- REQ-25 (consumer-facing schema carries no BSN field names): removed. See [REQ-79](pseudonymization.md#req-79) and [REQ-17](#req-17).
- REQ-26 (PEP translates between consumer schema and source schema): removed. See [REQ-79](pseudonymization.md#req-79) and [REQ-17](#req-17).
- REQ-27 (PDP enforces identity binding by AST argument inspection): removed. See [REQ-79](pseudonymization.md#req-79) and [REQ-17](#req-17).

## Data minimization requirements {#data-minimization}

The data minimization requirements apply to the source access. A request
selects fields, and a GBO component does not store source data. The
requirements are generic. They apply to DvTP, EUDI issuance, and the ASI
route. The rule that consent covers a whole data set applies only to DvTP.
That rule is [REQ-10](consent.md#req-10) on the consent page.

### REQ-08: Source access delivers only the fields that the request selects {#req-08}

> The source access MUST support selective data requests. A request MUST
> be able to state for each field which data it asks for, and the source
> MUST deliver only those fields.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S07](https://ictu.github.io/GBO-PSA/main/capabilities/#s07-gegevensontsluiting)
          ("de API ondersteunt vooraf geregistreerde, selectieve gegevensvragen").
        - [D-09](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/) and the
          additional requirements for the source access API in the
          [design principles](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/).
        - [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: interface agreement: the source access API.
    - **Evidence**: the sources in the demo offer GraphQL (source mock,
      [`graphql-server/main.go#L307`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/main.go#L307)).
      The PDP decides for each selected field
      ([REQ-17](authorization.md#req-17)).
    - **Related**: [REQ-17](authorization.md#req-17), [REQ-92](asi.md#req-92),
      [Q-16](../traceability/answered-questions.md#q-16),
      [ADR 0001](../decisions/0001-graphql-source-access.md).
    - **Notes**:
        - Design choice: GraphQL, as the PSA proposes. The API profile is not
          approved.
        - Selection alone does not minimize, because the consumer can select
          everything. The limit comes from
          [REQ-17](authorization.md#req-17).
        - The demo reads "registered in advance" as the fields that a rule
          covers. It does not read it as a list of fixed queries.

### REQ-11: A GBO component fetches source data from the source for each request and does not store it {#req-11}

> A GBO-delivered component that processes source data MUST fetch that
> data from the source for each request. It MUST NOT store the data after
> it handles that request.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design.
      [D-05](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
      ("GBO maakt geen structureel gegevensmagazijn") and
      [P-08](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: channel adapters, ASIP, and
      translation layer.
    - **Evidence**: the EUDI adapter calls the source through FSC for every
      issuance
      ([`eudi-adapter/main.go#L407-L422`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L407-L422)).
      The ASIP reads the BRP through FSC
      ([PR #527](https://github.com/ICTU/GBO-demo/pull/527)). No test shows
      that nothing is stored.
    - **Related**: [REQ-46](sources-identity.md#req-46), [REQ-92](asi.md#req-92).
    - **Notes**:
        - The adapter stores source metadata (registration, freshness). It
          does not store source data.
        - D-05 allows temporary storage if it is necessary and lawful, with a
          recorded retention period. Such an exception then goes here as a
          note.
        - Nobody checked whether the issuance server (nl-wallet, no GBO
          component) keeps attributes between the fetch and the issuance.

### Removed numbers

- REQ-09 (fields limited to a catalog set for each scope): merged into [REQ-17](authorization.md#req-17).

## Policy management guidelines {#policy-management}

The guidelines (RL-NN) cover the management side of the authorization
function: how a source manages its policy and rolls it out. They are
generic and apply to every source, whatever the trajectory (DvTP, EUDI,
ASI). They are guidelines for bronhouders and are no system requirements.
The design is in
[PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie).

### Why the items are guidelines and not requirements

The policy administration point (PAP) and the PDP are at the source. The
PDP is behind the FSC Inway of the bronhouder. The management function
(OpenFTV Manager) serves exactly that PDP. The demo runs all of this in
one compose stack. That is a demo artifact and makes no statement about
the architecture.

So all policy management is in the domain of the bronhouder:

- The policy engine is a product that the source chooses. The demo uses
  OpenFTV, but that is a demo choice and is no rule.
- The policy itself belongs to the source
  ([P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)).
- The management and deployment process around the policy is an internal
  matter of the source.

A GBO MUST on these points is a requirement on the installation of another
party. Nobody can enforce it, and it conflicts with the federated
direction of [Q-02](../traceability/answered-questions.md#q-02). For that
reason, each item is a guideline, written as SHOULD, with the reason and
the evidence. A bronhouder can use a guideline as advice, or as a
selection criterion for an engine choice. A guideline is no testable
requirement.

The promotion rule is this: a guideline becomes a requirement (REQ) only
when GBO delivers the management function itself (a reference
implementation or a shared facility). Then it is a requirement on a GBO
artifact and moves to a requirements page. In this design, policy
management stays with each source
([Q-21](../traceability/answered-questions.md#q-21), answered,
[ADR 0021](../decisions/0021-central-pap-signed-bundles.md)). Bundle
signing ([ICTU/GBO-demo#426](https://github.com/ICTU/GBO-demo/issues/426))
is not planned inside one organization. Each guideline names the extra
condition that makes it a requirement.

The requirements on GBO components are on other pages:
[REQ-59](logging-audit.md#req-59) (policy version in the decision record)
and [REQ-60](logging-audit.md#req-60) (minimization when the chain builds
the PDP input).

Terminology: the OpenFTV Manager on this page is the PAP and PIP half of
the authorization function. It is a different component from the FSC
Manager (contracts and token issuance). Always name which Manager you
mean.

### RL-01: Deliver policy as a versioned bundle instead of baking it into the PDP {#rl-01}

> A source SHOULD deliver its access policy to the PDP as an identified,
> versioned bundle, with version control as the source of the content. The
> PDP SHOULD be able to check the origin and integrity of that bundle. A
> policy baked into the PDP image, or mounted as a volume, makes every
> change a rebuild or restart. It also makes the active version hard to
> trace.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design.
      [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie)
      ("beleid is machineleesbaar, versieerbaar",
      "de ontvanger kan de authenticiteit en integriteit van gepubliceerde beleidssets controleren").
    - **Addressee**: guideline for bronhouders.
    - **Evidence**: a bundle with a version
      ([`gbo-pdp.yaml#L11-L17`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/bundles/gbo-pdp.yaml#L11-L17)).
      If `PDP_BUNDLE_MANAGER` is set, the PDP fetches the bundle
      ([`docker-compose.yml#L145-L149`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L145-L149)),
      as in `make demo-manager`.
    - **Related**: [REQ-59](logging-audit.md#req-59),
      [F-09](../traceability/findings-closed.md#f-09),
      [Q-21](../traceability/answered-questions.md#q-21),
      [ADR 0021](../decisions/0021-central-pap-signed-bundles.md).
    - **Notes**: in the default stack, the demo bakes the policy into the PDP
      image. Only `make demo-manager` delivers a bundle. Signing is missing and
      not planned ([#426](https://github.com/ICTU/GBO-demo/issues/426)).
      Inside one organization, integrity belongs to the configuration of that
      organization.
    - **Promotion rule**: if bundles come from outside the own organization,
      signing becomes a system requirement.

### RL-02: Authorize the management API with its own policy set and deny on an empty store {#rl-02}

> The management API of a policy engine (write policy, publish, attributes)
> SHOULD be authorized with its own policy set, apart from the policy that
> decides on data requests. An empty or unreadable management policy store
> SHOULD lead to a denial and SHOULD NOT give open access.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: derived. The guideline serves
      [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/). If
      management runs through the decision policy, the outcome is undefined,
      or the decision policy must open the management API.
    - **Addressee**: guideline for bronhouders, and a selection criterion for
      an engine choice.
    - **Evidence**: an own Cedar store that fails closed
      ([`docker-compose.yml#L254-L269`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L254-L269),
      [`admin.cedar`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/authz/admin.cedar)).
    - **Related**: [F-51](../traceability/findings.md#f-51),
      [ADR 0021](../decisions/0021-central-pap-signed-bundles.md).
    - **Notes**: the engine in use switches authorization off while the policy
      store is empty. This happens after a fresh install, after a failed
      migration, or with an empty volume. Check this behavior for every engine
      choice. The PDP itself does not follow this guideline: the decision
      policy covers its management endpoints. For that reason, the PDP fetches
      bundles and does not receive them
      ([`gbo-pdp.yaml#L18-L32`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/bundles/gbo-pdp.yaml#L18-L32)).
    - **Promotion rule**: the general promotion rule.

### RL-03: Separate writing from publishing, and publish with a non-personal, short-lived identity {#rl-03}

> Policy management SHOULD have read, write, and publish as separate
> rights. The API SHOULD enforce these rights. Enforcement in the user
> interface alone is not enough. Publication from version control SHOULD
> use a non-personal identity and a short-lived token. It SHOULD NOT use a
> shared administrator account or a long-lived key.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design.
      [D-11](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/)
      ("beheerrechten zijn beperkt, tijdelijk en aantoonbaar toegekend") and
      [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie)
      (owner, approver).
    - **Addressee**: guideline for bronhouders.
    - **Evidence**: roles
      ([`realm-gbo.json#L11-L19`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager-ui/keycloak/realm-gbo.json#L11-L19)),
      a deployment identity with a short-lived token
      ([`README.md#L20-L31`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager-ui/README.md#L20-L31)),
      and enforcement in the API
      ([`admin.cedar`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/authz/admin.cedar)).
    - **Related**: [REQ-59](logging-audit.md#req-59),
      [Q-21](../traceability/answered-questions.md#q-21).
    - **Notes**: the demo keeps the roles in a local realm at the facility,
      and the roles are not federated. The source decides who fills the roles,
      and through which IdP. The management interface reads rights from a
      top-level `roles` claim, which is a token form of the supplier.
    - **Promotion rule**: the general promotion rule.

### RL-04: Withdraw policy instead of deleting it, and reconcile the deployed set with version control {#rl-04}

> A source SHOULD withdraw policy that no longer applies, instead of
> deleting it. A withdrawal takes the policy out of the active bundle and
> keeps the record and the history. The publication process SHOULD
> reconcile the deployed set with version control at every
> publication. Thus what disappears from version control also disappears
> from the active set.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design.
      [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie)
      ("wijzigingshistorie", "een spoedprocedure en terugrolprocedure zijn beschikbaar").
    - **Addressee**: guideline for bronhouders.
    - **Evidence**: [`seed-openftv-manager.py#L116`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/scripts/seed-openftv-manager.py#L116)
      (`retire_stale`).
    - **Related**: [REQ-59](logging-audit.md#req-59),
      [F-52](../traceability/findings.md#f-52).
    - **Notes**: the store is cumulative. Without reconciliation, a renamed
      rule stays in the bundle ([F-52](../traceability/findings.md#f-52)). A
      store that keeps withdrawn policy is a precondition for
      [REQ-59](logging-audit.md#req-59).
    - **Promotion rule**: the general promotion rule.

### RL-05: Validate a bundle before activation, and fall back visibly to the last valid set {#rl-05}

> A bundle SHOULD be validated as a whole before publication: it compiles,
> it has no duplicate names, and the policy tests pass. The publisher
> SHOULD get feedback. A PDP that receives an invalid bundle, or cannot
> fetch a bundle, SHOULD continue to decide on the last valid set. It
> SHOULD report which version is active, and that a newer version did not
> load.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design.
      [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie)
      ("tests valideren wijzigingen vóór publicatie",
      "bij storingen vallen zij gecontroleerd terug").
    - **Addressee**: guideline for bronhouders.
    - **Evidence**: `make policy-check` runs before every start
      ([`Makefile#L92`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile#L92),
      [PR #372](https://github.com/ICTU/GBO-demo/pull/372), duplicate names in
      [PR #510](https://github.com/ICTU/GBO-demo/pull/510)). CI runs
      `opa check` and `opa test`
      ([`ci.yml#L130`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/.github/workflows/ci.yml#L130)).
      Visible fallback: not built.
    - **Related**: [REQ-59](logging-audit.md#req-59),
      [F-52](../traceability/findings.md#f-52),
      [Q-21](../traceability/answered-questions.md#q-21).
    - **Notes**: one bad rule gives no denial. It gives a failure on all
      requests ([F-52](../traceability/findings.md#f-52)). The engine in use
      reports a module that does not compile as loaded, and continues to
      decide on the previous policy
      ([#151](https://github.com/ICTU/GBO-demo/issues/151)). A PDP can report
      healthy without ever receiving a bundle
      ([PR #337](https://github.com/ICTU/GBO-demo/pull/337)).
    - **Promotion rule**: if more policy owners share one bundle or one PDP,
      an error of one owner must not stop the other. Then this guideline
      becomes a system requirement
      ([Q-21](../traceability/answered-questions.md#q-21)).

