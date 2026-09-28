# MHIOS Implementation Integrity Profile v0.8

## Concurrency

Use optimistic concurrency with revision identifiers. Material stale writes create conflicts; last-write-wins is prohibited for evidence, states, judgments, authority, controls, and public claims.

## Branching

Every branch records parent, frozen base, purpose, owner, status, and governing/non-governing standing. Challenges inherited before a branch point remain attached unless explicitly resolved.

## Evidence staleness

Use domain- and claim-specific freshness policies rather than a universal decay constant. Stale evidence cannot support a current strong claim without review and requalification.

## Normative-mandate snapshots

Represent every permission used for approved execution as a separately versioned `ExecutionMandateRecord`. Freeze the exact mandate records into a canonical snapshot hash at authorization time. Reject approval when a record is not yet effective, expired, revoked, superseded, conflicted, unverified, scope-inapplicable, hash-invalid, or absent from the exact configuration binding.

A qualified implementation may use a signed, locally pinned policy bundle rather than a live external service. Activation, rollback, external-source failure, conflicting authority, trust-store change and cache staleness must have explicit fail-state and requalification behavior.

## Execution-condition checks

Required controls and preconditions must have item-level verification records. Approved authorization requires exact coverage of the declared sets, current evidence, checks completed no later than the frozen authorization-evaluation time, active controls and satisfied preconditions. Empty sets require explicit not-applicable rationale rather than silence.

## Graph-aware redaction

Review identifiers, relationship edges, counts, timestamps, metadata, and retained conclusions for inference reconstruction. Redaction must not make the decision rationale misleading.

## Legal handling

MHIOS does not create privilege. Organizations define jurisdiction-specific retention, legal hold, access, and protected-handling rules before use. Legal-risk concerns do not justify silent omission of material unknowns or dissent.
