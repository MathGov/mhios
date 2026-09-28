# MHIOS–MathGov Core Integration Profile v0.8

**Status:** Candidate implementation crosswalk  
**Tested Core build:** `MathGov_Core_2026_09_v12.6_SGP_v8.5+2026.08.15.3`
**Tested Core package:** `MathGov_Core_2026_09_v12_6_SGP_v8_5_BUILD_2026_08_15_3_FINAL_PUBLICATION_READY.zip`  
**Core package SHA-256:** `475c4e50da133d6eec497d9cf7da7bbf6e7f7d9d79ce27f0d86b03fdbfccd69f`  
**Core VERSION_MANIFEST SHA-256:** `a11e023c3fb647319b8ac11571d5be684bc2750f6162c661c2d0d42f236b0ed6`  
**Core run-schema SHA-256:** `dc55a36a53203677a1d3961287269ff76f6b716ff80e25efda5d5d1b2e1ff6bf`

## Governing rule

Pinned MathGov Core semantic sources control decision meaning. MHIOS controls interaction, provenance, workflow, and generated views only.

## Final v12.6 stabilization compatibility note

Core build `+2026.08.15.3` preserves the five-stage cascade and all MHIOS-owned object semantics. MHIOS SHALL present provisional UCI as a diagnostic/evidence surface subject to the Core's non-substitution rule: provisional UCI alone does not establish a high-stakes CSV pass/fail or deterministic tie resolution. The Core token `RIGHTS_RELEVANT_EFFECT_UNROUTED` is carried verbatim through `canon_audit_flags`; no new MHIOS object type is required.

## Required v0.8 compatibility

- DecisionRun preserves `transition_or_action_boundary`.
- DecisionRun preserves the Reality Grounding outputs `reality_surface` and `consequence_pathways`.
- Claim and MethodologicalIntegrityRecord preserve `claim_type`, primary `claim_domain`, plural `warrant_domains`, and structured `cross_domain_bridges`.
- Every material cross-domain warrant relationship has its own bridge object.
- Legal-regulatory claims preserve jurisdiction, authority source, applicability boundary, interpretation status, and review or contest path.
- CapabilityAuthorityDecompositionRecord separately preserves generation method, reference source, constraint sources, objective source, objective-change authority, admissibility-warrant sources, execution interface, execution scope, execution authority, revocation authority, safe-state/shutdown path, and requalification trigger.
- Deprecated compound fields and scalar autonomy levels are not valid substitutes.
- GateRecord preserves `record_role`: RG is `CLAIM_AUTHORITY_PRECONDITION`; RF/NCRC, TRC, and CSV are `OPTION_REJECTING_GATE`.
- Canon audit-flag tokens are preserved verbatim in `canon_audit_flags`; local interface findings use a separate namespace.
- A selectable `CSV_PASS_WITH_CONTROLS` option identifies constitutive obligations that resolve to complete `MaterialObligationRecord` objects. Those obligations may reference lower-level controls; a bare `Control` identifier or owner is insufficient.
- Triggered consequence-tempo, responsibility-continuity, and human-compensation-load duties remain separate records and do not collapse into CSV status or execution authorization.
- Tier 3 and pilot runs preserve `ProjectionPreRegistrationRecord`; Tier 2 and Tier 3 runs preserve `ComputationalClosureRecord`; Refusal states preserve `RefusalRecord`.
- Triggered Core or companion records not modeled natively are carried only through validated, hash-bound `CoreRecordAttachment` objects under `MHIOS_CORE_RECORD_COVERAGE_v0_8.yaml`.
- A PCC may be labeled Tier-3-complete only when every triggered coverage slot is satisfied; otherwise it is an explicitly partial generated view.
- EmergencyOrderRecord preserves the Canon rights priority, within-right component order, violation tuples, comparison trace, challenge, remediation, appeal, expiry, and return-to-normal conditions without claiming an ordinary pass or RLS selection.
- MHIOS and ripple.md conformance claims remain orthogonal and separately version-pinned.

## Nonclaim

MHIOS compatibility does not establish evidence truth, legal authority, physical safety, ethical legitimacy, deployment authorization, or Core conformance beyond the checks actually performed.
