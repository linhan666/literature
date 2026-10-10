#!/usr/bin/env python3
"""Validate a JSON research-idea candidate against the repository schema.

Usage:
    python scripts/validate_candidate.py candidate.json

Requires:
    pip install jsonschema
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit("Missing dependency: install with `pip install jsonschema`.") from exc


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_candidate.py candidate.json", file=sys.stderr)
        return 2

    candidate_path = Path(sys.argv[1])
    root = Path(__file__).resolve().parents[1]
    schema_path = root / "schemas" / "idea_candidate.schema.json"

    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)
    with candidate_path.open("r", encoding="utf-8") as f:
        candidate = json.load(f)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(candidate), key=lambda e: list(e.absolute_path))

    if errors:
        print(f"INVALID: {len(errors)} schema error(s)")
        for err in errors:
            path = ".".join(str(p) for p in err.absolute_path) or "<root>"
            print(f"- {path}: {err.message}")
        return 1

    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
