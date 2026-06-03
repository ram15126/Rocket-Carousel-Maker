# Carousel Creation SOP

1. **Direct HTML Generation (No Intermediaries)**: Skip python generators, scripts, and intermediary markdown files. Write the carousel directly as a single, fully self-contained HTML file with embedded CSS.
2. **Template-Driven Design (Ground Truth)**: The visual template images located in the `templates/` folder (e.g., `carousel-template-1`) are the absolute Ground Truth for design. You must replicate their styling (background patterns, padding, fonts, card layouts, and alternating alignments) exactly using pure CSS/HTML.
3. **Screenshot-Ready Structure**: Output a **vertical, scrollable feed** where each slide is its own container. 
    - Enforce a strict **4:5 aspect ratio** by hardcoding slide dimensions to exactly `1080px` wide and `1350px` tall.
    - Set exactly an `80px` vertical gap between slides. 
    - Disable hover effects, transitions, and animations so the slides remain perfectly still for the user to screenshot easily.
4. **Self-Contained Assets**: Do not link to external local stylesheets. Use inline SVGs for background patterns (like chevrons or dots), import fonts directly from Google Fonts (e.g., Montserrat, Plus Jakarta Sans), and embed all CSS in a `<style>` block at the top of the file.
5. **Brand Adaptation**: When decoding a visual template, adapt the placeholder texts (e.g., "@reallygreatsite", "01") to use the current client's brand metadata (e.g., "DIGI MABBLE", "@digimabble"), while strictly maintaining the positional layout of the original template.
6. **Carousel Content Framework**: Always follow the core narrative arc: Hook -> Rehook -> Mirror -> Reveal -> CTA. Keep body text concise, and aggressively use `font-weight: 800/900` or contrasting accent colors to highlight keywords.
7. **UI/UX Pro Max**: Ensure generous padding, proper flexbox alignment, and zero text overlapping. Use contrasting cards (e.g., stark black cards against a vibrant background) to create an attention-seeking visual hierarchy.
8. **Token Conservation**: Always be token conservative and write clean, repetitive HTML structures efficiently.
9. **SOP Adherence**: Always keep this SOP in mind and follow these steps meticulously for every future carousel creation task to avoid repeating revisions.
