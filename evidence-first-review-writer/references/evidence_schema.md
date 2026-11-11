# Data model and audit semantics

All tables use UTF-8 CSV with a header row. IDs must be stable across updates. When unknown, leave a cell empty or use a defined unknown value; **do not guess**.

## Data entities

- **Record** `R0001`: bibliographic/report instance from a search or provided paper. One `record_id` per report version as appropriate.
- **Study** `S0001`: distinct underlying study/experiment/data collection. May link to multiple records. Decide identity from evidence, not only title.
- **Evidence** `E0001`: one source-linked observation, result, or methodological statement, with precise locator.
- **Claim** `CLM001`: one draft manuscript proposition linking to one or more evidence rows.
- **Search** `Q0001`: one actually executed search on one source/platform/date; never synthetically log a query as executed.

## CSV schemas

`records.csv`:

```text
record_id,study_id,title,authors,year,doi,pmid,source_type,venue,url,source_db,peer_review_status,access_level,metadata_status,notes
```

- `metadata_status`: `unverified`, `verified`, `mismatch`, `unavailable`. `verified` is a human-reviewed match to a trustworthy metadata record, not a heuristic match.
- `access_level`: `full_text`, `abstract`, `metadata_only`, `unavailable`.
- `peer_review_status`: `peer_reviewed`, `preprint`, `unknown`, `not_applicable`. A manuscript on a server is not automatically peer-reviewed.

`screening.csv`:

```text
record_id,title_abstract_decision,full_text_decision,exclusion_reason,reviewer,notes
```

`evidence.csv`:

```text
evidence_id,record_id,study_id,claim_id,section_or_page,evidence_type,task,dataset,model_or_method,comparator,metric,metric_value,split,uncertainty,limitations,quote_or_paraphrase,support_status
```

- `support_status`: `supports`, `partial`, `contradicts`, `unknown`.
- `evidence_type`: `primary_fulltext`, `primary_abstract`, `secondary`, `preprint`, `registry`, `benchmark`, `other`.
- `quote_or_paraphrase`: concise paraphrase; respect access rights and quotation limits.
- `split`: exact train/validation/test conditions (cold-target, scaffold, random, temporal, etc.); unknown is **not** random.

`claims.csv`:

```text
claim_id,claim_text,claim_type,strength,evidence_ids,verdict,limitations,manuscript_section
```

- `evidence_ids` separated with semicolons, e.g. `E0001;E0007`.
- `verdict`: `supported`, `qualified`, `contested`, `unsupported`, `unreviewed`.
- `strength`: `descriptive`, `associational`, `comparative`, `causal`, `predictive`, `hypothesis`.

`search_log.csv`: see `references/search_strategy.md`.

## Citations in draft

Use Pandoc-style cite keys derived from record IDs: `[@R0001]`, `[@R0001; @R0002]`; cite keys are stable research IDs and not polished author–year references. The audit tool checks that referenced `R....` IDs exist and their metadata status. Optional inline `{{C:CLM001}}` anchors enable a claim-to-evidence audit. The audit cannot know whether an uncited natural-language sentence is a substantive claim; **manual line-by-line reading remains necessary**. Remove internal tags and replace/export citations according to the target journal for submission.

## Deduplication

Duplicate reports can share DOI, PMID, or an unambiguous normalized title/year when no conflicting identifiers exist. Deduplicate *records*, never collapse different experiments or retracted/updated versions without review. Inspect `duplicate_map.csv`; automatic grouping is only a triage suggestion. Metadata disagreements are a blocking issue for manual resolution.

## Consistency failures to treat as significant

- `evidence.record_id` or `claims.evidence_ids` not present in canonical sources.
- `claims.verdict=supported` with evidence marked `unknown` or `contradicts` and no explicit reconciliation.
- Full-text-specific method claims backed only by metadata/abstract access.
- Cross-paper model superiority claims based on incompatible dataset versions, splits or endpoints.
- No verifiable source for a DOI, or a key cited by the draft absent from `records.csv`.
- A single report counted multiple times as independent samples.

The local CLI detects only some structural failures. The remainder require domain-aware expert review.
