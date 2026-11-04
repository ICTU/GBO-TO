# Building block view

GBO has one base and three channels. GBO Basis sits at every source holder (bronhouder)
and opens the source in one standard way. The DvTP, EUDI and OOTS
channels each serve a different kind of consumer, and GBO Basis feeds all
three. This picture is the overview of the
[Globaal Ontwerp](https://ictu.github.io/GBO-GO/main/#overzicht-voorgestelde-oplossing),
with the state of gbo-demo v0.9.0 added.

Each block with a thick border is clickable and zooms in one level. The
levels go from this overview, to one page per block, to the
[component catalog](components.md) with the code.

```mermaid
flowchart LR
  subgraph source holder["Source holder"]
    direction LR
    bron[("Government source<br/>BRP · BD · LVG · …")]
    subgraph gbo["GBO Basis"]
      direction TB
      cfg("Source configuration<br/>source metadata, registry")
      core("Generic source access<br/>FSC · GraphQL · PBAC")
      tools("GBO tools<br/>translation layer<br/><i>design only</i>")
    end
  end
  subgraph eudi["EUDI wallet channel"]
    direction LR
    asi("ASI provider<br/>verify / retrieve")
    pubeaa("PuB-EAA provider<br/>attestation issuance")
    qtsp["QTSP<br/>(QEAA)"]
    wallet["EUDI wallet"]
  end
  subgraph oots["OOTS channel"]
    direction LR
    ootsa("OOTS adapter<br/>semantic mapping<br/><i>design only</i>")
    ootsb["Basisinrichting OOTS"]
    eu["EU government<br/>SDG portal"]
  end
  subgraph dvtp["DvTP channel"]
    direction LR
    tv("Consent facility<br/>portal + register")
    pp["Pseudonymization facility<br/>BSNk PP"]
    dv["Private<br/>service provider"]
  end
  burger["Citizen"]

  cfg --- core
  core --- tools
  bron -- "source API (GraphQL)" --- gbo
  gbo -- "GraphQL over FSC" --- asi & pubeaa & ootsa & dv
  asi -- "verify · retrieve" --- qtsp
  qtsp -- "OpenID4VCI" --- wallet
  pubeaa -- "OpenID4VCI" --- wallet
  ootsa -- "GraphQL" --- ootsb
  ootsb -- "eDelivery/AS4" --- eu
  gbo -. "consent status (PIP)" .- tv
  tv -. "consent proof" .- dv
  tv -- "at consent only" --- pp
  wallet --- burger
  eu --- burger
  dv --- burger

--8<-- "mermaid/classes.mmd"
  class cfg,core basis
  class tools planned
  class asi,pubeaa eudi
  class ootsa planned
  class tv dvtp
  class pp,dv,qtsp,wallet,ootsb,eu ext
  class bron,burger source
  class cfg,core,tv,pp,asi,pubeaa,ootsa zoom
  style source holder fill:#FFFFFF,stroke:#6F94B8,stroke-dasharray:4 3
  style gbo fill:#F4F5F7,stroke:#16A34A
  style eudi fill:#F4F5F7,stroke:#D1D5DB
  style oots fill:#F4F5F7,stroke:#D1D5DB
  style dvtp fill:#F4F5F7,stroke:#D1D5DB

  click core "gbo-basis/" "GBO Basis: generic source access"
  click cfg "gbo-basis/source-configuration/" "Source configuration"
  click tv "dvtp/" "DvTP channel"
  click pp "../concepts/pseudonymization/" "Pseudonymization"
  click pubeaa "eudi/pubeaa/" "PuB-EAA provider"
  click asi "eudi/asi/" "ASI provider"
  click ootsa "oots/" "OOTS channel"
```

*Figure 1: GBO Basis feeds three channels. Thick border: click to zoom in.
Dashed: design only, not built in demo v0.9.0.*
{: .caption }

## The blocks

The overview has seven GBO blocks. Five of them run in the demo:

| Block | What it does | In demo v0.9.0 | Zoom in |
|---|---|---|---|
| Generic source access | Opens a source over FSC with GraphQL. The PDP of the source decides on every request, field by field. | Built | [GBO Basis](gbo-basis/index.md) |
| Source configuration | The source describes its own services. GBO validates the description and activates it as a release. | Built | [Source configuration](gbo-basis/source-configuration.md) |
| GBO tools | Help a source holder that cannot offer GraphQL, through a translation layer. | Design only | [ADR-0027](../decisions/0027-onboarding-toolkit.md) |
| Consent facility (toestemmingsvoorziening) | The citizen gives, views and revokes consent. The register signs a consent proof for the consumer. | Built, with a DigiD mock | [DvTP channel](dvtp/index.md) |
| PuB-EAA provider | Issues an attestation from source data to the wallet of the citizen. | Built on the nl-wallet stack | [PuB-EAA provider](eudi/pubeaa.md) |
| ASI provider | Lets a QTSP verify or retrieve an attribute at the source (eIDAS article 45e). | Built, demo grade | [ASI provider](eudi/asi.md) |
| OOTS adapter | Answers an EU evidence request with source data. | Design only | [OOTS channel](oots.md) |

The pseudonymization facility (pseudonimiseervoorziening) (BSNk PP) and the QTSP are not GBO
components. GBO uses them. The demo runs a mock of BSNk PP.

## How GBO Basis feeds every channel

Every channel reaches the source in the same way. A channel component
calls the source through its own FSC Outway. At the source, GBO Basis
decides and only then asks the source:

```mermaid
flowchart LR
  subgraph ch["Channel (one of three)"]
    direction TB
    c1("Consumer backend<br/>DvTP")
    c2("EUDI adapter<br/>PuB-EAA")
    c3("ASIP<br/>ASI")
  end
  out["Outway of the caller"]
  subgraph gb["GBO Basis at the source"]
    direction LR
    pep("FSC Inway<br/>PEP")
    pdp("PDP<br/>policy per field")
    gw("Source gateway")
  end
  api[("Source API")]
  subgraph rec["Records"]
    direction TB
    adl[("ADL<br/>decision")]
    ldv[("LDV<br/>processing")]
    txl[("FSC txlog<br/>transport")]
  end

  c1 & c2 & c3 --> out
  out -- "1 · mTLS + FSC token" --> pep
  pep -- "2 · AuthZEN question" --> pdp
  pdp -- "3 · allow or deny" --> pep
  pep -- "4 · only after allow" --> gw
  gw -- "5 · query" --> api
  pdp -.-> adl
  api -.-> ldv
  pep -.-> txl

--8<-- "mermaid/classes.mmd"
  class c1 ext
  class c2,c3 eudi
  class out,pep,pdp,gw basis
  class api source
  class adl,ldv,txl store
  class pep,pdp,gw zoom
  style gb fill:#F4F5F7,stroke:#16A34A
  click pep "gbo-basis/" "GBO Basis"
  click pdp "gbo-basis/authorization/" "Authorization"
  click gw "gbo-basis/source-access/" "Source access"
```

*Figure 2: One path to the source for all channels. Dotted lines: the
three audit records.*
{: .caption }

The channels differ in the evidence that a request carries. The evidence
selects the rules that the PDP applies, and it decides how the source
learns who the citizen is:

| Channel | Evidence in the request | Rules | How the source gets the citizen |
|---|---|---|---|
| DvTP | A consent proof, signed by the consent register (toestemmingsregister) | DVT0001, LVG0001 | The source decrypts its own value from the proof |
| PuB-EAA issuance | No consent proof: PID regime | EUD0001, EUD0002 | The adapter puts the BSN from the PID of the wallet in the query |
| ASI | No consent proof: PID regime | ASI0001 | The ASIP puts the BSN from its access token in the query |

For the regime rule, see
[ADR-0031](../decisions/0031-regime-from-evidence.md). For the five rules,
see [Authorization](gbo-basis/authorization.md#the-rules).

## Two ways down

This view goes down by block: from a channel to its components. The
[crosscutting concepts](../concepts/authorization.md) go down by theme.
The following table shows where each theme lives in the blocks:

| Theme | GBO Basis | DvTP | PuB-EAA | ASI |
|---|---|---|---|---|
| [Authorization](gbo-basis/authorization.md) | PEP, PDP and rules | DVT0001, LVG0001 | EUD0001, EUD0002 | ASI0001, and an OAuth server of its own |
| [Consent](../concepts/consent.md) | Status check per request | Consent facility | Not used | Login is the approval |
| [Pseudonymization](../concepts/pseudonymization.md) | Source gateway decrypts | Values made at consent | BSN from the PID | BSN in the token |
| [Source onboarding](../concepts/source-onboarding.md) | Source description, registry | Not used | `eudi` capability | `asi` capability |
| [Identity and trust](../concepts/identity-trust.md) | FSC certificates, admission | Admission register | Certificate set per source | QTSP register, seal |
| [Logging and audit](../concepts/logging.md) | ADL, LDV, txlog | Logbook of the consent facility | Logbook of the adapter | ADL and source logbook. The ASIP writes no LDV records |

## Diagram legend

All diagrams in this TO use the colors of the Globaal Ontwerp:

```mermaid
flowchart LR
  a("GBO Basis"):::basis
  b("GBO DvTP component"):::dvtp
  c("GBO EUDI or OOTS component"):::eudi
  d[("Source or citizen")]:::source
  e["External party or system"]:::ext
  f[("Register, log, store")]:::store
  g["Demo scaffolding or mock"]:::mock
  h("Design only"):::planned
--8<-- "mermaid/classes.mmd"
```

*Figure 3: Diagram legend.*
{: .caption }

## Traceability

- Requirements: [REQ-04](../requirements/authorization.md#req-04),
  [REQ-44](../requirements/authorization.md#req-44),
  [REQ-46](../requirements/sources-identity.md#req-46),
  [REQ-74](../requirements/authorization.md#req-74)
- Findings: [F-70](../traceability/findings.md#f-70) (open),
  [F-87](../traceability/findings.md#f-87) (open)
- Open questions: [Q-10](../traceability/answered-questions.md#q-10) (answered),
  [Q-17](../traceability/open-questions.md#q-17) (open)
- Demo increments: [SL-28](../traceability/increments.md#sl-28) (done),
  [SL-51](../traceability/increments.md#sl-51) (done)
