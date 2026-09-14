$htmlFiles = Get-ChildItem -Path . -Filter *.html
foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    if ($content -notmatch "html2canvas") {
        $content = $content -replace "<body>", "<body>`n`n    <!-- ── Download Button (Top of Body) ── -->`n    <div style=`"position: fixed; top: 20px; right: 20px; z-index: 1000; display: flex; gap: 10px;`">`n        <button onclick=`"downloadAllSlides()`" style=`"padding: 15px 25px; background: #0f172a; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; font-family: 'Inter', sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: all 0.2s;`">`n            ↓ Download 4K Carousel`n        </button>`n    </div>"
        
        $script = @"
    <!-- ── Scripts (Bottom of Body) ── -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
        async function downloadAllSlides() {
            const btn = document.querySelector('button[onclick="downloadAllSlides()"]');
            const originalText = btn.innerText;
            btn.innerText = "Generating 4K Images...";
            btn.style.opacity = "0.7";
            btn.disabled = true;

            const slides = document.querySelectorAll('.slide');
            for (let i = 0; i < slides.length; i++) {
                const canvas = await html2canvas(slides[i], { scale: 4, useCORS: true, backgroundColor: null });
                const link = document.createElement('a');
                link.download = \`slide_\${i + 1}.png\`;
                link.href = canvas.toDataURL("image/png", 1.0);
                link.click();
                await new Promise(r => setTimeout(r, 800));
            }
            btn.innerText = "Downloaded Successfully!";
            setTimeout(() => { btn.innerText = originalText; btn.style.opacity = "1"; btn.disabled = false; }, 3000);
        }
    </script>
</body>
"@
        $content = $content -replace "</body>", $script
        Set-Content -Path $file.FullName -Value $content
        Write-Host "Updated: $($file.Name)"
    }
}
