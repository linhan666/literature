#!/usr/bin/env python3
"""Initialize, structurally validate, and export a review dialogue handoff.

No external dependencies. This does NOT verify science, references, user consent,
external data, or the semantic accuracy of a discussion transcript.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "review-dialogue-handoff/v1"
REQUIRED_FIELDS = (
    "schema", "stage", "working_title", "dialogue_language",
    "review_type", "literature_status",
)
VALID = {
    "stage": {"provisional", "dialogue-complete"},
    "review_type": {"narrative-critical", "systematic", "scoping", "undecided"},
    "literature_status": {"not-searched", "discovery-only", "partially-checked"},
}
SECTIONS = (
    "Topic and original research goals",
    "Scope, exclusions, review type and audience",
    "Central thesis and research questions",
    "Concept map and proposed taxonomy",
    "Competing frameworks and critical debate",
    "Comparative evaluation dimensions",
    "Candidate scholarly contributions",
    "Proposed English review outline",
    "Planned figures and tables",
    "Candidate sources and evidence status",
    "Claim-verification backlog and search seeds",
    "Decision ledger and change history",
    "Open questions and prioritized next steps",
    "Downstream handoff brief (English)",
)
PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}|\[[A-Z][A-Z0-9 _/,.:()\-]{3,}\]")


def parse_header(content: str) -> tuple[dict[str, str], str, list[str]]:
    errors = []
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", content, re.DOTALL)
    if not match:
        return {}, content, ["Missing valid YAML frontmatter delimited by ---."]
    metadata = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"Malformed metadata line: {line!r}")
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        val = val.split(" #", 1)[0].strip().strip("\"'")
        if key in metadata:
            errors.append(f"Repeated metadata key: {key}")
        metadata[key] = val
    return metadata, match.group(2), errors


def validate(content: str) -> dict:
    meta, body, errors = parse_header(content)
    warnings = []
    for field in REQUIRED_FIELDS:
        if not meta.get(field):
            errors.append(f"Missing metadata: {field}")
    if meta.get("schema") and meta["schema"] != SCHEMA:
        errors.append(f"Unexpected schema {meta['schema']!r}; expected {SCHEMA!r}")
    for field, allowed in VALID.items():
        if meta.get(field) and meta[field] not in allowed:
            errors.append(f"Invalid {field}={meta[field]!r}; allowed: {', '.join(sorted(allowed))}")
    if meta.get("working_title", "").strip() in {"", "TBD", "Untitled"}:
        errors.append("Set a meaningful working_title.")
    if PLACEHOLDER_RE.search(content):
        found = PLACEHOLDER_RE.findall(content)[:4]
        errors.append(f"Unfilled template placeholders detected: {found}")
    for num, heading in enumerate(SECTIONS, start=1):
        expression = rf"(?m)^## {num}\. {re.escape(heading)}\s*$"
        occurrences = len(re.findall(expression, body))
        if occurrences != 1:
            errors.append(f"Require exactly one heading: ## {num}. {heading}; found {occurrences}")
    if "USER_GIVEN" not in body:
        warnings.append("No USER_GIVEN marker; confirm original objectives have been faithfully recorded.")
    if "ASSISTANT_PROPOSED" not in body:
        warnings.append("No ASSISTANT_PROPOSED marker; proposals may be misattributed as decisions.")
    if meta.get("stage") == "dialogue-complete" and "USER_CONFIRMED" not in body:
        warnings.append("Stage is dialogue-complete but no USER_CONFIRMED marker appears. Confirm that there was actual multi-turn interaction, or choose provisional.")
    if meta.get("literature_status") == "not-searched" and re.search(r"(?i)\b(search(?:es|ed)? (?:returned|identified|retrieved)|数据库检索获得)\s+\d+", body):
        warnings.append("Document claims a numeric search result although literature_status=not-searched; investigate.")
    if len(body.strip()) < 700:
        warnings.append("Summary body is very short; it may not be self-contained for the downstream reviewer.")
    return {
        "ok": not errors, "stage": meta.get("stage"),
        "literature_status": meta.get("literature_status"),
        "sections": len(SECTIONS), "errors": errors, "warnings": warnings,
        "note": "Structural check only; not a scientific, bibliographic or dialogue-provenance certification."
    }


def init_project(project: Path, force: bool = False) -> dict:
    project.mkdir(parents=True, exist_ok=True)
    files = {
        "input/topic.md": SKILL_ROOT / "assets/topic.template.md",
        "notes/session_state.md": SKILL_ROOT / "assets/session_state.template.md",
        "drafts/discussion_summary.md": SKILL_ROOT / "assets/discussion_summary.template.md",
    }
    created, skipped = [], []
    for rel, src in files.items():
        dest = project / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and not force:
            skipped.append(str(dest))
            continue
        shutil.copyfile(src, dest)
        created.append(str(dest))
    return {"created": created, "skipped_existing": skipped,
            "next_step": "Fill input/topic.md, discuss iteratively, and populate drafts/discussion_summary.md; then validate and export."}


def export(project: Path, source: Path | None, allow_provisional: bool, overwrite: bool) -> dict:
    source = source or project / "drafts/discussion_summary.md"
    if not source.is_file():
        raise ValueError(f"Draft missing: {source}")
    content = source.read_text(encoding="utf-8")
    result = validate(content)
    if not result["ok"]:
        raise ValueError("Validation failed:\n" + "\n".join(result["errors"]))
    if result["stage"] == "provisional" and not allow_provisional:
        raise ValueError("Draft is provisional; obtain actual author decisions or explicitly pass --allow-provisional.")
    target = project / "input/discussion_summary.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not overwrite:
        raise ValueError(f"Destination already exists: {target}; pass --overwrite if you intend replacement.")
    if source.resolve() != target.resolve():
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(target)
    return {"exported": str(target), "stage": result["stage"],
            "literature_status": result["literature_status"],
            "warnings": result["warnings"], "note": result["note"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    initialize = sub.add_parser("init", help="Create topic, state, and handoff draft templates")
    initialize.add_argument("--project", type=Path, required=True)
    initialize.add_argument("--force", action="store_true", help="Replace existing template files (use cautiously)")
    check = sub.add_parser("validate", help="Check handoff structure and metadata")
    check.add_argument("--file", type=Path, required=True)
    out = sub.add_parser("export", help="Copy validated draft to input/discussion_summary.md")
    out.add_argument("--project", type=Path, required=True)
    out.add_argument("--source", type=Path)
    out.add_argument("--allow-provisional", action="store_true")
    out.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init_project(args.project, force=args.force)
        elif args.command == "validate":
            if not args.file.is_file():
                raise ValueError(f"File not found: {args.file}")
            result = validate(args.file.read_text(encoding="utf-8"))
        else:
            result = export(args.project, args.source, args.allow_provisional, args.overwrite)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("ok", True) else 2
    except (OSError, ValueError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
