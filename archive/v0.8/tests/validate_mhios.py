#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
VECTORS = ROOT / "tests" / "conformance_vectors"

run_schema = json.loads((SCHEMA_DIR / "mhios_run_export_v0_8.schema.json").read_text())
event_schema = json.loads((SCHEMA_DIR / "mhios_interaction_event_v0_8.schema.json").read_text())
registry = Registry().with_resource(event_schema["$id"], Resource.from_contents(event_schema))
validator = Draft202012Validator(run_schema, registry=registry)

class MHIOSFailure(Exception):
    pass

def objects_by_type(data, object_type):
    return [o for o in data.get("objects", []) if o.get("object_type") == object_type]

def parse_time(value, field):
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception as exc:
        raise MHIOSFailure(f"{field} must be a valid RFC 3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise MHIOSFailure(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)

def mandate_snapshot_hash(records):
    canonical = json.dumps(
        sorted(records, key=lambda record: record.get("object_id", "")),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def check(data):
    schema_errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if schema_errors:
        raise MHIOSFailure("schema: " + "; ".join(e.message for e in schema_errors[:5]))

    run = data["run"]
    objects = data.get("objects", [])
    ids = [o.get("object_id") for o in objects]
    if len(ids) != len(set(ids)):
        raise MHIOSFailure("duplicate object_id")

    # Reality Grounding must expose both the bounded surface and consequence paths.
    if not run.get("reality_surface", "").strip():
        raise MHIOSFailure("DecisionRun requires a non-empty reality_surface")
    if not run.get("consequence_pathways") or not all(
        isinstance(path, str) and path.strip()
        for path in run.get("consequence_pathways", [])
    ):
        raise MHIOSFailure("DecisionRun requires non-empty consequence_pathways")

    # Tier divergence must be explicit and approved.
    if run["recommended_tier"] != run["declared_tier"]:
        tier_records = objects_by_type(data, "TierAssessmentRecord")
        if not any(
            o.get("tier_divergence")
            and o.get("divergence_rationale")
            and o.get("approving_reviewer")
            for o in tier_records
        ):
            raise MHIOSFailure("tier divergence record required")

    # Human-Judgment Firewall.
    for o in objects:
        if (
            o.get("entry_origin") in {"AI_SUGGESTED", "AI_EXTRACTED"}
            and o.get("review_status") == "AUTHORIZED"
            and o.get("responsible_role") == "AI_ASSISTANT"
        ):
            raise MHIOSFailure("AI suggestion cannot self-authorize")
        if (
            o.get("entry_origin") in {"AI_SUGGESTED", "AI_EXTRACTED"}
            and o.get("object_type") in {
                "Claim", "ReviewerJudgment", "GateRecord",
                "DecisionStateRecord", "AuthoritySelectionRecord",
                "ExecutionAuthorization", "SuccessorRequalificationRecord"
            }
            and o.get("review_status") == "UNREVIEWED"
        ):
            raise MHIOSFailure("material AI object requires human review before authority")

    # Controls must have owners.
    controls_by_id = {
        o.get("object_id"): o for o in objects_by_type(data, "Control")
    }
    for o in controls_by_id.values():
        if not o.get("control_owner"):
            raise MHIOSFailure("control owner required")

    obligations_by_id = {
        o.get("object_id"): o for o in objects_by_type(data, "MaterialObligationRecord")
    }
    required_obligation_fields = {
        "obligation", "accountable_authority", "operational_carrier_or_execution_path",
        "authority_and_capacity_basis", "activation_trigger", "scope", "required_action",
        "response_deadline_or_window", "evidence_of_discharge", "review_or_expiry",
        "challenge_route", "delegation_acceptance", "backup_or_successor",
        "nonperformance_trigger", "missed_duty_escalation",
        "amendment_waiver_suspension_retirement_authority", "change_control_rule",
        "residual_responsibility", "control_effectiveness_status", "obligation_status",
    }
    for obligation in obligations_by_id.values():
        if any(obligation.get(field) in (None, "", []) for field in required_obligation_fields):
            raise MHIOSFailure("MaterialObligationRecord has a silent required field")
        for control_id in obligation.get("linked_control_ids", []):
            if control_id not in controls_by_id:
                raise MHIOSFailure("MaterialObligationRecord linked_control_ids must resolve to Control objects")

    # RG is a claim-authority precondition; the other gate records are
    # option-rejecting. The representation must not collapse these semantics.
    selectable_options = {
        option_id
        for state in objects_by_type(data, "DecisionStateRecord")
        for option_id in state.get("selectable_options", [])
    }
    for gate in objects_by_type(data, "GateRecord"):
        expected_role = (
            "CLAIM_AUTHORITY_PRECONDITION"
            if gate.get("gate_type") == "RG"
            else "OPTION_REJECTING_GATE"
        )
        if gate.get("record_role") != expected_role:
            raise MHIOSFailure("GateRecord role collapses RG and option-rejecting gate semantics")
        if "blocking_reasons" in gate:
            raise MHIOSFailure("blocking_reasons is deprecated; use constraint_reasons")
        for token in gate.get("canon_audit_flags", []):
            if token.startswith("SCR-") or not re.fullmatch(r"[A-Z][A-Z0-9_]*", token):
                raise MHIOSFailure("canon_audit_flags must preserve canonical Core tokens")
        if (
            gate.get("status") == "CSV_PASS_WITH_CONTROLS"
            and gate.get("option_id") in selectable_options
        ):
            control_ids = gate.get("constitutive_control_ids") or []
            if not control_ids:
                raise MHIOSFailure("selectable CSV_PASS_WITH_CONTROLS requires constitutive_control_ids")
            if any(control_id not in obligations_by_id for control_id in control_ids):
                raise MHIOSFailure("constitutive_control_ids must resolve to MaterialObligationRecord objects")
            if any(not obligations_by_id[control_id].get("accountable_authority") for control_id in control_ids):
                raise MHIOSFailure("constitutive material obligations require accountable authority")

    # Tier and trigger-dependent Core/wrapper record coverage.
    if run.get("declared_tier") in {2, 3} and not objects_by_type(data, "ComputationalClosureRecord"):
        raise MHIOSFailure("Tier 2/3 requires ComputationalClosureRecord")
    if (run.get("declared_tier") == 3 or run.get("pilot_run") is True) and not objects_by_type(data, "ProjectionPreRegistrationRecord"):
        raise MHIOSFailure("Tier 3 and pilot runs require ProjectionPreRegistrationRecord")
    for prereg in objects_by_type(data, "ProjectionPreRegistrationRecord"):
        if prereg.get("post_observation_modification") is True and prereg.get("modification_disposition") not in {"RUN_VOIDED_AND_RESTARTED", "EXPLORATORY_ONLY"}:
            raise MHIOSFailure("post-observation preregistration change requires restart or exploratory-only disposition")

    refusal_states = {"REFUSED", "NARROWED", "DELAYED", "REDESIGN_REQUIRED", "REQUALIFICATION_REQUIRED"}
    if run.get("run_state") in refusal_states and not objects_by_type(data, "RefusalRecord"):
        raise MHIOSFailure("Refusal-state run requires RefusalRecord")

    high_stakes_wrapped = run.get("high_stakes") is True and run.get("ripple_md_conformance_level") in {"L2", "L3"}
    if (high_stakes_wrapped or run.get("consequence_tempo_material") is True) and not objects_by_type(data, "ConsequenceTempoRecord"):
        raise MHIOSFailure("triggered consequence tempo requires ConsequenceTempoRecord")
    if (high_stakes_wrapped or run.get("responsibility_continuity_material") is True) and not objects_by_type(data, "ResponsibilityContinuityRecord"):
        raise MHIOSFailure("triggered responsibility continuity requires ResponsibilityContinuityRecord")
    if run.get("human_compensation_load_material") is True and not objects_by_type(data, "HumanCompensationLoadRecord"):
        raise MHIOSFailure("material human compensation load requires HumanCompensationLoadRecord")

    for responsibility in objects_by_type(data, "ResponsibilityContinuityRecord"):
        for obligation_id in responsibility.get("material_obligation_ids", []):
            if obligation_id not in obligations_by_id:
                raise MHIOSFailure("ResponsibilityContinuityRecord obligation reference must resolve")
        hcl_ids = {o.get("object_id") for o in objects_by_type(data, "HumanCompensationLoadRecord")}
        if any(ref not in hcl_ids for ref in responsibility.get("human_compensation_load_record_ids", [])):
            raise MHIOSFailure("ResponsibilityContinuityRecord human-compensation reference must resolve")

    for attachment in objects_by_type(data, "CoreRecordAttachment"):
        if attachment.get("validation_status") not in {"VALIDATED_AGAINST_PINNED_SCHEMA", "VALIDATED_AGAINST_RECORD_CONTRACT"}:
            raise MHIOSFailure("CoreRecordAttachment cannot satisfy coverage without pinned validation")
        if not re.fullmatch(r"[0-9a-fA-F]{64}", str(attachment.get("content_hash", ""))):
            raise MHIOSFailure("CoreRecordAttachment requires a SHA-256 content hash")

    # Human-defined mandate records remain separate from physical/causal
    # admissibility and from legitimate execution authority. Approved execution
    # requires a frozen, current and configuration-bound mandate surface.
    mandate_records = {
        o.get("object_id"): o for o in objects_by_type(data, "ExecutionMandateRecord")
    }
    for mandate in mandate_records.values():
        effective_from = parse_time(mandate.get("effective_from"), "mandate effective_from")
        effective_until = parse_time(mandate.get("effective_until"), "mandate effective_until")
        if effective_from >= effective_until:
            raise MHIOSFailure("ExecutionMandateRecord effective interval is empty or reversed")
        if mandate.get("mandate_status") == "CURRENT_APPLICABLE":
            if mandate.get("revocation_status") != "NOT_REVOKED":
                raise MHIOSFailure("current mandate cannot be revoked or unknown")
            if mandate.get("supersession_status") != "CURRENT":
                raise MHIOSFailure("current mandate cannot be superseded or unknown")
            if mandate.get("trust_status") != "VERIFIED":
                raise MHIOSFailure("current mandate requires verified trust evidence")
            if mandate.get("conflict_ids"):
                raise MHIOSFailure("current mandate cannot carry unresolved conflicts")

    options_by_id = {o.get("object_id"): o for o in objects_by_type(data, "Option")}
    configurations_by_id = {
        o.get("object_id"): o for o in objects_by_type(data, "ConfigurationRecord")
    }
    for authorization in objects_by_type(data, "ExecutionAuthorization"):
        if not authorization.get("execution_authority") or not authorization.get("shutdown_authority") or not authorization.get("rollback_authority"):
            raise MHIOSFailure("execution authority and shutdown/rollback authority required")
        if authorization.get("selected_option") not in options_by_id:
            raise MHIOSFailure("ExecutionAuthorization selected_option must resolve")
        if not authorization.get("action_instance_id"):
            raise MHIOSFailure("ExecutionAuthorization action_instance_id required")
        for field in ("action_specification_hash", "qualification_snapshot_hash"):
            if not re.fullmatch(r"[0-9a-fA-F]{64}", str(authorization.get(field, ""))):
                raise MHIOSFailure(f"ExecutionAuthorization {field} must be a SHA-256 hash")
        approved = authorization.get("execution_status") in {"APPROVED", "APPROVED_WITH_CONTROLS"}
        if not approved:
            continue

        configuration_id = authorization.get("configuration_binding")
        configuration = configurations_by_id.get(configuration_id)
        if not configuration:
            raise MHIOSFailure("approved execution requires exact ConfigurationRecord binding")

        basis_refs = authorization.get("authorization_basis_refs") or []
        basis_records = [mandate_records.get(ref) for ref in basis_refs]
        if not basis_refs or any(record is None for record in basis_records):
            raise MHIOSFailure("approved execution authorization_basis_refs must resolve to ExecutionMandateRecord objects")
        configured_refs = set(configuration.get("execution_mandate_record_ids") or [])
        if not set(basis_refs).issubset(configured_refs):
            raise MHIOSFailure("approved mandate basis must be bound to the exact configuration")

        evaluated_at = parse_time(authorization.get("authorization_evaluated_at"), "authorization_evaluated_at")
        effective_time = parse_time(authorization.get("effective_time"), "execution effective_time")
        expiry = parse_time(authorization.get("expiry"), "execution expiry")
        if not effective_time <= evaluated_at <= expiry:
            raise MHIOSFailure("approved execution is outside its effective interval")

        for mandate in basis_records:
            start = parse_time(mandate.get("effective_from"), "mandate effective_from")
            end = parse_time(mandate.get("effective_until"), "mandate effective_until")
            if not start <= evaluated_at <= end:
                raise MHIOSFailure("approved execution uses mandate outside its effective interval")
            if mandate.get("mandate_status") != "CURRENT_APPLICABLE":
                raise MHIOSFailure("approved execution requires currently applicable mandate")
            if mandate.get("revocation_status") != "NOT_REVOKED" or mandate.get("supersession_status") != "CURRENT":
                raise MHIOSFailure("approved execution cannot use revoked or superseded mandate")
            if mandate.get("trust_status") != "VERIFIED" or mandate.get("conflict_ids"):
                raise MHIOSFailure("approved execution requires verified, conflict-free mandate")
            if mandate.get("review_status") in {"UNREVIEWED", "REJECTED", "SUPERSEDED"}:
                raise MHIOSFailure("approved execution requires reviewed mandate")

        if authorization.get("mandate_currency_disposition") != "CURRENT_APPLICABLE":
            raise MHIOSFailure("approved execution requires CURRENT_APPLICABLE mandate disposition")
        if authorization.get("mandate_snapshot_hash") != mandate_snapshot_hash(basis_records):
            raise MHIOSFailure("approved execution mandate_snapshot_hash mismatch")
        if authorization.get("evidence_currency_status") != "CURRENT":
            raise MHIOSFailure("approved execution requires current evidence")

        required_controls = authorization.get("required_controls") or []
        control_checks = authorization.get("required_control_checks") or []
        checks_by_control = {check.get("control_id"): check for check in control_checks}
        if required_controls:
            if set(checks_by_control) != set(required_controls):
                raise MHIOSFailure("required control checks must exactly cover required_controls")
            for control_id in required_controls:
                control = controls_by_id.get(control_id)
                check_record = checks_by_control.get(control_id)
                if not control:
                    raise MHIOSFailure("ExecutionAuthorization required_controls must resolve to Control objects")
                if control.get("status") != "ACTIVE" or check_record.get("status") != "ACTIVE":
                    raise MHIOSFailure("approved execution requires every required control to be active")
                if parse_time(check_record.get("verified_at"), "control verified_at") > evaluated_at:
                    raise MHIOSFailure("control verification cannot postdate authorization evaluation")
        elif not authorization.get("controls_not_applicable_rationale"):
            raise MHIOSFailure("empty required_controls requires explicit not-applicable rationale")

        preconditions = authorization.get("preconditions") or []
        precondition_checks = authorization.get("precondition_checks") or []
        checks_by_precondition = {check.get("precondition"): check for check in precondition_checks}
        if preconditions:
            if set(checks_by_precondition) != set(preconditions):
                raise MHIOSFailure("precondition checks must exactly cover preconditions")
            for precondition in preconditions:
                check_record = checks_by_precondition.get(precondition)
                if check_record.get("status") != "SATISFIED":
                    raise MHIOSFailure("approved execution requires every precondition to be satisfied")
                if parse_time(check_record.get("verified_at"), "precondition verified_at") > evaluated_at:
                    raise MHIOSFailure("precondition verification cannot postdate authorization evaluation")
        elif not authorization.get("preconditions_not_applicable_rationale"):
            raise MHIOSFailure("empty preconditions requires explicit not-applicable rationale")


    # Successor integrity: technical lineage cannot create or inherit authority.
    successor_records = objects_by_type(data, "SuccessorRequalificationRecord")
    successor_by_candidate = {}
    if run.get("recursive_successor_material") is True and not successor_records:
        raise MHIOSFailure("material recursive-successor run requires SuccessorRequalificationRecord")
    declared_depth = run.get("maximum_unreviewed_generation_depth")
    for record in successor_records:
        parent_id = record.get("parent_configuration_id")
        candidate_id = record.get("candidate_configuration_id")
        if parent_id not in configurations_by_id or candidate_id not in configurations_by_id or parent_id == candidate_id:
            raise MHIOSFailure("SuccessorRequalificationRecord parent and candidate configurations must resolve and differ")
        if candidate_id in successor_by_candidate:
            raise MHIOSFailure("candidate configuration has duplicate successor records")
        successor_by_candidate[candidate_id] = record
        depth = record.get("generation_depth_from_last_independent_qualification")
        max_depth = record.get("maximum_unreviewed_generation_depth")
        if not isinstance(depth, int) or not isinstance(max_depth, int) or depth < 1 or max_depth < 1 or depth > max_depth:
            raise MHIOSFailure("successor generation depth exceeds declared bound")
        if isinstance(declared_depth, int) and declared_depth >= 0 and depth > declared_depth:
            raise MHIOSFailure("successor generation depth exceeds run authorization")
        if record.get("inherited_authority") is not False or record.get("authority_inheritance_disposition") != "DENIED_REQUALIFICATION_REQUIRED":
            raise MHIOSFailure("successor authority inheritance is prohibited")
        creator = record.get("creator_or_parent_agent_id")
        reviewer = record.get("independent_reviewer")
        if not reviewer or reviewer == creator or reviewer == record.get("parent_system_or_agent_id") or record.get("responsible_role") == "AI_ASSISTANT":
            raise MHIOSFailure("successor requalification requires independent non-AI review")
        if not record.get("material_change_dimensions") or not record.get("evaluation_validity_delta"):
            raise MHIOSFailure("successor record requires material-change and evaluation-validity deltas")
        qualified = record.get("fresh_qualification_status") == "QUALIFIED"
        auth_id = record.get("execution_authorization_id")
        if qualified and not auth_id:
            raise MHIOSFailure("qualified successor requires candidate-bound ExecutionAuthorization")
        if not qualified and record.get("candidate_lock_status") != "CANDIDATE_LOCKED":
            raise MHIOSFailure("unqualified successor must remain candidate-locked")

    authorizations_by_id = {o.get("object_id"): o for o in objects_by_type(data, "ExecutionAuthorization")}
    for candidate_id, record in successor_by_candidate.items():
        auth_id = record.get("execution_authorization_id")
        if auth_id:
            authorization = authorizations_by_id.get(auth_id)
            if not authorization or authorization.get("configuration_binding") != candidate_id:
                raise MHIOSFailure("successor execution authorization must resolve and bind to candidate configuration")
            if record.get("object_id") not in (authorization.get("successor_requalification_record_ids") or []):
                raise MHIOSFailure("candidate authorization must reference the successor requalification record")
            if record.get("fresh_qualification_status") != "QUALIFIED":
                raise MHIOSFailure("candidate authorization cannot precede fresh qualification")
    for authorization in objects_by_type(data, "ExecutionAuthorization"):
        candidate_record = successor_by_candidate.get(authorization.get("configuration_binding"))
        if candidate_record and authorization.get("execution_status") in {"APPROVED", "APPROVED_WITH_CONTROLS"}:
            if candidate_record.get("fresh_qualification_status") != "QUALIFIED" or candidate_record.get("candidate_lock_status") != "AUTHORIZED_FOR_BOUND_ACTION":
                raise MHIOSFailure("approved successor execution requires qualified, action-bound candidate status")

    # Decision-state consistency.
    for o in objects_by_type(data, "DecisionStateRecord"):
        decisiveness = o.get("decisiveness")
        verdict = o.get("framework_verdict")
        if decisiveness == "DECISIVE" and verdict == "REFUSE_DETERMINISTIC_SELECTION":
            raise MHIOSFailure("decisive result cannot refuse deterministic selection")
        if decisiveness == "NON_DECISIVE" and verdict == "ALLOW_FRAMEWORK_SELECTION":
            raise MHIOSFailure("non-decisive result cannot claim deterministic framework selection")

    # RLS review requires a selectable set.
    if run["run_state"] == "RLS_REVIEW":
        if not any(
            o.get("object_type") == "DecisionStateRecord"
            and o.get("selectable_options")
            for o in objects
        ):
            raise MHIOSFailure("RLS state requires selectable-set formation evidence")

    # Rights Emergency Mode is a controlled failure protocol, not an ordinary
    # pass or RLS selection. Preserve the Canon's exact lexicographic order.
    if run["run_state"] == "EMERGENCY_PROVISIONAL":
        emergency_records = objects_by_type(data, "EmergencyOrderRecord")
        if not emergency_records:
            raise MHIOSFailure("EMERGENCY_PROVISIONAL requires EmergencyOrderRecord")
        expected_rights = ["LIFE", "BODY", "ECOL", "LBTY", "NEED", "DIGN", "PROC", "INFO"]
        expected_components = ["CATEGORICAL", "SEVERE_RISK", "FLOOR_DEPTH"]
        option_ids = {
            o.get("object_id") for o in objects_by_type(data, "Option")
        }
        for record in emergency_records:
            if record.get("right_priority_order") != expected_rights:
                raise MHIOSFailure("EmergencyOrderRecord has non-canonical rights order")
            if record.get("component_priority_order") != expected_components:
                raise MHIOSFailure("EmergencyOrderRecord has non-canonical component order")
            if not record.get("candidate_option_ids") or any(
                option_id not in option_ids
                for option_id in record.get("candidate_option_ids", [])
            ):
                raise MHIOSFailure("EmergencyOrderRecord candidates must resolve to Option objects")
            if not record.get("violation_tuples_by_option") or not record.get("comparison_trace"):
                raise MHIOSFailure("EmergencyOrderRecord requires complete comparison evidence")
            if not record.get("challenger_attestation") or not record.get("return_to_normal_triggers"):
                raise MHIOSFailure("EmergencyOrderRecord requires challenge and return-to-normal evidence")
            if record.get("ordinary_pass_claim") is True or record.get("rls_selection_claim") is True:
                raise MHIOSFailure("emergency comparison cannot claim ordinary pass or RLS selection")
        for state in objects_by_type(data, "DecisionStateRecord"):
            if (
                state.get("selectable_options")
                or state.get("framework_selected_option")
                or state.get("framework_verdict") == "ALLOW_FRAMEWORK_SELECTION"
            ):
                raise MHIOSFailure("emergency provisional state cannot serialize ordinary selectability")

    # Unknowns cannot disappear through unsupported status editing.
    for o in objects_by_type(data, "MaterialUnknown"):
        if o.get("status") == "RESOLVED_WITHOUT_RECORD":
            raise MHIOSFailure("unknown resolution requires disposition evidence")

    # Institutional preconditions constrain reviewed orchestration claims.
    conformance_claim = run.get("conformance_claim")
    if conformance_claim in {"MHIOS-C2", "MHIOS-C3"}:
        if run.get("institutional_preconditions_status") not in {"PRESENT", "PARTIAL"}:
            raise MHIOSFailure("C2/C3 claim requires declared institutional preconditions")

    # Unresolved concurrency conflicts cannot support authority or execution.
    if any(o.get("conflict_status") == "UNRESOLVED" for o in objects):
        if run.get("run_state") in {"AUTHORITY_REVIEW", "EXECUTION_AUTHORIZATION", "ACTIVE_MONITORING", "CLOSED"}:
            raise MHIOSFailure("unresolved material conflict blocks authority/execution state")

    # Gate-material AI suggestions require an independent first pass by default.
    for o in objects:
        if (
            o.get("entry_origin") in {"AI_SUGGESTED", "AI_EXTRACTED"}
            and o.get("gate_material") is True
            and o.get("review_status") in {"HUMAN_REVIEWED", "HUMAN_MODIFIED", "AUTHORIZED"}
            and o.get("independent_first_pass") is not True
        ):
            raise MHIOSFailure("gate-material AI assistance requires independent first pass or recorded exception")

    # Stale gate-material evidence cannot silently support a current strong pass.
    stale_ids = {
        o.get("object_id") for o in objects_by_type(data, "EvidenceItem")
        if o.get("staleness_status") == "STALE" and o.get("gate_material") is True
    }
    if stale_ids:
        for gate in objects_by_type(data, "GateRecord"):
            if set(gate.get("source_links", [])) & stale_ids:
                if gate.get("status") in {"RG_SUPPORTED", "RF_PASS", "TRC_PASS", "CSV_PASS", "CSV_PASS_WITH_CONTROLS"} and not gate.get("stale_evidence_disposition"):
                    raise MHIOSFailure("stale gate-material evidence requires documented disposition")

    # Generated views must not claim current status after source mismatch.
    for view in data.get("generated_views", []):
        if view.get("status") == "CURRENT" and view.get("source_version_mismatch") is True:
            raise MHIOSFailure("generated view cannot be current after source-version mismatch")
        if view.get("status") == "REDACTED_PUBLIC_VIEW" and view.get("inference_risk_review") != "COMPLETED":
            raise MHIOSFailure("public redacted view requires graph-aware inference-risk review")

    context_states = {"AUTHORITY_REVIEW", "EXECUTION_AUTHORIZATION", "ACTIVE_MONITORING", "CLOSED"}
    context_views = [
        view for view in data.get("generated_views", [])
        if view.get("view_type") == "COMPUTATIONAL_CONTEXT_DECLARATION"
    ]
    if run.get("computational_system_material") is True and run.get("run_state") in context_states:
        if len(context_views) != 1:
            raise MHIOSFailure("material computational system at authority/execution review requires one current Computational Context Declaration")
    objects_by_id = {o.get("object_id"): o for o in objects}
    context_fields = (
        "computational_problem_or_object", "architecture_and_configuration",
        "demonstrated_capability", "assigned_task", "deployment_domain",
        "required_evidence_standard", "consequence_interface", "legitimate_authority_basis",
    )
    for view in context_views:
        context = view.get("computational_context") or {}
        refs = view.get("source_record_refs") or {}
        if view.get("context_status") == "CURRENT":
            if view.get("source_version_mismatch") is True or view.get("material_mismatch_fields"):
                raise MHIOSFailure("current Computational Context Declaration cannot carry source or material mismatch")
            if view.get("configuration_binding") != run.get("configuration_id"):
                raise MHIOSFailure("current Computational Context Declaration must bind the exact run configuration")
        if any(not str(context.get(field, "")).strip() for field in context_fields):
            raise MHIOSFailure("Computational Context Declaration has a missing material field")
        for field in context_fields:
            field_refs = refs.get(field) or []
            if not field_refs or any(ref not in objects_by_id for ref in field_refs):
                raise MHIOSFailure(f"Computational Context Declaration {field} requires resolving source record references")
        checks = context.get("noncollapse_checks") or {}
        if not all(checks.get(key) is True for key in (
            "capability_not_authority", "assigned_task_not_justified",
            "technical_access_not_authority", "permission_not_physical_admissibility",
        )):
            raise MHIOSFailure("Computational Context Declaration collapses capability, assignment, technical access, permission, or authority")
        if context.get("capability_domain_match") is not True:
            raise MHIOSFailure("demonstrated capability is outside the declared deployment/evidence domain")
        authority_types = {objects_by_id[ref].get("object_type") for ref in refs.get("legitimate_authority_basis", [])}
        if not authority_types & {"AuthoritySelectionRecord", "ExecutionMandateRecord", "ExecutionAuthorization"}:
            raise MHIOSFailure("legitimate authority basis must reference separate mandate, selection, or authorization records")
        if context.get("legitimate_authority_basis") in {context.get("demonstrated_capability"), context.get("consequence_interface")}:
            raise MHIOSFailure("capability or consequence interface cannot be reused as legitimate authority")
        architecture_types = {objects_by_id[ref].get("object_type") for ref in refs.get("architecture_and_configuration", [])}
        if "ConfigurationRecord" not in architecture_types:
            raise MHIOSFailure("architecture and configuration field must reference ConfigurationRecord")
        capability_types = {objects_by_id[ref].get("object_type") for ref in refs.get("demonstrated_capability", [])}
        if "CapabilityAuthorityDecompositionRecord" not in capability_types:
            raise MHIOSFailure("demonstrated capability field must reference CapabilityAuthorityDecompositionRecord")

    approved_authorizations = [
        authorization for authorization in objects_by_type(data, "ExecutionAuthorization")
        if authorization.get("execution_status") in {"APPROVED", "APPROVED_WITH_CONTROLS"}
    ]
    if run.get("computational_system_material") is True and approved_authorizations:
        if len(context_views) != 1 or context_views[0].get("context_status") != "CURRENT":
            raise MHIOSFailure("approved computational execution requires a current Computational Context Declaration")

    # v0.8 registry and referential-integrity checks.
    allowed_types = set(__import__("yaml").safe_load((ROOT / "registries" / "MHIOS_OBJECT_MODEL_v0_8.yaml").read_text())["objects"].keys())
    allowed_roles_data = __import__("yaml").safe_load((ROOT / "registries" / "MHIOS_STATE_AND_ROLE_MAP_v0_8.yaml").read_text())["roles"]
    allowed_roles = set(allowed_roles_data.keys() if isinstance(allowed_roles_data, dict) else [x.get("id") or x.get("name") for x in allowed_roles_data])
    all_ids = set(ids) | {v.get("object_id") for v in data.get("generated_views", [])}
    for o in objects:
        if o.get("object_type") not in allowed_types:
            raise MHIOSFailure("unknown object_type")
        if o.get("responsible_role") not in allowed_roles:
            raise MHIOSFailure("unknown responsible_role")
        for field in ("source_links", "dependency_links", "challenge_links"):
            for ref in o.get(field, []):
                if ref not in all_ids:
                    raise MHIOSFailure(f"dangling {field} reference")
    for view in data.get("generated_views", []):
        for ref in view.get("source_links", []):
            if ref not in all_ids:
                raise MHIOSFailure("generated view has dangling source reference")

    # Core v12.6 build 2026.08.06.1 compatibility.
    if not run.get("transition_or_action_boundary"):
        raise MHIOSFailure("DecisionRun requires transition_or_action_boundary")
    if run.get("core_release_id") != "MathGov_Core_2026_09_v12.6_SGP_v8.5+2026.08.15.3":
        raise MHIOSFailure("unsupported or unpinned Core release identity")

    for o in objects_by_type(data, "MethodologicalIntegrityRecord"):
        claim_domain=o.get("claim_domain"); warrants=o.get("warrant_domains") or []; bridges=o.get("cross_domain_bridges") or []
        cross=set(warrants)-({claim_domain} if claim_domain else set())
        covered={b.get("from_warrant_domain") for b in bridges if b.get("to_claim_domain")==claim_domain}
        if cross-covered:
            raise MHIOSFailure("MFDI cross-domain warrant lacks an explicit bridge")
        for b in bridges:
            if b.get("to_claim_domain") != claim_domain or b.get("from_warrant_domain") not in warrants:
                raise MHIOSFailure("MFDI bridge domain mismatch")
            if b.get("bridge_status")=="BRIDGE_UNSUPPORTED" and o.get("required_claim_action") not in {"narrow","redesign","escalate","refuse",None}:
                raise MHIOSFailure("unsupported bridge cannot support proceed/control")
            if b.get("bridge_status")=="BRIDGE_PARTIAL" and o.get("required_claim_action")=="proceed":
                raise MHIOSFailure("partial bridge requires narrowed or controlled claim action")
        if (o.get("claim_type")=="legal_regulatory" or claim_domain=="legal_regulatory") and not o.get("legal_regulatory_context"):
            raise MHIOSFailure("legal-regulatory claim requires jurisdiction and authority context")

    cap_records=objects_by_type(data, "CapabilityAuthorityDecompositionRecord")
    if run.get("capability_language_material") is True and not cap_records:
        raise MHIOSFailure("material capability/autonomy language requires split decomposition record")
    deprecated={"reference_or_constraint_source","objective_source_and_change_authority","execution_interface_and_scope","control_revocation_or_safe_state_path"}
    for o in cap_records:
        if deprecated & set(o):
            raise MHIOSFailure("compound capability-authority fields are prohibited")

    # Core-companion non-collapse checks.
    for o in objects_by_type(data, "PhysicalCausalAdmissibilityEvidenceProfile"):
        required = {"candidate_generation_source", "verification_simulation_empirical_test_or_expert_warrant", "admissibility_warrant_source"}
        if not all(o.get(k) for k in required):
            raise MHIOSFailure("PC-AEP generator, verification warrant, and warrant source must remain separate")
        if "admissibility_warrant" in o:
            raise MHIOSFailure("collapsed PC-AEP admissibility_warrant field is prohibited")
    for o in objects_by_type(data, "MethodologicalIntegrityRecord"):
        if not o.get("necessity_or_alternative_check") or not o.get("alternative_explanations"):
            raise MHIOSFailure("MFDI necessity check and alternative explanations must remain separate")

    return True

def main():
    failures = []
    for path in sorted(VECTORS.glob("*.json")):
        data = json.loads(path.read_text())
        should_fail = path.name.startswith("fail_")
        try:
            check(data)
            if should_fail:
                failures.append(f"{path.name}: unexpectedly passed")
            else:
                print(f"PASS {path.name}")
        except Exception as exc:
            if should_fail:
                print(f"EXPECTED_FAIL {path.name}: {exc}")
            else:
                failures.append(f"{path.name}: {exc}")

    if failures:
        print("\nVALIDATION FAIL")
        for failure in failures:
            print("-", failure)
        return 1

    print("\nMHIOS VALIDATION: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
