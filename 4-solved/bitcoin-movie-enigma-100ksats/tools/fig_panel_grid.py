#!/usr/bin/env python3
"""
fig_panel_grid.py -- generate images/02-panel-grid-identification.svg.

Purpose:
    Draw the 34 movie panels as a grid of numbered slots, colored by identification
    confidence (confirmed, probable or uncertain, unidentified, or disputed between
    two candidates). This does not reproduce any movie still; it is a status diagram
    over panel numbers only.

Usage:
    python3 tools/fig_panel_grid.py

Input:
    data/films.csv (panel, title, mpaa, confidence, candidate_bip39_words).

Output:
    images/02-panel-grid-identification.svg
"""

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_PATH = os.path.join(ROOT, "data", "films.csv")
OUT_PATH = os.path.join(ROOT, "images", "02-panel-grid-identification.svg")

COLS = 6
CELL = 90
GAP = 8
MARGIN = 30
FONT = "DejaVu Sans"

COLOR_CONFIRMED = "#1F5FBF"
COLOR_UNCERTAIN = "#E07A1F"
COLOR_UNKNOWN = "#9A9A9A"
COLOR_TEXT_ON_DARK = "#FFFFFF"
COLOR_TEXT = "#1a1a1a"
COLOR_BG = "#FFFFFF"

COLOR_BY_CONFIDENCE = {
    "confirmed": COLOR_CONFIRMED,
    "confirmed-community": COLOR_CONFIRMED,
    "probable": COLOR_UNCERTAIN,
    "uncertain": COLOR_UNCERTAIN,
    "disputed": COLOR_UNCERTAIN,
    "unidentified": COLOR_UNKNOWN,
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, width=13):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def main():
    rows = []
    with open(DATA_PATH, encoding="utf-8", newline="") as f:
        lines = [line for line in f if not line.lstrip().startswith("#")]
    for row in csv.DictReader(lines):
        rows.append(row)

    n = len(rows)
    n_rows = -(-n // COLS)
    width = MARGIN * 2 + COLS * CELL + (COLS - 1) * GAP
    height = MARGIN * 2 + n_rows * CELL + (n_rows - 1) * GAP + 50

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}">'
    )
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="{COLOR_BG}"/>')

    for idx, row in enumerate(rows):
        r, c = divmod(idx, COLS)
        x = MARGIN + c * (CELL + GAP)
        y = MARGIN + r * (CELL + GAP)
        conf = row["confidence"]
        color = COLOR_BY_CONFIDENCE.get(conf, COLOR_UNKNOWN)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="6" '
            f'fill="{color}" stroke="#333333" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x + 6}" y="{y + 16}" font-size="11" font-weight="bold" '
            f'fill="{COLOR_TEXT_ON_DARK}">#{row["panel"]}</text>'
        )
        title = row["title"]
        if conf == "disputed":
            title_lines = ["disputed:", "2 candidates"]
        elif conf == "unidentified":
            title_lines = ["unidentified"]
        else:
            title_lines = wrap(title, 13)[:4]
        for li, line in enumerate(title_lines):
            parts.append(
                f'<text x="{x + 6}" y="{y + 32 + li * 12}" font-size="9" '
                f'fill="{COLOR_TEXT_ON_DARK}">{esc(line)}</text>'
            )

    legend_y = MARGIN + n_rows * (CELL + GAP) + 10
    legend_items = [
        (COLOR_CONFIRMED, "confirmed"),
        (COLOR_UNCERTAIN, "probable / uncertain / disputed"),
        (COLOR_UNKNOWN, "unidentified"),
    ]
    lx = MARGIN
    for color, label in legend_items:
        parts.append(f'<rect x="{lx}" y="{legend_y}" width="14" height="14" fill="{color}"/>')
        parts.append(
            f'<text x="{lx + 20}" y="{legend_y + 11}" font-size="10" fill="{COLOR_TEXT}">{esc(label)}</text>'
        )
        lx += 20 + len(label) * 6 + 30

    parts.append("</svg>")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes)")


if __name__ == "__main__":
    main()
