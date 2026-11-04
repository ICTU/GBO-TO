# Policy rules and their management

The Globaal Ontwerp names "Beleidsregels" as a block of GBO Basis: policy
rules decide who can get which data. Each source holder (bronhouder) owns, writes and
publishes the policy that its own PDP evaluates. GBO supplies a reference
policy set, the engine choice, and five guidelines, but no central policy
service ([ADR-0021](../../decisions/0021-central-pap-signed-bundles.md)).
The [Policy lifecycle](../../concepts/policy-lifecycle.md) concept page
and the [Policy distribution](../../runtime/policy-distribution.md)
runtime page have the detail and the links to the code.

[Overview](../index.md) › [GBO Basis](index.md) › Policy rules

## The policy set

```mermaid
flowchart LR
  pep("FSC Inway<br/>PEP")
  mgr("FSC Manager<br/>of the source")
  subgraph set["Policy set: policies/"]
    direction LR
    entry("authz.rego<br/>entrypoint")
    subgraph eng["Engine and readers"]
      direction TB
      e("engine.rego<br/>regime, binding,<br/>closed world")
      con("consent.rego<br/>consent PIP")
      pins("graphql_schemas.rego<br/>schema pins")
    end
    subgraph rules["Rules"]
      direction TB
      r1("rules/dvtp<br/>DVT0001 · LVG0001")
      r2("rules/eudi<br/>EUD0001 · EUD0002")
      r3("rules/asi<br/>ASI0001")
    end
    auto("fsc/autosign.rego<br/>contract policy")
  end
  tr[("Toestemmings-<br/>register")]
  pep -- "AuthZEN" --> entry --> e
  e --> r1 & r2 & r3
  e --- con
  e --- pins
  con -. "status over FSC" .-> tr
  mgr -- "AuthZEN autosign" --> auto
--8<-- "mermaid/classes.mmd"
  class pep,mgr,entry,e,con,pins,r1,r2,r3,auto basis
  class tr dvtp
  class r1,r2,r3,auto,con,pins zoom
  style set fill:#FFFFFF,stroke:#16A34A
  style eng fill:#F4F5F7,stroke:#16A34A
  style rules fill:#F4F5F7,stroke:#16A34A
  click r1 "../authorization/#the-rules" "The rules"
  click r2 "../authorization/#the-rules" "The rules"
  click r3 "../authorization/#the-rules" "The rules"
  click auto "../authorization/#admission-of-parties" "Admission"
  click con "../../dvtp/consent-service/#the-consent-proof" "Consent proof"
  click pins "../source-access/#the-pdp-copy-of-the-schema" "Schema copy"
```

*Figure 1: The policy set of demo v0.9.0. Thick border: click to zoom in.*
{: .caption }

All policy is Rego in version control, with tests next to the rules. The
set has four parts:

| Part | Files | Role |
|---|---|---|
| Entrypoint | `authz.rego` | The package that OpenFTV evaluates. It passes only `allow` and the coarse reason to OpenFTV. It allows the source-metadata fetch for two known peers on the two metadata services |
| Engine and readers | `gbo/engine.rego`, `gbo/lib.rego`, `gbo/consent.rego`, `gbo/graphql_schemas.rego` | Generic machinery: regime and service binding, the closed world, reason codes, the consent proof, and the schema pins |
| Rules | `gbo/rules/dvtp/`, `gbo/rules/eudi/`, `gbo/rules/asi/` | One package per access verdict: DVT0001, LVG0001, EUD0001, EUD0002, ASI0001 |
| Contract policy | `fsc/autosign.rego` | Decides for the FSC Manager of the source whether to sign a contract ([ADR-0015](../../decisions/0015-contract-acceptance-by-policy.md)) |

A new access verdict is a new rule file with tests. The engine does not
change. The policy is data for the PDP, so a source holder changes it
without a new build. The contract policy is a separate rule set from the
request policy, in the same bundle
([REQ-62](../../requirements/admission.md#req-62)).

Rules use data with four lifecycles. Some data is in the rule itself, for
example the years of EUD0001 and the actor lists of the PID rules. The
schema digests are in the bundle. The admission register is a PIP that
the PDP pulls every five seconds. The consent proof and its status arrive
with each request.

## Ownership

The policy belongs to the source
([P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/)). The
question who can manage and publish the policy of a source holder has an
answer: the source holder itself
([Q-21](../../traceability/answered-questions.md#q-21), October 28,
2026). Each party has a fixed role:

| Party | Does | Never does |
|---|---|---|
| Source holder | Writes, approves and publishes its own policy. Runs its own PAP and PDP. | Hands its policy to a central PAP |
| GBO | Supplies the reference policy set, the engine choice and the guidelines RL-01 to RL-05. | Sets requirements on the policy installation of another party |
| Another organization that builds or hosts bundles | Signs the bundles. The PDP verifies them. | Publishes without a signature across the organization boundary |

PSA S06 sets the norm for publication control. The norm asks for an
owner, an approver, an effective date, a change history, tests before
publication, and an emergency and rollback procedure. Authority over
policy is with competent public parties, so the management practices are
guidelines. A guideline becomes a requirement only if GBO delivers the
management setup itself.

## From version control to the PDP

A policy change goes through a fixed series of checks before the PDP
uses it:

```mermaid
flowchart LR
  a(["Author edits<br/>a .rego file"])
  g[("policies/<br/>with tests")]
  c["make policy-check<br/>Rego only, unique names,<br/>opa check"]
  t["make policy-test<br/>opa fmt, opa test"]
  ci["CI<br/>same checks, generated<br/>files up to date"]
  d["Distribution<br/>mount or bundle"]
  p("PDP compiles<br/>the whole set")
  ok(["Decides,<br/>writes ADL records"])
  stop(["PDP does not start"])
  br(["Every decision fails<br/>no visible fallback"])
  a --> g --> c --> t --> ci --> d --> p
  p -- "compiles" --> ok
  c -- "fails" --> stop
  p -- "one bad module" --> br
--8<-- "mermaid/classes.mmd"
  class a ext
  class g store
  class c,t,ci ext
  class d,p,ok basis
  class stop,br dvtp
  class d zoom
  click d "#two-distribution-modes" "Distribution modes"
```

*Figure 2: From version control to the PDP. Red: failure.*
{: .caption }

The PDP compiles the policy set as a whole. One bad module does not give a
deny. It breaks every decision
([F-52](../../traceability/findings.md#f-52)). The demo had this fault
several times:

- A stale policy declared the same package as an existing rule. Every
  request got HTTP 500.
- A non-Rego file under `policies/` removed every policy after it in walk
  order.
- A second file with the same name replaced the first, because the loader
  keys policies by file name.
- At hot reload, the PDP reports a module that does not compile as loaded,
  while the old policy keeps deciding
  ([#151](https://github.com/ICTU/GBO-demo/issues/151)).

`make policy-check` is the local safety net. It refuses non-Rego files and
duplicate file names, and then it runs `opa check`. Every make target that
starts the PDP depends on it. `make policy-test` adds `opa fmt --diff` and
`opa test`. CI repeats these steps. CI also checks that two generated
files are up to date: the schema pins and the rule list of the developer
portal.

The contract policy is in the same set. One broken module therefore also
stops the admission of new parties. Its package name is fixed
(`doelbinding.auto_sign_contract`). If someone renames it, every contract
stays pending without a signal.

## Two distribution modes

The demo gets the policy set to the PDP in one of two modes:

```mermaid
flowchart LR
  git[("policies/<br/>version control")]
  subgraph mount["Mount mode: default"]
    direction TB
    bm["Bind mount<br/>./policies"]
    pdp1("PDP<br/>hot reload")
    bm --> pdp1
  end
  subgraph bundle["Bundle mode: opt-in"]
    direction TB
    seed["seed-openftv-manager.py<br/>deployment identity"]
    kc["Keycloak<br/>realm gbo"]
    mgr("OpenFTV Manager<br/>PAP, Cedar on its API")
    pg[("postgres-ftv<br/>policy + audit trail")]
    pdp2("PDP<br/>pulls at start")
    seed -- "short-lived token" --> kc
    seed -- "write, retire" --> mgr
    mgr --> pg
    pdp2 -- "GET /v1/bundle/gbo-pdp" --> mgr
  end
  git --> bm
  git --> seed
--8<-- "mermaid/classes.mmd"
  class git store
  class bm,seed mock
  class kc ext
  class mgr,pdp1,pdp2 basis
  class pg store
  class pdp1,mgr zoom
  style mount fill:#F4F5F7,stroke:#16A34A
  style bundle fill:#F4F5F7,stroke:#16A34A
  click pdp1 "../../../runtime/policy-distribution/#mount-mode" "Mount mode"
  click mgr "../../../runtime/policy-distribution/#bundle-mode" "Bundle mode"
```

*Figure 3: The two distribution modes. Version control is the source of
the content in both.*
{: .caption }

The two modes differ as follows:

| | Mount mode | Bundle mode |
|---|---|---|
| How the PDP gets the policy | The image carries `policies/`, and compose bind-mounts `./policies` over it | The PDP pulls bundle `gbo-pdp` from the OpenFTV Manager, because `PDP_BUNDLE_MANAGER` is set |
| When a change takes effect | At each edit, by hot reload | At the next PDP start. `make manager-seed` restarts the PDP |
| Started by | Every `make demo*` target | `make demo-manager`, then `make manager-seed` |
| Version | None | The bundle has an ID and a version |

Bundle mode has these properties:

- The PDP pulls, and nothing pushes. The PDP guards its own management
  endpoints with the decision policy, which denies every request that is
  not a data request. A push therefore gets HTTP 403
  ([F-51](../../traceability/findings.md#f-51)).
- The seed script retires policy and does not delete it. It gives every
  policy that left version control the tag `gbo-retired`. A delete fails
  upstream on a foreign key to the audit trail.
- Cedar policies authorize the API of the OpenFTV Manager, apart from the
  Rego decision policy. The PDP shows no identity, so `pdp-bundle.cedar`
  allows only GET on the one bundle path.
- The Manager seeds its Cedar policies only into an empty store. An
  existing volume does not pick up a changed Cedar file.
- The realm has the roles `admin`, `author` and `auditor`. Publication
  uses a non-personal deployment identity with a token of 30 minutes. In
  demo v0.9.0, no Cedar policy grants `author` an action, so only `admin`
  writes and publishes.
- The bundle has no signature. Inside one organization, signing is not
  planned ([#426](https://github.com/ICTU/GBO-demo/issues/426)). If a
  source holder lets another organization build or host its bundles,
  signing and verification become a requirement
  ([F-09](../../traceability/findings-closed.md#f-09)).

Two components have the name Manager. The OpenFTV Manager manages policy.
The FSC Manager manages contracts and issues access tokens.

## Guidelines for source holders {#guidelines-for-bronhouders}

GBO gives five guidelines for policy management. Each guideline has a
status in demo v0.9.0:

| Guideline | Demo status |
|---|---|
| [RL-01](../../requirements/authorization.md#rl-01) Deliver policy as a versioned bundle. Do not bake it into the PDP | Opt-in only. The default mounts the policies. No signature |
| [RL-02](../../requirements/authorization.md#rl-02) Authorize the management API with its own policy set. Deny on an empty store | Built for the OpenFTV Manager (Cedar). The PDP itself does not follow it ([F-51](../../traceability/findings.md#f-51)) |
| [RL-03](../../requirements/authorization.md#rl-03) Separate writing from publishing. Publish with a non-personal, short-lived identity | Deployment identity built. The `author` role grants no action |
| [RL-04](../../requirements/authorization.md#rl-04) Withdraw policy, and do not delete it. Reconcile with version control | Built: `retire_stale` at every seed |
| [RL-05](../../requirements/authorization.md#rl-05) Validate a bundle before activation. Fall back visibly to the last valid set | Local check built (`make policy-check`). Visible fallback not built |

Source metadata has the lifecycle that RL-05 asks for: validation before
activation, atomic promotion, and rollback
([F-59](../../traceability/findings-closed.md#f-59),
[Source configuration](source-configuration.md)). For policy, this
lifecycle is a backlog item.

## Compared with the Globaal Ontwerp

The demo follows the Globaal Ontwerp in the PEP, PDP and PIP chain with
AuthZEN and Rego. It differs in the management of the policy:

| Topic | Globaal Ontwerp | Demo v0.9.0 |
|---|---|---|
| Place of the PAP | A PAP manages the policies and distributes them to the PDPs of the source holders | A PAP and a PDP at each source holder. No central PAP ([ADR-0021](../../decisions/0021-central-pap-signed-bundles.md)) |
| Bundles | Signed policy bundles | A bundle with an ID and a version, without a signature. Signing only across an organization boundary |
| Policy language | ODRL in the PAP | Rego for every decision, and Cedar for the API of the OpenFTV Manager ([Q-78](../../traceability/open-questions.md#q-78)) |

## Open points

The main open points in policy management are these:

- The PDP guards its own management endpoints with the decision policy
  ([F-51](../../traceability/findings.md#f-51)).
- One broken module stops every decision and the admission of new
  parties, without a visible fallback
  ([F-52](../../traceability/findings.md#f-52)).
- The decision record does not name the policy version that decided
  ([REQ-59](../../requirements/logging-audit.md#req-59),
  [Records](records.md)).
- The actor lists of the PID rules are policy data. They must stay apart
  from the consent consumers in every environment
  ([F-70](../../traceability/findings.md#f-70)).
- How the reference policy shows that it is not tied to one language or
  engine ([Q-78](../../traceability/open-questions.md#q-78)).

## Traceability

- Requirements: [RL-01](../../requirements/authorization.md#rl-01),
  [RL-02](../../requirements/authorization.md#rl-02),
  [RL-03](../../requirements/authorization.md#rl-03),
  [RL-04](../../requirements/authorization.md#rl-04),
  [RL-05](../../requirements/authorization.md#rl-05),
  [REQ-59](../../requirements/logging-audit.md#req-59),
  [REQ-62](../../requirements/admission.md#req-62)
- Findings: [F-09](../../traceability/findings-closed.md#f-09) (closed),
  [F-51](../../traceability/findings.md#f-51) (open),
  [F-52](../../traceability/findings.md#f-52) (open),
  [F-59](../../traceability/findings-closed.md#f-59) (closed),
  [F-70](../../traceability/findings.md#f-70) (open)
- Open questions: [Q-21](../../traceability/answered-questions.md#q-21) (answered),
  [Q-78](../../traceability/open-questions.md#q-78) (open)
- Demo increments: [SL-13](../../traceability/increments.md#sl-13) (done),
  [SL-44](../../traceability/increments.md#sl-44) (done),
  [SL-45](../../traceability/increments.md#sl-45) (done)
