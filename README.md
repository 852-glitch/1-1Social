# 1:1Social

**Brand-consistent social media post engine for The Financial Architect**

Automatically generate LinkedIn/Twitter/Instagram posts using your brand's visual identity — finance-standard layouts with colorful contextual highlights.

---

## What It Does

This engine takes structured post data (text, stats, quotes) and renders it into pixel-perfect branded images matching the visual system from [clarity_protocol.html](https://852-glitch.github.io/1-1/clarity_protocol.html).

**Input:** JSON object with headline, body, stats, quote  
**Output:** HTML ready for screenshot → social post image

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
  body: "Vacation rental demand in host cities is surging <strong>200%+</strong>. Millions of investors are seeing that chart and asking the wrong question.",
  quote: "Does this fit my rules — or am I just reacting to a headline?",
  stats: [
    { value: "200%+", label: "RENTAL DEMAND SURGE" },
    { value: "Weeks", label: "EVENT DURATION" },
    { icon: "∞", label: "FOMO THAT FOLLOWS" }
  ]
});

// Write to file or render in DOM
document.body.innerHTML = html;
```

---

## File Structure

```
1-1Social/
├── brand_tokens.json          # Complete design system (colors, fonts, spacing)
├── post_template.html         # Static template with example post
├── engine/
│   └── composer.js            # PostComposer class - programmatic post generator
└── README.md
```

---

## Usage Patterns

### Text-Only Post
```javascript
composer.compose({
  eyebrow: "INVESTING DISCIPLINE",
  headline: "Your biggest edge isn't speed. It's patience.",
  body: "The market rewards those who wait for their setup — not those who react to every headline.",
  quote: "Discipline beats conviction. Every time."
});
```

### Stats-Focused Post
```javascript
composer.compose({
  eyebrow: "MARKET PSYCHOLOGY",
  headline: "Retail traders are <span class='headline-accent'>90% wrong</span> at extremes.",
  stats: [
    { value: "90%", label: "WRONG AT TOPS" },
    { value: "85%", label: "WRONG AT BOTTOMS" },
    { icon: "📉", label: "HERD BEHAVIOR" }
  ]
});
```

### Quote-Led Post
```javascript
composer.compose({
  eyebrow: "WISDOM",
  quote: "The stock market is a device for transferring money from the impatient to the patient. — Warren Buffett",
  body: "This isn't just a quote. It's the entire strategy."
});
```

---

## Customization

### Changing Colors
Edit `brand_tokens.json`:
```json
"colors": {
  "accentTeal": "#34d399",  // Change this to your brand color
  "accent": "#4f46e5"
}
```

### Adjusting Layout
Edit spacing in `brand_tokens.json`:
```json
"spacing": {
  "canvasSize": "800px",
  "padding": "48px"
}
```

### Adding New Fonts
Update `fonts` section in `brand_tokens.json`, then modify `googleFontsUrl`.

---

## Export to Image

### Option 1: Browser Screenshot
1. Open the generated HTML in a browser
2. Use browser DevTools to set viewport to 800px width
3. Take screenshot

### Option 2: Headless Browser (Puppeteer)
```javascript
const puppeteer = require('puppeteer');

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setViewport({ width: 800, height: 1000 });
await page.setContent(html);
await page.screenshot({ path: 'post.png', fullPage: true });
await browser.close();
```

### Option 3: Use Claude/AI with Image Export
Paste the HTML into an AI that can render HTML → image (e.g., Claude with web preview).

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
- [ ] CLI tool for batch generation
- [ ] Figma plugin for design handoff

---

## Credits

Brand system extracted from [The Financial Architect / Clarity Protocol](https://852-glitch.github.io/1-1/clarity_protocol.html)  
Built with: HTML/CSS/Vanilla JS + Google Fonts (Manrope, Inter, Fraunces)

---

**License:** MIT  
**Maintained by:** [@852-glitch](https://github.com/852-glitch)
