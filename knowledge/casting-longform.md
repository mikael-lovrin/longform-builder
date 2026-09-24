# Casting and image — long form static

## Explicit supersession of the house default

The house casting guidelines that ship with the short-form ads skill (`ads-builder`) say the opposite of what this format needs. That file says: an overwhelming majority of **young white women, visual register in their twenties**, and it forbids wide ethnic variation inside a single batch (a correction given by the user in August 2026, driven by a short-form video batch).

**For long form static that rule does not apply**, and the reason is documented:

1. The product is sold to a **man 40 to 60**. In UGC video the young woman was the *narrator*, not the buyer's avatar. In long form static the image is the buyer's hook, not the spokesperson.
2. The **25-34 band shows 0.501 ROAS in the raw table, but those are exactly the 55 ads of one young-woman angle, which drops from 0.572 to 0.281 once May is excluded.** That is a May asset, not an avatar. Promoting a young avatar off that number repeats the mistake that cost four months.
3. The **53-60 band has the best cost per checkout in the account, $88.**

The old rule still holds where it was born: UGC video with a female narrator. Do not delete it, do not rewrite it. This file governs this format.

---

## The K variations per batch

The copy is the same in all of them. **The only variable tested in the image is the avatar cluster.**

**The default axis is ethnicity**, and it holds whenever the round does not specify another:

| Variation | Avatar |
|---|---|
| `1` | White American |
| `2` | Black |
| `3` | Latino |

When the angle calls for a female voice, the same distribution applies to women: **1 white American, 2 Black, 3 Latina.**

> **How this gets decided.** The user supplies the angles and the avatars each round, in Phase 0. If they specify a different axis (age band, composition, setting), the round file governs. **If they do not specify, the default is ethnicity.** The age band stays locked inside the angle's band and never becomes a variable by accident.

## Age band per angle (locked, not a variable)

| Angle POV | Avatar in the image | Band |
|---|---|---|
| Female, partner running a protocol | woman, or a couple scene | 45-55 (her) |
| Female, present-tense pain | woman alone | 45-55 |
| Male confession | man alone | 48-58 |
| Authority | physician in an office, or a man hearing the diagnosis | 45-60 |
| Single villain, neutral | man, or a symbolic image | 45-58 |

**Never 25-34.** In no batch, in no variation.

## Locked body rules (project memory, still in force)

- **Always a fit lean build**, aspirational: gray at the temples, salt-and-pepper beard, defined jaw.
- **Never any weight or fat cue**, in any state, not even in the before.
- Before and after is shown **only through energy**: tired eyes, hunched posture, dropped shoulder. Never through body.

## Setting

- The avatar alone in frame. **Avoid other people in the background**, even blurred (exception: the couple scene, when the angle calls for it).
- **Avoid background motion**: a car driving, traffic, blurred lights. A parked car is fine.
- Environments: home, kitchen, bedroom, porch, doctor's office, garage, parked car. Enclosed or controlled.

## What the image is for

The image **does not sell**. Its only job is to stop the scroll and earn the tap on see more.

Three families that work in this format:
- **Aspirational portrait** — the man the reader wants to be, or the woman whose attention he wants
- **Domestic scene** — the couple, the kitchen at 2 a.m., the couch
- **Proof** — the lab sheet, a symbolic split, the object that anchors the story

## Mandatory rules for the image prompt

Inherited from the house static image psychology guidelines, with one adjustment. Every prompt specifies, in this order:

1. Style declaration
2. Dimensions and format
3. Central subject and specific appearance: age, **ethnicity (mandatory here, it is the tested variable)**, clothing, expression, body language
4. What the subject is doing, a specific action and not a pose
5. Environmental detail
6. Lighting: direction, quality, temperature
7. Palette: 4 to 5 named colors
8. **What is NOT in the frame: no product, no logo, no before-and-after split, no embedded text**
9. Text inside the image: in this format, **none**. The hook is visual, the copy lives in the post.
10. Camera and composition: lens, angle, depth, grain
11. The emotional tone the image has to produce, in one sentence
12. Aspect ratio 1:1

**The relevant difference from `ads-builder`:** there is no lettering here. In short creative the embedded text is part of the hook; in long form static it competes with the copy and cuts the piece's organic reach.

## Pose: avoid a twisted torso with a bracing hand

Learned in a previous round. A pose with the body turned to one side, the head looking back over the shoulder and a hand braced on something (a door frame, a wall, a table) comes out with an arm crossing the body or a hand that belongs to no one. Write the pose as three-quarters to the camera, the bracing hand on the SAME side as the support, the other arm loose, and close the Action with an `Anatomy:` line (two arms, two hands, five fingers, no arm crossing the body, no extra limb).

## Image tone: do not mirror the pain of the copy

A previous round shipped with every image in a register of still pain (quiet shame, low light, washed-out palette) and the whole set came out depressing. The top competitor's library does the opposite: **an image of pleasure or promise with fear-driven copy**. The contrast between the two is what makes the piece aggressive. When writing the brief, choose the image's tone on purpose, not as a reflex of the copy's wound.

## Natural POV (learned in production)

When there is no avatar in the frame, the image is shot from the narrator's eyes. Three forms read as a real photo:

1. **One hand only**, entering from the edge of the frame, because the other hand holds the phone
2. **An empty room, no hand at all**, shot at eye height from the doorway
3. **The hand resting on the body** (knee, thigh), not posed on the object

What reads as artificial and gets regenerated: both arms entering from the top of the frame (strange anatomy), and a hand placed on the object like a product shot. In the empty-room form the skin and age cues leave the frame, so use it only when the cell's variable does not depend on the image.

## Doctors: casting follows the real doctor

In the authority angle the page and the copy belong to a **contracted, real** doctor. The doctor's image does not vary ethnicity: it follows how the real doctor looks. The cell's ethnicity variable moves to the other images (the patient, the couple). Whenever a real photo of the doctor exists, it replaces the generated image before the ad runs, because the model does not keep the same face across images.
