#!/usr/bin/env python3
"""
export.py  —  Step 3 of FA Content Engine pipeline

Converts branded HTML post → MP4 / GIF / PNG

Usage:
  python pipeline/export.py --slug 2026-03-31-abc123              # → GIF (default)
  python pipeline/export.py --slug 2026-03-31-abc123 --fmt mp4    # → MP4
  python pipeline/export.py --slug 2026-03-31-abc123 --fmt png    # → static PNG

Requires:
  pip install playwright pillow
  playwright install chromium
  # For MP4: ffmpeg on PATH  (brew install ffmpeg  /  apt install ffmpeg)
"""

import argparse
import io
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT        = Path(__file__).parent.parent
POSTS_DIR   = ROOT / "posts"
EXPORTS_DIR = ROOT / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

CANVAS_PX   = 800   # must match --fa-canvas-size
FPS         = 30
DURATION_S  = 3     # seconds of animation for GIF / MP4


# ── Screenshot via Playwright ─────────────────────────────────────────────────

def screenshot_html(html_path: Path) -> bytes:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": CANVAS_PX + 100, "height": CANVAS_PX + 100})
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")
        # Wait for web fonts
        page.wait_for_timeout(1200)
        # Crop to canvas
        canvas = page.locator(".fa-canvas")
        png_bytes = canvas.screenshot(type="png")
        browser.close()
    return png_bytes


# ── PNG ───────────────────────────────────────────────────────────────────────

def export_png(png_bytes: bytes, out: Path):
    out.write_bytes(png_bytes)
    print(f"[export] PNG  → {out}")


# ── GIF (animated fade-in) ────────────────────────────────────────────────────

def export_gif(png_bytes: bytes, out: Path, duration_s: int = DURATION_S, fps: int = 10):
    from PIL import Image
    n_frames = duration_s * fps
    frame_duration_ms = 1000 // fps

    base = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    frames = []

    for i in range(n_frames):
        # Fade-in over first 0.6s, hold, then subtle pulse
        t = i / n_frames
        if t < 0.2:
            alpha = int(255 * (t / 0.2))          # fade in
        elif t > 0.85:
            alpha = int(255 * (1 - (t - 0.85) / 0.15) * 0.15 + 255 * 0.85)  # slight dim
        else:
            alpha = 255

        f = base.copy()
        r, g, b, a = f.split()
        a = a.point(lambda x: int(x * alpha / 255))
        merged = Image.merge("RGBA", (r, g, b, a))
        # Flatten onto dark bg
        bg = Image.new("RGBA", merged.size, (13, 11, 43, 255))
        bg.alpha_composite(merged)
        frames.append(bg.convert("P", palette=Image.ADAPTIVE, colors=256))

    frames[0].save(
        str(out),
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=frame_duration_ms,
        optimize=True,
    )
    print(f"[export] GIF  → {out}  ({n_frames} frames @ {fps}fps)")


# ── MP4 (via ffmpeg) ──────────────────────────────────────────────────────────

def export_mp4(png_bytes: bytes, out: Path, duration_s: int = DURATION_S, fps: int = FPS):
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not found on PATH. Install: brew install ffmpeg")

    from PIL import Image
    base = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    n_frames = duration_s * fps

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for i in range(n_frames):
            t = i / n_frames
            # Ken-Burns: very subtle zoom 1.00→1.04
            scale = 1.0 + 0.04 * t
            new_w = int(CANVAS_PX * scale)
            new_h = int(CANVAS_PX * scale)
            resized = base.resize((new_w, new_h), Image.LANCZOS)
            # Center-crop back to CANVAS_PX
            left = (new_w - CANVAS_PX) // 2
            top  = (new_h - CANVAS_PX) // 2
            frame = resized.crop((left, top, left + CANVAS_PX, top + CANVAS_PX))
            frame.save(tmp / f"frame_{i:04d}.png")

        # Fade-in overlay: first 0.5s black→transparent
        fade_frames = int(fps * 0.5)
        for i in range(fade_frames):
            alpha = int(255 * (1 - i / fade_frames))
            overlay = Image.new("RGBA", (CANVAS_PX, CANVAS_PX), (0, 0, 0, alpha))
            base_f  = Image.open(tmp / f"frame_{i:04d}.png").convert("RGBA")
            base_f.alpha_composite(overlay)
            base_f.convert("RGB").save(tmp / f"frame_{i:04d}.png")

        frame_pattern = str(tmp / "frame_%04d.png")
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", frame_pattern,
            "-vf", f"scale={CANVAS_PX}:{CANVAS_PX}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-movflags", "+faststart",
            str(out),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"[export] MP4  → {out}  ({duration_s}s @ {fps}fps, Ken-Burns zoom)")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="FA pipeline: export branded post")
    parser.add_argument("--slug",     required=True,   help="Post slug")
    parser.add_argument("--fmt",      default="gif",   choices=["gif", "mp4", "png"], help="Output format")
    parser.add_argument("--duration", type=int, default=DURATION_S, help="Animation seconds")
    parser.add_argument("--fps",      type=int, default=None,       help="Frames per second")
    args = parser.parse_args()

    html_path = POSTS_DIR / f"{args.slug}.html"
    if not html_path.exists():
        raise SystemExit(f"Post HTML not found: {html_path}. Run compose.py first.")

    print(f"[export] rendering {html_path} …")
    png_bytes = screenshot_html(html_path)

    out = EXPORTS_DIR / f"{args.slug}.{args.fmt}"

    if args.fmt == "png":
        export_png(png_bytes, out)
    elif args.fmt == "gif":
        fps = args.fps or 10
        export_gif(png_bytes, out, duration_s=args.duration, fps=fps)
    elif args.fmt == "mp4":
        fps = args.fps or FPS
        export_mp4(png_bytes, out, duration_s=args.duration, fps=fps)

    print(f"[export] done  → {out}")


if __name__ == "__main__":
    main()
