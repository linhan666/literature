# Synthetic same-facts rewrite example

**Everything in the following study is fictional, provided solely to illustrate editing. These are not user results, not a published benchmark, and not values to insert into a manuscript.**

## Locked teaching facts

The hypothetical study compares a graph-feature predictor with the same head using concatenated precomputed graph and SMILES features. Four fictional binary endpoints use one fixed scaffold split each. Each configuration has one fitted model per endpoint. No uncertainty, mechanistic analysis, or prospective experiment is available.

| Fictional endpoint | Graph features: test ROC-AUC | Concatenated features: test ROC-AUC |
|---|---:|---:|
| A | 0.780 | 0.802 |
| B | 0.741 | 0.768 |
| C | 0.816 | 0.824 |
| D | 0.803 | 0.799 |

## Weak report-style paragraph

> We evaluated the two configurations on four endpoints using scaffold splits. The ROC-AUC values for graph features were 0.780, 0.741, 0.816, and 0.803, while the values for concatenated features were 0.802, 0.768, 0.824, and 0.799. The concatenated model was higher on three endpoints and lower on one endpoint. Only one model per configuration was fitted for each endpoint, and uncertainty was not measured.

This paragraph is not scientifically false. Its weakness is that it reproduces the table rather than making the comparison easier to interpret.

## Revised paragraph using the same facts

> Adding SMILES features increased test ROC-AUC on three of the four scaffold-split endpoints (Table X). The largest difference was on endpoint B, from 0.741 to 0.768; endpoint D instead decreased from 0.803 to 0.799. Thus, concatenation improved prediction on most of the evaluated endpoints, but the benefit was not uniform. These single-model comparisons do not establish whether the differences persist across retraining or alternative splits.

## Why the revision differs

It leads with the observed pattern, uses a selected contrast to show magnitude and an exception, leaves complete lookup values in the table, and identifies the specific unmeasured variability. It does not assert that fusion captured chemical mechanisms, improved all endpoints, or achieved significance.

The last sentence should not become a formula appended to every paragraph. Its placement depends on what the surrounding Methods and limitations already report.

## A visual-design decision from these same facts

A main table can preserve complete values. A separate paired-difference plot is justified only if examining variation across endpoints is important to the narrative; otherwise it duplicates the table. No error bars can be generated from these facts. A diagram should show actual precomputed feature branches and concatenation, not an invented attention or alignment module.

This is a design example, not a rendered figure. An actual pilot must generate and inspect the requested display before claiming visual improvement.

## A generic method sentence: change the information, not only the vocabulary

Weak: “Our framework synergistically integrates multiple representations through an effective fusion module.”

Same hypothetical mechanism, more explicit: “We concatenate the precomputed graph and SMILES feature vectors and feed the combined vector to the same prediction head used in the graph-only comparison.”

The second sentence is not inherently sufficient as a contribution. It simply tells the reader what the model does. Any motivation, novelty, or benefit still needs separate support.
