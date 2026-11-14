#!/usr/bin/env python3
"""Editable PowerPoint reference engine for scientific-presentation-designer.

The layout decisions are intentionally explicit and editable in python-pptx.
All sample numbers in examples/ are synthetic and must never be presented as results.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt

W, H = 13.333, 7.5

THEMES = {
    "lab-light": dict(ink="182B45", muted="607185", bg="FAFBFD", surface="FFFFFF",
                      dark="102139", teal="078B91", teal_dark="076F74", amber="E5A13D",
                      violet="7B67B4", red="B84E5D", border="E0E8F0", pale="EDF7F6",
                      dark_muted="B5C5D4", baseline="8A9BAB"),
    "editorial": dict(ink="1D2D3F", muted="667584", bg="F7F7F4", surface="FFFFFF",
                      dark="152438", teal="167C88", teal_dark="0C6873", amber="C9914A",
                      violet="83729B", red="B85F55", border="E5E6E5", pale="E9F2F1",
                      dark_muted="B6C4CE", baseline="8A9BAB"),
    "conference-dark": dict(ink="F5F8FC", muted="B5C5D4", bg="132235", surface="1B3046",
                      dark="0B1828", teal="4CC6BD", teal_dark="30AAA8", amber="F0BD65",
                      violet="AD94E4", red="E98D98", border="3B5368", pale="233C4B",
                      dark_muted="ADC1D0", baseline="9EB0C1"),
}


def rgb(value: str) -> RGBColor:
    v = value.lstrip("#")
    return RGBColor.from_string(v.upper())


def in_(x: float):
    return Inches(float(x))


def rect(slide, x, y, w, h, fill, line=None, radius=False, lw=0.9):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        in_(x), in_(y), in_(w), in_(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    if line:
        shape.line.color.rgb = rgb(line)
        shape.line.width = Pt(lw)
    else:
        shape.line.fill.background()
    if radius:
        try:
            shape.adjustments[0] = 0.10
        except Exception:
            pass
    return shape


def ellipse(slide, x, y, d, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, in_(x), in_(y), in_(d), in_(d))
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(fill)
    if line:
        shp.line.color.rgb = rgb(line)
    else:
        shp.line.fill.background()
    return shp


def line(slide, x1, y1, x2, y2, color, width=1.2):
    shp = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, in_(x1), in_(y1), in_(x2), in_(y2))
    shp.line.color.rgb = rgb(color)
    shp.line.width = Pt(width)
    return shp


def txt(slide, content, x, y, w, h, size=18, color="182B45", bold=False,
        align="left", valign="top", margin=0, font="Aptos", italic=False,
        no_wrap=False, tracking=None):
    shape = slide.shapes.add_textbox(in_(x), in_(y), in_(w), in_(h))
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = not no_wrap
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    tf.margin_left = tf.margin_right = in_(margin)
    tf.margin_top = tf.margin_bottom = in_(0)
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP,
                          "middle": MSO_ANCHOR.MIDDLE,
                          "bottom": MSO_ANCHOR.BOTTOM}[valign]
    lines = str(content).split("\n")
    for i, value in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = value
        p.alignment = {"left": PP_ALIGN.LEFT,
                       "center": PP_ALIGN.CENTER,
                       "right": PP_ALIGN.RIGHT}[align]
        p.space_after = Pt(0)
        p.line_spacing = 1.10
        for run in p.runs:
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.color.rgb = rgb(color)
    return shape


def text_list(slide, items, x, y, width, theme, size=19, gap=0.73,
              bullet_color=None, max_items=5):
    for i, item in enumerate(items[:max_items]):
        py = y + i * gap
        ellipse(slide, x, py + 0.12, 0.095, bullet_color or theme["teal"])
        txt(slide, str(item), x + 0.24, py, width - 0.24, gap - 0.08,
            size=size, color=theme["ink"])


def base_slide(prs, theme, dark=False):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, 0, 0, W, H, theme["dark"] if dark else theme["bg"])
    return slide


def header(slide, slide_data, theme, page, total):
    title = slide_data["title"]
    txt(slide, "RESEARCH  /  EVIDENCE-LED", 0.66, 0.29, 6.0, 0.24,
        size=10.0, bold=True, color=theme["teal"])
    title_size = 31 if len(title) < 66 else 27
    if any("\u4e00" <= ch <= "\u9fff" for ch in title):
        title_size = 29 if len(title) < 35 else 26
    txt(slide, title, 0.66, 0.69, 12.02, 0.86,
        size=title_size, color=theme["ink"], bold=True)
    rect(slide, 0.66, 1.61, 0.82, 0.055, theme["teal"])
    line(slide, 1.56, 1.638, 12.66, 1.638, theme["border"], 1)


def footer(slide, slide_data, theme, page, total, disclaimer="", dark=False):
    sources = slide_data.get("sources", [])
    left = "SOURCE  " + "  ·  ".join(str(x) for x in sources) if sources else ""
    foot_color = theme["dark_muted"] if dark else theme["muted"]
    if left:
        txt(slide, left[:115], 0.66, 7.12, 7.85, 0.23, size=9.6, color=foot_color)
    if disclaimer:
        txt(slide, str(disclaimer)[:95], 3.2, 7.115, 7.3, 0.24,
            size=9.0, color=theme["amber"] if dark else theme["red"],
            align="center")
    txt(slide, f"{page:02d} / {total:02d}", 11.95, 7.12, 0.72, 0.22,
        size=9.8, color=foot_color, align="right")


def add_notes(slide, data):
    notes = []
    if data.get("speaker_notes"):
        notes.append(str(data["speaker_notes"]))
    if data.get("sources"):
        notes.append("SOURCE IDs: " + ", ".join(map(str, data["sources"])))
    if data.get("citation"):
        notes.append("CITATION: " + str(data["citation"]))
    if notes:
        try:
            slide.notes_slide.notes_text_frame.text = "\n".join(notes)
        except Exception:
            pass


def right_insight(slide, d, theme, subtitle="INTERPRETATION"):
    x, y, w, h = 9.44, 1.93, 3.22, 4.66
    rect(slide, x, y, w, h, theme["pale"], radius=True)
    rect(slide, x + 0.27, y + 0.32, 0.08, 0.44, theme["teal"])
    txt(slide, subtitle, x + 0.48, y + 0.35, 2.38, 0.32, size=12.5,
        bold=True, color=theme["teal_dark"])
    take = d.get("takeaway") or d.get("insight") or "Inspect matched conditions before interpreting differences."
    txt(slide, take, x + 0.28, y + 1.00, w - 0.55, 1.55,
        size=21, color=theme["ink"], bold=True)
    if d.get("context"):
        line(slide, x + 0.28, y + 2.84, x + w - 0.28, y + 2.84,
             theme["border"], 1.1)
        txt(slide, d["context"], x + 0.28, y + 3.05, w - 0.56, 1.28,
            size=15.8, color=theme["muted"])


def draw_cover(prs, d, theme, page, total, global_data):
    s = base_slide(prs, theme, dark=True)
    rect(s, 0.0, 0, 0.13, 7.5, theme["teal"])
    rect(s, 0.70, 0.80, 0.76, 0.06, theme["teal"])
    txt(s, "SCIENTIFIC RESEARCH  /  PROJECT REPORT", 0.70, 0.42, 9, 0.26,
        size=12, color=theme["dark_muted"], bold=True)
    title = d.get("title", global_data.get("title", "Research presentation"))
    size = 37 if len(title) < 58 else 33
    txt(s, title, 0.70, 1.55, 7.7, 2.1, size=size,
        color="FFFFFF", bold=True)
    subtitle = d.get("subtitle", global_data.get("subtitle", ""))
    txt(s, subtitle, 0.72, 3.94, 7.20, 1.04,
        size=22.5, color="D3E0E9")
    author = d.get("author", global_data.get("author", ""))
    if author:
        txt(s, author, 0.72, 6.37, 7.60, 0.42,
            size=15.2, color="D2DFE8", bold=True)
    # right graphic: compact connected research steps, vector and editable
    rx = 9.12
    tags = d.get("tags", ["QUESTION", "METHOD", "EVIDENCE", "DECISION"])
    tags = (tags + ["", "", "", ""])[:4]
    line(s, rx + 0.42, 1.87, rx + 0.42, 5.94, "365268", 2.6)
    for i, label in enumerate(tags):
        yy = 1.68 + i * 1.25
        ellipse(s, rx + 0.27, yy + 0.12, 0.31, theme["teal"] if i == 2 else "38536D")
        rect(s, rx + 0.89, yy, 3.0, 0.72, "19334C", line="38536A", radius=True)
        txt(s, label, rx + 1.13, yy + 0.16, 2.5, 0.38,
            size=16.3, color="FFFFFF" if i == 2 else "D1DFE9", bold=(i == 2))
    footer(s, d, theme, page, total, global_data.get("disclaimer", ""), True)
    add_notes(s, d)
    return s


def draw_section(prs, d, theme, page, total, global_data):
    s = base_slide(prs, theme, dark=True)
    rect(s, 0.66, 1.15, 0.11, 4.35, theme["teal"])
    num = d.get("number", f"{page:02d}")
    txt(s, str(num), 1.02, 1.20, 2.0, 1.09,
        size=65, color="5B748B", bold=True)
    txt(s, d["title"], 1.01, 2.53, 10.98, 1.65,
        size=38, color="FFFFFF", bold=True)
    if d.get("subtitle"):
        txt(s, d["subtitle"], 1.05, 4.53, 9.98, 1.06,
            size=22, color="BFD0DE")
    footer(s, d, theme, page, total, global_data.get("disclaimer", ""), True)
    add_notes(s, d)
    return s


def draw_cards(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    cards = d.get("cards", [])
    if not 2 <= len(cards) <= 4:
        raise ValueError("cards slide needs 2-4 cards")
    n = len(cards)
    gap = 0.19
    cw = (12.0 - (n - 1) * gap) / n
    colors = [theme["teal"], theme["violet"], theme["amber"], theme["teal_dark"]]
    for i, card in enumerate(cards):
        x = 0.67 + i * (cw + gap)
        rect(s, x, 2.03, cw, 3.93, theme["surface"], line=theme["border"], radius=True)
        rect(s, x, 2.03, cw, 0.075, colors[i])
        txt(s, f"0{i+1}", x + 0.28, 2.40, 0.80, 0.54,
            size=27, bold=True, color=colors[i])
        txt(s, card["heading"], x + 0.26, 3.03, cw - 0.50, 0.78,
            size=22.2, bold=True, color=theme["ink"])
        txt(s, card.get("body", ""), x + 0.26, 4.10, cw - 0.50, 1.44,
            size=18.0 if n <= 3 else 16.3, color=theme["muted"])
    if d.get("takeaway"):
        txt(s, d["takeaway"], 0.68, 6.28, 11.76, 0.44,
            size=17, bold=True, color=theme["teal_dark"])
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def draw_kpis(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    rect(s, 0.66, 2.02, 5.54, 4.57, theme["dark"], radius=True)
    txt(s, "CENTRAL FINDING", 1.00, 2.43, 4.6, 0.34,
        size=12.5, color=theme["teal"], bold=True)
    txt(s, d.get("takeaway", "The result needs a matched evaluation context."),
        1.00, 3.03, 4.80, 2.31, size=27.0, bold=True, color="FFFFFF")
    if d.get("context"):
        txt(s, d["context"], 1.00, 5.65, 4.89, 0.58,
            size=14.5, color="C0CEDB")
    kpis = d.get("kpis", [])
    if not 1 <= len(kpis) <= 4:
        raise ValueError("kpis slide needs 1-4 kpis")
    locs = [(6.43, 2.03), (9.62, 2.03), (6.43, 4.40), (9.62, 4.40)]
    colors = [theme["teal"], theme["amber"], theme["violet"], theme["teal_dark"]]
    for i, k in enumerate(kpis):
        x, y = locs[i]
        rect(s, x, y, 3.00, 2.13, theme["surface"], line=theme["border"], radius=True)
        rect(s, x + 0.27, y + 0.27, 0.48, 0.045, colors[i])
        txt(s, str(k["value"]), x + 0.26, y + 0.58, 2.55, 0.72,
            size=31.5, bold=True, color=theme["ink"])
        txt(s, k.get("label", ""), x + 0.26, y + 1.39, 2.50, 0.55,
            size=15.4, color=theme["muted"])
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def draw_pipeline(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    steps = d.get("steps", [])
    n = len(steps)
    if not 3 <= n <= 6:
        raise ValueError("pipeline slide needs 3-6 steps")
    gap = 0.30
    cw = (12.0 - (n - 1) * gap) / n
    y = 2.37
    for i, step in enumerate(steps):
        x = 0.68 + i * (cw + gap)
        rect(s, x, y, cw, 2.66, theme["surface"], line=theme["border"], radius=True)
        rect(s, x, y, cw, 0.082,
             theme["teal"] if i == n - 1 else (theme["violet"] if i % 2 else theme["amber"]))
        txt(s, f"{i + 1:02d}", x + 0.20, y + 0.26, cw - 0.40, 0.43,
            size=22, bold=True, color=theme["teal"] if i == n - 1 else theme["muted"])
        txt(s, step["label"], x + 0.19, y + 0.91, cw - 0.38, 0.69,
            size=18.3 if n <= 4 else 16.8, bold=True, color=theme["ink"])
        txt(s, step.get("detail", ""), x + 0.19, y + 1.76, cw - 0.38, 0.68,
            size=15.0 if n <= 4 else 13.8, color=theme["muted"])
        if i < n - 1:
            lx = x + cw + 0.08
            cy = y + 1.31
            line(s, lx, cy, lx + 0.14, cy, theme["teal"], 2.4)
            tri = s.shapes.add_shape(MSO_SHAPE.CHEVRON, in_(lx + 0.13), in_(cy - 0.10), in_(0.13), in_(0.20))
            tri.fill.solid(); tri.fill.fore_color.rgb = rgb(theme["teal"])
            tri.line.fill.background()
    if d.get("takeaway") or d.get("context"):
        rect(s, 0.70, 5.56, 11.94, 0.79, theme["pale"], radius=True)
        txt(s, d.get("takeaway") or d.get("context"), 0.96, 5.77,
            11.48, 0.44, size=17.4, color=theme["teal_dark"], bold=True)
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def ticks(lo, hi, n=5):
    return [lo + (hi - lo) * i / (n - 1) for i in range(n)]


def fmt_num(value, format_spec=None):
    try:
        if format_spec:
            return format(value, format_spec)
        if abs(float(value)) < 10:
            return f"{float(value):.3f}"
        return f"{float(value):.1f}"
    except (ValueError, TypeError):
        return str(value)


def draw_bar_chart(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    rect(s, 0.66, 1.93, 8.55, 4.66, theme["surface"], line=theme["border"], radius=True)
    items = d.get("items", [])
    if not 2 <= len(items) <= 7:
        raise ValueError("bar_chart slide needs 2-7 items")
    values = [float(item["value"]) for item in items]
    lo, hi = float(d.get("xmin", 0)), float(d.get("xmax", max(values) * 1.1 or 1))
    if hi <= lo or min(values) < lo - 1e-10 or max(values) > hi + 1e-10:
        raise ValueError("bar_chart invalid x-axis boundaries")
    pl, pr = 3.17, 8.21
    y_top, y_bottom = 2.43, 5.79
    for v in ticks(lo, hi):
        x = pl + (v - lo) / (hi - lo) * (pr - pl)
        line(s, x, y_top, x, y_bottom, theme["border"], 0.95)
        txt(s, fmt_num(v, d.get("tick_format", ".2f")), x - 0.26, 5.93,
            0.53, 0.30, size=12.4, color=theme["muted"], align="center")
    row_h = (y_bottom - y_top - 0.13) / len(items)
    for i, (item, value) in enumerate(zip(items, values)):
        cy = y_top + (i + 0.48) * row_h
        txt(s, item["label"], 0.89, cy - 0.20, 2.04, 0.48,
            size=15.7 if len(items) <= 5 else 14.2, color=theme["ink"],
            bold=bool(item.get("highlight")))
        bx = pl + (max(lo, value) - lo) / (hi - lo) * (pr - pl)
        role = str(item.get("role", "")).lower()
        if item.get("highlight") or role in ("focus", "proposed", "focal"):
            col = theme["teal"]
        elif role == "baseline":
            col = theme["baseline"]
        elif role in ("secondary", "attention") or item.get("group") == "secondary":
            col = theme["violet"]
        else:
            col = theme["amber"]
        if value > lo:
            rect(s, pl, cy - 0.17, max(0.02, bx - pl), 0.33, col, radius=True)
        txt(s, fmt_num(value, d.get("value_format", ".3f")), 8.32, cy - 0.15,
            0.74, 0.33, size=15.0, bold=bool(item.get("highlight")),
            color=theme["ink"], align="right")
    txt(s, d.get("axis_label", "Metric"), 3.52, 6.27, 4.7, 0.24,
        size=12.3, color=theme["muted"], align="center")
    right_insight(s, d, theme)
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def draw_line_chart(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    rect(s, 0.66, 1.93, 8.55, 4.66, theme["surface"], line=theme["border"], radius=True)
    xs = d.get("x_labels", [])
    data = d.get("series", [])
    if not 2 <= len(xs) <= 8 or not 1 <= len(data) <= 4:
        raise ValueError("line_chart needs 2-8 x_labels and 1-4 series")
    if any(len(sv.get("values", [])) != len(xs) for sv in data):
        raise ValueError("series length must match x_labels")
    vals = [float(v) for sv in data for v in sv["values"]]
    lo, hi = float(d.get("ymin", min(vals))), float(d.get("ymax", max(vals)))
    if hi <= lo or min(vals) < lo - 1e-10 or max(vals) > hi + 1e-10:
        raise ValueError("line_chart invalid y bounds")
    pl, pr, pt, pb = 1.48, 8.64, 2.39, 5.66
    for v in ticks(lo, hi):
        y = pb - (v - lo) / (hi - lo) * (pb - pt)
        line(s, pl, y, pr, y, theme["border"], 0.9)
        txt(s, fmt_num(v, d.get("tick_format", ".2f")), 0.82, y - 0.12,
            0.53, 0.26, size=12.1, color=theme["muted"], align="right")
    for i, lab in enumerate(xs):
        x = pl + (i / (len(xs) - 1)) * (pr - pl)
        txt(s, str(lab), x - 0.40, 5.78, 0.81, 0.27,
            size=12.7, color=theme["muted"], align="center")
    default_colors = [theme["amber"], theme["violet"], theme["teal"], theme["red"]]
    for j, sv in enumerate(data):
        role = str(sv.get("role", "")).lower()
        col = (theme["teal"] if role in ("focus", "proposed", "focal") else
               theme["baseline"] if role == "baseline" else
               theme["violet"] if role in ("secondary", "attention") else
               theme["amber"] if role == "comparison" else default_colors[j])
        coords = []
        for i, val in enumerate(sv["values"]):
            x = pl + (i / (len(xs) - 1)) * (pr - pl)
            y = pb - (float(val) - lo) / (hi - lo) * (pb - pt)
            coords.append((x, y))
        for (x1, y1), (x2, y2) in zip(coords, coords[1:]):
            line(s, x1, y1, x2, y2, col, 2.5)
        for x, y in coords:
            ellipse(s, x - 0.073, y - 0.073, 0.146, col, theme["surface"])
        lx = 1.00 + j * 1.91
        line(s, lx, 6.30, lx + 0.28, 6.30, col, 2.8)
        txt(s, sv["label"], lx + 0.37, 6.17, 1.43, 0.33,
            size=12.7, color=theme["ink"])
    right_insight(s, d, theme)
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def draw_table(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    headers = d.get("columns", [])
    rows = d.get("rows", [])
    if not 2 <= len(headers) <= 6 or not 1 <= len(rows) <= 7:
        raise ValueError("metric_table needs 2-6 columns and 1-7 rows")
    if any(len(row) != len(headers) for row in rows):
        raise ValueError("metric_table row length differs from header length")
    n = len(headers)
    x0, y0, tw = 0.72, 2.04, 11.94
    hdr_h, row_h = 0.64, min(0.69, 3.95 / len(rows))
    widths = d.get("widths") or ([3.23] + [(tw - 3.23) / (n - 1)] * (n - 1))
    if len(widths) != n:
        raise ValueError("width count mismatch")
    scale = tw / sum(widths)
    widths = [w * scale for w in widths]
    rect(s, x0, y0, tw, hdr_h, theme["dark"], radius=False)
    curx = x0
    for i, head in enumerate(headers):
        txt(s, head, curx + 0.16, y0 + 0.17, widths[i] - 0.30, 0.32,
            size=15.0, bold=True, color="FFFFFF",
            align="left" if i == 0 else "center")
        curx += widths[i]
    hl = d.get("highlight_row", -1)
    for r, row in enumerate(rows):
        yy = y0 + hdr_h + r * row_h
        fill = theme["pale"] if r == hl else (theme["surface"] if r % 2 == 0 else theme["bg"])
        rect(s, x0, yy, tw, row_h, fill)
        curx = x0
        for c, val in enumerate(row):
            color = theme["teal_dark"] if r == hl else theme["ink"]
            txt(s, str(val), curx + 0.15, yy + 0.10,
                widths[c] - 0.28, row_h - 0.17,
                size=16.1, bold=(r == hl), color=color,
                align="left" if c == 0 else "center", valign="middle")
            curx += widths[c]
        line(s, x0, yy + row_h, x0 + tw, yy + row_h, theme["border"], 0.65)
    if d.get("takeaway"):
        rect(s, 0.72, 6.29, 11.94, 0.49, theme["pale"], radius=True)
        txt(s, d["takeaway"], 0.94, 6.40, 11.42, 0.28,
            size=15.3, bold=True, color=theme["teal_dark"])
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def draw_comparison(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    left = d["left"]
    right = d["right"]
    for j, (item, x, col) in enumerate([(left, 0.70, theme["amber"]), (right, 6.76, theme["teal"])]):
        rect(s, x, 2.02, 5.83, 3.87, theme["surface"], line=theme["border"], radius=True)
        rect(s, x, 2.02, 5.83, 0.088, col)
        txt(s, item["heading"], x + 0.32, 2.38, 5.17, 0.66,
            size=23, bold=True, color=theme["ink"])
        text_list(s, item.get("points", []), x + 0.34, 3.42, 5.0, theme,
                  size=17.1, gap=0.65, bullet_color=col, max_items=4)
    rect(s, 6.36, 3.61, 0.40, 0.44, theme["dark"], radius=True)
    txt(s, "VS", 6.39, 3.74, 0.34, 0.21, size=12.4,
        bold=True, color="FFFFFF", align="center")
    if d.get("takeaway"):
        txt(s, d["takeaway"], 0.75, 6.22, 11.77, 0.42,
            size=18, bold=True, color=theme["teal_dark"])
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def add_contained_image(slide, path: Path, x, y, w, h):
    if not path.exists():
        raise FileNotFoundError(f"Required scientific figure not found: {path}")
    with Image.open(path) as im:
        ww, hh = im.size
    if ww < 480 or hh < 270:
        print(f"WARNING: Low source image resolution {ww}x{hh}: {path}", file=sys.stderr)
    aspect = ww / hh
    target = w / h
    if aspect > target:
        pw, ph = w, w / aspect
    else:
        ph, pw = h, h * aspect
    xx, yy = x + (w - pw) / 2, y + (h - ph) / 2
    slide.shapes.add_picture(str(path), in_(xx), in_(yy), width=in_(pw), height=in_(ph))


def draw_image_panel(prs, d, theme, page, total, gd, base_dir):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    figures = d.get("figures", [])
    if not 1 <= len(figures) <= 3:
        raise ValueError("image_panel needs 1-3 figures")
    n = len(figures)
    gap = 0.22
    cw = (12.0 - (n - 1) * gap) / n
    for i, fig in enumerate(figures):
        x = 0.66 + i * (cw + gap)
        rect(s, x, 1.99, cw, 4.53, theme["surface"], line=theme["border"], radius=True)
        image_path = Path(fig["path"])
        if not image_path.is_absolute():
            image_path = (base_dir / image_path).resolve()
        add_contained_image(s, image_path, x + 0.18, 2.16, cw - 0.36, 3.45)
        txt(s, fig.get("caption", ""), x + 0.21, 5.74, cw - 0.42, 0.54,
            size=15.0 if n <= 2 else 13.5, color=theme["muted"])
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def draw_findings(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    findings = d.get("findings", [])
    if not 2 <= len(findings) <= 3:
        raise ValueError("findings needs 2-3 findings")
    colors = [theme["teal"], theme["violet"], theme["amber"]]
    gap = 0.24
    w = (12.0 - (len(findings) - 1) * gap) / len(findings)
    for i, f in enumerate(findings):
        x = 0.67 + i * (w + gap)
        rect(s, x, 2.04, w, 4.17, theme["surface"], line=theme["border"], radius=True)
        ellipse(s, x + 0.28, 2.39, 0.38, colors[i])
        txt(s, str(i+1), x + 0.35, 2.49, 0.24, 0.19,
            size=12.3, bold=True, color="FFFFFF", align="center")
        txt(s, f["heading"], x + 0.26, 3.10, w - 0.54, 1.03,
            size=21.7, color=theme["ink"], bold=True)
        line(s, x + 0.27, 4.38, x + w - 0.27, 4.38, theme["border"], 1)
        txt(s, f.get("detail", ""), x + 0.27, 4.61, w - 0.55, 1.35,
            size=16.9, color=theme["muted"])
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def draw_roadmap(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme)
    header(s, d, theme, page, total)
    steps = d.get("steps", [])
    if not 2 <= len(steps) <= 4:
        raise ValueError("roadmap needs 2-4 steps")
    rh = 1.03
    y0 = 2.02
    for i, item in enumerate(steps):
        y = y0 + i * 1.11
        rect(s, 0.69, y, 11.95, rh, theme["surface"], line=theme["border"], radius=True)
        rect(s, 0.70, y, 0.13, rh, theme["teal"] if i == 0 else theme["violet"])
        txt(s, f"{i+1:02d}", 0.99, y + 0.28, 0.50, 0.46,
            size=20.5, bold=True, color=theme["teal"] if i == 0 else theme["muted"])
        txt(s, item["action"], 1.66, y + 0.18, 5.38, 0.58,
            size=18.5, bold=True, color=theme["ink"])
        txt(s, item.get("criterion", ""), 7.20, y + 0.19, 4.96, 0.59,
            size=16, color=theme["muted"])
    footer(s, d, theme, page, total, gd.get("disclaimer", ""))
    add_notes(s, d)
    return s


def draw_closing(prs, d, theme, page, total, gd):
    s = base_slide(prs, theme, dark=True)
    rect(s, 0.66, 1.10, 0.10, 4.76, theme["teal"])
    txt(s, "TAKE-HOME MESSAGE", 1.06, 0.88, 9.9, 0.4,
        size=13.0, bold=True, color=theme["teal"])
    txt(s, d["title"], 1.05, 1.72, 10.64, 1.81,
        size=38, bold=True, color="FFFFFF")
    bullets = d.get("points", [])
    for i, b in enumerate(bullets[:3]):
        yy = 4.02 + i * 0.69
        ellipse(s, 1.08, yy + 0.07, 0.13, theme["teal"])
        txt(s, b, 1.43, yy, 10.3, 0.57, size=21.0, color="DCE6EF")
    footer(s, d, theme, page, total, gd.get("disclaimer", ""), True)
    add_notes(s, d)
    return s


RENDERERS = {
    "cover": draw_cover,
    "section": draw_section,
    "cards": draw_cards,
    "kpis": draw_kpis,
    "pipeline": draw_pipeline,
    "bar_chart": draw_bar_chart,
    "line_chart": draw_line_chart,
    "metric_table": draw_table,
    "comparison": draw_comparison,
    "image_panel": draw_image_panel,
    "findings": draw_findings,
    "roadmap": draw_roadmap,
    "closing": draw_closing,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plan", type=Path, required=True, help="Validated slide_plan.json path")
    ap.add_argument("--out", type=Path, required=True, help="Output .pptx path")
    ap.add_argument("--theme", choices=list(THEMES), help="Override plan theme")
    args = ap.parse_args()

    with args.plan.open(encoding="utf-8") as f:
        plan: dict[str, Any] = json.load(f)
    slides = plan.get("slides", [])
    if not slides or len(slides) > 60:
        raise ValueError("slides must be a nonempty list <=60")
    names = [s.get("id") for s in slides]
    if any(not n for n in names) or len(names) != len(set(names)):
        raise ValueError("Every slide must have a unique nonempty id")
    theme_name = args.theme or plan.get("theme", "lab-light")
    theme = THEMES.get(theme_name)
    if not theme:
        raise ValueError(f"Unknown theme: {theme_name}")

    prs = Presentation()
    prs.slide_width, prs.slide_height = in_(W), in_(H)
    prs.core_properties.title = plan.get("title", "Scientific research presentation")
    prs.core_properties.subject = "Evidence-led scientific presentation"
    prs.core_properties.author = plan.get("author", "")

    for index, d in enumerate(slides, start=1):
        kind = d.get("type")
        if kind not in RENDERERS:
            raise ValueError(f"Unknown slide type {kind!r} in {d['id']}")
        if not d.get("title"):
            raise ValueError(f"Missing title on {d['id']}")
        if "sources" not in d:
            raise ValueError(f"Missing required sources list on {d['id']} (may be [])")
        if kind == "image_panel":
            RENDERERS[kind](prs, d, theme, index, len(slides), plan, args.plan.parent)
        else:
            RENDERERS[kind](prs, d, theme, index, len(slides), plan)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(args.out)
    print(f"Saved {len(prs.slides)} editable slides → {args.out}")


if __name__ == "__main__":
    main()
