#!/usr/bin/env python3
"""
compose.py  —  Step 2 of FA Content Engine pipeline

Reads  pipeline/queue/<slug>.json
Writes branded HTML to  posts/<slug>.html

Usage:
  python pipeline/compose.py --slug 2026-03-31-abc123
  python pipeline/compose.py --slug 2026-03-31-abc123 --template templates/post-base.html
"""

import argparse
import json
import re
from pathlib import Path

ROOT      = Path(__file__).parent.parent
QUEUE_DIR = Path(__file__).parent / "queue"
POSTS_DIR = ROOT / "posts"
POSTS_DIR.mkdir(exist_ok=True)

DEFAULT_TEMPLATE = ROOT / "templates" / "post-base.html"


def truncate(text: str, max_chars: int = 180) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "…"


def accent_numbers(text: str) -> str:
    """Wrap numeric tokens like $10B, 4%, 1M in <em> for teal accent."""
    return re.sub(r"(\$?\d[\d,.]*[BMKbmk%x+]?)", r"<em>\1</em>", text)


def build_context(data: dict) -> dict:
    """Map raw ingested data to template placeholders."""
    body_raw  = data.get("body", "Content ingested from source.")
    headline  = truncate(body_raw, 80)
    body_text = truncate(body_raw, 180)

    stats = data.get("stats", [])
    while len(stats) < 3:
        stats.append({"value": "—", "label": ""})

    author  = data.get("author", "The Financial Architect")
    handle  = data.get("handle", "@TheFA")
    eyebrow = data.get("eyebrow", f"{author}  ·  {handle}")
    quote   = data.get("quote", truncate(body_raw, 100))

    return {
        "POST_TITLE":    data.get("slug", "post"),
        "EYEBROW":       eyebrow,
        "HEADLINE":      accent_numbers(headline),
        "BODY":          body_text,
        "QUOTE":         quote,
        "STAT_1_VALUE":  stats[0]["value"],
        "STAT_1_LABEL":  stats[0]["label"],
        "STAT_2_VALUE":  stats[1]["value"],
        "STAT_2_LABEL":  stats[1]["label"],
        "STAT_3_VALUE":  stats[2]["value"],
        "STAT_3_LABEL":  stats[2]["label"],
    }


def render_html(template_path: Path, ctx: dict) -> str:
    html = template_path.read_text()
    for key, val in ctx.items():
        html = html.replace("{{" + key + "}}", str(val))
    return html


def main():
    parser = argparse.ArgumentParser(description="FA pipeline: compose branded HTML")
    parser.add_argument("--slug",     required=True, help="Queue slug to process")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE), help="Template HTML path")
    parser.add_argument("--eyebrow",  help="Override eyebrow text")
    parser.add_argument("--quote",    help="Override pull quote")
    args = parser.parse_args()

    queue_file = QUEUE_DIR / f"{args.slug}.json"
    if not queue_file.exists():
        raise SystemExit(f"Queue file not found: {queue_file}")

    data = json.loads(queue_file.read_text())
    if args.eyebrow:
        data["eyebrow"] = args.eyebrow
    if args.quote:
        data["quote"] = args.quote

    ctx  = build_context(data)
    html = render_html(Path(args.template), ctx)

    out = POSTS_DIR / f"{args.slug}.html"
    out.write_text(html)
    print(f"[compose] rendered → {out}")
    print(args.slug)


if __name__ == "__main__":
    main()
