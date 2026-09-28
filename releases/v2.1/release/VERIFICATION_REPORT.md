# MHIOS verification and readiness

**Component:** MathGov Human Interface and Orchestration Standard v2.1  
**Build:** `MG-MHIOS-2.1-20260928-CORE13.0`  
**Governing dependency:** `MG-RL-13.0-20260926-RELEASE-I`

## 1. Release determination

The supplied MHIOS v2.0 source has been updated to the exact attached Core 15. The result is a publication-ready **research-and-teaching companion specification, bounded record-consistency implementation, preparation workbook and synthetic test package**. It does not create a sixteenth Core document, confer execution permission, establish M2/M3 conformance for a deployed system, or validate the framework empirically.

All fifteen governing Core files are included unchanged in `references/Core_15/`. Their SHA-256 hashes match both the current individual uploads and the Release-I publication archive. The new MHIOS edition does not increment Canon 13.0, SGP 8.8, Aligners 5.9 or any other Core version.

## 2. Executed checks

| Surface | Executed result | Interpretation |
|---|---|---|
| Python tests | **133 passed** | Schema, semantic, adversarial, source-reference, temporal, serialization and release-tool cases. Includes nine package-integrity/link negative tests. |
| Completed examples | **6 consistent** at the declared replay time | Synthetic decisive, authority-selected non-decisive, blocked, unassessed, recovery and scoped-authorization examples. None authorizes an action. |
| Governing Core identity | **15 of 15 matching SHA-256 values** | Exact delivered-source preservation, not a new full Core audit. |
| Core Word containers | **14 opened** through python-docx | Genuine readable Office containers; Core render evidence is not regenerated here. |
| Main Word/Markdown parity | **Complete body and table token sequence matches** | Checks the complete semantic text, excluding front cover/navigation and Markdown punctuation. |
| Main navigation | **115 of 115 internal links resolve to their rendered heading** | Unique Word bookmark names and matching PDF destinations; no live PAGEREF fields. |
| Main PDF | **41 pages rendered and visually reviewed** | No blank pages or text blocks outside page boundaries. Five final typography/list-repair pages were re-rendered and reviewed; other pages were unchanged at 72 dpi. |
| Audit report | **5 pages rendered and visually reviewed** | Complete audit, source boundaries and exact repair locations. |
| Preparation workbook | **14 sheets; 20 formulas; no cached error cells** | Untouched qualification rows display UNASSESSED, not assessed failure. |
| Workbook behavior probes | **8 of 8 matched** | Untouched, incomplete, valid tokens, rights failure, unknown rights, emergency, invalid token and missing source-reference cases. |
| Static website reading links | Checked by `reference/check_web.py` | Local files and HTML anchors only; remote sites are not fetched by this test. |
| Final integrity | `verify_release.py` checks every listed file | The SHA-256 ledger is generated after all semantic, render and workbook bytes are fixed. |

`verify_all.py` runs ten commands: checksum verification, the full test suite, artifact/source inspection, static-reading checks and six example CLI checks. It stores the command logs and receipt **outside** the publication directory and checks that the payload is unchanged after execution. The final delivered ZIP is extracted into a clean directory and this same suite is rerun there. The external delivery receipt names the archives and their exact hashes; do not substitute this report for those executable results.

## 3. Implementation behavior and its limits

The checker rejects inconsistent declarations such as ordinary ranking after failed qualification, missing or duplicated required contender comparisons, a declared joint stress omitted from the result matrix, a selected candidate that is not the nominal leader, false source-file hashes, escaped local reference paths, duplicate JSON keys, nonfinite numeric values, expired or mismatched execution bindings, a missing monitoring plan and unreconciled Agent recovery.

It **does not** independently calculate RLS or CVaR, discover every stakeholder or omitted alternative, choose the required stress family, decide whether a source is true, perform an SGP evaluation, authenticate a real operator, verify a real command signature, execute a tool, or validate physical-control effectiveness. A declared complete stress matrix is still subject to substantive reviewer challenge. A matching hash proves byte identity only.

An active synthetic authorization example is evaluated at `2026-09-28T12:00:00Z`. Omitting the replay clock uses present time; an old example may expire. Historical replay cannot restore live permission. The blank YAML draft intentionally fails completed-record validation.

The sixteen inherited conformance vectors are all listed in `CONFORMANCE_COVERAGE.csv`, which distinguishes automated checks from document-level and manual implementation tests. Describing a manual obligation is not a passed human-interaction, accessibility or operational test.

## 4. Preservation and migration

The 24-section organizing structure and ten inherited tables remain. Necessary source, state and interface requirements are revised in place. Existing table widths, borders, shading and style definitions are retained; 124 keep-row-together flags prevent split-row fragments. Five independent numbered sequences restart at one, and two literal Markdown emphasis spans are rendered as Word italics. Version identity moves to Appendix RELEASE; the running header/footer no longer names the old edition. Page/word metadata uses the documented render/text method.

The MHIOS preparation workbook retains its fourteen sheets and visual design. Its twenty local preparation formulas were corrected; it is **not** the unchanged Core Aligners workbook. `TOKENS_QUALIFY` denotes only accepted declared tokens and source-reference presence, not valid evidence, a Canon gate verdict or permission.

Existing v2.0 session records are not automatically wire-compatible with the stricter v2.1 schema. Migration creates a new linked record, supplies per-option status and reference fields, preserves unresolved values and requires revalidation. Never manufacture missing assessments merely to make an old record pass.

## 5. Unexecuted or unestablished surfaces

No native Excel/Calc spreadsheet recalculation or interoperability certification; no empirical rater study or cross-domain calibration; no interactive browser, keyboard, assistive-technology or participant study; no live website deployment or hosted CI execution; no actual domain authority, physical safety, cryptographic command acceptance or production-runtime test. Full external Canon schemas/registries, normative kernel libraries and applicable RPAP/PFAP remain separate dependencies. Their absence is disclosed rather than filled with invented files.

The right next use is publication of this bounded companion, independent review and implementation-specific testing. A deployment must separately demonstrate the human, organizational, legal, technical and consequence-domain conditions required by the unchanged Core.
