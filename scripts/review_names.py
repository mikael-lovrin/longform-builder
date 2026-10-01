# -*- coding: utf-8 -*-
"""
review_names.py — naming review for a round (Phase 6, before upload).

Reads the test folder, parses the name of every folder/file and prints what it
understood (test, funnel stage, format, author, batches, variations), cross-checked
against the main docx, the draft, tracking/batches.json and upload.csv.

Usage:
    python review_names.py "<test folder>"           # one round
    python review_names.py "<creatives folder>"      # every T### round that has batches

Output: a summary to confirm + a list of ERROR/WARNING. Exit code 1 if there is any ERROR.
"""
import argparse, csv, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FUNNELS = {"TF": "Top of funnel", "FF": "Bottom of funnel"}
CTA_BY_FUNNEL = {"TF": "Learn more", "FF": "Shop now"}
FORMATS = {"BLF": "Long form", "BS": "Static (image)", "BV": "Video", "B": "Legacy batch (no format)"}
MEDIA_EXT = {".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov"}
SUPPORT_DIRS = {"support", "drafts", "tracking", "audio", "profiles", "__pycache__"}

RE_ROUND = re.compile(r"^(T\d+)-(TF|FF)\s*-\s*(\d{4})\s*\[(.+)\]$")
RE_BATCH = re.compile(r"^(\S+) (\S+) (T\d+)-(TF|FF)-(BLF|BS|BV|B)(\d+)$")
RE_ANY_ROUND = re.compile(r"^T\d+")


class Report:
    def __init__(self):
        self.items = []  # (level, where, msg)

    def error(self, where, msg):
        self.items.append(("ERROR", where, msg))

    def warn(self, where, msg):
        self.items.append(("WARNING", where, msg))

    @property
    def n_errors(self):
        return sum(1 for i in self.items if i[0] == "ERROR")


def read_docx(path):
    """Fields of the main docx: the label sits on one line, the content on the lines below."""
    try:
        import docx
    except ImportError:
        return None
    d = docx.Document(str(path))
    lines = [p.text.strip() for p in d.paragraphs]
    labels = {"ANGLE", "AWARENESS LEVEL", "PROFILE", "HEADLINE", "DESCRIPTION", "CTA", "COPY"}
    out, current = {"_title": lines[0] if lines else ""}, None
    for l in lines[1:]:
        if l.upper() in labels:
            current = l.upper()
            out[current] = []
            continue
        if current and l:
            out[current].append(l)
    copy = [l for l in out.get("COPY", []) if l != "."]
    return {
        "title": out["_title"],
        "angle": (out.get("ANGLE") or [""])[0],
        "level": (out.get("AWARENESS LEVEL") or [""])[0],
        "profile": (out.get("PROFILE") or [""])[0],
        "headline": " ".join(out.get("HEADLINE", [])),
        "description": " ".join(out.get("DESCRIPTION", [])),
        "cta": (out.get("CTA") or [""])[0],
        "opening": copy[0] if copy else "",
        "chars": sum(len(l) for l in copy),
    }


def read_frontmatter(path):
    if not path.exists():
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    fm = {}
    if m:
        for l in m.group(1).splitlines():
            if ":" in l:
                k, v = l.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def read_upload(folder):
    p = folder / "upload.csv"
    if not p.exists():
        return None
    txt = p.read_text(encoding="utf-8-sig")
    head = txt.split("\n", 1)[0]
    sep = ";" if head.count(";") >= head.count(",") else ","
    return list(csv.DictReader(txt.splitlines(True), delimiter=sep))


def review_round(folder, rep):
    """Reviews one round and returns the summary (dict) to print."""
    name = folder.name
    r = {"folder": str(folder), "name": name, "batches": []}
    m = RE_ROUND.match(name)
    if m:
        r["test"], r["funnel"], r["date"], r["label"] = m.groups()
    else:
        rep.error(name, "test folder name does not follow 'T###-TF - DDMM [Label]'")
        mm = re.match(r"^(T\d+)(?:-(TF|FF))?", name)
        r["test"], r["funnel"] = (mm.group(1), mm.group(2)) if mm else ("?", None)
        r["date"], r["label"] = "?", "?"

    bj = folder / "tracking" / "batches.json"
    tracking = {}
    if bj.exists():
        try:
            d = json.loads(bj.read_text(encoding="utf-8"))
            tracking = {str(b.get("id")): b for b in d.get("batches", [])}
            for k in ("test", "funnel"):
                if d.get(k) and r.get(k) and d[k] != r[k]:
                    rep.error("tracking/batches.json", "%s = %s, but the folder says %s" % (k, d[k], r[k]))
        except Exception as e:
            rep.warn("tracking/batches.json", "could not read it (%s)" % e)
    else:
        rep.warn(name, "no tracking/batches.json")

    upload = read_upload(folder)
    if upload is None:
        rep.warn(name, "no upload.csv")
    csv_rows = {row.get("ad", "").strip(): row for row in (upload or [])}
    seen_ads = set()

    authors, products, formats, nums = set(), set(), set(), []
    for sub in sorted(p for p in folder.iterdir() if p.is_dir()):
        if sub.name in SUPPORT_DIRS:
            continue
        mb = RE_BATCH.match(sub.name)
        if not mb:
            rep.warn(sub.name, "folder does not follow the batch pattern '{AUTHOR} BRAND-SKU T###-TF-BLF{n}' (skipped)")
            continue
        author, product, test, funnel, fmt, n = mb.groups()
        cell = "%s%s" % (fmt, n)
        base = sub.name
        authors.add(author); products.add(product); formats.add(fmt); nums.append(int(n))
        if test != r["test"]:
            rep.error(base, "test %s differs from the round folder (%s)" % (test, r["test"]))
        if r.get("funnel") and funnel != r["funnel"]:
            rep.error(base, "funnel %s differs from the round folder (%s)" % (funnel, r["funnel"]))

        b = {"cell": cell, "base": base, "author": author, "funnel": funnel, "fmt": fmt,
             "n": int(n), "media": [], "docx": None, "prompts": False}

        # files inside the batch folder
        main_docx = sub / (base + ".docx")
        prompts = sub / (base + " - PROMPTS.docx")
        b["prompts"] = prompts.exists()
        if not main_docx.exists():
            rep.error(base, "main docx '%s.docx' is missing" % base)
        if not prompts.exists():
            rep.error(base, "'%s - PROMPTS.docx' is missing" % base)
        re_media = re.compile("^" + re.escape(base) + r"-V(\d+)$")
        for f in sorted(sub.iterdir()):
            if f.is_dir():
                rep.warn(base, "unexpected subfolder '%s'" % f.name)
                continue
            if f in (main_docx, prompts):
                continue
            if f.suffix.lower() in MEDIA_EXT:
                mv = re_media.match(f.stem)
                if mv:
                    b["media"].append((int(mv.group(1)), f))
                    continue
                hint = ""
                if re.search(r"[-.][vV]\d+$", f.stem) and not f.stem.startswith(base):
                    hint = " (prefix differs from the folder)"
                elif re.search(r"\.[vV]\d+$|-v\d+$", f.stem):
                    hint = " (variation must be '-V1', hyphen and capital V)"
                rep.error(base, "media file off pattern: '%s'%s" % (f.name, hint))
            elif f.name.startswith("~$"):
                rep.warn(base, "Word temp file (document still open): '%s'" % f.name)
            else:
                rep.warn(base, "unexpected file: '%s'" % f.name)
        b["media"].sort()
        vs = [v for v, _ in b["media"]]
        if not vs:
            rep.error(base, "no image/video '%s-V1'" % base)
        elif vs != list(range(1, len(vs) + 1)):
            rep.warn(base, "variations out of sequence: %s" % ", ".join("V%d" % v for v in vs))

        # main docx
        if main_docx.exists():
            info = read_docx(main_docx)
            b["docx"] = info
            if info is None:
                rep.warn(base, "python-docx not installed, docx not checked")
            else:
                if info["title"] != base:
                    rep.error(base, "title inside the docx is '%s'" % info["title"])
                if info["cta"] and info["cta"] != CTA_BY_FUNNEL.get(funnel):
                    rep.warn(base, "docx CTA is '%s', funnel %s calls for '%s'"
                             % (info["cta"], funnel, CTA_BY_FUNNEL.get(funnel)))
                for k in ("angle", "profile", "headline", "description", "cta"):
                    if not info[k]:
                        rep.error(base, "docx has no %s field" % k.upper())

        # draft
        fm = read_frontmatter(folder / "drafts" / (cell + ".md"))
        if fm is None:
            rep.warn(base, "no drafts/%s.md" % cell)
        else:
            if fm.get("id") and fm["id"] != base:
                rep.error(base, "drafts/%s.md has id '%s'" % (cell, fm["id"]))
            if fm.get("funnel") and fm["funnel"] != funnel:
                rep.error(base, "drafts/%s.md says funnel %s" % (cell, fm["funnel"]))
            if b["docx"] and fm.get("profile") and fm["profile"] != b["docx"]["profile"]:
                rep.warn(base, "draft profile (%s) differs from docx (%s)" % (fm["profile"], b["docx"]["profile"]))

        # tracking
        t = tracking.get(cell)
        if tracking and not t:
            rep.error(base, "batch %s is not in tracking/batches.json" % cell)
        elif t:
            expected = set(t.get("images", []))
            found = {"%s-V%d" % (cell, v) for v in vs}
            if expected and expected != found:
                rep.warn(base, "tracking lists %s, folder has %s" % (sorted(expected), sorted(found)))

        # upload.csv
        if upload is not None:
            for v, f in b["media"]:
                ad = "%s-V%d" % (base, v)
                seen_ads.add(ad)
                row = csv_rows.get(ad)
                if not row:
                    rep.error(base, "'%s' is not in upload.csv" % ad)
                    continue
                ad_set = "%s-%s-%s" % (test, funnel, cell)
                if row.get("ad_set", "").strip() != ad_set:
                    rep.error(ad, "ad_set in csv is '%s', expected '%s'" % (row.get("ad_set"), ad_set))
                if row.get("image", "").strip() != f.name:
                    rep.error(ad, "image in csv is '%s', file is '%s'" % (row.get("image"), f.name))
                if b["docx"] and row.get("cta") and row["cta"].strip() != b["docx"]["cta"]:
                    rep.warn(ad, "CTA in csv (%s) differs from docx (%s)" % (row["cta"], b["docx"]["cta"]))
                if b["docx"] and row.get("profile") and row["profile"].strip() != b["docx"]["profile"]:
                    rep.warn(ad, "profile in csv (%s) differs from docx (%s)" % (row["profile"], b["docx"]["profile"]))
        r["batches"].append(b)

    for ad in csv_rows:
        if ad and ad not in seen_ads and r["batches"]:
            rep.error("upload.csv", "row '%s' has no matching file in the folders" % ad)

    r["batches"].sort(key=lambda b: b["n"])
    for k, vals in (("author", authors), ("product", products), ("format", formats)):
        if len(vals) > 1:
            rep.warn(name, "more than one %s in the same round: %s" % (k, ", ".join(sorted(vals))))
    if nums:
        gaps = sorted(set(range(1, max(nums) + 1)) - set(nums))
        if gaps:
            rep.warn(name, "numbering has gaps, missing: %s" % ", ".join(str(n) for n in gaps))
        if len(nums) != len(set(nums)):
            rep.error(name, "repeated batch number")
    r["authors"], r["products"], r["formats"] = sorted(authors), sorted(products), sorted(formats)
    return r


def cut(s, n):
    s = s or ""
    return s if len(s) <= n else s[: n - 1] + "…"


def show(r):
    print("=" * 78)
    print("NAMING REVIEW  %s" % r["name"])
    print("=" * 78)
    fmt = ", ".join("%s = %s" % (f, FORMATS[f]) for f in r["formats"]) or "?"
    nvar = sorted({len(b["media"]) for b in r["batches"]})
    print("  Test        : %s" % r["test"])
    print("  Funnel      : %s (%s)" % (r.get("funnel") or "?", FUNNELS.get(r.get("funnel"), "not identified")))
    print("  Format      : %s" % fmt)
    print("  Author      : %s" % (", ".join(r["authors"]) or "?"))
    print("  Product     : %s" % (", ".join(r["products"]) or "?"))
    print("  Date/label  : %s  [%s]" % (r["date"], r["label"]))
    print("  Batches     : %d  (%s)" % (len(r["batches"]), ", ".join(b["cell"] for b in r["batches"])))
    print("  Variations  : %s per batch" % ("/".join(str(n) for n in nvar) or "0"))
    print()
    for b in r["batches"]:
        d = b["docx"] or {}
        vs = " ".join("V%d" % v for v, _ in b["media"]) or "-"
        print("  %-5s %s" % (b["cell"], b["base"]))
        print("        angle   : %s" % cut(d.get("angle"), 66))
        print("        level   : %s   profile: %s" % (d.get("level", ""), d.get("profile", "")))
        print("        headline: %s" % cut(d.get("headline"), 66))
        print("        opens on: %s" % cut(d.get("opening"), 66))
        print("        CTA %-12s  copy %s chars  media %s  PROMPTS %s" % (
            d.get("cta", "?"), "{:,}".format(d.get("chars", 0)), vs,
            "ok" if b["prompts"] else "MISSING"))
    print()


def main():
    ap = argparse.ArgumentParser(description="Naming review for long form / static / video rounds")
    ap.add_argument("folder", nargs="?", default=".", help="test folder, or the creatives folder to review all")
    a = ap.parse_args()

    folder = Path(a.folder).resolve()
    if not folder.is_dir():
        sys.exit("folder not found: %s" % folder)
    has_batch = lambda p: any(RE_BATCH.match(s.name) for s in p.iterdir() if s.is_dir())
    if has_batch(folder) or RE_ROUND.match(folder.name):
        targets = [folder]
    else:
        targets = [p for p in sorted(folder.iterdir())
                   if p.is_dir() and RE_ANY_ROUND.match(p.name) and has_batch(p)]
    if not targets:
        sys.exit("no round folder with batches in %s" % folder)

    rep = Report()
    rounds = [review_round(p, rep) for p in targets]
    for r in rounds:
        show(r)

    print("ISSUES")
    if not rep.items:
        print("  none. Names, docx, tracking and upload.csv all match.")
    for level, where, msg in rep.items:
        print("  [%s] %s: %s" % (level, where, msg))
    print()
    print("Result: %d error(s), %d warning(s)." % (rep.n_errors, len(rep.items) - rep.n_errors))
    sys.exit(1 if rep.n_errors else 0)


if __name__ == "__main__":
    main()
