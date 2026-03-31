# fa-content-engine

> The Financial Architect — Automated Social Content Studio

Lives inside `852-glitch/1-1Social`. Converts a tweet URL or screenshot → branded MP4 / GIF / PNG in one command.

---

## One-command usage

```bash
# From a tweet URL
python run.py --url https://x.com/user/status/123456789

# From a screenshot
python run.py --img ~/Desktop/screenshot.png

# Choose output format
python run.py --url https://x.com/... --fmt mp4
python run.py --url https://x.com/... --fmt png

# Override eyebrow or pull-quote
python run.py --url https://x.com/... --eyebrow "Markets · Mar 2026" --quote "Your quote here"
```

Output lands in `exports/<slug>.[gif|mp4|png]`.

---

## Pipeline

```
[URL or screenshot]
       │
       ▼
 pipeline/ingest.py   ← scrapes tweet text / OCR from image
       │               writes  pipeline/queue/<slug>.json
       ▼
 pipeline/compose.py  ← injects content into branded HTML template
       │               writes  posts/<slug>.html
       ▼
 pipeline/export.py   ← Playwright screenshots HTML
       │               Pillow/ffmpeg renders GIF or MP4
       ▼
 exports/<slug>.[gif|mp4|png]   ← ready to post
```

---

## Structure

```
fa-content-engine/
├── brand/
│   ├── brand.css          ← design tokens + utility classes
│   └── nazar.svg          ← evil eye mark
├── templates/
│   └── post-base.html     ← reusable card shell
├── pipeline/
│   ├── ingest.py          ← URL scraper / OCR
│   ├── compose.py         ← content → branded HTML
│   ├── export.py          ← HTML → GIF / MP4 / PNG
│   └── queue/             ← JSON queue (gitignored)
├── posts/                 ← rendered HTML (per post)
├── exports/               ← final files (gitignored)
├── run.py                 ← single entry point
├── requirements.txt
└── README.md
```

---

## Setup

```bash
pip install -r requirements.txt
playwright install chromium

# For MP4 export (Ken-Burns animated):
brew install ffmpeg       # macOS
sudo apt install ffmpeg   # Linux

# For screenshot OCR (--img mode):
brew install tesseract    # macOS
sudo apt install tesseract-ocr   # Linux
```

---

## Brand tokens

All visual rules live in `brand/brand.css` as CSS custom properties.
Source of truth: `brand_tokens.json` in repo root.

| Token | Value |
|---|---|
| `--fa-bg` | `#0d0b2b` |
| `--fa-accent` | `#4f46e5` |
| `--fa-accent-teal` | `#34d399` |
| `--fa-font-headline` | Manrope 800 |
| `--fa-font-body` | Inter |
| `--fa-font-accent` | Fraunces italic |

---

## Export formats

| Format | How | Notes |
|---|---|---|
| `gif` | Pillow animated | Fade-in, 10fps, 3s. Works everywhere. |
| `mp4` | ffmpeg + Ken-Burns zoom | Smooth 30fps, ready for Reels/Stories |
| `png` | Static screenshot | For feed posts or further editing |

---

## .gitignore

```
exports/
pipeline/queue/*.json
__pycache__/
*.pyc
.DS_Store
```
