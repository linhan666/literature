#!/usr/bin/env python3
"""Mechanical cross-reference checks for an AIDD review manuscript.

This tool does NOT verify source claims, DOI metadata, review methods,
scientific validity, or manuscript/figure quality. It supports Markdown/LaTeX
text and a BibTeX key list; it is deliberately dependency-free.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

BIB_ENTRY = re.compile(r"(?m)^\s*@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,")
TEX_CITATION = re.compile(
    r"\\(?:[A-Za-z]*cite[A-Za-z]*|parencite|textcite|autocite|footcite)\*?"
    r"(?:\[[^\]\n]*\]){0,2}\s*\{([^{}]+)\}",
    re.I,
)
MD_BRACKETS = re.compile(r"\[([^\]\n]{1,1000})\]")
MD_CITEKEY = re.compile(r"(?<![A-Za-z0-9])@([A-Za-z0-9_:.+\-]+)")
MD_IMAGE = re.compile(r"!\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)")
TEX_IMAGE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\s*\{([^{}]+)\}")
PLACEHOLDER = re.compile(
    r"\b(?:TODO|TBD|FIXME|VERIFY|PLACEHOLDER|INSERT\s+(?:FIGURE|TABLE)|CITATION\s+NEEDED)\b",
    re.I,
)
SUPPORTED = {".md", ".markdown", ".tex"}
IMAGE_SUFFIXES = (".pdf", ".png", ".jpg", ".jpeg", ".svg", ".eps", ".webp")


def hide_fenced_code(s: str) -> str:
    """Exclude fenced Markdown code from cross-reference counts, preserving lines."""
    rows: list[str] = []
    char = ""
    count = 0
    for line in s.splitlines(keepends=True):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if not char:
                char, count = token[0], len(token)
            elif token[0] == char and len(token) >= count:
                char, count = "", 0
            rows.append("\n" if line.endswith("\n") else "")
        elif char:
            rows.append("\n" if line.endswith("\n") else "")
        else:
            rows.append(line)
    return "".join(rows)


def extract_citekeys(manuscript: str) -> list[str]:
    results: list[str] = []
    for match in TEX_CITATION.finditer(manuscript):
        results.extend(x.strip() for x in match.group(1).split(",") if x.strip())
    for match in MD_BRACKETS.finditer(manuscript):
        content = match.group(1).lstrip()
        if content.startswith("@") or content.startswith("-@"):
            results.extend(MD_CITEKEY.findall(content))
    return results


def parse_bib(text: str) -> tuple[set[str], list[str]]:
    keys: set[str] = set()
    duplicates: list[str] = []
    for kind, key in BIB_ENTRY.findall(text):
        if kind.lower() in {"string", "comment", "preamble"}:
            continue
        if key in keys:
            duplicates.append(key)
        keys.add(key)
    return keys, sorted(set(duplicates))


def extract_local_images(manuscript: str) -> list[str]:
    paths = [x.strip("<>") for x in MD_IMAGE.findall(manuscript)]
    paths.extend(TEX_IMAGE.findall(manuscript))
    return paths


def issue(kind: str, severity: str, message: str, *, location: str = "") -> dict:
    return {"type": kind, "severity": severity, "message": message, "location": location}


def inspect(manuscript: Path, bib: Path | None = None) -> dict:
    report: dict = {
        "scope": "Mechanical checks ONLY. Does not verify DOIs, cited propositions, source versions, search conduct, figures' scientific correctness, or language quality.",
        "manuscript": str(manuscript),
        "bibliography": str(bib) if bib is not None else None,
        "issues": [],
        "not_checked": ["claim-to-source correspondence", "DOI and bibliographic identity", "literature review methodology", "visual and scientific correctness"],
    }
    issues: list[dict] = report["issues"]
    if manuscript.suffix.lower() not in SUPPORTED:
        issues.append(issue("UNSUPPORTED_FORMAT", "ERROR", "Only .md, .markdown and .tex are supported.", location=str(manuscript)))
        report["status"] = "STATIC_ISSUES_FOUND"
        return report
    if not manuscript.is_file():
        issues.append(issue("MISSING_MANUSCRIPT", "ERROR", "Manuscript file does not exist.", location=str(manuscript)))
        report["status"] = "STATIC_ISSUES_FOUND"
        return report

    raw = manuscript.read_text(encoding="utf-8-sig")
    cleaned = hide_fenced_code(raw) if manuscript.suffix.lower() != ".tex" else raw
    citekeys = extract_citekeys(cleaned)
    unique_cites = sorted(set(citekeys))
    report["citations_found"] = {"occurrences": len(citekeys), "unique_keys": len(unique_cites)}

    if bib is None:
        if unique_cites:
            issues.append(issue("BIB_NOT_PROVIDED", "WARNING", "Citation keys found but no --bib supplied; key resolution not checked."))
    elif not bib.is_file():
        issues.append(issue("MISSING_BIB_FILE", "ERROR", "Supplied BibTeX file is missing.", location=str(bib)))
    else:
        bibtext = bib.read_text(encoding="utf-8-sig")
        bibkeys, duplicates = parse_bib(bibtext)
        report["bibliography_entries"] = len(bibkeys)
        for key in duplicates:
            issues.append(issue("DUPLICATE_BIB_KEY", "ERROR", f"Duplicate BibTeX key: {key}", location=str(bib)))
        for key in unique_cites:
            if key not in bibkeys:
                issues.append(issue("MISSING_BIB_KEY", "ERROR", f"Unresolved citation key: {key}", location=str(manuscript)))
        report["unused_bib_entries"] = sorted(bibkeys - set(unique_cites))
        # Unused entries may be intentional; they are informational rather than failures.

    local_images = extract_local_images(cleaned)
    report["image_references_checked"] = len(local_images)
    for img in local_images:
        if img.startswith(("http://", "https://", "data:", "#")):
            continue
        # LaTeX macros and variable paths are not statically resolvable.
        if any(token in img for token in ("\\", "{", "}")):
            issues.append(issue("DYNAMIC_IMAGE_PATH", "WARNING", f"Cannot resolve dynamic graphic path: {img}"))
            continue
        clean = unquote(img.split("#", 1)[0].split("?", 1)[0])
        candidate = manuscript.parent / clean
        if candidate.is_file():
            continue
        if candidate.suffix == "" and any(candidate.with_suffix(ext).is_file() for ext in IMAGE_SUFFIXES):
            continue
        issues.append(issue("MISSING_IMAGE", "ERROR", f"Referenced local figure not found: {img}", location=str(manuscript)))

    for lineno, line in enumerate(cleaned.splitlines(), 1):
        if PLACEHOLDER.search(line):
            issues.append(issue("PLACEHOLDER", "WARNING", "Possible unresolved editorial placeholder.", location=f"{manuscript}:{lineno}"))

    report["status"] = "STATIC_ISSUES_FOUND" if issues else "NO_STATIC_ISSUES_DETECTED"
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manuscript", type=Path, required=True, help="Local .md or .tex manuscript")
    ap.add_argument("--bib", type=Path, help="Optional BibTeX .bib file")
    ap.add_argument("--report", type=Path, help="Write JSON report to this path")
    args = ap.parse_args(argv)
    try:
        result = inspect(args.manuscript, args.bib)
    except (OSError, UnicodeError) as exc:
        print(json.dumps({"status": "STATIC_ISSUES_FOUND", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if any(x["severity"] == "ERROR" for x in result["issues"]) else 0


if __name__ == "__main__":
    sys.exit(main())
