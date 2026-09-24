# Phase 1 — Matrix

Goal: write the grid of the round before any copy exists, so every cell is born with an identity, a lock and a reading criterion already defined.

## Step 1 — Build `matrix.md`

One section per cell. Each cell (angle x level) is a batch, numbered sequentially: `batch = (angle - 1) x 3 + level index + 1`, with A=0, B=1, C=2. A 5 x 3 round has 15 batches:

| | A — Problem aware | B — Solution aware | C — Hidden cause |
|---|---|---|---|
| Angle 1 | B1 | B2 | B3 |
| Angle 2 | B4 | B5 | B6 |
| Angle 3 | B7 | B8 | B9 |
| Angle 4 | B10 | B11 | B12 |
| Angle 5 | B13 | B14 | B15 |

Each cell gets:

```markdown
### B{batch} — Angle {n} {Angle Name} x {Level Name} ({level})

- **Delivery ID:** {AUTHOR} {BRAND-SKU} T###-B{batch}
- **Images:** {AUTHOR} {BRAND-SKU} T###-B{batch}-v1 / -2 / -3
- **Reference hook:** (from the structure document, an anchor and not final text)
- **Target:** who the reader of this cell is, in one sentence
- **Mechanism position:** late (A) / after the solution failure (B) / in the opening (C)
- **Angle lock:** what is forbidden in this cell
- **Character band:** (see `method-batches.md` and the round file)
- **3 proof modalities chosen:** (LOCK 1, chosen now, not while writing)
- **Xquad voices:** base, support, psychology
- **Avatars:** 1 white / 2 Black / 3 Latino, with the angle's locked age band
```

## Step 2 — Actually differentiate the columns

The easy mistake is writing three variations of the same text and calling them awareness levels. **The difference between A, B and C is structural, not cosmetic.**

| Level | Where the copy opens | Where the mechanism enters | What the opening has not delivered yet |
|---|---|---|---|
| **A** | A dated scene of a lived consequence | Movement 8, after the failure of authority | The cause |
| **B** | The graveyard of attempts, what already failed | Movement 8, but explaining why that failed | The cause and the alternative |
| **C** | The mechanism reveal, as news | Movement 1, it is the opening | The scene and the pain, which come later |

In column C the order of the movements in `longform-anatomy.md` **inverts**: mechanism first, pain as confirmation. It is not the same text with a paragraph moved.

**Matrix quality test:** read the first three lines of the three cells of the same angle. If they could be swapped between cells without anyone noticing, the columns are not differentiated and Phase 2 does not start.

## Step 3 — Distribute the proof modalities

LOCK 1 requires three per copy. Distribute them so the matrix does not run the same trio in every cell, or the round learns nothing about proof.

Suggested distribution by angle:

| Angle | Natural trio |
|---|---|
| Angle 1 Partner running a protocol | personal experience, third-party validation, demonstration |
| Angle 2 Dead bedroom, present tense | personal experience, mechanism logic, third-party validation |
| Angle 3 Male confession | personal experience, mechanism logic, verifiable number |
| Angle 4 Authority | mechanism logic, verifiable number, demonstration |
| Angle 5 Single villain | mechanism logic, verifiable number, third-party validation |

## Step 4 — `tracking/batches.json`

```json
{
  "test": "T101",
  "product": "BRAND-SKU",
  "destination": "quiz",
  "created_at": "2026-09-24",
  "directional_floor_usd": 850.85,
  "conclusive_floor_conversions": 10,
  "batches": [
    {
      "id": "B1",
      "angle_num": 1,
      "angle": "Partner running a protocol",
      "level": "A",
      "mechanism_position": "late",
      "proof": ["personal_experience", "third_party_validation", "demonstration"],
      "voices": ["andre-chaperon", "blair-warren"],
      "target_chars": [8000, 12000],
      "images": ["B1-v1", "B1-v2", "B1-v3"],
      "status": "planned"
    }
  ]
}
```

One record per batch, `B1` to `B15`. `target_chars` is **per batch id**: it is what `check_locks.py` reads for each draft `drafts/B{n}.md` (without the json it falls back to 8,000 to 12,000). The three batches of the same angle normally repeat the same band.

`status` moves through: `planned` -> `written` -> `gate_passed` -> `images_ok` -> `delivered` -> `live` -> `winner` or `dead`.

## Step 5 — Present and lock

Show the matrix to the user as a compact table and ask for confirmation. **The matrix does not change once Phase 2 starts** — changing an angle mid-round destroys the read of the round, which is the only thing the round actually produces.
