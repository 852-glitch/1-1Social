#!/usr/bin/env python3
"""
ingest.py  —  Step 1 of FA Content Engine pipeline

Accepts:
  --url   https://x.com/user/status/...  (scrapes tweet text + metadata)
  --img   /path/to/screenshot.png        (OCR extracts text)

Outputs a JSON file to  pipeline/queue/<slug>.json
that the next step (compose.py) reads.

Install:
  pip install playwright requests pillow pytesseract
  playwright install chromium
  # macOS: brew install tesseract
  # Linux: sudo apt install tesseract-ocr
"""

import argparse
import json
import re
import sys
import hashlib
from datetime import datetime
from pathlib import Path

QUEUE_DIR = Path(__file__).parent / "queue"
QUEUE_DIR.mkdir(exist_ok=True)


# ── URL ingestion (Playwright headless) ──────────────────────────────────────

def ingest_url(url: str) -> dict:
    from playwright.sync_api import sync_playwright

    data = {"source_url": url, "source_type": "url"}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)

        # X.com / Twitter
        if "x.com" in url or "twitter.com" in url:
            try:
                article = page.locator("article[data-testid='tweet']").first
                text = article.locator("[data-testid='tweetText']").inner_text(timeout=5000)
                handle = article.locator("[data-testid='User-Name']").inner_text(timeout=5000)
                data["author"] = handle.split("\n")[0].strip()
                data["handle"] = handle.split("\n")[-1].strip()
                data["body"]   = text.strip()
                # Try to grab engagement numbers
                likes    = page.locator("[data-testid='like'] span").first.inner_text(timeout=3000)
                retweets = page.locator("[data-testid='retweet'] span").first.inner_text(timeout=3000)
                data["stats"] = [
                    {"value": likes,    "label": "Likes"},
                    {"value": retweets, "label": "Retweets"},
                ]
            except Exception as e:
                print(f"[warn] Tweet scrape partial: {e}", file=sys.stderr)
        else:
            # Generic: grab page title + og:description
            data["title"] = page.title()
            og = page.locator('meta[property="og:description"]')
            if og.count():
                data["body"] = og.get_attribute("content", timeout=3000) or ""

        browser.close()

    return data


# ── Image / screenshot ingestion (Tesseract OCR) ─────────────────────────────

def ingest_image(img_path: str) -> dict:
    import pytesseract
    from PIL import Image

    img = Image.open(img_path)
    raw = pytesseract.image_to_string(img)
    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    return {
        "source_type": "image",
        "source_path": img_path,
        "body": "\n".join(lines),
        "raw_lines": lines,
    }


# ── Slug & save ──────────────────────────────────────────────────────────────

def make_slug(data: dict) -> str:
    seed = (data.get("source_url") or data.get("source_path") or "post") + datetime.utcnow().isoformat()
    short = hashlib.md5(seed.encode()).hexdigest()[:8]
    date  = datetime.utcnow().strftime("%Y-%m-%d")
    return f"{date}-{short}"


def save_queue(data: dict, slug: str) -> Path:
    data["slug"]       = slug
    data["ingested_at"] = datetime.utcnow().isoformat()
    out = QUEUE_DIR / f"{slug}.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"[ingest] queued → {out}")
    return out


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="FA pipeline: ingest post")
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL of tweet / post")
    group.add_argument("--img", help="Path to screenshot image")
    parser.add_argument("--slug", help="Override output slug")
    args = parser.parse_args()

    data = ingest_url(args.url) if args.url else ingest_image(args.img)
    slug = args.slug or make_slug(data)
    save_queue(data, slug)
    print(slug)  # stdout for chaining


if __name__ == "__main__":
    main()
