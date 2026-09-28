# MathGov Human Interface and Orchestration Standard

**MHIOS v2.1**, bound to **RippleLogic Canon v13.0**, **SGP v8.8**, and all fifteen files of **MG-RL-13.0-20260926-RELEASE-I**.

MHIOS is the interface and handoff companion. It helps people see what is grounded, protected, viable, ranked, separately chosen, authorized and actually observed. It does not create another Canon gate or turn a form, score, model, signature or local validation result into authority.

## Read first

- [Complete standard (PDF)](docs/MathGov_Human_Interface_and_Orchestration_Standard_v2.1.pdf)
- [Complete standard (Word)](docs/MathGov_Human_Interface_and_Orchestration_Standard_v2.1.docx)
- [Semantic source (Markdown)](docs/MathGov_Human_Interface_and_Orchestration_Standard_v2.1.md)
- [Browser reading copy](docs/MathGov_Human_Interface_and_Orchestration_Standard_v2.1.html)
- [Audit and exact-location improvement report](release/AUDIT_AND_IMPROVEMENTS.md)
- [Verification report](release/VERIFICATION_REPORT.md)
- [Migration guide](release/MIGRATION_GUIDE.md)

## Use the package

1. Read the standard and the scope-specific coverage register.
2. Use the [preparation workbook](templates/MHIOS_v2.1_Implementation_Workbook.xlsx) to assemble source records, not to calculate Canon scores. Blank rows correctly show UNASSESSED. TOKENS_QUALIFY checks only declared tokens and reference presence.
3. Complete a session projection per option. The YAML draft is deliberately incomplete; it must not pass untouched. Synthetic examples are teaching data, never evidence of actual authority or deployment.
4. Run local record checks, then obtain the separate domain, rights, authority and implementation review that the real action requires.

## Verify locally

Use Python 3.10 or newer. Install the tested dependency versions in a dedicated environment:

```bash
python -m pip install -r requirements.txt
python -B verify_all.py --output-dir ../mhios-verification
```

Validate the supplied synthetic example at its declared replay time:

```bash
python -B -m reference.validate examples/decisive_synthetic.json --at 2026-09-28T12:00:00Z --verify-local-references
```

Omitting `--at` checks present-time validity. Old authorization examples will then expire by design. A supplied historical replay time cannot revive real permission. The checker output **RECORD_CONSISTENT_WITHIN_SCOPED_CHECKS** is local record consistency, never authorization.

## Source and scope

The versioned Markdown standard owns MHIOS semantic text; Word, PDF and HTML are complete reading projections. The pinned Core owns its existing semantics. The schemas define only the MHIOS projection, **not** the external Canon run-record v4.1 schema. The source pin manifest records all fifteen unchanged Core hashes. Main document edition and lineage detail are in Appendix RELEASE.

The package has no connected actuators, messaging, financial operations, control daemon or autonomous execution. It does not establish M2/M3 conformance for a deployed interface, full canonical registry conformance, empirical validity, legal or physical safety, Microsoft Excel compatibility, Tier-4/ProofPack status or public hosting. Referenced RPAP/PFAP remain unbundled where required.

## Publication

Publish these files as a companion release, preserving relative paths. [index.html](index.html) is a static reading entry, not an operational dashboard. Do not replace or amend the frozen Core 15 because this companion changed. After publication, compare downloaded files against the locally trusted release/SHA256SUMS.txt; record live URLs, tags and hosting receipts separately. Do not upload Private_Provenance from the complete archive.
