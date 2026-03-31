#!/usr/bin/env python3
"""
FA Content Engine — render.py
Converts an HTML post into an animated GIF (or static PNG).

Usage:
  python scripts/render.py --out exports/my-post.gif
  python scripts/render.py --out exports/my-post.gif --frames 6 --duration 1500
  python scripts/render.py --out exports/my-post.png --static

Requires:
  pip install pillow selenium
  ChromeDriver matching your Chrome version on PATH
"""

import argparse
import os
import time
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow not found. Run: pip install pillow")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError:
    raise SystemExit("Selenium not found. Run: pip install selenium")


CANVAS_SIZE = 800  # pixels — must match --fa-canvas-size in brand.css


def capture_frame(driver, path: Path) -> Image.Image:
    """Screenshot the canvas element and return as PIL Image."""
    driver.get(f"file://{path.resolve()}")
    time.sleep(0.3)  # allow fonts to load
    png_bytes = driver.get_screenshot_as_png()
    import io
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    # Crop to canvas square
    w, h = img.size
    left = (w - CANVAS_SIZE) // 2
    top  = (h - CANVAS_SIZE) // 2
    return img.crop((left, top, left + CANVAS_SIZE, top + CANVAS_SIZE))


def build_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--window-size={CANVAS_SIZE + 100},{CANVAS_SIZE + 100}")
    return webdriver.Chrome(options=opts)


def main():
    parser = argparse.ArgumentParser(description="FA Content Engine renderer")
    parser.add_argument("--src",      default=None,  help="Path to post HTML (auto-detect if omitted)")
    parser.add_argument("--out",      required=True, help="Output path (.gif or .png)")
    parser.add_argument("--frames",   type=int, default=8,    help="Number of GIF frames")
    parser.add_argument("--duration", type=int, default=2000, help="Ms per frame")
    parser.add_argument("--static",   action="store_true",    help="Export PNG instead of GIF")
    args = parser.parse_args()

    # Auto-detect most-recent post if --src not given
    if args.src:
        src = Path(args.src)
    else:
        posts_dir = Path(__file__).parent.parent / "posts"
        htmls = sorted(posts_dir.glob("*.html"))
        if not htmls:
            raise SystemExit("No HTML posts found in posts/")
        src = htmls[-1]
        print(f"Auto-detected post: {src}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    driver = build_driver()
    try:
        frame = capture_frame(driver, src)

        if args.static or out.suffix.lower() == ".png":
            frame.save(str(out))
            print(f"PNG saved → {out}")
        else:
            # Repeat same frame with slight opacity pulse for subtle animation
            frames = []
            for i in range(args.frames):
                alpha = int(240 + 15 * (i % 2))  # subtle pulse
                f = frame.copy()
                r, g, b, a = f.split()
                a = a.point(lambda x: min(255, int(x * alpha / 255)))
                frames.append(Image.merge("RGBA", (r, g, b, a)).convert("P", palette=Image.ADAPTIVE))

            frames[0].save(
                str(out),
                save_all=True,
                append_images=frames[1:],
                loop=0,
                duration=args.duration,
            )
            print(f"GIF saved → {out} ({args.frames} frames @ {args.duration}ms each)")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
