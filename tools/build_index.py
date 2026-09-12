#!/usr/bin/env python3
"""
build_index.py -- generate the machine-readable index and the generated README tables.

Purpose:
    Walk every <tier>/<slug>/puzzle.json plus archive/dead-ends/rows.json, concatenate them into
    the root puzzles.json, and rewrite the generated table blocks (between
    <!-- generated:start --> and <!-- generated:end -->) in the root README.md and in each
    tier's README.md. Also fills in the "Snapshot: <N> puzzles, <M> still funded, about $<USD>
    at stake" line in the root README.md.

Usage (run from the repository root):
    python3 tools/build_index.py            # write puzzles.json and rewrite generated blocks
    python3 tools/build_index.py --check     # exit 1 if regenerating would change any file

Input:
    <tier-folder>/<slug>/puzzle.json for every puzzle folder.
    archive/dead-ends/rows.json for dead ends that have no folder of their own.

Output:
    puzzles.json at the repository root.
    The generated block of README.md at the repository root.
    The generated block of README.md in each tier folder.
"""

import argparse
import json
import os
import re
import sys
from datetime import date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRICE_SNAPSHOT = {"date": "2026-08-16", "BTC": 63000, "ETH": 1880, "AR": 1.81, "LTC": 54}

TIERS = [
    ("1-big-prizes", "big"),
    ("2-mid-prizes", "mid"),
    ("3-small-prizes", "small"),
    ("4-solved", "solved"),
    ("archive/dead-ends", "dead-end"),
]

GENERATED_START = "<!-- generated:start -->"
TOTALS_START = "<!-- totals:start -->"
TOTALS_END = "<!-- totals:end -->"
GENERATED_END = "<!-- generated:end -->"

BIG_MID_SMALL_HEADER = "| Puzzle | Prize | USD | Chain | Type | What remains | Escrow checked | Status |\n|---|---|---|---|---|---|---|---|"
SOLVED_HEADER = "| Puzzle | Cashed | Payout tx | Date | Series lesson |\n|---|---|---|---|---|"
DEAD_END_HEADER = "| Puzzle | Announced | Why | Verified | Lesson |\n|---|---|---|---|---|"


def load_puzzles():
    """Return the list of every puzzle manifest, folder-based and row-only, each with a
    "folder" key (a relative path, or None for row-only dead ends)."""
    puzzles = []
    for folder_prefix, _tier in TIERS:
        tier_dir = os.path.join(REPO_ROOT, folder_prefix)
        if not os.path.isdir(tier_dir):
            continue
        for entry in sorted(os.listdir(tier_dir)):
            entry_dir = os.path.join(tier_dir, entry)
            manifest_path = os.path.join(entry_dir, "puzzle.json")
            if os.path.isdir(entry_dir) and os.path.isfile(manifest_path):
                with open(manifest_path, encoding="utf-8") as f:
                    manifest = json.load(f)
                manifest = dict(manifest)
                manifest["folder"] = f"{folder_prefix}/{entry}"
                puzzles.append(manifest)

    rows_path = os.path.join(REPO_ROOT, "archive/dead-ends", "rows.json")
    if os.path.isfile(rows_path):
        with open(rows_path, encoding="utf-8") as f:
            rows_doc = json.load(f)
        for row in rows_doc.get("rows", []):
            row = dict(row)
            row["folder"] = None
            puzzles.append(row)

    return puzzles


def build_counts(puzzles):
    counts = {"big": 0, "mid": 0, "small": 0, "solved": 0, "dead-end": 0}
    for p in puzzles:
        tier = p.get("tier")
        if tier in counts:
            counts[tier] += 1
    return counts


def build_index_doc(puzzles):
    return {
        "schema_version": 1,
        "generated_on": PRICE_SNAPSHOT["date"],
        "price_snapshot": PRICE_SNAPSHOT,
        "counts": build_counts(puzzles),
        "puzzles": puzzles,
    }


def fmt_usd(value):
    if not isinstance(value, (int, float)):
        return ""
    return f"{value:,.0f}" if value == int(value) else f"{value:,.2f}"


def fmt_prize(prize):
    amount = prize.get("amount")
    asset = prize.get("asset", "")
    if amount is None:
        return ""
    if isinstance(amount, float) and amount == int(amount):
        amount_str = f"{int(amount):,}"
    elif isinstance(amount, (int, float)):
        amount_str = f"{amount:,}"
    else:
        amount_str = str(amount)
    return f"{amount_str} {asset}".strip()


def last_verified(p):
    dates = [a.get("verified_on") for a in p.get("addresses", []) if a.get("verified_on")]
    return max(dates) if dates else p.get("last_updated", "")


def puzzle_link(p, tier_relative=False):
    title = p.get("title") or p.get("slug", "")
    folder = p.get("folder")
    if folder:
        target = os.path.basename(folder) if tier_relative else folder
        return f"[{title}]({target}/)"
    return title


def sort_key_usd_desc(p):
    usd = p.get("prize", {}).get("usd_estimate")
    # None sorts last: use a flag then negative value for descending order.
    if not isinstance(usd, (int, float)):
        return (1, 0)
    return (0, -usd)


def row_big_mid_small(p, tier_relative=False):
    prize = p.get("prize", {})
    return "| {link} | {prize} | {usd} | {chain} | {types} | {remains} | {checked} | {status} |".format(
        link=puzzle_link(p, tier_relative),
        prize=fmt_prize(prize),
        usd=fmt_usd(prize.get("usd_estimate")),
        chain=p.get("chain", ""),
        types=", ".join(p.get("puzzle_type", [])),
        remains=p.get("difficulty_left", ""),
        checked=last_verified(p),
        status=p.get("status", ""),
    )


def row_solved(p, tier_relative=False):
    solutions = p.get("solutions", [])
    sol = solutions[0] if solutions else {}
    payout_txid = sol.get("payout_txid", "")
    explorer = sol.get("explorer", "")
    payout_link = f"[{payout_txid}]({explorer})" if payout_txid and explorer else payout_txid
    return "| {link} | {cashed} | {tx} | {date} | {lesson} |".format(
        link=puzzle_link(p, tier_relative),
        cashed=sol.get("payout_amount", ""),
        tx=payout_link,
        date=sol.get("date", ""),
        lesson=p.get("difficulty_note", ""),
    )


def row_dead_end(p, tier_relative=False):
    prize = p.get("prize", {})
    return "| {link} | {announced} | {why} | {verified} | {lesson} |".format(
        link=puzzle_link(p, tier_relative),
        announced=fmt_prize(prize),
        why=p.get("dead_end_reason", ""),
        verified=last_verified(p),
        lesson=p.get("difficulty_note", ""),
    )


def build_table(puzzles, tier, header, row_fn, empty_note, tier_relative=False):
    rows = [p for p in puzzles if p.get("tier") == tier]
    rows.sort(key=sort_key_usd_desc)
    if not rows:
        return f"{header}\n\n_{empty_note}_"
    lines = [header] + [row_fn(p, tier_relative) for p in rows]
    return "\n".join(lines)


def build_totals_block(puzzles):
    funded = [p for p in puzzles if p.get("status") in ("open", "watch")]
    btc = eth = ar = ltc = usdt = usdc = 0.0
    usd = 0.0
    for p in funded:
        pr = p.get("prize", {})
        amt = pr.get("amount") or 0
        a = pr.get("asset")
        if a == "BTC": btc += amt
        elif a == "sats": btc += amt / 1e8
        elif a == "ETH": eth += amt
        elif a == "AR": ar += amt
        elif a == "LTC": ltc += amt
        elif a == "USDT": usdt += amt
        elif a == "USDC": usdc += amt
        u = pr.get("usd_estimate")
        if isinstance(u, (int, float)): usd += u

    def rnd(v):
        if v >= 10000: return f"${round(v, -3):,.0f}"
        return f"${round(v, -2):,.0f}"

    def usd_for(asset_amt, per):
        return rnd(asset_amt * per)

    p = PRICE_SNAPSHOT
    rows = [
        "| Asset | Locked in unsolved puzzles | Approx. value |",
        "|---|---|---|",
        f"| Bitcoin | {btc:,.2f} BTC | {usd_for(btc, p['BTC'])} |",
        f"| Ethereum | {eth:,.2f} ETH | {usd_for(eth, p['ETH'])} |",
        f"| Arweave | {ar:,.0f} AR | {usd_for(ar, p['AR'])} |",
        f"| Litecoin | {ltc:,.2f} LTC | {usd_for(ltc, p['LTC'])} |",
        f"| Stablecoins | {usdt:,.0f} USDT + {usdc:,.0f} USDC | {rnd(usdt + usdc)} |",
        f"| **Total** | **across {len(funded)} funded puzzles** | **{rnd(usd)}** |",
    ]
    note = (f"\n\nChecked {p['date']} at BTC ${p['BTC']:,}, ETH ${p['ETH']:,}, AR ${p['AR']}. "
            "Prices and balances move; verify each escrow yourself.")
    return "\n".join(rows) + note


def build_root_block(puzzles):
    parts = [
        "## Big prizes (>= $10,000)\n",
        build_table(puzzles, "big", BIG_MID_SMALL_HEADER, row_big_mid_small, "No puzzles in this tier yet."),
        "\n\n## Mid prizes ($100 to $10,000)\n",
        build_table(puzzles, "mid", BIG_MID_SMALL_HEADER, row_big_mid_small, "No puzzles in this tier yet."),
        "\n\n## Small prizes (< $100)\n",
        build_table(puzzles, "small", BIG_MID_SMALL_HEADER, row_big_mid_small, "No puzzles in this tier yet."),
        "\n\n## Solved and cashed\n",
        build_table(puzzles, "solved", SOLVED_HEADER, row_solved, "None yet."),
    ]
    return "".join(parts)


def build_tier_block(puzzles, tier):
    if tier in ("big", "mid", "small"):
        return build_table(puzzles, tier, BIG_MID_SMALL_HEADER, row_big_mid_small, "No puzzles in this tier yet.", tier_relative=True)
    if tier == "solved":
        return build_table(puzzles, tier, SOLVED_HEADER, row_solved, "None yet.", tier_relative=True)
    return build_table(puzzles, tier, DEAD_END_HEADER, row_dead_end, "None logged yet.", tier_relative=True)


def replace_named_block(text, start_marker, end_marker, new_block):
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end < start:
        return text
    before = text[: start + len(start_marker)]
    after = text[end:]
    return f"{before}\n{new_block}\n{after}"


def replace_generated_block(text, new_block):
    start = text.find(GENERATED_START)
    end = text.find(GENERATED_END)
    if start == -1 or end == -1 or end < start:
        raise ValueError("generated block markers not found or out of order")
    before = text[: start + len(GENERATED_START)]
    after = text[end:]
    return f"{before}\n{new_block}\n{after}"


def compute_snapshot_numbers(puzzles):
    n_total = len(puzzles)
    funded = [p for p in puzzles if p.get("status") in ("open", "watch")]
    m_funded = len(funded)
    usd_total = 0
    for p in funded:
        usd = p.get("prize", {}).get("usd_estimate")
        if isinstance(usd, (int, float)):
            usd_total += usd
    return n_total, m_funded, usd_total


def replace_snapshot_line(text, n_total, m_funded, usd_total):
    new_line = (
        f"Snapshot: {n_total} puzzles, {m_funded} still funded, about ${usd_total:,.0f} at stake "
        f"(BTC ${PRICE_SNAPSHOT['BTC']:,}, ETH ${PRICE_SNAPSHOT['ETH']:,}, "
        f"AR ${PRICE_SNAPSHOT['AR']} on {PRICE_SNAPSHOT['date']}). Last escrow checks: see each table."
    )
    # The paragraph may wrap across more than one source line; replace through to the
    # next blank line (or end of file) so no orphan continuation line is left behind.
    pattern = re.compile(r"^Snapshot:.*?(?=\n\n|\Z)", re.MULTILINE | re.DOTALL)
    if not pattern.search(text):
        return text  # front page manages its own totals; nothing to replace
    return pattern.sub(lambda _m: new_line, text, count=1)


def process_readme(path, new_block, check, changed_files, is_root=False, snapshot_args=None):
    with open(path, encoding="utf-8") as f:
        original = f.read()
    updated = replace_generated_block(original, new_block)
    if is_root:
        updated = replace_snapshot_line(updated, *snapshot_args[:3])
        updated = replace_named_block(updated, TOTALS_START, TOTALS_END, snapshot_args[3])
    if updated != original:
        changed_files.append(path)
        if not check:
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated)


def main():
    parser = argparse.ArgumentParser(description="Build puzzles.json and the generated README tables.")
    parser.add_argument("--check", action="store_true", help="exit 1 if regenerating would change any file; do not write")
    args = parser.parse_args()

    puzzles = load_puzzles()
    index_doc = build_index_doc(puzzles)
    index_json = json.dumps(index_doc, indent=2, ensure_ascii=False, sort_keys=False) + "\n"

    changed_files = []

    puzzles_json_path = os.path.join(REPO_ROOT, "puzzles.json")
    existing_json = ""
    if os.path.isfile(puzzles_json_path):
        with open(puzzles_json_path, encoding="utf-8") as f:
            existing_json = f.read()
    if existing_json != index_json:
        changed_files.append(puzzles_json_path)
        if not args.check:
            with open(puzzles_json_path, "w", encoding="utf-8") as f:
                f.write(index_json)

    root_readme = os.path.join(REPO_ROOT, "README.md")
    root_block = build_root_block(puzzles)
    snapshot_numbers = compute_snapshot_numbers(puzzles) + (build_totals_block(puzzles),)
    process_readme(root_readme, root_block, args.check, changed_files, is_root=True, snapshot_args=snapshot_numbers)

    for folder_prefix, tier in TIERS:
        tier_readme = os.path.join(REPO_ROOT, folder_prefix, "README.md")
        if not os.path.isfile(tier_readme):
            continue
        tier_block = build_tier_block(puzzles, tier)
        process_readme(tier_readme, tier_block, args.check, changed_files)

    if args.check:
        if changed_files:
            print("STALE: regenerating would change:")
            for path in changed_files:
                print(f"  {os.path.relpath(path, REPO_ROOT)}")
            sys.exit(1)
        print("OK: puzzles.json and all generated README blocks are up to date.")
        sys.exit(0)

    print(f"Wrote {os.path.relpath(puzzles_json_path, REPO_ROOT)} and updated {len(changed_files)} file(s).")
    for path in changed_files:
        print(f"  {os.path.relpath(path, REPO_ROOT)}")


if __name__ == "__main__":
    main()
