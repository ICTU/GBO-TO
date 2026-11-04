# Authorization

GBO authorizes every data request with policy-based access control. A
policy engine decides, and the FSC Inway of the source enforces the
decision. The authorization model on this page is the model that
gbo-demo v0.9.0 builds. The model realizes capability
[S05](https://ictu.github.io/GBO-PSA/main/capabilities/#s05-autorisatie).

The model follows from seven architecture decisions:

- [ADR-0002](../decisions/0002-opa-rego-authzen.md): OPA/Rego in OpenFTV,
  the FSC Inway as PEP, and AuthZEN with the FTV GraphQL profile.
- [ADR-0004](../decisions/0004-federated-authorization.md): five
  concerns, federated evaluation, and no central authorization server.
- [ADR-0009](../decisions/0009-closed-world-rules.md): closed-world rules,
  bound by regime and service.
- [ADR-0013](../decisions/0013-pdp-request-mapper.md): the request mapper
  only maps.
- [ADR-0015](../decisions/0015-contract-acceptance-by-policy.md): FSC
  contract acceptance by policy.
- [ADR-0031](../decisions/0031-regime-from-evidence.md): the regime
  follows from the evidence.
- [ADR-0032](../decisions/0032-consent-proof.md): the policy verifies
  the consent proof.

For the consent proof, see [Consent](consent.md). For how the source fills
in the citizen after the decision, see
[Pseudonymization](pseudonymization.md). For how policy gets to the PDP,
see [Policy lifecycle](policy-lifecycle.md).

## Five concerns

Authorization answers five separate questions. Each question has its own
decision maker, protocol, and moment. Each concern has its own enforcement
point:

| # | Concern | Question | Enforced by |
|---|---|---|---|
| ① | Organization identity | Is this a legitimate organization? | mTLS with PKIoverheid certificates at every FSC connection ([Identity and trust](identity-trust.md)) |
| ② | Organization permission | Can this organization use this service? | FSC contract and access token, issued by the FSC Manager of the provider. Contract acceptance is a policy decision on the admission register ([Admission and contract acceptance](#admission-and-contract-acceptance)) |
| ③ | Access basis | Is there a consent, or a verified PID of the citizen? | PDP policy: the regime follows from the evidence ([Regime selection](#regime-selection)). The policy verifies the consent proof and gets the status online ([Consent verification in policy](#consent-verification-in-policy)). The design has a Gov-to-Gov regime on a legal basis. Demo v0.9.0 does not build it |
| ④ | Data scope | Which fields, records, and years can the source return? | PDP policy: per-field rules, the subject placeholder, and the year filter ([Rule model](#rule-model)) |
| ⑤ | Request validity | Is the request well-formed and complete? | Request mapper: FTV GraphQL profile, limits, and schema pins ([Query mapping](#query-mapping-ftv-graphql-profile)). The source gateway accepts only the judged request shape. Demo v0.9.0 does not build rate limiting ([Risks](../risks.md)) |

No central authorization server exists. Concerns ① and ② are in the FSC
layer, federated per organization. The PDP of the source evaluates
concerns ③ to ⑤ for each request. With the integrator path, concern ②
also has a part at request time: the mandate check
([ADR-0034](../decisions/0034-integrator-delegation.md)).

## PEP, PDP, PIP

```mermaid
flowchart LR
    C[Consumer Outway] -->|mTLS + FSC token| IN
    subgraph SRC[Bronhouder]
        IN[FSC Inway = PEP]
        subgraph PDP[OpenFTV PDP v0.1.0]
            MAP[FTV GraphQL mapper]
            POL[Rego policy]
        end
        OUT[PDP Outway]
        GW[Source gateway<br/>bron-sidecar]
        API[Source API]
    end
    REG[(Admission register)]
    CR[(Toestemmingsregister)]
    IN -->|AuthZEN evaluation, raw body| MAP
    MAP -->|field list| POL
    POL -->|status over FSC| OUT
    OUT --> CR
    POL -.->|JWKS, cached| CR
    REG -.->|PIP pull every 5 s| POL
    IN -->|only after allow| GW
    GW --> API

--8<-- "mermaid/classes.mmd"
    class C,IN,MAP,POL,OUT,GW basis
    class API source
    class REG store
    class CR dvtp
    style SRC fill:#FFFFFF,stroke:#6F94B8,stroke-dasharray:4 3
    style PDP fill:#F4F5F7,stroke:#16A34A
```

The components in the diagram have these roles:

- The PEP is the FSC Inway of the source. Its AuthZEN plugin sends every
  request, with its raw body, to the PDP. The plugin forwards the request
  only on allow
  ([`fsc-infra/docker-compose.yml#L769-L775`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/fsc-infra/docker-compose.yml#L769-L775)).
  No separate PEP service exists ([F-35](../traceability/findings-closed.md#f-35)).
  The PEP passes the request unchanged and never parses it
  ([REQ-42](../requirements/authorization.md#req-42)).
- The PDP is OpenFTV release v0.1.0 with embedded OPA/Rego. The demo
  builds it from the tag and patches in the FTV GraphQL mapper
  ([`Dockerfile#L3-L9`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/Dockerfile#L3-L9)).
  The mapper builds the field list and does nothing else
  ([`ftvgraphql.go#L1-L13`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/mapper/ftvgraphql.go#L1-L13)).
  It does not verify consent, does not call BSNk, and reads no flow. The
  policy establishes every fact that it decides on
  ([REQ-18](../requirements/authorization.md#req-18)).
- PIP 1 is the toestemmingsregister. During evaluation, the policy calls
  the register for the status of the consent. The call goes over FSC,
  through the own Outway of the PDP
  ([`docker-compose.yml#L141-L142`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docker-compose.yml#L141-L142)).
  The policy gets the verification keys (JWKS) directly from the register.
- PIP 2 is the admission register. Every 5 seconds, OpenFTV pulls the
  participants as `data.entities.dvtp_participant`. Each participant has
  the attributes `name`, `active`, `allowed_source_peer_ids`, and
  `acts_for`
  ([`dvtp-onboarding.yaml`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/openftv-pdp/pip-pull/dvtp-onboarding.yaml)).
  The contract policy reads this data. The request policy reads it for
  integrator mandates (`acts_for`).

The same PDP serves two enforcement points. Each point has its own policy
tree. FSC Inways send data requests (package `authz`). FSC Managers send
contract proposals (package `doelbinding.auto_sign_contract`).

The EUDI adapter and the ASIP call the source over FSC, like every other
consumer. They translate between protocols. The decision on source data
stays with the PDP of the source
([REQ-44](../requirements/authorization.md#req-44)).

The source gateway is behind the Inway. Only the Inway can reach the
gateway. As a result, the gateway does all its work after the decision
([REQ-04](../requirements/authorization.md#req-04),
[ADR-0033](../decisions/0033-gateway-decrypts-after-allow.md)).

## Regime selection

The PDP judges a request under one of two regimes. The evidence in the
request selects the regime
([REQ-74](../requirements/authorization.md#req-74),
[ADR-0031](../decisions/0031-regime-from-evidence.md)). A declared regime
plays no part. Each kind of evidence has its own outcome:

| Evidence in the request | Regime | Rules that bind |
|---|---|---|
| One `X-GBO-Consent-Token`, verified or not | consent | DVT0001, LVG0001 |
| No consent token | PID | EUD0001, EUD0002, ASI0001 |
| Two consent tokens | — | denied: `CONSENT_CONTEXT_INVALID` |

The selection code is in
[`engine.rego#L168-L181`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L168-L181).
The code that reads the token is in
[`consent.rego#L44-L62`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L44-L62).
FSC grants carry no properties. No component reads a `flow`.

The regime only decides which reasons the PDP reports. Access depends on
the rules, because each rule still checks its own basis. If no verified
consent is present, DVT0001 denies. If a consent token is present, the
PID rules deny.

Only consent is positive evidence
([F-70](../traceability/findings.md#f-70)). A request enters the PID
regime because no token is present. This asymmetry has two consequences:

- The PID regime needs its own positive evidence: a verified PID
  disclosure, bound to the subject of the query
  ([REQ-45](../requirements/eudi-issuance.md#req-45)). In demo v0.9.0,
  the EUDI adapter does not authenticate the callback that carries the PID
  ([#133](https://github.com/ICTU/GBO-demo/issues/133)).
- The actor lists of the PID rules (`designated_issuers`, `asip`) must
  stay disjoint from the consent consumers in every environment. If the
  lists overlap, a consumer can skip consent: it leaves out the token. A
  test checks this condition for the seeded peers only
  ([`engine_test.rego#L366-L376`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L366-L376)).

A Gov-to-Gov regime on a legal basis needs its own positive evidence. It
cannot be a third regime that the absence of evidence defines.

### Wallet approval is not a legal basis

In DvTP, the consent of the citizen is the legal basis for delivery to a
private consumer. In the EUDI route, the citizen chooses in the wallet
which data to present. The ARF says that this approval is never a legal
basis for the relying party ([F-83](../traceability/findings.md#f-83)).
In the ASI route, the citizen approves each request by logging in
([REQ-90](../requirements/asi.md#req-90)). This approval is not a stored,
revocable consent either.

As a result, no single "consent" covers all routes. The PID regime cannot
use a DvTP consent as its basis. The consent regime cannot use a wallet
presentation as its basis. If a consumer gets data both through DvTP and
through the wallet, it needs its own legal basis for the wallet route.
The GO and the PSA do not separate the two terms.

## Rule model

Each rule is a plain Rego package under
[`policies/gbo/rules/`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules)
([ADR-0009](../decisions/0009-closed-world-rules.md)). A rule declares
three things:

- `rule_id`, `regime` (`consent` or `pid`), and `services` (the FSC
  services that the rule applies to).
- `covers_fields` and `covers_types`: the fields that the rule can grant.
- Its reasons to refuse: `deny` for the whole request and `deny_field[i]`
  for one field.

If a rule gives no reason, it grants the field. Each rule checks actor and
scope itself ([REQ-48](../requirements/authorization.md#req-48)). The file
[`lib.rego`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L1-L7)
only reads the request and holds no checks.

Demo v0.9.0 has five rules:

| Rule | Regime | Service | What it grants | Own reasons to refuse |
|---|---|---|---|---|
| DVT0001 | consent | `bri` | Income declaration fields under consent | consent codes, `SCOPE_NOT_ALLOWED`, `CONSTRAINT_MISMATCH`, `YEAR_NOT_COVERED`, `CONSENT_ACTOR_MISMATCH` |
| LVG0001 | consent | `lvg` | Ownership check at the LVG, scope `lvg:vbo:eigendom` | consent codes, `SCOPE_NOT_ALLOWED`, `CONSTRAINT_MISMATCH` |
| EUD0001 | pid | `bri` | Inkomensverklaring to the wallet, years 2024 and 2025 | `PID_NOT_PRESENT`, `ACTOR_NOT_ALLOWED`, `YEAR_NOT_ALLOWED` |
| EUD0002 | pid | `brp` | Akte van overlijden to the wallet | `PID_NOT_PRESENT`, `ACTOR_NOT_ALLOWED` |
| ASI0001 | pid | `brp` | BRP fields for the ASIP | `PID_NOT_PRESENT`, `ACTOR_NOT_ALLOWED` |

The consent codes are the outcomes of the proof verification and the
status lookup. For more information, see
[Consent verification in policy](#consent-verification-in-policy).

### How the engine binds rules to fields

The engine
([`engine.rego`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego))
decides each data field of the field list separately, in these steps:

1. Only the rules of the active regime bind.
2. Only the rules that serve the FSC service of the request bind
   ([REQ-97](../requirements/authorization.md#req-97)). The service is the
   `service_name` from the FSC access token. The Manager of the source
   signed this token
   ([`engine.rego#L183-L192`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L183-L192)).
3. A field binds to the rules that name its key `ParentType.field`. An
   argument-free leaf outside the root types also binds to the rules that
   cover its parent type.
4. Every delegated call needs an integrator mandate for the represented
   party and the granting rule
   ([`engine.rego#L246-L267`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L246-L267)).
   The engine adds this check to every rule. No rule can leave it out.
5. For each field, the first bound rule without reasons grants the field
   ([`engine.rego#L269-L306`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L269-L306)).
6. The engine allows the request only if it allows every data field.

Service binding is necessary because a field key is unique only within one
schema. `Query.ingeschrevenPersoon` is in both `bri` and `brp`. If the
binding is absent, a rule for one service grants the same key on the other
service ([F-90](../traceability/findings-closed.md#f-90)). A test requires every
rule to name its services
([`engine_test.rego#L497-L501`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine_test.rego#L497-L501)).

The world is closed. If no rule covers a field, the engine denies the
field with `NO_APPLICABLE_RULE`. No separate catalog exists: the rule is
the catalog. If the engine cannot make a decision for a field, it refuses
the field as `RULE_NOT_EVALUABLE`. The request then fails as a
configuration error
([`engine.rego#L18-L23`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L18-L23)).
The engine never leaves a field out of the decision.

### Constraints inside the query

Field coverage answers "which fields". Two more checks answer "whose
records" and "which part of the records". Both checks read the arguments
of the query. So the selectors must be inside the query, where the PDP
can see them. The two checks work as follows:

- The subject check. Under consent, the query names the citizen with a
  placeholder: `consent:identity` for a BSN API, `consent:pseudonym` for a
  source-pseudonym API
  ([`lib.rego#L43-L53`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L43-L53)).
  Each rule lists the placeholders that it accepts. DVT0001 and LVG0001
  accept only `consent:identity`. The PDP denies three cases with
  `CONSTRAINT_MISMATCH`: a literal value, another placeholder, and a
  placeholder without a verified proof
  ([`dvt0001.rego#L72-L80`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L72-L80)).

    The PDP does not check who the subject is. It checks that the subject
    comes from the proof
    ([REQ-79](../requirements/pseudonymization.md#req-79),
    [F-77](../traceability/findings.md#f-77)).

- The year check. Every requested `belastingjaren` value needs a
  consented `bd:ib:<year>` scope. If a query has no year filter, it fails
  too, because the source then returns every year
  ([`dvt0001.rego#L82-L96`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/dvtp/dvt0001.rego#L82-L96)).
  An argument that comes from a schema default counts as missing.

The source returns only the fields that the query selects
([REQ-08](../requirements/authorization.md#req-08)).

## Consent verification in policy

The policy verifies the consent proof itself
([ADR-0032](../decisions/0032-consent-proof.md),
[`consent.rego`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego)).
The request mapper has no part in this verification. The policy ignores a
`pip.consent` in the input. The PDP decides only on a consent for which
it established the origin, the binding, and the status at evaluation time
itself ([REQ-68](../requirements/consent.md#req-68)).

For each evaluation, the policy does three steps in this order:

1. It verifies the ES256 signature against the JWKS of the register. It
   caches the JWKS for 300 seconds and fetches the JWKS again on an
   unknown `kid`.
2. It verifies the claims, with 30 seconds of clock skew.
3. Only then does it call the register for the status of the
   `consent_id`. This call goes over FSC, with no cache and a 2-second
   timeout.

Each failure maps to its own reason code
([`consent.rego#L174-L186`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/consent.rego#L174-L186)):

| Code | Cause |
|---|---|
| `CONSENT_CONTEXT_INVALID` | Two tokens. A wrong type, issuer, or audience. A missing claim or no `encrypted_subject`. A `valid_until` that is not equal to `exp` |
| `CONSENT_SIGNATURE_INVALID` | The token is no JWT, the algorithm is other than ES256, the key is unknown, or the signature does not verify |
| `CONSENT_KEYS_UNAVAILABLE` | The policy cannot fetch the JWKS |
| `CONSENT_TOKEN_EXPIRED` | The time is more than 30 seconds after `exp` |
| `CONSENT_STATUS_UNAVAILABLE` | The status lookup failed or timed out |
| `CONSENT_NOT_FOUND` | The register does not know the consent |
| `CONSENT_WITHDRAWN` | The status is `REVOKED` |
| `CONSENT_EXPIRED` | The time is after `valid_until`, within the clock skew |
| `CONSENT_ACTOR_MISMATCH` | The consent names a party other than the represented party of the call |

The consent binds the represented party. On a delegated call, this party
is the FSC delegator. On other calls, it is the calling peer
([`lib.rego#L55-L72`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L55-L72)).
The integrator gets no mandate from the consent
([REQ-106](../requirements/consent.md#req-106),
[ADR-0034](../decisions/0034-integrator-delegation.md)).

The policy fetches the status during evaluation. As a result, the input,
the policy, and the data do not reproduce the decision. The engine copies
the resolved consent into its response for the console decision log
([`engine.rego#L25-L29`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L25-L29)).
The ADL does not contain this copy
([F-72](../traceability/findings.md#f-72)). For the proof, the status
interface, and the freshness rules, see [Consent](consent.md).

## Query mapping (FTV GraphQL profile)

The GraphQL query of the consumer is the authorization object. The PEP
sends the raw body. The request mapper inside the PDP turns the body into
the field list of the FTV GraphQL profile for AuthZEN (`ftv-graphql/0.1`).
The mapper is a separate Go module,
[`services/ftv-graphql-mapper`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper),
with a thin OpenFTV adapter
([ADR-0013](../decisions/0013-pdp-request-mapper.md)).

The mapper applies four rules:

- It parses the body. It gives each field its parent type from the bundled
  schema of the FSC service of the request. It gives each field its
  arguments as the source executes them.
- It accepts only a query. A mutation or a subscription gives
  `OPERATION_NOT_SUPPORTED`
  ([`mapper.go#L194`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/mapper.go#L194)).
- It enforces limits: body 1 MiB, nesting depth 64, 100 fragment
  definitions, and selection depth 64. Further limits are 1000 field
  records, 100 aliased selections, and 1 second of validation
  ([`mapper.go#L252-L268`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/mapper.go#L252-L268)).
- It never accepts `persistedQuery`.

If the mapper cannot build a complete field list, it marks the request
`Unverifiable` with a code and a subcode
([`mapper.go#L27-L43`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/ftv-graphql-mapper/mapper.go#L27-L43)).
The engine then denies the whole request
([REQ-17](../requirements/authorization.md#req-17)). The mapper uses
these codes and subcodes:

| Code | Subcodes |
|---|---|
| `COVERAGE_UNVERIFIABLE` | `UNSUPPORTED_TRANSPORT`, `INVALID_BODY`, `PARSE_ERROR`, `INVALID_QUERY`, `NO_OPERATION`, `OPERATION_NOT_FOUND`, `OPERATION_AMBIGUOUS`, `VARIABLE_ERROR`, `LIMIT_EXCEEDED` |
| `OPERATION_NOT_SUPPORTED` | — |
| `CONFIG_ERROR` | `SCHEMA_UNAVAILABLE` |

Three controls keep the judged request equal to the executed request:

- Schema pins: the policy bundle pins the digest of the schema of each
  service in
  [`graphql_schemas.rego`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/graphql_schemas.rego).
  If a schema is not pinned, the PDP denies with
  `CONFIG_ERROR SCHEMA_MISMATCH`
  ([`engine.rego#L129-L141`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L129-L141)).
- Drift check: a CI job compares the bundled schemas with the schemas
  that the sources run
  ([`check-schema-drift.sh`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/scripts/check-schema-drift.sh)).
- Transport subset at the source: the source gateway accepts only POST
  with a JSON body on one path. It accepts no query string, no `Upgrade`,
  and no `Content-Encoding`
  ([`transport.go#L9-L13`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/bron-sidecar/transport.go#L9-L13)).
  A request that the PDP never judged cannot run.

For future sources, how the PDP models fields, recursion, and arguments
is an open question ([Q-14](../traceability/open-questions.md#q-14)).

## Reason codes: two layers

A denial carries a machine-readable reason in two layers
([REQ-06](../requirements/authorization.md#req-06)). The consumer gets a
coarse code. The administrator of the source gets the detail per field.
The consumer code never shows which field the PDP denied, whether a field
exists, or which check failed. Otherwise the consumer can map the schema
by trying names. The two layers differ in audience, route, and codes:

| Layer | Who sees it | Where it goes | Codes |
|---|---|---|---|
| Consumer code (`graphql.client`) | Consumer, ADL | `reason` → `reason_user.en` in the AuthZEN answer. The ADL stores it | `FIELD_NOT_PERMITTED`, `ACCESS_DENIED`, `COVERAGE_UNVERIFIABLE <subcode>`, `OPERATION_NOT_SUPPORTED`, `NO_DATA_FIELDS` |
| Administrator codes (`graphql.admin`) | Administrator of the source | OPA console decision log only (observability) | Request code, plus per denied field: the bound rules, their reasons in order, and the field code |

Each administrator request code maps to one consumer code
([`engine.rego#L95-L118`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L95-L118),
[`authz.rego#L42-L51`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/authz.rego#L42-L51)):

| Administrator request code | Consumer code |
|---|---|
| Fields denied by rules (`FIELD_NOT_PERMITTED`) | `FIELD_NOT_PERMITTED` |
| `COVERAGE_UNVERIFIABLE INVALID_QUERY` | `FIELD_NOT_PERMITTED` |
| `COVERAGE_UNVERIFIABLE` with another subcode | `COVERAGE_UNVERIFIABLE <subcode>` |
| `OPERATION_NOT_SUPPORTED`, `NO_DATA_FIELDS` | the same code |
| `PIP_UNAVAILABLE` (the toestemmingsregister, its keys, or the admission register did not answer) | `ACCESS_DENIED` |
| `CONFIG_ERROR` (`MAPPER_OUTPUT_MISSING`, `SCHEMA_MISMATCH`, `SCHEMA_UNAVAILABLE`, `RULE_NOT_EVALUABLE`) | `ACCESS_DENIED` |

To the consumer, a fault at the source looks like a normal denial. For
one field, a rule can give several reasons. The rule reports the first
reason in a fixed order
([`engine.rego#L321-L344`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/engine.rego#L321-L344)).
The order is the token, then the state of the consent, then the question,
then the caller.
As a result, if the consent is revoked and the year check also fails, the
code is `CONSENT_WITHDRAWN`.

Demo v0.9.0 has two limits for reason codes:

- The FSC Inway loses the reason. It reads `reasonUser`, but the PDP
  sends `reason_user`. Upstream has a fix that was not released at the
  time of demo v0.9.0
  ([`ftv-graphql-profile.md#L93-L96`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/ftv-graphql-profile.md#L93-L96)).
- The consumer backend shows the citizen only `FIELD_NOT_PERMITTED`, with
  an offer to consent again. Every other code becomes `UNAVAILABLE`
  ([`denial.go`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/dienstverlener-backend/consumer/denial.go)).

The ADL is the audit source ([ADR-0036](../decisions/0036-adl-decision-record.md)).
It holds only the consumer code. As a result, a supervisor can
reconstruct from the ADL only what the consumer can know
([F-72](../traceability/findings.md#f-72)). For the full list of deny
paths per scenario, see the runtime view, for example
[DvTP query](../runtime/dvtp-query.md).

## Admission and contract acceptance

Admission to the system is data in a register. The decision policy holds
no admissions ([REQ-61](../requirements/admission.md#req-61)). The FSC
Manager of the provider sends every contract proposal to the PDP. The
contract policy
([`autosign.rego`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego))
reads the admission register and runs eight checks. The first check that
fails names the refusal
([ADR-0015](../decisions/0015-contract-acceptance-by-policy.md),
[`autosign.rego#L165-L175`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L165-L175)).
The policy runs the checks in this order:

| # | Code | Refuses when |
|---|---|---|
| 1 | `NOT_AN_AUTOSIGN_REQUEST` | The input is not a well-formed autosign request |
| 2 | `GRANT_TYPE_NOT_ALLOWED` | The grants are not all type 2 (service connection) or all type 3 (delegated service connection) |
| 3 | `NO_COUNTERPARTY` | The contract has no party other than the provider itself |
| 4 | `ADMISSION_REGISTER_UNAVAILABLE` | The PIP pull supplied no register |
| 5 | `PARTY_NOT_IN_REGISTRY` | A party is not in the register |
| 6 | `PARTY_NOT_ACTIVE` | A party is suspended |
| 7 | `SOURCE_NOT_ALLOWED` | The party is not admitted for this source peer |
| 8 | `DELEGATION_NOT_REGISTERED` | A delegated grant has no registered integration |

A missing register and an empty register are different
([`autosign.rego#L51-L53`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/fsc/autosign.rego#L51-L53)).
An empty register is available data that admits nobody. After a refusal,
the contract stays proposed, so the party can submit it again
([REQ-63](../requirements/admission.md#req-63)).

The contract question and the request question are separate rule sets
([REQ-62](../requirements/admission.md#req-62)). A contract decides who
can connect at all. A request decides which field the party can read at
request time. The two rule sets share no rules and no reason codes. They
do share one availability object: one broken module stops both
([F-52](../traceability/findings.md#f-52)).

Four points are open:

- A suspended consumer keeps its existing contract. It can still send
  queries, also with a valid consent
  ([REQ-110](../requirements/admission.md#req-110),
  [Q-53](../traceability/open-questions.md#q-53)).
- No component logs changes to admissions, mandates, and activations
  ([REQ-123](../requirements/admission.md#req-123)).
- The autosign input of the Manager carries only peer IDs and grant
  types. As a result, the policy judges only the parties of a contract.
  It has no input about the content of the contract
  ([F-56](../traceability/findings-closed.md#f-56)).
- The task to run the admission register is assigned to the management
  organization ([Q-22](../traceability/answered-questions.md#q-22)).

For the scenario, see [Admission and activation](../runtime/admission.md).

## Data scope: demand side and supply side

What a consumer can request depends on two sides
([F-74](../traceability/findings.md#f-74)):

- Supply side: the source publishes what it offers. GBO validates and
  activates this description
  ([REQ-64](../requirements/sources-identity.md#req-64),
  [Source onboarding](source-onboarding.md)). The EUDI and ASI routes
  work this way.
- Demand side: for DvTP, a statutory service catalog sets the legal
  ceiling of what a consumer can request, per use case. The sector need
  defines this catalog.

What is technically allowed is the intersection of both sides. No text in
the GO, the PSA, or the FR-DvTP names that intersection. In demo v0.9.0,
the DvTP scopes are spread over the rules, the portal, and the field
coverage. The proposal is one DvTP catalog as the single source for
scopes, fields, and portal text. The proposal also adds an intersection
check at activation
([REQ-121](../requirements/consent.md#req-121),
[#382](https://github.com/ICTU/GBO-demo/issues/382)).

## Traceability

- Requirements: [REQ-04](../requirements/authorization.md#req-04), [REQ-06](../requirements/authorization.md#req-06), [REQ-08](../requirements/authorization.md#req-08), [REQ-17](../requirements/authorization.md#req-17), [REQ-18](../requirements/authorization.md#req-18), [REQ-42](../requirements/authorization.md#req-42), [REQ-44](../requirements/authorization.md#req-44), [REQ-45](../requirements/eudi-issuance.md#req-45), [REQ-48](../requirements/authorization.md#req-48), [REQ-61](../requirements/admission.md#req-61), [REQ-62](../requirements/admission.md#req-62), [REQ-63](../requirements/admission.md#req-63), [REQ-64](../requirements/sources-identity.md#req-64), [REQ-68](../requirements/consent.md#req-68), [REQ-74](../requirements/authorization.md#req-74), [REQ-79](../requirements/pseudonymization.md#req-79), [REQ-90](../requirements/asi.md#req-90), [REQ-97](../requirements/authorization.md#req-97), [REQ-106](../requirements/consent.md#req-106), [REQ-110](../requirements/admission.md#req-110), [REQ-121](../requirements/consent.md#req-121), [REQ-123](../requirements/admission.md#req-123)
- Findings: [F-35](../traceability/findings-closed.md#f-35) (resolved in demo), [F-52](../traceability/findings.md#f-52) (open), [F-56](../traceability/findings-closed.md#f-56) (closed), [F-70](../traceability/findings.md#f-70) (open), [F-72](../traceability/findings.md#f-72) (open), [F-74](../traceability/findings.md#f-74) (open), [F-77](../traceability/findings.md#f-77) (open), [F-83](../traceability/findings.md#f-83) (open), [F-90](../traceability/findings-closed.md#f-90) (resolved in demo)
- Open questions: [Q-14](../traceability/open-questions.md#q-14) (open), [Q-15](../traceability/answered-questions.md#q-15) (answered), [Q-16](../traceability/answered-questions.md#q-16) (answered), [Q-22](../traceability/answered-questions.md#q-22) (answered), [Q-53](../traceability/open-questions.md#q-53) (open)
- Demo increments: [SL-03b](../traceability/increments.md#sl-03b) (done), [SL-13](../traceability/increments.md#sl-13) (done), [SL-17](../traceability/increments.md#sl-17) (done), [SL-40](../traceability/increments.md#sl-40) (done), [SL-45](../traceability/increments.md#sl-45) (done), [SL-48](../traceability/increments.md#sl-48) (done)
