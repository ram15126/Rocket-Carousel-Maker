"""Building blocks for slide content.

Every function returns an HTML string. Text arguments are treated as HTML, so
you can use <b>bold</b> for emphasis. Use esc() for untrusted text.

Budget per content slide (1080x1350) that reliably fits:
  headline <= 2 lines, body <= ~35 words, and ONE block:
    panel with <= 3-4 rows   |   panel with <= 6 chips + one line
    diagram + one chip row   |   split stat
"""
from __future__ import annotations

import html as _html


def esc(text: str) -> str:
    return _html.escape(text, quote=False)


def eyebrow(lead: str, rest: str = "") -> str:
    """Two-part mono label: accent-coloured lead, muted remainder.  eyebrow("STEP 02", "QUALIFY")"""
    return f"<i>{lead}</i>" + (f" · {rest}" if rest else "")


def accent(text: str) -> str:
    """Italic serif accent phrase, usually the last line of a headline."""
    return f'<span class="flourish">{text}</span>'


def bd(text: str) -> str:
    """Body paragraph."""
    return f'<p class="bd">{text}</p>'


def pv(text: str) -> str:
    """Short supporting line, used inside panels."""
    return f'<div class="pv">{text}</div>'


def panel(caption: str, inner: str) -> str:
    """Bordered data panel with a mono caption.  caption accepts eyebrow()-style <i> lead."""
    return f'<div class="panel"><div class="cap">{caption}</div>{inner}</div>'


def chips(*items: str) -> str:
    return '<div class="chips">' + "".join(f'<span class="chip">{i}</span>' for i in items) + "</div>"


def rows(*pairs: tuple[str, str]) -> str:
    """Labelled rows: rows(("WHAT", "..."), ("WHEN", "...")). Keep labels <= 13 characters."""
    return '<div class="tl">' + "".join(
        f'<div class="r"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in pairs) + "</div>"


tl = rows  # alias


def kv(caption: str, value: str) -> str:
    return f'<div class="cap">{caption}</div><div class="pv">{value}</div>'


def split(left: str, right: str) -> str:
    """Two columns with a hairline divider."""
    return f'<div class="split"><div>{left}</div><div class="rule"></div><div>{right}</div></div>'


def stat_jump(before: str, after: str, caption: str, note: str) -> str:
    """ '20 min -> 104 hrs' style comparison with a note on the right. """
    return split(
        f'<div class="jump"><span class="n">{before}</span><span class="ar">&rarr;</span>'
        f'<span class="n on">{after}</span></div><div class="sub">{caption}</div>',
        f'<div class="pv">{note}</div>')


def diagram(svg: str, label: str) -> str:
    """Framed inline SVG. Inside the SVG use these classes so it recolours per slide:
         st  stroke in text colour     stc  stroke in accent
         fl  fill in text colour       flc  fill in accent
         dim hairline stroke           t    mono label text (combine: class="t fl")"""
    return f'<div class="dia">{svg}<div class="lab">{label}</div></div>'
