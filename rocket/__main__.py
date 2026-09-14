"""rocket command line.

    python -m rocket new my-deck                 # scaffold decks/my_deck.py from the template
    python -m rocket brand examples/brand.json   # contrast report for a brand file
    python -m rocket.render check decks/out/*.html
    python -m rocket.render export decks/out/*.html --out exports
    python -m rocket.recolor art.svg --bg dark --brand brand.json -o art-dark.svg
    python -m rocket.captions captions.json --out exports
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

from .theme import Brand

TEMPLATE = '''"""{title}"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rocket import Brand, Deck, c  # noqa: E402

brand = Brand.load(ROOT / "brand.json" if (ROOT / "brand.json").exists() else ROOT / "examples" / "brand.json")

# palette = (cover + odd slides, even slides, CTA). Use a different combination for each deck.
deck = Deck(brand, palette=("dark", "light", "accent"), slug="{slug}", title="{title}", tag="topic")

deck.cover(
    eyebrow=c.eyebrow("TOPIC", "ANGLE"),
    headline="A specific promise<br>in three short lines.<br>" + c.accent("The twist."),
    sub="One sentence on what the reader gets by swiping.",
    art="")  # inline <svg>; see: python -m rocket.recolor --help

deck.slide(c.eyebrow("POINT 01", "NAME"), "One idea, said plainly.",
           c.bd("Two or three sentences that earn the headline. Use <b>bold</b> for the phrase that matters."),
           c.panel(c.eyebrow("THE DETAIL", "LABEL"),
                   c.rows(("WHAT", "A concrete specific."),
                          ("WHY", "The consequence."),
                          ("HOW", "The action."))))

deck.slide(c.eyebrow("POINT 02", "NAME"), "Another idea, said plainly.",
           c.bd("Keep every slide to one idea. If you need a comma to join two, split the slide."),
           c.panel(c.eyebrow("CHECKLIST", "LABEL"),
                   c.chips("First", "Second", "Third", "Fourth")
                   + c.pv("A one-line takeaway with <b>the key phrase</b> in bold.")))

deck.cta("Want this done<br>" + c.accent("for you?"), "KEYWORD",
         ["The first thing they get", "The second thing they get", "The third thing they get"])

if __name__ == "__main__":
    print("wrote", deck.save(ROOT / "decks" / "out" / "{slug}.html"))
'''


def cmd_new(slug: str) -> int:
    slug = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-")
    if not slug:
        print("give the deck a name, e.g. python -m rocket new lead-flow")
        return 2
    path = pathlib.Path("decks") / f"{slug.replace('-', '_')}.py"
    if path.exists():
        print(f"{path} already exists")
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE.format(slug=slug, title=slug.replace("-", " ").capitalize()), encoding="utf-8")
    print(f"created {path}\n  edit it, then:  python {path}  &&  python -m rocket.render check decks/out/{slug}.html")
    return 0


def cmd_brand(path: str | None) -> int:
    b = Brand.load(path)
    print(f"{b.name}  {b.handle}  {b.site}")
    for role in ("dark", "light", "accent"):
        print(f"  {role:<6} {b.colors[role]}")
    print(f"  text on accent slides: {b.accent_text_role()}")
    ok = True
    for label, ratio, need in b.contrast_report():
        flag = "ok " if ratio >= need else "LOW"
        ok &= ratio >= need
        print(f"  [{flag}] {label:<22} {ratio:4.1f}:1  (aim for {need}:1)")
    if not ok:
        print("  tip: try \"accent_text\": \"auto\", or keep accent-slide text large and bold")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rocket", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="scaffold a deck script")
    n.add_argument("slug")
    b = sub.add_parser("brand", help="print a brand's colours and contrast report")
    b.add_argument("path", nargs="?")
    args = ap.parse_args(argv)
    return cmd_new(args.slug) if args.cmd == "new" else cmd_brand(args.path)


if __name__ == "__main__":
    sys.exit(main())
