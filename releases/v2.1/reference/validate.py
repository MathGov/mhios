"""MHIOS record consistency checks. Never authorizes execution or certifies evidence.

Run: python -m reference.validate examples/nondecisive_authority.json --at 2026-09-28T12:00:00Z
Schema validation precedes semantic checks. Cross-record truth, legal authority,
cryptographic attestations, physical adequacy and human UI testing stay external.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlsplit, unquote
from typing import Any
from jsonschema import Draft202012Validator, FormatChecker
from .constants import STAGES, FRAMEWORK_VERDICTS, DECISION_STATES, EXECUTION_STATES
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / 'schemas/mhios_session_v2.1.schema.json'
GOOD = {'rg': {'RG_SUPPORTED','RG_NARROWED'}, 'rf_ncrc': {'RF_PASS'},
        'trc': {'TRC_PASS','TRC_NOT_TRIGGERED'},
        'csv': {'CSV_PASS','CSV_PASS_WITH_CONTROLS','CSV_NOT_MATERIAL'}}

def _pairs(pairs):
    result = {}
    for key, val in pairs:
        if key in result: raise ValueError(f'duplicate JSON key: {key}')
        result[key] = val
    return result

def load_json(path: Path) -> Any:
    def bad(value): raise ValueError(f'non-finite JSON constant: {value}')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=_pairs, parse_constant=bad)

def parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None: raise ValueError('timezone required')
    return dt.astimezone(timezone.utc)

def selectable(option: dict) -> bool:
    return (all(option['states'][k] in values for k, values in GOOD.items())
            and not option['material_unresolved'] and not option['requalification_required']
            and (option['states']['csv'] != 'CSV_PASS_WITH_CONTROLS' or option['controls_available'] is True))

def _finite(value) -> bool:
    if isinstance(value, float): return math.isfinite(value)
    if isinstance(value, dict): return all(_finite(v) for v in value.values())
    if isinstance(value, list): return all(_finite(v) for v in value)
    return True

def validate_session(data: Any, *, at: str | None = None) -> dict:
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    errors = [f'SCHEMA:{"/".join(map(str,e.absolute_path))}:{e.message}'
              for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)]
    if not _finite(data): errors.append('SCHEMA:non-finite numeric value')
    if errors: return result(errors)
    now = parse_time(at) if at else datetime.now(timezone.utc)
    def check(condition: bool, code: str):
        if not condition: errors.append(code)
    cfg=data['configuration']; options=data['options']; ids=[o['option_id'] for o in options]
    from .constants import PIN_MANIFEST_SHA256
    check(hashlib.sha256((ROOT/'references/CORE_PIN_MANIFEST.json').read_bytes()).hexdigest()==PIN_MANIFEST_SHA256,
          'CORE_PIN_MANIFEST_CHANGED')
    check(len(ids)==len(set(ids)), 'DUPLICATE_OPTION_ID')
    by_id={o['option_id']:o for o in options}; qualified=[o['option_id'] for o in options if selectable(o)]
    check(parse_time(data['evidence_cutoff']) <= parse_time(data['created_at']), 'EVIDENCE_CUTOFF_AFTER_RECORD')
    check(parse_time(cfg['evaluated_at']) <= parse_time(data['created_at']), 'CONFIG_EVALUATED_AFTER_RECORD')
    check(parse_time(data['created_at']) <= now, 'FUTURE_RECORD')
    if data['record_mode']=='OBSERVED':
        def refs(obj):
            if isinstance(obj,dict):
                if set(obj)=={'id','locator','sha256','basis'}: yield obj
                for x in obj.values(): yield from refs(x)
            if isinstance(obj,list):
                for x in obj: yield from refs(x)
        check(all(r['basis']!='SYNTHETIC' for r in refs(data)), 'SYNTHETIC_REFERENCE_IN_OBSERVED_RECORD')
    for opt in options:
        oid=opt['option_id']; prev=True
        for stage,good in GOOD.items():
            val=opt['states'][stage]
            check(val is None or opt['record_refs'][stage] is not None, f'MISSING_STAGE_REFERENCE:{oid}:{stage}')
            if data['emergency'] is None:
                check(prev or val is None, f'DOWNSTREAM_ASSESSMENT_AFTER_PRIOR_BLOCK:{oid}:{stage}')
            prev=prev and val in good
        if opt['states']['trc']=='TRC_NOT_TRIGGERED':
            check(opt['record_refs']['trc_trigger'] is not None, f'MISSING_TRC_TRIGGER_ASSESSMENT:{oid}')
        if opt['states']['csv']=='CSV_PASS_WITH_CONTROLS':
            check(opt['record_refs']['controls'] is not None, f'MISSING_CONTROLS_RECORD:{oid}')
            check(opt['controls_available'] is True or opt['requalification_required'], f'CONTROL_UNAVAILABLE_WITHOUT_REOPEN:{oid}')
        if opt['material_unresolved']:
            check(bool(data['blockers']), f'UNRESOLVED_WITHOUT_VISIBLE_BLOCKER:{oid}')
        if opt['states']['rls']=='RLS_RANKED':
            check(selectable(opt), f'RLS_FOR_NONSELECTABLE_OPTION:{oid}')
            check(opt['record_refs']['rls'] is not None and opt['rls_score'] is not None and opt['sigma_rls'] is not None,
                  f'RANKED_WITHOUT_QUANTITATIVE_RECORD:{oid}')
        else:
            check(opt['rls_score'] is None and opt['sigma_rls'] is None, f'UNEVALUATED_SCORE_PRESENT:{oid}')
    fv=data['framework_verdict']; ds=data['decision_state']; winner=data['framework_selected_option_id']
    auth=data['authority_selection']; rob=data['robustness']; emergency=data['emergency']; provisional=data['provisional_choice']
    check(winner is None or winner in ids, 'UNKNOWN_FRAMEWORK_SELECTED_ID')
    check(auth['option_id'] is None or auth['option_id'] in ids, 'UNKNOWN_AUTHORITY_SELECTED_ID')
    if auth['option_id'] is not None:
        check(auth['record_ref'] is not None,'AUTHORITY_SELECTION_WITHOUT_RECORD')
        if emergency is None: check(auth['option_id'] in qualified,'AUTHORITY_SELECTION_OF_NONQUALIFIED_OPTION')
    else: check(auth['record_ref'] is None,'AUTHORITY_RECORD_WITHOUT_SELECTION')
    seen=set()
    for c in rob['comparisons']:
        key=(c['variant_id'],c['candidate_id'],c['contender_id'])
        check(key not in seen,'DUPLICATE_COMPARISON'); seen.add(key)
        check(c['variant_id'] in rob['required_variants'],'UNDECLARED_COMPARISON_VARIANT')
        check(c['candidate_id'] in ids and c['contender_id'] in ids and c['candidate_id']!=c['contender_id'], 'BAD_COMPARISON_OPTION')
    if fv=='ALLOW_FRAMEWORK_SELECTION':
        check(emergency is None,'EMERGENCY_CANNOT_BECOME_ORDINARY_ALLOW')
        check(winner in qualified,'WINNER_NOT_SELECTABLE')
        check(ds=='SELECTED_DECISIVE','ALLOW_DECISION_STATE_MISMATCH')
        check(auth['option_id'] is None or auth['option_id']==winner,'CONFLICTING_FRAMEWORK_AUTHORITY_SELECTION')
        check(not data['monitoring_and_outcome']['reopened_stages'],'ALLOW_WITH_REOPENED_QUALIFICATION')
        check(not cfg['material_change_since_qualification'],'STALE_QUALIFICATION_CANNOT_ALLOW')
        check(data['option_closure']['status']=='COMPLETE' and data['option_closure']['record_ref'] is not None,'OPTION_CLOSURE_INCOMPLETE')
        check(not data['blockers'],'ALLOW_WITH_UNRESOLVED_BLOCKERS')
        check(rob['status']=='COMPLETE' and rob['record_ref'] is not None,'ROBUSTNESS_INCOMPLETE')
        check(rob['evidence_basis'] in (['ACCEPTED_FOR_DECLARED_CLAIM','SYNTHETIC_STIPULATION'] if data['record_mode']=='SYNTHETIC' else ['ACCEPTED_FOR_DECLARED_CLAIM']), 'UNWARRANTED_DECISIVENESS_BASIS')
        check(rob['joint_stress_disposition']!='UNRESOLVED','JOINT_STRESS_UNRESOLVED')
        if rob['joint_stress_disposition']=='EVALUATED': check(rob['joint_record_ref'] is not None,'JOINT_STRESS_RECORD_MISSING')
        if len(qualified)>1:
            check(all(by_id[oid]['states']['rls']=='RLS_RANKED' for oid in qualified),'ALLOW_WITH_UNRANKED_CONTENDER')
            check(bool(rob['required_variants']),'NO_REQUIRED_VARIANTS')
            for variant in rob['required_variants']:
                for contender in qualified:
                    if contender==winner: continue
                    rows=[c for c in rob['comparisons'] if c['variant_id']==variant and c['candidate_id']==winner and c['contender_id']==contender]
                    check(len(rows)==1 and rows[0]['signed_gap']>rob['delta'],f'EVERY_CONTENDER_CHECK_FAILED:{variant}:{contender}')
            if winner in qualified and all(by_id[oid]['rls_score'] is not None for oid in qualified):
                check(all(by_id[winner]['rls_score'] > by_id[oid]['rls_score'] for oid in qualified if oid!=winner),
                      'WINNER_NOT_NOMINAL_SCORE_LEADER')
        elif len(qualified)==1:
            check(rob['sole_survivor_record_ref'] is not None,'SOLE_SURVIVOR_REVIEW_MISSING')
            check(not rob['comparisons'],'SOLE_SURVIVOR_FABRICATED_COMPARISON')
    else:
        check(winner is None,'NONALLOW_WITH_FRAMEWORK_WINNER')
        check(ds!='SELECTED_DECISIVE','DECISIVE_WITHOUT_ALLOW')
    if fv=='REFUSE_DETERMINISTIC_SELECTION':
        check(bool(qualified),'NONDECISIVE_WITHOUT_QUALIFIED_OPTION')
        if auth['option_id'] is not None:
            check(ds=='SELECTED_BY_AUTHORITY_NON_DECISIVE' or emergency is not None, 'AUTHORITY_DECISION_STATE_MISMATCH')
        else: check(ds in ['REFUSE','DELAY','ESCALATE','REDESIGN','PROVISIONAL_WITH_CONTROLS','EMERGENCY_PROVISIONAL'],'NONDECISIVE_DISPOSITION_MISSING')
    if ds=='SELECTED_BY_AUTHORITY_NON_DECISIVE':
        check(fv=='REFUSE_DETERMINISTIC_SELECTION' and auth['option_id'] is not None,'AUTHORITY_STATE_WITHOUT_SEPARATE_REFUSAL')
    if ds=='NO_SELECTABLE_OPTION':
        check(not qualified,'NONEMPTY_NO_SELECTABLE_SET')
        check(fv is not None,'NO_SELECTABLE_WITHOUT_VERDICT')
    if ds=='PROVISIONAL_WITH_CONTROLS':
        # The source record must define the ordinary provisional choice; controls alone do not select it.
        check(provisional is not None,'PROVISIONAL_CHOICE_UNRECORDED')
        if provisional is not None:
            check(provisional['option_id'] in qualified,'PROVISIONAL_OPTION_NOT_QUALIFIED')
        check(auth['option_id'] is None and winner is None,'PROVISIONAL_AND_FINAL_SELECTION_COLLAPSED')
    else:
        check(provisional is None,'PROVISIONAL_RECORD_WITHOUT_POSTURE')
    if fv is None:
        check(ds is None and winner is None and auth['option_id'] is None,'UNASSESSED_VERDICT_WITH_FINAL_STATE')
    if fv=='BLOCK': check(ds in ['NO_SELECTABLE_OPTION','REFUSE','REDESIGN','ESCALATE','EMERGENCY_PROVISIONAL'],'BLOCK_CAUSE_NOT_SERIALIZED')
    if fv=='ESCALATE': check(ds in ['ESCALATE','DELAY','REFUSE','REDESIGN','EMERGENCY_PROVISIONAL'],'ESCALATE_DISPOSITION_MISMATCH')
    if emergency is not None:
        check(ds=='EMERGENCY_PROVISIONAL' and fv!='ALLOW_FRAMEWORK_SELECTION','EMERGENCY_STATE_COLLAPSE')
        check(parse_time(emergency['expires_at'])>now,'EMERGENCY_EXPIRED')
    else: check(ds!='EMERGENCY_PROVISIONAL','MISSING_EMERGENCY_ROUTE')
    exe=data['execution']; rt=data['runtime']; active=exe['state'] in ['AUTHORIZED_WITHIN_SCOPE','EXECUTED_UNDER_MONITORING']
    if active:
        for k in ['option_id','action_id','authorization_ref','bound_configuration_id','authorized_at','expires_at','controls_ref']:
            check(exe[k] is not None,'MISSING_EXECUTION_BINDING:'+k)
        check(exe['option_id'] in ids,'UNKNOWN_EXECUTION_OPTION')
        chosen=auth['option_id'] if auth['option_id'] is not None else (provisional['option_id'] if provisional is not None else winner)
        check(exe['option_id']==chosen and chosen is not None,'EXECUTION_SELECTION_MISMATCH')
        if emergency is None: check(exe['option_id'] in qualified,'EXECUTION_OPTION_NOT_QUALIFIED')
        check(exe['bound_configuration_id']==cfg['configuration_id'],'EXECUTION_CONFIGURATION_MISMATCH')
        check(not cfg['material_change_since_qualification'],'STALE_EXECUTION_APPROVAL')
        check(not data['monitoring_and_outcome']['reopened_stages'],'EXECUTION_WITH_REOPENED_QUALIFICATION')
        if exe['authorized_at'] and exe['expires_at']:
            check(parse_time(exe['authorized_at'])<=now<parse_time(exe['expires_at']),'EXPIRED_OR_FUTURE_AUTHORIZATION')
        check(not data['blockers'] or emergency is not None,'ORDINARY_EXECUTION_WITH_BLOCKERS')
    if exe['state']=='EXECUTED_UNDER_MONITORING': check(exe['execution_event_ref'] is not None,'EXECUTION_EVENT_MISSING')
    if data['monitoring_and_outcome']['state']=='OBSERVED':
        check(data['monitoring_and_outcome']['observation_ref'] is not None,'OBSERVED_OUTCOME_WITHOUT_RECORD')
    if active:
        check(data['monitoring_and_outcome']['plan_ref'] is not None,'EXECUTION_MONITORING_PLAN_MISSING')
        check(exe['authorized_at'] is None or parse_time(exe['authorized_at'])<=parse_time(data['created_at']),
              'AUTHORIZATION_AFTER_RECORD')
    if rt['agent_present']:
        if active:
            check(rt['connectivity']=='CONNECTED' and rt['reconciled'],'RECOVERY_SUSPENDS_EXECUTION_APPROVAL')
        if rt['connectivity']!='CONNECTED':
            check(rt['mode']==0 and not rt['tool_execution_requested'],'DEGRADED_MODE_OR_TOOL_EXECUTION')
        if rt['reentry_required'] and rt['mode']>0:
            check(rt['reconciled'] and rt['authenticated_reentry_ref'] is not None,'AUTOMATIC_REENTRY_PROHIBITED')
        if rt['material_successor'] and (rt['mode']>0 or active):
            check(rt['successor_requalification_ref'] is not None,'SUCCESSOR_INHERITED_AUTHORITY')
        if rt['tool_execution_requested']:
            check(rt['mode']>=2,'MODE0_OR_ADVISORY_TOOL_EXECUTION')
            check(active,'TOOL_EXECUTION_WITHOUT_SCOPED_AUTHORIZATION')
    else: check(rt['mode']==0 and not rt['tool_execution_requested'],'AGENT_ACTION_WITHOUT_AGENT')
    for s in data['sgp_links']:
        if s['mps']!='NOT_EVALUATED': check(s['mps_record_ref'] is not None,'MPS_WITHOUT_SGP_SOURCE')
    if data['conformance']['assessment']=='EXTERNAL_ASSESSMENT_RECORDED':
        check(bool(data['conformance']['evidence_refs']),'CONFORMANCE_CLAIM_WITHOUT_EVIDENCE_REFERENCE')
    return result(errors,qualified, emergency is not None)

def result(errors, qualified=None, emergency=False):
    return {'status':'INVALID_RECORD' if errors else 'RECORD_CONSISTENT_WITHIN_SCOPED_CHECKS',
            'errors':sorted(set(errors)), 'declared_qualified_option_ids':qualified or [],
            'emergency_requires_external_review':emergency, 'execution_authorized_by_this_validator':False,
            'claim_boundary':'Local shape and declared-record consistency only; evidence truth, complete Canon conformance, cryptographic validation, legal authority and deployment safety are not established.'}

def validate_interface(data: Any) -> list[str]:
    schema=load_json(ROOT/'schemas/mhios_interface_state_v2.1.schema.json')
    errs=[e.message for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(data)]
    if errs:return errs
    tokens={'CANON_STAGE':{v for vals in STAGES.values() for v in vals},'CANON_FRAMEWORK':set(FRAMEWORK_VERDICTS),
            'RUN_DECISION':set(DECISION_STATES),'RUN_EXECUTION':set(EXECUTION_STATES),
            'AGENT_RUNTIME':{'LATENT_CAPABILITY','AVAILABLE_CAPABILITY','ENABLED_CAPABILITY','AUTHORIZED_CAPABILITY','SELECTED_ACTION','EXECUTION_APPROVED','EXECUTED_TRANSITION','OBSERVED_OUTCOME'},
            'SGP':{'NOT_EVALUATED','MPS-NE','MPS-0','MPS-1','MPS-2','MPS-3','MPS-4'}}
    if data['owner']=='MHIOS_LOCAL':
        if not data['status_token'].startswith('MHIOS_'):errs.append('LOCAL_TOKEN_REQUIRES_MHIOS_PREFIX')
    elif data['status_token'] not in tokens[data['owner']]:errs.append('TOKEN_OWNER_MISMATCH')
    if data['presentation_severity']=='PASS':
        positive={'RG_SUPPORTED','RF_PASS','TRC_PASS','CSV_PASS','ALLOW_FRAMEWORK_SELECTION','SELECTED_DECISIVE'}
        if data['status_token'] not in positive:errs.append('PASS_PRESENTATION_FOR_NONPASS_STATE')
    return errs

def verify_local_references(data:Any, package_root:Path=ROOT) -> dict:
    """Verify local bytes, never fetch a URL or infer truth from a hash."""
    verified=[];unverified=[];errors=[]
    def walk(x):
        if isinstance(x,dict):
            if set(x)=={'id','locator','sha256','basis'}:yield x
            for v in x.values():yield from walk(v)
        elif isinstance(x,list):
            for v in x:yield from walk(v)
    for r in walk(data):
        u=urlsplit(r['locator'])
        if u.scheme or u.netloc:unverified.append(r['locator']);continue
        path=(package_root/unquote(u.path)).resolve()
        if not path.is_relative_to(package_root.resolve()): errors.append('REFERENCE_PATH_ESCAPE');continue
        if not path.is_file():errors.append('REFERENCE_FILE_MISSING:'+r['locator']);continue
        if r['sha256'] is None:unverified.append(r['locator']);continue
        if hashlib.sha256(path.read_bytes()).hexdigest()!=r['sha256']:errors.append('REFERENCE_HASH_MISMATCH:'+r['locator']);continue
        if u.fragment and path.suffix=='.json':
            doc=load_json(path)
            record=doc.get('records',{}).get(u.fragment)
            if not isinstance(record,dict):errors.append('REFERENCE_FRAGMENT_MISSING:'+r['locator']);continue
            if record.get('record_id')!=r['id']:
                errors.append('REFERENCE_ID_MISMATCH:'+r['locator']);continue
            if record.get('fixture_only') and r['basis']!='SYNTHETIC':
                errors.append('SYNTHETIC_SOURCE_RELABELLED:'+r['locator']);continue
        verified.append(r['locator'])
    return {'verified_local_locators':sorted(set(verified)),'unverified_locators':sorted(set(unverified)),'errors':errors}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path);p.add_argument('--at');p.add_argument('--verify-local-references',action='store_true');a=p.parse_args()
    try:
        data=load_json(a.record);out=validate_session(data,at=a.at)
        if a.verify_local_references and not out['errors']:
            out['references']=verify_local_references(data)
            if out['references']['errors']:out['status']='INVALID_RECORD'
        print(json.dumps(out,indent=2,allow_nan=False));return 0 if out['status']=='RECORD_CONSISTENT_WITHIN_SCOPED_CHECKS' else 1
    except (OSError,ValueError,TypeError) as exc:
        print(json.dumps({'status':'INVALID_RECORD','error':str(exc)}));return 2
if __name__=='__main__': raise SystemExit(main())
