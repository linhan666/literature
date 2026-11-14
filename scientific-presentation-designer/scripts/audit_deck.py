#!/usr/bin/env python3
"""Static PPTX QA: geometry, text red flags, structural metadata.

Automated warnings are conservative and intentionally do not certify visual
quality or scientific correctness. Complement with rendered-image inspection.
"""
import argparse
import json
from pathlib import Path
from pptx import Presentation


def run(pptx_file: Path, plan_file: Path | None = None):
    prs = Presentation(pptx_file)
    slides = prs.slides
    warnings = []
    slide_stats = []
    plan = None
    if plan_file:
        with open(plan_file, encoding="utf-8") as f:
            plan = json.load(f)
        if len(plan.get("slides", [])) != len(slides):
            warnings.append({"slide": "deck", "severity": "error",
                             "issue": "Plan and PPTX slide counts differ"})
    for index, slide in enumerate(slides, start=1):
        stat = {"slide": index, "text_shapes": 0, "picture_shapes": 0,
                "min_main_text_pt": None, "total_text_chars": 0}
        for shape in slide.shapes:
            x, y, w, h = shape.left, shape.top, shape.width, shape.height
            tol = 20000
            if x < -tol or y < -tol or x + w > prs.slide_width + tol or y + h > prs.slide_height + tol:
                warnings.append({"slide": index, "severity": "error",
                                 "issue": "Shape extends beyond slide canvas",
                                 "shape_name": shape.name,
                                 "box_emu": [int(x), int(y), int(w), int(h)]})
            if shape.shape_type == 13:  # picture
                stat["picture_shapes"] += 1
            if not shape.has_text_frame:
                continue
            text = shape.text.strip()
            if not text:
                continue
            stat["text_shapes"] += 1
            stat["total_text_chars"] += len(text)
            main = y < int(6.9 * 914400) and y > int(1.65 * 914400)
            sizes = []
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if run.font.size:
                        sizes.append(run.font.size.pt)
            if main and sizes:
                fs = min(sizes)
                if stat["min_main_text_pt"] is None:
                    stat["min_main_text_pt"] = round(fs, 1)
                else:
                    stat["min_main_text_pt"] = min(stat["min_main_text_pt"], round(fs, 1))
                if fs < 12:
                    warnings.append({"slide": index, "severity": "warning",
                                     "issue": "Main-area text <12 pt may be unreadable",
                                     "font_pt": round(fs, 1), "text": text[:75]})
            if len(text) > 260:
                warnings.append({"slide": index, "severity": "warning",
                                 "issue": "Dense text box >260 characters; review visual fit",
                                 "characters": len(text), "text": text[:75]})
        if stat["total_text_chars"] > 1100:
            warnings.append({"slide": index, "severity": "warning",
                             "issue": "High overall text density; consider reducing content",
                             "characters": stat["total_text_chars"]})
        if plan:
            sdata = plan.get("slides", [])[index - 1]
            if sdata.get("type") not in ("cover", "section", "closing") and not sdata.get("sources"):
                warnings.append({"slide": index, "severity": "warning",
                                 "issue": "Content slide has no source IDs in plan"})
        slide_stats.append(stat)
    return {
        "pptx": str(pptx_file), "slides": len(slides),
        "static_geometry_checked": True,
        "visual_slide_inspection_completed": False,
        "scientific_source_verification_completed": False,
        "critical_limitations": ["A static QA script cannot detect all text overlaps/clipping",
                                 "Only inspection of rendered slides can assess visual quality",
                                 "Numerical claims require an independent evidence ledger"],
        "warnings": warnings, "slide_stats": slide_stats,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pptx", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--plan", type=Path)
    args = ap.parse_args()
    report = run(args.pptx, args.plan)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Checked {report['slides']} slides; {len(report['warnings'])} warnings → {args.out}")
    print("Static audit is not visual inspection or scientific verification.")


if __name__ == "__main__":
    main()
