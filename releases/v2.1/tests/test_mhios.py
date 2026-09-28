from __future__ import annotations
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import tempfile
import pytest
import yaml
from jsonschema import Draft202012Validator
from reference.validate import ROOT, load_json, validate_session, validate_interface, verify_local_references, parse_time
AT='2026-09-28T12:00:00Z'
def example(name='decisive_synthetic'):
    return load_json(ROOT/'examples'/f'{name}.json')
def check(x):return validate_session(x,at=AT)
def setp(x,path,value):
    parts=path.split('.')
    for p in parts[:-1]:x=x[int(p)] if isinstance(x,list) else x[p]
    last=parts[-1];x[int(last) if isinstance(x,list) else last]=value

@pytest.mark.parametrize('file',sorted((ROOT/'schemas').glob('*.json')),ids=lambda p:p.name)
def test_schema_structure(file):Draft202012Validator.check_schema(load_json(file))

@pytest.mark.parametrize('name',['decisive_synthetic','nondecisive_authority','rights_blocked','quick_unassessed','recovery_mode_zero','scoped_authorization_simulation'])
def test_supplied_example(name):
    x=example(name);r=check(x)
    assert not r['errors'],r
    assert r['execution_authorized_by_this_validator'] is False
    assert not verify_local_references(x)['errors']

@pytest.mark.parametrize('path,value',[
 ('mhios_version','2.0'),('core_release_id','latest'),('core_pin_manifest_sha256','0'*64),
 ('session_id',''),('session_id','  '),('revision_id',None),('tier',4),('tier',True),
 ('roles',[]),('roles.0.holder',''),('roles.0.conflict',42),
 ('created_at','not-a-date'),('created_at','2026-09-28T08:00:00'),('created_at','2026-09-29T00:00:00Z'),
 ('evidence_cutoff','2026-09-28T10:00:00Z'),('configuration.evaluated_at','2026-09-28T10:00:00Z'),
 ('options.0.states.csv','CSV_REDESIGN'),('options.0.states.csv','PASS'),('options.0.states.rf_ncrc','RF_FAIL'),
 ('options.0.states.rf_ncrc','NCRC_UNKNOWN'),('options.0.states.trc','TRC_FAIL'),('options.0.states.csv','CSV_FAIL'),
 ('options.0.states.rg','RG_REFUSED'),('options.0.record_refs.trc_trigger',None),
 ('options.0.record_refs.controls',None),('options.0.controls_available',False),
 ('options.0.material_unresolved',['unresolved rights harm']),('options.0.requalification_required',True),
 ('options.0.record_refs.rls',None),('options.0.record_refs.rg',None),('options.0.rls_score',None),
 ('options.0.rls_score',1.01),('options.0.sigma_rls',-0.1),('options.0.rls_score',float('nan')),
 ('options.0.sigma_rls',float('inf')),('options.1.option_id','A'),
 ('framework_selected_option_id','MISSING'),('framework_selected_option_id',None),
 ('framework_verdict','AUTHORIZED_SELECTION'),('framework_verdict','REFUSE_DETERMINISTIC_SELECTION'),
 ('decision_state','SELECTED_BY_AUTHORITY_NON_DECISIVE'),('decision_state','NO_SELECTABLE_OPTION'),
 ('option_closure.status','OPTION_SET_THIN'),('option_closure.record_ref',None),
 ('robustness.status','INCOMPLETE'),('robustness.record_ref',None),('robustness.joint_stress_disposition','UNRESOLVED'),
 ('robustness.joint_stress_disposition','EVALUATED'),('robustness.evidence_basis','PROVISIONAL_DEMONSTRATION'),
 ('robustness.required_variants',[]),('robustness.comparisons',[]),('robustness.delta',1.5),
 ('robustness.comparisons.0.signed_gap',2.0),('robustness.comparisons.1.signed_gap',-3.0),
 ('robustness.comparisons.0.contender_id','A'),('robustness.comparisons.0.variant_id','undeclared'),
 ('configuration.material_change_since_qualification',True),
 ('runtime.mode',4), # default MODE0 has no tool request; tested separately, not invalid by mode alone
 ('record_mode','OBSERVED'),('sgp_links.0.sgp_version','8.7'),('sgp_links.0.mps','MPS-5'),
 ('sgp_links.0.mps','MPS-0'),('conformance.assessment','EXTERNAL_ASSESSMENT_RECORDED'),
 ('monitoring_and_outcome.state','OBSERVED'),('monitoring_and_outcome.reopened_stages',['rf_ncrc']),
 ('authority_selection.option_id','A')])
def test_mutated_record_rejected(path,value):
    if path=='runtime.mode':
        # Mode declaration alone is not proof of authority and not a checker-complete mode policy.
        x=example();x['runtime']['reentry_required']=True;x['runtime']['reconciled']=False
    else:x=example()
    setp(x,path,value);assert check(x)['errors'],(path,value)

def test_every_contender_not_just_runner_up():
    x=example();c=deepcopy(x['options'][1]);c['option_id']='C';c['rls_score']=-.01;x['options'].append(c)
    assert any('EVERY_CONTENDER' in e for e in check(x)['errors'])

def test_unranked_contender_cannot_be_selected():
    x=example();o=x['options'][1];o['states']['rls']='NOT_EVALUATED';o['rls_score']=None;o['sigma_rls']=None;o['record_refs']['rls']=None
    assert 'ALLOW_WITH_UNRANKED_CONTENDER' in check(x)['errors']

def test_nominal_leader_mismatch():
    x=example();x['options'][1]['rls_score']=.5
    assert 'WINNER_NOT_NOMINAL_SCORE_LEADER' in check(x)['errors']

def test_duplicate_comparisons():
    x=example();x['robustness']['comparisons'].append(deepcopy(x['robustness']['comparisons'][0]));assert 'DUPLICATE_COMPARISON' in check(x)['errors']

def test_new_joint_variant_cannot_be_ignored():
    x=example();x['robustness']['required_variants'].append('sigma_times_two_adverse_dependence')
    assert check(x)['errors']
    c=deepcopy(x['robustness']['comparisons'][1]);c.update(variant_id='sigma_times_two_adverse_dependence',signed_gap=1.9)
    x['robustness']['comparisons'].append(c);assert check(x)['errors']
    c['signed_gap']=2.1;assert not check(x)['errors']

def test_separate_authority_selection_does_not_authorize():
    r=check(example('nondecisive_authority'));assert not r['errors'];assert not r['execution_authorized_by_this_validator']

def test_conflicting_authority_cannot_appear_framework_selected():
    x=example();x['authority_selection']=deepcopy(example('nondecisive_authority')['authority_selection']);x['authority_selection']['option_id']='B'
    assert 'CONFLICTING_FRAMEWORK_AUTHORITY_SELECTION' in check(x)['errors']

def test_sole_survivor_no_fabricated_gap():
    x=example();x['options']=x['options'][:1];x['robustness']['comparisons']=[]
    assert 'SOLE_SURVIVOR_REVIEW_MISSING' in check(x)['errors']
    x['robustness']['sole_survivor_record_ref']=x['robustness']['record_ref'];assert not check(x)['errors']

def test_ordinary_provisional_choice_needs_its_own_record():
    x=example('nondecisive_authority');x['authority_selection']={'option_id':None,'record_ref':None};x['decision_state']='PROVISIONAL_WITH_CONTROLS'
    assert 'PROVISIONAL_CHOICE_UNRECORDED' in check(x)['errors']
    x['provisional_choice']={'option_id':'A','record_ref':x['robustness']['record_ref'],'controls_ref':x['options'][0]['record_refs']['controls']}
    assert not check(x)['errors']

@pytest.mark.parametrize('path,value',[
 ('execution.authorization_ref',None),('execution.action_id',None),('execution.expires_at',AT),
 ('execution.authorized_at','2026-09-28T13:00:00Z'),('execution.authorized_at','2026-09-28T10:30:00Z'),
 ('execution.bound_configuration_id','OTHER'),('execution.option_id','B'),('execution.controls_ref',None),
 ('execution.state','EXECUTED_UNDER_MONITORING'),('runtime.mode',0),('runtime.mode',1),
 ('runtime.connectivity','RECOVERING'),('runtime.reconciled',False),('runtime.material_successor',True),
 ('runtime.agent_present',False),('configuration.material_change_since_qualification',True),
 ('monitoring_and_outcome.plan_ref',None),('monitoring_and_outcome.reopened_stages',['csv'])])
def test_execution_binding_mutations(path,value):
    x=example('scoped_authorization_simulation');setp(x,path,value);assert check(x)['errors'],path

def test_reentry_needs_reconciliation_and_source():
    x=example('recovery_mode_zero');x['runtime'].update(connectivity='CONNECTED',mode=1,reconciled=True)
    assert 'AUTOMATIC_REENTRY_PROHIBITED' in check(x)['errors']
    r=deepcopy(x['options'][0]['record_refs']['rg']);r['id']='reentry';r['locator']='examples/synthetic_records.json#reentry';x['runtime']['authenticated_reentry_ref']=r
    assert not check(x)['errors']

def test_emergency_never_ordinary_allow():
    x=example();r=x['options'][0]['record_refs']['rg']
    x['emergency']={'pathway':'TAIL_EMERGENCY','record_ref':r,'authority_ref':r,'expires_at':'2026-09-28T15:00:00Z','scope_and_exit':'simulation only'}
    assert check(x)['errors']
    x['framework_verdict']='BLOCK';x['framework_selected_option_id']=None;x['decision_state']='EMERGENCY_PROVISIONAL'
    out=check(x);assert not out['errors'];assert out['emergency_requires_external_review'];assert not out['execution_authorized_by_this_validator']
    x['emergency']['expires_at']=AT;assert 'EMERGENCY_EXPIRED' in check(x)['errors']

def test_extra_key_and_missing_required_group():
    x=example();x['sixth_gate']='PASS';assert check(x)['errors'];del x['sixth_gate'];del x['execution'];assert check(x)['errors']

def test_draft_intentionally_incomplete():
    x=yaml.safe_load((ROOT/'templates/mhios_session_DRAFT_v2.1.yaml').read_text());assert check(x)['errors']

@pytest.mark.parametrize('text',['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}'])
def test_strict_json(text,tmp_path):
    p=tmp_path/'bad.json';p.write_text(text)
    with pytest.raises(ValueError):load_json(p)

def test_interface_state_owner_and_noncolor():
    x=load_json(ROOT/'examples/interface_state.json');assert not validate_interface(x)
    y=deepcopy(x);y['owner']='RUN_EXECUTION';assert validate_interface(y)
    y=deepcopy(x);y['color_is_redundant']=False;assert validate_interface(y)
    y=deepcopy(x);y['presentation_severity']='PASS';assert validate_interface(y)
    y=deepcopy(x);y.update(owner='MHIOS_LOCAL',status_token='PASS');assert validate_interface(y)

@pytest.mark.parametrize('token',['MPS-NE','MPS-0','MPS-1','MPS-2','MPS-3','MPS-4','NOT_EVALUATED'])
def test_sgp_band_import_is_not_assignment(token):
    x=example();x['sgp_links'][0]['mps']=token
    if token!='NOT_EVALUATED':x['sgp_links'][0]['mps_record_ref']=x['options'][0]['record_refs']['rg']
    assert not check(x)['errors'] # presence only, content and patienthood evaluation remain SGP-owned

@pytest.mark.parametrize('kind',['bad_hash','missing','escape','fragment','id','relabel'])
def test_reference_failures(kind):
    x=example();r=x['options'][0]['record_refs']['rg']
    if kind=='bad_hash':r['sha256']='0'*64
    elif kind=='missing':r['locator']='does-not-exist.json'
    elif kind=='escape':r['locator']='../escape.json'
    elif kind=='fragment':r['locator']='examples/synthetic_records.json#missing'
    elif kind=='id':r['id']='OTHER'
    else:r['basis']='SUPPLIED_RECORD'
    assert verify_local_references(x)['errors']

def test_remote_and_null_hash_not_treated_verified():
    x=example();r=x['options'][0]['record_refs']['rg'];r['locator']='https://example.invalid/source'
    assert r['locator'] in verify_local_references(x)['unverified_locators']
    x=example();r=x['options'][0]['record_refs']['rg'];r['sha256']=None
    assert r['locator'] in verify_local_references(x)['unverified_locators']

def test_synthetic_gap_fixture_arithmetic():
    x=example()
    for c,scale in zip(x['robustness']['comparisons'],[1,2]):
        assert c['signed_gap']==pytest.approx(.04/math.sqrt(2*(.005*scale)**2+1e-6),abs=1e-12)
