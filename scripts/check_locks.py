# -*- coding: utf-8 -*-
"""
check_locks.py — the automatic gate of Phase 3.

Checks, over the copy drafts, whatever is verifiable from the text.
See ../knowledge/production-locks.md for where each lock comes from.

Usage (from the test folder):
    python "$HOME/.claude/skills/longform-builder/scripts/check_locks.py" drafts/
    python ... drafts/ --product "YourBrand" --json gate.json

Output: a report on stdout + exit code 1 if anything is BLOCKED.
"""
import argparse, json, re, sys, unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Fallback bands. The source of truth is tracking/batches.json (field target_chars, keyed
# by batch id B1..B15), which comes from the round file. These only apply without that json.
# Batch = angle x awareness level, numbered B1..B15 in a 5x3 round.
DEFAULT_LENGTH_RANGES = {}           # without batches.json, GENERIC_RANGE applies to every batch
GENERIC_RANGE = (8000, 12000)

def load_ranges(folder):
    """Reads target_chars from tracking/batches.json, walking up to 2 levels from the folder."""
    base = Path(folder).resolve()
    for cand in (base, base.parent, base.parent.parent):
        j = cand / "tracking" / "batches.json"
        if j.exists():
            try:
                d = json.loads(j.read_text(encoding="utf-8"))
                out = {}
                for b in d.get("batches", []):
                    target = b.get("target_chars") or b.get("chars_target")
                    bid = str(b.get("id", ""))
                    if target and len(target) == 2 and bid:
                        out[bid] = (int(target[0]), int(target[1]))
                if out:
                    return out, str(j)
            except Exception:
                pass
    return dict(DEFAULT_LENGTH_RANGES), "built-in fallback"

TRICK = re.compile(r"\b(trick|secret|hack|loophole)\b", re.I)
ENEMIES = {
    "blue_pill": r"(blue pill|viagra|sildenafil|cialis)",
    "trt": r"\b(trt|testosterone replacement|needle|inject)",
    "underdosed": r"(underdos|30\s?mg|amazon|booster|gnc|tribulus|proprietary blend)",
    "doctor_says_normal": r"(normal for (your|his) age|within range|normal range|perfectly normal|everything (is|was) normal)",
}

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

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

def section(body, title):
    m = re.search(r"^##\s*%s\s*$" % re.escape(title), body, re.M | re.I)
    if not m:
        return ""
    rest = body[m.end():]
    n = re.search(r"^##\s+", rest, re.M)
    return (rest[:n.start()] if n else rest).strip()

def check(path, product, ranges=None):
    txt = path.read_text(encoding="utf-8")
    fm, body = parse_front(txt)
    primary = section(body, "PRIMARY TEXT") or body
    first3 = section(body, "FIRST 3 LINES (what shows before see more)") \
             or section(body, "FIRST 3 LINES")
    head = section(body, "LINK HEADLINE")
    desc = section(body, "LINK DESCRIPTION")
    cta = section(body, "CTA")

    bid = fm.get("id") or path.stem
    # batch = angle x level (B1..B15); the length band is per batch id in batches.json
    batch = re.search(r"B(\d+)", path.stem)
    batch = "B%s" % batch.group(1) if batch else None
    n = len(primary)
    flat = strip_accents(primary.lower())

    blocks, pend, ok = [], [], []

    # LOCK 11 — em dashes and quotation marks (BLOCKING)
    dashes = primary.count("—") + primary.count("–")
    quotes = len(re.findall(r'["“”]', primary))
    if dashes or quotes:
        blocks.append("LOCK 11 em_dashes=%d quotes=%d in the primary text" % (dashes, quotes))
    else:
        ok.append("LOCK 11")

    # LOCK 3 — trick vocabulary + product position (vocabulary is BLOCKING)
    hits = TRICK.findall(primary)
    if hits:
        blocks.append("LOCK 3 trick vocabulary: %s" % ", ".join(sorted(set(h.lower() for h in hits))))
    prod_pos = None
    if product:
        mp = re.search(re.escape(product), primary, re.I)
        if mp:
            prod_pos = mp.start() / max(n, 1)
    if prod_pos is None:
        blocks.append("LOCK 2 product '%s' does not appear in the primary text" % product)
    else:
        ok.append("LOCK 2")
        if prod_pos < 0.5:
            pend.append("LOCK 3 product appears at %.0f%% of the text (expected late, >50%%)" % (prod_pos * 100))
        else:
            ok.append("LOCK 3")

    # LOCK 1 — 3 proof modalities
    proof = fm.get("proof") or []
    if isinstance(proof, str):
        proof = [proof]
    if len(proof) != 3:
        pend.append("LOCK 1 declared %d proof modalities (expected 3)" % len(proof))
    else:
        ok.append("LOCK 1")

    # LOCK 6 — dollar price
    if re.search(r"\$\s?\d|\b\d+\s?dollars\b", primary, re.I):
        ok.append("LOCK 6")
    else:
        pend.append("LOCK 6 no dollar price in the text")

    # LOCK 10 — lab value between 350 and 412
    nums = [int(x) for x in re.findall(r"\b(3[5-9]\d|4[0-1]\d)\b", primary)]
    if any(350 <= x <= 412 for x in nums):
        ok.append("LOCK 10")
    else:
        pend.append("LOCK 10 no lab number between 350 and 412")

    # LOCK 12 — first 3 lines
    if first3:
        L = len(first3)
        if 200 <= L <= 400:
            ok.append("LOCK 12")
        else:
            pend.append("LOCK 12 first 3 lines at %d chars (expected 200 to 400)" % L)
    else:
        pend.append("LOCK 12 FIRST 3 LINES section missing")

    # length
    band = (ranges or DEFAULT_LENGTH_RANGES).get(batch, GENERIC_RANGE)
    if band:
        if band[0] <= n <= band[1]:
            ok.append("length")
        else:
            pend.append("length %d chars, band for %s is %d to %d" % (n, batch, band[0], band[1]))
    if n < 2500:
        blocks.append("absolute floor: %d chars (<2500)" % n)

    # enemy block
    missing = [k for k, pat in ENEMIES.items() if not re.search(pat, flat, re.I)]
    if missing:
        pend.append("enemy block incomplete, missing: %s" % ", ".join(missing))
    else:
        ok.append("enemies")

    # placement fields
    for name, val, lo, hi in (("headline", head, 40, 70), ("description", desc, 60, 110)):
        if not val:
            pend.append("field %s missing" % name)
        elif not (lo <= len(val) <= hi):
            pend.append("%s at %d chars (expected %d to %d)" % (name, len(val), lo, hi))
        else:
            ok.append(name)
    if not cta:
        pend.append("field CTA missing")

    return {"file": path.name, "id": bid, "batch": batch, "chars": n,
            "blocks": blocks, "open_items": pend, "ok": ok}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--product", default="BRAND")
    ap.add_argument("--json")
    a = ap.parse_args()

    def batch_order(p):
        m = re.match(r"B(\d+)$", p.stem)
        return (0, int(m.group(1))) if m else (1, p.stem)
    files = sorted(Path(a.folder).glob("*.md"), key=batch_order)
    if not files:
        print("No .md found in %s" % a.folder); sys.exit(2)

    ranges, origin = load_ranges(a.folder)
    res = [check(p, a.product, ranges) for p in files]
    nb = sum(1 for r in res if r["blocks"])
    npd = sum(len(r["open_items"]) for r in res)

    print("=" * 78)
    print("length bands: %s" % origin)
    print("LOCK GATE  |  %d batches  |  %d blocked  |  %d open items"
          % (len(res), nb, npd))
    print("=" * 78)
    for r in res:
        status = "BLOCKED" if r["blocks"] else ("open item" if r["open_items"] else "OK")
        print("\n[%s] %s  (%d chars)  %s" % (status, r["id"], r["chars"], r["file"]))
        for b in r["blocks"]:
            print("   BLOCK     %s" % b)
        for p in r["open_items"]:
            print("   open item %s" % p)
    print("\n" + "=" * 78)
    if nb:
        print("NO blocked batch may go to Phase 4.")
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print("json: %s" % a.json)
    sys.exit(1 if nb else 0)

if __name__ == "__main__":
    main()
