#!/usr/bin/env python3
"""
fig_seed_grid.py -- generates images/01-seed-grid.svg

Purpose:
    Draw the 12-hour BIP39 seed grid: which hours are confirmed by eye, which carry a
    short candidate list because the numeral's row is ambiguous by +/-1 on the
    published raster. Every hour, status, and candidate word comes from
    data/seed-grid.json, not hard-coded here.

Usage:
    python3 tools/fig_seed_grid.py

Input:
    data/seed-grid.json

Output:
    images/01-seed-grid.svg
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "seed-grid.json"
OUT_FILE = ROOT / "images" / "01-seed-grid.svg"

ORANGE = "#E07A1F"  # unknown / candidate
BLUE = "#1F5FBF"    # confirmed
GRAY = "#9A9A9A"
INK = "#222222"


def main() -> None:
    with open(DATA_FILE, encoding="utf-8") as f:
        spec = json.load(f)
    hours = spec["hours"]

    cols, rows = 4, 3
    cell_w, cell_h = 200, 130
    margin = 20
    width = margin * 2 + cols * cell_w
    height = margin * 2 + rows * cell_h + 50

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="DejaVu Sans, sans-serif">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>',
        f'<text x="{margin}" y="30" font-size="18" font-weight="bold" fill="{INK}">'
        f'12-hour seed grid: confirmed word (blue) vs candidates (orange)</text>',
    ]

    for h in hours:
        idx = h["hour"] - 1
        col = idx % cols
        row = idx // cols
        x = margin + col * cell_w
        y = margin + 40 + row * cell_h
        confirmed = h["status"] == "confirmed"
        color = BLUE if confirmed else ORANGE
        parts.append(f'<rect x="{x}" y="{y}" width="{cell_w - 12}" height="{cell_h - 12}" '
                      f'rx="8" fill="none" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="{x + 10}" y="{y + 22}" font-size="14" font-weight="bold" '
                      f'fill="{INK}">hour {h["hour"]}</text>')
        if confirmed:
            parts.append(f'<text x="{x + 10}" y="{y + 48}" font-size="15" fill="{BLUE}">'
                          f'{h["candidates"][0]}</text>')
            parts.append(f'<text x="{x + 10}" y="{y + 68}" font-size="11" fill="{GRAY}">'
                          f'read cleanly by eye</text>')
        else:
            ty = y + 46
            parts.append(f'<text x="{x + 10}" y="{ty - 18}" font-size="11" fill="{GRAY}">'
                          f'{len(h["candidates"])} candidates (+/-1 row):</text>')
            for cand in h["candidates"]:
                parts.append(f'<text x="{x + 10}" y="{ty}" font-size="13" fill="{ORANGE}">{cand}</text>')
                ty += 18

    OUT_FILE.parent.mkdir(exist_ok=True)
    parts.append("</svg>")
    OUT_FILE.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
