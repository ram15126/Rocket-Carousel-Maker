"""Brand configuration: three colours, four fonts, handle, site, CTA wording."""
from __future__ import annotations

import copy
import json
import pathlib

DEFAULT = {
    "name": "rocket",            # wordmark text, rendered as  name.  with the dot in the accent colour
    "handle": "@yourhandle",
    "site": "yoursite.com",
    "colors": {
        "dark": "#1B3022",       # deep field colour
        "light": "#F4EFE6",      # paper / cream
        "accent": "#FF6542",     # the one colour that does the pointing
    },
    # Text colour on accent-coloured slides: "light", "dark", or "auto" (pick higher contrast)
    "accent_text": "light",
    "fonts": {
        "display": {"family": "Clash Display",
                    "css": "https://api.fontshare.com/v2/css?f[]=clash-display@500,600,700&display=swap"},
        "body":    {"family": "Satoshi",
                    "css": "https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap"},
        "mono":    {"family": "Space Mono",
                    "css": "https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap"},
        "serif":   {"family": "Fraunces",
                    "css": "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@1,9..144,500;1,9..144,600&display=swap"},
    },
    "cta": {
        "eyebrow": "<i>YOUR MOVE</i> · WORK WITH US",
        "card_left": "comment this word",
        "card_right": "on this post",
        "list_caption": "what lands in your dms",
        "fineprint": "free · no pitch · usually same day",
    },
}


def _merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6:
        raise ValueError(f"not a hex colour: #{h}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def luminance(h: str) -> float:
    """WCAG relative luminance."""
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = hex_to_rgb(h)
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


class Brand:
    def __init__(self, data: dict | None = None):
        self.data = _merge(DEFAULT, data or {})
        for role in ("dark", "light", "accent"):
            hex_to_rgb(self.colors[role])  # validates

    @classmethod
    def load(cls, path: str | pathlib.Path | None = None, **overrides) -> "Brand":
        data = {}
        if path:
            data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        return cls(_merge(data, overrides))

    # -- accessors ---------------------------------------------------------
    @property
    def name(self) -> str: return self.data["name"]
    @property
    def handle(self) -> str: return self.data["handle"]
    @property
    def site(self) -> str: return self.data["site"]
    @property
    def colors(self) -> dict: return self.data["colors"]
    @property
    def fonts(self) -> dict: return self.data["fonts"]
    @property
    def cta(self) -> dict: return self.data["cta"]

    def rgb(self, role: str) -> str:
        return "%d,%d,%d" % hex_to_rgb(self.colors[role])

    def accent_text_role(self) -> str:
        """Which of dark/light sits on accent-coloured slides."""
        mode = self.data.get("accent_text", "light")
        if mode in ("light", "dark"):
            return mode
        c = self.colors
        return "light" if contrast(c["light"], c["accent"]) >= contrast(c["dark"], c["accent"]) else "dark"

    def font_links(self) -> list[str]:
        seen, out = set(), []
        for f in self.fonts.values():
            url = f.get("css")
            if url and url not in seen:
                seen.add(url)
                out.append(url)
        return out

    def contrast_report(self) -> list[tuple[str, float, float]]:
        """(pairing, ratio, recommended minimum). Large bold display text can live with ~3:1."""
        c = self.colors
        at = self.accent_text_role()
        return [
            ("light text on dark", contrast(c["light"], c["dark"]), 4.5),
            ("dark text on light", contrast(c["dark"], c["light"]), 4.5),
            (f"{at} text on accent", contrast(c[at], c["accent"]), 3.0),
        ]
