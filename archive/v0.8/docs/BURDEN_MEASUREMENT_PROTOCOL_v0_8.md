# MHIOS Governance Burden Measurement Protocol v0.8

## Purpose

This protocol measures whether MHIOS reduces avoidable burden while preserving or improving evidence quality, stakeholder coverage, error detection, reviewer agreement, reconstructability, and responsible escalation. It is an empirical research protocol, not a gate.

## Primary outcomes

1. Completion time by stage and role.
2. Repeated entries avoided through object reuse.
3. Number of human judgments and review revisions.
4. Reviewer disagreement and resolution time.
5. Material stakeholder omissions discovered.
6. Contradictions and stale-view defects detected.
7. Run abandonment and stage of abandonment.
8. Recommended tier, selected tier, and divergence frequency.
9. Operator and reviewer burden ratings.
10. Replay success by an independent user or implementation.

## Secondary outcomes

- NOT_MATERIAL frequency and rationale quality;
- unknown visibility downstream;
- clerical time versus substantive-judgment time;
- AI suggestion acceptance, modification, rejection, and error;
- anti-theater false positives and false negatives;
- fields never used in a decision, review, export, or requalification;
- accessibility barriers and task-completion disparity.

## Study design

Use retrospective cases first, then facilitated prospective pilots. Compare MHIOS with current practice and, where feasible, a simpler structured checklist. Randomization is preferable when practical; otherwise use matched cases and state limitations.

## Burden scales

Collect 1-7 ratings with explicit endpoint anchors and preregistered direction. Recommended anchors are: 1 = none/very easy/very low and 7 = extreme/very difficult/very high for burden-negative items (mental effort, navigation difficulty, repetition, uncertainty about the next step); 1 = very low and 7 = very high for positive items (confidence in record completeness, usefulness). Positive-direction items MUST NOT be combined with burden-negative items without preregistered reverse-scoring and evidence that a composite is interpretable. Until measurement behavior is tested, report items separately rather than claiming a validated overall burden score. Subjective ratings do not prove decision quality.

## Safeguards

Burden metrics must not reward speed, discourage escalation, punish declaration of unknowns, or pressure reviewers to pass a run. Identifiable performance data require lawful authority, purpose limitation, data minimization, and privacy controls.

## Analysis plan

Report medians and distributions, not only averages. Stratify by tier, role, domain, experience, and accessibility needs. Examine whether lower completion time is accompanied by more omissions, weaker review, or lower replay success.

## Revision rule

A field or workflow should be considered for removal or simplification when it creates material burden, is rarely used, does not affect assurance, and does not prevent important errors. A requirement should be strengthened when evidence shows that it detects material omissions, contradictions, rights exposure, tail risk, or control failures.

## Operationalized success measures

The first pilot SHOULD keep four questions separate rather than compressing them into one effort ratio.

### 1. Valid completion burden

Report median active time and interaction steps for legitimate, well-evidenced completion, stratified by tier, role, and task type. Lower burden is desirable only when assurance, error detection, unknown visibility, and replay do not worsen.

### 2. Hollow-pass rate

`HPR = seeded hollow runs that reach the prohibited structural passage state / all seeded hollow runs`. Lower is better. A hollow run blocked early is a success, not evidence of poor burden performance.

### 3. Time to hollow detection

Report time and interaction steps from hollow-run start to the first blocking or challenge state. Lower is better, conditional on an acceptable false-positive rate.

### 4. False-positive challenge burden

For legitimate runs, report the proportion receiving unnecessary challenge/block events and the added time/steps caused by those events.

### Hollow-run detection probability

Define detection as a set union rather than double-counting automated and human detections:

`HRDP = |D_auto union D_human| / N_hollow`.

Also report `HRDP_auto = |D_auto| / N_hollow`, `HRDP_human = |D_human| / N_hollow`, and detection overlap `|D_auto intersection D_human| / N_hollow`, together with false-positive rate on legitimate runs.

### Legacy RHER boundary

`RHER_time` and `RHER_steps` MAY be retained only as exploratory descriptors when numerator and denominator refer to comparable completion states. They are undefined when no hollow run reaches the comparison completion state and MUST NOT be the primary first-pilot success criterion. The prior candidate threshold `RHER <= 1.50` is withdrawn pending pilot evidence.

No universal first-pilot success threshold is asserted for HPR, time-to-detection, false-positive challenge burden, or HRDP. Targets, if used, MUST be preregistered for the specific pilot and treated as research hypotheses.

## Object load-bearing analysis

For each object and field, record whether it prevented, detected, clarified, or made reconstructable a material error. Objects with no demonstrated contribution should be combined, demoted, or removed from the default surface.

## Automation and warning measures

Record AI exposure, independent-first-pass completion, source inspection, acceptance/modification/rejection, AI-off divergence, warning frequency, warning precision, false negatives, disposition time, and boilerplate explanations.
