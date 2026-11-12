#!/usr/bin/env python3
"""Optional deterministic tracker for Review Dialogue Architect v1.1.

The state is an *authored record* of the dialogue. It does not read or judge
conversations, detect semantic novelty, verify sources or establish consent.
The assistant/user must supply honest coverage and novelty annotations.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_REL = Path("notes/dialogue_state.json")
SCHEMA = "rda-dialogue-state/v1"
LEVELS = {"absent": 0, "proposed": 1, "examined": 2}
PHASES = {
    "P1-positioning": (
        "research_goals", "scope", "exclusions", "review_type_and_audience"
    ),
    "P2-frameworks": (
        "central_questions", "taxonomy", "taxonomy_boundaries", "competing_frameworks"
    ),
    "P3-critique": (
        "counterarguments", "fair_comparison", "claim_evidence_limits"
    ),
    "P4-convergence": (
        "contributions", "review_outline", "figures_and_tables", "verification_backlog"
    ),
}
COVERAGE = tuple(dict.fromkeys(x for values in PHASES.values() for x in values))
NOVELTY = ("substantial", "incremental", "none")
SEVERITIES = ("critical", "high", "medium", "low")


def new_state() -> dict:
    return {
        "schema": SCHEMA,
        "skill_version": "1.1.0",
        "budget": {"initial_target_min": 10, "initial_target_max": 12,
                   "target_min": 10, "target_max": 12, "extensions": []},
        "rounds": [],
        "coverage": {name: {"level": "absent", "note": ""} for name in COVERAGE},
        "issues": [],
        "last_updated_utc": None,
    }


def _state_path(project: Path) -> Path:
    return project / STATE_REL


def _save(project: Path, state: dict) -> None:
    dest = _state_path(project)
    dest.parent.mkdir(parents=True, exist_ok=True)
    state["last_updated_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    temp = dest.with_suffix(".json.tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(dest)


def load(project: Path) -> dict:
    path = _state_path(project)
    if not path.is_file():
        raise ValueError(f"State missing: {path}. Run 'init --project ...' first.")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError("State JSON is unreadable") from exc
    if state.get("schema") != SCHEMA:
        raise ValueError(f"Unexpected state schema; expected {SCHEMA}")
    if sorted(state.get("coverage", {})) != sorted(COVERAGE):
        raise ValueError("Coverage dimensions are missing or unexpected")
    for key, entry in state["coverage"].items():
        if not isinstance(entry, dict) or entry.get("level") not in LEVELS:
            raise ValueError(f"Invalid coverage level for {key}")
    return state


def initialize(project: Path, overwrite: bool = False) -> dict:
    target = _state_path(project)
    if target.exists() and not overwrite:
        return {"created": False, "path": str(target), "message": "Existing state retained"}
    _save(project, new_state())
    return {"created": True, "path": str(target)}


def record_round(project: Path, phase: str, novelty: str, user_input: str,
                 analysis: str, question: str = "") -> dict:
    if phase not in PHASES:
        raise ValueError(f"Unknown phase: {phase}")
    if novelty not in NOVELTY:
        raise ValueError(f"Unknown novelty: {novelty}")
    if not user_input.strip() or not analysis.strip():
        raise ValueError("A round needs a real user input description and assistant analysis")
    state = load(project)
    n = len(state["rounds"]) + 1
    state["rounds"].append({"round": n, "phase": phase, "novelty": novelty,
                            "user_input": user_input.strip(),
                            "analysis": analysis.strip(), "question": question.strip()})
    _save(project, state)
    return {"round": n, "phase": phase, "novelty": novelty, "note": "Self-reported, not transcript-verified"}


def set_coverage(project: Path, dimension: str, level: str, note: str) -> dict:
    if dimension not in COVERAGE:
        raise ValueError(f"Unknown coverage dimension: {dimension}. Known: {', '.join(COVERAGE)}")
    if level not in LEVELS:
        raise ValueError(f"Unknown level: {level}")
    if level != "absent" and not note.strip():
        raise ValueError("Evidence note required when a topic is proposed/examined")
    state = load(project)
    state["coverage"][dimension] = {"level": level, "note": note.strip()}
    _save(project, state)
    return {"dimension": dimension, "level": level, "note": note.strip()}


def raise_issue(project: Path, severity: str, description: str) -> dict:
    if severity not in SEVERITIES:
        raise ValueError(f"Invalid severity {severity}")
    if not description.strip():
        raise ValueError("Issue description must be nonempty")
    state = load(project)
    issue_id = f"ISS-{1 + max([int(x['id'].split('-')[-1]) for x in state['issues']], default=0):03d}"
    issue = {"id": issue_id, "severity": severity, "status": "open",
             "description": description.strip(), "resolution": ""}
    state["issues"].append(issue)
    _save(project, state)
    return issue


def resolve_issue(project: Path, issue_id: str, resolution: str) -> dict:
    if not resolution.strip():
        raise ValueError("Resolution or explicit downstream deferral required")
    state = load(project)
    for item in state["issues"]:
        if item["id"] == issue_id:
            if item["status"] == "closed":
                raise ValueError("Issue is already closed")
            item.update({"status": "closed", "resolution": resolution.strip()})
            _save(project, state)
            return item
    raise ValueError(f"Unknown issue: {issue_id}")


def extend(project: Path, reason: str, count: int = 3) -> dict:
    if not reason.strip():
        raise ValueError("A substantive extension reason is required")
    if not 1 <= count <= 10:
        raise ValueError("Extension must add between 1 and 10 rounds")
    state = load(project)
    state["budget"]["target_max"] += count
    state["budget"]["extensions"].append({"rounds_added": count,
                                            "reason": reason.strip(),
                                            "at_round": len(state["rounds"])})
    _save(project, state)
    return {"target_max": state["budget"]["target_max"], "reason": reason.strip()}


def assess(state: dict) -> dict:
    """Deterministic checks on self-reported state, not actual scientific truth."""
    rounds = state["rounds"]
    completed = {p: [dim for dim in dims if state["coverage"][dim]["level"] == "examined"]
                 for p, dims in PHASES.items()}
    phases = {
        p: {"ready_for_researcher_review": len(completed[p]) == len(dims),
            "examined": completed[p],
            "missing_or_only_proposed": [d for d in dims if d not in completed[p]]}
        for p, dims in PHASES.items()
    }
    stalled_three = len(rounds) >= 3 and all(r["novelty"] == "none" for r in rounds[-3:])
    critical = [i for i in state["issues"] if i["status"] == "open" and i["severity"] == "critical"]
    high = [i for i in state["issues"] if i["status"] == "open" and i["severity"] == "high"]
    all_phases = all(p["ready_for_researcher_review"] for p in phases.values())
    ready_to_offer = all_phases and not critical
    budget = state["budget"]
    if stalled_three and not ready_to_offer:
        suggestion = "Three self-rated non-novel exchanges: change analytical lens or seek counterevidence; do not mistake repetition for completion."
    elif ready_to_offer:
        suggestion = "Offer optional researcher review of the handoff. Never auto-export; author decides, regardless of round count."
    elif len(rounds) >= budget["target_max"]:
        suggestion = "Budget exceeded with unresolved gates: explain missing coverage and propose a justified extension (or a provisional handoff if the user requests)."
    elif len(rounds) >= budget["target_min"]:
        suggestion = "At target budget: prioritize unresolved gates; consider justified extension rather than a forced ending."
    else:
        suggestion = "Continue substantive dialogue, preferably addressing the earliest incomplete gate."
    return {
        "round_count": len(rounds),
        "target_round_range": [budget["target_min"], budget["target_max"]],
        "phase_gates": phases,
        "coverage": {key: value["level"] for key, value in state["coverage"].items()},
        "open_critical_issues": [x["id"] for x in critical],
        "open_high_issues": [x["id"] for x in high],
        "saturation_heuristic_triggered": stalled_three,
        "eligible_to_offer_final_review": ready_to_offer,
        "suggested_action": suggestion,
        "limitations": "Self-reported annotations only. Does not analyze transcripts, verify coverage, claim novelty, or certify user consent."
    }


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    commands = {}
    for c in ("init", "record", "coverage", "issue", "resolve", "extend", "status"):
        p = sub.add_parser(c)
        p.add_argument("--project", required=True, type=Path)
        commands[c] = p
    commands["init"].add_argument("--overwrite", action="store_true")
    commands["record"].add_argument("--phase", choices=PHASES, required=True)
    commands["record"].add_argument("--novelty", choices=NOVELTY, required=True)
    commands["record"].add_argument("--user-input", required=True)
    commands["record"].add_argument("--analysis", required=True)
    commands["record"].add_argument("--question", default="")
    commands["coverage"].add_argument("--dimension", choices=COVERAGE, required=True)
    commands["coverage"].add_argument("--level", choices=LEVELS, required=True)
    commands["coverage"].add_argument("--note", default="")
    commands["issue"].add_argument("--severity", choices=SEVERITIES, required=True)
    commands["issue"].add_argument("--description", required=True)
    commands["resolve"].add_argument("--id", required=True)
    commands["resolve"].add_argument("--resolution", required=True)
    commands["extend"].add_argument("--reason", required=True)
    commands["extend"].add_argument("--rounds", default=3, type=int)
    args = cli.parse_args(argv)
    try:
        if args.command == "init":
            result = initialize(args.project, args.overwrite)
        elif args.command == "record":
            result = record_round(args.project, args.phase, args.novelty,
                                  args.user_input, args.analysis, args.question)
        elif args.command == "coverage":
            result = set_coverage(args.project, args.dimension, args.level, args.note)
        elif args.command == "issue":
            result = raise_issue(args.project, args.severity, args.description)
        elif args.command == "resolve":
            result = resolve_issue(args.project, args.id, args.resolution)
        elif args.command == "extend":
            result = extend(args.project, args.reason, args.rounds)
        else:
            result = assess(load(args.project))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
