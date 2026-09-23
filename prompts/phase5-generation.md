# Phase 5 — Image generation (Higgsfield)

Starts only after `image-brief.md` has been approved in writing.

## Default route: the Higgsfield MCP

Fixed parameters for this format:

| Parameter | Value |
|---|---|
| `model` | `nano_banana_pro` |
| `aspect_ratio` | `1:1` |
| `resolution` | `2k` |

**No reference `medias` in this format.** A product mockup does not enter: rule 8 of the prompt forbids product and logo in the frame, and that is what makes the image look native.

## Flow per image

1. `mcp__higgsfield__generate_image` with the prompt from the brief
2. `mcp__higgsfield__job_status` with `sync: true` until `status: completed`
3. Download the `rawUrl` **straight to the final filename**, in the cell's folder (`AA BRAND-SKU T101-B1-A/`)

```bash
curl -sL "<rawUrl>" -o "AA BRAND-SKU T101-B1-A/AA BRAND-SKU T101-B1-A1.png"
```

Never leave it in a temp folder to rename later. The final name is the download name.

## Batch automation

For all 45 images, use the script. It reads the brief, feeds the MCP calls and validates the result:

```bash
python "$HOME/.claude/skills/longform-builder/scripts/image_batch.py" plan \
    --brief image-brief.md --test T101 --product BRAND-SKU
```

The `plan` mode produces `tracking/image-jobs.json` with one record per image: id, prompt, final filename, status. **The MCP call is made by you**, reading that file, because MCP is not reachable from inside a Python script. After each generation, record it with:

```bash
python "$HOME/.claude/skills/longform-builder/scripts/image_batch.py" record \
    --id B1-A1 --url "<rawUrl>"
```

The `record` mode downloads into the cell's folder (creating it if needed), names, validates the dimensions and updates the JSON. At the end:

```bash
python "$HOME/.claude/skills/longform-builder/scripts/image_batch.py" verify
```

`verify` confirms that all 45 exist, are 1:1, have a plausible file size and that no filename is off standard.

## Generation order

Do not generate all 45 at once without warning. Generate **one complete batch first** (3 images, the 3 ethnicities of the same scene), show it to the user and confirm that the scene replicated correctly across the variations. Only then continue.

That is where you catch the most expensive error of the phase: the model changing the scene along with the ethnicity, which destroys the cluster read.

## Mandatory visual check

Before considering the phase done, **open and look at** at least:
- the 3 images of the first batch generated (did the scene replicate?)
- one image from every batch (does the scene match the angle?)

Check specifically:
- [ ] Actually 1:1, no letterboxing and no white bars
- [ ] No embedded text appeared
- [ ] No product or logo in the frame
- [ ] No weight or fat cue
- [ ] Nobody in the background
- [ ] The ethnicity is the declared one and the age sits inside the band

If any item fails, regenerate with that point reinforced in the prompt. Do not deliver with a caveat.
