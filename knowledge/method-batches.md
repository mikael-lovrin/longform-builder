# The batch method — invariant across rounds

> This is the **how**, and it holds for any round. The angles, levels and avatars of a specific round live in `rounds/T###.md` and change every test.
>
> Source model: the long form static pipeline of a competitor in the same vertical, adapted through the round structure document supplied by the user.

## What a batch is

**1 batch = 1 angle + 1 awareness level + 1 long-form copy + K image variations.**

**Batch = angle x level.** Each combination is its own batch, numbered sequentially: a round of 5 angles x 3 levels has **15 batches, B1 to B15**. An angle on its own is not a batch: angles are called **Angle 1 to Angle 5**.

Formula: `batch = (angle - 1) x 3 + level index + 1`, with A=0, B=1, C=2.

| | A — Problem aware | B — Solution aware | C — Hidden cause |
|---|---|---|---|
| Angle 1 | B1 | B2 | B3 |
| Angle 2 | B4 | B5 | B6 |
| Angle 3 | B7 | B8 | B9 |
| Angle 4 | B10 | B11 | B12 |
| Angle 5 | B13 | B14 | B15 |

Image variations come after a hyphen: `B1-V1`, `B1-V2`, `B1-V3`. The hyphen is not optional, because without it `B11` would be ambiguous. Full names: folder `AA BRAND-SKU T101-TF-B1/`, docx `AA BRAND-SKU T101-TF-B1.docx`, images `AA BRAND-SKU T101-TF-B1-V1.png`. The level (A/B/C) and the angle number live in the draft frontmatter (`level:`, `angle_num:`), not in the name.

- The copy is the **same** across the K variations. Only the image changes.
- In long form static, **the hook is the image**. Its job is to stop the scroll and earn the tap on see more. The copy carries the angle.
- The K images are K avatar clusters, to find out who responds.

## The matrix

`N angles x M awareness levels = N*M cells`. Each cell is a batch, numbered B1 to B(N*M) angle by angle, levels A, B, C inside each angle.

When there is more than one copywriter, **they all write the entire matrix**. You do not split cells between copywriters: writing the full matrix is what gives you multiple executions per cell and lets you separate "good angle" from "good copywriter".

## The awareness levels (stable across rounds)

The horizontal axis tends to repeat, because the question it answers is structural.

**Default labels (fixed):** A = Problem aware, B = Solution aware, C = Hidden cause. These are the names that appear in the documents and in conversation.

**A — Problem aware.** Enters through the scene. Opens on a dated, concrete scene of a lived consequence, never on the clinical symptom and never on the problem in the abstract. The specificity is implicit proof before any argument. The pain is named by its social consequence, the cause stays open, and the mechanism arrives later, as absolution.

**B — Solution aware.** Opens on why everything he already tried failed.

**C — Hidden cause.** The mechanism comes first. Opens straight on the reveal. **A and C are the same classified level**; the difference is the **position of the mechanism**: in A it arrives late, as relief; in C it opens the copy, as news. The real question this axis answers is: **does the mechanism sell better early or late?**

In column C the order of the movements in `longform-anatomy.md` **inverts**: mechanism first, pain as confirmation. It is not the same text with a paragraph moved.

## Length — measured, not estimated

Floor 2,500 characters, but **2,500 is a floor and it sits well below the market.**

Real distribution of 68 active long forms from a competitor in the same vertical (public Ad Library sweep, collected 2026-09-23):

| Band | Creatives |
|---|---|
| under 2.5k | 3% |
| 2.5k to 5k | 15% |
| 5k to 8k | 10% |
| 8k to 12k | **40%** |
| over 12k | **32%** |

**Median: 10,809 characters. P75: 13,285. Max: 15,833.**

And the number that matters most: **the highest-volume profile in the sweep (21 creatives, 49 active ads) has a median of 14,984 characters.** Whoever scales the most is whoever writes the longest.

| Nature of the angle | Target band |
|---|---|
| Domestic story (wife, couple) | 8,000 to 12,000 |
| First-person male confession | 9,000 to 14,000 |
| Authority with a credential | 11,000 to 15,000 |
| Mechanism / consolidating villain | 8,000 to 12,000 |
| Light relationship / couple | 3,500 to 6,000 |

The only short family observed is the couple one (a dedicated couple-story page, median 3,922). Outside of it, short copy is a minority across the whole library.

> If the round document sets smaller bands, **raise it with the user before writing.** Writing 15 copies at 4k when the market runs 11k is the difference between testing the angle and accidentally testing length.

## Variable isolation

To read angle x level with a clean signal, **lock everything else in the round**: one destination, one product, one offer. Every extra variable multiplies the ads and makes it harder to say what caused what.

The next round takes the winners and only then tests destination, product format and offer.

## Budget and reading

- **$100 per batch** (per ad set), distributed automatically across the K images
- **Reading floor: $850.85 per cell** for a directional read, **10 conversions** for a conclusive read. Before that, no conclusions
- Cut order if cash tightens: first the column with prior negative evidence (a whole level, e.g. column B = B2, B5, B8, B11, B14), then the lowest-CTR batches inside each angle. **Never cut an execution** (copywriter)
- The winner scales in the **same ad set**, from $100 to about $300

## How to read the result

The matrix lets you read four things: by angle (the rows, e.g. Angle 1 = B1+B2+B3), by level (the columns, e.g. level A = B1+B4+B7+B10+B13), by batch (the winning combination) and by avatar (the K images of each batch).

**Two mandatory corrections, both learned from mistakes already made on this account:**

1. **High CTR on the image is not a winner signal.** Hook rate is not monotonic, retention is. Do not promote a batch on CTR. The signal is sales.
2. **Do not repeat the label, repeat the asset.** Reading performance as a property of the angle and ordering the label rewritten cost 4 months: 204 sales across 2 tests turned into 18 sales across 8 tests. When a batch wins, what scales is **that copy with that image**.

## What always ships, in any round

- The complete **enemy block**, in every batch, as enemies and never as the main villain
- The **production locks** in `production-locks.md`, no exceptions
- The **five placement fields** in `meta-placement.md`
- **Congruence between the copy POV and the page that runs it** (`publishing-profiles.md`)

## Where each round's angles come from

**From the user, before Phase 1.** Angles are specific to the product and the moment, and the next round replaces whichever ones lost.

The competitor examples in `support/` exist to **calibrate format, length and rhythm** — never to pick the angle. The angle is a business decision, not a swipe decision.

If the user does not specify the angles, ask. Do not inherit the previous round's angles out of inertia.
