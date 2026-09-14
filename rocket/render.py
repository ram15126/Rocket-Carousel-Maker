"""Verify and export carousels with a headless browser.

    python -m rocket.render check  out/*.html            # overflow + font check, exit 1 on problems
    python -m rocket.render check  out/*.html --sheet    # ...and write a contact sheet
    python -m rocket.render export out/*.html --out exports --scale 2

export writes, per deck:  <out>/<deck>/<deck>-slide-NN.png, <out>/<deck>.pdf, <out>/<deck>-png.zip
Slides are captured at 1080x1350 x scale (scale 2 -> 2160x2700 PNGs, PDF pages stay 1080x1350 pt).
"""
from __future__ import annotations

import argparse
import glob
import pathlib
import sys
import zipfile

FONT_JS = """() => {
  const first = sel => { const el = document.querySelector(sel); if (!el) return null;
    return getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim(); };
  const used = [...new Set(['.hl', '.bd', '.eb', '.flourish', '.pg'].map(first).filter(Boolean))];
  const loaded = new Set([...document.fonts].filter(f => f.status === 'loaded')
                                            .map(f => f.family.replace(/["']/g, '')));
  return { used, missing: used.filter(f => !loaded.has(f)) };
}"""


def _expand(patterns: list[str]) -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for p in patterns:
        hits = sorted(glob.glob(p))
        out.extend(pathlib.Path(h) for h in (hits or [p]))
    return out


def run(mode: str, files: list[pathlib.Path], out_dir: pathlib.Path, scale: int = 2, sheet: bool = False) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright is not installed:  pip install -r requirements.txt && python -m playwright install chromium")
        return 2
    issues: list[str] = []
    rows: list[list[pathlib.Path]] = []
    capture = mode == "export" or sheet
    if mode == "check":
        scale = 1
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for f in files:
            if not f.exists():
                issues.append(f"{f}: file not found")
                continue
            # JavaScript off: the browser preview script would otherwise shrink slides into a grid
            ctx = browser.new_context(java_script_enabled=False, viewport={"width": 1080, "height": 1350},
                                      device_scale_factor=scale)
            page = ctx.new_page()
            page.set_default_timeout(90000)
            page.goto(f.resolve().as_uri(), wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("load", timeout=45000)
            except Exception:
                print(f"  {f.name}: load event slow, continuing")
            page.wait_for_timeout(2500)

            fonts = page.evaluate(FONT_JS)
            if fonts["missing"]:
                issues.append(f"{f.name}: fonts not loaded {fonts['missing']} (offline? blocked CDN?)")
            slides = page.query_selector_all(".slide")
            if not slides:
                issues.append(f"{f.name}: no .slide elements")
            stem = f.stem
            dest = (out_dir / stem) if mode == "export" else (out_dir / "_check" / stem)
            pngs: list[pathlib.Path] = []
            for i, s in enumerate(slides, 1):
                over = page.evaluate("(el) => ({y: el.scrollHeight - el.clientHeight, x: el.scrollWidth - el.clientWidth})", s)
                if over["y"] > 0 or over["x"] > 0:
                    issues.append(f"{f.name}: slide {i} overflows by {over['y']}px vertically, {over['x']}px horizontally")
                if capture:
                    dest.mkdir(parents=True, exist_ok=True)
                    page.evaluate("(el) => el.scrollIntoView({block: 'center'})", s)
                    page.wait_for_timeout(100)
                    path = dest / f"{stem}-slide-{i:02d}.png"
                    s.screenshot(path=str(path))
                    pngs.append(path)
            ctx.close()

            if mode == "export" and pngs:
                import img2pdf
                layout = img2pdf.get_fixed_dpi_layout_fun((72 * scale, 72 * scale))
                (out_dir / f"{stem}.pdf").write_bytes(img2pdf.convert([str(x) for x in pngs], layout_fun=layout))
                with zipfile.ZipFile(out_dir / f"{stem}-png.zip", "w", zipfile.ZIP_DEFLATED) as z:
                    for x in pngs:
                        z.write(x, arcname=x.name)
            if pngs:
                rows.append(pngs)
            print(f"{f.name}: {len(slides)} slides")
        browser.close()

    if rows:
        from PIL import Image
        tw, th, pad = 216, 270, 6
        cols = max(len(r) for r in rows)
        sheet_img = Image.new("RGB", (cols * tw + (cols + 1) * pad, len(rows) * th + (len(rows) + 1) * pad), (17, 17, 17))
        for r, row in enumerate(rows):
            for c, path in enumerate(row):
                im = Image.open(path).convert("RGB").resize((tw, th))
                sheet_img.paste(im, (pad + c * (tw + pad), pad + r * (th + pad)))
        out_dir.mkdir(parents=True, exist_ok=True)
        sheet_path = out_dir / "contact-sheet.png"
        sheet_img.save(sheet_path)
        print(f"contact sheet: {sheet_path}")

    if issues:
        print("\nPROBLEMS:")
        for i in issues:
            print("  -", i)
        return 1
    print("\nOK: no overflow, fonts loaded")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["check", "export"])
    ap.add_argument("files", nargs="+", help="deck HTML files (globs ok)")
    ap.add_argument("--out", default="exports", help="output folder (default: exports)")
    ap.add_argument("--scale", type=int, default=2, help="export pixel ratio (default 2 -> 2160x2700)")
    ap.add_argument("--sheet", action="store_true", help="in check mode, also capture a contact sheet")
    args = ap.parse_args(argv)
    return run(args.mode, _expand(args.files), pathlib.Path(args.out), args.scale, args.sheet)


if __name__ == "__main__":
    raise SystemExit(main())
