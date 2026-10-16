# 03 — From a recovered study to original English prose

## A paper is not a translation of the notebook

The notes preserve the research record and the author’s intentions. They need not supply the final order, motivation, or section boundaries. Construct a reader path independently while preserving all material facts, uncertainties, and unfavorable findings.

Write a one-sentence thesis answering: what predictive task, what implemented response, what empirical evidence, and what scope? Separate technical novelty, empirical contribution, and application value. A contribution may be an evaluation or a bounded finding rather than a new architecture.

## Choose the argument before the title

Make a contribution map: problem → response → evidence → counterevidence → allowed conclusion. Consider up to two or three alternatives only when genuinely useful. Describe why the selected framing fits the author’s objective and frozen evidence. Do not select a fashionable frame requiring experiments that were never run.

If the author says “mechanism,” “universality,” or “breakthrough,” translate the intention into a testable claim and check its support. Missing support should narrow wording or become a clearly labeled future question, not a hidden change in the author’s study. Respect an explicit decision to emphasize a particular valid result, without suppressing contrary evidence.

Do not retroactively narrate a perfectly linear discovery history. It is acceptable to explain a design rationale after experiments; it is not acceptable to claim that a post hoc interpretation was a prospectively registered hypothesis.

## Build paragraph packets

Use [the packet template](../assets/paragraph-packet.md), or put compact entries in `blueprint.md`:
`destination; reader question; central proposition; required facts/citations; local exemplar card; relevant display; notation; inference limit; preceding/following logic`.

Not every sentence needs a ledger row. Trace material assertions, ambiguous interpretations, and important numerical claims. Do not produce enough paperwork to displace actual writing.

## Drafting order and section work

Draft concrete technical content and results before finalizing the introduction, abstract, or title. Adjust for a section-only request. Match the actual venue’s structure, not a mandatory IMRaD or conference template.

### Task and Methods

Define the prediction sample, inputs, output/label space, notation, training objective, and inference function. Use actual implementation details when known. Distinguish dataset construction, features/pretraining, architecture, optimization/model selection, and evaluation.

Explain a contribution-bearing operation with sufficient detail for its reader purpose. Expand the actual interaction or objective, not just its acronym. Conventional background components can be abbreviated. Equations must map to real operations; an elegant equation cannot substitute for missing information or imply an unsupported mechanism. Unknown constructor defaults are not historical training settings.

When only a high-level author description exists, write a high-level author-reported Methods draft and localize essential missing specifics. Do not invent batch size, optimizer, learning rate, checkpoint identity, frozen status, or split construction.

### Results

Start from the question a comparison answers. State the observed pattern, give the minimum comparison context, use a few representative values, then delimit the interpretation. Let a table carry the full results. Some paragraphs establish setup or exceptions rather than following a rigid five-step pattern.

Report negative/null findings. Do not say “consistently outperforms” when the ordering varies. A matched ablation can support a conditional performance attribution but not an unrestricted causal or biological conclusion. An absent ablation cannot be supplied by rhetoric.

Keep measured gains on their original scale. Use “numerically higher” or an equivalent bounded description when uncertainty is unavailable; do not imply that every numeric difference is meaningful. Different test sets or prevalence may prohibit the proposed comparison.

### Introduction

Introduce the specific computational problem early. Include only the drug-discovery context needed to understand it. State a real, sourced limitation or motivating question, then connect the implemented idea to it. End with contributions supported by the actual evidence.

Do not invent what “all existing methods” fail to do. A first draft can include `[[CITATION_NEEDED:...]]` for a required unverified external proposition, but it cannot disguise that placeholder as a real citation. Avoid a long generic importance paragraph followed by a shopping list of modules.

### Related Work

Organize verified close work by task, representation, learning mechanism, evaluation, or other relevant distinctions. Distinguish methodological overlap from genuine difference without straw-man criticisms. Search primary papers and verify the cited proposition, not just bibliographic existence. A claimed “first” requires scoped, current evidence and remains cautiously worded.

### Discussion and limitations

Explain what the results establish and leave open. Discuss plausible alternatives, data/protocol boundaries, untested transfer, label limitations, and actual computational tradeoffs. Distinguish predictive utility from therapeutic efficacy, physical binding evidence, or prospective validation. Do not pad limitations with generic disclaimers while hiding the study’s real constraint.

### Abstract and title

Finalize last. Include the precise problem, idea, evaluation setting, supported key finding, and bounded implication at the required length. Do not put stronger claims here than in Results. Choose a descriptive title; do not inflate it with “causal,” “universal,” “interpretable,” or “foundation” without support. No fake citations or result placeholders belong in a purported submission-ready abstract.

## Chinese-to-English semantic control

Keep Chinese source concepts and stable English technical terms in a small glossary. Preserve units, negation, chronology, and uncertainty. Avoid turning “探索” into “demonstrate,” “可能相关” into “causes,” or “效果更好” into “significantly superior.” Use terms appropriate to the actual endpoint, not a generic translation of “activity.”

Write direct sentences with identified objects and operations. “We integrate complementary representations” needs a specified integration operation and evidence for complementarity. Explain what is actually combined and tested instead of replacing vague words with more technical-sounding ones.

After drafting, back-check critical English claims against normalized source propositions, not through a full literal back-translation. Detect additions, omissions, and strength changes. Repeated claims and repeated motivation should be removed or assigned different functions.

## Local comparison and continuation

Reopen the appropriate transfer cards when reviewing a section. Point to concrete passages where the intended organizational choice was or was not implemented. Rewrite failed paragraph purposes before polishing individual synonyms. A source-faithful but flat paragraph still needs editorial work; an elegant but unsupported paragraph must be corrected or removed.

Do not stop a full-paper request after completing packets or a pilot. Save progress and deliver the actual current draft even when some scientific details remain explicitly unresolved.
