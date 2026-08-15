#!/usr/bin/env python3
from pathlib import Path
import json, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
PROFILE=yaml.safe_load((ROOT/"registries/MHIOS_CONFORMANCE_PROFILE_v0_8.yaml").read_text())

def evaluate(path):
    data=json.loads(Path(path).read_text())
    types={o.get("object_type") for o in data.get("objects",[])}
    highest="C0"; missing_by_level={}
    for level in ("C1","C2","C3"):
        required=set(PROFILE["levels"][level].get("required_object_types",[]))
        missing=sorted(required-types)
        missing_by_level[level]=missing
        if missing:
            break
        highest=level
    return highest, missing_by_level

if __name__=="__main__":
    if len(sys.argv)<2: raise SystemExit("usage: evaluate_conformance_profile.py <run.json> [...]")
    for arg in sys.argv[1:]:
        level,missing=evaluate(arg)
        print(f"{Path(arg).name}: highest_structurally_satisfied={level}; missing={missing}")
