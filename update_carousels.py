import os

font_link = '<link href="https://api.fontshare.com/v2/css?f[]=clash-display@600&f[]=satoshi@400,500,700&display=swap" rel="stylesheet">'
inter_link_1 = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">'
inter_link_2 = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap" rel="stylesheet">'
inter_link_3 = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;900&display=swap" rel="stylesheet">'

def update_file(filename, modifications):
    if not os.path.exists(filename): return
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in modifications:
        content = content.replace(old, new)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

mod1 = [
    ("color: #ffffff;", "color: var(--brand-bg);"),
    ("linear-gradient(135deg, #ffffff 0%, var(--brand-bg) 100%)", "var(--brand-bg)"),
    ("font-family: 'Space Mono', monospace;", "font-family: 'Satoshi', sans-serif;"),
    ("--brand-text: #000000;", "--brand-text: #1b3022;"),
    ("rgba(255, 255, 255, 0.3)", "rgba(244, 239, 230, 0.3)")
]

mod2 = [
    (inter_link_1, font_link),
    ("font-family: 'Inter', sans-serif;", "font-family: 'Satoshi', sans-serif;"),
    (".s1-title {\n      font-size: 140px;", ".s1-title {\n      font-family: 'Clash Display', sans-serif;\n      font-size: 140px;"),
    (".s2-title {\n      font-size: 140px;", ".s2-title {\n      font-family: 'Clash Display', sans-serif;\n      font-size: 140px;"),
    (".s5-title {\n      font-size: 130px;", ".s5-title {\n      font-family: 'Clash Display', sans-serif;\n      font-size: 130px;"),
    ("--orange: #EE9C58;", "--orange: #ff6542;"),
    ("--bg-orange: #D56C23;", "--bg-orange: #ff6542;"),
    ("background-color: white;", "background-color: #f4efe6;"),
    ("background: white;", "background: #f4efe6;"),
    ("color: black;", "color: #1b3022;"),
    ("background: black;", "background: #1b3022;"),
    ("color: white;", "color: #f4efe6;"),
    ("background-color: black;", "background-color: #1b3022;"),
    ('stroke="black"', 'stroke="#1b3022"'),
    ('stroke="white"', 'stroke="#f4efe6"'),
    ('fill="rgba(255,255,255,0.1)"', 'fill="rgba(27,48,34,0.1)"')
]

mod3 = [
    (inter_link_2, font_link),
    ("font-family: 'Inter', sans-serif;", "font-family: 'Satoshi', sans-serif;"),
    (".s1-title {\n      position: absolute;", ".s1-title {\n      font-family: 'Clash Display', sans-serif;\n      position: absolute;"),
    (".slide-title {\n      position: absolute;", ".slide-title {\n      font-family: 'Clash Display', sans-serif;\n      position: absolute;"),
    ("--purple: #8B5CF6;", "--purple: #ff6542;"),
    ("--bg-dark: #121212;", "--bg-dark: #f4efe6;"),
    ("--text-white: #FFFFFF;", "--text-white: #1b3022;"),
    ('fill="white"', 'fill="#1b3022"'),
    ('stroke="white"', 'stroke="#1b3022"'),
    ("rgba(255, 255, 255, 0.85)", "rgba(27, 48, 34, 0.85)"),
    ("rgba(255, 255, 255, 0.3)", "rgba(27, 48, 34, 0.3)"),
    ("rgba(255, 255, 255, 0.15)", "rgba(27, 48, 34, 0.15)"),
    ("color: #000;", "color: #f4efe6;")
]

mod4 = [
    (inter_link_3, font_link),
    ("font-family: 'Inter', sans-serif;", "font-family: 'Satoshi', sans-serif;"),
    (".main-title {\n      position: absolute;", ".main-title {\n      font-family: 'Clash Display', sans-serif;\n      position: absolute;"),
    ("--brand-text: #000000;", "--brand-text: #1b3022;")
]

update_file("axon_carousel_1.html", mod1)
update_file("axon_carousel_2.html", mod2)
update_file("axon_carousel_3.html", mod3)
update_file("axon_carousel_4.html", mod4)

if os.path.exists("axon_carousel_5.html"):
    with open("axon_carousel_5.html", "r", encoding='utf-8') as f:
        c5 = f.read()
    c5 = c5.replace(inter_link_3, font_link)
    c5 = c5.replace("font-family: 'Inter', sans-serif;", "font-family: 'Satoshi', sans-serif;", 1)
    c5 = c5.replace("font-family: 'Inter', sans-serif;", "font-family: 'Clash Display', sans-serif;")
    with open("axon_carousel_5.html", "w", encoding='utf-8') as f:
        f.write(c5)
