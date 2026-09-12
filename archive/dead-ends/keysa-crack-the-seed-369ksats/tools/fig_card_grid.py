#!/usr/bin/env python3
"""
fig_card_grid.py -- generate images/01-annotated-card-grid.png.

Purpose:
    Show the published ciphertext card next to a legend strip that renders the 70
    transcribed tokens, laid out in the same 6 rows of 12/12/11/12/12/11, with the 12
    tokens that carry no trailing dot on the card outlined. This is the "12 dotless
    tokens" set enumerated exhaustively in analysis/tested.md (L-001, 0 match under
    all 479,001,600 orderings).

    Follows the numbered-callout + legend-strip pattern used across this repository
    (see tools/fig_regions.py in blm-brave-new-world-0-2btc): the card's real pixels
    are kept untouched on top; nothing is drawn on the artwork itself. Below it, each
    of the card's 6 transcribed rows gets a small numbered marker (matching the card's
    own line order) followed by its tokens. Every element's width is measured before
    the canvas is sized, so no token or caption can run past the canvas edge.

Usage:
    python3 tools/fig_card_grid.py

Input:
    clues/L9rQ.jpg (the published card, untouched).
    data/card-tokens.txt (my transcription, dots mark tokens with a trailing period).

Output:
    images/01-annotated-card-grid.png
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CARD_PATH = os.path.join(ROOT, "clues", "L9rQ.jpg")
TOKENS_PATH = os.path.join(ROOT, "data", "card-tokens.txt")
OUT_PATH = os.path.join(ROOT, "images", "01-annotated-card-grid.png")

COLOR_MARKER = "#1F5FBF"    # confirmed: row order read directly off the card
COLOR_DOTLESS = "#E07A1F"   # unknown / under test: the 12 dotless tokens
COLOR_TEXT = "#1a1a1a"
COLOR_BG = "#FFFFFF"

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MARGIN = 24
ROW_H = 32
TOKEN_GAP = 14
MARKER_R = 11


def load_rows():
    rows = []
    with open(TOKENS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            tokens = line.split()
            row = [(t.rstrip("."), t.endswith(".")) for t in tokens]
            rows.append(row)
    return rows


def marker(draw, cx, cy, n, font_num):
    r = MARKER_R
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COLOR_MARKER, outline="#FFFFFF", width=2)
    label = str(n)
    bbox = draw.textbbox((0, 0), label, font=font_num)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), label, fill="#FFFFFF", font=font_num)


def main():
    card = Image.open(CARD_PATH).convert("RGB")
    rows = load_rows()

    font = ImageFont.truetype(FONT_PATH, 15)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, 15)
    font_small = ImageFont.truetype(FONT_PATH, 12)
    font_num = ImageFont.truetype(FONT_BOLD_PATH, 13)

    header = "My transcription (data/card-tokens.txt), 70 tokens in 6 rows, numbered in the card's own line order:"
    footnote = (
        "outlined = the 12 tokens with no trailing dot on the card "
        "(L-001, exhausted: 479,001,600 orderings, 0 match)"
    )
    row_text_x0 = MARGIN + 2 * MARKER_R + 14

    # Measuring pass: figure out the widest element so the canvas is sized to fit
    # everything with no clipping, instead of guessing a fixed width.
    probe = Image.new("RGB", (10, 10))
    pdraw = ImageDraw.Draw(probe)
    max_w = pdraw.textbbox((MARGIN, 0), header, font=font_bold)[2]
    max_w = max(max_w, pdraw.textbbox((MARGIN, 0), footnote, font=font_small)[2])
    row_widths = []
    for row in rows:
        x = row_text_x0
        for word, dotted in row:
            w = pdraw.textbbox((x, 0), word, font=font)[2] - x
            x += w + TOKEN_GAP
        row_widths.append(x)
    max_w = max(max_w, max(row_widths))

    legend_top = card.height + 20
    legend_h = 30 + len(rows) * ROW_H + 36
    width = max(card.width, max_w + MARGIN)
    height = legend_top + legend_h

    canvas = Image.new("RGB", (width, height), COLOR_BG)
    canvas.paste(card, ((width - card.width) // 2, 0))
    draw = ImageDraw.Draw(canvas)

    y = legend_top
    draw.text((MARGIN, y), header, font=font_bold, fill=COLOR_TEXT)
    y += 30

    for i, row in enumerate(rows, 1):
        marker(draw, MARGIN + MARKER_R, y + 8, i, font_num)
        x = row_text_x0
        for word, dotted in row:
            color = COLOR_TEXT if dotted else COLOR_DOTLESS
            bbox = draw.textbbox((x, y), word, font=font)
            w = bbox[2] - bbox[0]
            if not dotted:
                draw.rounded_rectangle(
                    [x - 3, y - 2, x + w + 3, y + 16], radius=4, outline=COLOR_DOTLESS, width=2
                )
            draw.text((x, y), word, font=font, fill=color)
            x += w + TOKEN_GAP
        y += ROW_H

    y += 8
    draw.rectangle([MARGIN, y, MARGIN + 14, y + 14], outline=COLOR_DOTLESS, width=2)
    draw.text((MARGIN + 22, y - 1), footnote, font=font_small, fill=COLOR_TEXT)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    canvas.save(OUT_PATH, "PNG", optimize=True)
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes), size {canvas.size}")


if __name__ == "__main__":
    main()
