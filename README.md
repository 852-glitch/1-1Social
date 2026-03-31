# 1:1Social

**Brand-consistent social media post engine for The Financial Architect**

Automatically generate LinkedIn/Twitter/Instagram posts using your brand's visual identity — finance-standard layouts with colorful contextual highlights.

---

## What It Does

This engine takes structured post data (text, stats, quotes) and renders it into pixel-perfect branded images matching the visual system from [clarity_protocol.html](https://852-glitch.github.io/1-1/clarity_protocol.html).

**Input:** JSON object with headline, body, stats, quote  
**Output:** HTML ready for screenshot → social post image

---

## Automated Pipeline

Send a URL or screenshot → get a ready-to-post MP4 / GIF / PNG. One command handles everything.

```bash
python run.py --url https://x.com/user/status/123456
# or
python run.py --img path/to/screenshot.png --fmt mp4
```

Output lands in `exports/<slug>.[gif|mp4|png]`.

### How it works

```
[Your URL or screenshot]
         │
         ▼
 pipeline/ingest.py    ← Playwright scrapes tweet text, author, likes/RTs
         │               OCR (Tesseract) if you pass a screenshot
         │               → writes pipeline/queue/<slug>.json
         ▼
 pipeline/compose.py   ← Reads queue JSON, fills {{PLACEHOLDERS}} in
         │               templates/post-base.html with brand CSS baked in.
         │               Numbers auto-wrap in teal <em> (e.g. $10B, 4%)
         │               → writes posts/<slug>.html
         ▼
 pipeline/export.py    ← Playwright screenshots the branded HTML
                         Pillow renders animated GIF (fade-in, 10fps)
                         ffmpeg renders MP4 (30fps, Ken-Burns zoom)
                         → exports/<slug>.[gif|mp4|png]
```

### What `pipeline/compose.py` does

`compose.py` is the bridge between raw scraped data and your branded template.  
It reads `pipeline/queue/<slug>.json` and maps each field into the template:

| JSON field | Template placeholder | Notes |
|---|---|---|
| `headline` | `{{HEADLINE}}` | Numbers auto-wrapped in teal `<em>` |
| `body` | `{{BODY}}` | Plain paragraph text |
| `eyebrow` | `{{EYEBROW}}` | Defaults to `author · handle` |
| `quote` | `{{QUOTE}}` | Pull-quote block |
| `stat_1_value` | `{{STAT_1_VALUE}}` | Stat card top line |
| `stat_1_label` | `{{STAT_1_LABEL}}` | Stat card label |

Result: a fully styled `posts/<slug>.html` ready for headless rendering.

### Output formats

| Format | Engine | Best for |
|---|---|---|
| `gif` | Pillow, 10fps, 3s fade-in | Twitter/X, everywhere |
| `mp4` | ffmpeg, 30fps, subtle zoom | Reels, Stories, TikTok |
| `png` | Static screenshot | Feed posts, further editing |

### Override flags

```bash
python run.py --url https://x.com/... \
  --eyebrow "Markets · Mar 2026" \
  --quote "Your custom pull quote" \
  --fmt mp4 \
  --duration 5
```

---

## @ Shortcut — Send Posts Directly

You can trigger the pipeline by mentioning `@1-1Social` anywhere in your workflow.  
Instead of opening a terminal each time, use the `@` shortcut to drop a URL or screenshot path directly into the pipeline.

> **Note:** The exact `@` trigger binding is configured in your app settings — see your settings panel to activate it. Once set, typing `@1-1Social <url>` routes the input straight to `run.py`.

---

## One-Time Setup (Windows)

```bash
cd fa-content-engine
pip install -r requirements.txt
playwright install chromium
```

### ffmpeg (required for MP4 output)

1. Go to **https://ffmpeg.org/download.html**
2. Under **Windows**, click **"Windows builds from gyan.dev"** or **"Windows builds by BtbN"** (both are official mirror links on the ffmpeg.org page)
3. Download the latest **full** static build `.zip`
4. Extract it (e.g. to `C:\ffmpeg`)
5. Add `C:\ffmpeg\bin` to your system **PATH**:
   - Search → "Edit the system environment variables"
   - Environment Variables → System variables → `Path` → Edit → New → paste `C:\ffmpeg\bin`
6. Open a **new** terminal and verify:
   ```bash
   ffmpeg -version
   ```

### Tesseract (required for screenshot / OCR input)

1. Download the Windows installer from:  
   **https://github.com/UB-Mannheim/tesseract/wiki**
2. Run the installer — note the install path (default: `C:\Program Files\Tesseract-OCR`)
3. Add `C:\Program Files\Tesseract-OCR` to your **PATH** (same steps as above)
4. Verify:
   ```bash
   tesseract --version
   ```

> After editing PATH, always open a **new terminal window** so changes take effect.

---

## Brand System

### Visual Identity
- **Fonts:** Manrope (headings), Inter (body), Fraunces (italic/accent)
- **Colors:** Deep navy gradient background (`#0d0b2b → #1a0b2e`) + aurora orbs (indigo/violet/pink)
- **Accent color:** Teal (`#34d399`) for highlighted text like "FOMO event"
- **Layout:** 800px canvas, dark glass stat cards, eyebrow category tags, footer branding

### Brand Voice
- Finance-standard structure
- Behavioral psychology focus
- Tagline: **NO HYPE. JUST DISCIPLINE.**

---

## File Structure

```
1-1Social/
├── brand_tokens.json          # Complete design system (colors, fonts, spacing)
├── post_template.html         # Static template with example post
├── engine/
│   └── composer.js            # PostComposer class
├── fa-content-engine/
│   ├── brand/
│   │   ├── brand.css          # Shared colors, fonts, CSS variables
│   │   └── nazar.svg          # Brand mark asset
│   ├── templates/
│   │   └── post-base.html     # Card shell with {{PLACEHOLDERS}}
│   ├── posts/                 # Generated per-post HTML files
│   ├── exports/               # Output GIFs / MP4s / PNGs land here
│   ├── pipeline/
│   │   ├── ingest.py          # URL/screenshot → queue JSON
│   │   ├── compose.py         # JSON → branded HTML
│   │   └── export.py          # HTML → GIF / MP4 / PNG
│   └── run.py                 # Single entry point
└── README.md
```

---

## Quick Start

### 1. Use the Template Directly
Open `post_template.html` in a browser to see the example post. Edit the HTML directly to customize content.

### 2. Use the Composer (Programmatic)

```javascript
// Load brand tokens
const brandTokens = await fetch('./brand_tokens.json').then(r => r.json());

// Initialize composer
const composer = new PostComposer(brandTokens);

// Generate post
const html = composer.compose({
  eyebrow: "BEHAVIORAL FINANCE",
  headline: "The World Cup isn't just a tournament. It's a FOMO event in disguise.",
  headlineAccent: "FOMO event",
  body: "Vacation rental demand in host cities is surging **200%+**.",
  quote: "Does this fit my rules — or am I just reacting to a headline?",
  stats: [
    { value: "200%+", label: "RENTAL DEMAND SURGE" },
    { value: "Weeks", label: "EVENT DURATION" },
    { icon: "∞", label: "FOMO THAT FOLLOWS" }
  ]
});
```

---

## Design Principles

1. **Finance-standard base** — Clean grids, structured hierarchy, professional spacing
2. **Colorful context layer** — Teal accents highlight key insights, aurora orbs add depth
3. **Behavioral focus** — Content emphasizes psychology over hype
4. **Consistent branding** — Every post carries logo, tagline, font system

---

## Future Enhancements

- [ ] Add graph/chart embedding support
- [ ] Multi-layout system (portrait, square, landscape)
- [ ] Animation layer (subtle aurora movement)
- [ ] `@` shortcut deep integration (pending settings configuration)
- [ ] Figma plugin for design handoff

---

## Credits

Brand system extracted from [The Financial Architect / Clarity Protocol](https://852-glitch.github.io/1-1/clarity_protocol.html)  
Built with: HTML/CSS/Vanilla JS + Python (Playwright, Pillow, ffmpeg) + Google Fonts

---

**License:** MIT  
**Maintained by:** [@852-glitch](https://github.com/852-glitch)
