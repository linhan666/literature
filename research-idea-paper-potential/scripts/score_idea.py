#!/usr/bin/env python3
"""Compute Paperability, High-Quality Potential, and optional Agent scores.

Usage:
    python scripts/score_idea.py evaluation.json

The input format is described in assets/evaluation-schema.json.
No third-party dependencies are required.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PAPERABILITY_WEIGHTS = {
    "problem_importance": 8,
    "knowledge_gap": 10,
    "novelty": 8,
    "claim_strength": 14,
    "mechanistic_insight": 6,
    "evidence_strength": 15,
    "alternative_explanations": 12,
    "generalizability": 5,
    "feasibility": 14,
    "reproducibility": 6,
    "narrative_coherence": 2,
}

HIGH_QUALITY_WEIGHTS = {
    "problem_importance": 15,
    "knowledge_gap": 10,
    "novelty": 15,
    "claim_strength": 12,
    "mechanistic_insight": 12,
    "evidence_strength": 12,
    "alternative_explanations": 8,
    "generalizability": 10,
    "feasibility": 3,
    "reproducibility": 2,
    "narrative_coherence": 1,
}

AGENT_WEIGHTS = {
    "necessity": 8,
    "scientific_autonomy": 10,
    "scientific_discovery_value": 12,
}


def validate_scores(scores: dict[str, float], expected: set[str]) -> None:
    missing = expected - scores.keys()
    extra = scores.keys() - expected
    if missing:
        raise ValueError(f"Missing score fields: {sorted(missing)}")
    if extra:
        raise ValueError(f"Unexpected score fields: {sorted(extra)}")
    for key, value in scores.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 5:
            raise ValueError(f"{key} must be a number between 0 and 5; got {value!r}")


def weighted_score(scores: dict[str, float], weights: dict[str, int]) -> float:
    return round(sum((scores[k] / 5.0) * w for k, w in weights.items()), 1)


def classify_paperability(score: float) -> str:
    if score < 50:
        return "Not ready"
    if score < 60:
        return "Research-shaped but weak/underspecified"
    if score < 70:
        return "Plausible paper candidate with significant risks"
    if score < 80:
        return "Defensible research-paper potential"
    if score < 90:
        return "Strong paper candidate"
    return "Unusually mature; re-check calibration and novelty"


def classify_quality(score: float) -> str:
    if score < 50:
        return "Low quality ceiling"
    if score < 65:
        return "Incremental or niche ceiling"
    if score < 75:
        return "Credible solid-paper ceiling"
    if score < 85:
        return "Strong high-quality-paper potential"
    if score <= 92:
        return "Very high potential if evidence survives reviewer attack"
    return "Exceptional on paper; aggressively verify prior art and overclaiming"


def classify_agent(score: float) -> str:
    if score <= 9:
        return "Mostly workflow automation; Agent positioning weak"
    if score <= 16:
        return "Useful agentic system; limited scientific autonomy/discovery"
    if score <= 22:
        return "Credible Scientific Agent contribution"
    if score <= 26:
        return "Strong Scientific Agent paper potential"
    return "Exceptional on paper; require strong ablation and prospective validation"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/score_idea.py evaluation.json", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"Invalid evaluation file: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("Invalid evaluation: top-level JSON value must be an object.", file=sys.stderr)
        return 1
    if "idea" in data and not isinstance(data["idea"], str):
        print("Invalid evaluation: 'idea' must be a string.", file=sys.stderr)
        return 1

    dims = data.get("dimensions")
    if not isinstance(dims, dict):
        print("Invalid evaluation: 'dimensions' must be an object.", file=sys.stderr)
        return 1
    try:
        validate_scores(dims, set(PAPERABILITY_WEIGHTS))
    except ValueError as exc:
        print(f"Invalid evaluation dimensions: {exc}", file=sys.stderr)
        return 1

    fatal_flaws = data.get("fatal_flaws", [])
    if not isinstance(fatal_flaws, list) or not all(
        isinstance(item, str) for item in fatal_flaws
    ):
        print("Invalid evaluation: 'fatal_flaws' must be an array of strings.", file=sys.stderr)
        return 1

    paperability = weighted_score(dims, PAPERABILITY_WEIGHTS)
    quality = weighted_score(dims, HIGH_QUALITY_WEIGHTS)

    output = {
        "idea": data.get("idea"),
        "paperability_score": paperability,
        "paperability_classification": classify_paperability(paperability),
        "high_quality_potential_score": quality,
        "high_quality_classification": classify_quality(quality),
        "fatal_flaws": fatal_flaws,
    }

    if "agent" in data:
        agent = data["agent"]
        if not isinstance(agent, dict):
            print("Invalid evaluation: 'agent' must be an object.", file=sys.stderr)
            return 1
        try:
            validate_scores(agent, set(AGENT_WEIGHTS))
        except ValueError as exc:
            print(f"Invalid Agent scores: {exc}", file=sys.stderr)
            return 1
        agent_score = weighted_score(agent, AGENT_WEIGHTS)
        output["agent_score"] = agent_score
        output["agent_classification"] = classify_agent(agent_score)
        output["agent_components"] = {
            key: round((agent[key] / 5.0) * weight, 1)
            for key, weight in AGENT_WEIGHTS.items()
        }

    if fatal_flaws:
        output["warning"] = (
            "Fatal flaws/gates are present. Do not interpret numeric scores as a Go decision "
            "until the gates are resolved."
        )

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
