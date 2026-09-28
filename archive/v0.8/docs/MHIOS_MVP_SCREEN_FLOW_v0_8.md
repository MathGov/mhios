# MHIOS MVP Screen Flow v0.8

**Status:** Candidate interaction specification  
**Relationship:** Implements MHIOS v0.8 without changing MathGov semantics.


## First-build boundary: Minimal Vertical Slice

The first implementation is not the full 20-screen target. It uses five combined screens and 12 core objects for one Tier 2 retrospective case:

| ID | Screen | Purpose |
| --- | --- | --- |
| MVS-01 | Run Setup | Decision, options, configuration, tier, roles, institutional preconditions, and frozen branch. |
| MVS-02 | Claims and Evidence | Claims, sources, assumptions, unknowns, evidence freshness, and reviewer first pass. |
| MVS-03 | Stakeholders and Grounding | Stakeholder discovery, reality surface, claim boundary, and RG state. |
| MVS-04 | Qualify and Rank | RF/NCRC, TRC, CSV, short-circuiting, selectable set, and one transparent RLS path. |
| MVS-05 | Review, Export, and Replay | Judgment, challenge, framework result, synchronized export, and independent replay. |

The 20-screen catalogue below remains a later full-product target. Conditional screens should be added only when pilot evidence shows that they address a material failure mode.

## Persistent navigation

Runs | Decision | Ground | Stakeholders | Qualify | Rank | Authorize | Monitor | Review | Export | Settings

## Persistent status bar

Run ID | Version | Tier | Configuration | Current Stage | Blocking Issues | Unresolved Unknowns | Active Challenges | Save Status

## Screen catalogue

| ID | Screen | User objective | Primary source objects |
| --- | --- | --- | --- |
| SCR-01 | Run Library | Find, create, import, clone, compare, or replay runs. | DecisionRun, GeneratedView |
| SCR-02 | New Run Wizard | Create decision identity, options, configuration, roles, triggers, and tier. | DecisionRun, Option, ConfigurationRecord, TierAssessmentRecord |
| SCR-03 | Decision Canvas | Understand the bounded run and unresolved setup. | DecisionRun, Option, ConfigurationRecord, roles |
| SCR-04 | Claim and Evidence Workspace | Build traceable claims, evidence, assumptions, unknowns, MFDI, and source coupling. | Claim, EvidenceItem, Assumption, MaterialUnknown, MFDI, SourceCoupling |
| SCR-05 | Stakeholder Discovery | Find omission-likely stakeholders and map exposure. | StakeholderInstance, ScopeMapping, RightsExposure, Challenge |
| SCR-06 | Ground Workspace | Establish the reality surface and claim boundary. | GateRecord(RG), Claims, Evidence, Unknowns, CategoryGrounding, PC-AEP |
| SCR-07 | Qualify Overview | See stage status and required actions. | GateRecords, ReviewerJudgments, Challenges |
| SCR-08 | Rights Floor | Review rights channels and subgroups. | RightsExposure, RF GateRecord |
| SCR-09 | Tail-Risk Constraint | Build and test tail scenarios and CVaR. | Scenario, CalculationRecord, TRC GateRecord |
| SCR-10 | CSV | Review structural viability, controls, dependencies, and execution conditions. | Control, Dependency, PC-AEP, CSV GateRecord |
| SCR-11 | Selectable Set | See governing gate history and survivors. | GateRecords, DecisionStateRecord |
| SCR-12 | Rank | Trace 7x7 impacts, weights, uncertainty, RLS, sensitivity, and decisiveness. | RLSCellRecord, WeightRecord, CalculationRecord |
| SCR-13 | Framework Result | Understand the technical result and remaining uncertainty. | DecisionStateRecord |
| SCR-20 | Emergency Rights Comparison | Reconstruct the Canon emergency rights-priority comparison without ordinary-pass or RLS-selection language. | EmergencyOrderRecord, RightsExposure, GateRecord, Challenge |
| SCR-14 | Authority Selection | Record lawful authority judgment and departures. | AuthoritySelectionRecord |
| SCR-15 | Execution Authorization | Verify configuration binding, mandate currency, preconditions, controls, evidence, conflicts, shutdown, rollback, and authority. | ExecutionMandateRecord, ExecutionAuthorization, ConfigurationRecord, Control |
| SCR-16 | Monitor | Track outcomes, incidents, drift, evidence expiry, and requalification. | MonitoringSignal, OutcomeObservation, RequalificationTrigger |
| SCR-17 | Review and Challenge | Resolve disagreements, appeals, theater warnings, and AI fields awaiting review. | Challenge, ReviewerJudgment |
| SCR-18 | Audit View | Reconstruct all provenance, versions, calculations, overrides, and events. | All objects, InteractionEvent |
| SCR-19 | Export | Generate synchronized machine and human views. | GeneratedView, all source objects |

## Screen interaction rules

- Every screen identifies the source objects it creates or changes.
- Every status explains the controlling rule and review owner.
- Governing, advisory, and audit-only results use distinct labels.
- Users can navigate from every material result to evidence and judgment.
- RLS is locked until the selectable set is formed.
- AI suggestions remain visibly labeled until human review.
- A source-object change marks dependent generated views stale.
- Tier divergence, overrides, and authority departures remain visible.

## MVP happy path

1. Create the run and options.
2. Capture configuration and materiality triggers.
3. Accept or challenge the recommended tier.
4. Build claims, evidence, assumptions, unknowns, and stakeholders.
5. Complete Reality Grounding.
6. Complete RF/NCRC, TRC, and CSV for each option in order.
7. Form the selectable set.
8. Rank survivors and evaluate uncertainty.
9. Record the framework result.
10. Record authority selection where necessary.
11. Verify execution preconditions.
12. Monitor and requalify.
13. Export a replay package.

## Failure and challenge paths

- A prior gate failure short-circuits later governing stages.
- Missing evidence can narrow, delay, redesign, escalate, or refuse.
- A stakeholder challenge reopens discovery and affected records.
- A material configuration change reopens dependent stages.
- A tier downgrade requires an explicit divergence record.
- A non-decisive result requires authority handling rather than deterministic selection.

## Detailed flow requirements

### New Run Wizard

The wizard captures decision identity, owner, authority boundary, options including baseline or delay, system configuration, horizon, environment, materiality triggers, recommended tier, selected tier, divergence record, assigned reviewers, and conflict declarations.

### Claim and Evidence Workspace

Claims and evidence remain separate objects. A source may support, challenge, or contextualize several claims. The interface must identify unsupported claims, unlinked evidence, stale evidence, and claims exceeding their validity domain.

### Stakeholder Discovery

Prompts cover direct, indirect, future, non-consenting, vulnerable, ecological, and difficult-to-observe stakeholders. Users can record representation and proxy arrangements. A challenger can allege omission.

### Qualify Overview

The stage card displays canonical status, plain-language meaning, reviewer, evidence and unknowns, blocking reason, required action, and reopen trigger. Later governing stages remain unavailable after prior failure.

### Rank

Only selectable options appear. The user can trace the RLS result through scope/dimension cells, impact instances, evidence, weights, uncertainty, sensitivity, and calculation records.

### Authority and Execution

Authority selection and execution authorization are separate screens and records. An execution authorization cannot be issued without named authority, active required controls, shutdown and rollback responsibility, and current evidence.

### Monitor

Signals are linked to claims, controls, expected ranges, outcomes, and requalification. A material trigger identifies the exact stages and objects that reopen.

### Export

The export workflow selects audience and redaction profile, validates the run, records source-object versions, generates content hashes, and marks previous views stale.
