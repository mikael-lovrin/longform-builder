# Phase 3 — Quality gate

This is not a copy edit. It is the gate that stops the round from shipping in violation of a known lock. It runs over **every** batch before any approval, and it produces `gate-report.md`.

## Part 1 — House locks (automatic, run the script)

```bash
python "$HOME/.claude/skills/longform-builder/scripts/check_locks.py" drafts/
```

The script checks whatever is verifiable from the text:

| Lock | Check |
|---|---|
| LOCK 1 | 3 proof modalities declared in the frontmatter |
| LOCK 2 | the product name present in the body |
| LOCK 3 | position of the first product mention > 50% of the text; absence of trick/secret/hack |
| LOCK 6 | a dollar sign with a number present |
| LOCK 10 | a number between 350 and 412 present |
| LOCK 11 | zero em dashes, zero quotation marks |
| LOCK 12 | first 3 lines between 200 and 400 characters |
| — | length inside the angle's band |
| — | enemy block: all 4 terms present |

**A failure on LOCK 11 or LOCK 3 blocks.** The rest become named open items.

## Part 2 — The Xquad 8-point gate (manual)

Run the squad's `checklists/output-quality.md` (COPY-M-CL-001). The CRITICAL items block delivery. See the translation of the three most relevant items in `knowledge/xquad-routing.md`.

## Part 3 — The checks only a human read catches

**1. Opening swap test.** Take the first 3 lines of the 3 cells of the same angle (e.g. B1, B2 and B3 for Angle 1). If they could be swapped between cells without anyone noticing, the columns are not differentiated. The whole row fails.

**2. Angle swap test.** Take the 5 cells of the same level (e.g. level A = B1, B4, B7, B10, B13). If two of them could trade angle names without a single rewrite, one of those two angles does not actually exist.

**3. Mobile paragraph test.** No block longer than 4 lines in the first 1,500 characters.

**4. Self-declaration test.** Search for first person declaring a result. Every occurrence becomes a rewrite.

**5. Villain test.** Is the main culprit biology? If the doctor or the industry became the central villain, it violates LOCK 5.

**6. Urgency test.** The only legitimate urgency is the biological window. Stock scarcity, imminent censorship or an expiring offer fail on LOCK 7.

## `gate-report.md`

```markdown
# Gate — T### Long Form Ads
Run on: YYYY-MM-DD | 15 batches

## Blocks
| Batch | Lock | What happened | Action |

## Open items
| Batch | Item | Note |

## Approved with no reservation
B1, B3, B4, ...

## Read of the set
- Are the 3 columns differentiated?
- Are the 5 angles differentiated?
- Do the 15 copies sound like 15 people?
```

No batch goes to Phase 4 with an open block.
