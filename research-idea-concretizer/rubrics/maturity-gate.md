# MRI Maturity Gate

This is a specification-completeness gate, not a paper-quality score.

A candidate passes only if every mandatory item is satisfied.

| Criterion | Pass condition | Common failure |
|---|---|---|
| Problem specificity | Bounded question with identifiable decision/outcome | “Improve drug discovery” |
| Gap clarity | Explicit deficiency/unknown with verification status | Gap asserted as fact without evidence |
| Falsifiable hypothesis | Plausible result could refute it | “Our method will be useful” |
| Causal fit | Method logically addresses the gap | Added complexity unrelated to bottleneck |
| Evaluation discriminability | Design can separate success from failure | Only qualitative showcase |
| Baseline adequacy | At least one credible simpler/current comparator | Comparison only to weak baseline |
| Contribution clarity | New knowledge/capability/resource is identifiable | “Build a platform” only |
| Assumption visibility | Critical assumptions are explicit | Hidden dependence on unavailable data |
| Portfolio distinctness | Not duplicate of another retained idea | Model/dataset swap only |

## Status rules

- **Mature:** all criteria pass.
- **Near-mature:** one or two criteria remain unresolved but are repairable without changing the core idea.
- **Deferred / needs evidence:** the core gap, evaluation, or feasibility cannot yet be specified credibly.
