# Rocket Carousel Maker v2

Build Instagram and LinkedIn carousels in Python. Each deck is one HTML file with 1080×1350 slides. A headless browser checks that every slide fits and every font loaded, then exports PNGs, a PDF and a ZIP.

v2 replaces the v1 approach of hand-writing HTML and copying templates. A deck is now a short script. Colours, type, spacing and the CTA are handled by the system, so every carousel looks consistent and nothing ends up off the slide.

```python
from rocket import Brand, Deck, c

brand = Brand.load("examples/brand.json")
deck = Deck(brand, palette=("dark", "light", "accent"), slug="lead-flow", tag="lead systems")

deck.cover(eyebrow=c.eyebrow("LEAD FLOW", "SIX STOPS"),
           headline="Every enquiry makes<br>the same journey.<br>" + c.accent("Most break at 2."),
           sub="The six stops between a message and a sale, and where they leak.")

deck.slide(c.eyebrow("STOP 03", "QUALIFY"), "Three questions sort every lead.",
           c.bd("The smallest set of answers that tells you who gets called today."),
           c.panel(c.eyebrow("THE MINIMUM SET"),
                   c.rows(("WHAT", "What are they trying to get done?"),
                          ("WHEN", "This month, or someday?"),
                          ("WHO", "Do they sign it off?"))))

deck.cta("Want your flow<br>" + c.accent("mapped?"), "FLOW",
         ["Your six stops, drawn out", "Where leads go cold", "The one fix to do first"])

deck.save("decks/out/lead-flow.html")
```

## Quick start

```bash
pip install -r requirements.txt
```

```bash
python -m playwright install chromium
```

```bash
python examples/lead_flow.py
```

```bash
python -m rocket.render check examples/out/*.html --sheet --out examples/out
```

```bash
python -m rocket.render export examples/out/*.html --out exports
```

Open `examples/out/lead-flow.html` in a browser to see a preview grid with **Download PDF** and **PNGs (ZIP)** buttons. The Python export gives more reliable results, so use it for anything you publish.

## What's in the box

| Path | What it does |
|---|---|
| `rocket/theme.py` | `Brand`: three colours, four fonts, handle, site and CTA wording, plus a contrast report |
| `rocket/engine.py` | `Deck`: cover, content slides and CTA. It numbers the slides, alternates the backgrounds and writes the HTML |
| `rocket/components.py` | Slide building blocks: `eyebrow`, `accent`, `bd`, `panel`, `rows`, `chips`, `split`, `stat_jump`, `diagram` |
| `rocket/render.py` | Playwright checks for overflow and fonts, 2× PNG export, img2pdf PDF, ZIP and a contact sheet |
| `rocket/recolor.py` | Recolours any flat SVG illustration to your palette for a dark, light or accent slide |
| `rocket/captions.py` | Checks captions (hashtag count, required tag, hook length) and writes `.txt` and `.docx` files |
| `rocket/__main__.py` | `python -m rocket new <slug>` scaffolds a deck. `python -m rocket brand <file>` prints the contrast report |
| `examples/` | Two complete 8-slide decks, a brand file and a captions file |
| `docs/SOP.md` | The full workflow and design rules |
| `skills/rocket-carousel/SKILL.md` | A Claude Code skill that runs this workflow end to end |
| `legacy/v1/` | The original v1 SOP, templates, skills and HTML carousels, kept for reference |

## The design system in one screen

- **Three colours only.** Dark, light and accent. Every slide background is one of the three.
- **Alternating backgrounds.** `palette=(cover/odd, even, cta)`. Give each deck a different combination so your grid doesn't repeat: `("dark","light","accent")`, `("accent","dark","light")`, `("light","dark","accent")`, and so on.
- **Clear hierarchy on every slide.** Mono eyebrow, then a bold display headline, then a 34px body, then one block (panel, rows, chips, diagram or stat).
- **One idea per slide.** The headline is at most 2 lines and the body is about 35 words or fewer. Every slide carries one block, and the space is spread out so there are no empty bands.
- **A big cover.** A three-line headline that ends in an italic serif accent, a one-sentence promise, and optional art up to 960×400.
- **A strong CTA.** A keyword card ("comment FLOW"), three numbered things they get, and a fine-print line.
- **Verified before export.** `render check` fails if any slide overflows or a font didn't load.

Full rules and the step-by-step workflow are in [docs/SOP.md](docs/SOP.md).

## Make it yours

Copy `examples/brand.json` to `brand.json` and change the name, handle, site, colours, fonts and CTA wording. Then run:

```bash
python -m rocket brand brand.json
```

```bash
python -m rocket new my-first-deck
```

Fonts can come from any stylesheet URL (Google Fonts, Fontshare) or a local `@font-face` file. Put the family name and the CSS URL in `fonts`.

## Illustrations

Rocket does **not** download or bundle illustrations. Bring your own SVGs and recolour them:

```bash
python -m rocket.recolor my-art.svg --bg dark --brand brand.json -o art-dark.svg
```

Before you use artwork from any library, read its licence. Some free libraries allow commercial use but forbid automated downloading, redistributing their files, or building tools around their collection. Download files by hand, and only where the licence allows. The inline SVG diagrams in `examples/` were drawn for this project and are MIT-licensed along with the rest of the code.

## Requirements

Python 3.9+, Playwright (Chromium), Pillow, img2pdf. python-docx is optional and only needed for `.docx` captions. Fonts load from their CDNs, so rendering needs a network connection.

## Licence

MIT. See [LICENSE](LICENSE).
