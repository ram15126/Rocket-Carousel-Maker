# Carousel SOP (v2)

This is how a carousel goes from idea to published files. Follow the steps in order. Each step has a check, and a step isn't finished until its check passes.

---

## 1. Brief

Write this down before you write any slides:

| Field | Example |
|---|---|
| Topic | Why enquiries go cold |
| Reader | Owner of a 5–50 person service business |
| The one takeaway | Most leads are lost in the first reply, not on price |
| Proof | A process, numbers you can cite, or a named framework |
| CTA keyword | FLOW |
| What they get for commenting | 3 concrete deliverables |

**Check:** you can say the takeaway in one sentence.

## 2. Structure (8 slides is the default)

| # | Role | Contents |
|---|---|---|
| 1 | Cover | Eyebrow, three-line headline ending in an accent phrase, one-line promise, optional art |
| 2–7 | Content | One idea per slide, each with one block |
| 8 | CTA | Keyword card, three numbered things they get, fine print |

Patterns that work: *six stops / steps*, *three models + the catch + how to choose*, *myth → truth*, *before → after*, *checklist*.

**Check:** read the headlines of slides 1–7 on their own. They should tell the whole story.

## 3. Copy rules

- **Headline:** 2 lines at most on content slides and 3 on the cover. Keep it concrete. Avoid questions on content slides.
- **Eyebrow:** `c.eyebrow("LEAD", "REST")`, uppercase, 2–4 words per part. The lead part tells the reader where they are ("STOP 03", "MODEL 02").
- **Body:** about 35 words or fewer. Bold the one phrase that matters with `<b>`.
- **Blocks:** labels in `rows` stay at 13 characters or fewer. Use 3–4 rows, or up to 6 chips plus one line.
- **Value first.** Every slide teaches something. Don't write filler slides like "let's dive in" or "follow for more".
- **No invented statistics.** Use a number only if you can name its source.

## 4. Design rules

1. **Three colours.** Dark, light and accent come from `brand.json`, and no other colours are allowed.
2. **Alternate backgrounds.** Use `palette=(odd, even, cta)`, and give every deck in a batch a different combination.
3. **Hierarchy.** Eyebrow at 26px mono, headline at 70–74px display 600–700, body at 34px, block text at 29–30px. Don't shrink type to make copy fit. Cut copy instead.
4. **No empty bands.** `.body-wrap` spreads the eyebrow, headline, body and block down the slide. If a slide still looks empty, add a block. Don't make the type bigger to fill it.
5. **Contrast.** Run `python -m rocket brand brand.json`. Light-on-dark and dark-on-light should reach 4.5:1. Text on the accent should reach 3:1 because it is set large and bold. If it falls short, set `"accent_text": "auto"`.
6. **Cover art.** Covers should be different from each other. Never reuse the same illustration across decks in a batch. Art sits in a 960×400 box.
7. **Diagrams** are inline SVG built from the recolouring classes (`st`, `stc`, `fl`, `flc`, `dim`, `t`), so they switch colour with the slide background automatically.
8. **No social-media icons** on slides. The handle in the footer does that job.

## 5. Build

```bash
python -m rocket new lead-flow
```

Edit `decks/lead_flow.py`, then run:

```bash
python decks/lead_flow.py
```

## 6. Verify

```bash
python -m rocket.render check decks/out/*.html --sheet --out decks/out
```

- The command exits 1 and lists the slide if anything overflows or a font failed to load. Fix the copy and run it again.
- Open `decks/out/contact-sheet.png` and look at the whole batch at once. Look for repeated covers, two neighbouring slides with the same background, and slides that look empty.

**Check:** the output ends with `OK: no overflow, fonts loaded`.

## 7. Export

```bash
python -m rocket.render export decks/out/*.html --out exports
```

For each deck you get `exports/<deck>/<deck>-slide-NN.png` (2160×2700), `exports/<deck>.pdf` and `exports/<deck>-png.zip`.

## 8. Captions

Write `captions.json` (see `examples/captions.json`), then run:

```bash
python -m rocket.captions captions.json --out exports
```

- **Instagram:** a hook line under 125 characters, 2–4 short value lines, a save prompt, the comment-keyword CTA, then the hashtags.
- **LinkedIn:** a hook line, a numbered or arrowed breakdown, one question to invite comments, then the hashtags.
- The tool enforces the hashtag count and required brand tag set in the JSON. Output is `.txt` per deck plus `ALL-CAPTIONS.txt` and `.docx`.

## 9. Ship

Hand over the PDF (for LinkedIn documents), the PNG folder (for Instagram) and the caption files. Keep the deck `.py` script. It is the source, and a rebuild takes seconds.
