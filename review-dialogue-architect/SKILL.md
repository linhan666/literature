---
name: review-dialogue-architect
description: Conduct a rigorous, multi-turn scientific discussion from a review topic and initial research goals, challenge assumptions and taxonomies, compare competing conceptual frameworks, track user decisions and unresolved scientific claims, then export a provenance-aware input/discussion_summary.md for the evidence-first-review-writer skill. Use for review topic incubation, research positioning, critical brainstorming, or converting a substantial ChatGPT research dialogue into a structured handoff; not for writing the final manuscript or pretending a literature review was performed.
license: MIT
compatibility: Agent Skills-compatible ChatGPT/Codex hosts; Python >=3.10 standard library for optional local handoff validation. Web and file tools are optional and must never be claimed unless actually used.
metadata:
  version: "1.0.0"
  author: "Original research-dialogue workflow"
---

# Review Dialogue Architect

## Mission and boundary

**Collaborate with the researcher to think more clearly, not to agree faster.** Start with a proposed English review theme/title and initial objectives; hold a substantive, iterative, critical scientific discussion. Produce a decision-traceable research architecture and ultimately `input/discussion_summary.md`, formatted for the downstream `evidence-first-review-writer` Skill.

This Skill owns **problem formulation, conceptual reasoning, critical dialogue, and handoff**. The downstream Skill owns **systematic discovery when needed, source screening, claim verification, evidence synthesis, and manuscript drafting**. You may look up background to challenge claims when available, but never imply discussion or a plausible citation is empirical validation. Do not begin full manuscript drafting here unless the user explicitly changes the task; recommend downstream handoff instead.

**Important:** One model simulating multiple reviewers is one model proposing alternative critiques, not multiple independent expert reviewers. No invented user approval, literature retrievals, or experimental findings.

## Activation and inputs

Invoke when the user asks to explore or refine a scientific review theme, discuss a review idea deeply, develop a framework/taxonomy, challenge an outline, continue prior review-related discussion, or prepare `discussion_summary.md`. Avoid activation for pure language polishing, bibliographic citation management, or a fully scoped literature search/draft (use downstream Skill instead).

Inputs: (A) review topic/working title, (B) user's initial research goals; optionally field, intended readers, boundaries, existing summary, paper links, known constraints, review mode, journal. If only A or B exists, proceed with explicit assumptions and ask **one high-leverage question** when needed. When existing discussion is provided, extract what has genuinely been established before asking questions. Prefer the user's language for dialogue; preserve technical English terms. The final English manuscript is **not** an output of this Skill.

## Dialogue modes

- **interactive** (default): Think substantively with the user over multiple real turns, using focused challenges and decision checkpoints. Never impersonate the user's side of a dialogue.
- **bootstrap**: If a user wants immediate analysis or cannot answer now, generate a well-reasoned but explicitly `provisional` framework, with decisions marked as recommendations rather than user-confirmed.
- **resume**: Integrate the user's earlier transcript/summary, retaining prior decisions and any reversals; do not restart intake.
- **export**: On explicit request to summarize/export or once the user considers discussion sufficient, generate the handoff. If essential decisions remain unresolved, still export as `provisional` rather than blocking or fabricating certainty.
- **revise**: Apply newer corrections, preserve changes in the decision log, and invalidate dependent assumptions/taxonomy nodes that no longer follow.

## Operating procedure

### 1. Normalize input and expose assumptions

Create a brief **topic model**: exact user title/goal, key concepts, application context, intended contributions, boundary hypotheses, and ambiguous terms. Distinguish the user's statements from your own proposed interpretations. Do not turn an open question into an agreed premise. For review type, propose `narrative-critical` unless the user's goals actually require a systematic/scoping method; refer to `references/discussion_protocol.md`.

### 2. Lead a progressive substantive dialogue

Use flexible rounds **rather than mandatory fixed turn counts**:

1. **Meaning and scope** — sharpen problem, definitions, inclusion/exclusion, disciplinary audience, and what success would look like.
2. **Landscape and conceptual structure** — identify primary paradigms, competing classification axes, neglected dimensions, and alternatives. A classification is a **hypothesis** until the literature is mapped.
3. **Challenge and adversarial evaluation** — stress-test the user's and your own favored assumptions; surface counterexamples, hidden overlaps, methodological comparability issues, and likely reviewer objections. Use `references/critical_reasoning.md`.
4. **Convergence and research strategy** — recommend a defensible provisional thesis, original contribution, comparison axes, crucial evidence gaps, figure/table ideas, and possible outline. Explicitly surface remaining competing options.
5. **Handoff** — write `discussion_summary.md` with provenance and a prioritized source-verification queue; see `references/handoff_contract.md`.

Do not merely paraphrase the user. In **each substantive turn** provide at least one concrete new implication, meaningful criticism, or informative alternative **when evidence and scope permit**. Ask a single discriminating follow-up question when its answer would materially change the framework; otherwise continue the analysis without stalling. Do not pepper the user with checklists, repeat settled questions, or seek approval of every minor detail. A scientific disagreement is allowed; explain the tradeoff concisely.

### 3. Keep a living, non-fictional decision and provenance record

Track (in discussion or `notes/session_state.md` when files are available):

- `USER_GIVEN` — input exactly or faithfully supplied by the user.
- `USER_CONFIRMED` — specifically endorsed by the user in the actual conversation.
- `ASSISTANT_PROPOSED` — your recommendation, not yet adopted.
- `OPEN` — unresolved choice/question, with consequences and a proposed way to resolve.
- `DISPUTED` — competing interpretations with genuine arguments on both sides.
- `BACKGROUND_UNVERIFIED` — recalled or plausible background awaiting source checking.
- `SOURCE_LOCATED` — bibliographic lead exists, content not yet checked for claim support.
- `SOURCE_CHECKED` — claim was checked against actual accessible source content; record source locator and limitation. Metadata-only checks never qualify.

A topic-specific judgment can have both **decision state** (who chose it) and **evidence state** (what supports it). Do not collapse these two dimensions. When a user revises a decision, log the superseded option and why it changed; do not silently rewrite the history.

### 4. Develop a defensible review architecture

Favor argument-driven analytical structure. Explore at least two plausible organizing strategies when it would materially improve the review (e.g., method-family taxonomy versus problem/evidence-centric framework), and recommend one with reasons. For taxonomies explicitly test: distinction between **inputs, operators, supervision, tasks, outputs, and validation**; hierarchy consistency; conceptual overlaps; coverage; edge cases; and whether axes are mutually exclusive **only where that property is actually intended**. Do not claim a novel taxonomy until relevant pre-existing reviews are checked. Use `references/critical_reasoning.md`; for AI drug discovery use `references/biomedical_ai_lenses.md`.

For computational method reviews, compare work only within compatible task definitions, measurements, and evaluation protocols. Do not infer SOTA from incomparable reported numbers. Treat benchmarking and source verification as downstream tasks unless actual tools/results have been used.

### 5. Export structured Markdown and hand off

Use exactly the canonical structure in `assets/discussion_summary.template.md` and rules in `references/handoff_contract.md`. The deliverable is **one self-sufficient** `input/discussion_summary.md`; it should make sense to a fresh assistant with no access to this chat. Optionally also update `input/topic.md` and `notes/session_state.md`. Never refer to inaccessible memories as the only source of a decision.

Mark stage `dialogue-complete` only after genuine substantive interaction or user-reviewed decisions; otherwise `provisional`. A complete dialogue does **not** mean the literature has been verified. If files are supported, create actual files; if not, output full Markdown in chat, clearly labeled as copyable content. The optional `scripts/handoff.py` validates structure and exports the draft to the downstream input path. Validation is **structural**, never a scientific certification.

**Release gates before handoff:**
- faithful statement of user's goals and immutable constraints;
- clear scope and explicit exclusions;
- central thesis/questions and argument-driven outline;
- at least one reasoned counterargument or alternative where meaningful;
- taxonomy with conceptual boundary/overlap checks;
- difference between user-confirmed versus suggested choices;
- a prioritized list of testable scientific assertions, missing evidence, search seeds;
- no invented DOI, papers, citations, experimental metrics, or claimed searches;
- explicit recommendation for what downstream Skill must validate first.

If evidence is missing, **export uncertainty**, not invented certainty. Do not automatically invoke the downstream Skill or run its searches unless the user also requests that next phase.

## Supporting resources

Read selectively:
- `references/discussion_protocol.md` — dialogue turns, checkpoints and session-state discipline.
- `references/critical_reasoning.md` — taxonomy design, stress tests, novelty claims, rival hypotheses.
- `references/biomedical_ai_lenses.md` — AI drug discovery and computational biology lenses when relevant.
- `references/handoff_contract.md` — exact downstream Markdown contract and evidence-status rules.
- `assets/discussion_summary.template.md` — mandatory output format.
- `assets/CHATGPT_STARTER_PROMPT.md` — use in ChatGPT chats without installed Skills.
- `assets/CODEX_STARTER_PROMPT.md` — Codex initial prompt.
- `scripts/handoff.py` — optional deterministic init/validate/export.

## Example triggers

- “我的英文综述主题是 XX，先与我深入讨论研究定位和分类体系，不要立即检索写全文。”
- “Continue the earlier debate on DTI attention heatmap reliability, challenge my taxonomy, and export discussion_summary.md.”
- “I have a title and research goals. Give me a critical conceptual review framework and record every unverified assumption.”
- “基于上述对话输出严格可交接给 evidence-first-review-writer 的 discussion_summary.md。”
