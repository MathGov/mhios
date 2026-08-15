# MHIOS v0.3 Core-Build Compatibility and Completion Report

## Verdict

MHIOS v0.3 is the compatible candidate interaction and orchestration package for MathGov Core v12.6 build `MathGov_Core_2026_09_v12.6_SGP_v8.5+2026.08.09.1`. It is not a Core component and does not alter the five-stage cascade.

## Changes from v0.2

1. **Transition/action boundary.** DecisionRun and the run-export schema now require the exact action or state transition under evaluation.
2. **Claim and warrant typing.** Material claims preserve `claim_type`, primary `claim_domain`, and plural `warrant_domains` rather than compressing mixed support into one label.
3. **Cross-domain bridges.** Every material cross-domain relationship is separately recorded with proposition, evidence or rationale, uncertainty, validity or jurisdiction boundary, status, and revision/refusal condition.
4. **Legal-regulatory context.** Legal-regulatory claims preserve jurisdiction, authority source, applicability, interpretation status, and review or contest path.
5. **Capability-authority decomposition.** Compound autonomy fields are replaced with separate generation, reference, constraint, objective, change-authority, warrant, interface, scope, execution-authority, revocation, safe-state, and requalification fields.
6. **Machine enforcement.** The schema and semantic validator reject missing boundaries, invented object types, dangling references, cross-domain bridge omission or mismatch, partial/unsupported bridge overclaiming, missing legal context, and collapsed capability fields.
7. **Core compatibility.** The integration profile and schema crosswalk are pinned to the exact tested Core build.

## Preserved boundaries

- MHIOS remains `ASSUMPTION_BOUND / TEST_REQUIRED`.
- The 12-object, five-screen Minimal Vertical Slice remains the first-build target.
- The full 36-object, 19-screen environment remains a reference design, not a validated optimum.
- AI assistance remains optional and cannot create authority.
- Artifact conformance does not establish decision correctness or deployment safety.
