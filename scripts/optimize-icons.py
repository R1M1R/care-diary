#!/usr/bin/env python3
"""Optimize apple-icon.png for PWA — keeps the original artwork, only resizes/compresses."""
from pathlib import Path

try:
    from PIL import Image
except ImportError as e:
    raise SystemExit("Pillow required: pip install pillow") from e

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "apple-icon.source.png"
APPLE = ROOT / "apple-icon.png"
MAX_BYTES = 500_000


def optimize(src: Image.Image) -> None:
    apple = src.resize((512, 512), Image.LANCZOS)
    apple.save(APPLE, "PNG", optimize=True)
    size = APPLE.stat().st_size
    print(f"apple-icon.png  {size:,} bytes (512×512)")
    if size > MAX_BYTES:
        raise SystemExit(f"apple-icon.png still too large ({size} > {MAX_BYTES})")


def main():
    if SOURCE.exists():
        src = Image.open(SOURCE).convert("RGBA")
    elif APPLE.exists():
        src = Image.open(APPLE).convert("RGBA")
        if src.size[0] > 512:
            print(f"Resizing from {src.size[0]}×{src.size[1]} …")
    else:
        raise SystemExit("apple-icon.png or apple-icon.source.png not found")

    optimize(src)
    print("Icon optimized (original design preserved)")


if __name__ == "__main__":
    main()
