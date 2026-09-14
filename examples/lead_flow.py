"""Example deck 1: 'Every enquiry makes the same journey' — dark / light alternating, accent CTA.

    python examples/lead_flow.py
    python -m rocket.render check examples/out/lead-flow.html
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rocket import Brand, Deck, c  # noqa: E402

brand = Brand.load(ROOT / "examples" / "brand.json")
TAG = "lead systems"

JOURNEY = """<svg viewBox="0 0 940 210">
<g class="dim" stroke-width="2" stroke-dasharray="3 9"><path d="M70 105 H870"/></g>
<g class="st" stroke-width="2.5"><circle cx="70" cy="105" r="26"/><circle cx="230" cy="105" r="26"/>
<circle cx="390" cy="105" r="26"/><circle cx="550" cy="105" r="26"/><circle cx="710" cy="105" r="26"/></g>
<circle cx="870" cy="105" r="30" class="flc"/>
<g class="fl"><circle cx="70" cy="105" r="6"/><circle cx="230" cy="105" r="6"/><circle cx="390" cy="105" r="6"/>
<circle cx="550" cy="105" r="6"/><circle cx="710" cy="105" r="6"/></g>
<g class="t fl" text-anchor="middle" style="font-size:19px"><text x="70" y="172">ARRIVE</text><text x="230" y="172">ACK</text>
<text x="390" y="172">QUALIFY</text><text x="550" y="172">ROUTE</text><text x="710" y="172">FOLLOW</text></g>
<text x="870" y="172" text-anchor="middle" class="t flc" style="font-size:19px">CLOSE</text>
<g class="t fl" text-anchor="middle" style="font-size:17px" opacity=".55"><text x="70" y="52">01</text><text x="230" y="52">02</text>
<text x="390" y="52">03</text><text x="550" y="52">04</text><text x="710" y="52">05</text><text x="870" y="52">06</text></g>
</svg>"""

LEAKS = """<svg viewBox="0 0 940 190">
<g class="dim" stroke-width="2"><path d="M40 95 H900"/></g>
<g class="st" stroke-width="2.5"><circle cx="40" cy="95" r="10"/><circle cx="900" cy="95" r="10"/></g>
<g class="stc" stroke-width="3"><path d="M235 95 v54"/><path d="M450 95 v54"/><path d="M665 95 v54"/></g>
<g class="flc"><circle cx="235" cy="95" r="11"/><circle cx="450" cy="95" r="11"/><circle cx="665" cy="95" r="11"/>
<circle cx="235" cy="163" r="6"/><circle cx="450" cy="163" r="6"/><circle cx="665" cy="163" r="6"/></g>
<g class="t fl" text-anchor="middle" style="font-size:18px"><text x="235" y="62">NIGHT GAP</text>
<text x="450" y="62">NO OWNER</text><text x="665" y="62">NO RECORD</text></g>
</svg>"""

deck = Deck(brand, palette=("dark", "light", "accent"), slug="lead-flow",
            title="Every enquiry makes the same journey", tag=TAG)

deck.cover(
    eyebrow=c.eyebrow("LEAD FLOW", "SIX STOPS"),
    headline="Every enquiry makes<br>the same journey.<br>" + c.accent("Most break at 2."),
    sub="The six stops between “someone messaged you” and “someone paid you” — and where they quietly leak.",
    art=JOURNEY)

deck.slide(c.eyebrow("STOP 01", "ARRIVAL"), "It never arrives where you think.",
           c.bd("Enquiries land across several channels at once, and hardly any of them are your contact form. "
                "If arrival is scattered, everything downstream is guesswork."),
           c.panel(c.eyebrow("WHERE IT LANDS", "TYPICAL SPREAD"),
                   c.chips("WhatsApp", "Instagram DM", "Missed call", "Web form", "Email")
                   + c.pv("The first fix is <b>one shared inbox</b>, not another channel.")))

deck.slide(c.eyebrow("STOP 02", "ACKNOWLEDGEMENT"), "The clock starts immediately.",
           c.bd("The gap between their message and your first reply is the biggest thing you control. "
                "It costs nothing to close."),
           c.panel(c.eyebrow("THE FIRST REPLY", "WHAT IT MUST DO"),
                   c.rows(("CONFIRM", "You have it, and who is looking at it."),
                          ("ANSWER", "The one obvious question they were about to ask."),
                          ("OFFER", "A specific next step with a time attached."))))

deck.slide(c.eyebrow("STOP 03", "QUALIFY"), "Three questions sort every lead.",
           c.bd("Qualification is not an interrogation. It is the smallest set of answers that tells you "
                "who gets called today and who gets a nurture sequence."),
           c.panel(c.eyebrow("THE MINIMUM SET", "ASK BEFORE YOU SEND"),
                   c.rows(("WHAT", "What are they actually trying to get done?"),
                          ("WHEN", "Is this a this-month problem or a someday one?"),
                          ("WHO", "Are they the person who signs it off?"))))

deck.slide(c.eyebrow("STOP 04", "ROUTE"), "Not every lead needs the same speed.",
           c.bd("Routing is where most systems stop and most revenue leaks. Hot leads need a person within the hour. "
                "Everything else needs a queue that will not forget."),
           c.panel(c.eyebrow("THREE LANES", "ONE RULE EACH"),
                   c.rows(("HOT", "A person calls today."),
                          ("WARM", "Sequence starts, human check-in on day three."),
                          ("COLD", "Nurture list. Quiet, useful, monthly."))))

deck.slide(c.eyebrow("STOP 05 — 06", "FOLLOW &amp; RECORD"), "Deals die in follow-up four.",
           c.bd("Almost nobody buys on first contact, and almost nobody keeps following up past the second attempt. "
                "The winners are simply the ones who did not stop."),
           c.panel(c.eyebrow("A SEQUENCE", "NO GUESSWORK"),
                   c.rows(("DAY 0", "Instant acknowledgement, question answered."),
                          ("DAY 1", "Human reply with a specific next step."),
                          ("DAY 3", "A useful nudge — a case, not a chase."),
                          ("DAY 7", "Direct ask, then move to nurture."))))

deck.slide(c.eyebrow("THE LEAKS", "WHERE IT BREAKS"), "Three gaps, every time.",
           c.bd("In most businesses the same three gaps account for most of the lost pipeline — "
                "and none of them is a sales-skill problem."),
           c.diagram(LEAKS, "the three places pipeline disappears")
           + c.chips("Auto-acknowledge", "Name an owner", "Log everything"))

deck.cta("Want your flow<br>" + c.accent("mapped?"), "FLOW",
         ["Your six stops, drawn out as a diagram",
          "The exact points where leads go cold",
          "The one fix to do first, and why"])

if __name__ == "__main__":
    print("wrote", deck.save(ROOT / "examples" / "out" / "lead-flow.html"))
