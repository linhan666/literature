# Claim-to-source provenance contract

## Sources ledger (`sources.csv`)

Columns: `source_id,title,authors,year,doi_or_url,source_file,identity_status,notes`.

- `identity_status`: `verified_original`, `verified_index`, `unverified`, `conflicting`.
- Keep two similarly titled projects distinct until lineage is proven. Never replace a missing DOI with a guessed one.
- Locate claim-support passages in primary material; record page/section/table/figure (plus PDF page indexing convention if needed).

## Claims ledger (`claims.csv`)

Columns: `claim_id,claim_text,epistemic_status,verification_status,source_ids,source_locator,verification_basis,comparability_scope,limitations,slide_ids`.

- `epistemic_status`: `source_reported` (source's statement), `independently_verified` (separate empirical reproduction or audit), `synthesis_inference` (reviewer's cross-source synthesis), `author_proposed` (new framework/concept), `disputed` (conflicting support), or `unresolved` (missing/unclear).
- `verification_status`: `verified_against_source`, `partially_checked`, `not_checked`, or `conflicting`.
- `source_ids`: semicolon-separated IDs from sources ledger. `source_locator`: actual inspected passage or table. `source_reported` can never be called independently replicated by this check alone.
- `independently_verified` must include `verification_basis` describing independent replication or code-level audit; simply reading the original paper does not qualify. `source_reported` requires original-source inspection, not just bibliographic metadata. An author proposal can be uncited if clearly labeled. A supported synthesis must cite its premises, explain inference, and disclose competing findings. Disputed/unresolved claims must be visually marked.
- For cross-paper performance comparisons: record endpoint, dataset version, labels, negatives, split, 3D access, pretraining, training budget and statistic conditions. No matched comparison → no leaderboard or causal effect.

## Figure manifest (`figure_manifest.csv`)

Columns: `figure_id,slide_id,file_path,figure_type,source_id,source_page,adapted_or_reproduced,license_or_permission,transformations,notes`.

Use `original_editable`, `original_raster`, `adapted`, `reproduced` as figure types; use explicit `unknown` permission status rather than implying permission. Images are not evidence by themselves. Artwork generated from a proposed synthesis should be marked `AUTHOR-PROPOSED`.

## Visible source mapping

Each content slide must show either valid compact citation IDs that resolve to a full bibliography, or an explicit `AUTHOR-PROPOSED / INTERPRETATION / UNRESOLVED / DEMO` label. Full source metadata and the specific reviewed material should be in speaker notes or appendix. A tiny citation ID is not a substitute for an auditable source record.

The reference validator checks schema, ID linkage and status compatibility; it cannot verify scientific truth, identity correctness, DOI resolution or study design by itself.
