"""Rocket Carousel Maker.

Build Instagram / LinkedIn carousels as one self-contained HTML file per deck,
verify every slide renders (no overflow, fonts loaded), then export PNG + PDF.

    from rocket import Brand, Deck, c
    brand = Brand.load("examples/brand.json")
    deck = Deck(brand, palette=("dark", "light", "accent"), slug="my-deck")
    deck.cover(eyebrow=c.eyebrow("TOPIC", "ANGLE"), headline="...", sub="...")
    deck.slide(eyebrow=..., headline=..., body=c.bd("..."), block=c.panel(...))
    deck.cta(headline="...", keyword="WORD", gets=["...", "...", "..."])
    deck.save("out/my-deck.html")
"""
from .theme import Brand
from .engine import Deck
from . import components as c

__all__ = ["Brand", "Deck", "c"]
__version__ = "2.0.0"
