# Phase 0 — Round onboarding

Goal: open the round with the variables locked and the folder created. Cheap and fast; it saves everything after it.

## Step 1 — Check continuity

Look for `progress.md` in the test folder. If it exists, read it, say which phase the round stopped at, and ask whether to continue or restart. If it does not exist, keep going.

## Step 2 — Confirm the round variables

Ask all at once, in one block, and accept a short answer:

1. **Test code and date** (e.g. T101, 24/09) — defines the folder and the naming
2. **Product and offer code** (e.g. the product name, `BRAND-SKU`)
3. **The matrix** — how many angles, how many levels, how many image variations. Common default: 5 x 3 x 3
4. **Destination** (quiz, PDP, advertorial) — defines the CTA and the link description
5. **Delivery language** (English for the US market, another language for the team)
6. **Author initials** for the naming (two letters)

If the user already gave all of that in the initial request, **do not ask again**, just confirm in one line and move on.

## Step 3 — Read the round structure

Read `knowledge/method-batches.md` (the how, stable) and the round file at `knowledge/rounds/T###.md` (the what, specific).

**If the round has no file yet, create it** from `knowledge/rounds/_TEMPLATE.md`. The angles come from the user, not from the previous round and not from a competitor swipe. Ask:

- What the angles of this round are, and the lock on each one
- The image variation axis (default: ethnicity, 1 white / 2 Black / 3 Latino)
- The locked mechanism, if it changed
- Proper names to use (physician, characters) — see the placeholder policy below

If the user pointed to a new structure document (PDF/docx), read the document and write the round file from it. A silent divergence between the document and the skill contaminates the whole round.

**Placeholder policy:** when a proper name is not confirmed, pick one and write it as if it were final. No brackets, no note, no reminder to check. The copy ships ready to publish and the swap, if any, is a string replacement.

## Step 4 — Create the folder

```
creatives/T### - DDMM [Long Form Ads]/
├── drafts/
├── support/
└── tracking/
```

## Step 5 — Read the brand context

In this order, and only what exists:
- The product's `kill-list.md` — no angle or hook already burned can come back
- The `brief.md` or offer doc — price, guarantee, ingredients, doses
- The most recent creative intelligence report for the account

**If the offer is not documented (dollar price, current guarantee, doses), ask now.** LOCK 6 requires a price in the copy and LOCK 10 requires a lab number; writing 15 copies and finding out afterwards that the price is wrong costs the entire round.

## Step 6 — Open `progress.md`

```markdown
# Progress — T### Long Form Ads
Product: [name] ([code])
Matrix: [N] angles x [M] levels x [K] images = [N*M] copies, [N*M*K] images
Destination: [quiz/PDP]
Language: [en/pt]
Last phase: Phase 0 — Onboarding
Next phase: Phase 1 — Matrix
Naming: {AUTHOR} {BRAND-SKU} T###-B{batch}-{variation}  (batch = angle x level, B1..B[N*M]; e.g. T101-B1-1)
```
