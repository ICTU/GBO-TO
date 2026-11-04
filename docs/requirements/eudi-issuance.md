# EUDI issuance requirements

These requirements apply only to the issuance of attestations to the EUDI
wallet (the PuB-EAA route). The citizen discloses a PID from the wallet.
The nl-wallet issuance server verifies the disclosure and calls the GBO
EUDI adapter. The adapter queries the source over FSC through the generic
PEP-PDP chain. Then the issuance server issues the attestation under the
certificate set of the bronhouder.

This route exposed a generic basis. The generic pages hold that basis:

- the regime from evidence ([REQ-74](authorization.md#req-74))
- the thin channel adapter ([REQ-44](authorization.md#req-44))
- the source-owned description ([REQ-64](sources-identity.md#req-64))

The requirements on this page cover only what is specific to the wallet.
[ADR 0018](../decisions/0018-eudi-disclosure-issuance.md),
[ADR 0017](../decisions/0017-gbo-simple-v1.md), and
[ADR 0028](../decisions/0028-pubeaa-productization.md) record the design.
The runtime view is in [EUDI issuance](../runtime/eudi-issuance.md).

Evidence links to gbo-demo point at tag `v0.9.0`.
## REQ-45: The source is queried only about the citizen from a verified PID disclosure {#req-45}

> The GBO issuance facility MUST take the subject of a source query for an attestation only from a verified PID disclosure. A verified PID disclosure has a signature that was checked against a trust list of PID providers. The facility MUST be able to show that this disclosure belongs to this request. A request without such a disclosure MUST NOT reach the source. A request with a shared attestation that is not a PID MUST NOT reach the source. A request that does not provably come from the verifying party MUST NOT reach the source either.

> The trust list for that check MUST hold only the anchors of PID providers.

| Case | Outcome |
|---|---|
| Verified PID disclosure, provably for this request | source queried with the BSN from the PID (*proposal, binding not built*) |
| Disclosure without a BSN | refused before the source with HTTP 400 (*from the code*) |
| Shared attestation is not a PID | refused (*proposal, reason open*) |
| Request not provably from the verifying runtime | refused (*proposal and not built: the adapter route has no caller authentication*) |
| Signature invalid or provider not on the list | no request to the adapter (*the issuance server verifies, without an independent test*) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design: ARF v3.0.0 Annex 2
        [OIA_12](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#OIA_12)
        (a relying party validates the PID signature with a trust anchor from
        the LoTE of PID providers) and
        [OIA_14](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#OIA_14)
        (LoTE per ETSI TS 119 602). The other source is
        [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
        ("issuance, verification and retrieval use suitable authentication,
        authorization and logging", "agreements arrange binding to citizen and
        wallet").
    - **Addressee**: GBO-delivered component: the EUDI adapter and the
        issuance configuration that GBO generates. The issuance server is part
        of nl-wallet. What the issuance server verifies is a product property.
        This requirement does not cover it.
    - **Evidence**: not built:
        [ICTU/GBO-demo#133](https://github.com/ICTU/GBO-demo/issues/133).
        Demo v0.9.0 has this state:
        - The adapter trusts the BSN
            ([`main.go#L23-L26`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L23-L26)).
            It refuses a disclosure without a BSN in
            [`#L249-L253`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L249-L253).
        - The route `POST /attestations/{sourceID}/{typeID}`
            ([`source_release_runtime.go#L69`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_release_runtime.go#L69))
            runs on a plain listener without caller authentication
            ([`main.go#L700`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L700)).
        - Issuance asks only for the BSN from the PID
            ([`issuance_config.go#L162`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_config.go#L162)).
        - The trust list is in
            [`issuance_server.toml.example#L3-L9`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/config/issuance_server.toml.example#L3-L9).
            The code in
            [`issuance_release.go#L120-L121`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_release.go#L120-L121)
            adds the issuer CA of every source to it.
    - **Related**: [REQ-44](authorization.md#req-44), [REQ-57](#req-57),
        [REQ-60](logging-audit.md#req-60),
        [REQ-74](authorization.md#req-74),
        [F-70](../traceability/findings.md#f-70),
        [F-83](../traceability/findings.md#f-83),
        [Q-18](../traceability/open-questions.md#q-18),
        [ADR 0018](../decisions/0018-eudi-disclosure-issuance.md),
        [ADR 0031](../decisions/0031-regime-from-evidence.md),
        [ADR 0043](../decisions/0043-identifiers-out-of-pdp-input.md).
    - **Notes**:
        - The issuance server verifies the PID disclosure. For that reason
            [SL-25](../traceability/increments.md#sl-25) (PID verification in the
            adapter) was dropped.
        - The gap is in the callback. The signature check is in place. Any
            caller that reaches the adapter URL can post a body with any BSN. The
            adapter then calls the source over FSC as the designated issuer peer,
            so the PDP allows the request. The adapter returns the projected
            claims without any wallet involvement.
        - Two solutions meet the requirement: the adapter verifies the SD-JWT
            itself, or the verifying runtime delivers signed evidence and
            authenticates the callback. Both solutions also need the binding of
            the disclosure to the request.
        - With this requirement, the PID becomes positive evidence for the PID
            regime. In demo v0.9.0, that regime is "no consent token" plus a list
            of designated issuers
            ([`eudi_helper.rego#L13-L30`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eudi_helper.rego#L13-L30),
            [F-70](../traceability/findings.md#f-70)).
        - In demo v0.9.0, the trust list also holds the GBO development CA and
            the issuer CAs of the sources. A PID verification must trust only PID
            providers.
            How fresh the list must be is open
            ([Q-18](../traceability/open-questions.md#q-18), sub-question 4).
            Which list anchors PuB-EAA providers is open as well
            ([Q-30](../traceability/open-questions.md#q-30)).
        - Checking the revocation status of the PID is a SHOULD
            ([VCR_13](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#VCR_13)).
        - The reference QTSP authenticates its callback with a secret path over
            CA-pinned HTTPS
            ([`qtsp_issuance.go#L134-L142`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/qtsp_issuance.go#L134-L142)).
            The source route does not.
        - The BSN from the PID stays in the PDP input and is in both decision
            logs. [REQ-60](logging-audit.md#req-60) is not met for EUDI
            ([ADR 0043](../decisions/0043-identifiers-out-of-pdp-input.md)).

## REQ-57: An attestation about someone other than the requester follows an agreed relation from the verified requester {#req-57}

> An attestation can hold data about someone other than the requester. For such an attestation, the chain that GBO delivers MUST query the source only along a relation that the source recorded in its service description. The starting point MUST be the subject from the verified PID ([REQ-45](#req-45)). The starting point MUST NOT be a value that the caller chooses. The reference policy MUST deny a query that takes another entry point or asks for fields outside that relation. The service description MUST mark such a relation, with the kind of relation.

| Case | Outcome |
|---|---|
| Requester with a marriage that ended by the death of the partner | certificate with the data of that partner (*from the code*) |
| Partner died on another date than the dissolution | no certificate. The source returns nothing, and the adapter answers HTTP 404 (*from the code*). |
| Date incomplete (only year and month) | certificate (*from the code*) |
| Entry point without the BSN of a citizen | denied: `PID_NOT_PRESENT` (*from the code*) |
| Field outside the view | denied: `FIELD_NOT_PERMITTED` (*from the code*) |
| Entry point with the BSN of someone other than the PID holder | the PDP cannot tell the difference, so this case depends on REQ-45 (*proposal*) |
| Relation not marked in the service description | *proposal, outcome open* |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: derived. The requirement serves
        [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
        ("agreements arrange binding to citizen and wallet") and
        [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
        Without a recorded relation from the requester, anyone with a valid PID
        can put data about any other person in an attestation. Compare
        Implementing Regulation (EU)
        [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj),
        Annex II point 2(c) (only the minimum set of attributes).
    - **Addressee**: GBO-delivered component: the reference policy and the
        adapter. Interface agreement: the marking of the relation in the
        service description.
    - **Evidence**: [PR #125](https://github.com/ICTU/GBO-demo/pull/125),
        [PR #304](https://github.com/ICTU/GBO-demo/pull/304).
        - The selection at the source is in
            [`brp-graphql-server/main.go#L671-L705`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/main.go#L671-L705),
            tested in
            [`main_test.go#L183`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/main_test.go#L183)
            and
            [`#L190`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/brp-graphql-server/main_test.go#L190).
        - The closed field list is in
            [`eud0002.rego#L33-L51`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0002.rego#L33-L51)
            and the entry point is in
            [`#L62-L66`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0002.rego#L62-L66),
            tested in
            [`eud0002_test.rego#L42`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/rules/eudi/eud0002_test.rego#L42).
        - The subject comes from the PID
            ([`source_metadata.go#L272-L273`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_metadata.go#L272-L273)).
        - The marking in the service description is not built.
    - **Related**: [REQ-45](#req-45), [REQ-64](sources-identity.md#req-64),
        [REQ-72](logging-audit.md#req-72), [REQ-78](#req-78),
        [AV-10](admission.md#av-10),
        [AV-11](admission.md#av-11),
        [F-47](../traceability/findings.md#f-47),
        [Q-14](../traceability/open-questions.md#q-14),
        [Q-20](../traceability/answered-questions.md#q-20).
    - **Notes**:
        - Design choice: in demo v0.9.0, the relation runs through a view of
            the source. Filter arguments in the schema, which the policy requires
            with fixed values, also meet the requirement
            ([ICTU/GBO-demo#425](https://github.com/ICTU/GBO-demo/issues/425)).
            In the view variant, the PDP does not see the relation and only limits
            the fields. The source carries the selection. The mechanism to check
            argument values exists
            ([`lib.rego#L30-L41`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/policies/gbo/lib.rego#L30-L41)).
        - Representation is outside this requirement. A person who asks on
            behalf of another falls under Annex II point 2(a) of Implementing
            Regulation 2025/1569 and a mechanism of its own (PSA
            [B-19](https://ictu.github.io/GBO-PSA/main/vraagstukken/#besluitregister)).
        - The deceased is not a data subject in the sense of the GDPR. The
            source logs the requester and the living parents
            ([AV-10](admission.md#av-10)).
        - More than one result from the source leads to a refusal
            ([REQ-116](#req-116)).

## REQ-58: Every source holder has its own certificate set for issuance, and missing material fails {#req-58}

> The GBO issuance facility MUST keep a certificate set of its own per bronhouder. The set holds a certificate that signs attestations, and an access certificate with which issuance shows itself to the wallet. The facility MUST NOT sign an attestation or a request to the wallet with the set of another bronhouder, in any case. If the set of a source is missing, incomplete, or differs from what is activated, issuance MUST refuse for that source. Issuance MUST NOT fall back to another set.

| Case | Outcome |
|---|---|
| Source with a complete set of its own | issuance under its own issuer and access certificate |
| Set missing | source blocked: `CERTIFICATE_SET_NOT_FOUND`. Other sources continue. |
| Set without OIN or organization name | source blocked: `CERTIFICATE_SET_INVALID` |
| Mounted material differs from the active release | no issuance configuration generated |
| Two sources behind one FSC peer | each its own set |

- **Status**: ready for review

??? note "Source, evidence and notes"

    - **Source**: design: ARF v3.0.0 Annex 2
        [Reg_10a](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#Reg_10a)
        (at least one access certificate per registered service),
        [PuBPNot_04](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#PuBPNot_04)
        (every PuB-EAA can be authenticated with the trust anchors notified for
        that provider), and
        [ISSU_73](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#ISSU_73)
        (signing certificates per ETSI TS 119 412-6 clause 8). The other source
        is
        [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
        ("the bronhouder stays legally and substantively responsible").
    - **Addressee**: GBO-delivered component: the reconciler and the
        generator of the issuance configuration.
    - **Evidence**: [ICTU/GBO-demo#225](https://github.com/ICTU/GBO-demo/issues/225),
        [PR #237](https://github.com/ICTU/GBO-demo/pull/237),
        [PR #247](https://github.com/ICTU/GBO-demo/pull/247),
        [PR #276](https://github.com/ICTU/GBO-demo/pull/276).
        - The set per source is in
            [`issuance_config.go#L159-L180`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_config.go#L159-L180).
        - The blocking is in
            [`source-registry/onboarding/service.go#L283-L297`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service.go#L283-L297),
            tested in
            [`service_test.go#L130`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/source-registry/onboarding/service_test.go#L130),
            [`fsc_contract_discovery_test.go#L225`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/fsc_contract_discovery_test.go#L225),
            and
            [`#L278`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/fsc_contract_discovery_test.go#L278).
        - The check for differing material is in
            [`issuance_release.go#L113-L116`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_release.go#L113-L116),
            without a test.
    - **Related**: [REQ-64](sources-identity.md#req-64),
        [REQ-67](sources-identity.md#req-67), [REQ-77](#req-77),
        [F-50](../traceability/findings-closed.md#f-50),
        [F-81](../traceability/findings.md#f-81),
        [Q-07](../traceability/answered-questions.md#q-07),
        [Q-17](../traceability/open-questions.md#q-17),
        [ADR 0023](../decisions/0023-identity-convergence.md),
        [ADR 0028](../decisions/0028-pubeaa-productization.md).
    - **Notes**:
        - The set also holds a certificate for the status list
            ([`issuance_config.go#L179`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_config.go#L179)).
            [Q-17](../traceability/open-questions.md#q-17) (#225) covers whether
            that certificate belongs to the source or to the facility, and who
            holds the keys. This requirement says which certificates exist. It
            does not say who keeps them.
        - No procedure exists to rotate and revoke certificates without a
            wallet update
            ([ICTU/GBO-demo#381](https://github.com/ICTU/GBO-demo/issues/381),
            rows 2 and 3).
        - In production, a registered service also needs a registration
            certificate, and the seal key sits in a QSCD
            ([F-81](../traceability/findings.md#f-81)).
        - In the demo, all sets hang under one development CA
            ([`issuance_server.toml.example#L4-L5`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/config/issuance_server.toml.example#L4-L5)).
            This CA is part of the demo configuration.
        - The reference QTSP gets a set of its own, and fails on an incomplete
            set
            ([`qtsp_issuance.go#L109-L131`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/qtsp_issuance.go#L109-L131)).
            Missing QTSP material does not block source issuance.

## REQ-77: An attestation gets the validity and revocation policy of the source holder {#req-77}

> For each attestation type, the GBO issuance facility MUST apply the validity period that the bronhouder records. The facility MUST NOT apply a value from its own code. An attestation that is valid for more than 24 hours MUST carry a status reference with which it can be revoked. On instruction of the bronhouder, the facility MUST be able to revoke an issued attestation, without an action of the holder.

| Case | Outcome |
|---|---|
| Validity recorded by the bronhouder | issued with that validity (*proposal, demo v0.9.0 uses 365 days for every source*) |
| Validity longer than 24 hours | status reference in the attestation (*from the code: status list per type*) |
| Source data changed while the attestation is still valid for at least 24 hours | revoked (*proposal, who signals the change is open*) |
| Bronhouder revokes | status set to revoked (*proposal*) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design:
        - Implementing Regulation (EU)
            [2025/1569](https://eur-lex.europa.eu/eli/reg_impl/2025/1569/oj),
            article 4, with these paragraphs:
            - paragraph 1: a written and public policy for validity and
                revocation
            - paragraph 2: only the provider can revoke
            - paragraph 3: for a validity of more than 24 hours, revoke in at
                least the listed cases
            - paragraph 5: status information available with integrity and
                authenticity
        - ARF v3.0.0 Annex 2
            [VCR_01b](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#VCR_01b)
            (SD-JWT VC: valid for at most 24 hours, or a status list),
            [VCR_11a](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#VCR_11a)
            (Token Status List), and
            [VCR_09](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#VCR_09)
            (revoke when an attribute changes)
        - [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
            ("agreements arrange … status, revocation and validity")
        - [GO](https://ictu.github.io/GBO-GO/main/) ("GBO is legally not a
            PubEAA provider")
    - **Addressee**: GBO-delivered component: the issuance facility.
    - **Evidence**: not built:
        [ICTU/GBO-demo#381](https://github.com/ICTU/GBO-demo/issues/381) (rows
        11 and 12), [ICTU/GBO-demo#225](https://github.com/ICTU/GBO-demo/issues/225).
        In demo v0.9.0, the validity is fixed in
        [`issuance_config.go#L166-L168`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_config.go#L166-L168)
        and
        [`qtsp_issuance.go#L152`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/qtsp_issuance.go#L152).
        The status list per type is in
        [`issuance_config.go#L179`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/issuance_config.go#L179).
    - **Related**: [REQ-58](#req-58), [REQ-64](sources-identity.md#req-64),
        [AV-12](admission.md#av-12),
        [AV-13](admission.md#av-13),
        [F-82](../traceability/findings.md#f-82),
        [Q-17](../traceability/open-questions.md#q-17),
        [Q-18](../traceability/open-questions.md#q-18),
        [ADR 0028](../decisions/0028-pubeaa-productization.md).
    - **Notes**:
        - The policy itself (paragraph 1) belongs to the bronhouder as
            provider. That policy is a candidate connection condition
            ([AV-12](admission.md#av-12)) and no requirement on GBO.
            The facility revokes technically, on instruction of the bronhouder
            ([AV-13](admission.md#av-13)).
            [Q-17](../traceability/open-questions.md#q-17) covers who holds the
            key of the status list.
        - GBO only queries. It gets no signal when source data changes
            ([F-82](../traceability/findings.md#f-82)). For each type, the choice
            is short-lived (less than 24 hours) or long-lived with a change feed
            and revocation.
        - The issuance server of nl-wallet sets the structure of the status
            list (random index, herd privacy). That structure is a product
            property.
        - The other points of the former security baseline are in
            [REQ-58](#req-58), [REQ-45](#req-45),
            [REQ-44](authorization.md#req-44),
            [REQ-64](sources-identity.md#req-64),
            [REQ-60](logging-audit.md#req-60),
            [REQ-72](logging-audit.md#req-72), and
            [REQ-11](authorization.md#req-11).

## REQ-78: Issuance issues nested claims, with selective disclosure per element as the schema prescribes {#req-78}

> The attestation schema of the source can define a claim as an object or a list. The GBO issuance facility MUST be able to issue such a claim in that form. It MUST apply the selective disclosure that the schema prescribes for each claim, also for each nested property and each list element. It MUST NOT refuse a schema, or flatten it, because it contains nested claims.

| Case | Outcome |
|---|---|
| Schema with only single-valued claims | issued, with `sd` per claim (*from the code*) |
| Schema with an object or a list (for example the parents per person) | issued, with disclosure per element (*proposal, demo v0.9.0 refuses it at validation*) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design: ARF v3.0.0 Annex 2
        [ARB_30](https://eudi.dev/3.0.0/annexes/annex-2/annex-2.02-high-level-requirements-by-topic/#ARB_30)
        (the rulebook records for all claims, also nested properties and list
        elements, whether they MUST, MAY, or MUST NOT be selectively
        disclosable),
        [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
        ("attestations follow an established attestation rulebook and schema",
        and the bronhouder records mapping and attestation schema in its GBO
        configuration), and
        [P-02](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
    - **Addressee**: GBO-delivered component: the mapping profile and the
        generation of Type Metadata in the EUDI adapter.
    - **Evidence**: not built:
        [ICTU/GBO-demo#381](https://github.com/ICTU/GBO-demo/issues/381),
        row 13. Demo v0.9.0 has only single-valued datatypes in
        [`profile.go#L117-L121`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/internal/gbosimplev1/profile.go#L117-L121).
        It sets `sd` per claim in
        [`source_claims.go#L237-L241`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_claims.go#L237-L241)
        ([PR #463](https://github.com/ICTU/GBO-demo/pull/463)).
    - **Related**: [REQ-57](#req-57), [REQ-64](sources-identity.md#req-64),
        [F-47](../traceability/findings.md#f-47),
        [Q-20](../traceability/answered-questions.md#q-20),
        [ADR 0017](../decisions/0017-gbo-simple-v1.md).
    - **Notes**:
        - The rulebook and the source choose whether a certificate models the
            parents per person. GBO does not make that choice.
        - Each claim in the source description has `sd` set to `always` (the
            default), `allowed`, or `never`. GBO carries this value into the
            generated Type Metadata.
        - Whether NL Wallet shows nested claims and lets the holder share them
            per element is wallet behavior (#381, row 13). That behavior decides
            whether the demo can show this requirement end to end. It does not
            decide whether the requirement applies.

## REQ-116: An attestation contains only what the source answered, per its mapping, and an answer that does not fit gives no attestation {#req-116}

> The GBO issuance facility MUST take every claim of an attestation from the answer of the source. It MUST use the mapping that the bronhouder records in its service description ([REQ-64](sources-identity.md#req-64)). It MUST NOT round, convert, add, or derive a source value beyond what that mapping prescribes.

> An answer does not fit the mapping if a mandatory claim is missing or empty. It also does not fit if a value does not have the recorded type, or if the answer holds more than one result. If the answer does not fit the mapping, the facility MUST NOT issue an attestation. That includes an attestation with only the claims that do fit. An answer without a result MUST end as "not found", distinct from an error.

| Case | Outcome |
|---|---|
| Answer fits the mapping | attestation with exactly the mapped claims. Fields outside the mapping stay out (code). |
| Amount with cents, datatype `number` | value unchanged in the claim and without rounding (code) |
| Mandatory claim missing | no attestation: HTTP 502, `GBO_SIMPLE_PATH_MISSING` in the log (code) |
| Mandatory claim is `null`, or has another type | no attestation: HTTP 502, `GBO_SIMPLE_TYPE_MISMATCH` in the log (code) |
| More than one result | no attestation: HTTP 502, `GBO_SIMPLE_RESULT_AMBIGUOUS` in the log (code) |
| No result | not found: HTTP 404. The processing is still logged (code). |
| Optional claim missing or `null` | claim left out, the rest issued (code) |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design: [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
        ("the bronhouder stays legally and substantively responsible for the
        public attributes issued", "if attestation issuance needs a semantic
        mapping, the bronhouder records in its GBO configuration which mapping
        … applies"),
        [PSA S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus)
        ("the set-up applies validation rules before delivery"), and
        [P-10](https://ictu.github.io/GBO-PSA/main/architectuurprincipes/).
        This requirement is stricter than these sources: no partial attestation
        and no conversion by GBO.
    - **Addressee**: GBO-delivered component: the mapping profile and the
        issuance runtime of the EUDI adapter. Interface agreement: the mapping
        profile as part of the service description.
    - **Evidence**: [PR #204](https://github.com/ICTU/GBO-demo/pull/204).
        - The projection is in
            [`profile.go#L126-L169`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/internal/gbosimplev1/profile.go#L126-L169).
            The runtime is in
            [`main.go#L302-L316`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main.go#L302-L316).
        - The test
            [`profile_test.go#L75`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/internal/gbosimplev1/profile_test.go#L75)
            uses the cases in
            [`cases.json#L82-L145`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/internal/gbosimplev1/testdata/cases.json#L82-L145).
            [`main_test.go#L582`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main_test.go#L582)
            tests that only mapped claims are issued.
            [`main_test.go#L609`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/main_test.go#L609)
            tests decimals.
            [`ldv_test.go#L505`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/ldv_test.go#L505)
            tests an answer without a result.
    - **Related**: [REQ-64](sources-identity.md#req-64), [REQ-78](#req-78),
        [REQ-101](asi.md#req-101), [REQ-124](#req-124),
        [Q-38](../traceability/open-questions.md#q-38),
        [ADR 0017](../decisions/0017-gbo-simple-v1.md).
    - **Notes**:
        - Design choice: `gbo-simple-v1` only copies, renames, and flattens.
            Selection, conversion, and conditions are not in it
            ([`docs/gbo-simple-v1.md#L5-L19`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/gbo-simple-v1.md#L5-L19)).
            A source that needs another form delivers it itself. Claims derived
            from source data are an open decision of PSA S11.
        - In demo v0.9.0, onboarding for EUDI accepts only whole amounts.
            nl-wallet v0.5 cannot show a non-integer value
            ([`source_claims.go#L220-L221`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/services/eudi-adapter/source_claims.go#L220-L221),
            [`docs/gbo-simple-v1.md#L121`](https://github.com/ICTU/GBO-demo/blob/v0.9.0/docs/gbo-simple-v1.md#L121)).
            That is a product property.
        - If an error occurs, the consumer sees only 502. The error code is in
            the adapter log.
        - The ASIP does not use `gbo-simple-v1`. Its `asi` capability composes
            values with `pointer`, `join`, `const`, and `each`
            ([ADR 0039](../decisions/0039-asi-source-described-attributes.md)).
            The rule "no partial result" holds there too
            ([REQ-101](asi.md#req-101)).

## REQ-124: For every attestation, the versions of the mapping, the source schema, and the attestation schema are traceable {#req-124}

> For every issued attestation, the GBO issuance facility MUST make the applied versions traceable. These are the versions of the mapping of the bronhouder, of the source schema, and of the attestation schema. The facility MUST apply only the mapping that the bronhouder recorded for that data service in its GBO configuration ([REQ-116](#req-116)). If the bronhouder recorded no mapping, the facility MUST convert nothing.

| Case | Outcome |
|---|---|
| Mapping recorded and activated | converted. The mapping version, the source version, and the target version are traceable at issuance. |
| No mapping recorded | nothing converted, and no attestation |
| New mapping version activated | later issuances name the new version, and earlier ones name the old version |

- **Status**: draft

??? note "Source, evidence and notes"

    - **Source**: design: [PSA S10](https://ictu.github.io/GBO-PSA/main/capabilities/#s10-semantiek-gegevenscatalogus)
        ("mappings to OOTS-EDM and attestation schemas are explicit. They can be
        traced to the source and target versions used"),
        [PSA S11](https://ictu.github.io/GBO-PSA/main/capabilities/#s11-attesteringsuitgifte)
        (the bronhouder records in its GBO configuration which mapping applies),
        and [D-14](https://ictu.github.io/GBO-PSA/main/ontwerpprincipes/).
    - **Addressee**: GBO-delivered component: issuance (the EUDI adapter).
    - **Evidence**: [REQ-116](#req-116) gives the evidence that only the
        mapping of the bronhouder is applied. The traceability of the versions
        is not checked.
    - **Related**: [REQ-59](logging-audit.md#req-59),
        [REQ-64](sources-identity.md#req-64),
        [REQ-66](sources-identity.md#req-66),
        [REQ-72](logging-audit.md#req-72), [REQ-116](#req-116),
        [Q-79](../traceability/open-questions.md#q-79).
    - **Notes**:
        - Traceability can come from the version of the activated source
            metadata ([REQ-66](sources-identity.md#req-66)) in the processing log
            record ([REQ-72](logging-audit.md#req-72)). The form is a design
            choice.
        - This requirement is the counterpart for the mapping of
            [REQ-59](logging-audit.md#req-59) (the policy version in the
            decision record).
        - S10 asks the same for the mapping to OOTS-EDM. That requirement
            follows after [Q-79](../traceability/open-questions.md#q-79).

## Removed numbers

- REQ-51: removed. [REQ-44](authorization.md#req-44) (thin channel
    adapter) and [REQ-64](sources-identity.md#req-64) (source-owned
    description) cover "The adapter does not hard-code use-case
    parameters".

The list of all removed numbers is on the
[requirements overview](index.md#removed-numbers).

