# Scientific slide design system

## Base canvas

- 13.333 × 7.5 in, ratio 16:9.
- Safe margin: 0.60 in horizontal, 0.42 top, 0.43 bottom. Content grid begins near y=1.44 in.
- Use 12-column alignment for custom layouts; align text, charts, images, and cards on common x/y edges.
- Limit to **2 typefaces**. Preferred: Aptos/Arial; Chinese: Microsoft YaHei/Noto Sans CJK SC. Test glyphs in renderer.
- Editorial headline: 29–35 pt, short and informative; content headings: 19–23 pt; body 18–22 pt; chart axes/legends: 13–17 pt; source footer: 9–11 pt. Avoid all-caps body copy.
- Line-spacing and padding must leave breathing room. Reduce content, not only font size, when it doesn't fit.

## Palette, lab-light

| Role | HEX | Usage |
|---|---|---|
| Ink | `#182B45` | titles / key claims |
| Muted Ink | `#607185` | captions / explanation |
| Background | `#FAFBFD` | content canvas |
| White | `#FFFFFF` | card surfaces |
| Teal | `#078B91` | study method / focal results |
| Amber | `#E8A23B` | competitor / comparison |
| Violet | `#7B67B4` | secondary conditions |
| Error | `#BD5757` | limitations / adverse results |
| Border | `#DEE6EF` | dividers, grids |
| Deep Navy | `#102139` | cover / section breaks |

Don't imply that a method is better solely through color; show the metric/delta. Use identical color mappings across slides. Light fills can use e.g. `#EDF8F7` for focus cards.

## Charts

- Quantitative charts must name metric, units, direction if nonobvious, dataset, and split/condition. Distinguish per-fold SD/SE/CI and sample counts.
- Prefer bars for a few independent categories, points/intervals for measured estimates, lines for ordered axes, heatmaps for a dense matrix, scatter for associations.
- For AUROC or AUPRC, either show the full 0–1 range or explicitly mark a nonzero baseline and restricted axis. Never conceal truncation. Avoid 3D charts.
- Label values directly when categories ≤ 6. Legends can be replaced by direct annotations. If space is tight, split crowded charts across slides.
- For imbalanced classification, include AUPRC and class prevalence when the inference depends on it. For DTI/DTA, state cold-target/scaffold/random split as applicable.
- Graphs must reproduce supplied metrics faithfully. No smoothing of empirical curves unless explicitly described. Never fake error bars.

## Scientific imagery

- Preserve residue IDs, molecular chirality, atom-color conventions, cryo-EM scale bars, unit labels, and scientific plot legends.
- Images from user sources may be cropped only if the cropped portion does not alter interpretation; never distort aspect ratio.
- Use at most two dense plots or scientific panels per slide. If the image contains small annotations, allocate a full slide or provide a faithful zoom inset from the source.
- Every figure needs a concise caption specifying dataset/experiment and its provenance.

## Visual rhythm

Mix 7-10 visual archetypes: dark cover; light framing slide; horizontal pipeline; clean 1-chart result; metric table; dark section marker; image inspection; annotated findings; ranked next steps; confident closing. Each layout should have a reason, not random variety.
