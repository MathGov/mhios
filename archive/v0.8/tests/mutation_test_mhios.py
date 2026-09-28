#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import copy, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from validate_mhios import check, mandate_snapshot_hash

base=json.loads((ROOT/'tests/conformance_vectors/pass_tier2_remote_work_policy.json').read_text())
mandate_base=json.loads((ROOT/'tests/conformance_vectors/pass_tier3_autonomous_shuttle_pilot.json').read_text())
successor_base=json.loads((ROOT/'tests/conformance_vectors/pass_successor_candidate_locked_v08.json').read_text())
context_base=json.loads((ROOT/'tests/conformance_vectors/pass_computational_context_preflight_v08.json').read_text())

def object_of(data, typ):
    return next(o for o in data['objects'] if o['object_type']==typ)

def mut_duplicate_id(d): d['objects'][1]['object_id']=d['objects'][0]['object_id']
def mut_silent_tier(d): d['run']['recommended_tier']=3; d['run']['declared_tier']=2; d['objects']=[o for o in d['objects'] if o['object_type']!='TierAssessmentRecord']
def mut_ai_self_authorize(d):
    o=object_of(d,'Claim'); o['entry_origin']='AI_SUGGESTED'; o['review_status']='AUTHORIZED'; o['responsible_role']='AI_ASSISTANT'
def mut_ai_unreviewed(d):
    o=object_of(d,'Claim'); o['entry_origin']='AI_SUGGESTED'; o['review_status']='UNREVIEWED'
def mut_control_owner(d): object_of(d,'Control')['control_owner']=''
def mut_decision_state(d):
    o=object_of(d,'DecisionStateRecord'); o['decisiveness']='NON_DECISIVE'; o['framework_verdict']='ALLOW_FRAMEWORK_SELECTION'
def mut_rls_precondition(d):
    d['run']['run_state']='RLS_REVIEW'; object_of(d,'DecisionStateRecord')['selectable_options']=[]
def mut_unknown(d): object_of(d,'MaterialUnknown')['status']='RESOLVED_WITHOUT_RECORD'
def mut_conflict(d): d['objects'][0]['conflict_status']='UNRESOLVED'
def mut_ai_first_pass(d):
    o=object_of(d,'Claim'); o['entry_origin']='AI_SUGGESTED'; o['review_status']='HUMAN_REVIEWED'; o['gate_material']=True; o['independent_first_pass']=False
def mut_stale_evidence(d):
    ev=object_of(d,'EvidenceItem'); ev['staleness_status']='STALE'; ev['gate_material']=True
    gate=next(o for o in d['objects'] if o['object_type']=='GateRecord' and o.get('status')=='RF_PASS'); gate.setdefault('source_links',[]).append(ev['object_id'])
def mut_current_stale_view(d):
    d['generated_views']=[{'object_id':'VIEW-M1','object_type':'GeneratedView','run_id':d['run']['run_id'],'version':'1','entry_origin':'SYSTEM_CALCULATED','review_status':'HUMAN_REVIEWED','status':'CURRENT','source_version_mismatch':True}]
def mut_public_inference(d):
    d['generated_views']=[{'object_id':'VIEW-M2','object_type':'GeneratedView','run_id':d['run']['run_id'],'version':'1','entry_origin':'SYSTEM_CALCULATED','review_status':'HUMAN_REVIEWED','status':'REDACTED_PUBLIC_VIEW','inference_risk_review':'NOT_COMPLETED'}]
def mut_institution(d):
    d['run']['conformance_claim']='MHIOS-C2'; d['run']['institutional_preconditions_status']='ABSENT'
def mut_missing_reality_surface(d): d['run']['reality_surface']=''
def mut_rg_role_collapse(d):
    next(o for o in d['objects'] if o['object_type']=='GateRecord' and o.get('gate_type')=='RG')['record_role']='OPTION_REJECTING_GATE'
def mut_unlinked_constitutive_controls(d):
    next(o for o in d['objects'] if o['object_type']=='GateRecord' and o.get('status')=='CSV_PASS_WITH_CONTROLS')['constitutive_control_ids']=[]
def mut_material_obligation_silent_field(d):
    object_of(d,'MaterialObligationRecord')['authority_and_capacity_basis']=''
def mut_bare_control_as_constitutive(d):
    gate=next(o for o in d['objects'] if o['object_type']=='GateRecord' and o.get('status')=='CSV_PASS_WITH_CONTROLS')
    gate['constitutive_control_ids']=[object_of(d,'Control')['object_id']]
def mut_missing_computational_closure(d):
    d['objects']=[o for o in d['objects'] if o['object_type']!='ComputationalClosureRecord']
def mut_pilot_without_preregistration(d): d['run']['pilot_run']=True
def mut_refusal_without_record(d): d['run']['run_state']='REFUSED'
def mut_high_stakes_l2_without_tempo(d):
    d['run']['high_stakes']=True; d['run']['ripple_md_conformance_level']='L2'
def mut_material_human_compensation_missing(d): d['run']['human_compensation_load_material']=True
def mut_unvalidated_attachment(d):
    d['objects'].append({
      'object_id':'CRA-MUT','object_type':'CoreRecordAttachment','run_id':d['run']['run_id'],
      'version':'1','entry_origin':'HUMAN_ENTERED','review_status':'HUMAN_REVIEWED',
      'responsible_role':'RUN_OWNER','record_type':'ReferenceStructureRecord',
      'governing_source':'Canon H.1A','governing_version':'v12.6','trigger_basis':'test',
      'tier_or_claim_scope':'Tier 2','artifact_ref':'artifact://mutant',
      'schema_ref':'record-contract://ReferenceStructureRecord','content_hash':'bad',
      'validation_status':'NOT_VALIDATED','validation_evidence_ref':'none',
      'reviewer_status':'UNREVIEWED','claim_effect_if_missing_or_invalid':'blocks claim'
    })

def refresh_mandate_snapshot(d):
    mandate=object_of(d,'ExecutionMandateRecord')
    object_of(d,'ExecutionAuthorization')['mandate_snapshot_hash']=mandate_snapshot_hash([mandate])
def mut_authorization_expired(d): object_of(d,'ExecutionAuthorization')['expiry']='2026-07-31T18:00:00Z'
def mut_authorization_future(d): object_of(d,'ExecutionAuthorization')['effective_time']='2026-08-02T08:00:00Z'
def mut_mandate_expired(d):
    p=object_of(d,'ExecutionMandateRecord'); p['effective_from']='2026-07-01T08:00:00Z'; p['effective_until']='2026-07-31T18:00:00Z'; p['mandate_status']='EXPIRED'; refresh_mandate_snapshot(d)
def mut_mandate_future(d):
    p=object_of(d,'ExecutionMandateRecord'); p['effective_from']='2026-08-02T08:00:00Z'; p['mandate_status']='NOT_YET_EFFECTIVE'; refresh_mandate_snapshot(d)
def mut_mandate_revoked(d):
    p=object_of(d,'ExecutionMandateRecord'); p['revocation_status']='REVOKED'; p['mandate_status']='REVOKED'; refresh_mandate_snapshot(d)
def mut_mandate_snapshot(d): object_of(d,'ExecutionMandateRecord')['source_hash']='c'*64
def mut_missing_action_instance(d): object_of(d,'ExecutionAuthorization')['action_instance_id']=''
def mut_invalid_action_specification_hash(d): object_of(d,'ExecutionAuthorization')['action_specification_hash']='bad'
def mut_invalid_qualification_snapshot_hash(d): object_of(d,'ExecutionAuthorization')['qualification_snapshot_hash']='bad'
def mut_execution_configuration(d): object_of(d,'ExecutionAuthorization')['configuration_binding']=None
def mut_execution_control(d):
    next(o for o in d['objects'] if o.get('object_id')=='CTL-003-A')['status']='INACTIVE'
    next(x for x in object_of(d,'ExecutionAuthorization')['required_control_checks'] if x['control_id']=='CTL-003-A')['status']='INACTIVE'
def mut_execution_precondition(d):
    next(x for x in object_of(d,'ExecutionAuthorization')['precondition_checks'] if x['precondition']=='route inspection')['status']='NOT_SATISFIED'
def mut_blank_authorization_basis(d): object_of(d,'ExecutionAuthorization')['authorization_basis']=''
def mut_empty_execution_controls(d):
    a=object_of(d,'ExecutionAuthorization'); a['required_controls']=[]; a['required_control_checks']=[]; a.pop('controls_not_applicable_rationale',None)
def mut_empty_execution_preconditions(d):
    a=object_of(d,'ExecutionAuthorization'); a['preconditions']=[]; a['precondition_checks']=[]; a.pop('preconditions_not_applicable_rationale',None)

def mut_context_view_missing(d): d['generated_views']=[]

mutations=[
 ('duplicate_object_id',mut_duplicate_id),('silent_tier_downgrade',mut_silent_tier),
 ('ai_self_authorization',mut_ai_self_authorize),('ai_material_unreviewed',mut_ai_unreviewed),
 ('control_without_owner',mut_control_owner),('decision_state_contradiction',mut_decision_state),
 ('rls_before_selectable_set',mut_rls_precondition),('unknown_disappears',mut_unknown),
 ('unresolved_conflict_at_authority',mut_conflict),('ai_no_independent_first_pass',mut_ai_first_pass),
 ('stale_gate_evidence',mut_stale_evidence),('current_view_source_mismatch',mut_current_stale_view),
 ('public_view_no_inference_review',mut_public_inference),('c2_no_institutional_preconditions',mut_institution),
 ('missing_reality_surface',mut_missing_reality_surface),('rg_role_collapse',mut_rg_role_collapse),
 ('unlinked_constitutive_controls',mut_unlinked_constitutive_controls),
 ('material_obligation_silent_field',mut_material_obligation_silent_field),
 ('bare_control_as_constitutive',mut_bare_control_as_constitutive),
 ('missing_computational_closure',mut_missing_computational_closure),
 ('pilot_without_preregistration',mut_pilot_without_preregistration),
 ('refusal_without_record',mut_refusal_without_record),
 ('high_stakes_l2_without_tempo',mut_high_stakes_l2_without_tempo),
 ('material_human_compensation_missing',mut_material_human_compensation_missing),
 ('unvalidated_attachment',mut_unvalidated_attachment),
]
mandate_mutations=[
 ('authorization_expired',mut_authorization_expired),
 ('authorization_not_yet_effective',mut_authorization_future),
 ('execution_mandate_expired',mut_mandate_expired),
 ('execution_mandate_not_yet_effective',mut_mandate_future),
 ('execution_mandate_revoked',mut_mandate_revoked),
 ('mandate_snapshot_mismatch',mut_mandate_snapshot),
 ('action_instance_missing',mut_missing_action_instance),
 ('action_specification_hash_invalid',mut_invalid_action_specification_hash),
 ('qualification_snapshot_hash_invalid',mut_invalid_qualification_snapshot_hash),
 ('execution_configuration_unbound',mut_execution_configuration),
 ('required_control_inactive',mut_execution_control),
 ('precondition_unsatisfied',mut_execution_precondition),
 ('authorization_basis_blank',mut_blank_authorization_basis),
 ('required_controls_silently_empty',mut_empty_execution_controls),
 ('preconditions_silently_empty',mut_empty_execution_preconditions),
]

def mut_successor_inherit(d): object_of(d,'SuccessorRequalificationRecord')['inherited_authority']=True
def mut_successor_depth(d): object_of(d,'SuccessorRequalificationRecord')['generation_depth_from_last_independent_qualification']=2
def mut_successor_self_review(d): object_of(d,'SuccessorRequalificationRecord')['independent_reviewer']='agent-parent-003'
def mut_successor_unlock(d): object_of(d,'SuccessorRequalificationRecord')['candidate_lock_status']='AUTHORIZED_FOR_BOUND_ACTION'
successor_mutations=[
 ('successor_authority_inheritance',mut_successor_inherit),
 ('successor_generation_depth',mut_successor_depth),
 ('successor_self_review',mut_successor_self_review),
 ('successor_unlock_without_authorization',mut_successor_unlock),
]

results=[]
for name,fn,source in [(n,f,base) for n,f in mutations]+[(n,f,mandate_base) for n,f in mandate_mutations]+[(n,f,successor_base) for n,f in successor_mutations]+[('computational_context_missing',mut_context_view_missing,context_base)]:
    d=copy.deepcopy(source); fn(d)
    killed=False; message=''
    try:
        check(d)
    except Exception as e:
        killed=True; message=str(e)
    results.append({'mutation':name,'killed':killed,'message':message})

out={'suite':'MHIOS v0.8 seeded mutation suite','mutants':len(results),'killed':sum(x['killed'] for x in results),'survived':sum(not x['killed'] for x in results),'mutation_score':sum(x['killed'] for x in results)/len(results),'results':results,'boundary':'Seeded mutation performance does not establish complete normative coverage, legal validity, physical safety, control effectiveness, or construct validity.'}
(ROOT/'release/MUTATION_TEST_REPORT.json').write_text(json.dumps(out,indent=2)+"\n")
for x in results: print(('KILLED' if x['killed'] else 'SURVIVED'),x['mutation'],x['message'])
print(f"MUTATION TEST: {'PASS' if out['survived']==0 else 'FAIL'} {out['killed']}/{out['mutants']} killed")
raise SystemExit(0 if out['survived']==0 else 1)
