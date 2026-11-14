# Research presentation storyboard

## The causal spine

The speaker needs to answer, in order: Why does this matter? What was attempted? How was the experiment made fair? What actually happened? How robust is that? Where did it fail? What decision or experiment follows?

A 12-minute group-meeting talk typically benefits from 10-12 slides: 1 question/title; 2 motivation + research gap; 3 objective or hypothesis; 4 data and split protocol; 5 method architecture; 6 headline benchmark; 7 matched comparison or ablation; 8 robustness/heterogeneity; 9 error analysis or examples; 10 constraints/threats to validity; 11 next-experiment prioritization; 12 conclusion. Do not fill an unneeded slot; integrate setup if the audience knows it.

The **title of a results slide must state a supported takeaway**, e.g., "Ablating cross-attention reduced mean AUROC on the matched test sets" rather than "Ablation Study". If statistical uncertainty is unknown, avoid "significantly" and qualitative certainty unsupported by the data.

## Slide object contract

Recommended `slide_plan.json` object:

```json
{
  "title": "Experiment title",
  "subtitle": "What was tested and why",
  "author": "Team or researcher",
  "language": "zh-CN",
  "theme": "lab-light",
  "disclaimer": "Only for explicitly illustrative figures",
  "slides": [
    {"id":"S01","type":"cover","title":"Research talk title","subtitle":"...","sources":[]},
    {"id":"S02","type":"pipeline","title":"The experiment separates target leakage from chemistry generalization","steps":[{"label":"Data audit","detail":"Remove duplicate pairs"}],"sources":["F01"]}
  ]
}
```

Every source-backed slide: `id`, `type`, `title`, `sources`; add a `takeaway`, `speaker_notes`, and `citation` if useful. `sources` should be IDs in `evidence_ledger.csv`; do not put an invented DOI or source there.

## Visual selection by scientific question

- "What changed?" → before–after, side-by-side comparison, signed delta chart.
- "Which method is better?" → matched dot plot/grouped bar with consistent scales; table only if precise lookup matters.
- "Does improvement generalize?" → splits/folds/datasets small multiples or per-group distribution.
- "How does it work?" → pipeline with information-flow arrows and annotated data/feature boundaries.
- "Why might it work?" → mechanistic hypothesis clearly marked as inference rather than demonstrated causality.
- "What failed?" → representative examples and error taxonomy, with selection criteria and counts.
- "What next?" → prioritized experiments, measurable success criteria, cost/risk.

## Prioritization

Trim upstream literature review before trimming actual results; display methods required to interpret evaluation; move implementation details and extra benchmarks into appendix. For a PI meeting, conclude with a decision or concrete experiment request. For a conference, keep the main result prominent and visual. For a defense, make data/splits/validation more explicit.
