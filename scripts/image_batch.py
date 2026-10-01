# -*- coding: utf-8 -*-
"""
image_batch.py — Phase 5. Orchestrates the K images per batch.

The Higgsfield MCP is not callable from inside Python, so the split is:
  plan    reads image-brief.md and builds the queue (tracking/image-jobs.json)
  next    prints the next pending job, with the prompt ready for the MCP
  record  downloads the returned rawUrl, names it, validates it and marks it done
  verify  checks the whole batch: count, 1:1, file size, filenames

Usage (from the test folder):
  python image_batch.py plan --brief image-brief.md --test T101 --product BRAND-SKU
  python image_batch.py next
  python image_batch.py record --id B1-V1 --url "https://..."
  python image_batch.py verify

Batch = angle x awareness level, numbered B1..B15 in a 5x3 round
(B1 = angle 1 level A, B2 = angle 1 level B, B4 = angle 2 level A).
The image variation comes after a hyphen, capital V: B1-V1, B1-V2, B1-V3.
The batch id can carry the format: BLF{n} long form, BS{n} static, BV{n} video.
"""
import argparse, json, re, sys, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

JOBS = Path("tracking/image-jobs.json")
UA = {"User-Agent": "Mozilla/5.0"}
# The label of each variation comes from the brief header, never from a fixed map:
# the variation axis changes per round (ethnicity, age band, composition).
DEFAULT_AUTHOR = "AA"

def load():
    if not JOBS.exists():
        print("Run 'plan' first."); sys.exit(2)
    return json.loads(JOBS.read_text(encoding="utf-8"))

def save(d):
    JOBS.parent.mkdir(parents=True, exist_ok=True)
    JOBS.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

# ------------------------------------------------------------------ plan
def cmd_plan(a):
    txt = Path(a.brief).read_text(encoding="utf-8")
    jobs = []
    # blocks '#### B1-V1 - label' followed by '**Prompt:**' and the prompt up to the next ####/###.
    # Batch = angle x level (B1..B15, or BLF/BS/BV); the -V1/-V2/-V3 suffix is the image variation.
    for m in re.finditer(r"^####\s*(B(?:LF|S|V)?\d{1,2}-[vV]\d)\b([^\n]*)\n(.*?)(?=^#{3,4}\s|\Z)",
                         txt, re.M | re.S):
        cid, label, block = m.group(1), m.group(2), m.group(3)
        label = label.strip().lstrip("-" + chr(8212) + chr(8211) + " ").strip() or "?"
        pm = re.search(r"\*\*Prompt:?\*\*\s*\n(.*)", block, re.S)
        prompt = (pm.group(1) if pm else block).strip()
        prompt = re.sub(r"\n{3,}", "\n\n", prompt)
        cid = cid[:-2] + cid[-2:].upper()   # legacy B1-v1 becomes B1-V1
        cell, var = cid.rsplit("-", 1)   # B1, V1
        jobs.append({
            "id": cid, "cell": cell, "variation": var,
            "cluster": label,
            # each batch has its own folder: 'AA BRAND-SKU T101-B1/AA BRAND-SKU T101-B1-V1.png'
            "file": "%s %s %s-%s/%s %s %s-%s.png" % (a.author, a.product, a.test, cell,
                                                    a.author, a.product, a.test, cid),
            "prompt": prompt, "status": "pending", "url": None, "bytes": 0, "dim": None,
        })
    # guard: a prompt that swallowed the header of the next batch
    suspects = [j for j in jobs
                if re.search(r"^#{2,4}\s", j["prompt"], re.M)
                or re.search(r"\*\*(Locked scene|Hook concept)", j["prompt"])
                or len(j["prompt"]) > 4000]
    if suspects:
        print("FORMAT ERROR: %d prompt(s) contain a header or marker of another batch." % len(suspects))
        print("Typical cause: a batch header written with '##' instead of '###'.")
        for j in suspects[:5]:
            print("   %s  (%d chars)" % (j["id"], len(j["prompt"])))
        sys.exit(2)
    if not jobs:
        print("No '#### B#-V#' block found in %s." % a.brief)
        print("Expected format: '#### B1-V1 - woman 45-52 · white' followed by '**Prompt:**'.")
        sys.exit(2)
    save({"test": a.test, "product": a.product,
          "model": "nano_banana_pro", "aspect_ratio": "1:1", "resolution": "2k",
          "jobs": jobs})
    cells = sorted({j["cell"] for j in jobs}, key=lambda c: int(re.sub(r"\D", "", c)))
    print("queue built: %d images across %d batches -> %s" % (len(jobs), len(cells), JOBS))
    print("batches: %s" % ", ".join(cells))
    short = [c for c in cells if sum(1 for j in jobs if j["cell"] == c) != 3]
    if short:
        print("WARNING, batches without 3 variations: %s" % ", ".join(short))

# ------------------------------------------------------------------ next
def cmd_next(a):
    d = load()
    pend = [j for j in d["jobs"] if j["status"] == "pending"]
    if not pend:
        print("Nothing pending. Run 'verify'."); return
    n = a.n
    print("Fixed parameters: model=%s  aspect_ratio=%s  resolution=%s\n"
          % (d["model"], d["aspect_ratio"], d["resolution"]))
    for j in pend[:n]:
        print("=" * 76)
        print("ID   : %s   (%s)" % (j["id"], j.get("cluster", j.get("ethnicity", "?"))))
        print("File : %s" % j["file"])
        print("-" * 76)
        print(j["prompt"])
        print()
    print("=" * 76)
    print("%d still pending." % len(pend))

# ------------------------------------------------------------------ record
def cmd_record(a):
    d = load()
    j = next((x for x in d["jobs"] if x["id"].upper() == a.id.upper()), None)
    if not j:
        print("id %s is not in the queue" % a.id); sys.exit(2)
    dest = Path(j["file"])
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(a.url, headers=UA)
        data = urllib.request.urlopen(req, timeout=300).read()
    except Exception as e:
        print("DOWNLOAD FAILED for %s: %s" % (a.id, e)); sys.exit(1)
    if len(data) < 20000:
        print("FAILED: suspicious file (%d bytes)" % len(data)); sys.exit(1)
    dest.write_bytes(data)
    dim = None
    try:
        from PIL import Image
        with Image.open(dest) as im:
            dim = list(im.size)
    except Exception:
        pass
    j.update(status="done", url=a.url, bytes=len(data), dim=dim)
    save(d)
    warning = ""
    if dim and dim[0] != dim[1]:
        warning = "   WARNING: not 1:1 (%dx%d), regenerate" % (dim[0], dim[1])
    print("ok %s -> %s  (%.1f MB%s)%s"
          % (a.id, dest.name, len(data) / 1e6,
             ", %dx%d" % tuple(dim) if dim else "", warning))

# ------------------------------------------------------------------ verify
def cmd_verify(a):
    d = load()
    jobs = d["jobs"]
    pending = [j for j in jobs if j["status"] != "done"]
    missing = [j for j in jobs if j["status"] == "done" and not Path(j["file"]).exists()]
    not_square = [j for j in jobs if j.get("dim") and j["dim"][0] != j["dim"][1]]
    small = [j for j in jobs if j["status"] == "done" and j["bytes"] < 200000]

    # frame/letterbox: passes the 1:1 check and still fails at delivery.
    # Detects a uniform dark border around a lighter center.
    framed = []
    try:
        from PIL import Image
        import numpy as np
        for j in jobs:
            if j["status"] != "done" or not Path(j["file"]).exists():
                continue
            arr = np.asarray(Image.open(j["file"]).convert("RGB").resize((256, 256)))
            k = 8
            border = np.concatenate([arr[:k].reshape(-1, 3), arr[-k:].reshape(-1, 3),
                                     arr[:, :k].reshape(-1, 3), arr[:, -k:].reshape(-1, 3)])
            center = arr[64:192, 64:192].reshape(-1, 3)
            if border.mean() < 12 and center.mean() > 40:
                framed.append(j["id"])
    except ImportError:
        framed = None

    print("=" * 76)
    print("VERIFY  %s  |  %d images planned" % (d.get("test"), len(jobs)))
    print("=" * 76)
    print("generated        : %d" % sum(1 for j in jobs if j["status"] == "done"))
    print("pending          : %d %s" % (len(pending), [j["id"] for j in pending][:10] if pending else ""))
    print("file missing     : %d %s" % (len(missing), [j["id"] for j in missing] if missing else ""))
    print("not 1:1          : %d %s" % (len(not_square), [j["id"] for j in not_square] if not_square else ""))
    print("suspicious (<200KB): %d %s" % (len(small), [j["id"] for j in small] if small else ""))
    if framed is None:
        print("framed           : not checked (install pillow and numpy)")
    else:
        print("framed           : %d %s" % (len(framed), framed if framed else ""))

    # complete cells
    cells = {}
    for j in jobs:
        cells.setdefault(j["cell"], []).append(j["status"] == "done")
    incomplete = [c for c, v in cells.items() if not all(v)]
    print("complete batches : %d/%d %s"
          % (len(cells) - len(incomplete), len(cells), incomplete if incomplete else ""))
    ok = not (pending or missing or not_square or small or framed)
    print("\n%s" % ("BATCH OK" if ok else "BATCH INCOMPLETE, see above"))
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan");  p.add_argument("--brief", default="image-brief.md")
    p.add_argument("--test", default="T101"); p.add_argument("--product", default="BRAND-SKU")
    p.add_argument("--author", default=DEFAULT_AUTHOR)
    p.set_defaults(f=cmd_plan)
    p = sub.add_parser("next");  p.add_argument("-n", type=int, default=3); p.set_defaults(f=cmd_next)
    p = sub.add_parser("record"); p.add_argument("--id", required=True)
    p.add_argument("--url", required=True); p.set_defaults(f=cmd_record)
    p = sub.add_parser("verify"); p.set_defaults(f=cmd_verify)
    a = ap.parse_args(); a.f(a)

if __name__ == "__main__":
    main()
