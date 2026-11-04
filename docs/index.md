# Introduction and goals

The Technisch Ontwerp (TO) is the technical design of Gemeenschappelijke
Bronontsluiting (GBO). It describes the GBO voorzieningen and
koppelvlakken. The TO goes one level deeper than the
[Globaal Ontwerp (GO)](https://ictu.github.io/GBO-GO/main/) and stays
within the kaders of the
[Projectstartarchitectuur (PSA)](https://ictu.github.io/GBO-PSA/main/).

The TO uses the [arc42](https://arc42.org/overview) template. It records
*how* the GBO components are built. For *why* GBO exists and *what* it
must do, see the [PSA inleiding](https://ictu.github.io/GBO-PSA/main/)
and the
[GO oplossingsrichting](https://ictu.github.io/GBO-GO/main/#2-voorgestelde-oplossingsrichting).

## Baseline: the demo at v0.9.0

The reference implementation
[gbo-demo](https://github.com/ICTU/GBO-demo) is the ground truth for the
behavior of GBO. This version of the TO is pinned to demo tag
[v0.9.0](https://github.com/ICTU/GBO-demo/tree/v0.9.0) (November 2, 2026).
Every statement about behavior links to code or a test at that tag.
Each divergence between the design and the implementation has a record
in one of these places:

- an [architecture decision](decisions/index.md),
- a [finding](traceability/findings.md),
- an entry in [Risks and technical debt](risks.md).

## Earlier work in the TO

The TO is the standalone reference for the technical design of GBO. It
absorbs two earlier bodies of work:

- The reference architecture v0.6.2 (archived and unpublished). The
  [ADR log](decisions/index.md) holds its decisions. This includes the
  decisions that the implementation superseded later.
- The traceability work that ran next to the demo. The TO holds its
  [requirements](requirements/index.md),
  [findings](traceability/findings.md),
  [open questions](traceability/open-questions.md),
  [demo increments](traceability/increments.md), and
  [design-to-demo matrix](traceability/matrix.md).
  [How to trace](traceability/index.md) explains how the IDs link.

The IDs did not change (REQ-NN, RL-NN, AV-NN, BSNK-NN, F-NN, Q-NN,
SL-NN). A reader who knows an old ID finds it under the same number.

## How this document is organized

The TO has three parts:

| Part | Content |
|---|---|
| arc42 sections 1 to 12 | The design: constraints, context, strategy, building blocks, runtime scenarios, deployment, crosscutting concepts, decisions, quality, risks, and glossary. |
| [Requirements](requirements/index.md) | Testable demands on what GBO builds and on its interfaces (REQ), guidelines for bronhouders (RL), candidate connection conditions (AV), and BSNk preconditions (BSNK). |
| [Traceability](traceability/index.md) | The chain from design to demo: the matrix, demo increments (SL), findings (F), open questions (Q), and feedback to standards bodies (E1 to E10). |

Each arc42 page and each ADR ends with a "Traceability" section. This
section lists the requirements, findings, open questions, and demo
increments that the page explains or depends on.

## Routes {#trajectories}

GBO gives bronhouders (government bronhouders) one technical backbone
for several gegevensstromen. A bronhouder exposes a GraphQL API behind an
FSC Inway. Every request passes the same chain: the FSC Inway as PEP, the
PDP of the source, the source gateway, and the source API. The
routes differ at the consumer edge and in the evidence that a
request carries. The evidence selects the authorization regime
([ADR-0031](decisions/0031-regime-from-evidence.md)).

gbo-demo v0.9.0 implements three routes end to end:

- **DvTP** (Delen van gegevens via Toestemming met Private
  dienstverleners). A citizen gives consent, and a private consumer
  requests source data under that consent. The consumer never holds a
  citizen identifier. An integrator can call on behalf of the consumer
  under FSC delegation
  ([ADR-0034](decisions/0034-integrator-delegation.md)). A second
  consumer pilot runs on the same chain: the Installatie Register asks
  the LVG source about ownership (rule LVG0001). See
  [DvTP query](runtime/dvtp-query.md).
- **EUDI issuance** (PuB-EAA route). A citizen discloses a PID from the
  EUDI wallet and gets an attestation from a government source. The
  bronhouder is the PuB-EAA provider. GBO operates the technical issuance
  facility ([ADR-0028](decisions/0028-pubeaa-productization.md)). The
  demo proves this route, but the PSA treats wallet support (P-06) as a
  hook outside version 1. See [EUDI issuance](runtime/eudi-issuance.md).
- **ASI verification** (eIDAS Article 45e). A QTSP verifies or retrieves
  attributes at the Authentic Source Interface, as specified in ETSI TS
  119 478 clause 6.1. The QTSP is an OAuth client and does not take part
  in FSC. The ASI provider calls the source over FSC
  ([ADR-0037](decisions/0037-asi-oauth-front-door.md)). The route is demo
  grade: it uses a stub register, development certificates, and a DigiD
  mock. See [ASI verification](runtime/asi-verification.md).

Three routes exist at design level only
([design-level scenarios](runtime/design-level.md)):

- **Gov-to-Gov**: exchange between government parties on a legal basis.
  The legal-basis regime needs its own positive evidence. No rule set
  exists for this regime.
- **SDG-OOTS**: cross-border evidence exchange through an AS4 bridge
  ([ADR-0020](decisions/0020-as4-bridge-for-oots.md)).
- **Relying-party presentation**: the citizen presents a wallet
  attestation to a relying party. This route has no GBO runtime.

For the interactiepatronen behind these routes, see the
[GO](https://ictu.github.io/GBO-GO/main/#3-interactiepatronen).

## Quality goals

The technical design has five main quality goals, in order of priority.
[Quality requirements](quality.md) refines them into testable scenarios.
Each goal has the following effect on the design:

| Priority | Quality goal | What it means for the design |
|---|---|---|
| 1 | Data minimization | The query of the consumer is the authorization object. The PDP decides on each requested field. It denies a field that no rule of the active regime covers ([REQ-17](requirements/authorization.md#req-17), [REQ-48](requirements/authorization.md#req-48)). See [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/). |
| 2 | Privacy (BSN-free) | In DvTP, the consumer gets no BSN and no other citizen identifier. The query names the subject with a placeholder. As a result, the PDP input and the decision logs hold no identity ([REQ-20](requirements/pseudonymization.md#req-20), [REQ-79](requirements/pseudonymization.md#req-79)). EUDI and ASI are an exception: the plain BSN is in the PDP input and in both decision logs ([REQ-60](requirements/logging-audit.md#req-60) not met). [ADR-0043](decisions/0043-identifiers-out-of-pdp-input.md) (proposed) records the fix. See [P-04](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/). |
| 3 | Verifiable authorization | A policy engine decides every data request. Application code does not make this decision. Each decision is allow or deny with a reason code. The consumer and the decision record get a coarse code. The operator gets the rule code per field ([REQ-06](requirements/authorization.md#req-06), [ADR-0036](decisions/0036-adl-decision-record.md)). See [S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie). |
| 4 | Traceability | One W3C trace ID links the processing records of all controllers. Next to it, the records hold the FSC transaction ID, which links the transport records ([REQ-55](requirements/logging-audit.md#req-55), [ADR-0035](decisions/0035-w3c-trace-context.md)). In demo v0.9.0, the link to the decision record behind the FSC Inway is missing ([risk R23](risks.md#r23)). See [P-12](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/). |
| 5 | Bronhouder autonomy | Sources own their schema, their service description, their decryption keys, and their policy. PAP and PDP are at the bronhouder ([ADR-0021](decisions/0021-central-pap-signed-bundles.md)). GBO keeps no copy of source data ([REQ-11](requirements/authorization.md#req-11)). See [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/). |

## Stakeholders

For the parties involved and the impact of GBO on them, see
[GO chapter 6](https://ictu.github.io/GBO-GO/main/#6-impact-op-betrokken-partijen).
The TO has three primary audiences:

- Engineers who build or integrate GBO components.
- Bronhouder teams that connect a source.
- Reviewers who check that the implementation stays within the PSA
  kaders.

## Document chain

The TO is level 3 in a chain of five documents:

| Level | Document | Role |
|---|---|---|
| 0 | [GBO site](https://ictu.github.io/GBO/) | Entry point and context |
| 1 | [Globaal Ontwerp](https://ictu.github.io/GBO-GO/main/) | System-level solution shape and interactiepatronen |
| 2 | [Projectstartarchitectuur](https://ictu.github.io/GBO-PSA/main/) | Normative principles, kaders, capabilities, and open decisions |
| 3 | Technisch Ontwerp (this document) | Technical design of components and koppelvlakken, with requirements and traceability |
| 4 | [gbo-demo](https://github.com/ICTU/GBO-demo) at [v0.9.0](https://github.com/ICTU/GBO-demo/tree/v0.9.0) | Reference implementation, ground truth for the behavior of GBO |

## Traceability

- Requirements: [REQ-06](requirements/authorization.md#req-06),
  [REQ-11](requirements/authorization.md#req-11),
  [REQ-17](requirements/authorization.md#req-17),
  [REQ-20](requirements/pseudonymization.md#req-20),
  [REQ-48](requirements/authorization.md#req-48),
  [REQ-55](requirements/logging-audit.md#req-55),
  [REQ-60](requirements/logging-audit.md#req-60),
  [REQ-79](requirements/pseudonymization.md#req-79),
  [REQ-106](requirements/consent.md#req-106)
- Findings: [F-54](traceability/findings.md#f-54) (open),
  [F-70](traceability/findings.md#f-70) (open),
  [F-87](traceability/findings.md#f-87) (open)
- Open questions: [Q-21](traceability/answered-questions.md#q-21) (answered),
  [Q-28](traceability/open-questions.md#q-28) (open),
  [Q-37](traceability/open-questions.md#q-37) (open)
- Demo increments: [SL-26](traceability/increments.md#sl-26) (done),
  [SL-28](traceability/increments.md#sl-28) (done),
  [SL-50](traceability/increments.md#sl-50) (done),
  [SL-51](traceability/increments.md#sl-51) (done)
