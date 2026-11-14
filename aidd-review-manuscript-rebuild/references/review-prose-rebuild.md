# Rewriting AIDD review prose: synthesis-first, evidence-bound

## Keep the review question visible

For each section, answer:
- What reader question does this section resolve?
- What are the two or three central propositions, not just headings?
- Which cited original studies directly support them, and under what constraints?
- What contrary cases or limitations change their meaning?
- What does the reader learn to *distinguish or decide* after this section?

Build a section map before rewriting thousands of words. Don't expand a thin chapter with unfounded literature just to make lengths look balanced. Move background definitions to first use; trim repeated general AI hype. A technical survey needs enough formulas or computational descriptions to discriminate methods; a critical narrative needs a defensible chain of reasoning, not a lexicon of architectures.

## Paragraph-level operations

1. **Claim:** begin with a bounded analytical proposition, not a list of titles.
2. **Evidence:** cite original methods/results tied to the proposition; name the actual task/evaluation regime when material.
3. **Compare:** distinguish the exact operation or validity condition, not merely “novel” or “state of the art.”
4. **Qualify:** explain uncertainty, negative evidence or incompatibility when it alters the conclusion.
5. **Advance:** connect to the next question or an experimentally testable distinction.

Use these as *functions*, not a mandatory five-sentence template. A definition paragraph may be short; a balanced conflicting-evidence discussion may be long. Avoid empty transition sentences, metadiscourse such as “It is worth mentioning,” and strings of architecture names without reader value.

## Before → after, without inventing evidence

**Inventory-only (problematic):**
“Study A uses cross-attention. Study B uses bilinear attention. Study C uses a GNN. These methods show the importance of attention.”

**Evidence-bounded rebuild (schematic, use real source citations in a manuscript):**
“Across the examined methods, the important distinction is not whether an attention layer is present but **how drug and protein features are coupled**. In Study A, attention weights control [source-verified operation], whereas Study B uses them for [different verified operation]. These two roles can coexist in hybrid modules and therefore should not be treated as mutually exclusive model families. The reported predictive gains do not isolate the contribution of either role because [specific unmatched condition]. A matched module-swap experiment would more directly test that question.”

All bracketed details must come from inspected originals; no fictional Study A/B citation should enter the actual manuscript. Do not replace concrete reported architectures with vagueness.

## Rebuild key sections by function

- **Title/abstract:** scope and contribution, not unsupported novelty. For a framework proposal say *propose*, for a verified synthesis say *synthesize*, for a systematic result report only executed methods.
- **Introduction:** define decision/problem → why existing reviews are insufficient *for that specific dimension* → promised analytical lens → bounded contribution and roadmap. Do not imply prior reviews are poor without evidence.
- **Foundations:** define endpoints, input modalities, methods and evaluation units needed later; distinguish terms like attention weights, contacts, binding activity, efficacy and causality.
- **Classification:** operational definitions, decision rules, informative examples/counterexamples, overlaps, caveats. Prefer explanatory figure plus precise table over repeated prose.
- **Comparative sections:** core mechanism, evidence type, matched/confounded comparisons, boundary conditions, implications for model choice/research.
- **Controversies:** competing interpretations and evidence gaps, not fake debates or balanced coverage when support is asymmetric.
- **Future directions:** prioritized questions with falsifiable controls and relevant data requirements, not generic “more benchmarks and interpretability.”
- **Conclusion:** bounded results of review, no new source claims, acknowledge non-independently validated proposed frameworks.

## Citation and voice handling

`Source-reported result` → “The authors reported ...”

`Review inference` → “Taken together, these studies suggest ... under [condition] ...”

`Author proposition` → “Here we distinguish ... as a proposed operational taxonomy.”

`Future hypothesis` → “One testable hypothesis is ...; this has not been evaluated in the cited evidence.”

Avoid “demonstrated” for an unreplicated proxy task if “reported” or “suggested” is more accurate. Conversely don't erase genuine robust experimental evidence by generic hedging. Cite at the sentence/proposition where it is used. Keep technical terms, symbols, data split names, units, terminology and lineages consistent.

## Bounded revision review

For each substantial paragraph rewrite verify: (a) meaning preserved or explicitly corrected, (b) cited sources support wording, (c) evidence vs inference visible, (d) stronger thread to previous/next paragraph, (e) no duplicative general claim. Revisit structure when iterations only swap adjectives. No bibliography-shaped prose.
