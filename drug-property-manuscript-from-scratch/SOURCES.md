# Provenance and verification scope

## Official Codex packaging and use

Checked on **2026-10-16**:

- OpenAI, **Build skills**. Current resolved page: `https://learn.chatgpt.com/docs/build-skills`.
- Original Codex entry opened: `https://developers.openai.com/codex/skills/`; it redirected to the above page.
- Creation entry opened: `https://developers.openai.com/codex/skills/create-skill/`; it also redirected to the above page.

The relevant inspected sections describe SKILL.md with name/description, optional references/assets/agents metadata, progressive loading, local `.agents/skills` discovery, explicit `$skill-name` invocation, and `policy.allow_implicit_invocation` in agents/openai.yaml. The package uses those documented structures. No official approval or end-to-end compatibility test is claimed.

## Design provenance

The user's request is for an **additional, independent first-draft workflow** using Chinese notes or a rough author intent plus completed experiment data and figures. The preceding conversation's rebuild v2 was inspected, including its README and SKILL.md. Its exemplar-observation → concrete transfer → actual-output comparison concept is retained, while intake, argument construction, baseline comparison, and deliverables are redesigned for the absence of a full manuscript.

The scientific/editorial workflow, templates, and evaluation scenarios in this package are original task-specific design instructions, not empirically validated conclusions from a cited benchmark. The domain checklist is selective reporting guidance; the agent must check actual study records and appropriate primary sources rather than treating this document as evidence for a study claim.

## What was not done

No actual user manuscript, Chinese notes, experimental dataset, or scientific figure was supplied for this new first-draft task. No field-specific exemplar set was selected or analyzed for the unknown study. The examples are explicitly fictional; they are not excerpts from real papers and do not establish model performance or writing effectiveness. Source PDFs, publisher figures, font files, third-party writing skills, and external executable dependencies are not redistributed.

This is an instruction-only local skill package, not a trained model, autonomous research system, installed plugin, or publisher-endorsed tool. Runtime browsing, vision, plotting, and compilation depend on the user's actual environment and permissions.
