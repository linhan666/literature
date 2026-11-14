#!/usr/bin/env python3
"""Structural provenance validation for review slide plans; not a scientific fact checker."""
import argparse
import csv
import json
from pathlib import Path

TYPES = {"cover", "big_idea", "scope", "taxonomy", "mechanisms", "lanes", "comparability",
         "matrix", "evidence_map", "timeline", "debate", "agenda", "synthesis", "figure", "closing"}
EPI = {"source_reported", "independently_verified", "synthesis_inference",
       "author_proposed", "disputed", "unresolved"}
VERIFY = {"verified_against_source", "partially_checked", "not_checked", "conflicting"}
IDENTITY = {"verified_original", "verified_index", "unverified", "conflicting"}


def load_csv(path):
    if not path:
        return []
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def split_keys(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return [x.strip() for x in str(value or "").split(";") if x.strip()]


def validate(plan, claims=None, sources=None, strict=False, plan_dir=None):
    messages = []
    mode = plan.get("mode", "production")
    claim_rows = claims or []
    source_rows = sources or []
    cidx = {x.get("claim_id", "").strip(): x for x in claim_rows}
    sidx = {x.get("source_id", "").strip(): x for x in source_rows}

    def add(sev, code, detail, slide=None):
        messages.append({"severity": sev, "code": code, "detail": detail, "slide": slide})

    if mode not in ("demo", "production"):
        add("error", "invalid_mode", f"Unknown mode: {mode}")
    if not plan.get("slides"):
        add("error", "missing_slides", "No slides in plan")
    for fld in ("claim_id", "source_id"):
        rows = claim_rows if fld == "claim_id" else source_rows
        ids = [x.get(fld, "").strip() for x in rows]
        if any(not x for x in ids):
            add("error", "empty_ids", f"Empty {fld} detected")
        if len(ids) != len(set(ids)):
            add("error", "duplicate_ids", f"Duplicate {fld} detected")

    for s in source_rows:
        if s.get("identity_status", "") not in IDENTITY:
            add("warning", "source_identity", f"{s.get('source_id')}: source identity missing/unknown")
    for c in claim_rows:
        cid = c.get("claim_id", "")
        status = c.get("epistemic_status", "")
        verify = c.get("verification_status", "")
        related = split_keys(c.get("source_ids", ""))
        if status not in EPI:
            add("error", "claim_status", f"Claim {cid} invalid epistemic_status {status}")
        if verify not in VERIFY:
            add("error", "verification_status", f"Claim {cid} invalid verification_status {verify}")
        for key in related:
            if key not in sidx:
                add("error", "unknown_claim_source", f"Claim {cid} references missing source {key}")
        if status in {"source_reported", "independently_verified"}:
            if not related:
                add("error", "factual_claim_uncited", f"Claim {cid} has no source IDs")
            if verify != "verified_against_source":
                add("error" if strict else "warning", "unverified_factual_claim",
                    f"Claim {cid} is {status} but source passage not verified")
            if not c.get("source_locator", "").strip():
                add("error" if strict else "warning", "no_source_locator", f"Claim {cid} lacks source location")
            for sid in related:
                if sid in sidx and sidx[sid].get("identity_status") != "verified_original":
                    add("error" if strict else "warning", "primary_source_not_checked",
                        f"Claim {cid}: source {sid} was not marked verified_original")
            if status == "independently_verified" and not c.get("verification_basis", "").strip():
                add("error" if strict else "warning", "no_independent_verification_basis",
                    f"Claim {cid}: independent validation needs documented replication/audit basis")
        if status == "synthesis_inference" and not related:
            add("error" if strict else "warning", "synthesis_uncited", f"Claim {cid}: inference has no supporting sources")
        if status in {"disputed", "unresolved"} and not c.get("limitations", "").strip():
            add("warning", "no_uncertainty_qualification", f"Claim {cid}: missing limitations")

    for i, slide in enumerate(plan.get("slides", []), start=1):
        t = slide.get("type")
        if t not in TYPES:
            add("error", "unknown_layout", f"Unsupported slide type {t}", i)
        if not slide.get("title"):
            add("error", "missing_title", "Slide title required", i)
        for cid in slide.get("claim_ids", []):
            if cid not in cidx and mode == "production":
                add("error", "unknown_slide_claim", f"Unknown claim ID {cid}", i)
        for sid in slide.get("source_ids", []):
            if sid not in sidx and mode == "production":
                add("error", "unknown_slide_source", f"Unknown source ID {sid}", i)
        if mode == "production" and t not in {"cover", "closing"}:
            if not slide.get("claim_ids"):
                add("error" if strict else "warning", "no_claim_mapping", "Content slide lacks mapped claim IDs", i)
            for cid in slide.get("claim_ids", []):
                if cid in cidx:
                    cm = cidx[cid]
                    cs = set(split_keys(cm.get("source_ids", "")))
                    ss = set(slide.get("source_ids", []))
                    if not cs.issubset(ss):
                        add("error" if strict else "warning", "slide_sources_missing",
                            f"Claim {cid} source IDs {sorted(cs - ss)} absent from slide", i)
                    ep = cm.get("epistemic_status", "")
                    if ep in {"author_proposed", "disputed", "unresolved", "synthesis_inference"}:
                        own = str(slide.get("epistemic_status", "")).lower().replace("-", "_")
                        if slide.get("type") in {"evidence_map", "synthesis"} and own == "mixed_evidence":
                            continue
                        if own != ep:
                            add("error" if strict else "warning", "episteme_label_mismatch",
                                f"Slide episteme {own} does not match {cid}:{ep}", i)
        if t == "matrix" and slide.get("comparison_mode") not in {"matched", "conditional", "unmatched"}:
            add("error", "comparison_context_missing", "Matrix requires comparison_mode", i)
        if t == "timeline":
            for track in slide.get("tracks", []):
                for node in track.get("nodes", []):
                    if mode == "production" and not node.get("source_ids"):
                        add("error" if strict else "warning", "unsourced_timeline_node",
                            f"Timeline node {node.get('label')} needs source_ids", i)
        if t == "figure":
            p = Path(slide.get("path", ""))
            if not p.is_absolute() and plan_dir is not None:
                p = Path(plan_dir) / p
            if not p.is_file():
                add("error", "missing_figure", f"Cannot find figure: {p}", i)
            if mode == "production" and not slide.get("credit"):
                add("error", "figure_credit", "Figure requires attribution/author-origin statement", i)
    return {"mode": mode, "slides": len(plan.get("slides", [])),
            "sources": len(source_rows), "claims": len(claim_rows),
            "errors": sum(m["severity"] == "error" for m in messages),
            "warnings": sum(m["severity"] == "warning" for m in messages),
            "messages": messages,
            "limitations": ["Structural validation is not DOI resolution or original-paper review",
                            "No inference is independently verified by this script",
                            "Visual inspection is outside this script"]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--claims", type=Path)
    p.add_argument("--sources", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--strict", action="store_true")
    a = p.parse_args()
    plan = json.loads(a.plan.read_text(encoding="utf-8"))
    if plan.get("mode", "production") == "production" and (not a.claims or not a.sources):
        p.error("Production plans require --claims and --sources")
    report = validate(plan, load_csv(a.claims), load_csv(a.sources), a.strict, a.plan.parent)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Provenance structural checks: {report['errors']} errors, {report['warnings']} warnings -> {a.out}")
    print("Verification means schema/linkage checks only, not independent source/review audit.")
    if a.strict and report["errors"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
