# MHIOS v2.0 to v2.1 migration

This is a companion update, not a Core revision. The old document’s organization and useful content are retained; the local wire schema is deliberately tightened and **not backward compatible**. Do not change only version strings and call an old record current.

## Required migration

Freeze the old record and its hash. Bind the new view to the fifteen current Core sources in CORE_PIN_MANIFEST.json. Move aggregate gate states to options[].states with stable option IDs and owner record references. Do not infer per-option qualification from a session-wide PASS. Preserve unknowns; use null only where the schema permits an unassessed or absent field.

Separate framework_verdict, decision_state, framework_selected_option_id, authority_selection, provisional_choice and execution. Carry configuration, evidence cutoff, controls, scoped authorization and expiry; declare runtime recovery and any material successor. Preserve all required every-contender robustness results and compatible joint variants, or withhold a unique-selection claim. A sole survivor needs a separate review record, not invented pairwise arithmetic.

Import SGP v8.8 outputs by reference. Legacy scalar SGP fields are not algebraic equivalents of MPS/FPP/GPR/SPR/ICP/RMCP; re-evaluation belongs to SGP. MPS-NE is not zero, and an informative RMCP summary is not permission or sentience evidence.

Rebuild manual workbook preparations, rather than copying a static YES/NO verdict. The workbook's twenty local formulas now distinguish UNASSESSED, INCOMPLETE, INVALID_STATUS, NOT_QUALIFIED and TOKENS_QUALIFY. The last is a token/reference check only. The original design’s fourteen sheets, practical prompts and existing visual style are retained.

Run schema validation first, then semantic record checks and local reference-hash resolution. Resolve all changed assumptions, qualification, source and authority issues under the owning documents. Matching hashes establish identity, not truth. Archive prior decisions rather than overwrite them.

## Deliberately not supplied

An automatic migration cannot recover missing evidence, determine lawful authority, validate sentience, certify a physical control or prove the complete stress family. Such gaps require review, narrower claims or refusal. No automatic migration script is supplied that fabricates these facts.
