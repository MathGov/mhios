# MHIOS — Human Interface and Orchestration Standard

**Version 2.1 · Core v13.0 Release I · SGP v8.8 · Apache-2.0**

MHIOS helps people inspect decision evidence, qualification, uncertainty, responsibility and handoffs. It keeps a framework verdict, an accountable choice, execution authorization and observed outcomes distinct. It is a companion to MathGov / RippleLogic, not a sixteenth Core document or an authorization service.

**[Read online](https://mathgov.github.io/mhios/)** · **[Download the complete publication](https://github.com/MathGov/mhios/releases/tag/v2.1-core13.0)** · [Standard PDF](releases/v2.1/docs/MathGov_Human_Interface_and_Orchestration_Standard_v2.1.pdf) · [Editable Word](releases/v2.1/docs/MathGov_Human_Interface_and_Orchestration_Standard_v2.1.docx) · [Semantic Markdown source](releases/v2.1/docs/MathGov_Human_Interface_and_Orchestration_Standard_v2.1.md)

## What is included

- Complete 41-page standard in Markdown, HTML, PDF and DOCX.
- Fourteen-sheet preparation workbook; schemas, an intentionally incomplete draft and six completed synthetic examples.
- Bounded, read-only record-consistency checker and 133 automated tests.
- All fifteen unchanged Core source files, pinned individually by SHA-256.
- [Audit and improvements](releases/v2.1/release/AUDIT_AND_IMPROVEMENTS.md), [verification scope](releases/v2.1/release/VERIFICATION_REPORT.md), [coverage register](releases/v2.1/release/CONFORMANCE_COVERAGE.csv), and [migration guide](releases/v2.1/release/MIGRATION_GUIDE.md).

The Markdown standard owns MHIOS semantic text. Its Word, PDF and HTML files are reading projections. Core semantics remain owned by the pinned Core sources. The preparation workbook checks declared tokens and reference presence; it does not calculate Canon scores or decide whether evidence is true.

## Exact edition and verification

Build: `MG-MHIOS-2.1-20260928-CORE13.0`. Core: `MG-RL-13.0-20260926-RELEASE-I`. The supplied 86-file publication is preserved without edits under `releases/v2.1/`; repository navigation and hosting records are separate.

Use Python 3.10 or newer in an isolated environment. On Windows, set `PYTHONUTF8=1` before running the supplied tools (PowerShell: `$env:PYTHONUTF8='1'`).

```sh
python -m pip install -r releases/v2.1/requirements.txt
python -B releases/v2.1/verify_all.py --output-dir verification-output
```

For the release ZIP, extract it and run the commands in its package README. Verification output must be outside the frozen package. `--at 2026-09-28T12:00:00Z` replays synthetic fixtures; it never revives real permission. The checker success label is `RECORD_CONSISTENT_WITHIN_SCOPED_CHECKS`, never authorization.

See [publication audit](PUBLICATION.md) and [CI results](https://github.com/MathGov/mhios/actions). The tests cover only their declared scope. No empirical effectiveness, production readiness, M2/M3 deployed-interface conformance, complete external Canon schemas/registries, native Excel interoperability or real authority is established.

## Version lineage and history

GitHub previously published v0.8. The supplied v2.1 package identifies a privately retained v2.0 source baseline; its internal v2.0 migration guide is not an automatic migration path from v0.8. The v0.8 repository snapshot is preserved in [archive/v0.8](archive/v0.8), and its [original fixed release](https://github.com/MathGov/mhios/releases/tag/v0.8) remains available. Do not relabel or silently migrate old records.

This release uses a new M0–M3 interface-conformance vocabulary and bounded implementation. Historical v0.8 test counts, object inventories and C0–C3 claims do not transfer to v2.1. Private provenance was not supplied in this publication ZIP and is not published here.

## Reuse, citation and contribution

The supplied edition is Apache-2.0; see [LICENSE](LICENSE), [NOTICE](NOTICE.md) and [citation metadata](CITATION.cff). Retain notices and identify modifications. External informative standards keep their own rights and are not incorporated or certified by linking them.

[Report a reproducible issue](https://github.com/MathGov/mhios/issues) · [Contribute](CONTRIBUTING.md) · [Security scope](SECURITY.md) · [MathGov directory](https://github.com/MathGov) · [Core v13](https://github.com/MathGov/ripple-logic) · [RippleLogic](https://ripplelogic.org/) · [MathGov foundation](https://mathgov.org/) · [Contact James](mailto:james@ripplelogic.org)
