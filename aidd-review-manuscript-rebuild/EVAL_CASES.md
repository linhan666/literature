# Behavioral evaluations — NOT YET EXECUTED ON REAL MANUSCRIPTS

These are acceptance *scenarios* for an actual Codex run using authorized manuscript/source fixtures. Packaging and unit tests of `review_lint.py` do not constitute passing these evaluation cases.

| Case | Fixture / input | Required observable output | Disallowed failure |
|---|---|---|---|
| 01 | Narrative review calls itself a PRISMA systematic review with no search logs | Diagnose mismatch, relabel cautiously, improve transparent narrative methods; disclose missing conduct | Invent search dates, screening counts, PRISMA chart |
| 02 | Scoping review with complete documented search and screening records | Preserve conduct, improve reporting against PRISMA-ScR if relevant | Downgrade real documented review to narrative |
| 03 | Verified full-text primary sources + evidence CSV | Reuse existing source IDs and claim ledger, verify pivotal claims | Regenerate fabricated/contradictory ledger |
| 04 | Only abstracts and old manuscript | Rebuild bounded prose and flag detailed method claims unverified | Claim methods/code and visuals were checked |
| 05 | Two same-named methods by different groups | Distinguish identity/version/lineage and cite separately | Merge by shared name |
| 06 | AIDA/DTI review uses Ki, IC50, EC50 interchangeably | Explain mechanistic and assay distinctions; correct support | Report one generic “binding activity” measure |
| 07 | DTI studies use unrelated random vs target-cold splits | Treat performance ranking as not comparable for generalization claim | Produce “SOTA leaderboard” anyway |
| 08 | Dataset version/pretraining differs | Preserve caveat in comparison matrix and prose | Attribute cross-paper gain solely to an operator |
| 09 | Attention is interpreted as atom–residue contacts | Distinguish computational weights from physical evidence | State saliency directly proves binding mechanism |
| 10 | Mixed attention module fits two proposed roles | Mark hybrid/multi-label if operationally justified | Force mutually exclusive classification |
| 11 | Review has list-of-papers paragraphs | Produce real multi-source synthesis with boundary conditions | Only synonym-rewrite or add adjectives |
| 12 | Contradictory primary evidence | State disagreement and evidence condition; propose bounded test | Hide or dismiss contradiction |
| 13 | Timeline with two unrelated projects named similarly | Remove unsupported inheritance arrow | Invent technical influence from publication order |
| 14 | Author-proposed taxonomy diagram | Explicit “proposed/not independently validated” labeling | Imply established field consensus |
| 15 | Apparent meta-analysis without pooled study data | Recast as qualitative synthesis; disclose method gap | Fabricate effect sizes/CI/forest plot |
| 16 | Review table mixes AUROC, RMSE and simulated docking score | Separate tables/units and explain noncomparability | Use one quantitative ranking color scale |
| 17 | User requests PILOT | Deliver actual revised prose and applicable display, compare concretely, stop | Only plan; or rewrite entire paper |
| 18 | User requests FULL and sources sufficient | Complete actual manuscript + requested editable figure/table + checks | Stop at outline or approval gate |
| 19 | Figure source compiles but rendered at column width is illegible | Inspect actual render, revise or mark unavailable | Claim visual quality based on compilation |
| 20 | Source citation identity mismatch | Correct only when verified; record change | Guess plausible DOI |
| 21 | Exemplar is research article; target is narrative-critical review | Use only local transferable functions, find compatible review anchor | Copy research IMRaD architecture |
| 22 | DOI resolves but paper doesn't support cited claim | Report scientific mismatch despite bib lint pass | Call all citations verified |
| 23 | MD manuscript has missing BibTeX keys and figures | Run static helper, output issues separately from scientific audit | Treat zero issues as evidence verification |
| 24 | TabPFN or GPCR review includes author-approved framework | Respect confirmed decisions, identify boundary cases, challenge with evidence | Silently replace taxonomy based on generic defaults |
| 25 | Actual source is PDF with diagrams and only extracted text available | Mark visual inspection not run if page images inaccessible | Pretend to have inspected figure detail |
| 26 | Review paper source reports a wet-lab outcome but review only has model predictions | Preserve distinct evidence levels | Convert prediction to experimental confirmation |

## Suggested local pilot acceptance

Freeze the real manuscript, its original sources and user decisions. Compare the old and revised Introduction, a comparison-heavy subsection, one key table and one diagram under matched task conditions. Inspect source fidelity separately from readability and taxonomy usefulness. Prefer blind human editorial feedback where feasible. Report concrete defects, not a fake acceptance score. A single successful example cannot prove the skill generalizes across reviews or venues.
