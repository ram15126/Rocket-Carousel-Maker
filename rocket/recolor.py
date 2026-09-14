"""Recolour any flat SVG illustration onto your brand palette for a given slide background.

Bring your own artwork. Check the licence of wherever it came from: some illustration
libraries allow commercial use but forbid automated downloading, redistribution in packs,
or use inside tools built around them. Rocket does not download or bundle illustrations.

    python -m rocket.recolor art.svg --bg dark  --brand examples/brand.json -o art-dark.svg
    python -m rocket.recolor art.svg --bg accent --accent-from "#6c63ff"

How colours are mapped (by the source colour's own lightness/saturation):
    skin tones (light, saturated)  -> text colour at ~75%
    saturated mid colours          -> accent  (on accent slides: the dark colour)
    darkest colours                -> text colour (the drawing)
    mid greys                      -> text colour at ~60%
    near-white                     -> slide background
    light greys                    -> text colour at ~15%
Gradients and filters are removed (flat look); clip paths and masks are kept.
"""
from __future__ import annotations

import argparse
import colorsys
import pathlib
import re
import sys

from .theme import Brand, hex_to_rgb

NAMED = {"white": "#ffffff", "black": "#000000"}


def _role(hexc: str, force_accent: set[str]) -> str:
    h = hexc.lower()
    if h in force_accent:
        return "accent"
    r, g, b = hex_to_rgb(h)
    _, light, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    luma = 0.2126 * r / 255 + 0.7152 * g / 255 + 0.0722 * b / 255
    if light > 0.72 and sat >= 0.30:
        return "skin"
    if sat >= 0.45 and 0.25 <= light <= 0.72:
        return "accent"
    if luma < 0.20:
        return "figure"
    if luma < 0.50:
        return "mid"
    if luma >= 0.97:
        return "field"
    return "tint"


def palette_for(brand: Brand, bg: str) -> dict:
    c = brand.colors
    if bg == "dark":
        t = brand.rgb("light")
        return dict(figure=c["light"], mid=f"rgba({t},.58)", tint=f"rgba({t},.15)", skin=f"rgba({t},.74)",
                    field=c["dark"], accent=c["accent"])
    if bg == "light":
        t = brand.rgb("dark")
        return dict(figure=c["dark"], mid=f"rgba({t},.58)", tint=f"rgba({t},.13)", skin=f"rgba({t},.5)",
                    field=c["light"], accent=c["accent"])
    if bg == "accent":
        at = brand.accent_text_role()
        other = "dark" if at == "light" else "light"
        t = brand.rgb(at)
        return dict(figure=c[at], mid=f"rgba({t},.62)", tint=f"rgba({t},.2)", skin=f"rgba({t},.78)",
                    field=c["accent"], accent=c[other])
    raise ValueError("bg must be dark, light or accent")


def recolor(svg: str, brand: Brand, bg: str, accent_from: list[str] | None = None) -> str:
    target = palette_for(brand, bg)
    force = {("#" + a.lower().lstrip("#")) for a in (accent_from or [])}
    force = {("#" + "".join(ch * 2 for ch in f[1:])) if len(f) == 4 else f for f in force}

    def sub_hex(m):
        h = m.group(0)
        if len(h) == 4:
            h = "#" + "".join(ch * 2 for ch in h[1:])
        return target[_role(h, force)]

    out = svg
    out = re.sub(r"<\?xml.*?\?>", "", out, flags=re.S)
    # flat look: drop gradients and filters, but keep <defs>/<style>/clipPath/mask
    out = re.sub(r"<(linear|radial)Gradient\b.*?</\1Gradient>", "", out, flags=re.S | re.I)
    out = re.sub(r"<filter\b.*?</filter>", "", out, flags=re.S | re.I)
    out = re.sub(r'\sfilter="[^"]*"', "", out)
    # paints that pointed at a removed gradient become the drawing colour (placeholder so the
    # hex pass below does not remap the already-mapped value)
    out = re.sub(r'(fill|stroke)="url\(#[^)]*\)"', lambda m: f'{m.group(1)}="@@FIGURE@@"', out)
    out = re.sub(r'(fill|stroke)\s*:\s*url\(#[^)]*\)', lambda m: f'{m.group(1)}:@@FIGURE@@', out)
    # named colours -> hex, then map every source hex exactly once
    out = re.sub(r'((?:fill|stroke|stop-color)="\s*)(white|black)(\s*")',
                 lambda m: m.group(1) + NAMED[m.group(2)] + m.group(3), out)
    out = re.sub(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", sub_hex, out)
    out = out.replace("@@FIGURE@@", target["figure"])
    # unfilled shapes default to black in SVG; make the default the drawing colour
    out = re.sub(r"<svg\b", f'<svg fill="{target["figure"]}"', out, count=1)
    # let CSS size it
    out = re.sub(r'(<svg\b[^>]*?)\swidth="[^"]*"', r"\1", out, count=1)
    out = re.sub(r'(<svg\b[^>]*?)\sheight="[^"]*"', r"\1", out, count=1)
    return out.strip()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", help="input SVG file")
    ap.add_argument("--bg", required=True, choices=["dark", "light", "accent"], help="background of the slide it sits on")
    ap.add_argument("--brand", help="brand JSON (defaults to the built-in palette)")
    ap.add_argument("--accent-from", action="append", default=[], metavar="HEX",
                    help="force this source colour to the accent role (repeatable)")
    ap.add_argument("-o", "--out", help="output file (default: stdout)")
    args = ap.parse_args(argv)
    brand = Brand.load(args.brand)
    result = recolor(pathlib.Path(args.svg).read_text(encoding="utf-8"), brand, args.bg, args.accent_from)
    if args.out:
        pathlib.Path(args.out).write_text(result, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
