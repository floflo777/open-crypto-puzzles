#!/usr/bin/env python3
"""
fig_coverage.py -- generate images/02-coverage-tested-space.png.

Purpose:
    Draw a horizontal, log-scale bar chart of the hypothesis families tested against
    the Keysa selection rule, sized by how many objects each family enumerated. Bars
    are colored by whether a witness (a known-good input recovered through the same
    code path) confirmed the family's negative result, or whether it remains
    uncertified.

Usage:
    python3 tools/fig_coverage.py

Input:
    data/coverage.csv (family, count, unit, witness, date).

Output:
    images/02-coverage-tested-space.png
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_PATH = os.path.join(ROOT, "data", "coverage.csv")
OUT_PATH = os.path.join(ROOT, "images", "02-coverage-tested-space.png")

COLOR_WITNESSED = "#9A9A9A"   # tested negative, confirmed
COLOR_UNCERTIFIED = "#E07A1F"  # unknown reliability (no witness)


def main():
    rows = []
    with open(DATA_PATH, encoding="utf-8", newline="") as f:
        lines = [line for line in f if not line.lstrip().startswith("#")]
    for row in csv.DictReader(lines, delimiter=",", skipinitialspace=True):
        rows.append(row)

    rows.sort(key=lambda r: int(r["count"]))

    labels = [f'{r["family"]} ({r["unit"]})' for r in rows]
    counts = [int(r["count"]) for r in rows]
    colors = [
        COLOR_WITNESSED if r["witness"] == "witnessed" else COLOR_UNCERTIFIED for r in rows
    ]

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(9, 3.2), dpi=150)
    bars = ax.barh(labels, counts, color=colors)
    ax.set_xscale("log")
    ax.set_xlabel("objects enumerated (log scale)")
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")

    for bar, count, r in zip(bars, counts, rows):
        ax.text(
            bar.get_width() * 1.15,
            bar.get_y() + bar.get_height() / 2,
            f"{count:,} -- 0 match ({r['witness']})",
            va="center",
            fontsize=8,
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes)")


if __name__ == "__main__":
    main()
