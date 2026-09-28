#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / 'docs/MATHGOV_HUMAN_INTERFACE_AND_ORCHESTRATION_STANDARD_v0_8.md'
REGISTRY = ROOT / 'registries/MHIOS_EXECUTABLE_CHECK_REGISTRY_v0_8.yaml'
REPORT = ROOT / 'release/NORMATIVE_COVERAGE_REPORT.json'
MODAL_RE = re.compile(r'\b(MUST NOT|MUST)\b')


def fail(message: str) -> None:
    raise SystemExit(f'NORMATIVE COVERAGE FAIL: {message}')


def sentence_for(line: str, position: int) -> str:
    starts = [line.rfind(mark, 0, position) for mark in ('. ', '; ', ': ')]
    start = max(starts) + 2 if max(starts) >= 0 else 0
    ends = [idx for idx in (line.find('. ', position), line.find('; ', position)) if idx >= 0]
    end = min(ends) + 1 if ends else len(line)
    return line[start:end].strip()


registry = yaml.safe_load(REGISTRY.read_text(encoding='utf-8'))
if registry.get('version') != '0.8' or registry.get('unit') != 'executable_check':
    fail('check-registry identity')
checks = registry.get('checks', {})
if not checks:
    fail('empty check registry')

compiled: dict[str, list[re.Pattern[str]]] = {}
for check_id, spec in checks.items():
    if spec.get('coverage_kind') not in {'DIRECT_EXECUTABLE', 'PARTIAL_EXECUTABLE'}:
        fail(f'{check_id}: invalid coverage_kind')
    patterns = spec.get('match_patterns') or []
    if not patterns:
        fail(f'{check_id}: no match patterns')
    compiled[check_id] = [re.compile(p, re.I) for p in patterns]
    evidence_paths = spec.get('evidence_paths') or []
    if not evidence_paths:
        fail(f'{check_id}: no evidence paths')
    for rel in evidence_paths:
        if not (ROOT / rel).is_file():
            fail(f'{check_id}: missing executable evidence path {rel}')

lines = STANDARD.read_text(encoding='utf-8').splitlines()
requirements: list[dict] = []
section = ''
for line_number, line in enumerate(lines, 1):
    if line.startswith('#'):
        section = line.lstrip('#').strip()
    matches = list(MODAL_RE.finditer(line))
    if not matches:
        continue
    # Normative-language definition names the tokens but is not itself a requirement.
    if 'indicates a conformance requirement' in line:
        continue
    for modal_ordinal, modal_match in enumerate(matches, 1):
        source_text = line.strip()
        clause_text = sentence_for(line, modal_match.start())
        matched_ids = [
            check_id for check_id, patterns in compiled.items()
            if any(pattern.search(source_text) for pattern in patterns)
        ]
        kinds = {checks[cid]['coverage_kind'] for cid in matched_ids}
        coverage = 'DIRECT_EXECUTABLE' if 'DIRECT_EXECUTABLE' in kinds else ('PARTIAL_EXECUTABLE' if kinds else 'UNLINKED')
        if coverage == 'UNLINKED':
            low = (section + ' ' + clause_text).lower()
            if any(k in low for k in ('pilot', 'inter-rater', 'burden', 'empirical', 'measure', 'precision', 'recall', 'usability', 'accessibility')):
                disposition = 'EMPIRICAL_TEST_REQUIRED'
            elif any(k in low for k in ('lawful', 'legal', 'jurisdiction', 'mandate validity', 'domain validity', 'physical safety')):
                disposition = 'LEGAL_OR_DOMAIN_DEPENDENT'
            elif any(k in low for k in ('reviewer', 'rationale', 'judgment', 'challenge', 'appeal', 'independent review', 'evidence truth')):
                disposition = 'MANUAL_AUDIT'
            else:
                disposition = 'NOT_MACHINE_TESTABLE'
        else:
            disposition = coverage
        requirements.append({
            'requirement_id': f'NORM-{len(requirements)+1:03d}',
            'line': line_number,
            'section': section,
            'modal_operator': modal_match.group(1),
            'modal_ordinal_in_line': modal_ordinal,
            'atomic_unit': 'ONE_UPPERCASE_MODAL_CLAUSE',
            'clause_text': clause_text,
            'source_text': source_text,
            'test_ids': matched_ids,
            'coverage': coverage,
            'coverage_disposition': disposition,
            'validity_not_established': ['semantic_truth', 'empirical_effectiveness', 'legal_validity', 'domain_validity'],
        })

if not requirements:
    fail('no normative modal clauses found')
source_modal_count = sum(
    len(MODAL_RE.findall(line))
    for line in lines
    if 'indicates a conformance requirement' not in line
)
if source_modal_count != len(requirements):
    fail(f'modal census mismatch source={source_modal_count} ledger={len(requirements)}')

covered = sum(r['coverage'] in {'DIRECT_EXECUTABLE','PARTIAL_EXECUTABLE'} for r in requirements)
direct = sum(r['coverage'] == 'DIRECT_EXECUTABLE' for r in requirements)
partial = sum(r['coverage'] == 'PARTIAL_EXECUTABLE' for r in requirements)
unlinked = [r for r in requirements if r['coverage'] == 'UNLINKED']
from collections import Counter
disposition_counts = Counter(r['coverage_disposition'] for r in unlinked)
machine_eligible = covered + sum(1 for r in unlinked if r['coverage_disposition'] == 'UNIMPLEMENTED_CHECK')
untested = len(unlinked)
report = {
    'standard': 'MHIOS',
    'version': '0.8',
    'coverage_unit': 'ONE_UPPERCASE_MODAL_CLAUSE',
    'method': 'One ledger record is created for every uppercase MUST or MUST NOT modal occurrence outside the normative-language definition. A completeness bundle governed by one modal remains one requirement; separately stated modal clauses are counted separately. Check linkage is drawn only from the executable-check registry and verified evidence paths.',
    'total_atomic_modal_clauses': len(requirements),
    'total_normative_statements': len(requirements),
    'clauses_with_any_executable_check': covered,
    'statements_with_any_executable_check': covered,
    'any_executable_coverage_ratio': covered / len(requirements),
    'clauses_with_direct_behavioral_check': direct,
    'statements_with_direct_behavioral_check': direct,
    'direct_behavioral_coverage_ratio': direct / len(requirements),
    'clauses_with_partial_executable_check': partial,
    'clauses_without_executable_check': untested,
    'machine_eligible_clauses': machine_eligible,
    'machine_eligible_clauses_with_direct_or_partial_coverage': covered,
    'machine_eligible_coverage_ratio': (covered / machine_eligible) if machine_eligible else 1.0,
    'non_machine_dispositions': dict(sorted(disposition_counts.items())),
    'executable_check_registry': 'registries/MHIOS_EXECUTABLE_CHECK_REGISTRY_v0_8.yaml',
    'requirements': requirements,
    'boundary': 'Coverage measures linkage to declared executable checks. Unlinked-clause dispositions are rule-based release-bookkeeping classifications and require human review before being treated as a research claim. Coverage does not establish evidence truth, complete semantic enforcement, empirical effectiveness, legal validity, domain validity, usability, burden reduction, institutional legitimacy, or construct validity.',
}
REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({
    'total_atomic_modal_clauses': report['total_atomic_modal_clauses'],
    'clauses_with_any_executable_check': covered,
    'any_executable_coverage_ratio': report['any_executable_coverage_ratio'],
    'clauses_with_direct_behavioral_check': direct,
    'direct_behavioral_coverage_ratio': report['direct_behavioral_coverage_ratio'],
    'clauses_without_executable_check': untested,
    'machine_eligible_clauses': machine_eligible,
    'machine_eligible_clauses_with_direct_or_partial_coverage': covered,
    'machine_eligible_coverage_ratio': (covered / machine_eligible) if machine_eligible else 1.0,
    'non_machine_dispositions': dict(sorted(disposition_counts.items())),
}, indent=2))
