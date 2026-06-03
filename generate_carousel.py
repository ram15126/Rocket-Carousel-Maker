#!/usr/bin/env python3
import os
import sys
import re

"""
===================================================================
ROCKET CAROUSEL MAKER — HTML Carousel Generator
Enforces Carousel 101 Structure & Taste / Impeccable Design Laws
===================================================================
"""

def parse_markdown(md_content):
    # Normalize line endings
    md_content = md_content.replace('\r\n', '\n')
    
    # 1. Parse Frontmatter (YAML-like)
    frontmatter = {}
    remaining_content = md_content
    
    if md_content.startswith('---'):
        parts = md_content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            remaining_content = parts[2]
            
            # Simple YAML parser
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    frontmatter[key.strip().lower()] = val.strip().strip('"').strip("'")

    # 2. Split Slides by H1 "Slide" headers or markdown separators "---"
    slide_raws = []
    # Match both standard Markdown divider '---' and slide headers like '# Slide 1'
    # We clean up double dividers to prevent empty slides
    raw_sections = re.split(r'\n---\n|# Slide\s+\d+[:\-\s]*', remaining_content)
    
    for section in raw_sections:
        section = section.strip()
        if section:
            slide_raws.append(section)

    slides = []
    for index, raw_slide in enumerate(slide_raws):
        lines = [l.strip() for l in raw_slide.split('\n') if l.strip()]
        if not lines:
            continue
            
        slide_type = "type-a" # Default layout type
        title_lines = []
        body_lines = []
        image_path = None
        pill_text = None
        
        # Look for custom slide parameters in the slide header block (first line)
        # Formats: "[type: hook]", "[badge: WARNING]", etc.
        first_line = lines[0]
        params_found = False
        
        if first_line.startswith('[') and first_line.endswith(']'):
            params_found = True
            param_content = first_line[1:-1]
            for param in param_content.split(','):
                if ':' in param:
                    k, v = param.split(':', 1)
                    k = k.strip().lower()
                    v = v.strip()
                    if k == 'type':
                        slide_type = v
                    elif k == 'badge' or k == 'pill':
                        pill_text = v
            lines = lines[1:] # Strip parameters line
            
        # Parse layout types based on standard keywords if not explicitly declared
        if not params_found:
            # Smart fallbacks for slides
            if index == 0:
                slide_type = "type-hook"
            elif index == len(slide_raws) - 1:
                slide_type = "type-cta"
            elif "metric" in raw_slide.lower() or "grid" in raw_slide.lower() or "data" in raw_slide.lower():
                # If there are bullet items that look like stats (e.g. "- 90% Increase")
                slide_type = "type-data"

        # Parse text content and image identifiers
        for line in lines:
            # Check for image triggers
            img_match = re.match(r'^\[image\]:\s*(.*)$|^!\[.*\]\((.*)\)$', line)
            if img_match:
                image_path = img_match.group(1) or img_match.group(2)
                image_path = image_path.strip().strip('"').strip("'")
                continue
                
            # Check for explicit pill badges
            pill_match = re.match(r'^\[badge\]:\s*(.*)$|^\[pill\]:\s*(.*)$', line)
            if pill_match:
                pill_text = pill_match.group(1) or pill_match.group(2)
                pill_text = pill_text.strip()
                continue
                
            # Standard lines
            if line.startswith('#'):
                # Secondary header line
                title_lines.append(line.lstrip('#').strip())
            else:
                body_lines.append(line)

        # Separate main header title from secondary descriptive lines
        title = ""
        body_html = ""
        bullets = []
        metrics = []

        # If we have title lines, compile them
        if title_lines:
            title = " ".join(title_lines)
            
        # Compile body text lines
        for b_line in body_lines:
            if b_line.startswith('-') or b_line.startswith('*'):
                bullet_item = b_line[1:].strip()
                # Check for metric definitions like "- 97% | Creators quit"
                if '|' in bullet_item:
                    m_val, m_lbl = bullet_item.split('|', 1)
                    metrics.append({
                        "value": m_val.strip(),
                        "label": m_lbl.strip()
                    })
                else:
                    bullets.append(bullet_item)
            else:
                if not title and len(title) == 0:
                    # Treat first text line as title if no explicit header existed
                    title = b_line
                else:
                    # Treat subsequent lines as description paragraph
                    if body_html:
                        body_html += "<br>"
                    body_html += b_line

        # Format accent highlights dynamically (converting **text** or *text* to span)
        def format_highlights(text):
            # Replace bold markdown with class span
            text = re.sub(r'\*\*(.*?)\*\*|\*(.*?)\*', r'<span class="highlight">\1\2</span>', text)
            # strictly BANNED emojis in content (design-taste-frontend rule)
            # Remove standard emojis dynamically if present
            text = re.sub(r'[\u2000-\u32FF\u2700-\u27BF\uE000-\uF8FF\uD83C-\uDBFF\uDC00-\uDFFF]', '', text)
            return text

        title = format_highlights(title)
        body_html = format_highlights(body_html)
        bullets = [format_highlights(b) for b in bullets]
        for m in metrics:
            m["value"] = format_highlights(m["value"])
            m["label"] = format_highlights(m["label"])

        slides.append({
            "type": slide_type,
            "title": title,
            "body": body_html,
            "bullets": bullets,
            "metrics": metrics,
            "image": image_path,
            "pill": pill_text
        })
        
    return frontmatter, slides

def generate_html(frontmatter, slides, output_path):
    # Extract frontmatter overrides or fallback to safe defaults
    brand_name = frontmatter.get("brand_name", "YOUR BRAND").upper()
    primary_color = frontmatter.get("primary_color", "#0F172A")
    accent_color = frontmatter.get("accent_color", "#0D9488")
    secondary_color = frontmatter.get("secondary_color", "#475569")
    slide_bg = frontmatter.get("slide_bg", "#FFFFFF")
    browser_bg = frontmatter.get("browser_bg", "#F1F5F9")
    
    # Generate inline CSS variable mapping to push tokens cleanly into carousel_core.css
    css_variables = f"""
    :root {{
      --brand-bg: {browser_bg};
      --brand-slide-bg: {slide_bg};
      --brand-primary: {primary_color};
      --brand-secondary: {secondary_color};
      --brand-accent: {accent_color};
      --brand-accent-glow: rgba({", ".join(str(int(accent_color.lstrip('#')[i:i+2], 16)) for i in (0, 2, 4))}, 0.08);
    }}
    """
    
    slides_html = ""
    slide_count = len(slides)
    
    for i, slide in enumerate(slides):
        index_str = f"{i+1:02d} / {slide_count:02d}"
        
        # Build progress dots dynamically
        dots_html = '<div class="pagination-progress">'
        for dot_idx in range(slide_count):
            active_class = " active" if dot_idx == i else ""
            dots_html += f'<div class="progress-dot{active_class}"></div>'
        dots_html += '</div>'
        
        # Header bar
        header_html = f"""
        <div class="slide-header">
            <div>
                <span class="brand-meta-label">{brand_name}</span>
                {dots_html}
            </div>
            <span class="slide-index-label">{index_str}</span>
        </div>
        """
        
        # Content elements
        pill_html = f'<div class="pill-badge">{slide["pill"]}</div>' if slide["pill"] else ''
        title_html = f'<h2>{slide["title"]}</h2>' if slide["title"] and slide["type"] != "type-hook" else ''
        
        if slide["type"] == "type-hook":
            title_html = f'<h1>{slide["title"]}</h1>'
            
        desc_html = f'<p>{slide["body"]}</p>' if slide["body"] else ''
        
        # Bullets formatting
        bullets_html = ""
        if slide["bullets"]:
            bullets_html = '<ul style="list-style-type: none; margin-top: 14px;">'
            for b in slide["bullets"]:
                bullets_html += f'<li style="position:relative; padding-left: 20px; margin-bottom: 8px; font-size:14px; color:var(--brand-secondary); font-weight:600;"><span style="position:absolute; left:0; color:var(--brand-accent);">•</span>{b}</li>'
            bullets_html += '</ul>'
            
        # Metrics formatting
        metrics_html = ""
        if slide["metrics"]:
            metrics_html = '<div class="metric-grid">'
            for m in slide["metrics"]:
                metrics_html += f"""
                <div class="metric-card">
                    <div class="metric-value">{m["value"]}</div>
                    <div class="metric-label">{m["label"]}</div>
                </div>
                """
            metrics_html += '</div>'
            
        # Background elements
        bg_elements_html = ""
        if slide["image"]:
            bg_elements_html = f"""
            <img class="slide-bg-overlay" src="{slide["image"]}" alt="Slide Background Image">
            <div class="slide-backdrop-scrim"></div>
            """

        # Custom swipe indicators
        swipe_indicator_html = ""
        if i < slide_count - 1:
            swipe_indicator_html = """
            <div class="swipe-indicator">
                <svg viewBox="0 0 24 24">
                    <path d="M5 12h14m0 0l-7-7m7 7l-7 7" />
                </svg>
            </div>
            """
            
        # Assembly based on layouts
        content_body = ""
        if slide["type"] == "type-hook":
            # Hook slide gets custom curved vector arrow
            content_body = f"""
            <svg class="decor-arrow-svg" viewBox="0 0 100 100">
                <path d="M 20 80 Q 50 20 90 30 M 75 15 L 90 30 L 75 45" />
            </svg>
            {pill_html}
            {title_html}
            {desc_html}
            {bullets_html}
            """
        elif slide["type"] == "type-cta":
            # CTA slide gets action button
            content_body = f"""
            {pill_html}
            {title_html}
            {desc_html}
            <a class="cta-button" href="#">{frontmatter.get("cta_text", "Follow for more")}</a>
            """
        else:
            # Normal type-a, type-b, type-data slides
            content_body = f"""
            {pill_html}
            {title_html}
            {desc_html}
            {bullets_html}
            {metrics_html}
            """

        # Add signature footer to every slide
        content_body += f"""
        <div class="slide-footer">
            <div class="bottom-left-url-pill">{brand_name.lower()}</div>
            <svg class="bottom-right-waves" viewBox="0 0 100 30">
                <path d="M 0 10 Q 12.5 0, 25 10 T 50 10 T 75 10 T 100 10 M 0 20 Q 12.5 10, 25 20 T 50 20 T 75 20 T 100 20" fill="none" stroke="rgba(255, 255, 255, 0.35)" stroke-width="2.5"/>
            </svg>
        </div>
        """

        # Outer slide container
        slides_html += f"""
        <div class="slide {slide["type"]}">
            {bg_elements_html}
            
            <div class="top-right-logo">
                <svg viewBox="0 0 100 100">
                    <path d="M 0 0 A 100 100 0 0 0 100 100 L 100 0 Z" fill="#86efac" opacity="0.8" />
                    <path d="M 30 0 A 70 70 0 0 0 100 70 L 100 0 Z" fill="#cbd5e1" opacity="0.9" />
                    <path d="M 60 0 A 40 40 0 0 0 100 40 L 100 0 Z" fill="#F59E0B" />
                </svg>
            </div>
            
            {header_html}
            <div class="content-wrapper">
                {content_body}
            </div>
            {swipe_indicator_html}
            
            <div class="bottom-gold-frame"></div>
        </div>
        """

    # Complete HTML output
    html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{frontmatter.get("brand_name", "Carousel")} - Instagram Feed</title>
    <link rel="stylesheet" href="assets/carousel_core.css">
    <style>
        {css_variables}
    </style>
</head>
<body>

    <div class="carousel-track">
        {slides_html}
    </div>

</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_carousel.py <input_script.md> <output_preview.html>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(input_path):
        print(f"Error: Script file '{input_path}' not found.")
        sys.exit(1)
        
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    print(f"Compiling '{input_path}'...")
    frontmatter, slides = parse_markdown(md_content)
    
    # Ensure assets directory exists for core stylesheet relative positioning
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) + "/assets", exist_ok=True)
    
    generate_html(frontmatter, slides, output_path)
    print(f"Success! Dynamic Branded Carousel HTML compiled at '{output_path}'.")

if __name__ == "__main__":
    main()
