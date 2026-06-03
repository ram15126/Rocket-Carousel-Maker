#!/usr/bin/env python3
import os
import sys

"""
===================================================================
DIGI MABBLE HEADLESS CAROUSEL SLIDE EXPORTER
Uses Playwright to screen-capture razor-sharp 1080x1350px PNGs
===================================================================
"""

def check_dependencies():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("\n[DEPENDENCY ALERT] Playwright is not installed.")
        print("To install Playwright and its browser binaries, please run:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print("\nExiting. Please run the install command and try again.")
        sys.exit(1)

def export_slides(html_path, output_dir):
    from playwright.sync_api import sync_playwright
    
    abs_html_path = os.path.abspath(html_path)
    if not os.path.exists(abs_html_path):
        print(f"Error: HTML file not found at '{abs_html_path}'")
        sys.exit(1)
        
    os.makedirs(output_dir, exist_ok=True)
    
    file_url = f"file:///{abs_html_path.replace(os.sep, '/')}"
    print(f"Launching headless browser to load: {file_url}")
    
    with sync_playwright() as p:
        # Launch headless chromium
        browser = p.chromium.launch(headless=True)
        
        # KEY QUALITY TRICK: Set device_scale_factor=2 (Retina density)
        # This renders our compact 540x675px slide bounding boxes at perfect 1080x1350px resolution!
        context = browser.new_context(
            viewport={"width": 1200, "height": 1600},
            device_scale_factor=2
        )
        
        page = context.new_page()
        
        # Load the HTML feed
        page.goto(file_url, wait_until="networkidle")
        
        # Locate all slide containers
        slides = page.query_selector_all(".slide")
        if not slides:
            print("Error: No slide elements ('.slide') found in the HTML file.")
            browser.close()
            sys.exit(1)
            
        print(f"Found {len(slides)} slides. Exporting sequential frames...")
        
        for i, slide in enumerate(slides):
            out_filename = f"{i+1:02d}.png"
            out_path = os.path.join(output_dir, out_filename)
            
            # Target screenshot exactly at the slide element's bounding box
            slide.screenshot(
                path=out_path, 
                type="png", 
                animations="disabled" # Strictly disables any dynamic hover shifts
            )
            
            # Calculate final dimensions of the screenshot
            # Since slide is 540x675 and scale factor is 2, output is exactly 1080x1350
            print(f"  [+] Captured Slide {i+1:02d} -> Saved to '{out_path}' (Retina 1080x1350)")
            
        browser.close()
        print(f"\nSuccess! All {len(slides)} slides exported to '{output_dir}/'. Ready to post!")

def main():
    check_dependencies()
    
    if len(sys.argv) < 3:
        print("Usage: python export_slides.py <carousel.html> <output_directory>")
        sys.exit(1)
        
    html_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    export_slides(html_path, output_dir)

if __name__ == "__main__":
    main()
