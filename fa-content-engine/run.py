#!/usr/bin/env python3
"""
run.py  —  FA Content Engine  /  One-command pipeline

Usage:
  # From a tweet URL:
  python run.py --url https://x.com/user/status/123456

  # From a screenshot:
  python run.py --img ~/Desktop/screenshot.png

  # With format override:
  python run.py --url https://x.com/... --fmt mp4

  # With manual overrides:
  python run.py --url https://x.com/... --eyebrow "Markets · Mar 2026" --quote "Your custom pull quote here"

Outputs:
  exports/<slug>.gif   (default)
  exports/<slug>.mp4
  exports/<slug>.png
"""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def run(cmd: list, label: str):
    print(f"\n{'─'*50}")
    print(f"  {label}")
    print(f"{'─'*50}")
    result = subprocess.run(
        [sys.executable] + cmd,
        capture_output=False,
        cwd=HERE,
    )
    if result.returncode != 0:
        raise SystemExit(f"Pipeline failed at: {label}")


def main():
    parser = argparse.ArgumentParser(
        description="FA Content Engine — full pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url",  help="Tweet / post URL")
    group.add_argument("--img",  help="Screenshot path")
    parser.add_argument("--fmt",      default="gif", choices=["gif", "mp4", "png"])
    parser.add_argument("--duration", type=int, default=3, help="Animation length in seconds")
    parser.add_argument("--eyebrow",  help="Override eyebrow text")
    parser.add_argument("--quote",    help="Override pull quote")
    parser.add_argument("--slug",     help="Force a specific slug (skip ingest if post already exists)")
    args = parser.parse_args()

    # ── Step 1: Ingest ──────────────────────────────────────────────────────
    if args.slug:
        slug = args.slug
        print(f"[run] using existing slug: {slug}")
    else:
        ingest_args = ["pipeline/ingest.py"]
        if args.url:
            ingest_args += ["--url", args.url]
        else:
            ingest_args += ["--img", args.img]

        import subprocess as sp
        result = sp.run(
            [sys.executable] + ingest_args,
            capture_output=True, text=True, cwd=HERE,
        )
        if result.returncode != 0:
            print(result.stderr)
            raise SystemExit("Ingest failed.")
        slug = result.stdout.strip().splitlines()[-1]
        print(result.stdout, end="")

    # ── Step 2: Compose ─────────────────────────────────────────────────────
    compose_args = ["pipeline/compose.py", "--slug", slug]
    if args.eyebrow:
        compose_args += ["--eyebrow", args.eyebrow]
    if args.quote:
        compose_args += ["--quote", args.quote]
    run(compose_args, f"compose  →  posts/{slug}.html")

    # ── Step 3: Export ──────────────────────────────────────────────────────
    export_args = ["pipeline/export.py", "--slug", slug, "--fmt", args.fmt, "--duration", str(args.duration)]
    run(export_args, f"export   →  exports/{slug}.{args.fmt}")

    print(f"\n✅  Done  →  fa-content-engine/exports/{slug}.{args.fmt}")


if __name__ == "__main__":
    main()
