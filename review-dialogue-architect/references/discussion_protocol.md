# Scientific dialogue protocol (adaptive, not a rigid questionnaire)

## Why the dialogue exists

A review theme plus initial objectives is **not** yet a publishable intellectual architecture. The task is to expose ambiguities, test relationships among concepts, elicit authorial preferences, construct alternative arguments, and preserve what must be verified from actual publications.

This is a **co-reasoning method**, not an automatically valid literature-review protocol. Conversation rounds are not a substitute for searching and reading the literature. The user remains the scientific decision-maker.

## Work from established context

Read the exact current message, attached `topic.md` and any discussion transcript/summary first. Preserve previously user-confirmed positions. If an earlier answer is available in the current context, do not ask it again. If a chat excerpt is missing, mark the gap and move on with a tentative interpretation. Never claim to have read earlier chats or files that the environment has not provided.

At the start:

1. State the topic in faithful terms and the user's stated goals.
2. Distinguish a working title from an agreed research question.
3. Identify one intellectual ambiguity that most changes the review's direction.
4. Offer an initial critical assessment or concrete candidate taxonomy, not just a request for more input.
5. Ask **at most one high-value clarification question by default**, unless the user explicitly requests a batch of questions.

## Rounds, checkpoints, and decisions

### Round A — Scope and definitions

Clarify the primary phenomenon, epistemic objective (explain mechanisms / compare models / map evidence / synthesize benchmarks), the intended scholarly readership, and exclusions. Distinguish *reviewing a phenomenon* from *reviewing methods applied to that phenomenon*. Identify what the title promises that the paper must deliver.

**Checkpoint example:** “The current proposal excludes purely unimodal attention and focuses on explicit inter-molecular coupling. Is that a firm scope boundary?” Ask only if it genuinely affects the classification.

### Round B — Alternative organizing models

Propose useful alternatives, e.g. (i) modality and interaction operator, (ii) physical supervision and observability, (iii) task and evaluation reliability. Explain what each illuminates and what each obscures. Do not presume five method names are all sibling categories; find parent/child or cross-cutting relationships. For each major group, supply one borderline case that tests the definition.

**Checkpoint:** Recommend a framework and ask for acceptance only if the choice genuinely determines the outline. Accept hybrid/multi-axis frames when a single hierarchy is misleading.

### Round C — Critical confrontation

Challenge popular claims and the user's favorite options as well as your own. Ask: “What observation would disprove this?” “What is the alternative explanation?” “Can two methods really be compared from their published numbers?” “What evidence would a skeptical reviewer ask for?” “Is this called a research gap only because of a missing literature search?” Do not fabricate a paper as the alleged counterexample.

### Round D — Convergence

Turn discussion into 3–6 major research questions, 2–4 contribution hypotheses, a prioritized evidence-verification queue, and a proposed flow of conceptual argument. Note which scientific claims are exploratory versus verified. Suggest figure/table types that actually advance argument (taxonomy schematic, assumption matrix, benchmark reproducibility matrix, failure mode map), rather than illustrations for decoration.

### Round E — Handoff

Export exactly when the user requests, ends the session, or asks to move downstream. No minimum round count is mandatory. With no genuine user feedback, mark `stage: provisional`. With substantive real dialogue and actual user-confirmed decisions, mark `dialogue-complete` while still recording literature verification status separately.

## Example turn pattern

**Analytical response:** “You currently group bilinear attention, co-attention and contact-map prediction together. The first two name fusion operators; the last names a supervised prediction output. That mixes different classification levels.”

**Reasoned repair:** “Use two axes: interaction operator and physical supervision. Contact-map prediction can become a task or supervision dimension, not a direct sibling of co-attention.”

**Consequential tradeoff:** “A two-axis frame improves conceptual orthogonality but complicates a one-dimensional paper outline. Use primary chapters by scientific question, with a matrix for operator families.”

**Discriminating question:** “Should the review's central contribution be a new model taxonomy, or the reliability of interpreting learned interactions as physical contacts?”

The model must not write an imaginary answer from the user to that question. If unanswered, record two alternative plans.

## What counts as high-quality discussion

- Reasoning advances beyond reiteration; claims have conditions of validity.
- User and agent propositions retain attribution.
- At least one serious competing perspective is considered, without false equivalence.
- Proposed novelty is a **hypothesis pending verification of existing reviews**.
- Scope and evidence requirements are concrete enough for a new assistant to continue.
- Decisions are recorded with confirmations, not inferred from silence.

## Practical state record

Store after major decisions if writable workspace exists:

```markdown
# Session state (not the final handoff)

## User-given and user-confirmed positions
- USER_GIVEN: ... (from actual messages)
- USER_CONFIRMED: ... (explicit confirmation)

## Current provisional recommendations
- ASSISTANT_PROPOSED: ... (reason and competing option)

## Disputes and unresolved questions
- OPEN: ... (consequences)
- DISPUTED: ... (alternative A vs B)

## Version changes
- Earlier: ... / Current: ... / Trigger: actual user message or new evidence

## Evidence status
- BACKGROUND_UNVERIFIED / SOURCE_LOCATED / SOURCE_CHECKED (with real link and locator)
```

If no files can be written, keep the record in the conversation and reproduce it accurately at export.
