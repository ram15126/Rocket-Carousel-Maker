"""Deck -> one self-contained HTML carousel (1080x1350 slides + in-browser PNG/PDF export)."""
from __future__ import annotations

import html as _html
import pathlib
import warnings

from .theme import Brand

ROLES = ("dark", "light", "accent")

CSS = r"""
:root{
  --dark:__D__; --light:__L__; --accent:__A__;
  --font-display:"__FD__","Helvetica Neue",Arial,sans-serif;
  --font-body:"__FB__",system-ui,sans-serif;
  --font-mono:"__FM__",ui-monospace,monospace;
  --font-serif:"__FS__",Georgia,serif;
}
*{ box-sizing:border-box; margin:0; padding:0; }

/* ===== three colours only; every slide is one of them ===== */
.slide{ position:relative; width:1080px; height:1350px; overflow:hidden;
  font-family:var(--font-body); -webkit-font-smoothing:antialiased;
  padding:74px 78px 92px; display:flex; flex-direction:column; }
.slide[data-bg="dark"]{ background:var(--dark); color:var(--light); --kwtext:var(--dark);
  --ac:var(--accent); --muted:rgba(__LRGB__,.9); --dim:rgba(__LRGB__,.66); --line:rgba(__LRGB__,.28);
  --panel:rgba(__LRGB__,.05); --strong:var(--light); }
.slide[data-bg="light"]{ background:var(--light); color:var(--dark); --kwtext:var(--light);
  --ac:var(--accent); --muted:rgba(__DRGB__,.86); --dim:rgba(__DRGB__,.6); --line:rgba(__DRGB__,.28);
  --panel:rgba(__DRGB__,.035); --strong:var(--dark); }
.slide[data-bg="accent"]{ background:var(--accent); color:var(--__AT__); --kwtext:var(--accent);
  --ac:var(--__AO__); --muted:var(--__AT__); --dim:rgba(__ATRGB__,.94); --line:rgba(__ATRGB__,.55);
  --panel:rgba(__ATRGB__,.12); --strong:var(--__AT__); }
.slide::before{ content:""; position:absolute; inset:0; pointer-events:none;
  background:radial-gradient(120% 80% at 18% 12%, rgba(255,255,255,.055), transparent 62%); }
.slide[data-bg="light"]::before{ background:radial-gradient(120% 80% at 18% 12%, rgba(__DRGB__,.045), transparent 62%); }
.slide > *{ position:relative; z-index:1; }

/* ---------- top bar ---------- */
.top{ display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:52px; }
.wm{ font-family:var(--font-display); font-weight:600; font-size:34px; letter-spacing:-.01em; }
.wm i{ color:var(--ac); font-style:normal; }
.pg{ font-family:var(--font-mono); font-weight:700; font-size:23px; letter-spacing:.12em; color:var(--dim); }
.pg b{ color:var(--ac); font-weight:400; }

/* ---------- hierarchy: eyebrow / headline / body ---------- */
.eb{ font-family:var(--font-mono); font-weight:700; font-size:26px; letter-spacing:.18em;
  text-transform:uppercase; color:var(--dim); margin-bottom:30px; }
.eb i{ color:var(--ac); font-style:normal; }
h1.hl{ font-family:var(--font-display); font-weight:600; font-size:74px; line-height:1.03;
  letter-spacing:-.012em; word-spacing:.08em; margin-bottom:18px; }
h2.hl{ font-family:var(--font-display); font-weight:700; font-size:70px; line-height:1.08;
  letter-spacing:-.01em; word-spacing:.08em; margin-bottom:30px; }
.flourish{ font-family:var(--font-serif); font-style:italic; font-weight:600; color:var(--ac); }
.bd{ font-family:var(--font-body); font-weight:500; font-size:34px; line-height:1.5;
  color:var(--muted); max-width:38ch; }
.bd b{ color:var(--strong); font-weight:700; }
.bd + .bd{ margin-top:18px; }

/* no dead space: distribute the blocks instead of pushing one to the bottom */
.body-wrap{ flex:1; display:flex; flex-direction:column; justify-content:space-between; gap:18px; }

/* ---------- panel ---------- */
.panel{ border:1px solid var(--line); border-radius:18px; background:var(--panel); padding:32px 34px; }
.panel .cap, .cap{ font-family:var(--font-mono); font-weight:700; font-size:23px; letter-spacing:.15em;
  text-transform:uppercase; color:var(--dim); }
.cap i{ color:var(--ac); font-style:normal; }
.pv{ font-family:var(--font-body); font-weight:500; font-size:29px; line-height:1.46; color:var(--muted); margin-top:16px; }
.pv b{ color:var(--strong); font-weight:700; }
.split{ display:grid; grid-template-columns:1fr 1px 1fr; gap:34px; align-items:start; }
.split .rule{ background:var(--line); height:100%; min-height:120px; }
.jump{ display:flex; align-items:baseline; gap:16px; margin-top:14px; flex-wrap:nowrap; }
.jump .n{ font-family:var(--font-display); font-weight:700; font-size:68px; line-height:1;
  letter-spacing:-.03em; white-space:nowrap; }
.jump .n.on, .jump .ar{ color:var(--ac); }
.jump .ar{ font-size:34px; }
.sub{ font-family:var(--font-mono); font-weight:700; font-size:21px; color:var(--dim); margin-top:12px; letter-spacing:.06em; }

/* ---------- chips ---------- */
.chips{ display:flex; flex-wrap:wrap; gap:16px; margin-top:28px; }
.chip{ border:1.5px solid var(--line); border-radius:12px; padding:15px 24px;
  font-family:var(--font-mono); font-weight:700; font-size:24px; color:var(--muted); }
.chip::before{ content:"\00B7  "; color:var(--ac); }

/* ---------- labelled rows ---------- */
.tl{ margin-top:28px; }
.tl .r{ display:grid; grid-template-columns:210px 1fr; gap:26px; align-items:baseline;
  padding:18px 0; border-top:1px solid var(--line); }
.tl .r:last-child{ border-bottom:1px solid var(--line); }
.tl .k{ font-family:var(--font-mono); font-weight:700; font-size:23px; color:var(--ac); letter-spacing:.05em; line-height:1.25; }
.tl .v{ font-family:var(--font-body); font-weight:600; font-size:30px; line-height:1.36; color:var(--strong); }

/* ---------- art + diagrams ---------- */
.coverart{ margin-top:6px; width:100%; display:flex; justify-content:center; align-items:flex-end; }
.coverart svg{ width:100%; max-width:960px; height:auto; max-height:400px; display:block; }
.dia{ margin-top:26px; border:1px solid var(--line); border-radius:16px; background:var(--panel); padding:30px 28px 22px; }
.dia svg{ width:100%; height:auto; display:block; }
.dia .lab{ font-family:var(--font-mono); font-weight:700; font-size:21px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--dim); margin-top:16px; }
.st{ stroke:currentColor; fill:none; } .stc{ stroke:var(--ac); fill:none; }
.fl{ fill:currentColor; } .flc{ fill:var(--ac); } .dim{ stroke:var(--line); fill:none; }
text.t{ font-size:20px; }
text.t, .t text{ font-family:var(--font-mono); letter-spacing:.1em; }

/* ---------- footer ---------- */
.ft{ display:flex; align-items:center; justify-content:space-between; margin-top:30px;
  font-family:var(--font-mono); font-size:22px; color:var(--dim); letter-spacing:.05em; }

/* ---------- cover ---------- */
.cover-sub{ font-family:var(--font-body); font-weight:600; font-size:31px; line-height:1.36; max-width:26ch; color:var(--muted); }
.swipe{ font-family:var(--font-mono); font-weight:700; font-size:24px; letter-spacing:.18em; text-transform:uppercase;
  color:var(--dim); margin-top:20px; display:flex; align-items:center; gap:14px; }
.swipe .dot{ width:9px; height:9px; border-radius:50%; background:var(--ac); display:inline-block; }

/* ---------- CTA ---------- */
.kwcard{ margin-top:32px; border:2px solid var(--ac); border-radius:20px; overflow:hidden; }
.kwcard .kw-top{ display:flex; align-items:center; justify-content:space-between; padding:16px 30px;
  border-bottom:2px solid var(--ac); font-family:var(--font-mono); font-size:21px; letter-spacing:.2em;
  text-transform:uppercase; color:var(--ac); }
.kwcard .kw-main{ display:flex; align-items:center; justify-content:space-between; padding:26px 30px 30px; background:var(--ac); }
.kwcard .kw-word{ font-family:var(--font-display); font-weight:700; font-size:92px; line-height:1; letter-spacing:-.02em; color:var(--kwtext); }
.kwcard .kw-arrow{ width:70px; height:70px; border-radius:50%; border:2.5px solid var(--kwtext);
  display:flex; align-items:center; justify-content:center; }
.kwcard .kw-arrow svg{ width:34px; height:34px; }
.kwcard .kw-arrow svg path{ stroke:var(--kwtext); }
.gets{ margin-top:30px; }
.gets .getcap{ font-family:var(--font-mono); font-weight:700; font-size:23px; letter-spacing:.15em;
  text-transform:uppercase; color:var(--dim); margin-bottom:4px; }
.gets .g{ display:grid; grid-template-columns:64px 1fr; gap:24px; align-items:baseline; padding:16px 0; border-top:1px solid var(--line); }
.gets .g:last-child{ border-bottom:1px solid var(--line); }
.gets .gi{ font-family:var(--font-mono); font-weight:700; font-size:24px; color:var(--ac); }
.gets .gt{ font-family:var(--font-body); font-weight:600; font-size:30px; line-height:1.34; color:var(--strong); }
.fineprint{ margin-top:26px; font-family:var(--font-mono); font-weight:700; font-size:23px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--dim); }
"""

# Browser-only preview grid + "Download PDF / PNGs" buttons. Not used by the Python renderer
# (which runs with JavaScript disabled so slides stay at full size).
PREVIEW = r"""
<style>
  html,body{ background:#111; margin:0; }
  body{ font-family:var(--font-mono); color:#eee; padding:0 0 120px; }
  .bar{ position:sticky; top:0; z-index:50; display:flex; gap:14px; align-items:center; padding:16px 24px;
        background:rgba(17,17,17,.92); backdrop-filter:blur(8px); border-bottom:1px solid #2a2a2a; }
  .bar h1{ font-size:14px; font-weight:400; letter-spacing:.05em; margin-right:auto; color:#bbb; }
  .bar button{ font:inherit; font-weight:700; font-size:13px; cursor:pointer; border:1px solid #444;
        background:var(--dark); color:var(--light); padding:10px 16px; border-radius:9px; }
  .bar button.primary{ background:var(--accent); border-color:var(--accent); }
  .stage{ display:flex; flex-wrap:wrap; gap:22px; justify-content:center; padding:34px 22px; }
  .frame{ position:relative; overflow:hidden; border-radius:12px; box-shadow:0 18px 50px rgba(0,0,0,.5); background:#000; }
  .frame .slide{ transform-origin:top left; }
  .frame .n{ position:absolute; top:8px; left:10px; z-index:3; font-size:11px; color:#fff;
        background:rgba(0,0,0,.5); padding:3px 8px; border-radius:999px; }
</style>
<script src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.13/dist/html-to-image.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.2/jspdf.umd.min.js"></script>
<script>
(function(){
  var W=1080,H=1350, SLUG=document.body.dataset.slug||"carousel";
  var slides=Array.prototype.slice.call(document.querySelectorAll(".slide"));
  function buildPreview(){
    var cols=Math.min(slides.length, window.innerWidth>1280?3:window.innerWidth>760?2:1);
    var scale=Math.min(.42,(Math.min(window.innerWidth-104,1400)-26*(cols-1))/cols/W);
    var stage=document.createElement("div"); stage.className="stage";
    slides.forEach(function(s,i){ var f=document.createElement("div"); f.className="frame";
      f.style.width=(W*scale)+"px"; f.style.height=(H*scale)+"px"; s.style.transform="scale("+scale+")";
      var t=document.createElement("div"); t.className="n"; t.textContent=(i+1)+" / "+slides.length;
      f.appendChild(s); f.appendChild(t); stage.appendChild(f); });
    document.body.appendChild(stage);
  }
  function ready(){ return (document.fonts?document.fonts.ready:Promise.resolve()).then(function(){
    return new Promise(function(r){ requestAnimationFrame(function(){ requestAnimationFrame(r); }); }); }); }
  var FC=null, CACHE=[];
  async function png(node,i){ if(CACHE[i]) return CACHE[i];
    var prev=node.style.transform; node.style.transform="none";
    if(FC==null){ try{ FC=await htmlToImage.getFontEmbedCSS(node);}catch(e){FC="";} }
    var o={width:W,height:H,pixelRatio:2,cacheBust:true,fontEmbedCSS:FC,style:{transform:"none",margin:"0"}};
    await htmlToImage.toPng(node,o); var u=await htmlToImage.toPng(node,o);
    node.style.transform=prev; CACHE[i]=u; return u; }
  function status(m){ document.getElementById("rcm-status").textContent=m; }
  function busy(on){ document.querySelectorAll(".bar button").forEach(function(b){ b.disabled=on; }); }
  async function zip(){ busy(true); status("Rendering…"); await ready();
    try{ var z=new JSZip();
      for(var i=0;i<slides.length;i++){ status("Slide "+(i+1)+"/"+slides.length);
        z.file(SLUG+"-slide-"+String(i+1).padStart(2,"0")+".png",(await png(slides[i],i)).split(",")[1],{base64:true}); }
      saveAs(await z.generateAsync({type:"blob"}), SLUG+".zip"); status("Saved ZIP");
    }catch(e){ console.error(e); status("Export failed — use python -m rocket.render export"); } busy(false); }
  async function pdf(){ busy(true); status("Rendering…"); await ready();
    try{ var d=new window.jspdf.jsPDF({unit:"px",format:[W,H],compress:true});
      for(var i=0;i<slides.length;i++){ status("Slide "+(i+1)+"/"+slides.length);
        var u=await png(slides[i],i); if(i>0) d.addPage([W,H]); d.addImage(u,"PNG",0,0,W,H); }
      d.save(SLUG+".pdf"); status("Saved PDF");
    }catch(e){ console.error(e); status("Export failed — use python -m rocket.render export"); } busy(false); }
  var bar=document.createElement("div"); bar.className="bar";
  bar.innerHTML='<h1>'+SLUG+' · '+slides.length+' slides · 1080×1350</h1>'+
    '<span id="rcm-status">Ready</span><button id="rcm-zip">PNGs (ZIP)</button><button id="rcm-pdf" class="primary">Download PDF</button>';
  document.body.prepend(bar);
  document.getElementById("rcm-zip").onclick=zip; document.getElementById("rcm-pdf").onclick=pdf;
  buildPreview();
})();
</script>
"""

ARROW_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke-width="2.6" stroke-linecap="round" '
             'stroke-linejoin="round"><path d="M4 12 H20 M14 6 L20 12 L14 18"/></svg>')


class Deck:
    """Collects slides, then renders a single HTML file.

    palette = (cover & odd slides, even slides, CTA slide), each one of "dark" | "light" | "accent".
    Slide numbers and the NN / TT counter are filled in automatically.
    """

    def __init__(self, brand: Brand, palette=("dark", "light", "accent"), slug="carousel",
                 title: str | None = None, tag: str = ""):
        if len(palette) != 3 or any(p not in ROLES for p in palette):
            raise ValueError(f"palette must be three of {ROLES}, got {palette!r}")
        if palette[0] == palette[1]:
            raise ValueError("palette[0] and palette[1] must differ so slides alternate")
        self.brand, self.palette, self.slug = brand, tuple(palette), slug
        self.title = title or slug
        self.tag = tag
        self._items: list[tuple[str, dict]] = []

    # -- authoring -----------------------------------------------------------
    def cover(self, eyebrow: str, headline: str, sub: str, art: str = "", swipe: str = "swipe"):
        """headline: up to 3 short lines joined with <br>; finish with c.accent("...") for the serif flourish.
        art: an inline <svg> (see rocket.recolor) sized to fit the bottom of the cover."""
        self._items.append(("cover", dict(eyebrow=eyebrow, headline=headline, sub=sub, art=art, swipe=swipe)))
        return self

    def slide(self, eyebrow: str, headline: str, body: str = "", block: str = ""):
        self._items.append(("slide", dict(eyebrow=eyebrow, headline=headline, body=body, block=block)))
        return self

    def cta(self, headline: str, keyword: str, gets: list[str], fineprint: str | None = None):
        self._items.append(("cta", dict(headline=headline, keyword=keyword, gets=list(gets), fineprint=fineprint)))
        return self

    # -- rendering -----------------------------------------------------------
    def _bg(self, n: int, kind: str) -> str:
        if kind == "cta":
            return self.palette[2]
        return self.palette[0] if n % 2 == 1 else self.palette[1]

    def _top(self, n: int, total: int) -> str:
        return (f'  <div class="top"><span class="wm">{self.brand.name}<i>.</i></span>'
                f'<span class="pg"><b>{n:02d}</b> / {total:02d}</span></div>')

    def _foot(self, right: str) -> str:
        return f'  <div class="ft"><span>{self.brand.handle}</span><span>{right}</span></div>'

    def _section(self, n: int, total: int, kind: str, a: dict) -> str:
        bg = self._bg(n, kind)
        top = self._top(n, total)
        if kind == "cover":
            art = f'<div class="coverart">{a["art"]}</div>' if a["art"] else ""
            return (f'<section class="slide" data-bg="{bg}" data-role="cover">\n{top}\n'
                    f'  <div class="body-wrap">\n    <div class="eb">{a["eyebrow"]}</div>\n'
                    f'    <h1 class="hl">{a["headline"]}</h1>\n    <p class="cover-sub">{a["sub"]}</p>\n'
                    f'    <div class="swipe"><span class="dot"></span>{a["swipe"]}</div>\n'
                    f'    {art}\n  </div>\n{self._foot(self.tag)}\n</section>')
        if kind == "slide":
            return (f'<section class="slide" data-bg="{bg}">\n{top}\n'
                    f'  <div class="body-wrap">\n    <div class="eb">{a["eyebrow"]}</div>\n'
                    f'    <h2 class="hl">{a["headline"]}</h2>\n    {a["body"]}\n    {a["block"]}\n'
                    f'  </div>\n{self._foot(self.tag)}\n</section>')
        cta = self.brand.cta
        rows = "".join(f'<div class="g"><span class="gi">{i:02d}</span><span class="gt">{g}</span></div>'
                       for i, g in enumerate(a["gets"], 1))
        fine = a["fineprint"] if a["fineprint"] is not None else cta["fineprint"]
        return (f'<section class="slide" data-bg="{bg}" data-role="cta">\n{top}\n'
                f'  <div class="body-wrap">\n    <div class="eb">{cta["eyebrow"]}</div>\n'
                f'    <h2 class="hl">{a["headline"]}</h2>\n'
                f'    <div class="kwcard">\n      <div class="kw-top"><span>{cta["card_left"]}</span>'
                f'<span>{cta["card_right"]}</span></div>\n'
                f'      <div class="kw-main"><span class="kw-word">{a["keyword"]}</span>'
                f'<span class="kw-arrow">{ARROW_SVG}</span></div>\n    </div>\n'
                f'    <div class="gets"><div class="getcap">{cta["list_caption"]}</div>{rows}</div>\n'
                f'    <div class="fineprint">{fine}</div>\n'
                f'  </div>\n  <div class="ft"><span>{self.brand.handle}</span><span>{self.brand.site}</span></div>\n</section>')

    def css(self) -> str:
        b = self.brand
        at = b.accent_text_role()
        other = "dark" if at == "light" else "light"
        tokens = {
            "__D__": b.colors["dark"], "__L__": b.colors["light"], "__A__": b.colors["accent"],
            "__DRGB__": b.rgb("dark"), "__LRGB__": b.rgb("light"),
            "__AT__": at, "__AO__": other, "__ATRGB__": b.rgb(at),
            "__FD__": b.fonts["display"]["family"], "__FB__": b.fonts["body"]["family"],
            "__FM__": b.fonts["mono"]["family"], "__FS__": b.fonts["serif"]["family"],
        }
        out = CSS
        for k, v in tokens.items():
            out = out.replace(k, v)
        return out

    def html(self) -> str:
        if not self._items:
            raise ValueError("deck has no slides")
        total = len(self._items)
        sections = []
        prev_bg = None
        for n, (kind, a) in enumerate(self._items, 1):
            bg = self._bg(n, kind)
            if bg == prev_bg:
                warnings.warn(f"slide {n} has the same background ({bg}) as slide {n-1}; pick a different CTA colour")
            prev_bg = bg
            sections.append(self._section(n, total, kind, a))
        links = "\n".join(f'<link href="{u}" rel="stylesheet">' for u in self.brand.font_links())
        return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
                "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
                f"<title>{_html.escape(self.title)}</title>\n"
                "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
                "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
                f"{links}\n<style>{self.css()}</style>\n</head>\n"
                f"<body data-slug=\"{_html.escape(self.slug)}\">\n<div class=\"deck\">\n"
                + "\n\n".join(sections) + "\n</div>\n" + PREVIEW + "\n</body>\n</html>\n")

    def save(self, path: str | pathlib.Path) -> pathlib.Path:
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.html(), encoding="utf-8")
        return p
