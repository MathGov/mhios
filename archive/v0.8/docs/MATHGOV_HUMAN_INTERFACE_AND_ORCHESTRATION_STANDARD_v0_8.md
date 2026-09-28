# MathGov Human Interface and Orchestration Standard v0.8

## Candidate Implementation Companion for MathGov / RippleLogic

**Short identifier:** MHIOS v0.8  
**Status:** Candidate experimental implementation standard  
**Version:** 0.8  
**Date:** 14 August 2026  
**Core relationship:** Not part of the frozen MathGov Core v12.6 release  
**Architecture preserved:** `RG -> RF/NCRC -> TRC -> CSV -> RLS`  
**Primary design rule:** **One run, one evidence graph, many generated records.**

---

## Executive summary

MHIOS specifies how people, software systems, optional AI assistants, reviewers, authorities, and auditors interact with a MathGov decision run. It addresses a central implementation risk: a rigorous specification can fail operationally when users must navigate disconnected forms, repeat the same information, interpret dense technical terminology without guidance, or rely on automation that hides judgment and responsibility.

MHIOS introduces an interaction and orchestration discipline, not another ethical or mathematical layer. It requires progressive disclosure, shared source objects, stable identifiers, trigger-derived tier recommendation, explicit provenance for human and automated contributions, preserved narrative evidence, canonical machine states beneath plain-language labels, challenge workflows, anti-audit-theater detection, generated records, monitoring, and requalification.

MHIOS does not change the MathGov cascade, rights rules, TRC, CSV, RLS, PLSS, SGP, PC-AEP, MFDI, Source Coupling, or authority boundaries. Its purpose is to make rigorous action easier than superficial compliance while preserving complete evidence, judgment, responsibility, and replay underneath the interface. This purpose is a design hypothesis, not an established empirical result. Version 0.8 has artifact-integrity evidence and a bounded structural test suite; it does not yet have construct-validity, burden-reduction, reviewer-agreement, anti-theater precision/recall, or real-world decision-performance evidence.


# Contents

## Standard

- [0. Document control and normative status](#0-document-control-and-normative-status)
- [1. Design objectives and success conditions](#1-design-objectives-and-success-conditions)
- [2. Interaction invariants](#2-interaction-invariants)
- [3. Roles, responsibilities, and separation of duties](#3-roles-responsibilities-and-separation-of-duties)
- [3A. Institutional preconditions and incentive integrity](#3a-institutional-preconditions-and-incentive-integrity)
- [4. Human-Judgment Firewall and provenance](#4-human-judgment-firewall-and-provenance)
- [5. Progressive disclosure and information architecture](#5-progressive-disclosure-and-information-architecture)
- [6. Tier orchestration and anti-downgrade controls](#6-tier-orchestration-and-anti-downgrade-controls)
- [7. Shared evidence graph and source-object architecture](#7-shared-evidence-graph-and-source-object-architecture)
- [8. Canonical MHIOS object model](#8-canonical-mhios-object-model)
- [9. Workflow and state orchestration](#9-workflow-and-state-orchestration)
- [10. Record generation and synchronization](#10-record-generation-and-synchronization)
- [11. Narrative evidence and typed interpretation](#11-narrative-evidence-and-typed-interpretation)
- [12. Anti-audit-theater detection](#12-anti-audit-theater-detection)
- [13. Calculation, state, and validation integrity](#13-calculation-state-and-validation-integrity)
- [14. Security, privacy, and access control](#14-security-privacy-and-access-control)
- [15. Accessibility and usability](#15-accessibility-and-usability)
- [16. Governance Burden Profile](#16-governance-burden-profile)
- [16A. Reviewer agreement and construct-operationalization study](#16a-reviewer-agreement-and-construct-operationalization-study)
- [17. MHIOS conformance levels](#17-mhios-conformance-levels)
- [18. Minimal vertical slice and later MVP boundary](#18-minimal-vertical-slice-and-later-mvp-boundary)
- [19. MVP screen registry and flow](#19-mvp-screen-registry-and-flow)
- [20. MVS-0.1 acceptance criteria](#20-mvs-01-acceptance-criteria)
- [21. Conformance-test programme](#21-conformance-test-programme)
- [22. Pilot and empirical validation plan](#22-pilot-and-empirical-validation-plan)
- [23. Recommended implementation architecture](#23-recommended-implementation-architecture)
- [24. Development roadmap](#24-development-roadmap)
- [25. Final governing rules](#25-final-governing-rules)

## Appendices

- [Appendix A - Identifier conventions](#appendix-a---identifier-conventions)
- [Appendix B - Generated-view map](#appendix-b---generated-view-map)
- [Appendix C - Permission principles](#appendix-c---permission-principles)
- [Appendix D - Required v0.8 artifact set](#appendix-d---required-v08-artifact-set)
- [Appendix E - Research and methodological references](#appendix-e---research-and-methodological-references)


# 0. Document control and normative status

## 0.1 Purpose

The MathGov Human Interface and Orchestration Standard specifies minimum interaction, workflow, provenance, record-generation, review, challenge, and audit requirements for software or structured processes that implement MathGov.

Its purpose is to reduce avoidable cognitive and administrative burden without weakening evidence requirements, rights protection, catastrophic-risk control, structural viability, uncertainty disclosure, human accountability, or independent challenge.

## 0.2 Governing principle

> **One run, one evidence graph, many generated records.**

A conforming implementation SHOULD collect each material fact, judgment, source, control, and decision once, assign it a stable identifier, and reuse it across every affected MathGov record. A conforming implementation MUST NOT require users to manually reproduce the same substantive information across disconnected forms when a shared source object can be referenced.

## 0.3 Human-automation boundary

> **Automate clerical work, propagation, calculation, synchronization, and contradiction detection. Preserve evidence interpretation, normative judgment, authorization, and accountability as explicit human responsibilities.**

## 0.4 Scope

MHIOS governs:

- guided creation and maintenance of a DecisionRun;
- role-specific and progressively disclosed interfaces;
- tier recommendation and tier-divergence records;
- evidence, claim, assumption, unknown, stakeholder, scenario, control, and dependency orchestration;
- provenance for human, imported, calculated, template, migrated, and AI-assisted content;
- generation of PCCs, Decision Notes, gate records, authority records, execution records, and public summaries from shared source objects;
- reviewer disagreement, challenge, appeal, override, and requalification;
- successor-lineage capture, material-change delta review, candidate locking, and non-heritable execution authority;
- audit reconstruction and independent replay;
- security, privacy, accessibility, usability, and burden measurement;
- anti-audit-theater pattern detection.

## 0.5 Nonclaims

MHIOS does not:

- add a sixth MathGov gate;
- change the seven Union Scopes or seven Welfare Dimensions;
- alter RG, RF/NCRC, TRC, CSV, RLS, PLSS, SGP, or companion-standard semantics;
- decide whether evidence is true merely because it is entered or processed;
- create moral, legal, democratic, engineering, clinical, or execution authority;
- authorize AI-generated judgments;
- allow technical derivation, self-modification, retraining, fine-tuning, composition, or successor creation to manufacture authority;
- replace domain expertise, safety cases, legal review, or democratic legitimacy;
- certify deployment safety;
- make an incomplete run complete merely by rendering a polished report;
- convert a friendly interface label into a new canonical state.

## 0.6 Relationship to existing MathGov components

MHIOS is subordinate to the RippleLogic Canon, canonical registries and schemas, RF/NCRC, TRC, CSV, RLS, SGP, PC-AEP, MFDI, Source Coupling, the Reproducibility and Use Standard, the Agent System, and ripple.md where wrapper claims are made. Where a MHIOS interface rule conflicts with a controlling MathGov rule, the controlling rule prevails.

MHIOS conformance classes and ripple.md assurance levels are orthogonal. A wrapped deployment MUST state both when both are claimed, for example `MHIOS-C2 / ripple.md L2`. MHIOS conformance MUST NOT be presented as evidence of a ripple.md assurance level, and a ripple.md level MUST NOT be presented as MHIOS conformance.

## 0.7 Normative language

- **MUST / MUST NOT** indicates a conformance requirement.
- **SHOULD / SHOULD NOT** indicates an expected practice unless a documented reason justifies departure.
- **MAY** indicates permission.
- **INFORMATIVE** identifies explanatory material that does not create a conformance obligation.

## 0.8 Experimental maturity

Version 0.8 is a candidate implementation standard for prototyping, usability studies, retrospective examples, controlled pilots, and conformance-test development. It MUST NOT be represented as a validated universal interface architecture. Requirements should be revised when evidence shows that a field, screen, workflow, or control creates burden without adding assurance, or creates false confidence despite apparent usability.


## 0.9 Self-application of MathGov claim discipline

MHIOS applies MathGov's own claim-boundary discipline to itself.

| Field | Current declaration |
| --- | --- |
| Material claim | A shared evidence graph, progressive disclosure, bounded automation, and generated records can reduce avoidable burden without materially reducing assurance. |
| Claim type | Design hypothesis with empirical, human-factors, governance, and implementation components. |
| Dependency position | Depends on usable software, institutional incentives, reviewer competence, domain evidence, security, accessibility, and honest organizational authority. |
| Present evidence surface | Internal consistency, schema validity, selected structural tests, document rendering, synthetic examples, and established human-factors reasons to guard against automation bias. |
| Alternative explanations | Burden reduction may come primarily from training or institutional reform; added structure may increase ritual compliance; progressive disclosure may conceal rather than manage complexity; AI assistance may homogenize judgments; anti-theater rules may become new Goodhart targets. |
| Present status | `ASSUMPTION_BOUND / TEST_REQUIRED`. Artifact integrity may be verified; construct validity and operational superiority are not established. |
| Falsification or revision triggers | Higher burden without improved assurance; low reviewer agreement; frequent tier gaming; unacceptably high false reassurance; hollow runs passing cheaply; automation increasing omission or commission errors; objects or screens that do not prevent material errors; inability to replay or reconstruct decisions. |
| Required action | Build the minimal vertical slice, pilot it against a simpler comparator, publish adverse findings, and remove or demote requirements that do not earn their cost. |

A release verifier may report `ARTIFACT_INTEGRITY_PASS`. It MUST NOT translate that result into `CONSTRUCT_VALIDITY_SUPPORTED`, empirical superiority, organizational effectiveness, or deployment assurance. The current MHIOS claim boundary is maintained in `docs/MHIOS_SELF_ASSESSMENT_AND_CLAIM_BOUNDARY_v0_8.md`.

# 1. Design objectives and success conditions

## 1.1 Assurance preservation

Interface simplification MUST NOT omit required evidence, suppress uncertainty, bypass a gate, weaken escalation triggers, hide a non-decisive result, transform monitoring into control, transform permission into admissibility, or transform an AI suggestion into authority.

## 1.2 Burden reduction

The implementation SHOULD reduce repeated data entry, duplicate review, manual synchronization, repeated formatting, unnecessary navigation, and calculations that can be executed transparently from declared inputs.

Burden reduction is not equivalent to deleting difficult judgments. The goal is to remove clerical repetition so that users can spend attention on evidence, affected parties, uncertainty, rights, ruin, controls, and authority.

## 1.3 Legibility

Every material interface state SHOULD answer:

1. What is being claimed?
2. What evidence supports or challenges the claim?
3. What remains unknown or assumption-bound?
4. Who is responsible for the judgment or control?
5. What must reopen if the assumption, configuration, or evidence changes?

## 1.4 Reconstructability

An independent reviewer SHOULD be able to reconstruct the original evidence, each interpretation, state transition, human judgment, automated calculation, override, challenge, authorization, and generated view.

## 1.5 Proportionality

The interface SHOULD adapt required depth to the declared tier, stakes, uncertainty, rights exposure, catastrophic-risk relevance, physical or causal consequence, reversibility, public impact, and configuration volatility. Proportionality MUST NOT suppress a triggered requirement.

## 1.6 Human responsibility

The system MUST expose the named person or lawful authority responsible for each material interpretive judgment, review, override, authority selection, and execution approval. Technical access alone MUST NOT create substantive authority.

## 1.7 Scientific improvement

MHIOS implementations SHOULD measure completion burden, error rates, reviewer disagreement, stakeholder omissions, contradictions detected, replay success, and user comprehension. Requirements should evolve from evidence rather than from the assumption that more fields always produce more assurance.

## 1.8 Measurable success criterion

> **The interface MUST NOT make rigorous action materially more burdensome than superficial compliance, and it MUST make superficial compliance materially more likely to be detected.**

This principle is evaluated through two linked pilot measures:

1. **Valid completion burden.** Median active time and interaction steps for legitimate, well-evidenced completion, stratified by tier and role.
2. **Hollow-pass rate and time to hollow detection.** Measure whether seeded hollow runs pass at all and, when blocked, how quickly the first blocking/challenge state occurs.
3. **False-positive challenge burden.** Measure unnecessary challenges or blocks imposed on legitimate runs and their added time/steps.
4. **Hollow-run detection probability (HRDP).** `HRDP = |D_auto union D_human| / N_hollow`, with automated detection, human detection, overlap, and legitimate-run false-positive rates reported separately.

RHER MAY be retained only as an exploratory descriptor when numerator and denominator refer to comparable completion states. It is undefined when no hollow run reaches the comparison completion state and MUST NOT be the primary first-pilot success criterion. The former candidate `RHER <= 1.50` target is withdrawn pending pilot evidence. Pilot targets, if used, MUST be preregistered for the specific study and reported with uncertainty and sensitivity analyses.

## 1.9 Specification-mass constraint

MHIOS does not presume that every object, role, screen, or pattern earns permanent inclusion. Version 0.8 distinguishes:

- a **12-object minimal vertical slice core** needed to test the central orchestration hypothesis;
- conditional objects activated by decision materiality or stage;
- advanced or research objects that should not burden the first build.

Each object is listed in `registries/MHIOS_OBJECT_JUSTIFICATION_LEDGER_v0_8.yaml` with the error it is intended to prevent, its implementation class, and its evidence status. Until retrospective or prospective evidence shows that an object prevents a material error or measurably improves reconstructability, its value remains a design rationale rather than a validated contribution.

# 2. Interaction invariants

## 2.1 Cascade invariant

The interface MUST represent the controlling sequence as:

`RG -> RF/NCRC -> TRC -> CSV -> RLS`

It MUST NOT depict SGP, UCI, HOI, PC-AEP, MFDI, Source Coupling, the PCC, or an assurance wrapper as additional headline cascade stages.

## 2.2 Qualification-before-ranking invariant

RLS MUST remain unavailable for ordinary ranking until the selectable set has been formed. Later-stage calculations performed after an earlier failure MAY be shown only as `NON_GOVERNING_AUDIT_ONLY` and MUST NOT alter the run state.

## 2.3 State-fidelity invariant

Plain-language labels MUST map to canonical machine states. Interface wording MUST NOT create a new state or silently merge different states.

| Plain-language display | Illustrative canonical state |
| --- | --- |
| Evidence sufficient for the declared claim | RG_SUPPORTED |
| Evidence supports only a narrower claim | RG_NARROWED |
| Grounding insufficient for the requested claim | RG_REFUSED or controlling equivalent |
| Rights floor passed | RF_PASS |
| Later stage not run after prior failure | NOT_EVALUATED_AFTER_PRIOR_FAILURE |
| Rank survivors | RLS enabled only after selectable-set formation |

## 2.4 Provenance invariant

Every material claim, judgment, calculation, status, control, override, authorization, and generated statement MUST identify its source object or source rule.

## 2.5 Human-accountability invariant

Every material interpretive judgment MUST have a named accountable human or legally recognized authority role. Acceptance of AI-generated text records only that a human adopted the suggestion; it does not increase the underlying evidence strength.

## 2.6 Unknown-preservation invariant

Unknown, contested, stale, missing, assumption-bound, and out-of-scope information MUST remain distinguishable. A missing value MUST NOT be silently represented as zero, false, safe, or not material.

## 2.7 No-silent-override invariant

The system MUST NOT silently replace evidence, uncertainty, tier, status, weight, threshold, stakeholder inclusion, scenario set, reviewer judgment, framework result, or authorization. Every material change MUST create an append-only event and a new object version, amendment, or revision branch.

## 2.8 Shared-object invariant

Generated documents are views. They MUST reference stable source-object identifiers and MUST NOT become independent conflicting sources merely because they exist as separate files.

## 2.9 Claim-boundary invariant

The interface MUST display the maximum legitimate claim supported by the declared evidence and configuration. Completion of a workflow MUST NOT be represented as proof that the underlying claim is true.

## 2.10 Configuration-bound assurance invariant

Every material capability, safety, admissibility, reliability, rights, viability, selection, and authorization claim MUST remain bound to a declared configuration, control stack, operating environment, evidence surface, authority state, and validity envelope.

## 2.11 Successor-integrity invariant

> **Derivation is not authorization. A system may help create a candidate successor; it may not create the successor's authority.**

A materially modified or derived system MUST NOT inherit deployment status, tool access, compute access, network access, physical execution permission, approved purpose, assurance status, or recursive successor-building authority merely because a parent system possessed them. The candidate MUST remain non-executable outside its bounded research envelope until a `SuccessorRequalificationRecord` identifies the lineage and material deltas, an independent reviewer determines which prior evidence remains valid, the affected MathGov stages are reopened, and a fresh `ExecutionAuthorization` is bound to the exact candidate configuration.

For parent system `S_t` and candidate successor `S_(t+1)`, `Authority(S_t)` does not imply `Authority(S_(t+1))`.

A high-consequence authorization MUST declare a maximum unreviewed generation depth. The conservative default is one: an authorized system may generate a candidate successor in a bounded research environment, but that candidate may not activate consequential tools or generate an executable descendant before independent requalification. A larger bound requires an explicit, time-limited, evidence-backed, independently authorized exception and still does not transfer execution authority.

MHIOS does not claim that recursive self-improvement is established or imminent. This invariant addresses the governance vulnerability created whenever system identity, capability, autonomy, controls, evaluation validity, or requested authority changes materially.


# 3. Roles, responsibilities, and separation of duties

| Role | Purpose |
| --- | --- |
| Run Owner | Creates and maintains the run; coordinates completion without automatically receiving review or authorization power. |
| Contributor | Supplies evidence, analysis, scenarios, controls, stakeholder information, or domain observations. |
| Domain Reviewer | Reviews domain-specific evidence, claims, methods, validity domains, and warrants. |
| Rights Reviewer | Reviews protected stakeholders, floor/categorical/severe-hazard channels, subgroups, and non-compensability. |
| Risk Reviewer | Reviews scenario discovery, probabilities, severity, dependence, uncertainty, and TRC calculation. |
| CSV Reviewer | Reviews containment, controls, dependencies, reversibility, monitoring, execution viability, and post-state integrity. |
| RLS Reviewer | Reviews impact construction, weights, uncertainty, PLSS, welfare cells, and decisiveness. |
| SGP Reviewer | Reviews SGP evidence narratives and typed interpretations without collapsing protection into authority. |
| Challenge Reviewer | Adjudicates formal challenges and appeals independently of the initial judgment where feasible. |
| Decision Authority | Selects among legally or institutionally available options where authority judgment remains necessary. |
| Execution Authority | Approves execution only after required preconditions, controls, and authority conditions are satisfied. |
| Auditor | Inspects complete provenance, state transitions, calculations, challenges, and generated views without altering the run. |
| Public Observer | Views an appropriately redacted transparency surface. |
| System Administrator | Maintains technical infrastructure but receives no substantive decision authority merely through technical access. |
| AI Assistant | Provides non-authoritative assistance subject to the Human-Judgment Firewall. |

## 3.1 Role separation

A conforming system SHOULD support separation among run ownership, substantive review, decision authority, execution authority, audit, and system administration. High-stakes Tier 2 and Tier 3 runs SHOULD include at least one reviewer who is not subordinate to the run owner where organizational structure permits.

## 3.2 Conflict-of-interest declarations

Material reviewers and authorities MUST disclose organizational relationships, financial or personal interests, prior advocacy, operational responsibility, and other conflicts that could affect judgment. Disclosure does not automatically disqualify a reviewer, but it MUST be visible to independent review and public reporting where legally and ethically appropriate.

## 3.3 Minimum responsibility fields

Every material task SHOULD identify the accountable role, assigned person or office, due date, review status, authority boundary, escalation route, and continuity plan where failure would create a control gap.

## 3.4 Technical access is not authority

System administrators, software developers, model providers, and data custodians MUST NOT receive decision or execution authority merely because they can modify infrastructure. Privileged technical actions MUST be logged and independently reviewable.


# 3A. Institutional preconditions and incentive integrity

Software cannot supply organizational independence, budget, authority, or protection against retaliation. An implementation that satisfies interface and schema requirements may still be operationally decorative when institutional conditions make honest escalation costly or futile.

## 3A.1 Minimum institutional preconditions

For reviewed Tier 2 and Tier 3 use, the organization SHOULD provide:

- budgeted reviewer time that is not treated as uncompensated overhead;
- a challenge and escalation process with documented non-retaliation protection;
- an approver for downward tier divergence who is outside the run owner's direct reporting line where feasible;
- authority for reviewers to delay, narrow, redesign, or refuse claims without requiring informal permission from the interested delivery team;
- protected channels for affected stakeholders and dissenting reviewers;
- periodic outcome audits comparing downgraded, maintained, escalated, and refused runs;
- consequences and remediation when material tier downgrades, evidence suppression, or authority misstatements are confirmed.

## 3A.2 Institutional Preconditions Record

A Tier 2 or Tier 3 operational implementation MUST record whether these preconditions are present, partial, absent, contested, or legally constrained. Where a gate-material precondition is absent, the system MUST narrow its conformance and assurance claim and display `INSTITUTIONAL_PRECONDITIONS_INCOMPLETE` or the controlling equivalent.

## 3A.3 No software substitution

Conflict disclosure, workflow completion, and electronic sign-off do not establish independence. MHIOS MUST NOT imply that a well-designed interface compensates for incentives that reward passing, punish delay, suppress dissent, or deny reviewers sufficient time and authority.

## 3A.4 Outcome accountability

Organizations SHOULD compare declared assumptions, tier decisions, dissent records, controls, and predicted outcomes with incidents and observed outcomes. Trend review should ask whether lower-tier classifications, waived requirements, or repeated reviewer acceptance were associated with later harm or unreconstructable decisions.

The complete profile is defined in `docs/INSTITUTIONAL_PRECONDITIONS_PROFILE_v0_8.md`.

# 4. Human-Judgment Firewall and provenance

## 4.1 Contribution origin

Every material field MUST carry one origin status:

- `HUMAN_ENTERED`
- `IMPORTED_FROM_SOURCE`
- `SYSTEM_CALCULATED`
- `AI_SUGGESTED`
- `AI_EXTRACTED`
- `TEMPLATE_DEFAULT`
- `MIGRATED_FROM_PRIOR_RUN`

## 4.2 Review status

Every material interpretive field MUST carry one review status:

- `UNREVIEWED`
- `HUMAN_REVIEWED`
- `HUMAN_MODIFIED`
- `REVIEW_DISAGREEMENT`
- `CONTESTED`
- `AUTHORIZED`
- `REJECTED`
- `SUPERSEDED`

## 4.3 AI-permitted assistance

AI MAY summarize evidence, propose claims, suggest stakeholders or scenarios, detect contradictions, draft plain-language explanations, identify missing records, map narrative evidence to candidate typed interpretations, and propose anti-audit-theater challenges.

## 4.4 AI-prohibited authority

AI MUST NOT independently exclude a stakeholder, declare evidence credible, determine rights materiality, approve catastrophic-risk exposure, establish physical admissibility, assign legal authority, authorize emergency action, grant SGP participation or authority, issue final execution approval, or certify its own output.

## 4.5 Acceptance rule

Human acceptance of an AI suggestion MUST create a ReviewerJudgment linking the original suggestion, the reviewer, modifications, evidence considered, rationale, and final disposition. Acceptance MUST NOT transform weak or missing evidence into strong evidence.

## 4.6 AI trace

An AI contribution SHOULD preserve service/model identifier, version where available, task description, source materials, timestamp, output hash, reviewer, modification history, and final disposition. Confidential prompt content MAY be redacted from public views but SHOULD remain available to authorized audit where lawful.

## 4.7 No-AI operating mode

A conforming MHIOS implementation MUST remain usable when AI assistance is disabled. Core calculations, state routing, provenance, reviews, exports, and replay MUST NOT depend on an unavailable proprietary model.


## 4.8 Automation-bias controls

Provenance labels are necessary but not sufficient. Human reviewers may over-rely on plausible automated suggestions even when instructed to verify them.

For gate-material claims, evidence classifications, stakeholder exclusions, risk states, and authority-relevant judgments, a conforming assisted interface SHOULD use an **independent-first-pass control**:

1. the reviewer records an initial judgment and rationale without seeing the AI recommendation;
2. the system then reveals the AI suggestion and its sources;
3. the reviewer records agreement, modification, or rejection and explains material divergence;
4. the system preserves both passes.

A reviewer MAY request early AI assistance when necessary, but the exception and reason MUST be recorded.

## 4.9 Acceptance and modification diagnostics

The system SHOULD measure AI suggestion exposure, acceptance without modification, acceptance with modification, rejection, time-to-review, source inspection, and reviewer divergence. Near-universal acceptance across a material sample is not evidence of efficiency by itself; it is a review trigger for possible rubber-stamping, task triviality, or over-trust.

## 4.10 AI-off comparison

Pilot deployments SHOULD sample comparable tasks or runs under AI-assisted and AI-disabled conditions. The study should compare omissions, commission errors, state assignments, stakeholder coverage, completion burden, confidence, and reviewer agreement. Divergence is evidence to investigate, not automatic proof that either condition is superior.

# 5. Progressive disclosure and information architecture

## 5.1 Four interface layers

### Layer 1 - Public or learner view

Shows Reality, Rights, Ripples, Qualify first, and Rank second. It explains the logic without exposing all machine identifiers.

### Layer 2 - Operator view

Shows required questions, evidence tasks, missing items, current status, responsible roles, and next actions.

### Layer 3 - Reviewer view

Shows canonical terminology, evidence status, thresholds, calculations, assumptions, uncertainties, challenges, downstream dependencies, and claim boundaries.

### Layer 4 - Auditor and implementation view

Shows raw states, schemas, formulas, versions, hashes, transition events, overrides, validator output, redactions, and exports.

## 5.2 No-information-loss rule

Progressive disclosure MAY hide complexity temporarily but MUST NOT delete, merge, or alter the underlying information.

## 5.3 Explainability on demand

Every calculated or assigned status SHOULD expose the controlling rule, input objects and values, evidence and unknowns, reviewer and date, blocking or narrowing reasons, required action, and route to challenge or revise.

## 5.4 Plain-language/canonical duality

The operator-facing question SHOULD be understandable without specialized terminology. The system MUST preserve the corresponding canonical status and record beneath the interface.

> **Question:** Do we have enough reliable evidence to make this claim at the requested strength?  
> **Canonical record:** `MethodologicalIntegrityStatus = ASSUMPTION_BOUND`

## 5.5 Cognitive-load controls

The interface SHOULD use task-focused steps, contextual definitions, role-specific queues, saved progress, clearly labeled defaults, and summary views. It SHOULD NOT display every field from every companion standard at once.


# 6. Tier orchestration and anti-downgrade controls

## 6.1 System recommendation

The system MUST derive a recommended tier from declared materiality triggers. It MUST NOT present tier selection merely as a preference for more or less paperwork.

## 6.2 Trigger families

The TierAssessmentRecord SHOULD evaluate:

- rights exposure and severe-harm pathways;
- catastrophic or irreversible risk;
- physical, medical, biological, ecological, or cyber-physical execution;
- critical infrastructure;
- vulnerable or unrepresented populations;
- autonomous or agentic action;
- public, cross-border, or biosphere externalities;
- legal novelty or contested authority;
- high uncertainty, evidence conflict, or source-coupling weakness;
- long-duration commitment, lock-in, or difficult reversibility;
- emergency action;
- major configuration or control-stack change.

## 6.3 Required tier fields

The system MUST preserve `system_recommended_tier`, `operator_selected_tier`, trigger results, divergence status, divergence rationale, approving reviewer, review status, and reopen trigger.

## 6.4 Downward deviation

A downward deviation MUST identify each triggered condition being discounted, explain why it is not material, identify the accepting authority, remain challengeable, and remain visible in audit exports.

## 6.5 Automatic escalation

A run MUST reopen tier assessment when newly entered evidence activates a higher-tier trigger. The system SHOULD identify newly required records and reuse existing source objects wherever possible.

## 6.6 Burden-gaming signal

Repeated downward divergence across runs SHOULD create a governance-level trend review. It SHOULD NOT automatically establish misconduct, but it MUST NOT remain invisible.


# 7. Shared evidence graph and source-object architecture

## 7.1 Graph principle

The system SHALL maintain linked decision objects rather than treating documents as independent sources. The graph may be implemented in a relational database; a graph database is not required.

## 7.2 Source-object principle

Evidence items, claims, judgments, controls, calculations, and state transitions are operational source objects. Generated DOCX, PDF, HTML, and public summaries are derived views.

## 7.3 Stable identifiers

Every object MUST have a stable identifier. Identifiers MUST remain stable across generated views and revisions unless a genuinely new object is created.

## 7.4 Universal fields

Every object SHOULD carry `object_id`, `object_type`, `run_id`, `version`, `status`, `title`, `description`, creation and update metadata, `entry_origin`, `review_status`, `responsible_role`, validity dates, configuration binding, source links, dependency links, challenge links, supersession links, sensitivity class, visibility class, retention class, and content hash.

## 7.5 Versioning

Material changes MUST create a new object version, amendment, or revision branch. A post-result change to an assumption, threshold, weight, scope, scenario, or evidence basis MUST NOT be represented as uninterrupted continuation of the original frozen run.

## 7.6 Evidence reuse

When one evidence item affects multiple records, the system SHOULD link the same object rather than copy its text. A controller temperature envelope, for example, may constrain Reality Grounding, PC-AEP, Source Coupling, CSV, monitoring, requalification, and public claim language.

## 7.7 Dependency reopening

A material object change MUST identify every dependent object and stage that requires re-review. The user MUST be able to see why a stage reopened.

## 7.8 Generated-view integrity

Every generated view MUST include run ID, run version, generation time, template and generator versions, source-object identifiers, content hash, claim boundary, redaction profile, and stale/current status.


# 8. Canonical MHIOS object model

The machine-readable object catalogue is provided in `registries/MHIOS_OBJECT_MODEL_v0_8.yaml` and the validation schema in `schemas/mhios_run_export_v0_8.schema.json`.

The catalogue is intentionally partitioned by implementation class. The first build uses the minimal vertical slice core; conditional and advanced/research objects are activated only when the case or pilot question requires them.

## 8.0A Minimal vertical slice core objects

| Object | Purpose | Principal fields |
| --- | --- | --- |
| DecisionRun | One bounded MathGov evaluation and its complete lifecycle. | run_id, run_title, decision_question, purpose, decision_owner, authority_boundary, configuration_id, environment_id, time_horizon, geographic_scope, legal_context, declared_tier, recommended_tier, run_state, transition_or_action_boundary, reality_surface, consequence_pathways, claim_boundary, freeze_timestamp, branch_parent, branch_id, branch_status, governing_branch_id, merge_parent_ids, institutional_preconditions_status |
| Option | Candidate action, policy, design, delay, redesign, refusal, or baseline path. | option_id, name, description, option_type, baseline_or_comparator, current_state, proposed_transition, post_state, implementation_path, configuration_effect, reversibility |
| ConfigurationRecord | Exact system configuration and validity envelope to which qualification and claims apply. | configuration_id, system_name, software_version, model_version, hardware_version, control_stack, execution_mandate_record_ids, tools, data_sources, operating_environment, authority_state, validity_envelope, known_limitations, qualification_status |
| Claim | A proposition used to support, qualify, rank, authorize, or communicate the run. | claim_id, claim_text, claim_type, claim_domain, warrant_domains, claim_strength, claim_owner, validity_domain, claim_boundary, evidence_status, methodological_integrity_status, falsification_or_revision_trigger, downstream_uses |
| EvidenceItem | Traceable evidence, counterevidence, measurement, testimony, model result, source, or warrant. | evidence_id, evidence_type, source_title, source_author, source_date, source_location, content_summary, original_content_reference, reliability_status, relevance_status, freshness_status, validity_domain, supports_claims, challenges_claims, known_limitations, freshness_policy_id, last_verified_at, next_review_at, staleness_status, staleness_rationale |
| MaterialUnknown | Unknown condition material to rights, ruin, viability, ranking, authority, or claim strength. | unknown_id, unknown_description, why_unknown, materiality, potential_rights_effect, potential_tail_effect, potential_csv_effect, potential_ranking_effect, resolution_path, deadline, responsible_role, claim_action |
| StakeholderInstance | Stakeholder-in-role-in-context with a declared exposure pathway. | stakeholder_instance_id, stakeholder_type, role, context, exposure_path, vulnerability, representation_method, voice_or_proxy, scope_mappings, rights_exposures |
| GateRecord | Base record for the RG claim-authority precondition and RF/NCRC, TRC, and CSV option-rejecting gates without collapsing their roles. | gate_record_id, gate_type, record_role, option_id, status, controlling_rule, inputs, evidence_links, unknown_links, reviewer, review_timestamp, constraint_reasons, canon_audit_flags, constitutive_control_ids, required_actions, reopen_triggers |
| ReviewerJudgment | Named human interpretation, review, agreement, disagreement, or adoption of assistance. | judgment_id, subject_object_id, reviewer, reviewer_role, judgment, rationale, evidence_considered, uncertainty, conflict_of_interest, review_status |
| DecisionStateRecord | Single source for selectable set, framework verdict, decisiveness and authority-selection need. | decision_state_id, selectable_options, framework_verdict, framework_selected_option, decisiveness, gap, threshold, authority_selection_required, run_decision_state, controlling_calculation_ids |
| GeneratedView | Human- or machine-readable report generated from shared source objects. | view_id, view_type, source_object_ids, template_version, generated_at, generator_version, content_hash, redaction_profile, stale_status, source_revision_map, inference_risk_review, suppressed_edges, residual_disclosure_risk |
| InteractionEvent | Append-only event for creation, edit, review, challenge, override, calculation, export, or authorization. | event_id, run_id, event_type, actor_id, actor_role, timestamp, target_object_id, previous_hash, new_hash, reason, metadata, base_revision, proposed_revision, conflict_status, merge_disposition |

## 8.0B Conditional objects

| Object | Purpose | Principal fields |
| --- | --- | --- |
| TierAssessmentRecord | Trigger-derived recommended tier and any justified divergence. | tier_assessment_id, system_recommended_tier, operator_selected_tier, trigger_results, tier_divergence, divergence_rationale, approving_reviewer, review_status, reopen_trigger |
| Assumption | Explicit assumption whose failure may alter claims, gates, ranking, or authority. | assumption_id, assumption_text, necessity, basis, uncertainty, affected_claims, affected_gates, failure_consequence, sensitivity_test, revision_trigger |
| CategoryGroundingRecord | Grounds a material category and prevents term or category authority laundering. | category_id, material_category, definition, category_discriminator, primitive_basis, inclusion_boundary, exclusion_boundary, noncollapse_pairs, reference_structure, evidence_surface, category_maturity_status, semantic_debt_flag, refusal_condition |
| ScopeMapping | Maps a stakeholder instance to one or more Union Scopes with redundancy controls. | scope_mapping_id, stakeholder_instance_id, union_scope, mapping_rationale, redundancy_method, effect_token, allocation_coefficient, review_status |
| RightsExposure | Option-specific rights exposure through floor, categorical, and severe-hazard channels. | rights_exposure_id, stakeholder_instance_id, right_id, option_id, exposure_path, floor_channel, categorical_channel, severe_hazard_channel, subgroup, uncertainty, evidence_links, rf_status |
| Scenario | Option-specific scenario with probability bounds, severity, irreversibility, dependencies and evidence. | scenario_id, option_id, scenario_family, description, probability_lower, probability_central, probability_upper, severity_class, catastrophe_cells, irreversibility, dependencies, evidence_links, scenario_status |
| Control | Preventive, limiting, monitoring, detection, shutdown, rollback, recovery, legal, or procedural control. | control_id, control_name, control_type, control_owner, target_risk, preventive_function, limiting_function, detection_function, shutdown_function, rollback_function, recovery_function, verification_method, activation_condition, failure_mode, residual_risk |
| Dependency | External or internal dependency whose failure can alter viability or qualification. | dependency_id, dependency_name, dependency_type, provider, required_for, failure_effect, substitutability, concentration_risk, verification_status, monitoring_status, requalification_trigger |
| PhysicalCausalAdmissibilityEvidenceProfile | MHIOS representation of PC-AEP without replacing the governing PC-AEP standard. | pcaep_id, option_id, candidate_generation_source, physical_or_causal_model, validity_domain, boundary_conditions, uncertainty_range, failure_modes, reversibility_boundary, verification_simulation_empirical_test_or_expert_warrant, admissibility_warrant_source, monitoring_and_shutoff, residual_unknowns, required_claim_action, pcae_status |
| MethodologicalIntegrityRecord | MHIOS representation of MFDI for a material claim. | mdi_id, claim_id, claim_type, claim_domain, warrant_domains, cross_domain_bridges, legal_regulatory_context, dependency_position, starting_assumptions, definition_or_operator, necessity_or_alternative_check, alternative_explanations, test_surface, revision_trigger, uncertainty_method, downstream_dependencies, re_derivation_scope, required_claim_action, method_status |
| CapabilityAuthorityDecompositionRecord | Split record for material automation, autonomy, agentic, reasoning, intent, capability, and execution-authority claims. | capability_decomposition_id, subject_system_or_configuration_id, triggering_terms, candidate_generation_method, reference_source, constraint_sources, objective_source, objective_change_authority, admissibility_warrant_sources, execution_interface, execution_scope, execution_authority_source, revocation_authority, safe_state_or_shutdown_path, requalification_trigger, reviewer_status, required_claim_action |
| SourceCouplingRecord | Connects a claimed capability to enabling and boundary conditions. | source_coupling_id, claim_id, claimed_capability, enabling_conditions, boundary_conditions, source_evidence, generator_output_distinction, inherited_assumptions, downstream_compensations, source_debt_flag, recheck_trigger, source_coupling_status, required_claim_action |
| RLSCellRecord | One Union Scope x Welfare Dimension cell for one option. | rls_cell_id, option_id, union_scope, welfare_dimension, impact_instances, base_impact, confidence, temporal_weight, cell_multiplier, uncertainty, effective_weight, nonmaskable_status, evidence_links |
| WeightRecord | Constitutional floor, democratic tuning, PLSS adjustment, final weight and sensitivity. | weight_record_id, weight_type, constitutional_floor, democratic_tuning, plss_adjustment, final_weight, authority_source, approval_status, sensitivity_result |
| CalculationRecord | Reproducible calculation trace with inputs, engine, formula version, output and hash. | calculation_id, calculation_type, formula_version, input_object_ids, input_values, output_value, units, engine, engine_version, timestamp, rounding_rule, validation_status, content_hash |
| Challenge | Formal challenge, disagreement, appeal, or missing-stakeholder claim. | challenge_id, target_object_id, challenger, challenge_type, challenge_text, evidence_links, severity, status, assigned_reviewer, resolution, resolution_rationale, appeal_path |
| AuthoritySelectionRecord | Lawful or institutional selection where authority judgment remains necessary. | authority_selection_id, decision_authority, legal_or_institutional_mandate, options_available, framework_result, selected_option, selection_basis, departure_from_framework_result, departure_rationale, conflicts_declared, conditions, review_status |
| ExecutionMandateRecord | Versioned, scoped and time-bound human-defined mandate source; it neither establishes physical/causal admissibility nor creates legitimate authority by itself. | mandate_record_id, authority_source, authority_scope, jurisdiction_or_applicability_scope, instrument_id, instrument_version, action_scope, subject_scope, applicability_conditions, effective_from, effective_until, revocation_authority, revocation_status, supersession_status, trust_status, source_hash, signature_or_verification_evidence, last_verified_at, mandate_status, conflict_ids, requalification_trigger, reviewer_status |
| ExecutionAuthorization | Separates selection from current mandate and authority to execute, and binds both to one exact action and MathGov qualification snapshot. | execution_authorization_id, action_instance_id, action_specification_hash, qualification_snapshot_hash, selected_option, execution_authority, authorization_basis, authorization_basis_refs, configuration_binding, authorization_evaluated_at, mandate_snapshot_hash, mandate_currency_disposition, required_controls, required_control_checks, preconditions, precondition_checks, evidence_currency_status, effective_time, expiry, rollback_authority, shutdown_authority, execution_status, execution_disposition |
| RequalificationTrigger | Condition requiring reopening after material change, incident, drift, or new evidence. | trigger_id, trigger_type, description, affected_objects, activation_condition, activated_at, required_reopen_scope, responsible_role, resolution_status |
| SuccessorRequalificationRecord | Preserves technical lineage and material deltas while preventing a candidate successor from inheriting parent authority. | parent_configuration_id, candidate_configuration_id, lineage_relation, generation_depth_from_last_independent_qualification, maximum_unreviewed_generation_depth, material_change_dimensions, capability/autonomy/tool/objective/evaluation/control/risk/authority deltas, evidence-reuse basis, creator identity, independent reviewer, inherited_authority, candidate_lock_status, fresh_qualification_status, execution_authorization_id, rollback boundary, disposition, reopen triggers |
| EmergencyOrderRecord | Canon emergency rights comparison when no option passes RF/NCRC; never an ordinary pass or RLS selection. | emergency_order_id, emergency_declaration, candidate_option_ids, right_priority_order, component_priority_order, violation_tuples_by_option, comparison_trace, resolving_coordinate, unresolved_unknown_fields, challenger_attestation, mitigation_and_remediation_plan, monitoring_and_appeal_path, exit_and_review_cadence, return_to_normal_triggers |
| MaterialObligationRecord | Complete carried-duty record for every obligation material to selectability, execution, monitoring, repair, or requalification. | obligation, accountable_authority, operational_carrier_or_execution_path, authority_and_capacity_basis, activation_trigger, scope, required_action, response_deadline_or_window, evidence_of_discharge, review_or_expiry, challenge_route, delegation_acceptance, backup_or_successor, nonperformance_trigger, missed_duty_escalation, amendment_waiver_suspension_retirement_authority, change_control_rule, residual_responsibility, control_effectiveness_status, obligation_status, linked_control_ids |
| ConsequenceTempoRecord | Dependency-aware comparison of consequence propagation and the credible control critical path. | option_id, action_initiation_mode, earliest_material_harm_boundary, timing_elements, declared_safety_margin, constitutional_latency, harm_of_delay, tempo_disposition, evidence_refs, reviewer_status, reopen_trigger |
| ResponsibilityContinuityRecord | Typed responsibility and accepted handoffs from evidence through remedy and residual responsibility. | decision_authority, evidence_accountability, model_analytical_responsibility, operational_responsibility, execution_authority, intervention_authority, appeal_owner, communication_owner, remedy_owner, residual_responsibility, handoffs, material_obligation_ids, human_compensation_load_record_ids, reconstructability_status, reopen_trigger |
| HumanCompensationLoadRecord | Hidden human exception-handling, memory, relationship work, recovery, and weak-signal detection when material. | carrier_role_classes, hidden_work_performed, formal_workflow_gap, burden indicators, single-person dependency, recovery effects, consequence if stopped, evidence, privacy/non-retaliation, preservation or redesign action, review trigger, status |
| ProjectionPreRegistrationRecord | Signed and timestamped freeze of the projection map for Tier 3 and pilots. | decision boundary, horizon, options, stakeholder map, rights and TRC parameters, CSV triggers, weights, SGP bindings, kernel, sensitivity, refusal conditions, freeze hash, timestamp, signature, post-observation modification |
| RefusalRecord | Canon Refusal evidence and re-run path, separate from gate failure and ordinary authority choice. | trigger code and description, affected options/scopes/dimensions/cells, evidence and provenance, no-action status, escalation, provisional status, re-run conditions, reviewer |
| ComputationalClosureRecord | Exact scopes, horizons, propagation paths, and externalities included and excluded from computation. | scopes evaluated/guardrail/outside, horizons evaluated/outside, kernel mode, edges included/excluded, externalities excluded, claim boundary |
| CoreRecordAttachment | Schema-identified, hash-bound, validated reference to a triggered Core or companion record intentionally not duplicated by MHIOS. | record type, governing source/version, trigger, tier/claim scope, artifact and schema refs, content hash, validation status/evidence, reviewer, claim effect if missing or invalid |

## 8.0C Advanced and research objects

| Object | Purpose | Principal fields |
| --- | --- | --- |
| SGPEvidenceNarrative | Preserved qualitative SGP evidence, context, ambiguity, and alternatives. | sgp_narrative_id, subject_configuration, source_observation, context, alternative_interpretations, uncertainty, original_source, reviewer_comments |
| SGPTypedInterpretation | Typed SGP interpretation traceable to preserved narrative evidence. | sgp_interpretation_id, sgp_narrative_id, register, status, evidence_strength, what_follows, what_does_not_follow, reviewer, challenge_status, revision_trigger |
| MonitoringSignal | Observed signal that may confirm, challenge, or reopen qualification. | signal_id, target_object_id, metric, source, expected_range, observed_value, timestamp, materiality, control_response, requalification_effect |
| OutcomeObservation | Observed outcome for learning, accountability, and model revision. | outcome_id, option_id, observed_effect, affected_stakeholders, expected_or_unexpected, severity, evidence_links, comparison_to_prediction, model_update_required, requalification_required |
| BurdenObservation | Empirical usability and burden measurement; never a gate result. | burden_observation_id, run_id, stage, metric, value, unit, observer, timestamp, notes |

## 8.1 Object-model boundary

MHIOS object definitions organize interaction and provenance. They do not supersede governing semantic definitions in the MathGov Canon or companion standards. Where an object embeds a PC-AEP, MFDI, SGP, gate, or scoring status, the controlling component defines the meaning.

## 8.2 Implementation classes

The 47-object catalogue is a superset, not the mandatory data-entry surface for every run.

- `MVS_CORE`: 12 objects required for the first empirical vertical slice.
- `CONDITIONAL`: activated by tier, materiality, domain, stage, or authority need.
- `ADVANCED_RESEARCH`: deferred until a pilot or specialized use justifies the burden.

The classification does not remove substantive MathGov requirements. A conditional object may become mandatory when its trigger holds. The first build MUST NOT expose all 47 object types as separate forms.

## 8.0D Gate-role and constitutive-control integrity

Every `GateRecord` MUST carry `record_role`. RG uses `CLAIM_AUTHORITY_PRECONDITION`; RF/NCRC, TRC, and CSV use `OPTION_REJECTING_GATE`. An interface may show that `RG_REFUSED` removes an option from the claim-bounded qualified set, but it MUST explain that this follows from insufficient claim authority rather than an ethical gate verdict.

When a selectable option has `CSV_PASS_WITH_CONTROLS`, its CSV record MUST carry non-empty `constitutive_control_ids` that resolve to current `MaterialObligationRecord` objects. Each record MUST satisfy Canon Section 4.10A and MAY link one or more lower-level `Control` objects; a `Control` identifier alone is insufficient. The interface MUST render the carried obligations and any linked controls as constitutive parts of the option. Removing, expiring, failing, or materially weakening a constitutive obligation or linked control reopens CSV and removes the unconditional selectable-state display until requalification.

MHIOS-local `SCR-*` identifiers are reserved exclusively for screens. If structural checks receive identifiers, they MUST use `STC-*`. Neither namespace is a Canon audit-flag namespace. Where a MHIOS condition implies a Canon audit flag, the record MUST carry the Canon token verbatim in `canon_audit_flags`; MHIOS MUST NOT invent, rename, or silently rescope controlling Canon tokens.

## 8.3 Core-integration and non-collapse rule

MHIOS object fields that represent a Core companion record MUST preserve every field whose separation carries a governing non-collapse purpose. The interface MAY group fields visually, but the exported source objects MUST retain the canonical distinctions. In particular:

- `candidate_generation_source`, `verification_simulation_empirical_test_or_expert_warrant`, and `admissibility_warrant_source` are distinct PC-AEP fields. A generator, simulation, test result, expert warrant, and authority source MUST NOT be collapsed into one generic `admissibility_warrant`.
- `necessity_or_alternative_check` is distinct from `alternative_explanations` in MFDI. The former records whether a necessity claim has survived comparison with alternatives; the latter records the alternatives themselves.
- SGP protection, participation, capability, and authority fields remain separately typed.
- Gate status, framework selection, authority selection, execution authorization, and observed outcome remain separate records.
- A named control and a carried material obligation remain separate: the latter preserves authority, capacity, handoff acceptance, deadlines, escalation, expiry, change control, residual responsibility, and effectiveness.
- Consequence tempo and responsibility continuity remain separate from CSV status and from execution authorization.

The complete mapping is governed by `docs/MHIOS_MATHGOV_CORE_INTEGRATION_PROFILE_v0_8.md` and `registries/MHIOS_TO_CORE_SCHEMA_CROSSWALK_v0_8.yaml`. When a crosswalk entry conflicts with the pinned Core release, the Core source controls and the MHIOS package MUST be updated before a stronger conformance claim is made.


## 8.0E Core-record coverage and Tier-3 export boundary

MHIOS does not need a separate data-entry form for every Core record, but it MUST account for every record triggered by the pinned Core and invoked companions. `registries/MHIOS_CORE_RECORD_COVERAGE_v0_8.yaml` is the controlling coverage matrix for this release.

A coverage slot is satisfied only when (a) the required information is represented by the declared native MHIOS object, or (b) a `CoreRecordAttachment` identifies the governing record contract or schema, artifact, version, content hash, validation evidence, reviewer disposition, and claim effect if missing or invalid. A filename, URL, generic attachment, or unchecked pointer is insufficient.

The following records are native in v0.8 because they control orchestration timing, carried duties, mandate currency, refusal, or claim boundaries: `MaterialObligationRecord`, `ConsequenceTempoRecord`, `ResponsibilityContinuityRecord`, `HumanCompensationLoadRecord`, `ProjectionPreRegistrationRecord`, `RefusalRecord`, `ComputationalClosureRecord`, and the conditional `ExecutionMandateRecord`. Other triggered records remain governed by their Core or companion source and are referenced through validated attachments to avoid duplicating normative semantics.

MHIOS v0.8 MAY generate a Tier-3-complete PCC only when the coverage matrix reports every triggered slot as satisfied and every required attachment validates against the pinned governing contract. Otherwise the generated view MUST be labeled `INCOMPLETE_FOR_TIER3_PCC`, identify the unsatisfied slots, and MUST NOT support a complete Tier-3, deployment-readiness, validation, or ProofPack claim.

This coverage mechanism establishes representational and validation capacity only. It does not establish that the attached evidence is true, that a reviewer judgment is correct, that a control is effective, or that a deployment is safe or lawful.

## 8.0F Execution mandate currency and ordered readiness contract

MHIOS keeps six warrant roles distinct: domain evidence for physical or causal claims; MathGov qualification and selection; a human-defined mandate basis; a named legitimate authority; active controls and satisfied preconditions; and conflict/requalification status. Evidence in one role does not silently substitute for another.

An approved execution state MUST satisfy every prerequisite below for the same action instance, exact action specification, selected option, configuration, scope, and evaluation time:

For audit references, this ordered conjunction is named `EXECUTION_READINESS(a,t)`. The identifier names the complete contract below; it is not a shortcut, independent authority source, or substitute for any prerequisite.

1. the option is selectable and selected under the pinned MathGov run;
2. the action has a current qualification snapshot, including VALID current state, ADMISSIBLE transition, VIABLE post-state, and CURRENT qualification;
3. any material physical or causal execution claim has a current domain-appropriate warrant inside its validity domain;
4. every human-defined mandate basis is current, applicable, verified, unrevoked, unsuperseded, conflict-free, and bound to the exact configuration;
5. a named legitimate execution authority applies to the exact action, scope, configuration, and time;
6. required evidence is current, controls are active, preconditions are satisfied, and pause/shutdown and rollback authorities are named;
7. no material conflict or requalification trigger is unresolved; and
8. the authorization freezes `action_instance_id`, `action_specification_hash`, `qualification_snapshot_hash`, `mandate_snapshot_hash`, and `authorization_evaluated_at`.

This ordered contract is intentionally not reduced to a two-factor slogan or a single formula. The prerequisites have different sources, failure modes, and reviewers. Passing the schema and validator establishes record conformance only; it does not prove physical safety, legal validity, democratic legitimacy, control effectiveness, or deployment readiness.

Every human-defined mandate used to support approved execution MUST be represented by an `ExecutionMandateRecord`. The record identifies its source, instrument and version, action and subject scope, applicability conditions, effective interval, revocation and supersession states, verification evidence, source hash, conflicts, reviewer status, and requalification trigger. A mandate record is a governance input. It is not physical evidence and does not create legitimate authority by itself.

An approved `ExecutionAuthorization` MUST identify the selected option, exact action instance, exact action specification, exact configuration, frozen MathGov qualification snapshot, current mandate records, named authorities, current evidence, active required controls, satisfied preconditions, monitoring, pause/shutdown, rollback, and conflict disposition. Empty control or precondition sets are allowed only with an explicit `NOT_APPLICABLE` disposition and non-empty rationale.

An expired, not-yet-effective, revoked, superseded, conflicted, unverified, source-hash-invalid, scope-inapplicable, stale-evidence, inactive-control, unsatisfied-precondition, configuration-unbound, action-mismatched, qualification-stale, or trigger-affected surface MUST NOT serialize an approved execution status. It MUST block execution or require requalification. A signed, versioned, locally pinned mandate snapshot MAY be used when activation, rollback, failure, conflict, and requalification behavior are qualified and auditable.

## 8.0H Computational Context Declaration View

### Purpose

The human interface should not present an umbrella label such as “AI,” “agent,” “autonomous system,” “model,” or “controller” as sufficient information for consequential review. For consequential digital, cyber-physical, or physical actions, the interface SHOULD present a compact Computational Context Declaration containing:

| Field | Required meaning |
| --- | --- |
| `computational_problem_or_object` | What computational question or object is actually being addressed? |
| `architecture_and_configuration` | What exact architecture, system composition, version, tools, permissions, control stack, and configuration are active? |
| `demonstrated_capability` | What has this exact configured system demonstrated it can do within the evidence boundary? |
| `assigned_task` | What specific task or action is the system being asked to perform? |
| `deployment_domain` | In what physical, digital, institutional, commercial, scientific, or social environment will the task occur? |
| `required_evidence_standard` | What evidence must support the material claims for this domain and consequence class? |
| `consequence_interface` | What downstream effect can the output technically produce: inform, recommend, constrain, authorization request, actuate, execute, or other? |
| `legitimate_authority_basis` | What separately valid human, legal, or institutional authority, if any, applies to this exact action, configuration, scope, and time? |

### Critical interface distinctions

> **Consequence Interface ≠ Legitimate Authority**

The interface MUST NOT visually or semantically imply that because a system can technically execute, actuate, constrain, or recommend an action, it has legitimate authority to do so.

> **Assigned task ≠ justified task**

The fact that an operator, model, planner, workflow, policy, or institution has assigned a task does not establish that the task is ethically admissible, rights-compatible, structurally viable, lawful, or legitimately authorized.

### Existing-record rule

The Computational Context Declaration is a `GeneratedView`, not a new authoritative object type. The view SHOULD populate from existing `ConfigurationRecord`, `CapabilityAuthorityDecompositionRecord`, `Claim`, domain-evidence or PC-AEP records, action specification, `ExecutionMandateRecord`, `ExecutionAuthorization`, qualification snapshot, active controls, and requalification state. It SHOULD reference source object IDs and content hashes where available rather than duplicate governing facts.

### Missing-field and mismatch behavior

If a material field is unknown, stale, contested, incomplete, or inconsistent with the frozen action or qualification snapshot, the view MUST display the applicable existing MathGov disposition rather than infer completion. Available dispositions include narrowed claim, advisory only, evidence required, contested, requalification required, escalation, refusal, or block.

When `computational_system_material` is true and the run has reached authority or execution review, a current Computational Context Declaration MUST be present. If the exact architecture/configuration, demonstrated capability, assigned task, deployment domain, required evidence standard, consequence interface, or authority source no longer matches the frozen qualification surface, an approved execution state MUST NOT be serialized until the affected stages are requalified.


## 8.4 Required object minimum

A full conforming structured run MUST include at least a DecisionRun, one or more Options, a ConfigurationRecord, TierAssessmentRecord, Claims, EvidenceItems, material Assumptions and Unknowns, StakeholderInstances, GateRecords, ReviewerJudgments, a DecisionStateRecord, InteractionEvents, and GeneratedViews appropriate to its tier and stage.


# 9. Workflow and state orchestration

## 9.1 Primary lifecycle

`DRAFT -> SCOPING -> TIER_ASSESSMENT -> EVIDENCE_COLLECTION -> RG_REVIEW -> RF_REVIEW -> TRC_REVIEW -> CSV_REVIEW -> SELECTABLE_SET_FORMED -> RLS_REVIEW -> FRAMEWORK_RESULT -> AUTHORITY_REVIEW -> EXECUTION_AUTHORIZATION -> ACTIVE_MONITORING -> CLOSED`

## 9.2 Non-linear states

The run MAY enter `NARROWED`, `DELAYED`, `REDESIGN_REQUIRED`, `ESCALATED`, `REFUSED`, `NO_SELECTABLE_OPTION`, `EMERGENCY_PROVISIONAL`, `REQUALIFICATION_REQUIRED`, `REOPENED`, or `SUPERSEDED` as defined by controlling MathGov rules.

## 9.3 Short-circuit rule

When an option fails an earlier option-rejecting gate, later governing gate states MUST be `NOT_EVALUATED_AFTER_PRIOR_FAILURE` or the controlling canonical equivalent. Later calculations MAY be performed for learning or audit but MUST be separately labeled and MUST NOT change the formal run state.

## 9.4 State-transition event

Every material transition MUST create an InteractionEvent identifying actor, role, timestamp, prior state, new state, target object, reason, and content hashes where applicable.

## 9.5 Concurrency, freeze, branching, and merge

### 9.5.1 Optimistic concurrency

Each mutable object MUST expose a revision number or equivalent entity tag. A material update based on a stale revision MUST create a conflict rather than silently overwrite a newer value. Last-write-wins behavior is prohibited for evidence, judgments, tiers, gate states, calculations, authority, controls, redaction, and public claims.

### 9.5.2 Conflict resolution

A conflict record SHOULD show the common base, both proposed versions, affected dependencies, reviewers, and available dispositions: accept one, merge with rationale, retain both on separate branches, or escalate. A conflict remains `UNRESOLVED` until an accountable reviewer records a disposition.

### 9.5.3 Branch authority

Every branch MUST identify its parent, branch purpose, owner, frozen base, and status. Only one branch may be designated `CURRENT_GOVERNING` for a declared decision and authority context. Comparative, exploratory, and audit branches MUST be labeled non-governing.

### 9.5.4 Merge semantics

A merge MUST preserve source versions, conflicting judgments, challenge history, hashes, and the rationale for the merged result. Material challenges that predate a branch point remain attached to every descendant branch unless explicitly resolved with branch-specific reasoning.

### 9.5.5 Post-result change

Material changes after a framework result create a revision branch or a new run. They MUST NOT be represented as uninterrupted continuation of the frozen evaluation.

## 9.6 Requalification

Material change to configuration, evidence, controls, authority, environment, stakeholders, model behavior, incident status, or validity envelope MUST create or activate a RequalificationTrigger. The system SHOULD reopen only affected stages but MUST reopen every stage materially dependent on the change.

### 9.6A Successor and material-change requalification

A `SuccessorRequalificationRecord` MUST be created when a system is derived, retrained, fine-tuned, composed, scaffolded, self-modified, replaced, or otherwise changed beyond the currently qualified envelope. The record MUST preserve parent and candidate configuration identities; technical lineage; generation depth; capability, autonomy, tools/infrastructure, objective/policy, evaluation-validity, control-assumption, risk-pathway, and requested-authority deltas; evidence proposed for reuse and its validity basis; creator identity; an independent reviewer; candidate-lock state; rollback boundary; requalification disposition; and any fresh candidate-bound execution authorization.

A candidate MAY reuse evidence after its validity domain is demonstrated, but it MUST NOT reuse permission by default. If evaluation validity has expired, the candidate MUST be narrowed, staged, independently tested, or refused until the missing assurance is restored. If evaluation, verification, monitoring, containment, or correction capacity cannot keep pace with a material capability change, MHIOS MUST block authority expansion rather than silently carry the old approval forward.


## 9.7 Evidence freshness and staleness

MHIOS does not impose a universal time-decay formula. Evidence freshness depends on claim type, domain volatility, configuration change, source update frequency, legal or standards change, and incident history.

Each gate-material EvidenceItem SHOULD identify a freshness policy, last verification date, next review date or event trigger, and staleness status. A stale item may remain historically relevant but MUST NOT support a current strong claim without a documented reviewer disposition. An expiry or material contradiction creates a RequalificationTrigger for dependent claims and stages.

# 10. Record generation and synchronization

## 10.1 Many views, one source

The system MAY generate a Decision Note, gate and grounding records, stakeholder record, PC-AEP, MFDI record, Source-Coupling record, Rights Floor record, TRC report, CSV report, RLS report, Authority Selection Record, Execution Authorization, monitoring plan, public summary, and audit package from one shared graph. A PCC MAY be labeled tier-complete only under Section 8.0E; otherwise it is a partial generated view with explicit missing-record disclosure.

## 10.2 Traceability requirement

Every rendered statement that affects gate status, selection, authority, execution, or public claim strength MUST be traceable to one or more source objects and a controlling rule.

## 10.3 Synchronization requirement

A generated view MUST be regenerated or marked stale when a source object changes. The system MUST NOT display a stale generated view as current without a visible warning.

## 10.4 Editable-view restriction

If a generated document can be edited outside the system, imported changes MUST NOT silently overwrite source objects. Import MUST show a diff, identify changed claims and fields, require human confirmation, and create new versions, amendments, or challenges.

## 10.5 Public transparency view

A public view SHOULD disclose the decision question, options, affected stakeholders, major evidence and unknowns, gate results, reasons, controls, monitoring, authority, and challenge route, subject to lawful and ethical redaction.

## 10.6 Redaction provenance

Redaction MUST create a record identifying the source object or field withheld, reason, authority, date, and review or expiry where appropriate.

## 10.7 Generated-view status

Every view MUST be one of `CURRENT`, `STALE_SOURCE_CHANGED`, `SUPERSEDED`, `DRAFT`, or `REDACTED_PUBLIC_VIEW`. A stale view cannot support a current conformance or authorization claim.


## 10.8 Graph-aware redaction and inference review

Field-level suppression is insufficient when retained relationships, counts, identifiers, timestamps, or dependency edges allow a reasonable reader to reconstruct protected content.

Before a public or cross-boundary export, the system SHOULD perform an inference-risk review covering:

- direct identifiers and quasi-identifiers;
- relationship and dependency edges;
- unique combinations of remaining facts;
- counts and timing information;
- filenames, hashes, comments, metadata, and object identifiers;
- conclusions that reveal the withheld premise.

A GeneratedView intended for public release MUST record whether inference-risk review was completed, what edges or derived facts were suppressed, and the residual disclosure risk. Redaction MUST NOT create a misleading account of why a gate, refusal, or authority decision occurred.

# 11. Narrative evidence and typed interpretation

## 11.1 Dual-layer rule

Qualitative evidence MUST be preservable as narrative and context even when the system also requires structured fields.

## 11.2 SGP application

For SGP, the system SHOULD preserve an SGPEvidenceNarrative containing observations, testimony, source excerpts, context, alternative interpretations, and uncertainty. A separate SGPTypedInterpretation records the relevant register, status, evidence strength, what follows, what does not follow, reviewer, challenge status, and revision trigger.

## 11.3 No-erasure rule

Typed interpretation MUST remain traceable to the preserved narrative and MUST NOT erase ambiguity, disagreement, or limitations in the source.

## 11.4 Free-text boundary

Free text is permitted and often necessary. An untraceable free-text override that changes a status, threshold, stakeholder, authority, or execution result is prohibited.

## 11.5 Orchestration support

The interface SHOULD help users map narrative evidence to candidate fields while showing that the mapping is an interpretation requiring review, not an extraction of moral truth.

## 11.6 Narrative/version integrity

When a typed interpretation changes, the system MUST preserve the prior interpretation, reviewer, rationale, and source narrative version. Reclassification MUST NOT rewrite the historical observation.


# 12. Anti-audit-theater detection

The system SHOULD detect patterns that suggest formal completion without substantive grounding. Detection creates a challenge or sampling trigger, not an automatic accusation or proof of assurance. Pattern visibility can itself create evasion pressure, so the engine MUST be evaluated against adversarial hollow runs and supplemented by human review.

## 12.0A Record-quality and evidence-linkage patterns

| ID | Pattern | Signal | Required response |
| --- | --- | --- | --- |
| AT-01 | Generic rationale repetition | Near-identical rationales appear across materially different options or objects. | Raise a review challenge; require option-specific explanation or justified reuse. |
| AT-02 | Universal low uncertainty | All material uncertainty fields are marked low despite contested, sparse, or extrapolated evidence. | Request evidence basis and route unsupported fields to review. |
| AT-03 | Monitoring presented as prevention | Controls describe observation or reporting but no preventive, limiting, shutdown, rollback, or recovery function. | Classify as monitoring-only and require a true control or explicit residual-risk acceptance. |
| AT-04 | Unexplained NOT_MATERIAL | Repeated NOT_MATERIAL declarations lack trigger-specific rationale. | Require rationale and reviewer sign-off; escalate if gate material. |
| AT-05 | Insider-only stakeholder set | Stakeholder map contains only decision owners, operators, or institutional insiders. | Reopen stakeholder discovery and challenge omission risk. |
| AT-06 | Human oversight without power | Human oversight is named without a person, intervention right, response time, competence, or shutdown authority. | Do not count as a binding control until fields are complete. |
| AT-07 | Evidence without claim linkage | Evidence items exist but support or challenge no material claim. | Require linkage or classify as background/non-decision-material. |

## 12.0B State, tier, authority, and control patterns

| ID | Pattern | Signal | Required response |
| --- | --- | --- | --- |
| AT-08 | Unknown disappearance | A material unknown is present in RG but absent downstream without explicit resolution. | Block claim strengthening and require disposition. |
| AT-09 | AI self-certification | AI-generated content is marked authoritative without named human review or independent evidence. | Revert to advisory status and require human judgment. |
| AT-10 | Tier downgrade pattern | Operators repeatedly select a lower tier despite triggered higher-tier conditions. | Require divergence record, independent approval, and trend review. |
| AT-11 | Routine emergency mode | Emergency-provisional status is repeatedly renewed or used as ordinary operation. | Escalate, require redesign or normal authorization, and review emergency capture. |
| AT-12 | All-pass improbability | Every status passes despite contested evidence, unresolved unknowns, or adverse scenarios. | Challenge evidence and reviewer independence; do not automatically fail. |
| AT-13 | No adverse scenarios | TRC contains no adverse or failure scenarios for a consequential option. | Reopen scenario discovery and challenger review. |
| AT-14 | Control owner missing | A required control has no accountable owner or activation condition. | Control cannot support CSV or execution authorization. |
| AT-22 | Permission-currency theater | Approved execution cites a permission label but omits source, version, scope, effective interval, revocation, supersession, trust, hash, or evaluation time. | Block approval, require a complete mandate record, bind it to the configuration, and rerun authorization. |
| AT-23 | Factor-collapse sufficiency collapse | Admissibility and permission are presented as sufficient authority while legitimate authority, current evidence, control integrity, configuration binding, or conflict standing is omitted. | Restore the complete conjunctive dependency and identify each missing warrant or authority surface. |

## 12.0C Subgroup, staleness, automation, and evasion patterns

| ID | Pattern | Signal | Required response |
| --- | --- | --- | --- |
| AT-15 | Copied subgroup values | Subgroup values or thresholds are reused without identity, evidence, or derivation. | Require derivation and affected-group trace. |
| AT-16 | Policy as physical warrant | Approval, certification, or policy is used as sole evidence of physical or causal admissibility. | Trigger PC-AEP and domain-warrant review. |
| AT-17 | Stale evidence continuity | Expired or materially changed evidence remains linked to current claims without requalification. | Activate requalification. |
| AT-18 | Post-result parameter editing | Weights, assumptions, scope, scenarios, or thresholds change after the result without a revision branch. | Create a new run or branch and mark the prior result superseded. |
| AT-19 | AI suggestion rubber-stamping | Near-universal acceptance of gate-material AI suggestions with little modification, source inspection, or independent first-pass divergence. | Sample for independent review; compare AI-off judgments; inspect task difficulty and reviewer incentives. |
| AT-20 | Warning-disposition boilerplate | Repeated identical explanations or dismissals across materially different anti-theater warnings. | Review alarm fatigue, warning precision, reviewer workload, and substantive adequacy of dispositions. |
| AT-21 | Pattern-aware evasion | Formally varied rationales, token stakeholders, nominal controls, or uncertainty distributions satisfy literal patterns while remaining substantively hollow. | Route to adversarial human sampling and semantic evidence review; include in precision/recall corpus. |

## 12.1 Pattern-engine boundary

Pattern detection is a sampling and review trigger, not assurance. It MUST NOT silently change a gate result or be represented as proof that a run is honest. Structural incompleteness may block a conformance or publishability claim; disputed substantive judgments remain assigned to accountable reviewers.

The pattern registry is intentionally public for challengeability, but publication also creates a Goodhart surface. A motivated actor may vary wording, add token stakeholders, distribute uncertainty values, or describe nominal controls to evade literal rules. The engine therefore SHOULD combine transparent rules with adversarial human review, randomized sampling, semantic comparison, and periodic undisclosed evaluation cases under authorized testing conditions.

## 12.2 Pattern transparency

Each warning SHOULD show the matched evidence, rule, severity, false-positive possibility, and available dispositions: resolve, explain, contest, or escalate.

## 12.3 Institutional trend analysis

Aggregated patterns such as repeated tier downgrades, routine emergency mode, universal low uncertainty, or insider-only stakeholder maps SHOULD be reviewable across runs. Trend analysis MUST respect privacy, purpose limitation, and due process.

## 12.4 No theater score

MHIOS SHOULD NOT collapse all warnings into one opaque “integrity score.” A single score can itself become a gaming target. Patterns should remain inspectable, typed, and linked to evidence.


## 12.5 Precision, recall, and evasion testing

Before claiming anti-theater effectiveness, an implementation SHOULD evaluate the pattern engine against a labeled corpus containing substantive runs, obvious hollow runs, and adversarial hollow runs created by people attempting to evade the published patterns. Report precision, recall, false-positive burden, false-negative severity, and confidence intervals. A clean pattern report does not establish a clean run.

## 12.6 Alarm-fatigue control

The system SHOULD measure warning frequency, repeat warnings, time to disposition, dismissal rate, and repeated boilerplate explanations. If warnings become ubiquitous or routinely receive identical dispositions, the pattern set, thresholds, interface, and reviewer workload require re-evaluation.

## 12.7 Human-review sampling

Pattern detections SHOULD route a risk-proportionate sample to independent or adversarial human review. Runs with no detections may also be sampled so the system can estimate false negatives and avoid treating silence as assurance.

# 13. Calculation, state, and validation integrity

## 13.1 Calculation records

Every material calculation SHOULD produce a CalculationRecord containing formula version, input object IDs and values, engine and version, timestamp, output, units, rounding rule, validation status, and content hash.

## 13.2 Single-source result integrity

A controlling result such as CVaR, RLS, Gap, decisiveness, selectable set, framework verdict, flag counts, or publishability MUST have one authoritative calculation or state source. Dashboards, reports, and exports MUST reference that source rather than duplicate the logic.

## 13.3 Formula transparency

Users and auditors SHOULD be able to inspect the controlling formula and input values. Friendly interfaces MUST NOT obscure the computational path.

## 13.4 Contradiction detection

The validator MUST reject or challenge contradictions such as:

- RLS executed before selectable-set formation;
- a decisive result paired with refusal of deterministic selection;
- an active invalid flag paired with publishable status;
- a later governing gate evaluated after a prior failure;
- authority selection without named authority or mandate;
- execution authorization without required controls;
- AI content marked authorized without human review;
- stale configuration evidence used after a material change;
- generated-view hashes that do not match current source objects;
- a tier downgrade without a divergence record;
- a control treated as preventive when it only monitors;
- an unknown removed without evidence of resolution.

## 13.5 Independent replay

A conforming export SHOULD enable an independent implementation to reconstruct the run state and calculations from frozen inputs, while recognizing that replay does not verify evidence truth or normative legitimacy.

## 13.6 Engine diversity

High-assurance calculations SHOULD be replayed in an independent implementation or engine where feasible. Engine agreement establishes computational consistency only, not validity of inputs or models.

## 13.7 Display-value integrity

Displayed values, exported values, and machine values MUST derive from the same calculation record. Formatting and rounding may differ, but the rule and precision MUST be declared.

Ordinary human-facing surfaces SHOULD render RLS, CVaR, normalized Gap, uncertainty, and derived scores to no more than three decimal places unless additional displayed precision is decision-material and justified. Full precision remains in the `CalculationRecord` and replay trace; a rounded display never becomes the controlling calculation value.


# 14. Security, privacy, and access control

## 14.1 Minimum controls

An MVP SHOULD support role-based access, least privilege, encryption in transit and at rest, append-only audit events, backups, recovery, explicit retention, secure export, and version history.

## 14.2 Separation of sensitive data

The system MUST support separation among identity data, analysis data, privileged review material, public summaries, and security-sensitive control details.

## 14.3 Visibility and sensitivity

Each object SHOULD carry a visibility class and sensitivity class. Access decisions MUST be logged. Public exports MUST NOT expose personal data, protected testimony, privileged legal material, security-sensitive vulnerabilities, or restricted SGP evidence without lawful and ethical authority.

## 14.4 Purpose limitation

Evidence collected for one run SHOULD NOT be reused for unrelated surveillance, performance management, profiling, or model training without explicit lawful authority and disclosure.

## 14.5 AI service boundary

Confidential evidence MUST NOT be transmitted to an external AI service unless the data-handling basis, provider, retention, access, jurisdiction, and security controls are declared and authorized.

## 14.6 Export integrity

Exports SHOULD use deterministic serialization where required, stable identifiers, checksums, schema versions, and signed manifests for high-assurance use.

## 14.7 Security nonclaim

MHIOS conformance does not establish cybersecurity certification. Implementations require independent threat modeling, secure development, testing, monitoring, incident response, and domain-appropriate assurance.

## 14.8 Administrator control

Privileged administrators SHOULD use separate accounts for infrastructure administration and substantive participation. Emergency administrator changes to records or permissions MUST be logged and independently reviewed.

## 14.9 Retention and deletion

Retention rules SHOULD distinguish governing records, evidence, personal data, security logs, public views, and superseded drafts. Deletion of personal data MUST preserve enough non-identifying audit evidence to explain the lawful deletion and its effect on the run.


## 14.10 Legal handling, privilege, and chilling-effect boundary

Governance records may be discoverable or otherwise subject to legal, regulatory, employment, public-records, contractual, or investigative processes. MHIOS does not create legal privilege and MUST NOT label a record privileged without jurisdiction-specific legal authority and counsel.

An organization SHOULD define, before use:

- lawful purpose and authority for each record class;
- privilege or protected-handling claims and their limits;
- retention, deletion, legal-hold, and disclosure rules;
- access boundaries for dissent, legal advice, incidents, and protected testimony;
- how material unknowns and adverse scenarios are recorded without unnecessary personal data or speculative accusation;
- how staff are protected from retaliation for good-faith risk documentation.

Legal-risk concerns MUST NOT be resolved by silently omitting gate-material unknowns, dissent, adverse evidence, or rights exposure. Where complete recording is legally constrained, the run MUST narrow its claim, identify the constraint, and route the matter to authorized legal and governance review.

# 15. Accessibility and usability

## 15.1 Accessibility baseline

The implementation SHOULD support keyboard navigation, screen readers, sufficient contrast, no reliance on color alone, understandable focus order, accessible tables, clear labels, error summaries, and text alternatives for meaningful graphics.

## 15.2 Usability baseline

The system SHOULD support autosave, saved progress, undo, contextual help, plain-language summaries, technical detail on demand, mobile-safe review, and remediation-oriented errors.

## 15.3 Error design

Errors SHOULD identify what failed, why it matters, the controlling rule, the affected result, and how to resolve or contest it. An error message that merely says “invalid” is insufficient for a material state.

## 15.4 Role-specific queues

Users SHOULD see tasks relevant to their role. A rights reviewer should not need to navigate infrastructure controls to find rights exposures; an execution authority should see unresolved controls and validity limits without editing RLS cells.

## 15.5 Terminology assistance

Canonical terms SHOULD be available through tooltips, glossaries, examples, and “why this matters” explanations without forcing users to leave the workflow.

## 15.6 Interruption and resumption

A user SHOULD be able to stop and resume without losing context. The system should show the last material action, unresolved tasks, stale views, and newly reopened requirements.

## 15.7 Accessibility testing

Automated checks are insufficient. Pilot testing SHOULD include users with relevant accessibility needs and report barriers, task-completion differences, and remediation.


# 16. Governance Burden Profile

## 16.1 Status

The Governance Burden Profile is an empirical measurement surface. It is not a gate and MUST NOT determine whether a decision is ethically admissible.

## 16.2 Metrics

In addition to ordinary burden and quality measures, pilots SHOULD report:

- valid-completion time and interaction steps;
- hollow-pass rate and time to hollow detection;
- false-positive challenge burden on legitimate runs;
- hollow-run detection probability, reported as automated, human, union, and overlap measures;
- AI suggestion acceptance, modification, rejection, and source-inspection rates;
- AI-assisted versus AI-off divergence by state family;
- warning frequency, dismissal, and boilerplate-disposition rates;
- object and field usage, including whether each prevented or revealed a material error;
- institutional precondition status and reviewer-time sufficiency.


Implementations SHOULD record total completion time, time by stage, number of human judgments, repeated entries avoided, generated records, reviewer revisions, disagreements, challenges, abandoned runs, tier changes, contradictions detected, stakeholder omissions discovered, fields left unused, operator burden rating, reviewer burden rating, perceived usefulness, replay success, and inter-rater agreement where studied.

## 16.3 Scientific questions

Burden data should test:

- which requirements improve evidence quality, error detection, stakeholder coverage, reviewer agreement, or reconstructability;
- which requirements create work without affecting assurance;
- where users misunderstand questions;
- where automation reduces error;
- where automation creates false confidence;
- whether simplified interfaces preserve decision quality;
- whether users shift runs to lower tiers to avoid burden.

## 16.4 No perverse incentive

Burden metrics MUST NOT be used to reward superficial speed, discourage escalation, penalize users for declaring unknowns, or pressure reviewers to produce passes.

## 16.5 Revision discipline

A future MHIOS version SHOULD remove or simplify requirements shown to be redundant and strengthen requirements shown to prevent material errors or omissions. Changes MUST preserve the evidence and reasoning behind revision.

## 16.6 Minimum pilot dataset

Each pilot run SHOULD record role, tier, domain, stage times, field counts, evidence reuse, number and type of challenges, contradictions caught, user burden ratings, and replay outcome. Personal performance reporting should be minimized and governed.


# 16A. Reviewer agreement and construct-operationalization study

Inter-rater agreement is a central empirical test of whether MHIOS statuses operate as reproducible decision instruments rather than as shared vocabulary.

## 16A.1 Initial study design

Before Core-inclusion consideration, MHIOS SHOULD be tested with approximately 20 trained reviewers across 8-10 heterogeneous retrospective cases. Reviewers should independently assign RG claim-authority status, RF/NCRC, TRC and CSV states, selectable-set membership, and downstream ranking/authority states as applicable before consensus discussion. Primary cases MUST use neutral evidence packets and neutral instructions; training/calibration cases are separate and excluded from the primary analysis. Cases should include clear, borderline, high-uncertainty, rights-material, tail-risk, physical-admissibility, non-material, refusal, `TRC_NOT_TRIGGERED`, pass-with-controls, and non-decisive ranking conditions.

## 16A.2 Reporting

Report observed agreement and confidence intervals by state family. Select statistics appropriate to the scale and prevalence pattern, which may include weighted kappa for ordinal states, Fleiss-type measures for multiple raters, Krippendorff's alpha where missingness or different measurement levels are relevant, and Gwet's AC1/AC2 where prevalence effects make kappa unstable. Do not select the coefficient after seeing which one appears most favorable.

## 16A.3 Interpretation boundary

No single universal cutoff is adopted in v0.8. The study MUST preregister the exact Core/MHIOS builds and case hashes, reviewer eligibility/conflicts, training/calibration materials, case randomization or counterbalancing, primary coefficient, agreement targets, confidence-interval method, handling of missing ratings/attrition, and revision rules. Case authors MUST NOT rate their own primary cases, and unequal mid-study clarification is prohibited. Low agreement that changes gate outcomes, tier assignment, or authorization standing requires definition, training, interface, or evidence-guidance revision even when an aggregate coefficient appears acceptable.

## 16A.4 Publication discipline

Publish disagreement matrices, confidence intervals, difficult cases, training effects, adjudication changes, and unflattering results. Consensus reached after discussion does not substitute for independent agreement measurement.

The complete protocol is defined in `docs/PILOT_AND_INTER_RATER_RELIABILITY_PROTOCOL_v0_8.md`.

# 17. MHIOS conformance levels

## MHIOS-C0 - Conceptual alignment

The implementation presents MathGov in the correct order, distinguishes qualification from ranking, and does not distort the cascade.

## MHIOS-C1 - Structured run

The implementation uses stable objects, canonical states, provenance, generated records, and traceable calculations.

## MHIOS-C2 - Reviewed orchestration

The implementation adds reviewer roles, challenges, tier-divergence controls, AI provenance, contradiction detection, and role separation.

## MHIOS-C3 - Reproducible operational environment

The implementation adds independent replay, complete transition logs, burden metrics, access controls, validated exports, configuration-bound requalification, and full audit reconstruction.

## 17.1 Conformance nonclaim

MHIOS conformance MUST NOT be represented as correctness of the decision, truth of evidence, legal authority, deployment certification, or empirical superiority of MathGov.

## 17.2 Conformance evidence

A conformance claim SHOULD include implementation version, supported level, test results, known deviations, schemas, test vectors, validator output, and date.

The machine-readable level requirements are defined in `registries/MHIOS_CONFORMANCE_PROFILE_v0_8.yaml`. Implementations claiming C1-C3 SHOULD evaluate the highest fully satisfied level and list missing requirements; partial implementation or branding MUST NOT imply a higher level.

## 17.3 Partial conformance

Partial conformance claims MUST identify unimplemented requirements and MUST NOT imply a higher level through branding or visual appearance.

## 17.4 Expiry

A conformance claim SHOULD expire or require reassessment after material implementation change, security incident, schema change, or discovery of a load-bearing validator defect.


# 18. Minimal vertical slice and later MVP boundary

## 18.1 First-build objective

The first empirical build is the **MHIOS Minimal Vertical Slice (MVS-0.1)**, not the full 47-object, 20-screen environment. It tests whether a shared source model can preserve evidence, canonical state routing, human review, calculation, export, and replay with acceptable burden.

## 18.2 MVS-0.1 scope

The first slice uses:

- one bounded Tier 2 retrospective decision;
- 12 core object types: DecisionRun, Option, ConfigurationRecord, Claim, EvidenceItem, MaterialUnknown, StakeholderInstance, GateRecord, ReviewerJudgment, DecisionStateRecord, InteractionEvent, and GeneratedView;
- one conditional `ComputationalClosureRecord`, serialized for the Tier 2 case but generated through the review/export flow rather than exposed as a thirteenth default form;
- five combined screens: Run Setup; Claims/Evidence; Stakeholders/Grounding; Qualify/Rank; Review/Export;
- one transparent calculation path;
- one human-review workflow;
- JSON and human-readable export;
- independent replay;
- no-AI mode as the baseline condition.

A conditional record may be rendered within a core screen for the slice, but it remains a separately typed export object whenever the pinned Core requires that separation.

## 18.3 MVS exclusions

The first slice excludes enterprise identity integration, full SGP orchestration, live execution authorization, autonomous monitoring, production AI assistance, the full anti-theater engine, public deployment claims, and all 20 full-product screens.

## 18.4 MVS acceptance

The slice is suitable for a reviewer pilot only when it can preserve canonical short-circuit states, trace every material conclusion to evidence and a reviewer, export and replay the run, reveal stale or conflicting edits, and operate without AI.

## 18.5 Later full MVP

Only after the slice produces burden, agreement, error, and replay evidence should the project activate conditional objects, specialized profiles, full review queues, anti-theater analytics, monitoring, authority, and optional AI assistance. The later full MVP remains described by the 20-screen registry as a target architecture, not the first implementation mandate.

## 18.6 Local-first and spreadsheet boundary

The slice SHOULD support local or organization-controlled storage. It may import or export spreadsheets for comparison, but spreadsheet cells MUST NOT become the only authoritative state or calculation source.

The detailed profile and five-screen flow are defined in `docs/MHIOS_MINIMAL_VERTICAL_SLICE_PROFILE_v0_8.md` and `wireframes/minimal_vertical_slice.html`.

# 19. MVP screen registry and flow

The 20-screen registry is a later full-product target. It is grouped below to keep the specification readable and to distinguish it from the five-screen minimal vertical slice that must be built and tested first.

## 19.0A Setup, evidence, and grounding target screens

| ID | Screen | Purpose |
| --- | --- | --- |
| SCR-01 | Run Library | Create, import, clone, compare, or open a run; show status and blocking issues. |
| SCR-02 | New Run Wizard | Capture decision identity, options, configuration, materiality prompts, roles, and recommended tier. |
| SCR-03 | Decision Canvas | Show the bounded run, authority, configuration, horizon, tier, and unresolved setup items. |
| SCR-04 | Claim and Evidence Workspace | Link claims, evidence, counterevidence, assumptions, unknowns, MFDI, and source coupling. |
| SCR-05 | Stakeholder Discovery | Build the Local Stakeholder Set, scope mappings, rights candidates, omissions, and challenge opportunities. |
| SCR-06 | Ground Workspace | Complete reality surface, evidence trace, unknowns, transition, consequences, claim boundary, and triggered profiles. |

## 19.0B Qualification and ranking target screens

| ID | Screen | Purpose |
| --- | --- | --- |
| SCR-07 | Qualify Overview | Display RG -> RF/NCRC -> TRC -> CSV with statuses, reviewers, missing evidence, and reopen triggers. |
| SCR-08 | Rights Floor | Review floor, categorical, severe-hazard, subgroup, and protected-cell channels. |
| SCR-09 | Tail-Risk Constraint | Discover scenarios, assign probability bounds, classify severity/irreversibility, calculate CVaR, and review uncertainty. |
| SCR-10 | CSV | Review current state, transition, post-state, controls, dependencies, reversibility, monitoring, authority, and UCI/HOI where material. |
| SCR-11 | Selectable Set | Show option gate history and separate governing states from audit-only calculations. |
| SCR-12 | Rank | Display the 7x7 field, impacts, weights, PLSS, uncertainty, RLS, sensitivity, and decisiveness. |
| SCR-13 | Framework Result | Show selectable options, ranking, Gap, decisiveness, framework verdict, and unresolved reviews. |
| SCR-20 | Emergency Rights Comparison | Render the Canon emergency rights-priority tuples, comparison trace, challenger status, remediation, expiry, and return-to-normal conditions without ordinary pass or RLS language. |

## 19.0C Authority, operations, audit, and export target screens

| ID | Screen | Purpose |
| --- | --- | --- |
| SCR-14 | Authority Selection | Record authority, mandate, available options, framework result, selected option, basis, conflicts, and departures. |
| SCR-15 | Execution Authorization | Confirm configuration binding, current mandate records, controls, preconditions, warrants, evidence currency, monitoring, shutdown, rollback, authority, conflicts, and requalification triggers. |
| SCR-16 | Monitor | Track controls, incidents, evidence expiry, configuration drift, outcomes, and triggered reopening. |
| SCR-17 | Review and Challenge | Manage disagreements, appeals, stakeholder challenges, tier disputes, AI fields awaiting review, and theater warnings. |
| SCR-18 | Audit View | Provide read-only reconstruction of objects, versions, transitions, calculations, overrides, AI contributions, and hashes. |
| SCR-19 | Export | Generate canonical JSON, PCC, gate reports, authority/execution records, public summary, and validation package. |

## 19.0 Minimal vertical slice five-screen flow

| MVS screen | Combined function |
| --- | --- |
| MVS-01 Run Setup | Decision, options, configuration, tier declaration, roles, and freeze. |
| MVS-02 Claims and Evidence | Claims, sources, assumptions, unknowns, and reviewer first pass. |
| MVS-03 Stakeholders and Grounding | Stakeholder discovery, reality surface, claim boundary, and RG state. |
| MVS-04 Qualify and Rank | RF/NCRC, TRC, CSV, selectable set, one transparent RLS calculation, and short-circuiting. |
| MVS-05 Review, Export, and Replay | Reviewer judgment, framework result, challenge, JSON/report export, and independent replay. |

The 20-screen registry remains a later full-product target. The first build SHOULD not expose screens or records that are not needed by the selected retrospective case.

## 19.1 Persistent status bar

Every working screen SHOULD display run ID, run version, tier, configuration, current stage, blocking issues, unresolved unknowns, active challenges, save status, and last material change.

## 19.2 Screen-level rules

Each screen MUST expose the source objects it creates or modifies, the required reviewer, the controlling rule, and whether the screen is displaying a governing result, advisory result, or audit-only calculation.

## 19.3 New Run Wizard flow

1. Decision identity and purpose.
2. Options, baseline, delay, redesign, or no-action comparator.
3. Configuration and validity envelope.
4. Materiality prompts.
5. Trigger-derived tier recommendation.
6. Role assignment and conflict declarations.
7. Run freeze or draft continuation.

## 19.4 Claim and evidence flow

Claims are created independently from evidence so a source cannot silently define the proposition it is supposed to support. Evidence can support, challenge, or contextualize multiple claims. The interface MUST show unlinked evidence and unsupported claims.

## 19.5 Stakeholder flow

The system prompts for direct, indirect, future, non-consenting, vulnerable, ecological, and difficult-to-observe stakeholders. A reviewer can challenge omissions and reopen the Local Stakeholder Set.

## 19.6 Qualify flow

The Qualify Overview displays RG, RF/NCRC, TRC, and CSV. A stage card shows status, role, reviewer, missing evidence, constraint reason, required action, unresolved challenge, constitutive controls where applicable, and reopen trigger. RLS remains locked until the selectable set exists.

When the run enters the Canon RF/NCRC emergency pathway, the Emergency Rights Comparison screen MUST render the complete right-priority order `[LIFE, BODY, ECOL, LBTY, NEED, DIGN, PROC, INFO]`, component order `categorical -> severe risk -> floor depth`, every candidate's violation tuple, the resolving coordinate, unknown fields, challenger status, mitigation, appeal and remedy, expiry, and return-to-normal conditions. It MUST NOT label the provisional result `RF_PASS`, ordinary selectability, or RLS selection.

The Rank and Framework Result screens MUST display a prominent `MPS_HYPOTHESIS_SENSITIVE` banner whenever that Canon flag is present and MUST explain that a single welfare ranking is not claimable across the evaluated inclusion hypotheses.

## 19.7 Rank flow

The Rank screen displays only selectable options, with the 7x7 welfare field, impact instances, evidence per cell, weights, PLSS effects, uncertainty, RLS, sensitivity, Gap, and decisiveness. Every score MUST be traceable to evidence and judgments.

## 19.8 Authority and execution flow

The Authority Selection screen records named authority, mandate, options, framework result, selection, basis, conflicts, departure rationale, and conditions. The Execution Authorization screen separately verifies the selected option, exact action instance, action-specification hash, qualification-snapshot hash, exact configuration binding, current scoped and versioned mandate records, control and precondition checks, warrants, evidence currency, monitoring, shutdown, rollback, named authority, unresolved conflicts, and requalification triggers. It MUST display the frozen authorization-evaluation time and mandate-snapshot hash. It MUST NOT present `APPROVED` or `APPROVED_WITH_CONTROLS` when any load-bearing mandate, control, precondition, evidence, configuration, action binding, qualification snapshot, or conflict check is invalid or unresolved.

### 19.8A Candidate-successor execution boundary

The Authority and Execution surface MUST display parent identity, candidate identity, generation depth, candidate-lock status, evaluation-validity disposition, requested authority delta, and independent reviewer. A successor remains a candidate artifact until: its exact configuration is recorded; the lineage and material deltas are complete; generation depth is within the authorized bound; reused evidence remains valid; affected RG, RF/NCRC, TRC, and CSV records are reopened; and a fresh mandate and `ExecutionAuthorization` are bound to the candidate.

A parent, candidate, descendant, or automated evaluator MUST NOT be the sole reviewer of its own lineage record. Competitive pressure, expected performance gains, or improved results after removing oversight do not create authority.

## 19.9 Monitoring flow

Monitoring tracks control status, incidents, evidence expiry, configuration drift, successor lineage, generation depth, candidate-lock status, evaluation-validity expiry, changed stakeholders, environmental change, observed outcomes, and requalification triggers. A material trigger creates `REQUALIFICATION_REQUIRED` and identifies stages to reopen.

## 19.10 Review and challenge flow

Open challenges are visible to affected reviewers and authorities. A challenge cannot be closed without a recorded disposition and rationale. Appeals should be assigned independently where feasible.

## 19.11 Export flow

The user selects audience and redaction profile. The system generates the view, runs validation, calculates a hash, records source-object versions, and marks any prior view stale.


# 20. MVS-0.1 acceptance criteria

The first vertical slice is acceptable for pilot use when it demonstrates all of the following:

1. Six to ten representative reviewers can complete the same Tier 2 retrospective case without editing a spreadsheet.
2. The 12-object core plus the Tier-2 `ComputationalClosureRecord` are sufficient to reconstruct the bounded case; any other triggered conditional object is serialized or the run is explicitly incomplete.
3. Evidence is entered once and reused across grounding, qualification, ranking, and export.
4. The reviewer records an independent first pass before any gate-material AI suggestion is shown; the baseline study operates with AI disabled.
5. RLS remains unavailable until a selectable set is formed.
6. An earlier gate failure produces `NOT_EVALUATED_AFTER_PRIOR_FAILURE` for later governing stages.
7. Every material status identifies evidence, controlling rule, and named reviewer.
8. A stale concurrent edit produces a visible conflict rather than silent overwrite.
9. A material evidence expiry or configuration change reopens the correct dependency chain.
10. JSON and human-readable exports are synchronized and independently replayable.
11. A public-view test performs graph-aware inference review, not field suppression alone.
12. The package reports artifact integrity separately from construct validity.
13. Normative coverage and mutation-test reports are generated.
14. The pilot preregisters burden, agreement, hollow-run detection, and revision targets.
15. Adverse results, abandoned tasks, disagreement, and removed requirements are publishable outputs rather than hidden failures.

The full-product acceptance criteria remain a later design target and should be activated only after the MVS demonstrates that added objects and screens earn their burden.

# 21. Conformance-test programme

## 21.1 Positive vectors

The package includes positive vectors for a low-stakes Tier 1 procurement choice, a Tier 2 remote-work policy, a Tier 3 autonomous-shuttle pilot, an emergency-rights comparison, and a locked candidate-successor requalification case. Positive vectors demonstrate structure, not evidence truth.

## 21.2 Negative vectors

The package includes negative vectors for missing human review of AI content, RLS-before-selectable-set, silent tier downgrade, unknown disappearance, missing control owner, authorization collapse, contradictory decisiveness, expired and future permission, revoked permission, permission-source mismatch, inactive required controls, unsatisfied preconditions, and missing configuration binding, successor authority inheritance, missing successor records, excessive generation depth, non-independent review, and candidate unlocking without authorization.

## 21.3 Validator scope

The supplied validator checks structural fields, identifiers, declared states, selected invariants, and JSON Schema conformance. It does not verify whether evidence is true, probabilities are justified, rights judgments are legitimate, engineering warrants are valid, or authorities are lawful.

## 21.4 Required future tests

Future versions should add full state-transition replay, deeper jurisdictional conflict resolution, consent/delegation chains, adversarial signature and trust-store tests, redaction tests, role-separation tests, event-log replay, cross-engine calculation replay, representative-user accessibility testing, security testing, and empirical burden studies. The v0.8 execution-mandate and successor-integrity tests establish structural and temporal enforcement only; they do not determine whether an authority, instrument, signature, jurisdictional interpretation, or permission is legally valid.

## 21.5 Adversarial development

Every load-bearing rule should have at least one test that intentionally violates it. A verifier is not adequate merely because all supplied examples pass.

## 21.6 Normative coverage ratio

The release MUST report the number and proportion of atomic `MUST`/`MUST NOT` modal clauses linked to at least one executable check. Each uppercase modal occurrence is a separate coverage unit; independently testable modal clauses MUST be recorded separately. Every clause without executable linkage MUST receive an explicit disposition such as `MANUAL_AUDIT`, `EMPIRICAL_TEST_REQUIRED`, `LEGAL_OR_DOMAIN_DEPENDENT`, `NOT_MACHINE_TESTABLE`, or `UNIMPLEMENTED_CHECK`, with a reason. Report total clauses, machine-eligible clauses with direct/partial coverage, and non-machine dispositions by category; the total raw ratio MAY remain as an honesty metric but MUST NOT be presented alone. A linked test may establish only structural or syntactic coverage. The ledger MUST state whether semantic, empirical, legal, or domain validity remains untested. Coverage is an honesty measure, not a quality score.

## 21.7 Mutation testing

The release SHOULD mutate load-bearing examples or configuration surfaces one rule at a time and confirm that at least one relevant test fails. Report mutants generated, mutants killed, surviving mutants, and excluded rules with reasons. A 100% mutation score on a small seeded set does not establish complete assurance.

## 21.8 Reflexive anti-theater review

A package in which every seeded check passes MUST still report untested requirements, construct-validity gaps, adverse design hypotheses, and the absence of real-user disagreement data. `ARTIFACT_INTEGRITY_PASS` is compatible with `CONSTRUCT_VALIDITY_UNTESTED`.



# 22. Pilot and empirical validation plan

## 22.1 Priority sequence

1. Freeze the original v0.1 design hypothesis as revised and formalized in v0.8 and the self-assessment.
2. Build the five-screen MVS-0.1 with 12 core object types plus the Tier-2 `ComputationalClosureRecord` for one retrospective case.
3. Conduct usability sessions with 6-10 representative reviewers and publish what breaks.
4. Refine definitions and interaction flow without adding optional modules merely to answer criticism.
5. Run the preregistered inter-rater study with approximately 20 reviewers and 8-10 cases.
6. Compare the MVS with current practice and a simpler structured checklist.
7. Add conditional objects or AI assistance only when evidence identifies a specific unresolved failure.

## 22.2 Measures

Measure valid-completion time and interaction steps, field comprehension, reviewer agreement, stakeholder coverage, contradiction detection, challenge resolution, replay success, false reassurance, tier gaming, operator burden, hollow-pass rate, time to hollow detection, false-positive challenge burden, hollow-run detection probability (auto/human/union/overlap), automation-bias indicators, and whether generated records remain synchronized.

## 22.3 Falsification and revision triggers

MHIOS requires revision, narrowing, or removal of requirements when users cannot complete the slice without expert facilitation, the interface hides material unknowns, independent reviewers reach materially different gate states, automation increases omission or commission errors, hollow runs pass much more cheaply than rigorous runs, pattern warnings create alarm fatigue, or an object cannot be linked to a prevented or detected material error.

## 22.4 Publication discipline

Pilot reports SHOULD include adverse outcomes, abandoned runs, disagreement, false positives, false negatives, surviving mutation tests, reviewer complaints, and fields or objects removed for lack of value. A polished interface and complete package are not evidence of decision improvement.

## 22.5 Comparison conditions

Comparisons should include the organization's current process and a simpler structured alternative. MHIOS should not be evaluated only against unstructured decision-making when the realistic alternative is a mature governance process.

## 22.6 Preregistration

Primary outcomes, agreement statistics, candidate thresholds, missing-data handling, exclusion criteria, AI conditions, hollow-run construction, and revision rules SHOULD be frozen before pilot results are examined.

# 23. Recommended implementation architecture

## 23.1 Suggested MVP stack

- Frontend: React or Next.js with TypeScript.
- Backend: Python FastAPI or TypeScript.
- Database: SQLite for local prototype; PostgreSQL for deployed use.
- Relationship model: relational tables with explicit link tables; graph database only if evidence demonstrates a need.
- Validation: JSON Schema plus MathGov- and MHIOS-specific validators.
- Document generation: structured templates rendered to DOCX, PDF, and HTML.
- Audit events: append-only event table.
- AI assistance: optional adapter, disabled by default.
- Calculation engine: transparent tested functions, not spreadsheet-only logic.

## 23.2 Reference architecture modules

1. Identity and access.
2. Run and object service.
3. Evidence and provenance service.
4. Tier and workflow engine.
5. Calculation service.
6. Review and challenge service.
7. Generated-view service.
8. Monitoring and requalification service.
9. Audit and replay service.
10. Optional AI-assistance adapter.

## 23.3 Build-versus-buy boundary

Commodity functions such as authentication, file storage, encryption, and document rendering MAY use established components. MathGov-specific state routing, formulas, provenance, challenge logic, and claim boundaries SHOULD remain transparent and testable.

## 23.4 Migration

Existing spreadsheets and forms MAY be imported as source data, but import MUST preserve provenance, flag ambiguous mappings, and avoid treating cached values as authoritative calculations.

## 23.5 API boundary

APIs SHOULD use versioned schemas, idempotent writes where practical, explicit conflict handling, stable identifiers, and authenticated actor/role context. Bulk operations MUST preserve per-object provenance.

## 23.6 Event-sourcing boundary

A full event-sourced architecture is optional. The minimum requirement is an append-only audit event stream sufficient to reconstruct material changes and state transitions.


# 24. Development roadmap

## Stage 1 - Self-audit and coverage baseline

Maintain the MHIOS self-assessment, normative coverage ledger, object-justification ledger, and mutation suite. Report artifact verification separately from construct validity.

## Stage 2 - Minimal vertical slice

Build one Tier 2 retrospective case using 12 core objects and five screens. Implement real state routing, one calculation path, conflict handling, export, and replay. Keep AI disabled.

## Stage 3 - Reviewer break test

Place the slice before 6-10 representative reviewers. Record errors, confusion, abandoned tasks, burden, conflicts, missing objects, and replay failures. Remove or simplify requirements that do not earn their cost.

## Stage 4 - Inter-rater and comparator study

Run the preregistered multi-reviewer study across 8-10 cases. Compare current practice, a simpler checklist, and MHIOS. Publish agreement and burden data including adverse findings.

## Stage 5 - Conditional modules

Add specialized objects, institutional workflows, anti-theater sampling, monitoring, or SGP orchestration only to address empirically observed failure modes.

## Stage 6 - Optional AI assistance

Introduce AI only after no-AI baseline performance is known. Apply independent-first-pass controls, acceptance diagnostics, AI-off sampling, source inspection, and human accountability.

## Stage 7 - v0.8 and Core-inclusion review

Revise the standard from evidence. Core inclusion requires demonstrated usability, agreement, reconstructability, institutional preconditions, security evidence, and a clear account of which requirements were removed or retained and why.

## 24.1 Recursive-successor anti-theater patterns

A conforming implementation MUST detect or surface at least the following patterns when the relevant fields exist:

| Pattern | Required response |
| --- | --- |
| Parent authority copied to a candidate | Block; require fresh qualification and Action Binding |
| Candidate operates beyond research envelope | Halt; log; de-escalate; notify named authority |
| Generation depth exceeds the declared maximum | Block further recursive activation |
| Evaluation is stale for the candidate configuration | Mark evidence expired and reopen qualification |
| Parent, creator, or descendant is sole reviewer | Require independent review |
| Oversight removal is justified only by performance gain | Treat removal as a material action change and requalify |
| Candidate identity or lineage is missing | Refuse consequential execution |
| Automated safety-case generation is presented as authorization | Preserve as evidence proposal only; require human authority |

# 25. Final governing rules

1. Enter each material fact once and show it wherever it matters.
2. Preserve original evidence and narrative beneath every typed interpretation.
3. Use plain language at the interaction surface and canonical states underneath.
4. Automate repetition, propagation, calculation, synchronization, and contradiction detection.
5. Preserve human responsibility for evidence interpretation, normative judgment, authority, and refusal.
6. Never let automation certify its own output.
7. Never let interface completion imply evidence truth or deployment readiness.
8. Make tier downgrades, overrides, uncertainty, and authority departures visible.
9. Reopen dependent stages after material change, including successor identity, capability, autonomy, tools, controls, evaluation validity, or authority scope.
10. Never let technical lineage manufacture authority; derivation does not authorize execution.
11. Keep candidate successors locked until independent requalification and exact Action Binding are complete.
12. Measure whether the interface improves assurance rather than assuming that more documentation is better.

> **MHIOS should not make MathGov appear simple by hiding complexity. It should make MathGov usable by presenting the right complexity to the right person at the right time, while preserving the complete evidence, judgment, authority, and audit structure underneath.**


# Appendix A - Identifier conventions

## A.1 Minimal vertical slice core identifiers

| Object | Prefix |
| --- | --- |
| DecisionRun | RUN |
| Option | OPT |
| ConfigurationRecord | CFG |
| Claim | CLM |
| EvidenceItem | EVD |
| MaterialUnknown | UNK |
| StakeholderInstance | STK |
| GateRecord | GATE |
| ReviewerJudgment | JDG |
| DecisionStateRecord | DST |
| GeneratedView | VIEW |
| InteractionEvent | EVT |

## A.2 Conditional-object identifiers

| Object | Prefix |
| --- | --- |
| TierAssessmentRecord | TIER |
| Assumption | ASM |
| CategoryGroundingRecord | CAT |
| ScopeMapping | SCP |
| RightsExposure | RGT |
| Scenario | SCN |
| Control | CTL |
| Dependency | DEP |
| PhysicalCausalAdmissibilityEvidenceProfile | PCAE |
| MethodologicalIntegrityRecord | MDI |
| CapabilityAuthorityDecompositionRecord | CAD |
| SourceCouplingRecord | SRC |
| RLSCellRecord | RLSC |
| WeightRecord | WGT |
| CalculationRecord | CALC |
| Challenge | CHL |
| AuthoritySelectionRecord | AUTH |
| ExecutionMandateRecord | EMR |
| ExecutionAuthorization | EXEC |
| RequalificationTrigger | REQ |
| EmergencyOrderRecord | EMR |
| MaterialObligationRecord | MOB |
| ConsequenceTempoRecord | CTR |
| ResponsibilityContinuityRecord | RCR |
| HumanCompensationLoadRecord | HCL |
| ProjectionPreRegistrationRecord | PPR |
| RefusalRecord | REF |
| ComputationalClosureRecord | CCL |
| CoreRecordAttachment | CRA |
| SuccessorRequalificationRecord | SRR |

## A.3 Advanced and research-object identifiers

| Object | Prefix |
| --- | --- |
| SGPEvidenceNarrative | SGPN |
| SGPTypedInterpretation | SGPI |
| MonitoringSignal | MON |
| OutcomeObservation | OUT |
| BurdenObservation | BUR |

Identifiers SHOULD be opaque, stable, and sufficiently non-semantic to survive label changes. Human-readable labels remain separate fields. Implementations may use UUIDs while displaying the prefixes for readability.

# Appendix B - Generated-view map

| Generated view | Primary source objects |
| --- | --- |
| Decision Note | DecisionRun, Options, ConfigurationRecord, Claims, TierAssessmentRecord |
| Reality Grounding record | Claims, EvidenceItems, Assumptions, MaterialUnknowns, CategoryGrounding, MFDI, Source Coupling, PC-AEP |
| PCC | GateRecords, DecisionStateRecord, ReviewerJudgments, Challenges, CalculationRecords, Authority and Execution records, RefusalRecord, ComputationalClosureRecord, ProjectionPreRegistrationRecord, MaterialObligationRecords, and validated CoreRecordAttachments required by the coverage matrix |
| Rights report | StakeholderInstances, ScopeMappings, RightsExposures, RF GateRecords |
| TRC report | Scenarios, EvidenceItems, CalculationRecords, TRC GateRecords |
| CSV report | Controls, Dependencies, PC-AEP, Source Coupling, CSV GateRecords |
| RLS report | RLSCellRecords, WeightRecords, CalculationRecords, DecisionStateRecord |
| Authority Selection Record | DecisionStateRecord, AuthoritySelectionRecord |
| Execution Authorization | ExecutionAuthorization, Controls, MonitoringSignals, RequalificationTriggers, SuccessorRequalificationRecords |
| Successor Requalification Record | Parent and candidate ConfigurationRecords, delta evidence, independent review, candidate lock, requalification records, and fresh ExecutionAuthorization |
| Public summary | Redacted run, stakeholders, evidence/unknowns, gate results, reasons, controls, monitoring, challenge path |
| Audit package | All source objects, InteractionEvents, schemas, hashes, validator outputs, generated views |

A generated view MUST indicate stale status when any source object changes after generation.


# Appendix C - Permission principles

- Contributors may propose but not authorize.
- Reviewers may assess within their mandate but do not automatically select or execute.
- Decision Authorities may select only among options legally and institutionally available after qualification.
- Execution Authorities may authorize execution only when preconditions and controls are active.
- Auditors are read-only by default.
- System Administrators may maintain infrastructure but not alter substantive records without logged, reviewable authority.
- AI Assistants are advisory and have no decision or execution authority.
- Technical descendants do not inherit the authority of their parent configurations.
- A candidate successor remains locked from consequential execution until fresh qualification and exact authorization.
- Technical descendants do not inherit the authority of their parent configurations.
- A candidate successor remains locked from consequential execution until fresh qualification and exact authorization.
- No user may delete audit history through the normal interface.
- Sensitive-data access MUST follow least privilege and purpose limitation.


# Appendix D - Required v0.8 artifact set

The release package includes:

- the human-readable standard in Markdown, DOCX, and PDF;
- machine-readable object, role, state, full-screen, minimal-slice-screen, provenance, object-justification, and anti-theater registries;
- JSON Schemas for run exports and interaction events;
- the full target screen-flow specification and five-screen Minimal Vertical Slice profile;
- self-assessment and claim-boundary record;
- institutional-preconditions and implementation-integrity profiles;
- security/privacy profile;
- burden-measurement and inter-rater pilot protocols;
- AI-assistance firewall profile;
- implementation roadmap;
- full-target and minimal-slice clickable wireframes;
- Tier 1, Tier 2, and Tier 3 synthetic example runs;
- positive and negative conformance vectors;
- structural validation, normative-coverage, and seeded-mutation test scripts;
- release manifest, artifact validation report, normative coverage report, mutation report, and SHA-256 ledger.

# Appendix E - Research and methodological references

The following references inform v0.8 safeguards and pilot design. Their inclusion does not establish that MHIOS itself is validated.

- Haynes, A. B., et al. (2009). A Surgical Safety Checklist to Reduce Morbidity and Mortality in a Global Population. *New England Journal of Medicine*, 360, 491-499. [DOI 10.1056/NEJMsa0810119](https://doi.org/10.1056/NEJMsa0810119)
- Urbach, D. R., et al. (2014). Introduction of Surgical Safety Checklists in Ontario, Canada. *New England Journal of Medicine*, 370, 1029-1038. [DOI 10.1056/NEJMsa1308261](https://doi.org/10.1056/NEJMsa1308261). This population-level study found no significant mortality or complication reduction after implementation, supporting MHIOS's rule that checklist structure is not evidence of implementation effectiveness.
- Bainbridge, L. (1983). Ironies of Automation. *Automatica*, 19(6), 775-779. [DOI 10.1016/0005-1098(83)90046-8](https://doi.org/10.1016/0005-1098(83)90046-8). This classic analysis motivates preserving human capability, intervention authority, and practice for abnormal conditions.
- W3C. (2024). Web Content Accessibility Guidelines (WCAG) 2.2, W3C Recommendation, 12 December 2024. [WCAG 2.2](https://www.w3.org/TR/WCAG22/).
- Parasuraman, R., & Riley, V. (1997). Humans and Automation: Use, Misuse, Disuse, Abuse. *Human Factors*, 39(2), 230-253. [DOI 10.1518/001872097778543886](https://doi.org/10.1518/001872097778543886)
- Skitka, L. J., Mosier, K. L., & Burdick, M. (1999). Does automation bias decision-making? *International Journal of Human-Computer Studies*, 51(5), 991-1006. [DOI 10.1006/ijhc.1999.0252](https://doi.org/10.1006/ijhc.1999.0252)
- Skitka, L. J., Mosier, K. L., & Burdick, M. (2000). Accountability and automation bias. *International Journal of Human-Computer Studies*, 52(4), 701-717. [DOI 10.1006/ijhc.1999.0349](https://doi.org/10.1006/ijhc.1999.0349)
- Gwet, K. L. (2008). Computing inter-rater reliability and its variance in the presence of high agreement. *British Journal of Mathematical and Statistical Psychology*, 61(1), 29-48. [DOI 10.1348/000711006X126600](https://doi.org/10.1348/000711006X126600)
- Hughes, J. (2021). krippendorffsalpha: An R Package for Measuring Agreement Using Krippendorff's Alpha Coefficient. *The R Journal*, 13(1), 413-425. [DOI 10.32614/RJ-2021-046](https://doi.org/10.32614/RJ-2021-046)

- Field, S., Douglas, R., & Krueger, D. (2026). AI Researchers' Views on Automating AI R&D and Intelligence Explosions. *arXiv:2603.03338*. [Preprint](https://arxiv.org/abs/2603.03338)
- METR. (2026). *Task-Completion Time Horizons of Frontier AI Models*. Updated 8 May 2026. [Project page](https://metr.org/time-horizons/)
- Wen, J., Qiu, L., Benton, J., Kirchner, J. H., & Leike, J. (2026). *Automated Weak-to-Strong Researcher*. Anthropic Alignment Science Blog. [Report](https://alignment.anthropic.com/2026/automated-w2s-researcher/)
