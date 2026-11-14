#!/usr/bin/env python3
"""Render a PowerPoint deck to per-slide PNGs and a labeled contact sheet.

Requires LibreOffice (or soffice), PyMuPDF, and Pillow. Does not mark the
presentation as human-reviewed; users must inspect the resulting images.
"""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont


def get_font(size=18):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def export_with_powerpoint(pptx: Path, pdf: Path):
    """Windows fallback when Microsoft PowerPoint and pywin32 are installed."""
    try:
        import win32com.client  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "PowerPoint rendering on Windows needs Microsoft PowerPoint and "
            "pywin32 (`py -m pip install pywin32`).") from exc
    app, pres = None, None
    try:
        app = win32com.client.DispatchEx("PowerPoint.Application")
        # 32 = ppSaveAsPDF; execute in a temporary folder.
        pres = app.Presentations.Open(str(pptx.resolve()), WithWindow=False)
        pres.SaveAs(str(pdf.resolve()), 32)
    finally:
        if pres is not None:
            pres.Close()
        if app is not None:
            app.Quit()


def render_pptx(pptx: Path, outdir: Path):
    office = shutil.which("libreoffice") or shutil.which("soffice")
    if not office and os.name != "nt":
        raise RuntimeError(
            "No slide renderer found. Install LibreOffice or export the PPTX "
            "from PowerPoint manually; visual QA remains mandatory.")
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pptx_render_") as tempdir:
        t = Path(tempdir)
        pdf = t / (pptx.stem + ".pdf")
        if office:
            profile = (t / "lo_profile").as_uri()
            cmd = [office, f"-env:UserInstallation={profile}", "--headless",
                   "--convert-to", "pdf", "--outdir", str(t), str(pptx.resolve())]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if proc.returncode != 0 or not pdf.exists():
                raise RuntimeError(f"PowerPoint render failed: {proc.stdout}\n{proc.stderr}")
            backend = "LibreOffice"
        else:
            export_with_powerpoint(pptx, pdf)
            if not pdf.exists():
                raise RuntimeError("PowerPoint COM export did not create PDF")
            backend = "Microsoft PowerPoint COM"
        doc = fitz.open(pdf)
        paths = []
        for i, page in enumerate(doc, 1):
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            p = outdir / f"slide_{i:02d}.png"
            pix.save(str(p))
            paths.append(p)
        doc.close()
    return paths, backend


def contact_sheet(images, outfile: Path, columns=3, thumb_w=640):
    font = get_font(18)
    thumb_h = round(thumb_w * 9 / 16)
    gap, label_h = 21, 31
    rows = (len(images) + columns - 1) // columns
    width = gap + columns * (thumb_w + gap)
    height = gap + rows * (thumb_h + label_h + gap)
    canvas = Image.new("RGB", (width, height), "#E9EDF2")
    draw = ImageDraw.Draw(canvas)
    for i, item in enumerate(images):
        x = gap + (i % columns) * (thumb_w + gap)
        y = gap + (i // columns) * (thumb_h + label_h + gap)
        with Image.open(item) as orig:
            img = orig.convert("RGB")
            img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            canvas.paste(img, (x + (thumb_w - img.width) // 2, y))
        draw.rectangle((x, y, x + thumb_w, y + thumb_h), outline="#C7D0DC", width=2)
        draw.text((x + 8, y + thumb_h + 6), f"Slide {i+1:02d}",
                  font=font, fill="#263A54")
    canvas.save(outfile)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pptx", type=Path)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--columns", type=int, default=3)
    args = ap.parse_args()
    if not args.pptx.exists():
        ap.error(f"File not found: {args.pptx}")
    imgs, backend = render_pptx(args.pptx, args.outdir)
    contact_sheet(imgs, args.outdir / "contact_sheet.png", columns=args.columns)
    with (args.outdir / "render_status.json").open("w", encoding="utf-8") as f:
        json.dump({"renderer": backend + " -> PDF -> PyMuPDF PNG",
                   "slides_rendered": len(imgs), "result": "render_completed",
                   "visual_inspection_completed": False,
                   "note": "Render success does not imply human or visual QA pass."},
                  f, indent=2)
    print(f"Rendered {len(imgs)} slides: {args.outdir}")
    print("Inspect each slide PNG visually; render success is not a visual-QA pass.")


if __name__ == "__main__":
    main()
