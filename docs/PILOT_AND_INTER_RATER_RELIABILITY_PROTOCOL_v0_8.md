# MHIOS Pilot and Inter-Rater Reliability Protocol v0.8

**Status:** preregistration-ready research protocol. This protocol tests reproducibility and burden; it does not establish construct validity, ethical truth, legal validity, or deployment assurance.

## 1. Exact study identity

Before data collection, record and freeze: exact MHIOS build/hash, exact MathGov Core build/hash, case-packet hashes, rater instructions, training materials, primary outcomes, analysis code/version, and all exclusions. Any post-freeze change is logged and either triggers a new study version or is treated as a documented deviation.

## 2. Phase 1: reviewer break test

Use 6-10 representative reviewers on one retrospective Tier 2 case. Capture task completion, assistance requests, abandoned steps, errors, burden, and replay success. Screen recording or structured observation is used only where lawful and consented. This phase is formative and excluded from the primary agreement analysis.

## 3. Phase 2: independent agreement study

Use approximately 20 independently trained reviewers across 8-10 heterogeneous cases. Evidence packets and neutral instructions are frozen before rating. Primary packets MUST contain evidence and task instructions only: no predicted state, intended answer, "likely stress" language, expected refusal, hidden teaching cue, or explanation of what interpretive error the case is designed to expose.

Training/calibration cases are separate from blind primary cases. Calibration keys may be shown only after the reviewer has independently completed the calibration exercise. Calibration cases are excluded from the primary reliability dataset.

## 4. Reviewer eligibility and independence

Preregister inclusion/exclusion criteria, relevant expertise, prior MathGov/MHIOS exposure, conflicts of interest, and training completion. Case authors MUST NOT rate their own primary cases. The MathGov/MHIOS author SHOULD NOT adjudicate primary ratings where an independent non-author lead is feasible. No reviewer receives unequal mid-study clarification; ambiguities are logged for post-lock analysis. Attrition and missing ratings are reported.

## 5. Architecture-preserving rating targets

Do not use generic "gate-state" language. Rate separately:

1. RG claim-authority status and claim boundary;
2. RF/NCRC option-rejecting state;
3. TRC state;
4. CSV state, including control dependence;
5. selectable-set membership;
6. RLS/ranking and decisiveness where applicable;
7. authority-selection state and execution/authorization state where the case reaches them.

RG refusal means insufficient warrant at the requested claim strength; it is not an ethical condemnation of the option.

## 6. Prespecified case-mix matrix

The primary corpus SHOULD include enough variation to avoid trivial agreement from never-triggered states. Prespecify representation of: ordinary survivor ranking, genuine unknown/underdetermination, `TRC_NOT_TRIGGERED`, rights failure, TRC failure/escalation, CSV pass-with-controls/redesign, non-material conditions, refusal, physical-admissibility questions, and non-decisive RLS/authority-routing cases.

## 7. Primary and sensitivity statistics

Select the primary coefficient before observing study results. Report observed agreement and confidence intervals by state family. Weighted kappa may be used for ordinal states; Krippendorff alpha where missingness or mixed measurement levels require it; Gwet AC1/AC2 as a preregistered sensitivity analysis where prevalence destabilizes kappa. Do not select the coefficient after seeing which appears most favorable.

Also report disagreement matrices, consequential state flips, missing-rating patterns, and case-level heterogeneity.

## 8. Randomization and counterbalancing

Preregister case order randomization or counterbalancing. Where interface variants or AI/no-AI conditions are compared, randomize or counterbalance condition order when practical and record deviations.

## 9. Burden and hollow-run measures

Use the current `BURDEN_MEASUREMENT_PROTOCOL_v0_8.md`: valid-completion burden, hollow-pass rate, time to hollow detection, false-positive challenge burden, HRDP set-union measures, and item-level burden scales. Legacy RHER is exploratory only under comparable completion states.

## 10. Automation study

After the no-AI baseline, compare independent-first-pass AI assistance with no-AI conditions. Measure omission and commission errors, source inspection, acceptance without modification, state divergence, confidence, burden, and automation-related false reassurance.

## 11. Missingness, attrition, and deviations

Preregister how missing ratings, partial completions, reviewer withdrawal, excluded cases, corrupted packets, and protocol deviations are handled. Do not silently drop difficult cases.

## 12. Revision rules

Low agreement that changes RG claim authority, gate outcome, tier, selectability, deterministic-selection status, authority standing, or execution standing is a material finding. Before changing the framework, classify whether the cause is ambiguous evidence, ambiguous definition, interface failure, inadequate training, case contamination, or a genuine unresolved judgment surface.

## 13. No universal cutoff

v0.8 does not adopt a universal 0.6 threshold or any universal pass/fail reliability coefficient. Targets and material-state-flip tolerances are preregistered for the study and interpreted with uncertainty.

## 14. Publication

Publish the frozen protocol, case hashes where disclosure is safe, analysis plan, adverse results, abandoned cases, low agreement, false positives, false negatives, consequential disagreements, protocol deviations, and requirements removed or demoted. A failed reliability study is evidence about MHIOS, not an embarrassment to be hidden.
