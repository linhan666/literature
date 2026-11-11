# Literature discovery and reproducible search

## Search-source selection

- **PubMed / MEDLINE**: biomedical and pharmacology discovery; record exact PubMed query and date; respect field tags and MeSH definitions.
- **Europe PMC**: Europe PMC abstract/full-text access for biomedical records; differentiate indexed metadata, abstract, licensed full text, and preprint.
- **OpenAlex**: cross-disciplinary discovery and citation graph. Reconfirm current API quota/authentication before calling; it is not a full-text verifier.
- **Crossref**: DOI resolution and publisher metadata; not a claim-support validator.
- **Web of Science / Scopus**: curated indexes and citation analysis if the researcher has authorized access. Avoid claiming access otherwise.
- **IEEE Xplore / ACM Digital Library**: essential for CS/ML architecture and evaluation papers when applicable.
- **arXiv / bioRxiv / medRxiv**: contemporary preprints; label version and publication status.
- **Semantic Scholar / Google Scholar**: supplemental discovery, citation following, alternative queries; be mindful of API terms and scraping restrictions.
- **ChEMBL / BindingDB / DrugBank / PDB / GPCRdb**: primary domain data sources and database documentation, not automatic evidence for performance claims.

No arbitrary global minimum number of citations proves quality. Coverage depends on the scope, field, eligibility and search results, not a paper quota.

## Keyword blocks

Create disjunctions **within** blocks and conjunctions **between** blocks. Preserve the exact final query adapted to each database's syntax:

- Domain: `("drug target interaction" OR DTI OR "drug target affinity" OR DTA OR "protein ligand")`
- Mechanism: `(cross-attention OR "bilinear attention" OR "pairwise interaction" OR "contact map" OR "interaction fingerprint")`
- Evaluation: `(interpretability OR explanation OR benchmark OR ablation OR "external validation")`

For PubMed use appropriate field restrictions (e.g., `[Title/Abstract]`) and MeSH only after verifying terms exist. For ML conferences, use architecture names and synonyms without forcing PubMed syntax onto IEEE/arXiv. Expand with key paper names and backward/forward citations. Preserve original search terms, not AI paraphrases.

## Minimum search-log fields

`search_id,database,query,filters,run_date,sort,limit,retrieved_count,notes`

- `run_date`: ISO date of *actual* query execution.
- `limit`: the cutoff actually used; a limited API window does not equal total results.
- `retrieved_count`: observed value or blank; no guesses.
- `notes`: access restrictions, API errors, query-string transformation, dedup boundaries, citation chasing.

Each source record has `source_db`, `url`, `source_type`, `access_level` and `metadata_status` recorded. The record's `doi` should be lowercased and normalized without `https://doi.org/`; store original input separately if needed. Do not replace a DOI for a preprint with the journal DOI unless publication equivalence has been verified.

## Freshness policy

When asked for "latest" or "as of today", execute a current search and record the cutoff date. Include seminal older studies where needed for causal or methodological lineage. State whether a source is a new publication, older preprint now published, correction, review, or software-only update. For dynamic benchmark papers, verify repository revision or reported version where available.

## Metadata verification vs claim verification

- Metadata: Crossref / publisher / PubMed title, authors, year, publication state and DOI/PMID.
- Claim: the relevant full-text section, table or figure actually supports the precise wording, including task, sample size, endpoint and comparison direction.
- Quality: assess dataset provenance, split/leakage, baseline fairness, external validation, uncertainty, bias, reproducibility, and conflicts.

DOI matching alone cannot establish the second or third level. `verify_dois.py` emits a **candidate metadata comparison report** for manual review; it must not automatically change `metadata_status` or `support_status`.

## Bibliographic provenance

Keep both raw discovery results and deduplicated canonical records. Preserve linkouts to source/publisher. Prefer original studies when discussing their own methods; label secondary summaries. If a source is inaccessible, say it is abstract-only and limit the claim accordingly. If a citation is retracted or corrected, log and evaluate its implications rather than deleting silently.

## Suggested citation escalation

1. Identify a candidate from primary databases.
2. Check that bibliographic identity is correct.
3. Obtain permitted abstract/full text or source figure/table.
4. Read and record a precise source locator and scope.
5. Map source to evidence row and claim row.
6. Use it in English prose with proportional language; cite the best available primary evidence.
