#!/usr/bin/env python3
"""
fig_prize_bars.py -- generates assets/prize-map.svg for the root README.

A dark-theme horizontal bar chart of the biggest unsolved prizes (status open or watch),
valued in USD at live prices, one bar per puzzle, coloured by chain, with the native amount
and the USD value on each bar. Prices come from CoinGecko at run time (no key); a scheduled
GitHub Actions job re-runs this daily so the picture follows the market. Escrow balances
are the ones recorded in each folder's puzzle.json (re-checked by tools/check_escrows.py).

Usage:
    python3 tools/fig_prize_bars.py                 # fetch live prices, write the SVG
    python3 tools/fig_prize_bars.py --prices p.json # use a saved {"BTC": 77378, ...} file
    python3 tools/fig_prize_bars.py --offline       # use the snapshot prices in build_index.py
"""
import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "puzzles.json"
OUT = ROOT / "assets" / "prize-map.svg"
sys.path.insert(0, str(ROOT / "tools"))

COINGECKO = ("https://api.coingecko.com/api/v3/simple/price"
             "?ids=bitcoin,ethereum,litecoin,arweave,solana,tether,usd-coin&vs_currencies=usd")
GECKO_IDS = {"BTC": "bitcoin", "ETH": "ethereum", "LTC": "litecoin", "AR": "arweave",
             "SOL": "solana", "USDT": "tether", "USDC": "usd-coin"}

SURFACE = "#0d1117"
PANEL = "#161b22"
INK = "#f0f6fc"
MUTED = "#8b949e"
GRID = "#30363d"
CHAIN_COLOR = {"bitcoin": "#f7931a", "ethereum": "#8b9cf7", "base": "#3987e5", "arweave": "#199e70",
               "litecoin": "#c9d1d9", "solana": "#d55181", "none": "#6e7681"}

SHORT = {
    "gsmg-io-5btc-puzzle": "GSMG.io",
    "ballet-bobby-lee-2btc-cards": "Ballet cards (Bobby Lee)",
    "bitaps-shamir-challenge-1btc": "Bitaps Shamir",
    "aoi-nakamoto-quizchain-0-854btc": "Aoi Nakamoto Quizchain",
    "peter-todd-hash-collision-bounties-0-59btc": "Peter Todd bounties",
    "guntis-vitolins-metamask-8-6eth": "Guntis Vitolins",
    "blm-brave-new-world-0-2btc": "BLM collage",
    "teikhos-bipedaljoe-solver-bounties-2eth": "TeikhosBounty",
    "arweave-puzzle-11-1eth": "Arweave #11",
    "smith-lyle-moore-hunt-2-0-032btc": "Smith, Lyle & Moore #2",
    "wealth-in-poetry-0-03btc": "Wealth in Poetry",
    "fe-lang-bountiful-compiler-bounty-1eth": "Fe compiler bounty",
    "arweave-puzzle-3-1000ar": "Arweave #3",
    "logicbeach-powerful-moss-0-54eth": "LogicBeach",
    "path-to-greatness-treasure-hunt-3ltc": "Path to Greatness",
}


def short_name(p):
    slug = (p.get("folder") or "").split("/")[-1]
    if slug in SHORT:
        return SHORT[slug]
    t = p["title"]
    for sep in (":", " - ", " / "):
        if sep in t:
            t = t.split(sep)[0]
    return t.strip()[:26]


def fetch_prices():
    with urllib.request.urlopen(COINGECKO, timeout=30) as r:
        data = json.load(r)
    return {sym: float(data[gid]["usd"]) for sym, gid in GECKO_IDS.items() if gid in data}


def snapshot_prices():
    from build_index import PRICE_SNAPSHOT
    p = dict(PRICE_SNAPSHOT)
    p.pop("date", None)
    p.setdefault("USDT", 1.0)
    p.setdefault("USDC", 1.0)
    return p


def native_amount(prize):
    amt = float(prize.get("amount") or 0)
    asset = prize.get("asset", "")
    if asset == "sats":
        return amt / 1e8, "BTC"
    return amt, asset


def usd_value(prize, prices):
    amt, asset = native_amount(prize)
    if asset not in prices:
        return None
    return amt * prices[asset]


def fmt_native(amt, asset):
    if asset == "BTC":
        return f"{amt:.4f} BTC" if amt < 1 else f"{amt:.2f} BTC"
    if asset in ("ETH", "LTC", "SOL"):
        return f"{amt:.2f} {asset}"
    if asset in ("USDT", "USDC"):
        return f"{amt:,.0f} {asset}"
    return f"{amt:,.0f} {asset}"


def fmt_usd(v):
    if v >= 1_000_000:
        return f"${v/1e6:.2f}M"
    if v >= 10_000:
        return f"${v/1000:.0f}k"
    if v >= 1000:
        return f"${v/1000:.1f}k"
    return f"${v:.0f}"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(rows, others, total, n_funded, prices, when, source):
    W = 1000
    top = 146
    row_h = 34
    n = len(rows) + (1 if others else 0)
    H = top + n * row_h + 78
    label_w = 235
    bar_x = label_w + 16
    bar_max = W - bar_x - 150
    vmax = max(r[2] for r in rows) if rows else 1.0
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">',
           f'<rect width="{W}" height="{H}" rx="12" fill="{SURFACE}"/>',
           f'<text x="32" y="44" fill="{INK}" font-size="22" font-weight="700">Where the unsolved prize money sits</text>',
           f'<text x="32" y="70" fill="{MUTED}" font-size="14">{esc(fmt_usd(total))} across {n_funded} funded puzzles, '
           f'valued at {source} prices on {when}. Balances are the ones recorded in each folder.</text>']
    # price strip
    x = 32
    for sym in ("BTC", "ETH", "LTC", "AR", "SOL"):
        if sym in prices:
            label = f"{sym} ${prices[sym]:,.0f}" if prices[sym] >= 100 else f"{sym} ${prices[sym]:,.2f}"
            out.append(f'<rect x="{x}" y="84" width="{len(label)*8+18}" height="22" rx="11" fill="{PANEL}" stroke="{GRID}"/>')
            out.append(f'<text x="{x+9}" y="99" fill="{INK}" font-size="12" font-weight="600">{esc(label)}</text>')
            x += len(label) * 8 + 28
    # grid lines at 25 / 50 / 75 / 100 percent of vmax
    for k in (0.25, 0.5, 0.75, 1.0):
        gx = bar_x + bar_max * k
        out.append(f'<line x1="{gx:.0f}" y1="{top-8}" x2="{gx:.0f}" y2="{top + n*row_h}" stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<text x="{gx:.0f}" y="{top-14}" fill="{MUTED}" font-size="11" text-anchor="middle">{esc(fmt_usd(vmax*k))}</text>')
    y = top
    for name, native, v, chain in rows:
        w = max(4, bar_max * v / vmax)
        col = CHAIN_COLOR.get(chain, CHAIN_COLOR["none"])
        out.append(f'<text x="{label_w}" y="{y+22}" fill="{INK}" font-size="14" text-anchor="end">{esc(name)}</text>')
        out.append(f'<rect x="{bar_x}" y="{y+6}" width="{w:.1f}" height="22" rx="6" fill="{col}" opacity="0.92"/>')
        out.append(f'<text x="{bar_x + w + 10:.1f}" y="{y+22}" fill="{INK}" font-size="13" font-weight="600">{esc(fmt_usd(v))}</text>')
        out.append(f'<text x="{bar_x + w + 10 + len(fmt_usd(v))*8.5 + 6:.1f}" y="{y+22}" fill="{MUTED}" font-size="12">{esc(native)}</text>')
        y += row_h
    if others:
        cnt, v = others
        w = max(4, bar_max * v / vmax)
        out.append(f'<text x="{label_w}" y="{y+22}" fill="{MUTED}" font-size="14" text-anchor="end">{cnt} smaller puzzles</text>')
        out.append(f'<rect x="{bar_x}" y="{y+6}" width="{w:.1f}" height="22" rx="6" fill="{CHAIN_COLOR["none"]}" opacity="0.9"/>')
        out.append(f'<text x="{bar_x + w + 10:.1f}" y="{y+22}" fill="{INK}" font-size="13" font-weight="600">{esc(fmt_usd(v))}</text>')
        y += row_h
    # legend
    lx = 32
    ly = H - 30
    for chain, col in (("bitcoin", "Bitcoin"), ("ethereum", "Ethereum"), ("base", "Base"), ("arweave", "Arweave"), ("litecoin", "Litecoin")):
        out.append(f'<rect x="{lx}" y="{ly-11}" width="12" height="12" rx="3" fill="{CHAIN_COLOR[chain]}"/>')
        out.append(f'<text x="{lx+18}" y="{ly}" fill="{MUTED}" font-size="12">{col}</text>')
        lx += 18 + len(col) * 7.5 + 22
    out.append(f'<text x="{W-32}" y="{ly}" fill="{MUTED}" font-size="12" text-anchor="end">tools/fig_prize_bars.py, refreshed daily</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prices", help="JSON file {\"BTC\": 77378, ...}")
    ap.add_argument("--offline", action="store_true", help="use the snapshot prices from build_index.py")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if a.prices:
        prices = {k: float(v) for k, v in json.load(open(a.prices)).items()}
        source = "saved"
    elif a.offline:
        prices = snapshot_prices()
        source = "snapshot"
    else:
        try:
            prices = fetch_prices()
            source = "CoinGecko"
        except Exception as exc:  # noqa: BLE001
            print(f"price fetch failed ({exc}); using snapshot prices", file=sys.stderr)
            prices = snapshot_prices()
            source = "snapshot"
    doc = json.load(open(INDEX, encoding="utf-8"))
    funded = [p for p in doc["puzzles"] if p.get("status") in ("open", "watch")]
    valued = []
    for p in funded:
        v = usd_value(p["prize"], prices)
        if v is None:
            continue
        amt, asset = native_amount(p["prize"])
        valued.append((short_name(p), fmt_native(amt, asset), v, p.get("chain", "none")))
    valued.sort(key=lambda r: -r[2])
    rows = valued[: a.top]
    rest = valued[a.top:]
    others = (len(rest), sum(r[2] for r in rest)) if rest else None
    total = sum(r[2] for r in valued)
    when = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    svg = render(rows, others, total, len(funded), prices, when, source)
    Path(a.out).write_text(svg, encoding="utf-8")
    print(f"wrote {a.out}: {len(rows)} bars, total {fmt_usd(total)} at {source} prices ({when})")


if __name__ == "__main__":
    main()
