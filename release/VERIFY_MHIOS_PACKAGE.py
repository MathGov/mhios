#!/usr/bin/env python3
"""Verify the independent MHIOS v0.8 candidate package."""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys, zipfile
from pathlib import Path
import fitz, yaml
from lxml import etree
from jsonschema import Draft202012Validator

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SKIP_HASHES = "--skip-hashes" in sys.argv

def fail(message: str) -> None:
    raise SystemExit(f"VERIFY FAIL: {message}")

required = [
    "README.md", "CHANGELOG.md", "LICENSE", "NOTICE", "VERSION.yaml",
    "docs/MATHGOV_HUMAN_INTERFACE_AND_ORCHESTRATION_STANDARD_v0_8.md",
    "docs/MATHGOV_HUMAN_INTERFACE_AND_ORCHESTRATION_STANDARD_v0_8.docx",
    "docs/MATHGOV_HUMAN_INTERFACE_AND_ORCHESTRATION_STANDARD_v0_8.pdf",
    "docs/MHIOS_MATHGOV_CORE_INTEGRATION_PROFILE_v0_8.md",
    "docs/BURDEN_MEASUREMENT_PROTOCOL_v0_8.md",
    "docs/PILOT_AND_INTER_RATER_RELIABILITY_PROTOCOL_v0_8.md",
    "docs/MHIOS_V0_7_INDEPENDENCE_AND_ACTION_BINDING_REPORT.md",
    "registries/MHIOS_OBJECT_MODEL_v0_8.yaml", "registries/MHIOS_STATE_AND_ROLE_MAP_v0_8.yaml",
    "registries/MHIOS_SCREEN_REGISTRY_v0_8.yaml", "registries/MHIOS_MVS_SCREEN_REGISTRY_v0_8.yaml",
    "registries/MHIOS_OBJECT_JUSTIFICATION_LEDGER_v0_8.yaml",
    "schemas/mhios_run_export_v0_8.schema.json", "schemas/mhios_interaction_event_v0_8.schema.json",
    "release/MHIOS_V0_7_BUILD_2026_08_10_1_CHANGE_LEDGER.json", "release/MHIOS_V0_8_BUILD_2026_08_15_3_CHANGE_LEDGER.json", "release/NORMATIVE_COVERAGE_REPORT.json",
    "release/MUTATION_TEST_REPORT.json", "release/VALIDATION_REPORT.md",
    "tests/validate_mhios.py", "tests/mutation_test_mhios.py", "tests/normative_coverage.py", "tests/evaluate_conformance_profile.py",
    "registries/MHIOS_EXECUTABLE_CHECK_REGISTRY_v0_8.yaml", "registries/MHIOS_CONFORMANCE_PROFILE_v0_8.yaml",
]
for rel in required:
    if not (ROOT / rel).is_file():
        fail(f"missing required file: {rel}")

version = yaml.safe_load((ROOT / "VERSION.yaml").read_text())
if version.get("version") != "0.8" or version.get("release_id") != "MHIOS_v0_8+2026.08.15.3":
    fail("version identity")
if version.get("tested_core_release_id") != "MathGov_Core_2026_09_v12.6_SGP_v8.5+2026.08.15.3":
    fail("exact Core compatibility pin")
if version.get("tested_core_package_name") != "MathGov_Core_2026_09_v12_6_SGP_v8_5_BUILD_2026_08_15_3_FINAL_PUBLICATION_READY.zip" or version.get("tested_core_package_sha256") != "475c4e50da133d6eec497d9cf7da7bbf6e7f7d9d79ce27f0d86b03fdbfccd69f":
    fail("exact Core package pin")
if version.get("tested_core_version_manifest_sha256") != "a11e023c3fb647319b8ac11571d5be684bc2750f6162c661c2d0d42f236b0ed6" or version.get("tested_core_run_schema_sha256") != "dc55a36a53203677a1d3961287269ff76f6b716ff80e25efda5d5d1b2e1ff6bf":
    fail("exact Core interface hash pin")
if version.get("construct_validity") != "UNTESTED" or version.get("core_inclusion") is not False:
    fail("claim boundary")
if version.get("build_id") != "2026.08.15.3" or version.get("package_name") != "MathGov_Human_Interface_and_Orchestration_Standard_v0_8_BUILD_2026_08_15_3_FINAL_PUBLICATION_READY":
    fail("build identity")

registries = {}
for path in (ROOT / "registries").glob("*v0_8.yaml"):
    data = yaml.safe_load(path.read_text())
    if data.get("version") != "0.8":
        fail(f"registry version {path.name}")
    registries[path.name] = data
for registry_name in ("MHIOS_TO_CORE_SCHEMA_CROSSWALK_v0_8.yaml", "MHIOS_CORE_RECORD_COVERAGE_v0_8.yaml"):
    if "WDBIP v1.5" in (ROOT / "registries" / registry_name).read_text() or "WDBIP v1.6" not in (ROOT / "registries" / registry_name).read_text():
        fail(f"WDBIP compatibility pin {registry_name}")
crosswalk = registries["MHIOS_TO_CORE_SCHEMA_CROSSWALK_v0_8.yaml"]
if crosswalk.get("core_release") != "MathGov v12.6 / SGP v8.5 build 2026.08.15.3" or crosswalk.get("tested_core_release_id") != "MathGov_Core_2026_09_v12.6_SGP_v8.5+2026.08.15.3":
    fail("crosswalk exact Core build pin")
if crosswalk.get("tested_core_package_sha256") != "475c4e50da133d6eec497d9cf7da7bbf6e7f7d9d79ce27f0d86b03fdbfccd69f" or crosswalk.get("tested_core_version_manifest_sha256") != "a11e023c3fb647319b8ac11571d5be684bc2750f6162c661c2d0d42f236b0ed6" or crosswalk.get("tested_core_run_schema_sha256") != "dc55a36a53203677a1d3961287269ff76f6b716ff80e25efda5d5d1b2e1ff6bf":
    fail("crosswalk exact Core hash pin")
crosswalk_surfaces = {item.get("mhios_object"): item.get("core_surface") for item in crosswalk.get("mappings", [])}
if crosswalk_surfaces.get("MethodologicalIntegrityRecord") != "MFDI v2.3":
    fail("MFDI compatibility pin")
if crosswalk_surfaces.get("SourceCouplingRecord") != "Source-Coupling Integrity v2.3":
    fail("Source-Coupling compatibility pin")
if "WDBIP v1.6" not in str(crosswalk_surfaces.get("RLSCellRecord", "")):
    fail("WDBIP compatibility pin in active crosswalk")
objects = registries["MHIOS_OBJECT_MODEL_v0_8.yaml"]["objects"]
if len(objects) != 47 or "ExecutionMandateRecord" not in objects or "SuccessorRequalificationRecord" not in objects or "NormativePermissionRecord" in objects:
    fail("object-model identity")
if list(objects.values()).count(None):
    fail("null object specification")
roles = registries["MHIOS_STATE_AND_ROLE_MAP_v0_8.yaml"]
if len(roles.get("roles", {})) != 15:
    fail("role inventory")
if len(registries["MHIOS_SCREEN_REGISTRY_v0_8.yaml"].get("screens", [])) != 20:
    fail("screen inventory")
if len(registries["MHIOS_MVS_SCREEN_REGISTRY_v0_8.yaml"].get("screens", [])) != 5:
    fail("MVS screen inventory")

run_schema = json.loads((ROOT / "schemas/mhios_run_export_v0_8.schema.json").read_text())
event_schema = json.loads((ROOT / "schemas/mhios_interaction_event_v0_8.schema.json").read_text())
Draft202012Validator.check_schema(run_schema); Draft202012Validator.check_schema(event_schema)
if run_schema["properties"]["mhios_version"].get("const") != "0.8":
    fail("run-export schema version")
serialized = json.dumps(run_schema)
for token in ("ExecutionMandateRecord", "SuccessorRequalificationRecord", "action_instance_id", "action_specification_hash", "qualification_snapshot_hash", "mandate_snapshot_hash", "candidate_lock_status"):
    if token not in serialized:
        fail(f"schema missing {token}")

vectors = list((ROOT / "tests/conformance_vectors").glob("*.json"))
passes = [p for p in vectors if p.name.startswith("pass_")]
failures = [p for p in vectors if p.name.startswith("fail_")]
if len(passes) != 6 or len(failures) != 64:
    fail(f"vector inventory {len(passes)} pass/{len(failures)} fail")

# Every active conformance vector must be registry-linked or explicitly supporting/non-normative.
check_registry = yaml.safe_load((ROOT / "registries/MHIOS_EXECUTABLE_CHECK_REGISTRY_v0_8.yaml").read_text())
registry_vector_refs = {Path(rel).name for spec in check_registry.get("checks", {}).values() for rel in spec.get("evidence_paths", []) if rel.startswith("tests/conformance_vectors/")}
active_vector_names = {p.name for p in (ROOT / "tests/conformance_vectors").glob("*.json")}
unmapped_vectors = sorted(active_vector_names - registry_vector_refs)
if unmapped_vectors:
    fail("unmapped active conformance vector(s): " + ", ".join(unmapped_vectors))

profile = yaml.safe_load((ROOT / "registries/MHIOS_CONFORMANCE_PROFILE_v0_8.yaml").read_text())
if profile.get("version") != "0.8" or profile.get("unit") != "conformance_profile":
    fail("conformance profile identity")
for level in ("C0","C1","C2","C3"):
    if level not in profile.get("levels", {}): fail(f"missing conformance level {level}")

for path in vectors + list((ROOT / "examples").glob("*.json")):
    if json.loads(path.read_text()).get("mhios_version") != "0.8":
        fail(f"fixture version {path.relative_to(ROOT)}")

env = dict(os.environ); env["PYTHONDONTWRITEBYTECODE"] = "1"
for script, marker in (
    ("tests/validate_mhios.py", "MHIOS VALIDATION: PASS"),
    ("tests/mutation_test_mhios.py", "MUTATION TEST: PASS 45/45 killed"),
    ("tests/normative_coverage.py", "total_atomic_modal_clauses"),
):
    result = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, text=True, capture_output=True, env=env)
    if result.returncode or marker not in result.stdout:
        fail(f"{script}\n{result.stdout}{result.stderr}")

coverage = json.loads((ROOT / "release/NORMATIVE_COVERAGE_REPORT.json").read_text())
mutation = json.loads((ROOT / "release/MUTATION_TEST_REPORT.json").read_text())
if coverage.get("version") != "0.8" or coverage.get("coverage_unit") != "ONE_UPPERCASE_MODAL_CLAUSE":
    fail("normative coverage identity")
if coverage.get("total_atomic_modal_clauses") != len(coverage.get("requirements", [])) or coverage.get("total_atomic_modal_clauses", 0) < 100:
    fail("normative coverage census")
if any(not row.get("validity_not_established") for row in coverage.get("requirements", [])):
    fail("normative coverage validity boundary")
if any(not row.get("coverage_disposition") for row in coverage.get("requirements", [])):
    fail("normative coverage disposition missing")
if coverage.get("clauses_without_executable_check", 0) != sum(coverage.get("non_machine_dispositions", {}).values()):
    fail("normative coverage disposition accounting")
if mutation.get("mutants") != 45 or mutation.get("survived") != 0:
    fail("mutation report")

main = (ROOT / "docs/MATHGOV_HUMAN_INTERFACE_AND_ORCHESTRATION_STANDARD_v0_8.md").read_text()
for token in (
    "ExecutionMandateRecord", "SuccessorRequalificationRecord", "Derivation is not authorization", "mandate_snapshot_hash", "action_instance_id",
    "action_specification_hash", "qualification_snapshot_hash", "EXECUTION_READINESS(a,t)",
    "ASSUMPTION_BOUND / TEST_REQUIRED", "RG -> RF/NCRC -> TRC -> CSV -> RLS",
):
    if token not in main:
        fail(f"main standard missing {token}")
if "Version 0.6" in main or "permission-snapshot hash" in main:
    fail("stale current prose")

burden = (ROOT / "docs/BURDEN_MEASUREMENT_PROTOCOL_v0_8.md").read_text()
for token in (
    "Valid completion burden", "Hollow-pass rate", "Time to hollow detection",
    "False-positive challenge burden", "D_auto union D_human",
    "prior candidate threshold `RHER <= 1.50` is withdrawn",
):
    if token not in burden:
        fail(f"burden protocol missing {token}")

irr = (ROOT / "docs/PILOT_AND_INTER_RATER_RELIABILITY_PROTOCOL_v0_8.md").read_text()
for token in (
    "Primary packets MUST contain evidence and task instructions only",
    "Case authors MUST NOT rate their own primary cases",
    "RG claim-authority status",
    "Calibration cases are excluded from the primary reliability dataset",
):
    if token not in irr:
        fail(f"IRR protocol missing {token}")

excluded_terms = ("Ely" + "ria", "S" + "OS")
for path in ROOT.rglob("*"):
    if path.is_dir() and path.name == "__pycache__":
        fail(f"bytecode directory {path.relative_to(ROOT)}")
    if path.is_file() and path.suffix.lower() in {".pyc", ".pyo", ".tmp", ".bak", ".swp"}:
        fail(f"ephemeral artifact {path.relative_to(ROOT)}")
    if path.is_file() and (path.name.startswith(".~lock.") or path.name.startswith("~$") or path.name in {".DS_Store", "Thumbs.db"}):
        fail(f"ephemeral office or editor artifact {path.relative_to(ROOT)}")
    if path.is_file() and path.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".json", ".py", ""}:
        value = path.read_text(encoding="utf-8", errors="ignore")
        if any(re.search(rf"\b{re.escape(term)}\b", value, re.I) for term in excluded_terms):
            fail(f"excluded-lineage term in {path.relative_to(ROOT)}")

docx = ROOT / "docs/MATHGOV_HUMAN_INTERFACE_AND_ORCHESTRATION_STANDARD_v0_8.docx"
with zipfile.ZipFile(docx) as archive:
    if archive.testzip() is not None:
        fail("DOCX ZIP integrity")
    names = set(archive.namelist())
    if any("comments" in name.lower() or "vba" in name.lower() for name in names):
        fail("DOCX comments/VBA")
    xml = archive.read("word/document.xml")
    root = etree.fromstring(xml)
    if any(token in xml for token in (b"<w:ins>", b"<w:ins ", b"<w:del>", b"<w:del ")):
        fail("DOCX tracked changes")
    running = b" ".join(archive.read(name) for name in names if name.startswith(("word/header", "word/footer")) and name.endswith(".xml"))
    if b"v0.8" not in running:
        fail("DOCX running version")
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    tables = root.xpath(".//w:tbl", namespaces=ns)
    if not tables:
        fail("DOCX table inventory")
    for index, table in enumerate(tables, 1):
        if not table.xpath("./w:tblPr/w:tblBorders", namespaces=ns):
            fail(f"DOCX table borders {index}")
        rows = table.xpath("./w:tr", namespaces=ns)
        if len(rows) >= 2:
            if not rows[0].xpath("./w:trPr/w:tblHeader", namespaces=ns):
                fail(f"DOCX repeating table header {index}")
            for cell in rows[0].xpath("./w:tc", namespaces=ns):
                fills = cell.xpath("./w:tcPr/w:shd/@w:fill", namespaces=ns)
                if not fills or fills[-1].upper() != "D9EAF7":
                    fail(f"DOCX table header fill {index}")
pdf = fitz.open(ROOT / "docs/MATHGOV_HUMAN_INTERFACE_AND_ORCHESTRATION_STANDARD_v0_8.pdf")
a11y = json.loads((ROOT / "release/DOCX_ACCESSIBILITY_AUDIT.json").read_text())
if pdf.page_count != a11y.get("pdf_pages") or pdf.page_count < 60:
    fail(f"PDF page count {pdf.page_count}")
if any(len(page.get_text().strip()) < 20 and not page.get_images() for page in pdf):
    fail("blank PDF page")
pdf.close()

if not SKIP_HASHES:
    ledger = ROOT / "release/SHA256SUMS.txt"
    ledger_entries = {}
    for line in ledger.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        ledger_entries[rel] = digest
        path = ROOT / rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            fail(f"hash mismatch {rel}")
    manifest = json.loads((ROOT / "release/RELEASE_MANIFEST.json").read_text())
    manifest_entries = {entry["path"]: entry for entry in manifest.get("files", [])}
    if manifest.get("release_id") != "MHIOS_v0_8+2026.08.15.3" or manifest.get("active_file_count") != len(manifest_entries):
        fail("release manifest identity or count")
    if set(manifest_entries) != set(ledger_entries):
        fail("release manifest and SHA-256 ledger inventory differ")
    for rel, entry in manifest_entries.items():
        path = ROOT / rel
        if entry.get("size_bytes") != path.stat().st_size or entry.get("sha256") != ledger_entries[rel]:
            fail(f"release manifest metadata mismatch {rel}")

print("MHIOS ARTIFACT VERIFICATION: PASS")
print("CONSTRUCT VALIDITY: UNTESTED")
print(f"objects=47 roles=15 screens=20 mvs_screens=5 vectors=6 pass/64 expected fail mutation=45/45 pdf_pages={a11y.get('pdf_pages')}")
