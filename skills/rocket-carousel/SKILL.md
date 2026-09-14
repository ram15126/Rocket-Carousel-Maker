---
name: rocket-carousel
description: Build Instagram/LinkedIn carousels with Rocket Carousel Maker v2. Use for "make a carousel", "carousel about X", "turn this into a carousel", "write carousel captions", "export carousels as PDF/PNG". Writes a Python deck script, renders 1080x1350 slides, verifies overflow and fonts, exports PNG/PDF/ZIP and captions.
---

# Rocket Carousel

You are building carousels with the `rocket` package in this repository. Follow `docs/SOP.md`. These are the non-negotiables:

## Workflow

1. **Read** `brand.json` (fall back to `examples/brand.json`) and run `python -m rocket brand <file>`.
2. **Brief.** Get the topic, reader, one takeaway, CTA keyword and three deliverables. If the user only gives a topic, choose the rest and state what you chose.
3. **Scaffold.** Run `python -m rocket new <slug>`, then write the deck in `decks/<slug>.py`. Use `examples/lead_flow.py` as the reference for tone and density.
4. **Build.** Run `python decks/<slug>.py`.
5. **Verify.** Run `python -m rocket.render check decks/out/<slug>.html --sheet --out decks/out`. When it reports overflow, **cut copy**. Never shrink type. Then look at the contact sheet image before you report back.
6. **Export.** Run `python -m rocket.render export decks/out/<slug>.html --out exports`.
7. **Captions** (if asked). Write `captions.json` and run `python -m rocket.captions captions.json --out exports`. Deliver `.txt`/`.docx`, not markdown.

## Content rules

- Every slide teaches something specific. No filler, and no statistics without a source.
- One idea per slide. Content headlines are 2 lines at most, body is about 35 words or fewer, and each slide has exactly one block (`panel` + `rows`/`chips`, `diagram`, or `stat_jump`).
- The cover headline is 3 short lines, and the last line is wrapped in `c.accent(...)`.
- The CTA uses a single uppercase keyword and three concrete deliverables.

## Design rules

- Only the three brand colours. Choose `palette=(odd, even, cta)` so it differs from the other decks in the batch, and make sure slide 7 and the CTA don't share a background.
- Diagrams are inline SVG using the classes `st` / `stc` / `fl` / `flc` / `dim` / `t`, so they recolour per slide. Keep the viewBox about 940 wide.
- Cover art: use an SVG the user supplied, recoloured with `python -m rocket.recolor <file> --bg <cover bg>`. Never reuse the same art across decks. Don't scrape or bulk-download illustration libraries. Respect their licences.
- No social icons on slides.

## Report back with

The file paths (HTML, PDF, PNG folder, captions), the check result line, and the contact sheet image.
