#!/usr/bin/env python3
"""Upscale Kindle cover to KDP spec (1600x2560 JPG)."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageFilter

from shared.constants import KINDLE_COVER_HEIGHT, KINDLE_COVER_WIDTH


def upscale_cover(src: Path, dest: Path) -> None:
    img = Image.open(src).convert("RGB")
    img = img.resize((KINDLE_COVER_WIDTH, KINDLE_COVER_HEIGHT), Image.Resampling.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=92, optimize=True)
    print(f"Wrote {dest} ({KINDLE_COVER_WIDTH}x{KINDLE_COVER_HEIGHT})")


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(ROOT / "books" / "book06_strong_son"))
    import meta

    src = Path("/opt/cursor/artifacts/assets/06_a_strong_son_kindle_cover_source.png")
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
    dest = ROOT / "outputs" / f"{meta.OUTPUT_BASENAME}_kindle_cover.jpg"
    upscale_cover(src, dest)
