# Phase 4 — Visual hook and image brief

## The premise that organizes the phase

**In long form static, the image is the hook.** It does not illustrate the copy and it does not sell the product. Its only job is to stop the scroll and buy the tap on see more.

That changes who decides the image. The scene does not come from a suggestion table or from visual taste: it comes from the same process that produces a video hook, because the psychological work is identical. What changes is the channel, not the function.

So this phase runs in two stages, and the first one belongs to `hook-lab`.

---

## Stage 1 — Generate and qualify the visual hook concepts

**Invoke `hook-lab` for real**, through the `Skill` tool. Do not describe its process here and do not reproduce its frameworks from memory: its gates are literal and not skippable.

What to ask `hook-lab`, per batch:

> Format: long form static for Meta, cold top of funnel. The hook is the IMAGE, not the line. I need 4 to 5 visual hook concepts of different types for angle [X], level [Y], with the Big Idea and the mechanism already locked in [file]. Each concept has to describe the scene that stops the scroll, not the line.

What it returns and what you use:

| hook-lab phase | What lands here |
|---|---|
| 1 — Big Idea Check | The Momentum+Virality gate. **If the batch idea does not pass, the image will not save it.** Go back to the copy before spending on images |
| 2 — Hook generation | 4 to 5 concepts tagged by type (Contrarian, Open Loop, Ouch Factor, Bold Statement, Curiosity) |
| 3 — Headline QA | The 7-element checklist, applied to the visual concept |

**Translating the verbal types into a scene**, which is the only part of the work that belongs to this skill:

| Hook type | How it becomes an image |
|---|---|
| `Ouch Factor` | the scene the reader recognizes and wishes he did not: the smooth sheet on the empty side, the couch at eight |
| `Open Loop` | the scene that does not explain itself: the woman smiling in the kitchen at 1:47 |
| `Contrarian` | the scene that contradicts the expectation: the 58-year-old with the energy of a 30-year-old |
| `Bold Statement` | the object that carries the claim: the lab sheet in his hand |
| `Curiosity` | the detail that is out of place: two bottles sitting next to her vitamins |

## Stage 2 — From the winning scene to the K prompts

**One scene per batch, replicated across the K variations.** Inside a batch the images are the same scene, the same framing, the same light, the same emotion. The avatar changes, and nothing else.

If the scene changes too, the test stops measuring the avatar and starts measuring the scene, and the cluster read dies.

Between batches the scene **must** change: every angle has its own hook.

Read `knowledge/casting-longform.md` before writing the prompts. It supersedes the default casting of `ads-builder` and explains why.

### Format in `image-brief.md`

```markdown
### B1 — Partner running a protocol x Problem aware

**Hook concept (hook-lab):** [type] — why this scene stops the scroll
**Passed Momentum+Virality:** yes
**Locked scene:** woman alone, kitchen, 1:47 a.m., warm light off the stove, mug in both hands, looking out of frame.

#### B1-1 — woman 45-52 · white
**Prompt:**
(full prompt, 12 items)

#### B1-2 — woman 53-60 · Black
**Prompt:**
(identical, changing only the subject description)

#### B1-3 — couple 45-60 · Latino
**Prompt:**
(same)
```

The batch header is `### B{batch} — {Angle} x {Level}` and each variation header is `#### B{batch}-{variation} — {label}`. The hyphen before the variation is mandatory (`B11-1`, never `B111`), and the scripts parse exactly this pattern. The batch must be at `###` and the variation at `####`: with `##` the last variation swallows the next batch.

## Mandatory check on every prompt

- [ ] Ethnicity declared explicitly (it is the tested variable)
- [ ] Age band inside the angle's locked band, never 25-34
- [ ] `fit lean build`, aspirational; **zero weight or fat cue**, not even in the before
- [ ] No other people in the background (except a declared couple scene)
- [ ] No background motion
- [ ] Declared what is NOT in the frame: no product, no logo, no split, **no embedded text**
- [ ] Aspect ratio 1:1
- [ ] Emotional tone declared in one sentence

**No lettering in this format.** In short creative the embedded text is part of the hook; here it competes with the copy of the post and cuts reach.

## Approve before generating

Present the brief with the hook concept next to each scene and wait for written approval. Phase 5 costs money, and 45 wrong images cost 45 times.
