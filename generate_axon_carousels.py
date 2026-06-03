import os

carousels = [
    {
        "filename": "carousel_1_mcp.html",
        "colors": {"bg": "#1b3022", "text": "#f4efe6", "accent": "#ff6542", "button_bg": "#000000", "button_text": "#f4efe6"},
        "slides": [
            {"type": "cover", "headline": "The AI skill your competitors haven't learned yet"},
            {"type": "inner", "num": "01", "headline": "What is MCP?", "body": "Model Context Protocol &mdash; it connects AI to your real business tools like CRM, ads, and analytics."},
            {"type": "inner", "num": "02", "headline": "Think of it like USB-C for AI.", "body": "One standard. Every tool plugs in. No messy custom integrations."},
            {"type": "inner", "num": "03", "headline": "One AI agent can now &mdash;", "body": "update your CRM, pull ad reports, send follow-ups, and trigger campaigns. All in one conversation."},
            {"type": "inner", "num": "04", "headline": "Agencies using MCP in 2026", "body": "will work 10x faster than those still doing it manually."},
            {"type": "cta", "headline": "Follow NeoArk Digital", "body": "for weekly AI insights that actually grow your business."}
        ]
    },
    {
        "filename": "carousel_2_github.html",
        "colors": {"bg": "#f4efe6", "text": "#1b3022", "accent": "#3a4f40", "button_bg": "#000000", "button_text": "#f4efe6"},
        "slides": [
            {"type": "cover", "headline": "3 free AI tools on GitHub that most agencies haven't found yet"},
            {"type": "inner", "num": "01", "headline": "awesome-ai-agents-2026", "body": "300+ AI agents for marketing, sales, and research. Free. Updated monthly."},
            {"type": "inner", "num": "02", "headline": "ai-marketing", "body": "Open-source lead gen + Google Maps scraper with AI email and WhatsApp templates. Built for agencies."},
            {"type": "inner", "num": "03", "headline": "Microsoft AutoGen 1.0", "body": "Multi-agent system where one agent writes, one reviews, one executes. Zero human coordination needed."},
            {"type": "inner", "num": "04", "headline": "The best tools aren't always the paid ones.", "body": "The open-source AI ecosystem is moving faster than any SaaS product."},
            {"type": "cta", "headline": "Save this post.", "body": "Share it with your team. Follow NeoArk Digital for more."}
        ]
    },
    {
        "filename": "carousel_3_ai_skills.html",
        "colors": {"bg": "#ff6542", "text": "#000000", "accent": "#f4efe6", "button_bg": "#000000", "button_text": "#f4efe6"},
        "slides": [
            {"type": "cover", "headline": "5 AI skills hiring managers are looking for right now"},
            {"type": "inner", "num": "01", "headline": "Prompt Engineering", "body": "Writing AI instructions that actually produce results, not just answers."},
            {"type": "inner", "num": "02", "headline": "AI Workflow Automation", "body": "Building multi-step flows using n8n, Make, or Zapier with AI nodes."},
            {"type": "inner", "num": "03", "headline": "MCP Integration", "body": "Connecting AI agents to live business tools and data."},
            {"type": "inner", "num": "04", "headline": "AI Content Production", "body": "Generating video, copy, and creatives at scale without losing quality."},
            {"type": "inner", "num": "05", "headline": "Agentic Thinking", "body": "Designing systems where AI plans and executes tasks independently."},
            {"type": "cta", "headline": "Which skill are you working on?", "body": "Comment below. Follow NeoArk Digital for more."}
        ]
    },
    {
        "filename": "carousel_4_hot_take.html",
        "colors": {"bg": "#3a4f40", "text": "#e5e7eb", "accent": "#ff6542", "button_bg": "#000000", "button_text": "#f4efe6"},
        "slides": [
            {"type": "cover", "headline": "Unpopular opinion: AI will replace campaign managers before it replaces copywriters"},
            {"type": "inner", "num": "01", "headline": "Coordination vs Creation", "body": "Campaign management is mostly coordination &mdash; pulling reports, chasing approvals, syncing dashboards. AI agents already do this."},
            {"type": "inner", "num": "02", "headline": "Human Element", "body": "But strategy, brand voice, cultural insight, and emotional storytelling? Still human work."},
            {"type": "inner", "num": "03", "headline": "The Winning Formula", "body": "The agencies that win aren't replacing people with AI. They're using AI to free their people for work that actually matters."},
            {"type": "inner", "num": "04", "headline": "Shift Your Focus", "body": "Stop learning to do tasks. Start learning to design systems."},
            {"type": "cta", "headline": "Agree or disagree?", "body": "Drop it in the comments. Follow NeoArk Digital for more hot takes."}
        ]
    },
    {
        "filename": "carousel_5_multi_agent.html",
        "colors": {"bg": "#e5e7eb", "text": "#1b3022", "accent": "#ff6542", "button_bg": "#000000", "button_text": "#f4efe6"},
        "slides": [
            {"type": "cover", "headline": "AI Insight of the Week &mdash; the biggest shift nobody's talking about"},
            {"type": "inner", "num": "01", "headline": "The Multi-Agent Era", "body": "We're moving from 'one AI, one answer' to a full team of AI agents working together."},
            {"type": "inner", "num": "02", "headline": "How It Works", "body": "One agent researches. One writes. One reviews. One publishes. No human coordination needed."},
            {"type": "inner", "num": "03", "headline": "Already Here", "body": "This is already happening inside content teams, ad agencies, and marketing firms in 2026."},
            {"type": "inner", "num": "04", "headline": "The New Workforce", "body": "The era of the solo AI assistant is ending. The era of the AI workforce is starting."},
            {"type": "cta", "headline": "Are you ready for it?", "body": "Follow NeoArk Digital &mdash; every week we break down what's actually moving in AI and marketing."}
        ]
    }
]

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Axon Studios Carousel</title>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&f[]=clash-display@400,500,600,700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: {bg};
      --text: {text};
      --accent: {accent};
      --btn-bg: {button_bg};
      --btn-text: {button_text};
    }}
    body {{
      margin: 0; padding: 40px; background: #222; 
      display: flex; gap: 40px; overflow-x: auto;
      font-family: 'Satoshi', sans-serif;
    }}
    .slide {{
      width: 1080px; height: 1350px; flex-shrink: 0;
      background: var(--bg); color: var(--text);
      position: relative; overflow: hidden;
      display: flex; flex-direction: column;
      padding: 100px 80px; box-sizing: border-box;
      box-shadow: rgba(0, 0, 0, 0.25) 0px 25px 50px -12px;
    }}
    .slide-number {{
      font-family: 'Space Mono', monospace;
      font-size: 32px; font-weight: 700;
      color: var(--accent); margin-bottom: 40px;
      display: flex; align-items: center; gap: 20px;
    }}
    .slide-number::after {{
      content: ''; flex: 1; height: 2px;
      background: var(--text); opacity: 0.2;
    }}
    .headline {{
      font-family: 'Clash Display', sans-serif;
      font-size: 85px; font-weight: 700; line-height: 1.1;
      margin-top: auto; margin-bottom: 40px;
      letter-spacing: -1px;
    }}
    .cover-headline {{
      font-size: 100px;
      margin-top: 100px;
    }}
    .body-text {{
      font-size: 40px; line-height: 1.5; font-weight: 500;
      margin-bottom: auto; opacity: 0.9;
    }}
    .cta-container {{
      margin-top: auto;
      display: flex; flex-direction: column; gap: 30px;
    }}
    .cta-button {{
      background: var(--btn-bg); color: var(--btn-text);
      padding: 24px 48px; border: none; border-radius: 0;
      font-family: 'Space Mono', monospace; font-size: 28px;
      font-weight: 700; text-transform: uppercase;
      align-self: flex-start;
      box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px;
      cursor: pointer;
      transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .cta-button:hover {{
      opacity: 0.8;
    }}
    .brand-mark {{
      position: absolute; bottom: 60px; right: 80px;
      font-family: 'Space Mono', monospace; font-size: 20px;
      font-weight: 700; opacity: 0.5; letter-spacing: 2px;
      text-transform: uppercase;
    }}
    .shape-1 {{
      position: absolute; top: -100px; right: -100px;
      width: 400px; height: 400px; border-radius: 50%;
      background: var(--accent); opacity: 0.1; z-index: 0;
    }}
    .shape-2 {{
      position: absolute; bottom: -50px; left: -50px;
      width: 200px; height: 200px; border-radius: 50%;
      background: var(--text); opacity: 0.05; z-index: 0;
    }}
    .content {{ z-index: 1; display: flex; flex-direction: column; height: 100%; }}
  </style>
</head>
<body>
{slides_html}
</body>
</html>
"""

slide_template = """
  <div class="slide">
    <div class="shape-1"></div>
    <div class="shape-2"></div>
    <div class="content">
      {top}
      <div class="headline {extra_class}">{headline}</div>
      {body_html}
      <div class="brand-mark">AXON STUDIOS</div>
    </div>
  </div>
"""

def build():
    output_dir = r"c:\Users\acer\Downloads\digi mabble carousel maker"
    for c in carousels:
        slides_html = ""
        for s in c["slides"]:
            top = ""
            body_html = ""
            extra_class = ""
            if s["type"] == "cover":
                top = '<div class="slide-number">SWIPE TO LEARN</div>'
                extra_class = "cover-headline"
            elif s["type"] == "inner":
                top = f'<div class="slide-number">{s["num"]}</div>'
                body_html = f'<div class="body-text">{s["body"]}</div>'
            elif s["type"] == "cta":
                top = '<div class="slide-number">NEXT STEPS</div>'
                body_html = f'''
                <div class="body-text">{s["body"]}</div>
                <div class="cta-container">
                  <button class="cta-button">Follow NeoArk</button>
                </div>
                '''
            
            slides_html += slide_template.format(
                top=top,
                headline=s["headline"],
                body_html=body_html,
                extra_class=extra_class
            )
        
        final_html = html_template.format(
            bg=c["colors"]["bg"],
            text=c["colors"]["text"],
            accent=c["colors"]["accent"],
            button_bg=c["colors"]["button_bg"],
            button_text=c["colors"]["button_text"],
            slides_html=slides_html
        )
        
        filepath = os.path.join(output_dir, c["filename"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"Generated {filepath}")

build()
