"""Example deck 2: 'How you pay for AI work is changing' — accent / dark alternating, light CTA.

    python examples/pricing_models.py
    python -m rocket.render check examples/out/pricing-models.html
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rocket import Brand, Deck, c  # noqa: E402

brand = Brand.load(ROOT / "examples" / "brand.json")
TAG = "pricing"

PLANS = """<svg viewBox="0 0 940 320">
<g class="st" stroke-width="2.5" fill="none"><rect x="30" y="70" width="270" height="230" rx="18"/>
<rect x="640" y="70" width="270" height="230" rx="18"/></g>
<rect x="335" y="20" width="270" height="280" rx="18" class="flc"/>
<g class="t fl" style="font-size:20px"><text x="58" y="116">BUILD</text><text x="668" y="116">OUTCOME</text></g>
<text x="363" y="66" class="t" style="font-size:20px;fill:var(--kwtext)">USAGE</text>
<g class="fl" opacity=".5"><rect x="58" y="150" width="200" height="12" rx="5"/><rect x="58" y="178" width="160" height="12" rx="5"/>
<rect x="58" y="206" width="180" height="12" rx="5"/><rect x="668" y="150" width="200" height="12" rx="5"/>
<rect x="668" y="178" width="150" height="12" rx="5"/><rect x="668" y="206" width="180" height="12" rx="5"/></g>
<g style="fill:var(--kwtext)" opacity=".75"><rect x="363" y="104" width="210" height="12" rx="5"/><rect x="363" y="132" width="170" height="12" rx="5"/>
<rect x="363" y="160" width="190" height="12" rx="5"/></g>
<rect x="363" y="236" width="214" height="40" rx="20" style="fill:var(--kwtext)"/>
</svg>"""

MODELS = """<svg viewBox="0 0 940 250">
<g class="dim" stroke-width="2"><path d="M150 30 V230"/></g>
<g class="st" stroke-width="2.5" fill="none"><rect x="170" y="24" width="300" height="52" rx="12"/>
<rect x="170" y="99" width="520" height="52" rx="12"/><rect x="170" y="174" width="700" height="52" rx="12"/></g>
<rect x="170" y="174" width="240" height="52" rx="12" class="flc"/>
<g class="t fl" style="font-size:20px"><text x="190" y="57">ONE-OFF BUILD</text><text x="190" y="132">PER RUN</text></g>
<text x="430" y="207" class="t fl" style="font-size:20px">PER RESULT</text>
<g class="t fl" text-anchor="end" style="font-size:17px" opacity=".6"><text x="140" y="57">01</text>
<text x="140" y="132">02</text><text x="140" y="207">03</text></g>
</svg>"""

deck = Deck(brand, palette=("accent", "dark", "light"), slug="pricing-models",
            title="How you pay for AI work is changing", tag=TAG)

deck.cover(
    eyebrow=c.eyebrow("PRICING", "WHAT IS CHANGING"),
    headline="How you pay for AI<br>work is quietly<br>" + c.accent("changing."),
    sub="Retainers and per-seat licences are giving way to usage and outcomes. Worth understanding before you sign.",
    art=PLANS)

deck.slide(c.eyebrow("THE SHIFT", "WHY SEATS STOPPED WORKING"), "Per-seat pricing lost its logic.",
           c.bd("Software was priced per person because people did the work. When an agent does it instead, "
                "a seat count stops measuring anything real."),
           c.panel(c.eyebrow("THE OLD LOGIC", "vs WHAT IS TRUE NOW"),
                   c.rows(("THEN", "More staff, more licences, more value."),
                          ("NOW", "The work runs at 2am with nobody logged in."))))

deck.slide(c.eyebrow("MODEL 01", "BUILD FEE"), "You buy the system once.",
           c.bd("A fixed price to design and build it, then it is yours to run. The oldest model, "
                "and still the right one more often than people admit."),
           c.panel(c.eyebrow("THE TRADE", "ONE-OFF BUILD"),
                   c.rows(("BEST FOR", "Steady, predictable volume."),
                          ("YOU GET", "Ownership and costs you can forecast."),
                          ("WATCH FOR", "Who maintains it in month six, and at what price."))))

deck.slide(c.eyebrow("MODEL 02", "USAGE"), "You pay for what it runs.",
           c.bd("A price per conversation, per document, per workflow run. Costs follow your actual activity "
                "instead of your headcount."),
           c.panel(c.eyebrow("THE TRADE", "PAY PER RUN"),
                   c.rows(("BEST FOR", "Volume that moves month to month."),
                          ("YOU GET", "A small start; you pay for real work done."),
                          ("WATCH FOR", "A busy month costing far more than planned."))))

deck.slide(c.eyebrow("MODEL 03", "OUTCOME"), "You pay when it works.",
           c.bd("Per booked call, per resolved ticket, per qualified lead. The newest model, and the one that puts "
                "the risk on the provider rather than you."),
           c.panel(c.eyebrow("THE TRADE", "PAY PER RESULT"),
                   c.rows(("BEST FOR", "A job with one clear, countable result."),
                          ("YOU GET", "Little downside if it does not perform."),
                          ("WATCH FOR", "How “a result” is defined. Agree it in writing."))))

deck.slide(c.eyebrow("THE CATCH", "USAGE PRICING"), "A meter with no ceiling is a risk.",
           c.bd("Usage pricing is fair until the month a loop misfires or a spike floods your inbox. "
                "Then the bill arrives."),
           c.panel(c.eyebrow("ASK FOR ALL FOUR", "BEFORE YOU AGREE"),
                   c.chips("A monthly cap", "An alert at 70%", "A kill switch", "A dry-run estimate")
                   + c.pv("Good providers offer these <b>without being asked twice</b>.")))

deck.slide(c.eyebrow("HOW TO CHOOSE", "A SHORT GUIDE"), "Match the model to your volume.",
           c.bd("There is no best model, only a best fit. It comes down to how predictable your volume is "
                "and how much proof you still need."),
           c.diagram(MODELS, "further down, more risk sits with the provider")
           + c.chips("Predictable → build fee", "Spiky → usage + cap", "Unproven → outcome"))

deck.cta("Not sure which<br>" + c.accent("one fits?"), "PRICING",
         ["Which model fits your volume, and why",
          "The caps and clauses to ask for in writing",
          "A rough cost range for your use case"])

if __name__ == "__main__":
    print("wrote", deck.save(ROOT / "examples" / "out" / "pricing-models.html"))
