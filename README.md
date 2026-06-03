# 🎠 Digi Mabble — HTML Carousel Maker

A lightweight tool that takes a simple text template (Markdown) and generates a **beautiful, brand-ready HTML carousel** — ready to open in your browser and screenshot for Instagram or LinkedIn.

---

## ✨ How It Works

1. **Write** your carousel content in a Markdown file (like `sample_carousel.md`)
2. **Run** the generator script
3. **Open** the output HTML in your browser
4. **Screenshot** each slide manually (or auto-export using the Playwright script)

That's it. No design software needed.

---

## 🚀 Quick Start

### 1. Install Python (if not already installed)
Download from [python.org](https://python.org). Make sure to check **"Add to PATH"** during install.

### 2. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/carousel-maker.git
cd carousel-maker
```

### 3. Generate your carousel
```bash
python generate_carousel.py sample_carousel.md my_carousel.html
```

### 4. View it
Open `my_carousel.html` in any browser (double-click the file).  
Each slide is sized at **540×675px** — perfect for Instagram 4:5 format.  
Screenshot each slide individually to get your images!

---

## 📝 Writing Your Carousel Template

The template is a simple Markdown `.md` file. Here's the structure:

### Frontmatter (Top of file — brand settings)
```markdown
---
brand_name: "YOUR BRAND"
primary_color: "#0F172A"
accent_color: "#0D9488"
secondary_color: "#475569"
slide_bg: "#FFFFFF"
browser_bg: "#F1F5F9"
cta_text: "Follow for more"
---
```

### Slides (Separated by `---`)
```markdown
[type: type-hook, pill: YOUR BADGE]
# Your **main hook** headline goes here.
A short supporting sentence that explains the hook.

---

[type: type-a, pill: THE POINT]
# The **core insight** of this slide.
More detail here to support the headline.

---

[type: type-data, pill: THE PROOF]
# The **numbers** don't lie.
- 97% | Stat one label
- 84% | Stat two label

---

[type: type-cta, pill: JOIN US]
# Ready to **take action?**
Save this and implement it today.
```

### Slide Types
| Type | Use For |
|---|---|
| `type-hook` | First slide — grabs attention |
| `type-a` | Regular content slide |
| `type-b` | Content slide with a background image |
| `type-data` | Stats / metrics grid |
| `type-cta` | Last slide — call to action |

### Adding a Background Image
```markdown
[type: type-b, pill: VISUAL PROOF]
# Your **headline** here.
Supporting text.
[image]: assets/your_image.png
```
Drop your image into the `assets/` folder and reference it like above.

---

## ⚡ Auto-Screenshot (Optional)

If you want to auto-capture all slides as PNG images instead of manual screenshots:

### Install Playwright
```bash
pip install playwright
playwright install chromium
```

### Run the exporter
```bash
python export_slides.py my_carousel.html output_slides/
```

This saves each slide as a numbered PNG (e.g., `01.png`, `02.png`) in the `output_slides/` folder at **1080×1350px retina quality**.

---

## 📁 File Structure

```
carousel-maker/
├── generate_carousel.py      # Main engine — converts .md to .html
├── export_slides.py          # Optional: auto-screenshot each slide
├── sample_carousel.md        # Example template to start from
├── carousel_sop.md           # Design rules & standard operating procedure
├── assets/
│   ├── carousel_core.css     # All the carousel styling
│   └── *.png                 # Background images you can use
└── README.md
```

---

## 🎨 Design SOPs

This tool enforces a strict set of design rules so every carousel looks premium:
- See [`carousel_sop.md`](carousel_sop.md) for the full Standard Operating Procedure
- See [`taste skill.md`](taste%20skill.md) for advanced design taste guidelines

Key rules:
- ✅ Clean, minimal layouts with one strong accent color
- ✅ No emojis in slide content
- ✅ Proper type hierarchy (one H1 per hook slide)
- ✅ Consistent padding and spacing
- ✅ Bold keywords using `**bold**` markdown syntax

---

## 📄 License

MIT License — free to use, modify, and share.
