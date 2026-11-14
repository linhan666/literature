# Slide archetypes

The bundled renderer supports these types. Codex may build additional custom types when warranted by data.

| Type | When to use | Required structure | Avoid |
|---|---|---|---|
| `cover` | Open a talk | topic + subtitle + author/date | stock microscopes |
| `section` | Major transition | one large section message | generic "Part II" alone |
| `cards` | Three-part framework / research questions | 2–4 concise cards | fake KPI numerics |
| `kpis` | Executive scientific takeaway | big numeric values with exact conditions | unqualified success claims |
| `pipeline` | Datasets → model → evaluation | 3–6 meaningful blocks and arrows | implying absent causal links |
| `bar_chart` | Compare a few matched categories | axis + direct values + context | 3D bars / inconsistent axes |
| `line_chart` | Trend across ordered x-axis | labeled series, x/y, direct context | fabricated interpolation |
| `metric_table` | Exact side-by-side lookup | short rows + metric units | 20-row appendix tables |
| `comparison` | Controlled variant contrast | parallel strengths/limits | qualitative "wins" without data |
| `image_panel` | Source figures / molecular structures | uncropped/undistorted images + captions | placeholder screenshot |
| `findings` | Evidence synthesis and caveats | max 3 observations | claims beyond supplied findings |
| `roadmap` | Proposed follow-up experiments | ranked steps and test criteria | vague "future work" |
| `closing` | Final decision or headline | one finding + 2–3 concise messages | new evidence |

## Two important distinctions

**Key result vs raw result:** a bar chart is not a finding until the title says what the fair comparison actually shows. **Credible vs visually shiny:** editorial typography + restrained shape language + faithful figures beat random gradients, fake 3D models, and logo-heavy decoration.

## Layout sanity rules

- A single dominant chart/image should occupy 55–70% of usable slide width.
- At most 4 KPI cards, 6 pipeline nodes, 7 visible table data rows, 3 scientific images, or 3 summary findings on one slide.
- Never allow caption/legend to sit below the safe bottom margin.
- Move source identifiers to the bottom; full references can live in notes/appendix.
- Always preserve whitespace around arrows and dense structures.
