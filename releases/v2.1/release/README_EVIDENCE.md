# Evidence map

- `AUDIT_AND_IMPROVEMENTS.*`: substantive audit and exact section repair locations.
- `CHANGE_REGISTER.json`: 85 semantic, source and synchronization edit operations.
- `FINAL_LAYOUT_POLISH.json`: one italic-rendering repair and five independent list restarts.
- `TABLE_PAGINATION_REPAIR.json`: 124 keep-row-together flags.
- `DOCUMENT_STATISTICS.json`: page-count and reproducible text-count metadata.
- `WORKBOOK_EDITS.json`: preparation-workbook changes only.
- `WORKBOOK_FORMULA_PROBES.json`: eight actual artifact_tool behavior probes.
- `CORE_PIN_MANIFEST.json` is in `../references/`: all fifteen unchanged Core sources.
- `CONFORMANCE_COVERAGE.csv`: sixteen inherited vectors, with executable versus manual boundaries.
- `VERIFICATION_REPORT.md`: executed and unexecuted surfaces.
- `EXECUTION_RECEIPT.json` and `execution/`: pre-package command execution records.
- `MANIFEST.json` and `SHA256SUMS.txt`: final payload inventory, generated last.

The separate delivery receipt records the fresh-extraction rerun and final archive hashes. It is not included inside its own hashed ZIP.
