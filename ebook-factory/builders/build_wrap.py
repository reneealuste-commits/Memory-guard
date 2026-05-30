#!/usr/bin/env python3
"""KDP paperback wrap cover builder (PIL + Ghostscript CMYK)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "books" / "book06_strong_son"))

import meta  # noqa: E402
from shared.constants import KINDLE_COVER_HEIGHT, KINDLE_COVER_WIDTH, WRAP_BLEED, WRAP_TRIM_H, WRAP_TRIM_W
from shared.entities import plain_text
from shared.text_utils import wrap_text

DPI = 300
GOLD = (168, 116, 26)
DARK = (28, 28, 32)
WHITE = (245, 245, 240)


def spine_width_inches(page_count: int) -> float:
    return page_count * 0.002252


def upscale_cover(src: Path, width: int, height: int) -> Image.Image:
    img = Image.open(src).convert("RGB")
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    return img


def get_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    fonts = {
        "serif": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "serif-bold": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "serif-italic": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "sans-bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    }
    key = name.lower().replace(" ", "-")
    if "italic" in key:
        path = fonts["serif-italic"]
    elif "bold" in key and "sans" in key:
        path = fonts["sans-bold"]
    elif "bold" in key:
        path = fonts["serif-bold"]
    elif "sans" in key:
        path = fonts["sans-bold"]
    else:
        path = fonts["serif"]
    return ImageFont.truetype(path, size)


def draw_wrapped(draw, text, font, x, y, max_width, fill, align="left", line_spacing=8):
    lines = wrap_text(draw, plain_text(text), font, max_width)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        tx = x if align == "left" else x - w // 2 if align == "center" else x - w
        draw.text((tx, y), line, font=font, fill=fill)
        y += h + line_spacing
    return y


def build_wrap(front_cover: Path, page_count: int, output_rgb: Path, output_cmyk: Path) -> None:
    bleed = WRAP_BLEED
    trim_w = WRAP_TRIM_W
    trim_h = WRAP_TRIM_H
    spine_in = spine_width_inches(page_count)
    total_w_in = bleed + trim_w + spine_in + trim_w + bleed
    total_h_in = bleed + trim_h + bleed
    W = int(total_w_in * DPI)
    H = int(total_h_in * DPI)
    canvas = Image.new("RGB", (W, H), DARK)
    draw = ImageDraw.Draw(canvas)

    px_per_in = DPI
    back_x0 = int(bleed * px_per_in)
    back_x1 = back_x0 + int(trim_w * px_per_in)
    spine_x1 = back_x1 + int(spine_in * px_per_in)
    front_x0 = spine_x1
    front_x1 = front_x0 + int(trim_w * px_per_in)

    # Back cover text block
    margin = int(0.55 * px_per_in)
    text_w = back_x1 - back_x0 - 2 * margin
    y = int(bleed * px_per_in + 0.85 * px_per_in)

    hook_lines = [
        "Your son is learning manhood from a culture that never asked your permission.",
        "Uncle Al tells you what to do about it.",
    ]
    hook_font = get_font("Serif-Italic", 46)
    for line in hook_lines:
        y = draw_wrapped(draw, line, hook_font, back_x0 + (back_x1 - back_x0) // 2, y, text_w, WHITE, align="center")
    y += 20
    draw.line([(back_x0 + margin, y), (back_x1 - margin, y)], fill=GOLD, width=3)
    y += 28

    body_font = get_font("Serif", 28)
    body_paras = [
        "Between school, screens, and the boys around him, someone is teaching your son what strength looks like, how to treat women, and whether anger is power or poison.",
        "A Strong Son is the final book in The Honest Father Series — fourteen chapters, ten rules in the Son's Code, and zero therapy-speak.",
    ]
    for para in body_paras:
        y = draw_wrapped(draw, para, body_font, back_x0 + margin, y, text_w, WHITE)
        y += 16

    y += 10
    draw.text((back_x0 + margin, y), "INSIDE:", font=get_font("Sans-Bold", 30), fill=GOLD)
    y += 42
    bullets = [
        "Why silence looks like strength but often isn't",
        "How the screen competes for your authority",
        "Discipline that builds men who govern themselves",
        "Talking about sex before the internet does",
        "Launching him without losing him",
    ]
    bullet_font = get_font("Serif", 26)
    for b in bullets:
        draw.ellipse((back_x0 + margin, y + 8, back_x0 + margin + 10, y + 18), fill=GOLD)
        y = draw_wrapped(draw, b, bullet_font, back_x0 + margin + 22, y, text_w - 22, WHITE)
        y += 8

    y += 12
    closer_font = get_font("Serif-Italic", 28)
    y = draw_wrapped(
        draw,
        "The man you are is the man he'll become. Start tonight.",
        closer_font,
        back_x0 + (back_x1 - back_x0) // 2,
        y,
        text_w,
        WHITE,
        align="center",
    )

    series_font = get_font("Sans-Bold", 22)
    draw.text(
        (back_x0 + margin, H - int(bleed * px_per_in + 0.45 * px_per_in)),
        "THE HONEST FATHER SERIES",
        font=series_font,
        fill=GOLD,
    )

    # Spine — blank under 79 pages (dark fill only)
    draw.rectangle([back_x1, 0, spine_x1, H], fill=DARK)

    # Front cover from Kindle art
    front = upscale_cover(front_cover, front_x1 - front_x0, H)
    canvas.paste(front, (front_x0, 0))

    output_rgb.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_rgb, "JPEG", quality=95, dpi=(DPI, DPI))

    # CMYK via Ghostscript if available
    gs = "gs"
    try:
        subprocess.run(
            [
                gs,
                "-dSAFER",
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=pdfwrite",
                "-dPDFSETTINGS=/printer",
                "-sColorConversionStrategy=CMYK",
                "-sProcessColorModel=DeviceCMYK",
                f"-sOutputFile={output_cmyk}",
                str(output_rgb),
            ],
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        # fallback: save RGB PDF via PIL
        canvas.convert("RGB").save(output_cmyk.with_suffix(".rgb.pdf"), "PDF", resolution=DPI)
        output_cmyk.write_bytes(output_rgb.read_bytes())  # copy jpg as fallback marker
        print("Ghostscript unavailable; saved RGB wrap only")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--cover", required=True, type=Path)
    parser.add_argument("--pages", type=int, default=72)
    args = parser.parse_args()
    out_dir = ROOT / "outputs"
    rgb_out = out_dir / f"{meta.OUTPUT_BASENAME}_wrap_rgb.jpg"
    cmyk_out = out_dir / f"{meta.OUTPUT_BASENAME}_wrap_cmyk.pdf"
    build_wrap(args.cover, args.pages, rgb_out, cmyk_out)
    print(f"Wrote {rgb_out} and {cmyk_out}")
