# Exemplar analysis: turn a paper into usable editorial decisions

## Select by function, not reputation alone

For each candidate, record title, stable identifier, version/date, source path/URL, article type, read scope, inspected pages/figures, and why it matches. Reject poor matches explicitly. A wet-lab discovery story is not automatically an appropriate structure for a method-only benchmark paper. A pretraining paper can illustrate a local explanation pattern without turning this study into pretraining research.

Use one primary whole-paper anchor when possible. Other papers supply local practices, not competing full outlines. In the absence of a venue, keep a provisional computational-research genre; do not invent a page limit. Reference count is not evidence of quality.

## Read in three passes

**Whole-paper pass.** Identify the central claim; question answered by each section; when the technical idea becomes concrete; which evidence earns main-text space; which details are deferred. Note an actual structural weakness as well as strengths. An accepted paper is not perfect.

**Local prose pass.** Read complete spans, including adjacent paragraphs. Assign roles to sentences, such as problem, prior capability, limitation, consequence, proposed principle, operation, observation, qualifier, interpretation, or transition. The roles explain the actual paragraph; they are not a fixed order to impose elsewhere.

Inspect opening subjects and information flow: what is familiar at the start of a sentence, what new concept arrives at its end, and how the next sentence uses it. Identify where technical nouns replace vague references, how definitions precede use, how numbers are selected, and how claims are qualified without drowning in boilerplate caveats.

**Visual pass.** View the figure/table itself, its caption, its page placement, and the paragraph using it. Determine the question, reading path, emphasis, grouping, scale, and visual vocabulary. Inspect page images, not just extracted text. Do not infer final figure size from screen pixels; distinguish final published layout from preprint layout.

## Required transfer-card form

```text
ID / intended function:
Source / version / exact locator:
Read/viewed scope:
Observed choice (concrete, paraphrased):
Why it may help this reader (editorial inference):
When transferable / when not:
Our relevant fact or display source:
Our proposed implementation location:
What will NOT be borrowed:
Verification question against the revised output:
```

A locator should remain retrievable: section + paragraph opening identifier or PDF page + figure/panel. Avoid lengthy source quotations. Sources provide writing examples, not permission to use their findings as this study's evidence.

### Invalid versus usable observations

| Invalid | Usable |
|---|---|
| “The introduction is logical.” | “The paragraph first names the capability of the closest approach, then identifies the exact unaddressed condition before introducing the new design.” |
| “The Results are concise.” | “The paragraph uses a selected comparison to explain one cross-dataset pattern; the full per-dataset values remain in its table.” |
| “The architecture is professional.” | “The central interaction is expanded, whereas the standard encoders remain compact; spatial emphasis tracks explanatory importance.” |
| “The table is clean.” | “The rows separate comparison regimes and the header identifies the evaluation context, reducing ambiguous cross-regime ranking.” |

These are examples of specificity, not claims that all good papers use those choices.

## Make the project-specific contract short

Record decisions for: opening problem, contribution framing, paragraph progression, method abstraction, Results selectivity, permissible claim strength, display hierarchy, visual semantics, and table grouping. Each decision needs a source card or a label `EDITORIAL_PROPOSAL`, plus a local verification question.

Do not copy exact sentence counts, page fractions, panel coordinates, palettes, unusual metaphors, or article-wide phrasing. A measured paragraph length or font size is a contextual observation. It becomes a constraint only if appropriate to the project and approved or required by the target format.

Do not flatten all exemplars into an “average style.” Resolve conflicts by target readership and evidence. When no suitable reference supports a decision, say so rather than pretending it is learned from a paper.

## Preserve grounding during writing

For a local rewrite, keep the selected card and source span accessible along with the study's locked facts. Before accepting the rewrite, reopen the card and check the stated function. Never treat having downloaded papers or generated summaries as completion of exemplar learning.
