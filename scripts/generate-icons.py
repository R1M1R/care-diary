#!/usr/bin/env python3
"""Generate lightweight PWA icons (always overwrite — safe to re-run)."""
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError as e:
    raise SystemExit(
        "Pillow required: pip install pillow\n"
        "Then run: python scripts/generate-icons.py"
    ) from e

ROOT = Path(__file__).resolve().parent.parent
MAX_ICON_BYTES = 100_000  # fail CI if larger


def draw_heart(draw, cx, cy, s, color):
    draw.ellipse((cx - s, cy - s * 0.4, cx, cy + s * 0.55), fill=color)
    draw.ellipse((cx, cy - s * 0.4, cx + s, cy + s * 0.55), fill=color)
    draw.polygon([(cx - s, cy + s * 0.1), (cx + s, cy + s * 0.1), (cx, cy + s * 1.15)], fill=color)


def make_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (255, 240, 245, 255))
    d = ImageDraw.Draw(img)
    pad = max(12, size // 20)
    d.ellipse((pad, pad, size - pad, size - pad), fill=(232, 50, 90, 255))
    inner = max(pad * 3, size // 5)
    d.ellipse((inner, inner, size - inner, size - inner), fill=(255, 255, 255, 40))
    draw_heart(d, size // 2, int(size * 0.41), max(36, size // 7), (255, 255, 255, 245))
    return img


def main():
    apple = ROOT / "apple-icon.png"
    icon192 = ROOT / "icon-192.png"

    master = make_icon(512)
    master.save(apple, "PNG", optimize=True)
    master.resize((192, 192), Image.LANCZOS).save(icon192, "PNG", optimize=True)

    apple_size = apple.stat().st_size
    icon192_size = icon192.stat().st_size

    print(f"apple-icon.png  {apple_size:,} bytes")
    print(f"icon-192.png    {icon192_size:,} bytes")

    if apple_size > MAX_ICON_BYTES:
        raise SystemExit(f"apple-icon.png too large ({apple_size} > {MAX_ICON_BYTES})")

    print("Icons OK")


if __name__ == "__main__":
    main()
