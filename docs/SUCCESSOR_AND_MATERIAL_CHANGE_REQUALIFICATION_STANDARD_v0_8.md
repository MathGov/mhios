# Successor and Material-Change Requalification Standard v0.8

**Status:** Candidate MHIOS companion control  
**Date:** 14 August 2026  
**Governing rule:** **Derivation is not authorization.**

## 1. Purpose

This standard specifies the minimum record, review, runtime, and authority controls required when an AI system, agent, model, scaffold, or automated R&D process creates or materially modifies a candidate successor. It does not add a MathGov gate. It operationalizes requalification and Action Binding across technical generations.

## 2. Trigger

Create a `SuccessorRequalificationRecord` whenever a change leaves the previously qualified envelope in one or more dimensions: capability, autonomy, tools, infrastructure, data, objective or policy, agent composition, evaluation validity, control assumptions, risk pathways, deployment population, resource limits, or requested authority.

Routine patches inside a declared and tested envelope may remain under configuration change control. The authority that defined the envelope must also define its materiality criteria and review cadence.

## 3. Non-heritable authority

For a parent `S_t` and candidate `S_(t+1)`, `Authority(S_t)` does not imply `Authority(S_(t+1))`. A parent may generate a candidate artifact. It may not generate a legitimate execution mandate or approval for that artifact.

The candidate inherits no consequential tool, network, compute, physical-action, deployment, replication, or recursive-successor-building permission by default. Evidence may be reused only after its validity domain is demonstrated for the candidate.

## 4. Required record

The record must include parent/candidate identity; lineage; generation depth; maximum allowed depth; delta profiles; evidence-reuse basis; evaluation expiry; creator identity; independent reviewer; candidate-lock state; rollback boundary; requalification result; and any fresh candidate-bound authorization.

## 5. Runtime controls

- Parent and candidate configuration hashes are recorded externally.
- Candidate execution is default-deny outside a bounded research environment.
- Permission ceilings are enforced outside the candidate model.
- The candidate cannot alter its lineage record, maximum generation depth, authorization token, or audit log.
- A descendant cannot be the sole reviewer of an ancestor or sibling.
- Exceeding the generation-depth bound triggers halt and requalification.
- Stale evaluation validity triggers narrowing, staging, or refusal.
- Loss of monitoring, containment, rollback, or external halt capacity blocks authority expansion.

## 6. Alignment adaptation lag

Implementations should compare consequential capability change against evaluation, verification, monitoring, containment, governance, and correction capacity as a profile. No universal scalar is claimed. When assurance capacity cannot keep pace, the response is to narrow the envelope, slow the recursive process, increase observability, strengthen independent review, stage the work, or refuse consequential execution.

## 7. Maximum unreviewed generation depth

The conservative high-consequence default is one. A qualified parent may generate a candidate. The candidate may not itself activate consequential tools or generate an executable descendant before independent review. Any exception must be explicit, bounded, independently authorized, and revocable.

## 8. Conformance boundary

Artifact conformance shows that declared fields and structural checks exist. It does not prove that recursive self-improvement will occur, that a candidate is safe, that evaluations are complete, or that the controls are effective in practice.
