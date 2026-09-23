# Phase 1 — Matrix

Goal: write the grid of the round before any copy exists, so every cell is born with an identity, a lock and a reading criterion already defined.

## Step 1 — Build `matrix.md`

One section per cell. Each cell gets:

```markdown
### B{n}-{level} — {Angle Name} x {Level Name}

- **Delivery ID:** {AUTHOR} {BRAND-SKU} T###-B{n}-{level}
- **Images:** {AUTHOR} {BRAND-SKU} T###-B{n}-{level}1 / 2 / 3
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

| Batch | Natural trio |
|---|---|
| B1 Partner running a protocol | personal experience, third-party validation, demonstration |
| B2 Dead bedroom, present tense | personal experience, mechanism logic, third-party validation |
| B3 Male confession | personal experience, mechanism logic, verifiable number |
| B4 Authority | mechanism logic, verifiable number, demonstration |
| B5 Single villain | mechanism logic, verifiable number, third-party validation |

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
      "id": "B1-A",
      "angle": "Partner running a protocol",
      "level": "A",
      "mechanism_position": "late",
      "proof": ["personal_experience", "third_party_validation", "demonstration"],
      "voices": ["andre-chaperon", "blair-warren"],
      "target_chars": [8000, 12000],
      "images": ["B1-A1", "B1-A2", "B1-A3"],
      "status": "planned"
    }
  ]
}
```

`status` moves through: `planned` -> `written` -> `gate_passed` -> `images_ok` -> `delivered` -> `live` -> `winner` or `dead`.

## Step 5 — Present and lock

Show the matrix to the user as a compact table and ask for confirmation. **The matrix does not change once Phase 2 starts** — changing an angle mid-round destroys the read of the round, which is the only thing the round actually produces.
