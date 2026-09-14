# Carousel Creation SOP

1. **Direct HTML Generation (No Intermediaries)**: Skip python generators, scripts, and intermediary markdown files. Write the carousel directly as a single, fully self-contained HTML file with embedded CSS.
2. **Template-Driven Design (Ground Truth)**: The visual template images located in the `templates/` folder (e.g., `carousel-template-1`) are the absolute Ground Truth for design. You must replicate their styling (background patterns, padding, fonts, card layouts, and alternating alignments) exactly using pure CSS/HTML.
3. **Screenshot-Ready Structure**: Output a **vertical, scrollable feed** where each slide is its own container. 
    - Enforce a strict **4:5 aspect ratio** by hardcoding slide dimensions to exactly `1080px` wide and `1350px` tall.
    - Set exactly an `80px` vertical gap between slides. 
    - Disable hover effects, transitions, and animations so the slides remain perfectly still for the user to screenshot easily.
4. **Self-Contained Assets**: Do not link to external local stylesheets. Use inline SVGs for background patterns (like chevrons or dots), import fonts directly from Google Fonts (e.g., Montserrat, Plus Jakarta Sans), and embed all CSS in a `<style>` block at the top of the file.
5. **Brand Adaptation**: When decoding a visual template, adapt the placeholder texts (e.g., "@reallygreatsite", "01") to use the current client's brand metadata (e.g., their brand name and handle), while strictly maintaining the positional layout of the original template. Never add any watermark or brand name unless explicitly provided by the user.
6. **Carousel Content Framework**: Always follow the core narrative arc: Hook -> Rehook -> Mirror -> Reveal -> CTA. Keep body text concise, and aggressively use `font-weight: 800/900` or contrasting accent colors to highlight keywords.
7. **UI/UX Pro Max**: Ensure generous padding, proper flexbox alignment, and zero text overlapping. Use contrasting cards (e.g., stark black cards against a vibrant background) to create an attention-seeking visual hierarchy.
8. **Token Conservation**: Always be token conservative and write clean, repetitive HTML structures efficiently.
9. **4K High-Quality Export (ZIP)**: Every carousel MUST include a "Download 4K Carousel" button, `html2canvas`, and `jszip` scripts. This replaces manual screenshotting and downloads all slides cleanly in a single folder.
    - Add the download button right after the opening `<body>` tag.
    - Add the `jszip` and `html2canvas` CDNs and export script right before the closing `</body>` tag.
    - Ensure `scale: 4` is used for 4K quality output (4320x5400).
    - Code snippet to include:
    ```html
    <!-- ── Download Button (Top of Body) ── -->
    <div style="position: fixed; top: 20px; right: 20px; z-index: 1000; display: flex; gap: 10px;">
        <button onclick="downloadAllSlides()" style="padding: 15px 25px; background: #0f172a; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; font-family: 'Inter', sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: all 0.2s;">
            ↓ Download 4K Carousel (ZIP)
        </button>
    </div>

    <!-- ── Scripts (Bottom of Body) ── -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
        async function downloadAllSlides() {
            const btn = document.querySelector('button[onclick="downloadAllSlides()"]');
            const originalText = btn.innerText;
            btn.innerText = "Generating ZIP...";
            btn.style.opacity = "0.7";
            btn.disabled = true;

            let fileName = window.location.pathname.split('/').pop();
            let baseName = fileName ? decodeURIComponent(fileName).replace('.html', '') : 'carousel';

            try {
                const zip = new JSZip();
                const folder = zip.folder(`${baseName}_slides`);
                const slides = document.querySelectorAll('.slide');
                
                for (let i = 0; i < slides.length; i++) {
                    btn.innerText = `Processing ${i + 1}/${slides.length}...`;
                    const canvas = await html2canvas(slides[i], { scale: 4, useCORS: true, backgroundColor: null });
                    const dataUrl = canvas.toDataURL("image/png", 1.0);
                    const base64Data = dataUrl.split(',')[1];
                    folder.file(`${baseName}_slide_${i + 1}.png`, base64Data, {base64: true});
                }
                
                btn.innerText = "Zipping...";
                const content = await zip.generateAsync({type: "blob"});
                
                const link = document.createElement('a');
                link.href = URL.createObjectURL(content);
                link.download = `${baseName}.zip`;
                link.click();
                
                URL.revokeObjectURL(link.href);
                btn.innerText = "Downloaded Successfully!";
            } catch (err) {
                console.error("Error generating zip:", err);
                btn.innerText = "Error generating ZIP";
            }
            
            setTimeout(() => { btn.innerText = originalText; btn.style.opacity = "1"; btn.disabled = false; }, 3000);
        }
    </script>
    ```
10. **SOP Adherence**: Always keep this SOP in mind and follow these steps meticulously for every future carousel creation task to avoid repeating revisions.
