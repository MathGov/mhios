#!/usr/bin/env python3
"""Run the bounded MHIOS package checks and keep execution evidence outside the release."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parent

def inventory():
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob('*') if p.is_file()}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    out=a.output_dir.resolve()
    if out.is_relative_to(ROOT):p.error('Output directory must be outside the immutable release.')
    out.mkdir(parents=True,exist_ok=True)
    before=inventory();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    py=sys.executable
    commands=[('checksums',[py,'-B','verify_release.py','--output',str(out/'checksums.json')]),
              ('unit_tests',[py,'-B','-m','pytest','-q','-p','no:cacheprovider','--disable-warnings','tests']),
              ('artifact_and_Core_identity',[py,'-B','-m','reference.check_artifacts','--output',str(out/'artifacts.json')]),
              ('static_reading_links',[py,'-B','-m','reference.check_web','--output',str(out/'reading_links.json')])]
    for name in ['decisive_synthetic','nondecisive_authority','rights_blocked','quick_unassessed','recovery_mode_zero','scoped_authorization_simulation']:
        commands.append(('example_'+name,[py,'-B','-m','reference.validate',f'examples/{name}.json','--at','2026-09-28T12:00:00Z','--verify-local-references']))
    # Inspect the heavier document surface before running isolated mutation cases.
    commands[1],commands[2]=commands[2],commands[1]
    results=[]
    for name,cmd in commands:
        start=time.monotonic()
        print('RUN',name,flush=True)
        log_path=out/f'{name}.log'
        with log_path.open('w',encoding='utf-8') as log:
            try:
                run=subprocess.run(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,text=True,timeout=180)
                code=run.returncode
            except subprocess.TimeoutExpired:
                code=124;log.write('\nTIMEOUT\n')
        results.append({'name':name,'command':cmd,'exit_code':code,'status':'PASS' if code==0 else 'FAIL','duration_seconds':round(time.monotonic()-start,3)})
        print(name,results[-1]['status'],flush=True)
    after=inventory();same=before==after
    receipt={'status':'PASS' if same and all(x['status']=='PASS' for x in results) else 'FAIL',
             'executed_at_utc':datetime.now(timezone.utc).isoformat(),
             'build':'MG-MHIOS-2.1-20260928-CORE13.0','tests':results,
             'release_files_unchanged_after_tests':same,'inventory_files':len(before),
             'changed_paths':sorted(k for k in set(before)|set(after) if before.get(k)!=after.get(k)),
             'scope':'Supplied local reference checks and immutable-file verification. No execution authority, empirical validation, full Core replay or native spreadsheet roundtrip.'}
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'])
    return 0 if receipt['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
