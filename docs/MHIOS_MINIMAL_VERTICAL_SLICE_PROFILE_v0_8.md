# MHIOS Minimal Vertical Slice Profile v0.8

## Objective

Test the central MHIOS hypothesis with the smallest working system that can preserve evidence, canonical state routing, human judgment, calculation, export, and replay.

## Case and tier

Use one bounded Tier 2 retrospective decision with a known evidence record and at least two plausible options.

## Twelve core objects

DecisionRun, Option, ConfigurationRecord, Claim, EvidenceItem, MaterialUnknown, StakeholderInstance, GateRecord, ReviewerJudgment, DecisionStateRecord, InteractionEvent, and GeneratedView.

Because the case is Tier 2, the export also carries one conditional `ComputationalClosureRecord`. It is generated through the review/export flow and need not become a thirteenth default form, but it remains separately typed in the machine record.

## Five screens

1. Run Setup.
2. Claims and Evidence.
3. Stakeholders and Grounding.
4. Qualify and Rank.
5. Review, Export, and Replay.

## Required functions

- shared source identifiers;
- no silent overwrite;
- canonical short-circuiting;
- one transparent calculation path;
- named reviewer judgments;
- JSON and human-readable export;
- stale-view detection;
- independent replay;
- no-AI baseline mode.

## Exclusions

No production AI, enterprise identity integration, live execution authority, full SGP workflow, autonomous monitoring, or full anti-theater engine.

## Pilot group

Begin with 6-10 representative reviewers. Record task completion, confusion, abandonment, burden, missing objects, agreement, and replay success.
