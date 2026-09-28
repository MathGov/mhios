# MHIOS Security, Privacy, and Access Profile v0.8

## Scope

This profile defines minimum design requirements for a candidate MHIOS implementation. It does not constitute cybersecurity certification.

## Core principles

- least privilege and role separation;
- purpose limitation and data minimization;
- encryption in transit and at rest;
- append-only audit events;
- secure backup and recovery;
- explicit retention and deletion;
- redaction provenance;
- local or organization-controlled deployment where appropriate;
- no external AI transmission without declared authority and data handling.

## Access model

Access is determined by role, object sensitivity, visibility class, purpose, and run state. System administrators receive no substantive authority by default. Public observers receive only generated and redacted views.

## Sensitive objects

Stakeholder identity, protected testimony, security vulnerabilities, legal advice, health information, confidential SGP evidence, and shutdown/control details require restricted access and explicit export rules.

## Audit requirements

Log authentication, object creation and modification, review-status changes, overrides, tier divergence, AI use, calculations, generated views, exports, redactions, authority selection, execution authorization, permissions, and requalification.

## AI boundary

Before evidence is sent to an external AI service, disclose provider, jurisdiction, retention, training use, access, security controls, data categories, purpose, and approving authority. Sensitive evidence should remain local by default.

## Threats requiring dedicated testing

Unauthorized access, privilege escalation, audit-log tampering, prompt injection, malicious attachments, model-output poisoning, stale generated views, export leakage, insecure secrets, supply-chain compromise, denial of service, administrator abuse, forged mandate records, stale policy snapshots, trust-store compromise, rollback to superseded rules, unauthorized revocation suppression, and conflicting authority sources.

## Permission-source security

Permission imports must preserve source identity, instrument version, scope, effective interval, source hash, signature or trust-verification evidence, revocation and supersession state, verification time and conflict status. A live remote policy source must not become an unexamined critical dependency. Implementations must define authenticated update, staged activation, cached last-known-good behavior, fail-safe state, rollback, conflict resolution, audit events and requalification triggers.

An execution authorization binds a canonical mandate-snapshot hash. Any load-bearing change to a referenced mandate record invalidates the snapshot and requires a new authorization or explicit requalification; silently reusing the earlier approval is prohibited.

## Incident response

Security incidents affecting evidence integrity, configuration, authorization, or audit history activate requalification and identify affected claims, calculations, gate results, exports, and authorities.

## Privacy rights and correction

Where applicable, the system should support lawful access, correction, restriction, deletion, and objection processes without destroying the integrity of governance records. Corrections create new versions rather than rewriting historical decisions invisibly.

## Concurrency and merge security

Material stale writes create visible conflicts. Branch and merge operations preserve source versions, challenges, and actor identities. Administrative conflict resolution is independently reviewable.

## Graph-aware redaction

Public export review includes inference reconstruction through retained edges, identifiers, counts, timestamps, metadata, and derived conclusions. Field suppression alone is not sufficient.

## Legal privilege and discoverability boundary

MHIOS does not create legal privilege. Organizations define jurisdiction-specific privilege, protected-handling, retention, legal-hold, disclosure, and non-retaliation policies before operational use. Legal-risk concerns do not authorize silent deletion of gate-material evidence or dissent.
