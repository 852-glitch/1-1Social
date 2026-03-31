# fa-content-engine

> The Financial Architect — Social Content Studio

Lives inside `852-glitch/1-1Social`. Handles all post creation, GIF export, and brand asset management. The main site repo (`852-glitch/1-1`) stays untouched.

---

## Structure

```
fa-content-engine/
├── brand/
│   ├── brand.css        ← All design tokens (colors, fonts, spacing)
│   └── nazar.svg        ← Evil eye mark — exact favicon.svg colors
├── templates/
│   └── post-base.html   ← Card shell (inherit for every post)
├── posts/
│   └── 2026-03-worldcup.html
├── exports/             ← GIFs and PNGs land here (gitignored)
├── scripts/
│   └── render.py        ← HTML → animated GIF via Pillow + Selenium
└── README.md
```

---

## Brand Tokens (`brand/brand.css`)

All CSS custom properties are locked to `brand_tokens.json`:

| Token | Value | Use |
|---|---|---|
| `--fa-bg` | `#0d0b2b` | Canvas background |
| `--fa-accent` | `#4f46e5` | Indigo accent / logo |
| `--fa-accent-teal` | `#34d399` | Headline em, stat values |
| `--fa-accent-purple` | `#a78bfa` | Subtle highlights |
| `--fa-font-headline` | Manrope 800 | Headlines |
| `--fa-font-body` | Inter | Body / eyebrow |
| `--fa-font-accent` | Fraunces italic | Quotes / em |
| `--fa-nazar-deep` | `#1A1F71` | Nazar SVG outer |
| `--fa-nazar-light` | `#89C4E1` | Nazar SVG mid ring |

---

## Create a New Post

1. Duplicate `posts/2026-03-worldcup.html`
2. Rename: `posts/YYYY-MM-topic.html`
3. Edit the `<!-- EDITABLE ZONE -->` section only
4. Export:

```bash
python scripts/render.py --out exports/YYYY-MM-topic.gif
```

---

## Export Options

```bash
# Default (8 frames, 2s each)
python scripts/render.py --out exports/my-post.gif

# Custom frames + speed
python scripts/render.py --out exports/my-post.gif --frames 6 --duration 1500

# Static PNG
python scripts/render.py --out exports/my-post.png --static
```

---

## Requirements

```bash
pip install pillow selenium
# + ChromeDriver on PATH matching your Chrome version
```

---

## .gitignore

```
exports/
__pycache__/
*.pyc
.DS_Store
```
