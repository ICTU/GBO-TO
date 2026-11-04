# Deployment view

The GBO deployment in this chapter follows the infrastructure configuration
of gbo-demo v0.9.0:
[docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml),
[fsc-infra/docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml),
the [Makefile](https://github.com/ICTU/GBO-demo/blob/v0.9.0/Makefile), and
the [Helm chart](https://github.com/ICTU/GBO-demo/tree/v0.9.0/deploy/helm/gbo-app).
The demo is a reference deployment. It is not a production topology. The
[availability model](#availability-model) lists what changes for
production.

## Environments

The demo runs in two environments:

| Environment | Platform | Purpose |
|---|---|---|
| Local | Two Docker Compose projects: the main stack and `fsc-infra`. Make targets start them: `demo-minimal`, `demo-dvtp` (the default `make demo`), `demo-eudi`, `demo-full`, `demo-manager`, `demo-integrator`, and `demo-asi`. | Development and demonstration |
| Simulation | Kubernetes with the generic [gbo-app Helm chart](https://github.com/ICTU/GBO-demo/tree/v0.9.0/deploy/helm/gbo-app). Each application is one release with a Deployment or a Job, a Service, and a Gateway API HTTPRoute. It runs in the MinEZK and MinBZK tenants. | Public demo at [gbo.simulatie.datastelsel.nl](https://gbo.simulatie.datastelsel.nl/) |

Compose profiles switch on optional parts. The base (no profile) runs the
PDP and its databases, the admission register, and the toestemmingsregister.
It also runs the BD and BRP sources with their gateways, the BSNk mock, the
decryption component, the LDV logbooks, the developer portal, and
observability. Each profile adds parts to the base:

| Profile | Adds | Make target |
|---|---|---|
| `dvtp` | Toestemmingsportaal, consumer backends and frontends (Hypotheek-BV, Installatie Register with `keyper-mock`), and the LVG source and gateway | `demo-dvtp` |
| `eudi` | Issuance chain: `postgres-eudi`, source registry bootstrap and migrations, issuance migrations, configuration materializer, issuance server, and EUDI adapter | `demo-eudi` |
| `onboarding` | Source reconciler as the registry writer, with `postgres-eudi` and the registry jobs | `onboard-demo-sources` |
| `full` | `dvtp` and `eudi` together | `demo-full` |
| `integrator` | Integrator backend and the `int-*` peer in `fsc-infra` | `demo-integrator` (after `demo-dvtp` or `demo-full`) |
| `asi` | ASIP, ASI authorization server, wallet verifier, discovery stub, reference QTSP, and the `asip-*` peer in `fsc-infra` | `demo-asi` (after `demo-eudi` or `demo-full`) |
| `manager` | OpenFTV Manager, its UI, and Keycloak | `demo-manager` |

In demo v0.9.0, the ASI route runs only locally. The chart has no values
for the ASI services. Issue [#594](https://github.com/ICTU/GBO-demo/issues/594)
covers the deployment to the simulation environment. The simulation uses
its own Peer IDs, for example `0000009961MINEZK0000` for the issuance peer.

## Deployment units and network zones

The local stack separates traffic with Docker networks. The isolation of
the source gateway is a security control. The gateway acts on the consent
token after the PDP allows the request. It does not verify the token again
([REQ-81](requirements/pseudonymization.md#req-81),
[ADR-0033](decisions/0033-gateway-decrypts-after-allow.md)). The local
stack has these networks:

| Network | Members | Purpose |
|---|---|---|
| `frontend` | Browser-facing UIs | UI traffic |
| `backend` | Most services | Service traffic |
| `dvtp-onboarding` | PDP and admission register only | Keeps admission data away from other services |
| `eudi` | Issuance chain, `postgres-eudi`, reconciler, ASIP, and reference QTSP | Source registry and issuance |
| `source-gateways` | Source Inways (`bd-inway`, `brp-inway`) and source gateways | The only path to a gateway. `fsc-infra` owns this network. |
| `sources` | Source gateways, source APIs, decryption component, source logbooks, and OTel collector | Traffic of the components that serve the sources. No consumer is on this network. |
| `fsc-infra` | FSC components and the services they reach | FSC transport |

The source gateways publish no port and are only on `source-gateways` and
`sources`
([docker-compose.yml](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L829-L836)).
Two limits apply to this isolation:

- The source APIs are also on `backend` and `fsc-infra`. The FSC metadata
  services of BD and RvIG point at them directly. In the demo, a container on
  those networks can reach a source API without the PDP. Production must
  limit a source API to its gateway and its metadata path.
- The chart has no NetworkPolicy. A Kubernetes deployment needs one, or an
  equivalent control ([F-79](traceability/findings.md#f-79)).

The toestemmingsregister also relies on network placement. Its portal API
must serve only the portal backend
([REQ-39](requirements/consent.md#req-39)). The API does not
authenticate the caller. It is open whether it must
([Q-58](traceability/open-questions.md#q-58)).

The status listener of the register answers only with the FSC peer that
`cr-inway` forwards ([REQ-76](requirements/consent.md#req-76)). In the
demo, the listener is also reachable on the compose networks. Production
does not accept that exposure.

The data path runs through these peers and networks:

```mermaid
graph LR
    subgraph CONSUMERS["Consumer peers"]
        HVOUT["hv-outway (…0300)"]
        IROUT["ir-outway (…1000)"]
        INTOUT["int-outway (…1100)"]
        EDIOUT["edi-outway (…0100)"]
        ASIPOUT["asip-outway (…1200)"]
        PDPOUT["pdp-outway (…0800)"]
    end
    subgraph GATEWAYS["source-gateways network"]
        BDIN["bd-inway (…0200)"]
        BRPIN["brp-inway (…0400)"]
        SIDE[bron-sidecar]
        BRPSIDE[brp-sidecar]
        LVGSIDE[lvg-sidecar]
    end
    subgraph SOURCES["sources network"]
        GQL[graphql-server]
        BRPGQL[brp-graphql-server]
        LVGGQL[lvg-graphql-server]
        DEC[decryption-component]
        LOGS[("source logbooks")]
    end
    subgraph GBO["GBO backend"]
        PDP[openftv-pdp]
        PGFTV[("postgres-ftv: ftv_adl")]
        CRIN["cr-inway (…0700)"]
        CR[consent-register]
    end
    ONB[dvtp-onboarding-register]

    HVOUT -->|mTLS| BDIN
    IROUT -->|mTLS| BDIN
    INTOUT -->|mTLS, delegated| BDIN
    EDIOUT -->|mTLS| BDIN
    ASIPOUT -->|mTLS| BDIN
    PDPOUT -->|mTLS| CRIN --> CR
    BDIN -->|AuthZEN| PDP
    BRPIN -->|AuthZEN| PDP
    PDP --> PGFTV
    PDP -.->|dvtp-onboarding network| ONB
    BDIN --> SIDE --> GQL
    BDIN --> BRPSIDE --> BRPGQL
    BDIN --> LVGSIDE --> LVGGQL
    BRPIN --> BRPSIDE
    SIDE --> DEC
    BRPSIDE --> DEC
    LVGSIDE --> DEC
    SIDE -.-> LOGS

--8<-- "mermaid/classes.mmd"
    class HVOUT,IROUT,INTOUT,EDIOUT,ASIPOUT,PDPOUT basis
    class BDIN,BRPIN,SIDE,BRPSIDE,LVGSIDE,DEC basis
    class GQL,BRPGQL,LVGGQL source
    class LOGS,PGFTV,ONB store
    class PDP,CRIN basis
    class CR dvtp
    style CONSUMERS fill:#F4F5F7,stroke:#D1D5DB
    style GATEWAYS fill:#F4F5F7,stroke:#16A34A
    style SOURCES fill:#FFFFFF,stroke:#6F94B8,stroke-dasharray:4 3
    style GBO fill:#F4F5F7,stroke:#D1D5DB
```

### FSC peers

The FSC group `fsc-demo` runs OpenFSC v2.4.0. Each organization has its own
FSC components, a txlog API, and a Peer ID. A self-hosted directory peer and
certificate portal serve the group. The group has these peers:

| Organization | Peer ID | Units | Role |
|---|---|---|---|
| Directory peer | `…0000` | `directory-manager`, `directory-inway`, `directory-controller`, `directory-txlog-api`, `directory-ui` | Group registry. It signs service publications automatically. It signs nothing else. |
| EDI issuer (GBO) | `…0100` | `edi-manager`, `edi-outway`, `edi-controller`, `edi-txlog-api` | Consumer for EUDI issuance (`bri`, `brp`) and for the metadata services. The EUDI rules list it as a designated issuer. |
| Belastingdienst mock | `…0200` | `bd-manager`, `bd-inway`, `bd-controller`, `bd-txlog-api` | Provider of `bri`, `brp` (RvIG), `lvg`, `gbo-metadata-bd`, and `gbo-metadata-rvig`. Its Manager decides contracts through the PDP. Its Inway is the PEP. |
| Hypotheekverlener mock | `…0300` | `hv-manager`, `hv-outway`, `hv-controller`, `hv-txlog-api` | DvTP consumer of `bri` |
| BRP/RvIG mock | `…0400` | `brp-manager`, `brp-inway`, `brp-controller`, `brp-txlog-api` | Provider peer with its own PEP and contract decision. The default demo publishes RvIG on `…0200` instead. `make fsc-seed-brp` publishes `brp` here. |
| Toestemmingsregister (GBO) | `…0700` | `cr-manager`, `cr-inway`, `cr-controller`, `cr-txlog-api` | Provider of `consent-status`. The Inway has no AuthZEN hook. The Manager decides contracts through the PDP. |
| PDP (GBO) | `…0800` | `pdp-manager`, `pdp-outway`, `pdp-controller`, `pdp-txlog-api` | Consumer of `consent-status` |
| Installatie Register | `…1000` | `ir-manager`, `ir-outway`, `ir-controller`, `ir-txlog-api` | DvTP consumer of `lvg` |
| Integrator (opt-in) | `…1100` | `int-*` (profile `integrator`) | Delegated consumer of `bri` for Hypotheek-BV |
| ASIP (GBO, opt-in) | `…1200` | `asip-manager`, `asip-outway`, `asip-controller`, `asip-txlog-api` (profile `asi`) | Consumer of `brp` on `…0200` with grant link `/brp`. The admission register lists it as a system participant. |

One FSC peer can host more than one logical source. In the default demo,
the RvIG and LVG sources use the Belastingdienst peer `…0200` and its OIN.
Each source still has its own service, gateway, metadata document, and
certificate set. This shared peer is a demo shortcut. The demo therefore
does not show one OIN per bronhouder
([REQ-67](requirements/sources-identity.md#req-67)).

### ASI units

The `asi` profile runs these units:

| Unit | Host port (container) | Networks | Notes |
|---|---|---|---|
| `asi-provider` | 9424 (4020) | `backend`, `fsc-infra`, `eudi` | Reads the source registry with the reader role. Uses `asip-outway`. |
| `asi-authorization-server` | 9425 (4021) | `backend` | Keeps clients, codes, and transactions in memory |
| `asi-wallet-verifier` | 9428 (8001), internal API 8002 | `backend` | Needs the nl-wallet sources. A real wallet needs HTTPS, through a tunnel. |
| `asi-discovery-stub` | 9426 (4022) | `backend` | External role, stub |
| `qtsp-reference` | 9427 (4023) | `backend`, `eudi` | External role, demo scaffolding |

### One-shot jobs

The chart renders a task as a Job (`job.enabled: true`). The source
registry bootstrap, the source registry migrations, and the issuance
migrations are Jobs. A database lock or one transaction stops a second copy
of a Job from running at the same time. The issuance configuration
materializer is an init container. It writes `issuance_server.toml` into an
`emptyDir` for each pod. `postgres-eudi` is a Deployment with `Recreate`
and a ReadWriteOnce volume.

The rollout order is bootstrap, then migrations, then the reconciler, the
adapter, and the issuance server
([chart README](https://github.com/ICTU/GBO-demo/blob/v0.9.0/deploy/helm/gbo-app/README.md)).

## Certificates and PKI

FSC traffic is mTLS inside a self-generated PKI. cfssl serves a root CA
and an intermediate CA, with a certificate portal for CSRs. Each
organization gets a group certificate with its OIN in `serialNumber` and
its name in `O`. It also gets internal mTLS certificates
([fsc-infra/pki](https://github.com/ICTU/GBO-demo/tree/v0.9.0/fsc-infra/pki)).
The legal identity of an organization comes from its certificate
([REQ-67](requirements/sources-identity.md#req-67)).

Private keys are not in Git. Each checkout generates them again.

The EUDI and ASI material comes from two pre-provisioned development CAs:
an issuer CA and a reader CA. The Makefile refuses to generate them. A
separate privileged command mints leaf certificates under them. The
runtime gets leaves and public CA certificates. It never gets a CA private
key. The demo has the following certificate and key material:

| Material | Minted by (demo) | Held at runtime by | Production |
|---|---|---|---|
| FSC group and internal certificates, per organization | `fsc-infra/pki` bootstrap scripts (cfssl) | The FSC components of that organization | PKIoverheid ([REQ-46](requirements/sources-identity.md#req-46)) |
| PDP AuthZEN TLS certificate | `generate-pdp-cert.sh` | PDP. Inways and Managers pin it as CA. | Platform TLS (Helm: Secret `openftv-pdp-tls`) |
| Consent proof signing key | Toestemmingsregister at start, or a mounted file (`CONSENT_SIGNING_KEY_PATH`, required with a persistent store) | Toestemmingsregister | Managed key. Key rotation is an open question ([Q-55](traceability/open-questions.md#q-55)). |
| Source decryption keys | Demo keys in the gateway image, for the shared demo OIN | Source gateway and decryption component. A deployment mounts its own keys (`SUBJECT_KEYS_DIR`). | BSNk key delivery per source ([BSNK-09](requirements/pseudonymization.md#bsnk-09)). Old key versions stay available as long as consent proofs that use them are valid ([AV-09](requirements/admission.md#av-09)). |
| EUDI certificate set per source: issuer, reader, status list | `make provision-development-certificates` | Issuance server (private keys through the init step) and reconciler (public leaves only) | Qualified seal certificate in a QSCD, access and registration certificates, and a status-list certificate. Key custody is an open question ([Q-17](traceability/open-questions.md#q-17)). |
| Reference QTSP issuance set: reader, issuer, status list, callback TLS | `make provision-qtsp-issuance-certificates` | Issuance server, reference QTSP | Outside GBO. The QTSP holds its own set. |
| ASIP seal certificate | `make provision-asip-seal-certificate` (issuer CA) | ASIP | Qualified seal certificate. It is open who holds it ([Q-28](traceability/open-questions.md#q-28), [ADR-0041](decisions/0041-asi-seal-format.md)). |
| QTSP client certificate | `make provision-asip-qtsp-certificate` (reader CA) | Reference QTSP | Wallet-relying-party access certificate ([Q-35](traceability/open-questions.md#q-35)) |
| Wallet verifier reader certificates (`asi-login`, `qtsp-login`) | `make provision-asi-wallet-verifier` (reader CA) | Wallet verifier | Access certificate |
| ASI authorization server signing key | If `AZSP_SIGNING_KEY_FILE` is not set, the server makes an ephemeral key at start. | Authorization server | Managed key |

Missing or incomplete EUDI material blocks only that source
([REQ-58](requirements/eudi-issuance.md#req-58)). The issuance server
trusts the pre-production NL PID issuer CA. Its PID trust list also holds
the development issuer CA and the issuer CA of every source. This list is
too broad ([REQ-45](requirements/eudi-issuance.md#req-45)). The ASI wallet
verifier trusts a fixed list: the pre-production PID issuer and the
development issuer CA. Neither list is the EU Trusted List.

Production needs separate certificate roles per bronhouder for EUDI:
access, registration, qualified seal, and status list. It is open which
trust list anchors PuB-EAA providers
([Q-30](traceability/open-questions.md#q-30)). [Identity and
trust](concepts/identity-trust.md) and
[ADR-0023](decisions/0023-identity-convergence.md) explain the roles.

## Data stores

GBO and the demo keep data in these stores:

| Store | Backing | Content |
|---|---|---|
| Toestemmingsregister | In memory by default. Postgres is optional. | Consent records and the portal's PI and PP per `subject_ref` ([REQ-69](requirements/pseudonymization.md#req-69)). No BSN, no VI, and no VP. |
| Admission register | SQLite volume `dvtp-onboarding-data` | Participants and integrator mandates |
| Authorization Decision Log | Postgres `postgres-ftv`, database `ftv_adl`, in every profile. Readers use the SELECT-only role `adl_reader`. | One record per PDP evaluation ([REQ-71](requirements/logging-audit.md#req-71)) |
| OpenFTV Manager (opt-in) | Same `postgres-ftv` instance | Policies and the bundle |
| LDV logbooks | Seven SQLite volumes `logboek-*-data` | Processing records per controller ([REQ-72](requirements/logging-audit.md#req-72)) |
| LDV outboxes | Volume `ldv-outbox-*` per writer | Records that wait for delivery to the logbook |
| FSC txlogs | Postgres in `fsc-infra`, one database per peer | Transport records |
| Issuance server session store | Postgres `postgres-eudi` | Wallet session state |
| Source registry | Postgres `postgres-eudi`, schema `source_registry`, writer and reader roles | Candidates, statuses, immutable releases (snapshot 3.0, or 4.0 with `asi`), and the active-release pointer |
| Issuance runtime | Volume `eudi-issuance-runtime` | `issuance_server.toml`, written from the active release |
| Source documents (`file` transport) | Read-only mount `source-metadata/` | Operator-managed descriptions for sources without an endpoint |
| GBO attribute catalog | [schemas/asi-attributes.json](https://github.com/ICTU/GBO-demo/blob/v0.9.0/schemas/asi-attributes.json) | `value_schema` per ASI attribute identifier |
| ASI state | In memory, plus a register stub file | Registrations, codes, and transactions of the authorization server. Logins and pending statements of the reference QTSP. |
| Jaeger, Loki | Volumes, seven-day retention | Debug traces and logs, including the engine's console decision log |

## Observability and audit stores

The stores fall into two groups with different duties
([logging](concepts/logging.md)):

- Audit stores hold the authoritative records: the ADL for decisions, the
  LDV logbooks for processings, and the FSC txlogs for transport
  ([REQ-32](requirements/logging-audit.md#req-32)). Each peer has its own
  txlog API. This includes the GBO peers `cr`, `pdp`, and `asip`.
- Observability stores are for debugging. An OpenTelemetry collector
  receives OTLP from all services. It exports to Jaeger and to the
  developer portal's live event stream. Promtail ships container logs to
  Loki, including the engine's console decision log. Grafana shows
  dashboards. These stores are never the record of a decision.

One W3C trace ID per request joins the records. The FSC transaction ID is
recorded next to it ([ADR-0035](decisions/0035-w3c-trace-context.md)). On
the simulation platform, one observability stack runs in MinEZK, and
MinBZK shares it
([OBSERVABILITY.md](https://github.com/ICTU/GBO-demo/blob/v0.9.0/OBSERVABILITY.md)).
In demo v0.9.0, no audit store has a retention policy, an access model, or
tamper evidence ([Q-08](traceability/open-questions.md#q-08)).

## Availability model

The demo is built for inspection. Availability is not one of its goals.
The demo-grade choices in the following lists must change for production.
[Risks and technical debt](risks.md) tracks them.

Authorization and consent have these demo-grade choices:

- One PDP serves all providers. The target is a PDP per bronhouder
  ([ADR-0004](decisions/0004-federated-authorization.md)). The PDP does not
  start without its ADL database, so `postgres-ftv` runs in every profile.
- Every DvTP decision needs the consent status, live, over FSC. By
  default, the register keeps its data in memory. Production needs a
  replicated store and an availability target for this role
  ([REQ-75](requirements/consent.md#req-75)).
- The PDP pulls the admission register every 5 s. If the register is
  missing, the PDP denies contracts with `ADMISSION_REGISTER_UNAVAILABLE`.
  It denies delegated calls with `INTEGRATOR_REGISTER_UNAVAILABLE`.
- The LDV logbooks are off the critical path. If a logbook is down, the
  outbox delays the record. The request still completes.

EUDI issuance has these demo-grade choices:

- The issuance server reads its configuration at start. After a change of
  the active release, the server needs a controlled restart (state
  `rollout_required`).
- If one source is outside its stale grace period, it blocks new releases
  for all sources. Then the offer catalog answers 503 for all sources
  ([REQ-66](requirements/sources-identity.md#req-66)).
- The adapter callback must be reachable over public HTTPS. It needs caller
  authentication ([REQ-45](requirements/eudi-issuance.md#req-45)).

The ASI chain has these demo-grade choices:

- The authorization server keeps registrations in memory. After a restart,
  every QTSP registers again. Without `AZSP_SIGNING_KEY_FILE`, issued
  tokens also stop working after a restart.
- If the register is unreachable at a re-check, the client stays active
  ([Q-34](traceability/open-questions.md#q-34)).
- If the current source description or the keys of the authorization
  server are missing, the ASIP fails closed (503).

In production, the mocked services become external dependencies with their
own availability: BSNk, DigiD, and the register of relying parties.

## Traceability

- Requirements: [REQ-32](requirements/logging-audit.md#req-32),
  [REQ-45](requirements/eudi-issuance.md#req-45),
  [REQ-39](requirements/consent.md#req-39),
  [REQ-46](requirements/sources-identity.md#req-46),
  [REQ-58](requirements/eudi-issuance.md#req-58),
  [REQ-66](requirements/sources-identity.md#req-66),
  [REQ-67](requirements/sources-identity.md#req-67),
  [REQ-69](requirements/pseudonymization.md#req-69),
  [REQ-71](requirements/logging-audit.md#req-71),
  [REQ-72](requirements/logging-audit.md#req-72),
  [REQ-75](requirements/consent.md#req-75),
  [REQ-76](requirements/consent.md#req-76),
  [REQ-81](requirements/pseudonymization.md#req-81),
  [BSNK-09](requirements/pseudonymization.md#bsnk-09),
  [AV-09](requirements/admission.md#av-09)
- Findings: [F-42](traceability/findings-closed.md#f-42) (closed),
  [F-79](traceability/findings.md#f-79) (open)
- Open questions: [Q-08](traceability/open-questions.md#q-08),
  [Q-17](traceability/open-questions.md#q-17),
  [Q-28](traceability/open-questions.md#q-28),
  [Q-30](traceability/open-questions.md#q-30),
  [Q-34](traceability/open-questions.md#q-34),
  [Q-35](traceability/open-questions.md#q-35),
  [Q-55](traceability/open-questions.md#q-55),
  [Q-58](traceability/open-questions.md#q-58)
- Demo increments: [SL-10](traceability/increments.md#sl-10),
  [SL-26](traceability/increments.md#sl-26),
  [SL-28](traceability/increments.md#sl-28),
  [SL-34](traceability/increments.md#sl-34),
  [SL-34a](traceability/increments.md#sl-34a),
  [SL-34b](traceability/increments.md#sl-34b),
  [SL-34c](traceability/increments.md#sl-34c),
  [SL-35](traceability/increments.md#sl-35),
  [SL-36](traceability/increments.md#sl-36),
  [SL-37](traceability/increments.md#sl-37),
  [SL-49](traceability/increments.md#sl-49)
