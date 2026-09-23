# -*- coding: utf-8 -*-
"""
build_batch_docx.py — Phase 6.

(1) Builds two .docx per batch, in the house document standard:
    Arial 12pt, 1.5 line spacing, black, headings in ALL CAPS and bold.
      AA BRAND-SKU T###-B1-A/AA BRAND-SKU T###-B1-A.docx   only the copy (primary text +
                                                          first 3 lines), in the cell folder
                                                          next to the 3 images
      infos/AA BRAND-SKU T###-B1-A INFOS.docx   angle, awareness level and the 3 image prompts
(2) Builds the round upload sheet (upload.csv), one row per ad, already carrying
    the classification columns that creative-intel will read afterwards.
    Headline, description and CTA live only in this sheet, never in a docx.

The INFOS prompts are read from image-brief.md, so the document carries the real
prompt that generated each image.
Awareness levels (default): A Problem aware, B Solution aware, C Hidden cause.

Usage:
    python build_batch_docx.py --draft drafts/B1-A.md   (writes to AA BRAND-SKU T101-B1-A/)
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

# ------------------------------------------------------------------ image brief
LEVELS = {"A": "Problem aware", "B": "Solution aware", "C": "Hidden cause"}

def read_brief(cell, path="image-brief.md"):
    """Locked scene of the cell + the label of each variation (from its #### header)."""
    p = Path(path)
    if not p.exists():
        return None
    txt = p.read_text(encoding="utf-8")
    # the lookahead must exclude '####', otherwise the block closes at the first variation
    pat_cell = r"^###[^#\n][^\n]*\b" + re.escape(cell) + r"\b(.*?)(?=^###[^#]|\Z)"
    m = re.search(pat_cell, txt, re.M | re.S)
    if not m:
        return None
    block = m.group(0)
    scene = ""
    ms = re.search(r"\*\*Locked scene:?\*\*\s*([^\n]+)", block)
    if ms:
        scene = ms.group(1).strip()
    labels = {}
    # '.' does not match newlines without DOTALL, so this only takes the header line
    pat_lab = r"^####.*?" + re.escape(cell) + r"(\d)(.*)$"
    for ml in re.finditer(pat_lab, block, re.M):
        labels[ml.group(1)] = ml.group(2).strip().lstrip("-" + chr(8212) + chr(8211) + " ").strip()
    return {"scene": scene, "labels": labels}

def read_prompts(cell, path="image-brief.md"):
    """Full prompt of each variation of the cell, keyed by '1', '2', '3'."""
    p = Path(path)
    if not p.exists():
        return {}
    txt = p.read_text(encoding="utf-8")
    out = {}
    pat = r"^####[^\n]*\b" + re.escape(cell) + r"(\d)\b[^\n]*\n(.*?)(?=^#{3,4}\s|\Z)"
    for m in re.finditer(pat, txt, re.M | re.S):
        pm = re.search(r"\*\*Prompt:?\*\*\s*\n(.*)", m.group(2), re.S)
        out[m.group(1)] = (pm.group(1) if pm else m.group(2)).strip()
    return out

def cell_path(author, product, test, cell):
    """Each cell has its own folder holding the copy docx and the 3 images:
    AA BRAND-SKU T101-B1-A/AA BRAND-SKU T101-B1-A.docx"""
    name = "%s %s %s-%s" % (author, product, test, cell)
    Path(name).mkdir(exist_ok=True)
    return str(Path(name) / (name + ".docx"))

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

def lead_text(doc, lead, text):
    """Paragraph with a bold lead followed by regular text."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(10)
    _run(p.add_run(lead), 12, bold=True)
    _run(p.add_run(text), 12, bold=False)
    return p

def build_docx(md_path, out_path, brief="image-brief.md", infos_dir="infos"):
    fm, body = parse_front(Path(md_path).read_text(encoding="utf-8"))
    doc_id = fm.get("id") or Path(out_path).stem

    primary = section(body, "PRIMARY TEXT")
    first3 = section(body, "FIRST 3 LINES (what shows before see more)",
                     "FIRST 3 LINES")
    angle_txt = section(body, "ANGLE")
    base = Path(out_path).stem
    mcell = re.search(r"(B\d)-([ABC])", base)
    cell = mcell.group(0) if mcell else ""
    level = mcell.group(2) if mcell else str(fm.get("level", ""))

    # document 1: literally only the copy. It is the file that goes to whoever
    # uploads the ad, so no title, angle, avatars, headline, description or CTA.
    doc = new_doc()
    body_text(doc, primary)
    if first3:
        heading(doc, "first three lines (%d characters)" % len(first3))
        body_text(doc, first3)
    doc.save(out_path)

    # document 2: batch infos, with the real prompt of each image
    b = read_brief(cell, brief) if cell else None
    prompts = read_prompts(cell, brief) if cell else {}
    labels = (b or {}).get("labels", {})
    info = new_doc()
    heading(info, doc_id, center=True)
    heading(info, "angle")
    if fm.get("angle"):
        lead_text(info, "%s." % fm["angle"], "")
    body_text(info, angle_txt)
    heading(info, "awareness level")
    body_text(info, "%s (%s)" % (LEVELS.get(level, level), level))
    heading(info, "image prompts")
    if b and b.get("scene"):
        lead_text(info, "Locked scene. ", b["scene"])
    for k in ("1", "2", "3"):
        lead_text(info, "Image %s, %s. " % (k, labels.get(k) or ETHNICITY[k]),
                  "File %s%s.png" % (base, k))
        body_text(info, prompts.get(k, ""), justify=False)
    # INFOS lives outside the cell folder, which only holds the copy docx and the 3 images
    folder = Path(infos_dir)
    folder.mkdir(exist_ok=True)
    info.save(folder / ("%s INFOS.docx" % base))
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
    ap.add_argument("--brief", default="image-brief.md")
    ap.add_argument("--destination", default=""); ap.add_argument("--campaign", default="")
    a = ap.parse_args()

    if a.sheet:
        build_sheet(a.folder or "drafts", a.test, a.product, a.destination,
                    a.campaign, a.out or "upload.csv", a.author)
        return
    if a.draft:
        out = a.out or cell_path(a.author, a.product, a.test, Path(a.draft).stem)
        out, n = build_docx(a.draft, out, a.brief)
        print("built: %s  (%d chars of copy)" % (out, n)); return
    if a.folder:
        for md in sorted(Path(a.folder).glob("*.md")):
            m = re.search(r"B(\d)-([ABC])", md.stem)
            if not m:
                continue
            out = cell_path(a.author, a.product, a.test, "B%s-%s" % (m.group(1), m.group(2)))
            _, n = build_docx(md, out, a.brief)
            print("built: %s  (%d chars)" % (out, n))
        return
    ap.error("pass --draft, --folder or --sheet")

if __name__ == "__main__":
    main()
