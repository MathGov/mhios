# MHIOS v2.1 publication audit

The supplied `MathGov_MHIOS_v2.1_Core13.0_Publication.zip` has SHA-256:

`7af9f50b9853957283768548fe51f5502758485eab6cf8006b83640ca0a534f1`

All 86 supplied files are preserved without modification in `releases/v2.1`. The original ZIP is the fixed release download. The private v2.0 provenance described inside the documents was not included in this public ZIP and is not needed to read or run the v2.1 package. We cannot independently reproduce claims about unprovided v2.0 source changes.

## Independently repeated checks

- All ten supplied verification commands passed; 133 tests and six completed synthetic examples passed at the declared replay time.
- The payload was unchanged after running the suite. The supplied ledger covers 85 files plus the ledger itself.
- All fifteen Core source hashes match the previously verified live Core Release I masters. No Core source was altered.
- Complete Markdown/Word body-and-table token parity passed; all 115 rendered PDF contents links resolved to the expected headings. The 41-page PDF had no blank pages or out-of-page text blocks. All pages were visually inspected as rendered contact sheets; no obvious clipping or table-fragment defects were found. This is not a full assistive-technology audit of the PDF.
- Workbook structure: fourteen sheets, twenty formulas, no cached error cells, untouched formula rows UNASSESSED. The package reports eight prior formula probes; this publication pass does not claim a new native Excel recalculation or independently rerun those prior spreadsheet-engine probes.
- All supplied local reading links passed. Hosted website checks and CI publication receipts are recorded separately after deployment.

See [local execution receipt](publication/v2.1/local-verification.json), [Core comparison](publication/v2.1/core-comparison.json), and the [package's detailed evidence boundary](releases/v2.1/release/VERIFICATION_REPORT.md).

## Findings addressed in the publication layer

The package is suitable for publication as a bounded research companion. Its v2.0-to-v2.1 lineage is now distinguished from the previous public v0.8 release. The current release is prominent, old repository files are clearly archived, readers and editable downloads are linked, and version-pinned CI runs the unchanged verifier. Windows users are instructed to enable Python UTF-8 mode because several supplied read operations use the interpreter default encoding. The original publication remains unchanged.

The internal reports' statements that hosting/CI were not yet performed are preparation-time history, not a claim about the repository's subsequent deployment. Likewise old version strings explicitly labeled historical are preserved as provenance.

## Limits

Passing the suite demonstrates the listed checks, not exhaustive semantic correctness or complete conformance. Full external Canon schemas/registries, applicable RPAP/PFAP, actual authority/cryptographic acceptance, human-interface implementation tests, empirical validation and domain safety remain separate. Sixteen listed interface vectors have mixed executable/manual/document-level coverage; 133 tests do not mean 133 independent empirical findings. MHIOS v2.1 is not automatically compatible with v0.8 or v2.0 records.

## Clean-environment and browser findings repaired

The initial clean Linux CI run passed 131 tests but failed two malformed-date tests because the supplied requirements omit jsonschema’s optional RFC3339 date-time dependency. The local environment already contained it. Root `requirements.txt` now explicitly pins `rfc3339-validator==0.1.4`; all checks are rerun in hosted CI. No failing test was skipped or weakened. The recommended publication-edition download includes these installation requirements and preserves the original package under `releases/v2.1/`.

The supplied HTML reader has an empty language attribute and narrow-screen overflow. The hosted `/read/` projection sets English, adds keyboard-focusable scrolling tables, a main landmark, a collapsible contents list and publication navigation. The builder asserts that its complete standard-body text is unchanged. The original HTML remains in the frozen package.
