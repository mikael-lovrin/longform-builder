# Round T### — <product>, long form static

> Copy this file to `rounds/T###.md` and fill every bracket. This file defines ONE round. The method lives in `../method-batches.md` and does not change here.
>
> Angles and avatars are **user input per round** and apply only to this round.
>
> Source: the round structure document supplied by the user, closed on DD/MM/YYYY.

| | |
|---|---|
| Test | T###, DD/MM/YYYY |
| Product | <product name> (`BRAND-SKU`) |
| Matrix | N angles x M levels x K images = **N*M batches (B1 to B{N*M}), N*M copies, N*M*K images** |
| Destination | <quiz / PDP / advertorial> — one only |
| Image variation axis | <ethnicity by default; see `../casting-longform.md`> |
| Folder | `creatives/T### - DDMM [Long Form Ads]/` |

## Locked mechanism

> One mechanism for the whole round. Every angle enters through a different door and reveals the same chain. Name the chain and name its links, in plumbing language, not biochemistry.

**<Mechanism name>.**

1. **<Link 1 name>** — what it does, in one line
2. **<Link 2 name>** — what it does, in one line
3. **<Link 3 name>** — what it does, in one line

Declared differentiator: **<the connection no competitor makes>.** It appears in every copy.

<!-- Illustrative example of a filled mechanism, from a past round in the ED vertical:
     "Three-System Shutdown": chronic cortisol burns the raw material that would become
     testosterone; abdominal fat converts what is left into estrogen; the same cortisol
     destroys the nitric oxide that actually opens the vessel. Declared differentiator:
     no competitor connects cortisol to erection. -->

## The N angles

> One block per angle, Angle 1 to Angle N. The angle is a business decision and comes from the user.
> The **lock** line is the most important one: it is what the gate checks and what keeps two
> angles from collapsing into each other.

Batch = angle x level (see `../method-batches.md`). Numbering for this round:

| Angle | A — Problem aware | B — Solution aware | C — Hidden cause |
|---|---|---|---|
| Angle 1 — <name> | B1 | B2 | B3 |
| Angle 2 — <name> | B4 | B5 | B6 |
| Angle 3 — <name> | B7 | B8 | B9 |
| Angle 4 — <name> | B10 | B11 | B12 |
| Angle 5 — <name> | B13 | B14 | B15 |

Drafts `drafts/B1.md` to `drafts/B15.md`, folders `AA BRAND-SKU T###-B1/` to `-B15/`, images `AA BRAND-SKU T###-B{n}-v1.png` to `-3.png`.

### Angle {n} — <angle name> (<who it is aimed at>)
- **Reference hook:** <one line, an anchor and not final text>
- **Target:** <who this reader is, and the frame the copy uses, in two or three lines>
- **Why:** <the evidence that justifies the angle: account data, a market gap, a documented recommendation>
- **Lock:** <what is forbidden in this angle, and the emotion it must carry>
- **Names to use:** <only if the angle needs a proper name; see the placeholder policy below>

<!-- Illustrative angle families that have worked in this vertical, one line each, as
     calibration only. Do not copy them into a round without the user choosing them:
     - Partner running a protocol: female buyer, intimate timestamp, 30-day diary,
       silent-protocol CTA. Lock: HER wound opens the piece, not his failure.
     - Dead bedroom, present tense: same buyer, no recovery arc. Lock: the
       "he changed one thing and now I cannot keep up" arc is negative evidence, forbidden.
     - Male confession: witnessed humiliation, slow descent, the decision.
       Lock: the emotion is shame, not anger.
     - Authority: the professional speaks in the first person with his own credential,
       and delivers the closing window. Lock: a doctor quoted in the third person does not count.
     - Single villain: eight symptoms consolidated into one root.
       Lock: the villain is biology; doctor, industry and pill are enemies, never the culprit. -->

## Enemy block (mandatory in all angles)

> Four named enemies, present in every batch, as enemies and never as the main villain (LOCK 5).

- **<enemy 1>** — why it fails, in one line
- **<enemy 2>** — why it fails, in one line
- **<enemy 3>** — why it fails, in one line
- **<enemy 4>** — why it fails, in one line

<!-- Illustrative set from this vertical: the blue pill (rents hours, never refills the tank);
     TRT (a needle for life, shuts down your own production); the underdosed marketplace
     supplement (30mg when the study used 600mg); the doctor who says normal with the lab
     value between 350 and 412. -->

## The M levels

A, B and C per `../method-batches.md`. Round-specific notes go here.

> Write down any column that enters with prior evidence, positive or negative, and say so out
> loud. A column entering with known negative evidence is the first one to be cut if cash
> tightens, and nobody should be surprised when it dies.

<!-- Illustrative note from a past round: column B entered at 0.278 ROAS on the account,
     conclusive negative evidence, and was only justified because the prior evidence came
     from video and a different funnel. -->

## Avatars — variation axis

| Variation | Avatar |
|---|---|
| `1` | <White American, by default> |
| `2` | <Black, by default> |
| `3` | <Latino, by default> |

When the angle calls for a female voice, the same distribution applies to women.

Age band locked per angle, never 25-34. See `../casting-longform.md`.

## Length per angle

> Fill from `../method-batches.md`. If the round structure document sets shorter bands than the
> measured market, put both columns side by side and settle it with the user **before Phase 2**.

| Angle | Target band | Band in the original document |
|---|---|---|
| Angle 1 <name> (B1 to B3) | | |
| Angle 2 <name> (B4 to B6) | | |
| Angle 3 <name> (B7 to B9) | | |
| Angle 4 <name> (B10 to B12) | | |
| Angle 5 <name> (B13 to B15) | | |

The band goes into `tracking/batches.json` as `target_chars` on each of the angle's three batches.

**Decision to confirm with the user before Phase 2.** Raising the band raises the production cost of the whole matrix. Keeping a band below the market makes the round test the angle with pieces at half the length the market runs, which introduces length as an undeclared variable.

## Name placeholders

> Policy: when a proper name is not confirmed, pick one and write it **as if it were final**.
> No brackets, no footnote, no reminder to check. The copy ships ready to publish, and swapping
> a name, if it happens, is a manual string replacement.

The same applies to any invented proper name in the copy (the friend, the trainer, the neighbor): pick it, write it, do not mark it.

Special case, authority angle: the physician is contracted and real, and the copy is written to be published by him. See the compliance line in `../publishing-profiles.md`.

## Reserve (next round)

> Angles and hooks that were considered and did not make this matrix. Park them here so the
> next round does not have to rediscover them, and so nothing already burned comes back.
