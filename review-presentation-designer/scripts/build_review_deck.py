#!/usr/bin/env python3
"""Editable PowerPoint generator for scientific review presentations.

Render support: 15 review-first layouts. Native vector/text rather than slide screenshots.
This is a layout scaffold, not an autonomous scientific source-verification system.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt

W, H = 13.333, 7.5
C = dict(bg="F9FAF8", paper="FFFFFF", dark="132A40", ink="183044", muted="617482",
         teal="087E83", teal_pale="E8F4F3", amber="C58C3B", amber_pale="FBF3E6",
         purple="786C9F", purple_pale="F2EFF8", red="A65B5C", red_pale="F8EEEE",
         border="DAE5E7", line="C4D3DA", slate="F1F5F6", dark_muted="ADC3D2")
FONT = "Noto Sans CJK SC"
STATUS = {
    "source_reported": ("SOURCE-REPORTED", C["teal"]),
    "independently_verified": ("INDEPENDENTLY CHECKED", C["teal"]),
    "synthesis_inference": ("REVIEW INFERENCE", C["purple"]),
    "author_proposed": ("AUTHOR-PROPOSED", C["purple"]),
    "disputed": ("DISPUTED", C["red"]),
    "unresolved": ("UNRESOLVED", C["amber"]),
    "mixed_evidence": ("MIXED EVIDENCE", C["purple"]),
}


def I(v): return Inches(float(v))
def color(v): return RGBColor.from_string(str(v).lstrip("#").upper())


def shape_rect(slide, x, y, w, h, fill, outline=None, rounded=False, linewidth=0.8):
    obj = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        I(x), I(y), I(w), I(h))
    obj.fill.solid(); obj.fill.fore_color.rgb = color(fill)
    if outline:
        obj.line.color.rgb = color(outline); obj.line.width = Pt(linewidth)
    else:
        obj.line.fill.background()
    if rounded:
        try: obj.adjustments[0] = 0.08
        except Exception: pass
    return obj


def circ(slide, x, y, d, fill, stroke=None):
    obj = slide.shapes.add_shape(MSO_SHAPE.OVAL, I(x), I(y), I(d), I(d))
    obj.fill.solid(); obj.fill.fore_color.rgb = color(fill)
    if stroke: obj.line.color.rgb = color(stroke)
    else: obj.line.fill.background()
    return obj


def segment(slide, x1, y1, x2, y2, tone=None, width=1.3, dashed=False):
    obj = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                     I(x1), I(y1), I(x2), I(y2))
    obj.line.color.rgb = color(tone or C["line"])
    obj.line.width = Pt(width)
    if dashed:
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        obj.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return obj


def txt(slide, content, x, y, w, h, size=17, tone=None, bold=False, align="left",
        valign="top", italic=False, font=None, margin=0, tracking=None):
    t = slide.shapes.add_textbox(I(x), I(y), I(w), I(h))
    tf = t.text_frame; tf.clear(); tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = I(margin)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                          "bottom": MSO_ANCHOR.BOTTOM}[valign]
    for i, s in enumerate(str(content).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                       "right": PP_ALIGN.RIGHT}[align]
        p.line_spacing = 1.11
        p.space_before = Pt(0); p.space_after = Pt(0)
        r = p.add_run(); r.text = s
        r.font.name = font or FONT; r.font.size = Pt(size)
        r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = color(tone or C["ink"])
    return t


def marker(slide, label, x, y, tone=None, w=None, light=False):
    tone = tone or C["teal"]
    w = w or min(4.7, max(1.15, 0.12 * len(label) + 0.36))
    bg = (C["teal_pale"] if tone == C["teal"] else
          C["purple_pale"] if tone == C["purple"] else
          C["amber_pale"] if tone == C["amber"] else
          C["red_pale"] if tone == C["red"] else C["slate"])
    if light: bg, tone = "224258", "D6E9F1"
    shape_rect(slide, x, y, w, 0.34, bg, rounded=True)
    txt(slide, label, x+0.10, y+0.056, w-0.20, 0.24, size=10.1,
        tone=tone, bold=True)


def add_notes(slide, d, gd):
    parts = []
    if d.get("speaker_notes"): parts.append(str(d["speaker_notes"]))
    if d.get("claim_ids"): parts.append("CLAIM IDS: " + ", ".join(map(str, d["claim_ids"])))
    if d.get("source_ids"): parts.append("SOURCE IDS: " + ", ".join(map(str, d["source_ids"])))
    if d.get("caveat"): parts.append("CAVEAT: " + d["caveat"])
    if gd.get("mode") == "demo": parts.append("DEMO ONLY — NO PRIMARY-SOURCE VERIFICATION.")
    try: slide.notes_slide.notes_text_frame.text = "\n\n".join(parts)
    except Exception: pass


def bg(prs, dark=False, fill=None):
    s = prs.slides.add_slide(prs.slide_layouts[6]); shape_rect(s, 0, 0, W, H, fill or (C["dark"] if dark else C["bg"])); return s


def frame(slide, d, gd, n, total, dark=False):
    main = "EVIDENCE-LED  /  CRITICAL SYNTHESIS"
    if dark: return
    txt(slide, d.get("section", main), .70, .29, 8.1, .25, 10.5, C["teal"], bold=True)
    title = str(d.get("title", ""))
    fontsize = (29 if len(title) < 49 else 26) if gd.get("language") == "zh" else (30 if len(title) < 72 else 27)
    txt(slide, title, .70, .67, 12.05, .69, fontsize, C["ink"], bold=True)
    segment(slide, .70, 1.58, 12.67, 1.58, C["border"], 1.3)
    shape_rect(slide, .70, 1.565, .94, .047, C["teal"])
    epi = d.get("epistemic_status", "").lower().replace("-", "_")
    if gd.get("mode") == "demo":
        txt(slide, "DEMO  /  NOT SOURCE VERIFIED", 8.95, .29, 3.72, .23, 9.7, C["red"], bold=True, align="right")
    elif epi in STATUS:
        code, tone = STATUS[epi]
        txt(slide, code, 9.55, .29, 3.12, .23, 9.8, tone, bold=True, align="right")


def footer(slide, d, gd, n, total, dark=False):
    t = C["dark_muted"] if dark else C["muted"]
    if gd.get("mode") == "demo":
        txt(slide, "DEMO  ·  CONCEPTUAL CONTENT  ·  NOT SOURCE VERIFIED", .70, 7.105, 8.7, .23, 9.8,
            "CFDFE6" if dark else C["red"], bold=True)
    else:
        sources = ", ".join(map(str, d.get("source_ids", [])))
        if sources:
            txt(slide, "SOURCE  " + sources[:90], .70, 7.105, 8.6, .23, 9.8, t)
        elif d.get("epistemic_status"):
            txt(slide, STATUS.get(d["epistemic_status"].lower().replace("-", "_"),
                                  (d["epistemic_status"], t))[0], .70, 7.105, 8.6, .23, 9.8, t)
    txt(slide, f"{n:02d}  /  {total:02d}", 11.75, 7.105, .9, .23, 10, t, align="right")
    add_notes(slide, d, gd)


def draw_cover(prs, d, gd, n, total, root):
    s = bg(prs, True)
    shape_rect(s, 0, 0, .13, H, C["teal"])
    txt(s, "REVIEW  /  RESEARCH SYNTHESIS", .78, .52, 7, .32, 12, "9EBFCA", bold=True)
    title = d.get("title", gd.get("deck_title", "Scientific review"))
    font = 40 if len(title) < 54 else 35
    txt(s, title, .78, 1.40, 7.47, 2.20, font, "FFFFFF", bold=True)
    shape_rect(s, .80, 3.96, .92, .06, C["teal"])
    txt(s, d.get("subtitle", gd.get("subtitle", "")), .79, 4.32, 7.1, 1.26, 22, "C7D6E0")
    txt(s, d.get("author", gd.get("author", "")), .79, 6.43, 7.80, .38, 14, "C1D4DE")
    rx = 8.86
    for j, lab in enumerate(d.get("tags", ["MAP THE FIELD", "TEST EVIDENCE", "SYNTHESIZE"])[:3]):
        y = 1.75 + j*1.37
        shape_rect(s, rx, y, 3.67, 1.03, "1B3A51", outline="43627A", rounded=True)
        circ(s, rx + .23, y + .33, .35, C["teal"] if j==1 else "547085")
        txt(s, f"0{j+1}", rx + .29, y+.37, .29, .20, 12, "FFFFFF", bold=True)
        txt(s, lab, rx + .80, y + .31, 2.60, .48, 17, "FFFFFF" if j==1 else "C6D9E2", bold=True)
    footer(s, d, gd, n, total, True)


def draw_big_idea(prs, d, gd, n, total, root):
    s=bg(prs); frame(s,d,gd,n,total)
    shape_rect(s, .70, 2.05, 7.35, 4.73, C["paper"], outline=C["border"], rounded=True)
    shape_rect(s, .99, 2.40, .10, .75, C["teal"])
    txt(s, d.get("statement", d["title"]), 1.31, 2.37, 6.15, 2.18, 33, C["dark"], bold=True)
    segment(s, 1.31, 4.93, 7.54, 4.93, C["border"])
    txt(s, d.get("context", ""), 1.31, 5.16, 5.88, 1.10, 17, C["muted"])
    txt(s, "WHY THIS REVIEW MATTERS", 8.51, 2.11, 4.1, .36, 12, C["teal"], bold=True)
    pillars=d.get("pillars", [])[:3]
    for i,p in enumerate(pillars):
        y=2.66 + 1.31*i
        shape_rect(s, 8.48, y, 4.15, 1.12, C["slate"], rounded=True)
        txt(s, f"{i+1:02d}", 8.75, y+.28, .56, .43, 22, C["teal"], bold=True)
        txt(s, p, 9.42, y+.22, 2.91, .71, 17.2, C["ink"], bold=True)
    footer(s,d,gd,n,total)


def draw_scope(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    columns=d.get("columns", [])[:3]
    tones=[C["teal"], C["amber"], C["purple"]]
    for i,col in enumerate(columns):
        x=.71+i*4.02
        shape_rect(s,x,2.05,3.79,4.57,C["paper"],outline=C["border"],rounded=True)
        shape_rect(s,x,2.05,3.79,.065,tones[i])
        txt(s,col.get("heading",""),x+.27,2.39,3.24,.62,22,C["ink"],bold=True)
        txt(s,col.get("body",""),x+.27,3.13,3.19,.92,16.5,C["muted"])
        segment(s,x+.27,4.20,x+3.49,4.20,C["border"])
        for j,item in enumerate(col.get("items",[])[:3]):
            yy=4.40+j*.62
            circ(s,x+.27,yy+.13,.09,tones[i]); txt(s,item,x+.49,yy,2.94,.55,15.5,C["ink"])
    footer(s,d,gd,n,total)


def draw_taxonomy(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    shape_rect(s,2.75,2.03,7.85,.69,C["dark"],rounded=True)
    txt(s,d.get("parent","Scientific question / taxonomy axis"),3.02,2.20,7.31,.36,20,"FFFFFF",bold=True,align="center")
    items=d.get("items",[])[:4]; k=len(items); gap=.18; cw=(12.0-gap*(k-1))/max(1,k)
    xs=[.67+i*(cw+gap) for i in range(k)]
    segment(s,6.67,2.72,6.67,3.10,C["line"],1.45)
    if xs:
        segment(s,xs[0]+cw/2,3.10,xs[-1]+cw/2,3.10,C["line"],1.45)
    tones=[C["teal"],C["purple"],C["amber"],C["teal"]]
    for i,item in enumerate(items):
        x=xs[i]
        segment(s,x+cw/2,3.10,x+cw/2,3.29,C["line"],1.4)
        shape_rect(s,x,3.29,cw,2.53,C["paper"],outline=C["border"],rounded=True)
        shape_rect(s,x,3.29,cw,.06,tones[i])
        txt(s,item.get("tag",f"T{i+1}"),x+.25,3.60,cw-.5,.31,12.5,tones[i],bold=True)
        txt(s,item.get("label",""),x+.25,4.10,cw-.47,.68,22 if k<=3 else 20,C["ink"],bold=True)
        txt(s,item.get("body",""),x+.25,4.96,cw-.50,.63,15.6 if k<=3 else 14.5,C["muted"])
    shape_rect(s,.69,6.06,11.96,.63,C["teal_pale"],rounded=True)
    txt(s,d.get("takeaway","Categories reflect an explicit operational rule, not performance ordering."),.93,6.22,11.48,.31,16.3,C["teal"],bold=True)
    footer(s,d,gd,n,total)


def draw_mechanisms(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    items=d.get("items",[])[:3]; k=len(items); gap=.21; cw=(12.01-gap*(k-1))/k
    tones=[C["teal"],C["purple"],C["amber"]]
    for i,item in enumerate(items):
        x=.67+i*(cw+gap); tone=tones[i]
        shape_rect(s,x,1.98,cw,4.87,C["paper"],outline=C["border"],rounded=True)
        shape_rect(s,x,1.98,cw,.067,tone)
        txt(s,item.get("label",f"ROLE {i+1}"),x+.25,2.20,cw-.48,.35,11,tone,bold=True)
        txt(s,item.get("role",""),x+.25,2.62,cw-.45,.55,21,C["ink"],bold=True)
        ww=(cw-.87)/2
        shape_rect(s,x+.29,3.40,ww,.55,C["teal_pale"],rounded=True)
        shape_rect(s,x+.58+ww,3.40,ww,.55,C["amber_pale"],rounded=True)
        txt(s,item.get("input_a","Drug tokens"),x+.33,3.53,ww-.07,.26,12.6,C["teal"],bold=True,align="center")
        txt(s,item.get("input_b","Protein tokens"),x+.63+ww,3.53,ww-.08,.26,12.6,C["amber"],bold=True,align="center")
        txt(s,"↘",x+.92,3.91,.45,.38,19,C["muted"],bold=True)
        txt(s,"↙",x+cw-1.27,3.91,.45,.38,19,C["muted"],bold=True)
        shape_rect(s,x+.53,4.38,cw-1.07,.76,C["slate"],outline=C["border"],rounded=True)
        txt(s,item.get("operator","Interaction operator"),x+.66,4.56,cw-1.33,.39,17,C["ink"],bold=True,align="center")
        txt(s,"↓",x+cw/2-.20,5.16,.40,.36,18,C["muted"],align="center")
        shape_rect(s,x+.81,5.62,cw-1.62,.52,tone,rounded=True)
        txt(s,item.get("output","Pair representation"),x+.94,5.72,cw-1.88,.28,12.4,"FFFFFF",bold=True,align="center")
        txt(s,item.get("note",""),x+.30,6.35,cw-.6,.40,12.5,C["muted"])
    footer(s,d,gd,n,total)


def draw_lanes(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    items=d.get("items",[])[:4]; k=len(items); gap=.15; cw=(12.01-gap*(k-1))/k
    tones=[C["teal"],C["amber"],C["purple"],C["red"]]
    for i,item in enumerate(items):
        x=.67+i*(cw+gap); tone=tones[i]
        shape_rect(s,x,2.04,cw,4.74,C["paper"],outline=C["border"],rounded=True)
        shape_rect(s,x,2.04,cw,.078,tone)
        txt(s,item.get("code",str(i+1)),x+.23,2.34,.80,.72,43,tone,bold=True)
        txt(s,item.get("label",""),x+.25,3.18,cw-.49,.69,19,C["ink"],bold=True)
        txt(s,item.get("question",""),x+.25,4.12,cw-.50,1.00,16.6,C["ink"])
        segment(s,x+.26,5.33,x+cw-.27,5.33,C["border"])
        txt(s,"EVIDENCE TEST",x+.27,5.53,cw-.55,.22,10.5,tone,bold=True)
        txt(s,item.get("tests",""),x+.27,5.85,cw-.52,.73,14.4,C["muted"])
    footer(s,d,gd,n,total)


def draw_comparability(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    txt(s,"CHECK THE CONDITIONS",.78,1.92,7.5,.31,11,C["teal"],bold=True)
    checks=d.get("checks",[])[:5]
    for i,v in enumerate(checks):
        y=2.41+i*.83
        shape_rect(s,.74,y,7.21,.68,C["paper"],outline=C["border"],rounded=True)
        circ(s,1.00,y+.19,.29,C["teal_pale"])
        txt(s,str(i+1),1.08,y+.219,.15,.18,11.4,C["teal"],bold=True)
        txt(s,v,1.49,y+.19,6.14,.38,17.5,C["ink"],bold=True)
    segment(s,8.13,4.40,8.58,4.40,C["line"],1.8)
    txt(s,"COMPARISON CLAIM",8.76,1.91,3.75,.32,11,C["teal"],bold=True)
    outcomes=d.get("outcomes",[])[:3]
    tones=[C["teal"],C["amber"],C["red"]]
    for j,o in enumerate(outcomes):
        y=2.44+j*1.35
        shape_rect(s,8.65,y,3.96,1.11,C["paper"],outline=C["border"],rounded=True)
        shape_rect(s,8.65,y,.08,1.11,tones[j])
        txt(s,o.get("label",""),8.93,y+.16,3.37,.33,17.7,tones[j],bold=True)
        txt(s,o.get("body",""),8.93,y+.61,3.37,.37,12.6,C["muted"])
    footer(s,d,gd,n,total)


def draw_matrix(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    columns=d.get("columns",[])[:5]; rows=d.get("rows",[])[:6]
    x0=.70; width=11.96; cols=len(columns); widths=[width/cols]*cols
    if cols>1: widths=[width*.23]+[width*.77/(cols-1)]*(cols-1)
    xp=[x0]
    for ww in widths: xp.append(xp[-1]+ww)
    shape_rect(s,x0,2.03,width,.57,C["dark"])
    for j,lab in enumerate(columns): txt(s,lab,xp[j]+.17,2.18,widths[j]-.33,.30,14.3,"FFFFFF",bold=True)
    rh=min(.72,3.68/max(1,len(rows)))
    for i,row in enumerate(rows):
        y=2.60+i*rh
        shape_rect(s,x0,y,width,rh,C["paper"] if i%2==0 else C["slate"])
        for j in range(cols):
            v=row[j] if j<len(row) else "—"
            txt(s,v,xp[j]+.17,y+.17,widths[j]-.32,rh-.18,13.2 if cols>=5 else 14.5,
                C["teal"] if j==0 else C["ink"],bold=(j==0))
        segment(s,x0,y+rh,x0+width,y+rh,C["border"],.55)
    caveat = d.get("takeaway","") or ("Comparisons are conditional on matched task/split/context." if d.get("comparison_mode")!="matched" else "Matched conditions explicitly checked.")
    shape_rect(s,.72,6.28,11.93,.57,C["amber_pale"] if d.get("comparison_mode")!="matched" else C["teal_pale"],rounded=True)
    txt(s,caveat,.95,6.42,11.38,.30,15.1,C["muted"],bold=True)
    footer(s,d,gd,n,total)


def draw_evidence_map(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    txt(s,"CLAIM",1.00,1.94,4.1,.25,11,C["muted"],bold=True)
    txt(s,"EPISTEMIC STATUS",7.19,1.94,2.13,.25,11,C["muted"],bold=True)
    txt(s,"SOURCE / GAP",9.52,1.94,2.74,.25,11,C["muted"],bold=True)
    tones={"source-reported":C["teal"],"author-proposed":C["purple"],"inference":C["purple"],
           "disputed":C["red"],"unresolved":C["amber"],"independently-checked":C["teal"]}
    for i,item in enumerate(d.get("items",[])[:4]):
        y=2.28+i*1.11
        shape_rect(s,.72,y,11.92,.93,C["paper"],outline=C["border"],rounded=True)
        circ(s,.95,y+.37,.12,C["teal"])
        txt(s,item.get("claim",""),1.24,y+.22,5.66,.58,16.5,C["ink"],bold=True)
        sta=item.get("status","unresolved").lower()
        tone=tones.get(sta,C["muted"])
        marker(s,sta.upper(),7.08,y+.27,tone,2.03)
        txt(s,item.get("source",item.get("limitation","")),9.48,y+.18,2.72,.62,13.6,C["muted"])
    txt(s,d.get("takeaway",""),.82,6.79,11.7,.24,12.5,C["teal"],bold=True)
    footer(s,d,gd,n,total)


def draw_timeline(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    tracks=d.get("tracks",[])[:3]; tones=[C["teal"],C["purple"],C["amber"]]
    for i,track in enumerate(tracks):
        y=2.06+i*1.55; tone=tones[i]
        shape_rect(s,.71,y,2.00,1.25,C["paper"],outline=C["border"],rounded=True)
        shape_rect(s,.71,y,.07,1.25,tone)
        txt(s,track.get("label",""),.94,y+.27,1.55,.72,18.0,C["ink"],bold=True)
        segment(s,3.07,y+.65,12.43,y+.65,C["line"],1.8)
        nodes=track.get("nodes",[])[:3]
        step=3.1
        for j,node in enumerate(nodes):
            xx=3.29+j*step
            circ(s,xx,y+.515,.26,tone)
            shape_rect(s,xx-.19,y-.06,2.70,.46,C["paper"],rounded=True)
            txt(s,node.get("time",""),xx-.05,y-.02,2.49,.31,11.2,tone,bold=True)
            txt(s,node.get("label",""),xx-.06,y+.82,2.85,.43,15.0,C["ink"],bold=True)
    txt(s,d.get("takeaway","Chronological position does not establish technical lineage."),.75,6.76,11.6,.23,12.4,C["muted"])
    footer(s,d,gd,n,total)


def draw_debate(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    halves=[d.get("left",{}),d.get("right",{})]
    tones=[C["teal"],C["amber"]]
    for i,half in enumerate(halves):
        x=.72+i*6.08; tone=tones[i]
        shape_rect(s,x,2.02,5.85,3.88,C["paper"],outline=C["border"],rounded=True)
        shape_rect(s,x,2.02,5.85,.065,tone)
        txt(s,half.get("heading",""),x+.32,2.41,5.20,.70,22,C["ink"],bold=True)
        txt(s,half.get("body",""),x+.32,3.34,5.12,1.36,18,C["muted"])
        segment(s,x+.32,4.95,x+5.52,4.95,C["border"])
        txt(s,half.get("evidence",""),x+.32,5.12,5.12,.63,14,tone,bold=True)
    shape_rect(s,.73,6.15,11.93,.69,C["teal_pale"],rounded=True)
    txt(s,d.get("resolution",d.get("takeaway","")),.98,6.31,11.35,.38,16.6,C["teal"],bold=True)
    footer(s,d,gd,n,total)


def draw_agenda(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    tones=[C["teal"],C["purple"],C["amber"]]
    for i,item in enumerate(d.get("items",[])[:3]):
        x=.71+i*4.02; tone=tones[i]
        shape_rect(s,x,2.07,3.78,4.64,C["paper"],outline=C["border"],rounded=True)
        txt(s,str(item.get("number",f"0{i+1}")),x+.28,2.37,1.21,.78,42,tone,bold=True)
        txt(s,item.get("heading",""),x+.28,3.27,3.19,.71,21.6,C["ink"],bold=True)
        txt(s,item.get("method",""),x+.28,4.20,3.18,.97,16.4,C["muted"])
        segment(s,x+.28,5.45,x+3.50,5.45,C["border"])
        txt(s,"DELIVERABLE",x+.29,5.65,3.07,.24,10.8,tone,bold=True)
        txt(s,item.get("deliverable",""),x+.29,6.00,3.13,.58,14.6,C["ink"],bold=True)
    footer(s,d,gd,n,total)


def draw_synthesis(prs,d,gd,n,total,root):
    s=bg(prs); frame(s,d,gd,n,total)
    items=d.get("items",[])[:4]
    tones=[C["teal"],C["purple"],C["amber"],C["red"]]
    for i,item in enumerate(items):
        x=.70+(i%2)*6.07; y=2.04+(i//2)*2.37
        shape_rect(s,x,y,5.86,2.18,C["paper"],outline=C["border"],rounded=True)
        shape_rect(s,x,y,.075,2.18,tones[i])
        txt(s,item.get("status","").upper(),x+.28,y+.25,5.2,.27,10.7,tones[i],bold=True)
        txt(s,item.get("title",""),x+.28,y+.66,5.22,.64,21,C["ink"],bold=True)
        txt(s,item.get("body",""),x+.28,y+1.49,5.15,.53,15,C["muted"])
    footer(s,d,gd,n,total)


def draw_figure(prs,d,gd,n,total,root):
    from PIL import Image
    s=bg(prs); frame(s,d,gd,n,total)
    p=Path(d.get("path",""))
    if not p.is_absolute(): p=(root/p).resolve()
    if not p.exists(): raise FileNotFoundError(f"Figure path is missing: {p}")
    shape_rect(s,.72,1.98,8.40,4.86,C["paper"],outline=C["border"],rounded=True)
    with Image.open(p) as img: iw,ih=img.size
    maxw,maxh=7.98,4.45
    scale=min(maxw/iw,maxh/ih)
    pw,ph=iw*scale,ih*scale
    s.shapes.add_picture(str(p),I(.93+(maxw-pw)/2),I(2.18+(maxh-ph)/2),width=I(pw),height=I(ph))
    shape_rect(s,9.34,1.98,3.32,4.85,C["teal_pale"],rounded=True)
    txt(s,"FIGURE  /  PROVENANCE",9.64,2.27,2.71,.25,11,C["teal"],bold=True)
    txt(s,d.get("caption",""),9.64,2.92,2.70,1.75,19.2,C["ink"],bold=True)
    segment(s,9.64,5.05,12.36,5.05,C["border"])
    txt(s,d.get("credit","Unknown credit"),9.64,5.30,2.65,1.01,13.8,C["muted"])
    footer(s,d,gd,n,total)


def draw_closing(prs,d,gd,n,total,root):
    s=bg(prs,True)
    shape_rect(s,0,0,.13,H,C["teal"])
    txt(s,"SYNTHESIS  /  OPEN QUESTIONS",.78,.48,9,.34,11.9,"9FC4CC",bold=True)
    txt(s,d.get("statement",d.get("title","")),.78,1.51,10.83,1.75,38,"FFFFFF",bold=True)
    segment(s,.80,3.68,12.48,3.68,"49677B",1.5)
    for i,p in enumerate(d.get("points",[])[:3]):
        y=4.22+i*.79
        circ(s,.84,y+.13,.18,C["teal"])
        txt(s,p,1.22,y,11.03,.53,20,"CFDEE7")
    footer(s,d,gd,n,total,True)


DRAW={"cover":draw_cover,"big_idea":draw_big_idea,"scope":draw_scope,
      "taxonomy":draw_taxonomy,"mechanisms":draw_mechanisms,"lanes":draw_lanes,
      "comparability":draw_comparability,"matrix":draw_matrix,"evidence_map":draw_evidence_map,
      "timeline":draw_timeline,"debate":draw_debate,"agenda":draw_agenda,
      "synthesis":draw_synthesis,"figure":draw_figure,"closing":draw_closing}


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--plan",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    a.add_argument("--claims",type=Path,help="Required in production mode")
    a.add_argument("--sources",type=Path,help="Required in production mode")
    a.add_argument("--notes-out",type=Path,help="Export readable presentation speaker notes Markdown")
    args=a.parse_args()
    gd=json.loads(args.plan.read_text(encoding="utf-8"))
    if gd.get("mode","production")=="production":
        if not args.claims or not args.sources:
            a.error("Production mode requires --claims and --sources to validate provenance")
        from validate_review_plan import load_csv, validate
        report=validate(gd,load_csv(args.claims),load_csv(args.sources),strict=True,plan_dir=args.plan.parent)
        if report["errors"]:
            for r in report["messages"][:20]: print(r,file=sys.stderr)
            a.error(f"Provenance validation failed: {report['errors']} errors")
        print("Provenance ID/status checks passed (NOT independent primary-source verification).")
    prs=Presentation(); prs.slide_width=I(W); prs.slide_height=I(H)
    root=args.plan.parent
    slides=gd.get("slides",[])
    for i,d in enumerate(slides,start=1):
        t=d.get("type")
        if t not in DRAW: raise ValueError(f"Unsupported layout: {t}")
        DRAW[t](prs,d,gd,i,len(slides),root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(args.out)
    notes_out = args.notes_out or (args.out.parent / "speaker_notes.md")
    buf = ["# Review presentation — speaker notes", "", "*Sources and claim IDs require independent inspection of original literature.*", ""]
    for i, d in enumerate(slides, 1):
        buf += [f"## Slide {i:02d} — {d.get('title', '')}", ""]
        if d.get("claim_ids"): buf += ["Claim IDs: " + ", ".join(map(str,d["claim_ids"])), ""]
        if d.get("source_ids"): buf += ["Source IDs: " + ", ".join(map(str,d["source_ids"])), ""]
        if d.get("speaker_notes"): buf += [str(d["speaker_notes"]), ""]
        if d.get("caveat"): buf += ["Caveat: " + str(d["caveat"]), ""]
    if gd.get("mode") == "demo": buf += ["---", "DEMO ONLY — material not verified against primary sources.", ""]
    notes_out.parent.mkdir(parents=True, exist_ok=True)
    notes_out.write_text("\n".join(buf), encoding="utf-8")
    print(f"Created {len(prs.slides)} editable review slides -> {args.out}; speaker notes -> {notes_out}")
    print("This process does not verify source text, dates, DOI or scientific conclusions.")

if __name__=="__main__": main()
