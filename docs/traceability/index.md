# How to trace

This TO is the reference for what GBO builds, the reasons for it, and the
points that are open. From any kind of information in the TO, you can
follow the chain to the other kinds. The TO connects five kinds of
information:

| Kind | ID | Question it answers | Where |
|---|---|---|---|
| Architecture decision | ADR-NNNN | What did the GBO team choose, and which alternatives did it refuse? | [Decision log](../decisions/index.md) |
| Requirement | REQ-NN, RL-NN, AV-NN, BSNK-NN | What must the result do, and how does a test check it? | [Requirements](../requirements/index.md) |
| Demo increment | SL-NN | Which demo work proved it, and with which PRs? | [Demo increments](increments.md) |
| Finding | F-NN | What did the demo build show about the design? | [Open findings](findings.md), [closed findings](findings-closed.md) |
| Open question | Q-NN | What must another forum decide, and what does the TO assume until then? | [Open questions](open-questions.md), [answered questions](answered-questions.md) |

Two more pages support the chain:

- The [design to demo matrix](matrix.md) takes each element of the GO,
  the PSA, FR-DvTP v0.9, and the EUDI regulation. For each element, it
  records whether the demo covers it.
- [Standards feedback](standards-feedback.md) lists the open points in
  ETSI TS 119 478 (E1 to E10) that the ASI route found.

## The chain

```mermaid
graph LR
    ADR[Architecture decision<br/>ADR-NNNN] -->|serves| REQ[Requirement<br/>REQ / RL / AV / BSNK]
    REQ -->|proved by| SL[Demo increment<br/>SL-NN + demo PRs]
    SL -->|exposed| F[Finding<br/>F-NN]
    F -->|lands in| REQ
    F -->|lands in| ADR
    F -->|needs a decision| Q[Open question<br/>Q-NN]
    Q -->|blocks| ADR
    ARC[arc42 section<br/>building blocks, runtime, concepts] -->|explains| ADR
    ARC -->|explains| SL

--8<-- "mermaid/classes.mmd"
    class ADR,REQ,SL,F,Q store
    class ARC ext
```

Each kind of item in the chain carries these links:

- A decision serves one or more requirements. An accepted decision has
  evidence in the demo. A *proposed* decision waits for an open question.
- A requirement names its source, its addressee, and its evidence in the
  demo. The source is the GO, the PSA, FR-DvTP, or the demo itself.
- A demo increment is a bounded piece of demo work. It names its demo PRs
  and the requirements, findings, and questions that it produced.
- A finding names its trigger, what it showed, and where it landed: a
  requirement, a decision, a risk, or an open question.
- An open question names the forum that must answer it. It also names the
  working assumption that the demo and this TO use until then.

Every arc42 page and every ADR ends with a *Traceability* section. That
section lists the IDs that the page explains or depends on.

## Start points

The first step depends on where you start:

| You start at | Do this |
|---|---|
| A part of the demo | Find the component in the [building block view](../building-blocks/components.md) or the flow in the [runtime view](../runtime/index.md). Its *Traceability* section names the decisions, requirements, and increments. |
| A demo increment | Open its entry in [Demo increments](increments.md). *Explained in* links the TO section. *Produced* links the requirements, findings, and questions. |
| An open finding | Open its entry in [Findings](findings.md). Read the summary first. The block *Evidence, impact and proposal* links the requirement, decision, or question. [Coverage](coverage.md#findings) lists every page that cites the finding. |
| An open question | Open its entry in [Open questions](open-questions.md). The summary gives the question and the working assumption. The block below it names the forum that decides. [Coverage](coverage.md#open-questions) lists the decisions that the question blocks. |
| A decision | Read the ADR. [Coverage](coverage.md#decision-chains) shows its full chain in one row. |
| A requirement | Open it from the [list of all requirements](../requirements/index.md). *Evidence* links the demo test or code. [Coverage](coverage.md#requirements) lists the pages that explain the requirement. |

### Example: the consumer has no citizen identifier

The chain for this example has six steps:

1. The runtime page [DvTP query](../runtime/dvtp-query.md) shows that the
   consumer sends a placeholder. After the allow, the source gateway puts
   the source's own value in place of the placeholder.
2. The decision is [ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md),
   with the consent proof in [ADR-0032](../decisions/0032-consent-proof.md).
3. The decision serves [REQ-21](../requirements/pseudonymization.md#req-21),
   [REQ-79](../requirements/pseudonymization.md#req-79), and
   [REQ-80](../requirements/pseudonymization.md#req-80).
4. The demo work is increment [SL-51](increments.md#sl-51), with its
   demo PRs.
5. Three findings are open against the decision:
    - [F-76](findings.md#f-76): what the consumer records about "this
      person".
    - [F-77](findings.md#f-77): the PDP checks that the subject comes from
      the proof. The PDP does not check who the subject is.
    - [F-79](findings.md#f-79): "after the decision" holds only if nothing
      but the Inway reaches the gateway.
6. One decision waits: who is the BSNk participant
   ([Q-49](open-questions.md#q-49))? The proposed
   [ADR-0040](../decisions/0040-route-d-citizen-recognition.md) records the
   working assumption (route D).

## Baseline and maintenance

- **Demo baseline**: [gbo-demo v0.9.0](https://github.com/ICTU/GBO-demo/tree/v0.9.0)
  (November 2, 2026). Links to demo code use this tag. A few historical
  evidence links pin an earlier demo commit.
- **Status of the registers**: November 2, 2026. On that date, 34 findings
  and 61 open questions are open or partly answered.
- **Numbers**: numbers are never reused. A withdrawn or removed
  requirement keeps its line in the
  [list of removed numbers](../requirements/index.md).
- **When the demo changes**: make these four updates:
    1. Update the requirement *Evidence*.
    2. Add or close findings.
    3. Update the increment.
    4. Update the *Traceability* section of the pages that explain the
       change.
- **Generated page**: `scripts/gen_traceability.py` generates
  [Coverage](coverage.md). CI runs the script with `--check`. The script
  fails in two cases:
    - A page links an ID that no register defines.
    - No TO page or decision cites an open finding or an open question.
