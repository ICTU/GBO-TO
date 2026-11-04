# Logging and audit requirements

These requirements cover the three records of GBO: the decision record (ADL), the processing record (LDV), and the trace that links them. For the design, see [Logging, audit and traceability](../concepts/logging.md).

This page has the following parts:

- [Decision audit requirements](#decision-audit)
- [Processing logging requirements](#processing-logging)
- [Observability requirements](#observability)

## Decision audit requirements {#decision-audit}

The decision audit requirements cover the record of authorization
decisions. They set rules for these topics:

- the Authorization Decision Log (ADL) of Logius
- the protection of the record
- the policy version that the record names
- the personal data that the record can hold

The requirements are generic. They apply to DvTP, EUDI issuance, and the
ASI route. [Processing logging](logging-audit.md#processing-logging) covers the record
of each processing (LDV). [Observability](logging-audit.md#observability) covers the
trace ID.
### REQ-32: Audit records are protected, complete, and stored apart from operational logs {#req-32}

> Decision records (ADL) and processing log records (LDV) MUST be
> protected against change and deletion. This protection applies to
> anyone who does not manage them. They MUST NOT be sampled. They MUST have
> their own retention period and access, independent of those of
> operational logs and traces. Operational logs MAY carry the same trace
> ID, but they are no audit source.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
          ("maatregelen beschermen loggegevens tegen ongeautoriseerde wijziging en verwijdering",
          "afspraken regelen bewaartermijnen, toegang, inzage en vernietiging expliciet").
        - [LDV, behavior of the application](https://logius-standaarden.github.io/logboek-dataverwerkingen/#gedrag-van-applicatie)
          (no log sampling).
        - [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the logbook and the components
      that write to it. Interface and audit agreement: the decision record at
      the source.
    - **Evidence**:
        - The ADL is in Postgres, apart from the console log in Loki
          ([`docker-compose.yml#L117-L125`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L117-L125),
          [PR #337](https://github.com/ICTU/GBO-demo/pull/337)).
        - Readers get only SELECT
          ([`adl-reader.sql#L17`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/adl/adl-reader.sql#L17),
          [PR #373](https://github.com/ICTU/GBO-demo/pull/373)).
        - The logbook in the demo has write and read, and no change or delete
          ([`handler.go#L49-L53`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek/internal/httpapi/handler.go#L49-L53)).
          That logbook is a stand-in for the logbook of the controller
          (Verantwoordelijke). It is no GBO component.
        - Retention period and tamper resistance at storage level: not built.
    - **Related**: [REQ-71](#req-71), [REQ-72](logging-audit.md#req-72),
      [REQ-123](admission.md#req-123), [Q-08](../traceability/open-questions.md#q-08),
      [ADR 0036](../decisions/0036-adl-decision-record.md).
    - **Notes**: retention periods and read access are open in
      [Q-08](../traceability/open-questions.md#q-08). Nobody tested whether the
      writing role of the PDP can change its own records.

### REQ-59: The decision record names the policy version that decided {#req-59}

> Every decision record ([REQ-71](#req-71)) MUST carry the identity and
> version of the policy set that made the decision
> (`adl.core.policies`). For every policy set, it MUST be traceable which
> version became active when. The source decides how it forms that
> version (bundle ID with version, commit hash, image version).

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
          ("autorisatiebeslissingen verwijzen naar de toegepaste beleidsversie en relevante informatie over de grondslag").
        - [ADL `adl.core.policies`](https://logius-standaarden.github.io/authorization-decision-log/#adl-core-policies).
        - [PSA S06](https://ictu.github.io/GBO-PSA/main/capabilities/#s06-beleidsbeheer-distributie)
          (start date and change history).
    - **Addressee**: interface and audit agreement: every PDP that decides on
      a data request.
    - **Evidence**: not built, and there is no demo issue for it. The bundle
      carries a version
      ([`gbo-pdp.yaml#L17`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-manager/bundles/gbo-pdp.yaml#L17)),
      but that version does not reach the ADL record
      ([PR #373](https://github.com/ICTU/GBO-demo/pull/373)). Records carry
      `policies: 0`.
    - **Related**: [REQ-71](#req-71), [F-53](../traceability/findings-closed.md#f-53),
      [Q-08](../traceability/open-questions.md#q-08),
      [Q-21](../traceability/answered-questions.md#q-21),
      [RL-01](authorization.md#rl-01), [RL-04](authorization.md#rl-04).
    - **Notes**: without this field, nobody can link the history of the policy
      (who published which version) to a decision. In the default stack, the
      policy comes from the PDP image. In that case, the version must also be
      traceable.

### REQ-60: Logging contains no BSN that the processing does not need {#req-60}

> A GBO-delivered component MUST keep the BSN and other directly
> identifying data out of its operational logs and spans. Some
> identifying values in the PDP input are not necessary for the
> decision. A component that builds the PDP input MUST keep such a value
> out of the input, or replace it before it sends the input. If that
> fails, the request does not continue. Masking in the decision log MUST
> NOT be the only safeguard.

| Case | Outcome |
|---|---|
| Operational log or span | no BSN. A data subject only as pseudonym or opaque reference |
| PDP input, DvTP | no identity: a placeholder, which the source replaces only after the consent |
| Decryption or replacement fails | the request does not reach the source |
| PDP input, EUDI and ASI | no BSN (not met in demo v0.9.0, see the notes) |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design.
      [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
      ("logging bevat niet meer persoonsgegevens dan noodzakelijk") and
      [P-03, P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the GBO components and the
      chain that builds the PDP input. It is no requirement on the policy
      engine of the source.
    - **Evidence**:
        - DvTP: [PR #469](https://github.com/ICTU/GBO-demo/pull/469), tested
          in
          [`substitution_test.go#L76`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/substitution/substitution_test.go#L76),
          [`#L247`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/substitution/substitution_test.go#L247),
          and
          [`ldv_test.go#L385`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/ldv_test.go#L385).
        - Logs and spans in the ASI chain:
          [`e2e_test.go#L425`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/qtsp-reference/e2e_test.go#L425)
          ([PR #535](https://github.com/ICTU/GBO-demo/pull/535)) and
          [`trace_test.go#L110`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/trace_test.go#L110)
          ([PR #530](https://github.com/ICTU/GBO-demo/pull/530)).
        - For the other components, there is no automatic check.
    - **Related**: [REQ-20](pseudonymization.md#req-20),
      [REQ-21](pseudonymization.md#req-21), [REQ-71](#req-71),
      [REQ-72](logging-audit.md#req-72),
      [F-54](../traceability/findings.md#f-54),
      [F-72](../traceability/findings.md#f-72),
      [Q-08](../traceability/open-questions.md#q-08),
      [ADR 0043](../decisions/0043-identifiers-out-of-pdp-input.md).
    - **Notes**:
        - Design choice: leave the value out before the policy engine, instead
          of masking it inside the engine. From the outside, a masking rule
          that does not work looks the same as one that works
          ([F-54](../traceability/findings.md#f-54)).
        - In the EUDI channel and the ASI route, the BSN is in the PDP input,
          and so in the decision record
          ([`eudi-adapter/source_metadata.go#L272-L273`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata.go#L272-L273),
          [`asi-provider/internal/graphqlsource/source.go#L94`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/source.go#L94)).
        - Demo issue [#368](https://github.com/ICTU/GBO-demo/issues/368)
          decides how the BSN goes out. If the team chooses masking there,
          this requirement must change.

### REQ-71: Every authorization decision is in an ADL-conformant decision record, and that record is the audit source {#req-71}

> Every authorization decision on a data request MUST be recorded in a
> record according to the Logius standard Authorization Decision Log. The
> record MUST make it possible to replay the decision. It holds the
> request, the answer, and the policy version ([REQ-59](#req-59)). It also
> holds the answer of every information source consulted during the
> evaluation (`adl.core.information`). A reference to that answer can
> replace the answer. The reference MUST then stay available as long as
> the record exists.

> If the request passes an FSC Inway or Outway, `adl.fsc.transaction_id`
> MUST be set. Where more decision logs exist side by side, the ADL record
> MUST be the designated audit source. Other streams MUST NOT be an audit
> source.

| Case | Outcome |
|---|---|
| Allowed or denied | one record, with outcome and reason code |
| Evaluation fails | also one record |
| Decision depends on the consent status | the status answer is in or with the record |
| Request through FSC | `adl.fsc.transaction_id` next to `trace_id` |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
          (Authorization Decision Log to record authorization decisions).
        - [GO, reused building blocks](https://ictu.github.io/GBO-GO/main/)
          (ADL 1.0.0).
        - [ADL](https://logius-standaarden.github.io/authorization-decision-log/)
          ([`adl.core.information`](https://logius-standaarden.github.io/authorization-decision-log/#adl-core-information),
          [`adl.fsc.transaction_id`](https://logius-standaarden.github.io/authorization-decision-log/#adl-fsc-transaction_id)).
        - FR-31 criterion 1.
    - **Addressee**: interface and audit agreement: the PDP of every source,
      whatever the product. GBO-delivered component: what GBO delivers to the
      PDP (request mapping, policy).
    - **Evidence**: the ADL in Postgres is mandatory
      ([`docker-compose.yml#L125`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L125),
      [PR #337](https://github.com/ICTU/GBO-demo/pull/337)). The demo reads it
      as the audit source ([PR #373](https://github.com/ICTU/GBO-demo/pull/373)).
      The demo does not meet these parts:
        - transaction ID and trace behind the Inway
          ([#369](https://github.com/ICTU/GBO-demo/issues/369))
        - policy version ([REQ-59](#req-59))
        - status answer in the record ([F-72](../traceability/findings.md#f-72))
    - **Related**: [REQ-32](#req-32), [REQ-55](logging-audit.md#req-55),
      [REQ-59](#req-59), [REQ-60](#req-60), [REQ-06](authorization.md#req-06),
      [F-41](../traceability/findings-closed.md#f-41),
      [F-53](../traceability/findings-closed.md#f-53),
      [F-63](../traceability/findings-closed.md#f-63),
      [F-72](../traceability/findings.md#f-72),
      [Q-08](../traceability/open-questions.md#q-08),
      [Q-25](../traceability/open-questions.md#q-25),
      [ADR 0036](../decisions/0036-adl-decision-record.md).
    - **Notes**:
        - The detail for each field (which fields were allowed or denied) does
          not need to be in the record. It follows from a replay, and the ADL
          prefers a reference to a copy.
        - A reference brings a retention duty for its source
          ([Q-08](../traceability/open-questions.md#q-08)).
        - The ADL is working version 1.0.0. Pin the version in a conformance
          claim.
        - The policy fetches the consent status during evaluation. For that
          reason, a replay from (input, policy, data) needs the status answer
          in the record.

### Removed numbers

- REQ-31 (persistent, correlatable audit record for each authorization decision): merged into [REQ-71](#req-71).

## Processing logging requirements {#processing-logging}

The processing logging requirement covers the record of each processing
of personal data. [Decision audit](logging-audit.md#decision-audit) covers the decision
side (ADL). The requirement on this page covers the processing side. It is
generic and applies to DvTP, EUDI issuance, and the ASI route.

The Logius standard Logboek Dataverwerkingen (LDV) asks for a log record
for every processing (Dataverwerking), for each controller
(Verantwoordelijke). Only trace metadata crosses an organization boundary.
The decision of a PDP is no processing. A transformation at the source,
such as the decryption by the source gateway, is a processing
([F-64](../traceability/findings-closed.md#f-64)).

### REQ-72: A GBO component that processes personal data writes an LDV log record for each processing at its controller {#req-72}

> Every GBO-delivered component that processes data of a data subject
> (Betrokkene) MUST write a log record according to Logboek
> Dataverwerkingen for each action. It MUST write the record to the
> logbook of the controller of that processing. The trace ID in that
> record MUST follow from [REQ-55](logging-audit.md#req-55). There MUST be
> a separate log record for each data subject. A further data subject of
> the same processing hangs as a child under the first.

> The field `dpl.core.data_subject_id` MUST name the data subject in an
> identifier space of the controller itself, with an explicit
> `data_subject_id_type`. It MUST NOT name the data subject with the
> BSN. The field `dpl.core.processing_activity_id` MUST refer to a
> versioned, resolvable processing activity. A component that calls another party during the
> processing MUST set `dpl.read.nextLogbookId` to the read API of that
> party. Only trace metadata crosses an organization boundary.

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [LDV](https://logius-standaarden.github.io/logboek-dataverwerkingen/#gedrag-van-applicatie)
          and its
          [read extension](https://logius-standaarden.github.io/logboek-extensie-lezen/).
        - [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
          (LDV as functional frame,
          "iedere component legt de gebeurtenissen vast die voor zijn verantwoordelijkheid relevant zijn").
        - [GO, reused building blocks](https://ictu.github.io/GBO-GO/main/).
        - FR-31 criterion 1.
    - **Addressee**: GBO-delivered component: source gateway (source gateway),
      consent register (toestemmingsregister) and consent portal (toestemmingsportaal), EUDI adapter, and ASIP.
      The logbook and the source application of a bronhouder belong to that
      bronhouder ([P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)).
    - **Evidence**: [ICTU/GBO-demo#302](https://github.com/ICTU/GBO-demo/issues/302),
      [PR #366](https://github.com/ICTU/GBO-demo/pull/366),
      [PR #469](https://github.com/ICTU/GBO-demo/pull/469). Code and tests:
        - The source gateway logs decryption and forwarding
          ([`bron-sidecar/ldv_test.go#L309`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/ldv_test.go#L309)).
        - The EUDI adapter names the holder without a BSN
          ([`eudi-adapter/ldv_test.go#L159`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/ldv_test.go#L159))
          and points to the logbook of the source
          ([`#L471`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/ldv_test.go#L471)).
        - Child records:
          [`brp-graphql-server/ldv_query.go#L219`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/ldv_query.go#L219).
        - Write side: [PR #303](https://github.com/ICTU/GBO-demo/pull/303). A
          processing that cannot be logged delivers nothing
          ([`bron-sidecar/ldv_test.go#L475-L492`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/ldv_test.go#L475-L492)).
    - **Related**: [REQ-32](logging-audit.md#req-32),
      [REQ-55](logging-audit.md#req-55), [REQ-60](logging-audit.md#req-60),
      [REQ-76](consent.md#req-76), [AV-02](admission.md#av-02),
      [AV-10](admission.md#av-10),
      [F-64](../traceability/findings-closed.md#f-64),
      [F-68](../traceability/findings.md#f-68),
      [F-69](../traceability/findings-closed.md#f-69),
      [Q-08](../traceability/open-questions.md#q-08),
      [Q-25](../traceability/open-questions.md#q-25),
      [Q-72](../traceability/open-questions.md#q-72),
      [ADR 0026](../decisions/0026-ldv-integration.md).
    - **Notes**:
        - The `ldv-logboek` in the demo is a stand-in for the logbook of the
          controller, and is no GBO component. It refuses a record with a BSN
          ([`validate.go#L148`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek/internal/ldv/validate.go#L148),
          tested in [`validate_test.go#L94`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek/internal/ldv/validate_test.go#L94))
          or with an activity that does not resolve
          ([`validate.go#L119`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek/internal/ldv/validate.go#L119)).
          That is therefore no evidence for this requirement.
        - LDV allows `BSN` as a type. "Never the BSN" is a stricter rule from
          S09 and P-04.
        - The register of processing activities is a stand-in for each logbook
          ([`register.go#L28`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-logboek/internal/ldv/register.go#L28)).
          A real register is missing. For GBO components it belongs with the
          management organization ([Q-08](../traceability/open-questions.md#q-08)).
        - `dpl.core.foreign_operation.processor` is a URL made from the FSC
          peer ID or the grant hash. It identifies the caller, but nothing
          resolves behind it.
        - In demo v0.9.0, the ASIP writes no log records.
        - Design choice: a processing delivers data only after its log record
          is durable locally (outbox). An outage of the logbook does not stop
          the chain
          ([`graphql-server/main.go#L394-L398`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/main.go#L394-L398),
          [`bron-sidecar/main.go#L541-L549`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/main.go#L541-L549)).
        - It is open whether GBO components write attributes outside the LDV
          core: [Q-72](../traceability/open-questions.md#q-72).

### Removed numbers

- REQ-73 (a consumer sends trace context and records the transaction ID of every source call): removed, replaced by connection condition [AV-01](admission.md#av-01).

## Observability requirements {#observability}

The observability requirement covers the correlation of logs and traces
over the chain. Each request has one trace ID, and the components record
the FSC transaction ID next to it. The requirement is generic. It applies
to DvTP, EUDI issuance, and the ASI route.
[Decision audit](logging-audit.md#decision-audit) covers the decision record.
[Processing logging](logging-audit.md#processing-logging) covers the processing
record.

### REQ-55: One trace ID per request across the whole chain, and the transaction ID can be linked to it {#req-55}

> Every GBO-delivered component MUST take the trace ID of an incoming
> request unchanged from W3C Trace Context (`traceparent`). It MUST record
> the span of the caller as parent. It MUST send `traceparent` with every
> outgoing call. Every record that the component writes about the request
> (processing log record, operational log record, span) MUST carry that
> trace ID. The `Fsc-Transaction-Id` MUST NOT replace an incoming trace. A
> component that starts or receives an FSC transaction MUST record the
> transaction ID next to the trace ID.

| Case | Outcome |
|---|---|
| Request with `traceparent` | trace ID taken over, and the span of the caller is parent. An `Fsc-Transaction-Id` that comes with it does not change the trace ID |
| Request without `traceparent`, with `Fsc-Transaction-Id` | the transaction ID MAY be the trace ID |
| Entry component without `traceparent` that starts a transaction itself | MAY choose its trace ID equal to that transaction ID |
| Processing with more than one FSC hop | one trace ID, several transaction IDs. The link runs through the records that carry both, and does not depend on equality |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design:
        - [PSA S09](https://ictu.github.io/GBO-PSA/main/capabilities/#s09-logging-audit-traceerbaarheid)
          ("iedere gegevensvraag krijgt een verzoekidentificator die over de hele keten bruikbaar is",
          standardized correlation and trace context).
        - [LDV `trace_id`](https://logius-standaarden.github.io/logboek-dataverwerkingen/#trace_id).
        - [W3C Trace Context](https://www.w3.org/TR/trace-context/).
        - FR-31 criterion 1 (traceable correlation references across
          components).
    - **Addressee**: GBO-delivered component.
    - **Evidence**: [PR #366](https://github.com/ICTU/GBO-demo/pull/366),
      [PR #530](https://github.com/ICTU/GBO-demo/pull/530). Code and tests:
        - Order of sources for the trace ID:
          [`tracecontext.go#L78`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/tracecontext.go#L78),
          tested in [`tracecontext_test.go#L100`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/tracecontext_test.go#L100)
          and [`#L86`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/tracecontext_test.go#L86).
        - Take-over: source gateway
          [`bron-sidecar/ldv_test.go#L415`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/ldv_test.go#L415),
          EUDI adapter [`eudi-adapter/ldv_test.go#L308`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/ldv_test.go#L308),
          and ASIP [`graphqlsource/trace_test.go#L96`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/asi-provider/internal/graphqlsource/trace_test.go#L96).
        - Pass-on:
          [`outway.go#L45-L50`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/outway/outway.go#L45-L50).
        - Transaction ID on the span behind the Inway:
          [`graphql-server/main.go#L385-L387`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/main.go#L385-L387).
        - Trace ID in operational logs:
          [`slogctx.go#L15-L24`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/graphql-server/slogctx.go#L15-L24).
        - Parent only within the same trace
          ([PR #329](https://github.com/ICTU/GBO-demo/pull/329),
          [`tracecontext.go#L166-L192`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/tracecontext.go#L166-L192),
          tested in [`tracecontext_test.go#L146-L170`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ldv-client/tracecontext_test.go#L146-L170)).
        - The PDP passes trace and transaction ID on to the register
          ([PR #305](https://github.com/ICTU/GBO-demo/pull/305),
          [`consent.rego#L190-L200`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L190-L200)).
    - **Related**: [REQ-71](logging-audit.md#req-71),
      [REQ-72](logging-audit.md#req-72),
      [AV-01](admission.md#av-01),
      [F-16](../traceability/findings-closed.md#f-16),
      [F-39](../traceability/findings-closed.md#f-39),
      [F-41](../traceability/findings-closed.md#f-41),
      [F-67](../traceability/findings-closed.md#f-67),
      [ADR 0035](../decisions/0035-w3c-trace-context.md).
    - **Notes**:
        - Behind the FSC Inway, the decision record does not meet this
          requirement. The Inway gives the PDP no `traceparent`, and gives the
          transaction ID only as `X-Request-Id`. So the ADL record gets its own
          trace and no `adl.fsc.transaction_id`
          ([F-41](../traceability/findings-closed.md#f-41),
          [#369](https://github.com/ICTU/GBO-demo/issues/369)). That is
          behavior of FSC and the policy engine. The fix lies upstream.
        - In demo v0.9.0, the operational logs of the source gateway, the EUDI
          adapter, and the ASIP do not carry a trace ID.
        - Design choice: logs and traces are joined on identifier equality.
          The join does not use timestamps.
        - Consent issuance and the later query are separate units of work, with
          separate traces. The `consent_id` joins them
          ([F-16](../traceability/findings-closed.md#f-16)).

### Removed numbers

- REQ-16 (end-to-end `traceparent` propagation): merged into [REQ-55](#req-55).
- REQ-28 (logs and traces can be reconstructed by a shared identifier for each request): merged into [REQ-55](#req-55).
- REQ-29 (no BSN in observability logs): merged into [REQ-60](logging-audit.md#req-60).
- REQ-54 (peer transaction log and portal correlation by `Fsc-Transaction-Id`): merged into [REQ-55](#req-55).

