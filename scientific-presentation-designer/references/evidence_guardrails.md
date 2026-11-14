# Evidence integrity and reproducibility

## Source hierarchy

1. Original machine-readable result files and code-generated outputs for **numbers**.
2. Original figures and raw figure data for trends and distributions.
3. Experiment protocols and configuration for split/seed/hyperparameter details.
4. Research report text for interpretation.
5. Researcher's clearly marked scientific speculation for possible mechanisms and follow-up work.

If sources conflict, log the discrepancy and do not conceal it. If only a report summary exists, say "reported" rather than "independently verified". Do not search the web to fill a private experiment's missing measurements.

## Experimental comparison safety

Record: measured endpoint, metric and optimization direction; mean or individual run; dataset/split; sample n; target/compound leakage policy; seed/fold; baseline tuning; test vs validation vs training; comparability. A comparison is **matched** only if sources establish the relevant conditions. Otherwise use side-by-side reporting without causal or performance superiority claims.

Never generate or infer:

- significance levels, SD/CI, unseen folds, test sizes, class ratios, error bars, p-values;
- missing ablation numbers, model rankings, timing, speedups, runtime savings;
- molecular docking contacts, residue labels, or precise geometry from unlabeled figures;
- source paper citations, experimental replication, or independent verification.

When plotting change, compute the exact arithmetic from the source and state whether it is absolute difference (e.g. +0.023 AUROC) or relative percent (e.g. +2.3%). Do not conflate percent points with percent. Explain any axis truncation. For ligand/target datasets, make leakage concerns explicit, particularly sequence/scaffold homology and overlap.

## Evidence ledger

`id` is stable, e.g., R001 (result), M001 (method), F001 (figure), C001 (claim). In `source_location`, use a CSV row/column, Markdown heading, file range, report figure number, or code artifact. `exact_value` retains source precision. `verification_status` refers to **source-checking**, not independently re-running experiments. Add `slide_ids` when storyboard is fixed. Preserve original files and add a separate `derived_outputs/` folder for generated charts.

## Slide label policy

- Reported observation: "On the supplied test set, X reached ...".
- Derived observation: "Difference calculated from reported values: ...".
- Hypothesis: "Possible explanation (not experimentally tested): ...".
- Proposed experiment: "Next test: ...".
- Unknown: "Not reported / needs verification".

Synthetic demo plans must be labeled on the slide canvas as synthetic. Never treat sample JSON as actual results.
