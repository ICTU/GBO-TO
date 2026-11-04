# Authorization in GBO Basis

The Globaal Ontwerp calls this part "configurable authorization". Each
source has a PDP that decides on every request, field by field, with
rules written as policy. The FSC Inway of the source enforces the
decision. This page shows the parts, the order of the checks, and the
admission of parties. The [Authorization](../../concepts/authorization.md)
concept page has the detail and the links to the code.

[Overview](../index.md) › [GBO Basis](index.md) › Authorization

## Five questions, five places

Authorization answers five separate questions. Each question has its own
place in the chain:

```mermaid
flowchart LR
  req(["Request"])
  subgraph s1["① Organization"]
    direction TB
    a1("Is this a known<br/>organization?")
    b1["FSC connection<br/>mTLS + PKI certificate"]
    a1 --- b1
  end
  subgraph s2["② Permission"]
    direction TB
    a2("Can it use<br/>this service?")
    b2["FSC Manager<br/>contract after admission"]
    a2 --- b2
  end
  subgraph s5["⑤ Validity"]
    direction TB
    a5("Is the request complete<br/>and well formed?")
    b5["Request mapper<br/>field list, limits, pins"]
    a5 --- b5
  end
  subgraph s3["③ Basis"]
    direction TB
    a3("Consent<br/>or PID?")
    b3["Policy<br/>regime from evidence"]
    a3 --- b3
  end
  subgraph s4["④ Scope"]
    direction TB
    a4("Which fields, whose<br/>data, which years?")
    b4["Policy<br/>rules per field"]
    a4 --- b4
  end
  src[("Source")]
  req --> s1 --> s2 --> s5 --> s3 --> s4 --> src
--8<-- "mermaid/classes.mmd"
  class req ext
  class src source
  class a1,a2,a5,a3,a4 basis
  class b1,b2,b5,b3,b4 ext
  class a2,a5,a3,a4 zoom
  style s1 fill:#F4F5F7,stroke:#D1D5DB
  style s2 fill:#F4F5F7,stroke:#D1D5DB
  style s5 fill:#F0FDF4,stroke:#16A34A
  style s3 fill:#F0FDF4,stroke:#16A34A
  style s4 fill:#F0FDF4,stroke:#16A34A
  click a2 "#admission-of-parties" "Admission"
  click a3 "#regime-from-evidence" "Regime"
  click a4 "#the-rules" "The rules"
  click a5 "#from-query-to-decision" "Decision pipeline"
```

*Figure 1: The five authorization questions and where each one is
answered. Grey: FSC, once per connection. Green: the PDP of the source,
for every request.*
{: .caption }

Questions ① and ② belong to FSC and hold for the whole connection. The
PDP answers ③ to ⑤ again for every request
([ADR-0004](../../decisions/0004-federated-authorization.md)). No central
authorization server exists.

## The parts

The PEP, the PDP and two PIPs work together as follows:

```mermaid
flowchart LR
  out["Outway of<br/>the caller"]
  subgraph src["At the source holder"]
    direction LR
    pep("FSC Inway<br/>PEP")
    subgraph pdp["PDP: OpenFTV v0.1.0"]
      direction TB
      map("FTV GraphQL mapper<br/>query → field list")
      eng("Rego policy<br/>engine + rules")
    end
    pout("Outway<br/>of the PDP")
    gw("Source gateway")
  end
  adm[("PIP: admission register<br/>parties, mandates")]
  tr[("PIP: consent register<br/>keys, consent status")]
  adl[("ADL")]

  out -- "request + raw body" --> pep
  pep -- "AuthZEN" --> map
  map --> eng
  eng -- "status, over FSC" --> pout --> tr
  tr -. "keys (JWKS), cached 5 min" .-> eng
  adm -. "pulled every 5 s" .-> eng
  eng --> adl
  pep -- "only after allow" --> gw
--8<-- "mermaid/classes.mmd"
  class out ext
  class pep,map,eng,pout,gw basis
  class adm,adl store
  class tr dvtp
  class eng,map,tr,adm zoom
  style src fill:#FFFFFF,stroke:#6F94B8,stroke-dasharray:4 3
  style pdp fill:#F4F5F7,stroke:#16A34A
  click map "#from-query-to-decision" "Decision pipeline"
  click eng "#the-rules" "The rules"
  click tr "../../dvtp/consent-service/" "Toestemmingsvoorziening"
  click adm "#admission-of-parties" "Admission"
```

*Figure 2: PEP, PDP and PIPs at one source.*
{: .caption }

The parts have these roles:

| Part | Role |
|---|---|
| PEP | The FSC Inway. Its AuthZEN plugin sends every request with the raw body to the PDP and forwards the request only on an allow. There is no separate PEP service ([ADR-0002](../../decisions/0002-opa-rego-authzen.md)). |
| Request mapper | Turns the GraphQL body into a list of fields with their arguments, following the FTV GraphQL profile. It does nothing else ([ADR-0013](../../decisions/0013-pdp-request-mapper.md)). |
| Policy | Rego code that selects the regime, checks the consent proof and decides each field. The policy is data for the PDP, so a source holder (bronhouder) changes it without a new build. |
| PIP: consent register (toestemmingsregister) | Gives the status of a consent for every request, over FSC. Gives the keys to check the proof. DvTP only. |
| PIP: admission register | Lists the admitted parties and the mandates of integrators. OpenFTV pulls it every five seconds. |

## From query to decision

The PDP takes a fixed series of steps for each request. The first step
that fails decides the outcome:

```mermaid
flowchart TB
  in(["AuthZEN question<br/>with raw GraphQL body"])
  m{"Mapper: complete<br/>field list?"}
  r{"Regime: how many<br/>consent tokens?"}
  cv{"Consent proof:<br/>signature, claims, status OK?"}
  b["Bind rules to each field:<br/>same regime · same FSC service ·<br/>rule names the field"]
  f{"Every field granted<br/>by a rule?"}
  allow(["ALLOW<br/>query goes to the source"])
  d1(["DENY<br/>COVERAGE_UNVERIFIABLE"])
  d2(["DENY<br/>two tokens"])
  d3(["DENY<br/>consent reason"])
  d4(["DENY<br/>FIELD_NOT_PERMITTED"])

  in --> m
  m -- "no" --> d1
  m -- "yes" --> r
  r -- "two" --> d2
  r -- "one: consent regime" --> cv
  r -- "none: PID regime" --> b
  cv -- "no" --> d3
  cv -- "yes" --> b
  b --> f
  f -- "yes" --> allow
  f -- "no, or no rule at all" --> d4
--8<-- "mermaid/classes.mmd"
  class in ext
  class m,r,cv,f,b basis
  class allow basis
  class d1,d2,d3,d4 dvtp
  class cv zoom
  click cv "../../dvtp/consent-service/#the-consent-proof" "Consent proof"
```

*Figure 3: The decision pipeline of the PDP. Red: deny.*
{: .caption }

Three properties of this pipeline matter for the design:

- **Closed world.** A field that no rule names is denied
  (`NO_APPLICABLE_RULE`). There is no separate catalog of allowed
  fields: the rules are the catalog
  ([ADR-0009](../../decisions/0009-closed-world-rules.md)).
- **All or nothing.** The PDP allows the request only if it allows every
  field. It never removes fields from a query.
- **Two layers of reasons.** The consumer gets one coarse code, so it
  cannot learn the schema by trying field names. The administrator of
  the source sees the reason per field
  ([REQ-06](../../requirements/authorization.md#req-06)).

## Regime from evidence

The evidence in the request selects the regime. A declared regime or a
contract property plays no part
([ADR-0031](../../decisions/0031-regime-from-evidence.md)):

```mermaid
flowchart LR
  q{"X-GBO-Consent-Token<br/>in the request?"}
  c["Consent regime<br/>DVT0001 · LVG0001"]
  p["PID regime<br/>EUD0001 · EUD0002 · ASI0001"]
  x(["Deny"])
  q -- "one" --> c
  q -- "none" --> p
  q -- "two" --> x
--8<-- "mermaid/classes.mmd"
  class q basis
  class c dvtp
  class p eudi
  class x dvtp
```

*Figure 4: Regime selection.*
{: .caption }

The regime only selects which rules apply. Each rule still checks its own
basis: DVT0001 denies without a verified consent, and the PID rules deny
if a consent token is present.

Only consent is positive evidence. A request enters the PID regime
because it carries no token
([F-70](../../traceability/findings.md#f-70)). For that reason, the PID
rules admit only named callers: the EUDI adapter and the ASIP. These
lists must never contain a DvTP consumer. The fix in the design is a
verified PID as positive evidence
([REQ-45](../../requirements/eudi-issuance.md#req-45)).

## The rules

Demo v0.9.0 has five rules. Each rule names its regime, the FSC services
it serves, and the fields it can grant:

| Rule | Regime | Service | Grants |
|---|---|---|---|
| DVT0001 | consent | `bri` | Income declaration fields, per consented year |
| LVG0001 | consent | `lvg` | The ownership check of the LVG pilot |
| EUD0001 | PID | `bri` | Inkomensverklaring to the wallet, years 2024 and 2025 |
| EUD0002 | PID | `brp` | Akte van overlijden to the wallet |
| ASI0001 | PID | `brp` | The BRP fields behind the ASI attributes, for the ASIP only |

A rule binds to a field only on its own services. A field name such as
`Query.ingeschrevenPersoon` exists in several schemas. Without this
binding, a rule for one source grants the same field at another source
([REQ-97](../../requirements/authorization.md#req-97),
[F-90](../../traceability/findings-closed.md#f-90)).

Under consent, two checks look inside the query. The citizen must be the
placeholder `consent:identity`, never a real number. Every requested year
must have a consented scope, and a query without a year filter is denied.
The PDP checks that the citizen comes from the proof. It never learns who
the citizen is ([F-77](../../traceability/findings.md#f-77)).

## Admission of parties

Before a party can send requests, it needs an FSC contract. The FSC
Manager of the source asks the same PDP whether to sign it. The contract
policy reads the admission register and stops at the first failed check:

```mermaid
flowchart LR
  p(["Contract proposal"])
  c1{"Well-formed<br/>request?"}
  c2{"Grant type 2 or 3?"}
  c3{"Has a<br/>counterparty?"}
  c4{"Register<br/>available?"}
  c5{"Party in<br/>the register?"}
  c6{"Party<br/>active?"}
  c7{"Admitted for<br/>this source?"}
  c8{"Delegation<br/>registered?"}
  ok(["Manager signs"])
  no(["Stays proposed<br/>with a reason code"])
  p --> c1 --> c2 --> c3 --> c4 --> c5 --> c6 --> c7 --> c8 --> ok
  c1 & c2 & c3 & c4 & c5 & c6 & c7 & c8 -. "no" .-> no
--8<-- "mermaid/classes.mmd"
  class p ext
  class c1,c2,c3,c4,c5,c6,c7,c8 basis
  class ok basis
  class no dvtp
```

*Figure 5: The eight checks for a contract, in order
([ADR-0015](../../decisions/0015-contract-acceptance-by-policy.md)).*
{: .caption }

Admission is data in a register, not a rule in the policy
([REQ-61](../../requirements/admission.md#req-61)). An operator admits,
pauses or widens a party without a policy change. A refused contract stays
proposed, so the party can try again after admission
([REQ-63](../../requirements/admission.md#req-63)). The contract decides
who can connect. The request rules decide what each request can get
([REQ-62](../../requirements/admission.md#req-62)).

## Open points

The main open points in authorization are these:

- The PID regime needs positive evidence of its own
  ([F-70](../../traceability/findings.md#f-70),
  [REQ-45](../../requirements/eudi-issuance.md#req-45)).
- The ADL record does not hold the consent status that the PDP used, so a
  decision cannot be replayed from the record
  ([F-72](../../traceability/findings.md#f-72)).
- The FSC Inway of demo v0.9.0 loses the reason code on the way back to
  the consumer
  ([detail](../../concepts/authorization.md#reason-codes-two-layers)).
- How to model fields, recursion and arguments for future sources
  ([Q-14](../../traceability/open-questions.md#q-14)).

## Traceability

- Requirements: [REQ-06](../../requirements/authorization.md#req-06),
  [REQ-17](../../requirements/authorization.md#req-17),
  [REQ-18](../../requirements/authorization.md#req-18),
  [REQ-45](../../requirements/eudi-issuance.md#req-45),
  [REQ-61](../../requirements/admission.md#req-61),
  [REQ-62](../../requirements/admission.md#req-62),
  [REQ-63](../../requirements/admission.md#req-63),
  [REQ-74](../../requirements/authorization.md#req-74),
  [REQ-97](../../requirements/authorization.md#req-97)
- Findings: [F-70](../../traceability/findings.md#f-70) (open),
  [F-72](../../traceability/findings.md#f-72) (open),
  [F-77](../../traceability/findings.md#f-77) (open),
  [F-90](../../traceability/findings-closed.md#f-90) (resolved in demo)
- Open questions: [Q-14](../../traceability/open-questions.md#q-14) (open)
- Demo increments: [SL-03a](../../traceability/increments.md#sl-03a) (done),
  [SL-45](../../traceability/increments.md#sl-45) (done),
  [SL-48](../../traceability/increments.md#sl-48) (done)
