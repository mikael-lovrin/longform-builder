# -*- coding: utf-8 -*-
"""
build_batch_docx.py — Phase 6.

(1) Builds the delivery .docx of a batch, in the house document standard:
    Arial 12pt, 1.5 line spacing, black, headings in ALL CAPS and bold.
(2) Builds the round upload sheet (upload.csv), one row per ad, already carrying
    the classification columns that creative-intel will read afterwards.

Usage:
    python build_batch_docx.py --draft drafts/B1-A.md --out "AA BRAND-SKU T101-B1-A.docx"
    python build_batch_docx.py --folder drafts/ --test T101 --product BRAND-SKU   # all of them
    python build_batch_docx.py --sheet --folder drafts/ --test T101 --product BRAND-SKU \
           --destination "https://..." --campaign "T101 Long Form" --out upload.csv
"""
import argparse, csv, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BLACK = RGBColor(0, 0, 0)
ETHNICITY = {"1": "White American", "2": "Black", "3": "Latino"}
DEFAULT_AUTHOR = "AA"

# ------------------------------------------------------------------ parsing
def parse_front(txt):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.S)
    if not m:
        return {}, txt
    fm, body = {}, txt[m.end():]
    for line in m.group(1).split("\n"):
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        fm[k.strip()] = v
    return fm, body

def section(body, *titles):
    for t in titles:
        m = re.search(r"^##\s*%s\s*$" % re.escape(t), body, re.M | re.I)
        if m:
            rest = body[m.end():]
            n = re.search(r"^##\s+", rest, re.M)
            return (rest[:n.start()] if n else rest).strip()
    return ""

# ------------------------------------------------------------------ docx
def _run(run, size=12, bold=False):
    run.font.name = "Arial"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = BLACK
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia"):
        rf.set(qn(attr), "Arial")

def new_doc():
    doc = Document()
    s = doc.sections[0]
    s.top_margin, s.left_margin = Cm(3), Cm(3)
    s.bottom_margin, s.right_margin = Cm(2), Cm(2)
    n = doc.styles["Normal"]
    n.font.name = "Arial"; n.font.size = Pt(12); n.font.color.rgb = BLACK
    pf = n.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    pf.space_after = Pt(10)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return doc

def heading(doc, text, center=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    _run(p.add_run(text.upper()), 12, bold=True)
    return p

def body_text(doc, text, justify=True):
    for block in [b for b in text.split("\n") if b.strip()]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(10)
        _run(p.add_run(block.strip()), 12, bold=False)

def build_docx(md_path, out_path, extra=None):
    fm, body = parse_front(Path(md_path).read_text(encoding="utf-8"))
    extra = extra or {}
    doc_id = fm.get("id") or Path(out_path).stem

    primary = section(body, "PRIMARY TEXT")
    first3 = section(body, "FIRST 3 LINES (what shows before see more)",
                     "FIRST 3 LINES")
    head = section(body, "LINK HEADLINE")
    desc = section(body, "LINK DESCRIPTION")
    cta = section(body, "CTA")
    angle_txt = section(body, "ANGLE") or extra.get("angle_desc", "")
    level_txt = section(body, "AWARENESS LEVEL") or extra.get("level_desc", "")
    avatar_txt = section(body, "AVATARS", "AVATAR")

    doc = new_doc()

    # 1. document name
    heading(doc, doc_id, center=True)

    # 2. angle
    heading(doc, "angle")
    body_text(doc, angle_txt or "%s" % fm.get("angle", ""))

    # 3. awareness level
    heading(doc, "awareness level")
    body_text(doc, level_txt or "Level %s." % fm.get("level", ""))

    # 4. avatars
    heading(doc, "avatars")
    if avatar_txt:
        body_text(doc, avatar_txt)
    else:
        base = Path(out_path).stem
        for k in ("1", "2", "3"):
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
            p.paragraph_format.line_spacing = 1.5
            _run(p.add_run("Avatar %s (%s), %s%s.  " % (k, ETHNICITY[k], base, k)), 12, bold=True)
            _run(p.add_run(extra.get("avatar_%s" % k,
                 "The locked scene of the batch, identical to the other variations. "
                 "The only variable is ethnicity.")), 12)

    # 5. primary text
    heading(doc, "primary text (%d characters)" % len(primary))
    body_text(doc, primary)

    # 6. first three lines
    if first3:
        heading(doc, "first three lines (%d characters)" % len(first3))
        body_text(doc, first3)

    # 7-9. placement
    for t, v in (("link headline", head), ("link description", desc), ("cta", cta)):
        if v:
            heading(doc, "%s (%d characters)" % (t, len(v)) if t != "cta" else t)
            body_text(doc, v, justify=False)

    # 10. files
    heading(doc, "image files")
    base = Path(out_path).stem
    body_text(doc, "\n".join("%s%s.png" % (base, k) for k in ("1", "2", "3")), justify=False)

    doc.save(out_path)
    return out_path, len(primary)

# ------------------------------------------------------------------ sheet
def build_sheet(folder, test, product, destination, campaign, out, author=DEFAULT_AUTHOR):
    rows = []
    for md in sorted(Path(folder).glob("*.md")):
        fm, body = parse_front(md.read_text(encoding="utf-8"))
        m = re.search(r"B(\d)-([ABC])", md.stem)
        if not m:
            continue
        b, level = m.group(1), m.group(2)
        base = "%s %s %s-B%s-%s" % (author, product, test, b, level)
        primary = section(body, "PRIMARY TEXT")
        head = section(body, "LINK HEADLINE")
        desc = section(body, "LINK DESCRIPTION")
        cta = section(body, "CTA") or "Learn More"
        for v in ("1", "2", "3"):
            rows.append({
                "campaign": campaign or "%s Long Form" % test,
                "ad_set": "%s-B%s-%s" % (test, b, level),
                "ad": "%s%s" % (base, v),
                "image": "%s%s.png" % (base, v),
                "primary_text": primary,
                "headline": head,
                "description": desc,
                "cta": cta,
                "destination": destination or "",
                "angle": fm.get("angle", "B%s" % b),
                "level": level,
                "variation": v,
                "ethnicity": ETHNICITY[v],
                "chars": len(primary),
            })
    if not rows:
        print("No valid draft found in %s" % folder); return
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)
    print("upload sheet: %s  (%d ads, %d ad sets)"
          % (out, len(rows), len({r['ad_set'] for r in rows})))

# ------------------------------------------------------------------ cli
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft"); ap.add_argument("--folder")
    ap.add_argument("--out"); ap.add_argument("--sheet", action="store_true")
    ap.add_argument("--test", default="T101"); ap.add_argument("--product", default="BRAND-SKU")
    ap.add_argument("--author", default=DEFAULT_AUTHOR)
    ap.add_argument("--destination", default=""); ap.add_argument("--campaign", default="")
    a = ap.parse_args()

    if a.sheet:
        build_sheet(a.folder or "drafts", a.test, a.product, a.destination,
                    a.campaign, a.out or "upload.csv", a.author)
        return
    if a.draft:
        out, n = build_docx(a.draft, a.out or (Path(a.draft).stem + ".docx"))
        print("built: %s  (%d chars of copy)" % (out, n)); return
    if a.folder:
        for md in sorted(Path(a.folder).glob("*.md")):
            m = re.search(r"B(\d)-([ABC])", md.stem)
            if not m:
                continue
            out = "%s %s %s-B%s-%s.docx" % (a.author, a.product, a.test, m.group(1), m.group(2))
            _, n = build_docx(md, out)
            print("built: %s  (%d chars)" % (out, n))
        return
    ap.error("pass --draft, --folder or --sheet")

if __name__ == "__main__":
    main()
