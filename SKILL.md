---
name: longform-builder
description: "Runs the full production of a long form static ad round for Meta: the batch matrix (angle x awareness level), the 2,500+ character long-form copies, the Meta placement fields (primary text, link headline, link description, CTA), the image prompts and image generation, the formatted .docx delivery per batch and the upload sheet. Use when the user asks to build a batch round or test, create long form statics, produce a T### long form round, or write long-form copy for a cold top-of-funnel static image. For short video/UGC creative use ads-builder; for a page advertorial use adv-builder."
---

# Long Form Builder

You produce **long form static test rounds** for Meta: a static image as the hook, long-form copy in the primary text, cold top of funnel.

The format exists to answer one cheap question: **which angle and which awareness level convert.** It is not a scaling format. Whatever wins here becomes video and advertorial later.

Your foundation lives in `knowledge/`, and it is not opinion. The production locks came out of a 199-ad classification of one DTC account in the men's health / ED supplement vertical (May to September 2026), and each one survived both the cut that excludes May and the cut restricted to a single product. When a lock conflicts with the writer's taste, the lock wins.

---

## Rule 1 — keep the method separate from the round

Two different things, in two different places:

- **`knowledge/method-batches.md`** — the **how**. What a batch is, the awareness levels, length, budget, reading floors, how to read the result. Stable across rounds.
- **`knowledge/rounds/T###.md`** — the **what of this round**. Angles, avatars, mechanism, destination, placeholders. **Changes every test.** Start from `knowledge/rounds/_TEMPLATE.md`.

Every round has a **matrix**: N angles x M awareness levels, with K image variations per cell. Each cell (angle x level) is a batch, and batches are numbered sequentially: 5 x 3 = 15 batches, B1 to B15. It is defined before a single word is written and it does not change mid-round.

**Angles are user input, round by round.** Do not inherit the previous round's angles out of inertia and do not pull them from a competitor swipe: the angle is a business decision. If the user did not specify, ask. A competitor example is there to calibrate **format, length and rhythm**, never to pick the angle.

Read both files at the moment you build the matrix. Do not reproduce them from memory.

**What never changes between rounds:**
- 1 batch = 1 angle + 1 level + **1 long-form copy** + **K images**. The copy is the SAME across the K variations. **Only the image changes.**
- In long form static the **hook is the image**. Its job is to stop the scroll and earn the tap on "see more". The copy carries the angle.
- Whoever writes the matrix writes EVERY cell. You do not split cells between copywriters, or you cannot separate "good angle" from "good copywriter".

---

## Rule 2 — do not repeat the label, repeat the asset

The most expensive mistake already made on this account: reading an asset's performance as a property of the **angle**, then ordering the label rewritten from scratch. 204 sales across 2 tests turned into 18 sales across 8 tests.

When a batch wins, what scales is **that copy with that image**. Never hand off "the winning angle" to be rewritten. When you log a winner, log the file, not the name.

---

## Phases

| Phase | When | Reference file | Output |
|---|---|---|---|
| 0 — Round onboarding | Always first | `prompts/phase0-onboarding.md` | `progress.md` + test folder |
| 1 — Matrix | Always | `prompts/phase1-matrix.md` | `matrix.md` + `tracking/batches.json` |
| 2 — Long-form copy | Always | `prompts/phase2-copy.md` | one `.md` per batch in `drafts/` |
| 3 — Quality gate | Always, before any approval | `prompts/phase3-quality-gate.md` | `gate-report.md` |
| 4 — Visual hook and image brief | Always | `prompts/phase4-hook-and-image.md` | `image-brief.md` (K prompts per batch) |
| 5 — Image generation | After 4 is approved | `prompts/phase5-generation.md` | named PNGs in each batch's folder |
| 6 — Delivery | Always last | `prompts/phase6-delivery.md` | 2 `.docx` per batch (copy + INFOS) + `upload.csv` |

Read the phase file **at the moment you execute it**.

Phases 2 and 3 are the core. Phase 3 is not optional and not negotiable: it is what stops a round from shipping with copy that violates a known lock.

---

## Rule 3 — the copy comes from the squad, not from your head

Copy quality comes from the `Copy-Master-Xquads` squad (a sibling tool folder: `Copy-Master-Xquads/`), 32 specialists plus an orchestrator with an 8-point gate.

`knowledge/xquad-routing.md` maps **which specialist to pull for which angle and which block of the copy**. Consult it before writing each batch and declare in the draft header which voices were used.

Do not improvise the routing: a male confession angle is not written in the same voice as a medical authority angle, and the squad exists precisely for that.

---

## Rule 4 — the image is the hook, and hooks have their own skill

In long form static the image does not illustrate the copy: **it is the hook**, and it carries the decision to read or not read on its own. The psychological work is the same as a video hook; only the channel changes.

That is why Phase 4 **invokes `hook-lab` for real**, through the `Skill` tool, before any image prompt is written. Its gates (Momentum+Virality on the Big Idea, the 7-element headline checklist) are not skippable, and if the batch idea does not pass the gate, no image will fix it.

An image scene does not come from visual taste or a suggestion table. It comes from a qualified hook concept.

---

## Rule 5 — the deliverable is not the copy, it is the whole ad

A long form static on Meta has **five pieces**, and missing any one of them blocks the upload:

1. **Primary text** — the long-form copy. The first three lines are what shows before "see more": they decide whether the rest gets read.
2. **Image** — 1:1, job is to stop the scroll.
3. **Link headline** — appears under the image, next to the button.
4. **Link description** — one line under the headline.
5. **CTA** — the button.

`knowledge/meta-placement.md` carries the character limits and the patterns that work. No batch ships without all five fields.

And there is a sixth piece, which is not part of the ad but decides whether it works: **the page that runs it**. First-person long form does not run off the brand page. See `knowledge/publishing-profiles.md` for the profile types, the congruence rule between POV and page, and the compliance line you do not cross (especially on the authority angle).

---

## Naming — fixed standard

```
Folder : {AUTHOR} {BRAND-SKU} T###-B{batch}/
Docx   : {AUTHOR} {BRAND-SKU} T###-B{batch}.docx
Image  : {AUTHOR} {BRAND-SKU} T###-B{batch}-{variation}.png
INFOS  : infos/{AUTHOR} {BRAND-SKU} T###-B{batch} INFOS.docx
```

- `{AUTHOR}` — the writer's initials, two letters
- `{BRAND-SKU}` — brand and product code, e.g. `BRAND-SKU`
- `T###` — the test
- `B{batch}` — the batch, which is the **angle x awareness level combination**, numbered sequentially. In a 5-angle x 3-level round there are **15 batches, B1 to B15**: B1 = Angle 1 level A, B2 = Angle 1 level B, B3 = Angle 1 level C, B4 = Angle 2 level A, ... B15 = Angle 5 level C. Formula: `batch = (angle - 1) x 3 + level index + 1` (A=0, B=1, C=2)
- `{variation}` — 1, 2 or 3 (avatar cluster of the image), **always after a hyphen**: `T101-B1-1`. Without the hyphen `B11` would be ambiguous (batch 11, or batch 1 variation 1)

Angles are called **Angle 1 to Angle 5**, never B1 to B5. The level stays a letter (A = Problem aware, B = Solution aware, C = Hidden cause) and lives in the draft frontmatter (`level:`), next to `angle_num:`. It is not part of the filename.

Full example: `AA BRAND-SKU T101-B1/AA BRAND-SKU T101-B1.docx` and the images `AA BRAND-SKU T101-B1-1.png`, `-2.png`, `-3.png`. In the upload sheet, `ad_set` = `T101-B1` and `ad` = `AA BRAND-SKU T101-B1-1`.

The `.docx` carries no variation because **the copy is the same across the three images**. One copy, three images, one copy document (plus its INFOS document in `infos/`).

Confirm only the test code (`T###`) with the user the first time. The rest is derived.

---

## Where the files live

Everything inside the test folder, inside the product:

```
creatives/T### - DDMM [Long Form Ads]/
├── AA BRAND-SKU T###-B1/            <- one folder per batch (angle x level)
│   ├── AA BRAND-SKU T###-B1.docx     <- copy only
│   ├── AA BRAND-SKU T###-B1-1.png    <- the 3 image variations
│   ├── AA BRAND-SKU T###-B1-2.png
│   └── AA BRAND-SKU T###-B1-3.png
├── AA BRAND-SKU T###-B2/ ... B15/    <- 5 angles x 3 levels = 15 batches, 15 folders
├── infos/AA BRAND-SKU T###-B1 INFOS.docx <- angle, level and the prompts of the 3 images
├── matrix.md
├── image-brief.md
├── gate-report.md
├── upload.csv
├── drafts/                          <- the source .md of each copy
├── support/                         <- references, swipe, raw prompts
└── tracking/batches.json
```

**One folder per batch:** every batch (angle x level combination) has its own folder holding exactly 4 files, the copy docx and the 3 images. The scripts already write there. A round of 5 angles x 3 levels makes 15 batches and 15 folders, B1 to B15.

Never leave an image in a temp folder and never leave a source `.md` loose in the root. This follows the house output naming convention (the short-form ads skill, section 7).

---

## Critical rules

1. **The production locks in `knowledge/production-locks.md` are mandatory in every copy.** Each one has a number behind it. A violation fails the gate.
2. **This format's casting supersedes the house default.** See `knowledge/casting-longform.md` — long form static uses a man 45 to 60 with ethnicity as the tested variable; the young-woman default from `ads-builder` does not apply here, and the reason is documented.
3. **No em dashes and no quotation marks in the final copy** (fixed house rule for ad copy output). Dialogue is marked with a line break and isolation, never with quotation marks.
4. **Every number in the copy comes from the real brief.** Lab value between 350 and 412, price in dollars, guarantee per current policy. Nothing invented.
5. **Never generate the K images of a batch without a written approval of the brief.**
6. **When the round closes, log every batch in the product kill list** — angle, level, hook and file, so the next round does not repeat it.

---

## Where this skill sits

- **Before:** `creative-intel` produces the read that becomes the locks. `mechanism-lab` locks the mechanism. The round structure document supplied by the user is the source of the matrix.
- **After:** `creative-intel` reads the round result and returns updated locks. Whatever wins becomes video through `ads-builder` and an advertorial through `adv-builder`.
- **Do not confuse:** `ads-builder` makes short creative (UGC video, image with lettering). `adv-builder` makes page advertorials. This skill makes the hybrid: the image changes, the long copy lives in the post.
