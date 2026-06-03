# Rocket Carousel Maker

A lightweight tool that takes visual template references and generates **beautiful, brand-ready HTML carousels** — ready to open in your browser and screenshot for Instagram or LinkedIn.

---

## How It Works

1. **Pick** a template from the `templates/` folder for visual reference
2. **Get** your carousel content written by AI based on your topic
3. **Open** the output HTML in your browser
4. **Screenshot** each slide — that's it!

No Python. No design software. No dependencies.

---

## Quick Start

### 1. Pick a Template
Browse the `templates/` folder and pick the design you want to use as visual reference. Each folder contains numbered slide PNGs showing the design style.

### 2. Request a Carousel
Provide your topic and your chosen template to the AI. It will generate a complete, self-contained HTML file styled to exactly match the template.

### 3. Open and Screenshot
Open the generated HTML in any browser. Each slide is a fixed `1080x1350px` block, stacked vertically with 80px gaps — perfectly sized for Instagram 4:5 format. Screenshot each slide individually to get your images!

---

## File Structure

```
carousel-maker/
├── templates/
│   ├── carousel-template-1/     # Yellow & Black bold style
│   ├── carousel-template-2/     # Alt style
│   ├── carousel-template-3/     # Alt style
│   ├── carousel-template-4/     # Alt style
│   └── carousel-template-5/     # Alt style
├── carousel_sop.md              # Design rules & SOP protocol
└── README.md
```

---

## Design SOPs

All carousels are generated following a strict set of rules. See [`carousel_sop.md`](carousel_sop.md) for the full Standard Operating Procedure.

Key rules:
- Every carousel is a **single, fully self-contained HTML file** (no external dependencies)
- Fixed **1080x1350px** slide dimensions (Instagram 4:5 ratio)
- Templates in the `templates/` folder are the **absolute Ground Truth** for design
- All text is brand-adapted — no placeholder handles or watermarks
- Clean type hierarchy, generous padding, zero text overlap

---

## License

MIT License — free to use, modify, and share.
