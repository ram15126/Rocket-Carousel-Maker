---
name: carousel-maker
description: "This skill should be used when creating Instagram carousels from video content, transcripts, topics, or ideas. Two generation modes: Mode A (AI-generated slides, styles 1-6) and Mode B (screenshot-based slides, style 7). Includes automatic watermark removal. Triggers: 'make a carousel', 'create carousel', 'instagram carousel', 'carousel from this video', 'turn this into a carousel', any video link with carousel intent."
---

**Tool Stack:** Follow `~/.claude/skills/_shared/tool-stack.md` for ALL tool choices.
**Quality Gates:** Follow `~/.claude/skills/_shared/quality-gates.md` for ALL quality checks.

# Instagram Carousel Maker

## Interactive Decision Points

### 1. Generation Mode

Ask the user:
- **Question:** "How should we create the carousel slides?"
- **Options:**
  - "Screenshot-Based (Recommended)" — Real frames from source video, preserves exact faces/details
  - "AI-Generated" — Gemini Pro generates stylized slides from scratch
  - "Watermark Removal Only" — Clean up existing Gemini-generated images

### 2. Carousel Format

Ask the user:
- **Question:** "What format fits your content?"
- **Options:**
  - "The List" — "5 Ways to..." "7 Mistakes..." (educational, high saves)
  - "Framework Reveal" — "The 3-Step System for..." (authority, high follows)
  - "Myth-Bust" — "You've been told X. Here's the truth." (contrarian, high comments)
  - "Story Arc" — "This one decision changed everything." (narrative, high engagement)

### 3. Visual Style

Ask the user:
- **Question:** "What visual style do you want?"
- **Options:**
  - "Screenshot + Annotation (Recommended)" — Real frames with text overlays and highlights (Mode B)
  - "Keynote (Luis Carrillo Original)" — Black background, Inter font, Apple colors, massive typography, one idea per slide. Jobs-style story arc. Pure #000000, white text, accent colors (blue #2997ff, green #30d158, purple #bf5af2, red #ff453a). Each slide = downloadable 4:5 image.
  - "Cards Against Humanity" — Stark white, black border, bold Helvetica
  - "Handwritten Whiteboard" — Hand-drawn markers, slightly imperfect
  - "Custom / Brand Match" — Provide a reference image to clone the vibe

## Mode Decision Logic

| Signal | Mode |
|--------|------|
| Real person on camera | **Mode B** (screenshot) |
| Product demos / physical items | **Mode B** (screenshot) |
| Concept / educational / no face | Mode A (AI-generated) |
| User says "use frames" or "screenshots" | **Mode B** (screenshot) |

## The 5-Step Workflow

| Step | What | Details |
|------|------|---------|
| 1 | Content Ingestion | Video link, transcript, or topic + character ref + aesthetic ref |
| 2 | Format Selection | List / Myth-Bust / Before-After / Story / Framework / Hot Take |
| 3 | Style & CTA | 7 visual styles + 5 CTA options |
| 4 | Script + Visual Plan | Slide-by-slide text + visual descriptions |
| 5 | Generation + Cleanup | Generate → watermark removal → rename → verify |

## Readability Rules (ENFORCE ALWAYS)

1. Max 15 words per slide (8-12 ideal)
2. One idea per slide — if it needs a comma, split it
3. No paragraphs — bullet points or single lines only
4. High contrast — black on white or white on black
5. Readable on mobile without zooming
6. ALWAYS center-aligned, both axes
7. Minimum 10% margin on all sides

## Tools

| Tool | Purpose |
|------|---------|
| Gemini Pro | Generate & edit slides |
| yt-dlp | Download source videos |
| ffmpeg | Extract frames (Mode B) |
| Pillow (PIL) | Canvas layout & text overlays (Mode B) |
| Google Drive MCP | Access Drive folders |


## Trust Enforcement (Inherited — Global Law, Mar 16, 2026)

| Pillar | Rule |
|--------|------|
| **Verify Before Claim** | Tool call before stating facts. Never answer from memory alone. |
| **Data Accuracy** | All handles, URLs, IDs from source files ONLY. Never fabricate. |
| **Complete The Ask** | Do EVERYTHING the user asked. All items. Not just the first one. |
| **Show Your Work** | Open Kitchen — show every step as it happens. No black boxes. |
| **Source Everything** | Cite where information comes from. |
| **Internet-First** | Fetch official docs before advising on any tool/API. |

Enforcement: `trust-guardian.js` hook + `quality-gates.md` Trust Gate. Full: `~/.claude/skills/trust/SKILL.md`

## Gate Protocol
- **Pre-flight:** Verify image generation tool is available (Glif, DALL-E, etc.). Confirm style requirements and dimensions. Check for brand guidelines if client work.
- **Mid-flight:** Validate prompt quality before generation. Review output for quality, accuracy, and brand alignment. Iterate if first generation misses the brief.
- **Post-flight:** Verify output image exists at expected path. Check resolution and format. Confirm no artifacts, text errors, or brand violations.

---

## AI Agent Readiness Layer

### I/O Schema

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `input_source` | `string` — URL \| filepath \| raw_text | YES | `"https://youtube.com/..."` |
| `mode` | `enum` — A \| B \| watermark_only | NO (auto-detected) | `"B"` |
| `format` | `enum` — list \| framework \| myth-bust \| story | NO (prompted) | `"list"` |
| `style` | `enum` — keynote \| cards \| whiteboard \| screenshot \| custom | NO (prompted) | `"keynote"` |
| `slide_count` | `int` 8–10 | NO (default: 10) | `9` |
| `client_name` | `string` | NO | `"Ryan Magin"` |
| `output_dir` | `filepath` | NO (default: `~/Downloads/[name]/clean/`) | `"~/Downloads/carousel-ep42/clean/"` |
| `output_files` | `array[filepath]` — PNG, 4:5, ≥1080px wide | YES (post-flight) | `["01.png", "02.png", ...]` |
| `slide_count_verified` | `boolean` | YES (post-flight) | `true` |
| `watermarks_removed` | `boolean` | YES (Mode A post-flight) | `true` |

### Error Handling Table

| Error | Trigger | Agent Action |
|-------|---------|--------------|
| No input provided | `input_source` empty | BLOCK: "Provide a video link, transcript, or topic to continue." |
| yt-dlp download fails | Non-zero exit code | Retry once. If fail: INFORM "Download failed — paste transcript manually." |
| Gemini API error | HTTP 4xx/5xx from Gemini | Retry once with simplified prompt. If fail: BLOCK + log error. |
| ffmpeg frame extraction fails | No frames in output dir | INFORM: "Frame extraction failed. Check video file path and ffmpeg install." |
| design-system.md unreachable | File not found | BLOCK for Keynote style: "Cannot load design system. Check /keynote-generator/references/design-system.md" |
| Slide word count > 15 | Word count check on script | BLOCK generation: rewrite offending slide before continuing |
| Watermark not removed | Watermark still visible post-script | Re-run removal with higher threshold. If 2x fail: INFORM user to manually crop |
| Output dir write error | Permission denied | INFORM: "Cannot write to [dir]. Check permissions or specify alternate path." |
| Slide count mismatch | `len(output_files) != slide_count` | Flag missing slides, retry generation for missing indices only |

### Handoff Labels

| Step | Handoff Type | Condition |
|------|-------------|-----------|
| Mode selection (ambiguous input) | APPROVAL-REQUIRED | Cannot auto-detect mode — present options, await user choice |
| Style selection | APPROVAL-REQUIRED | No style specified and no client brand guide available |
| Slide script review | INFORM | Script generated — show to user before image generation begins |
| Generation complete | INFORM | All slides generated and renamed — surface output path |
| Error recovery (retries exhausted) | APPROVAL-REQUIRED | Cannot auto-resolve — surface error + options to user |
| Clean final delivery | AUTONOMOUS | All gates pass, files verified, path confirmed — no user action needed |

### Exact Tool Calls

```bash
# Download video
/opt/homebrew/bin/yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4" \
  --cookies-from-browser chrome \
  -o "~/Downloads/[carousel-name]/source.%(ext)s" "[VIDEO_URL]"

# Extract frames (Mode B) — 1 frame per second
ffmpeg -i ~/Downloads/[carousel-name]/source.mp4 \
  -vf "fps=1" ~/Downloads/[carousel-name]/frames/frame_%04d.png

# Transcribe audio
groq-transcribe ~/Downloads/[carousel-name]/source.mp4

# Run watermark removal
/opt/homebrew/bin/python3.13 \
  ~/.claude/plugins/cache/every-marketplace/compound-engineering/2.28.0/skills/gemini-imagegen/scripts/remove_watermark.py \
  --input ~/Downloads/[carousel-name]/raw/ \
  --output ~/Downloads/[carousel-name]/clean/

# Rename slides sequentially
/opt/homebrew/bin/python3.13 -c "
import os, glob
files = sorted(glob.glob('~/Downloads/[carousel-name]/clean/*.png'))
for i, f in enumerate(files, 1):
    os.rename(f, f'~/Downloads/[carousel-name]/clean/{i:02d}.png')
"
```


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)


## Change Log
- [2026-03-09]: Context Diet — split 294 lines into routing card (171 lines) + references/full-details.md (143 lines). Zero content deleted. By skill-diet.py.
- [2026-03-02]: AI Agent Readiness upgrade — scored 4/10, upgraded to 10/10. By Agent Luis.
- [2026-03-02]: War Room Tier 2 — content quality upgrade (gate→image).
- [2026-03-02]: War Room Tier 1 audit — skill structure verified and standardized.
