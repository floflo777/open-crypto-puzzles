#!/usr/bin/env python3
"""
validate.py -- QA runner for open-crypto-puzzles (blueprint section 9).

Purpose:
    Run the automated checks a puzzle folder (or the whole repository) must pass before
    publication: manifest schema, README heading order, forbidden characters and words,
    link and cross-reference sanity, file size and file type limits, oracle self-tests,
    figure bookkeeping, date sanity, and index consistency. French leftovers are reported
    as warnings, never as failures, since quoted French source material is expected.

Usage (run from the repository root):
    python3 tools/validate.py                  # whole repository
    python3 tools/validate.py --folder <path>   # one folder only (repo-relative or absolute)

Input:
    The repository tree, or one folder given by --folder.

Output:
    One PASS/FAIL/WARN line per check, with file:line references for failures. Exit code 1
    if any check fails; exit code 0 if every check passes (warnings do not affect the exit
    code).
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from urllib.parse import urlparse

try:
    import jsonschema
except ImportError:
    jsonschema = None

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(REPO_ROOT, "schema", "puzzle.schema.json")
TODAY = date.today().isoformat()
ROOT_SNAPSHOT_DATE = "2026-08-16"

TIER_DIR_TO_KEY = {
    "1-big-prizes": "big",
    "2-mid-prizes": "mid",
    "3-small-prizes": "small",
    "4-solved": "solved",
    "archive/dead-ends": "dead-end",
}

STATUS_BADGE = {
    "open": "[OPEN]",
    "watch": "[WATCH]",
    "solved": "[SOLVED]",
    "dead-end": "[DEAD END]",
}

BASE_HEADINGS = [
    "## At a glance",
    "## The puzzle as published",
    "## What is understood",
    "## What has been tested",
    "## Open leads, ranked",
    "## Files in this folder",
    "## Sources",
]

FORBIDDEN_CHARS_PATTERN = re.compile(
    "[\u2013\u2014\u2026\u201C\u201D\u2018\u2019\u00A0\u2190-\u21FF"
    "\U0001F300-\U0001FAFF\u2600-\u27BF]"
)

# Section 5.2 style words, plus the section 9.4 jargon/tool-name list.
FORBIDDEN_WORDS = [
    "delve", "worth noting", "it's worth", "tapestry", "realm", "landscape", "navigate",
    "journey", "unlock", "embark", "dive into", "deep dive", "testament to", "game-changer",
    "cutting-edge", "leverage", "utilize", "seamless", "robust", "crucial", "pivotal",
    "exciting", "fascinating", "intriguing", "needless to say", "at the end of the day",
    "in today's", "let's",
    "impossible", "proven impossible", "hopeless", "wall",
    "claude", "anthropic", "openai", "chatgpt", "gpt-", "copilot", "fable", "opus", "sonnet",
    "vast.ai", "supervisor", "partie b", "make brief", "f-0", "l-0", "ev-2", "adr-",
]

# Files allowed to name AI/agent tools (blueprint section 9 check 4 exceptions).
WORD_CHECK_TOOL_NAME_EXCEPTIONS = {"AGENTS.md", "CONTRIBUTING.md"}

# Meta-documentation that must quote the forbidden words themselves to document the rule,
# and templates that hold placeholder text. Excluded from the forbidden-words content scan;
# still subject to the forbidden-characters scan.
WORD_CHECK_FULL_EXCEPTIONS = {
    os.path.join(REPO_ROOT, "docs", "style-guide.md"),
}

FRENCH_CHARS_PATTERN = re.compile(r"[àâçéèêëîïôûùüÿœ]", re.IGNORECASE)
FRENCH_WORDS = ["dossier", "piste", "porte", "témoin", "épuisé", "réfuté"]

FORBIDDEN_EXTENSIONS = {
    ".epub", ".mobi", ".azw", ".azw3", ".mp3", ".wav", ".m4a", ".flac",
    ".mp4", ".mkv", ".webm", ".pyc",
}

TEXT_EXTS = {".md", ".json", ".py", ".svg", ".dot", ".txt", ".csv"}

EXPLORER_HOST_BY_CHAIN = {
    "bitcoin": "mempool.space",
    "ethereum": "etherscan.io",
    "base": "basescan.org",
    "arweave": "viewblock.io",
    "litecoin": "litecoinspace.org",
    "solana": "solscan.io",
}


class Report:
    def __init__(self):
        self.checks = []  # (number, name, status, details)

    def record(self, number, name, failures, warnings=None):
        warnings = warnings or []
        if failures:
            self.checks.append((number, name, "FAIL", failures))
        elif warnings:
            self.checks.append((number, name, "WARN", warnings))
        else:
            self.checks.append((number, name, "PASS", []))

    def print_and_exit(self):
        any_fail = False
        for number, name, status, details in self.checks:
            print(f"[{status}] check {number}: {name}")
            for d in details:
                print(f"    {d}")
            if status == "FAIL":
                any_fail = True
        print()
        n_pass = sum(1 for c in self.checks if c[2] == "PASS")
        n_warn = sum(1 for c in self.checks if c[2] == "WARN")
        n_fail = sum(1 for c in self.checks if c[2] == "FAIL")
        print(f"{n_pass} passed, {n_warn} warned, {n_fail} failed.")
        sys.exit(1 if any_fail else 0)


def iter_files(root, exts=None):
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirpath.split(os.sep):
            continue
        for fn in filenames:
            if exts is None or os.path.splitext(fn)[1].lower() in exts:
                yield os.path.join(dirpath, fn)


def rel(path):
    try:
        return os.path.relpath(path, REPO_ROOT)
    except ValueError:
        return path


def find_puzzle_folders(scope_root):
    """Return list of (folder_path, tier_dir_name_or_None) for every folder with a puzzle.json."""
    results = []
    if scope_root == REPO_ROOT:
        for tier_dir in TIER_DIR_TO_KEY:
            tier_path = os.path.join(REPO_ROOT, tier_dir)
            if not os.path.isdir(tier_path):
                continue
            for entry in sorted(os.listdir(tier_path)):
                folder = os.path.join(tier_path, entry)
                if os.path.isdir(folder) and os.path.isfile(os.path.join(folder, "puzzle.json")):
                    results.append((folder, tier_dir))
    else:
        if os.path.isfile(os.path.join(scope_root, "puzzle.json")):
            results.append((scope_root, None))
    return results


# ---------------------------------------------------------------------------
# Check 1: manifest schema + slug/tier/status consistency
# ---------------------------------------------------------------------------

def check_manifest(folders):
    failures = []
    if jsonschema is None:
        failures.append(f"{rel(SCHEMA_PATH)}:1: jsonschema package not installed, cannot validate")
        return failures

    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    validator = jsonschema.Draft202012Validator(schema)

    for folder, tier_dir in folders:
        manifest_path = os.path.join(folder, "puzzle.json")
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        except json.JSONDecodeError as exc:
            failures.append(f"{rel(manifest_path)}:{exc.lineno}: invalid JSON: {exc.msg}")
            continue

        for err in validator.iter_errors(manifest):
            loc = "/".join(str(p) for p in err.path) or "(root)"
            failures.append(f"{rel(manifest_path)}:1: schema error at {loc}: {err.message}")

        folder_name = os.path.basename(folder.rstrip(os.sep))
        slug = manifest.get("slug")
        if slug != folder_name:
            failures.append(f"{rel(manifest_path)}:1: slug '{slug}' does not match folder name '{folder_name}'")

        tier = manifest.get("tier")
        if tier_dir is not None:
            expected_key = TIER_DIR_TO_KEY.get(tier_dir)
            if tier != expected_key:
                failures.append(f"{rel(manifest_path)}:1: tier '{tier}' does not match containing folder '{tier_dir}' (expected '{expected_key}')")

        status = manifest.get("status")
        reason = manifest.get("dead_end_reason")
        if tier == "dead-end" and reason is None:
            failures.append(f"{rel(manifest_path)}:1: tier is 'dead-end' but dead_end_reason is null")
        if tier == "solved" or status == "solved":
            solutions = manifest.get("solutions", [])
            if not solutions:
                failures.append(f"{rel(manifest_path)}:1: status/tier is solved but solutions[] is empty")
            else:
                for i, sol in enumerate(solutions):
                    if not sol.get("payout_txid"):
                        failures.append(f"{rel(manifest_path)}:1: solutions[{i}] is missing payout_txid")

    return failures


# ---------------------------------------------------------------------------
# Check 2: heading order and title badge
# ---------------------------------------------------------------------------

def extract_h2_headings(text):
    return [line.strip() for line in text.splitlines() if line.strip().startswith("## ")]


def check_headings(folders):
    failures = []
    for folder, tier_dir in folders:
        readme_path = os.path.join(folder, "README.md")
        manifest_path = os.path.join(folder, "puzzle.json")
        if not os.path.isfile(readme_path):
            failures.append(f"{rel(folder)}:0: missing README.md")
            continue
        with open(readme_path, encoding="utf-8") as f:
            text = f.read()
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            manifest = {}

        tier = manifest.get("tier")
        status = manifest.get("status", "open")
        slug = manifest.get("slug", os.path.basename(folder))

        expected = list(BASE_HEADINGS)
        # Series folders that cover a whole family of lots/contracts, tier "mid" (not
        # "solved") because some lots/contracts in the family remain open, but which carry
        # a "## Solution" section for the lot(s) already solved and claimed.
        PARTIAL_SOLVE_SERIES_SLUGS = {
            "keir-finlow-bates-blockchain-book-600ksats",
            "teikhos-bipedaljoe-solver-bounties-2eth",
        }
        is_solved = tier == "solved" or slug in PARTIAL_SOLVE_SERIES_SLUGS
        if is_solved:
            idx = expected.index("## Files in this folder")
            expected.insert(idx, "## Solution")
        if tier == "dead-end":
            idx = expected.index("## The puzzle as published")
            expected.insert(idx, "## Why this is a dead end")

        headings = extract_h2_headings(text)
        # Keep only headings that are part of the controlled vocabulary, to compare order
        # without being thrown off by ad hoc "### " subheadings picked up incorrectly.
        controlled = [h for h in headings if h in set(expected) | {"## Solution", "## Why this is a dead end"}]

        if controlled != expected:
            line_no = 1
            for i, line in enumerate(text.splitlines(), start=1):
                if line.strip() == "# " + text.splitlines()[0].lstrip("# ") if False else False:
                    pass
            failures.append(
                f"{rel(readme_path)}:1: heading order mismatch. expected {expected}, found {controlled}"
            )

        if "## Solution" in headings and not is_solved:
            failures.append(f"{rel(readme_path)}:1: '## Solution' present but tier/status is not solved")
        if "## Why this is a dead end" in headings and tier != "dead-end":
            failures.append(f"{rel(readme_path)}:1: '## Why this is a dead end' present but tier is not dead-end")

        first_line = text.splitlines()[0] if text.splitlines() else ""
        expected_badge = STATUS_BADGE.get(status)
        if expected_badge and expected_badge not in first_line:
            failures.append(f"{rel(readme_path)}:1: title line does not contain the expected badge {expected_badge}: '{first_line}'")

    return failures


# ---------------------------------------------------------------------------
# Check 3: forbidden characters
# ---------------------------------------------------------------------------

def check_forbidden_chars(scope_root):
    failures = []
    for path in iter_files(scope_root, TEXT_EXTS):
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, start=1):
            m = FORBIDDEN_CHARS_PATTERN.search(line)
            if m:
                cp = hex(ord(m.group(0)))
                failures.append(f"{rel(path)}:{i}: forbidden character {cp} in: {line.strip()[:80]}")
    return failures


# ---------------------------------------------------------------------------
# Check 4: forbidden words
# ---------------------------------------------------------------------------

def check_forbidden_words(scope_root):
    failures = []
    for path in iter_files(scope_root, {".md"}):
        basename = os.path.basename(path)
        if path in WORD_CHECK_FULL_EXCEPTIONS:
            continue
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()
        except (UnicodeDecodeError, OSError):
            continue

        is_ai_name_exception_file = basename in WORD_CHECK_TOOL_NAME_EXCEPTIONS
        is_root_readme = os.path.abspath(path) == os.path.join(REPO_ROOT, "README.md")

        for i, line in enumerate(lines, start=1):
            lower = line.lower()
            for word in FORBIDDEN_WORDS:
                pattern = re.compile(r"\b" + re.escape(word) + r"\b")
                if pattern.search(lower):
                    tool_name_word = word in {
                        "claude", "anthropic", "openai", "chatgpt", "gpt-", "copilot",
                        "fable", "opus", "sonnet",
                    }
                    if tool_name_word and (is_ai_name_exception_file or is_root_readme):
                        continue
                    failures.append(f"{rel(path)}:{i}: forbidden word '{word}' in: {line.strip()[:80]}")
    return failures


# ---------------------------------------------------------------------------
# Check 5: French leftovers (warning only)
# ---------------------------------------------------------------------------

def check_french_leftovers(scope_root):
    warnings = []
    for path in iter_files(scope_root, {".md"}):
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()
        except (UnicodeDecodeError, OSError):
            continue
        in_fence = False
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or stripped.startswith(">"):
                continue
            if FRENCH_CHARS_PATTERN.search(line):
                warnings.append(f"{rel(path)}:{i}: possible French leftover (accented character): {stripped[:80]}")
                continue
            for word in FRENCH_WORDS:
                if re.search(r"\b" + re.escape(word) + r"\b", line, re.IGNORECASE):
                    warnings.append(f"{rel(path)}:{i}: possible French leftover ('{word}'): {stripped[:80]}")
                    break
    return warnings


# ---------------------------------------------------------------------------
# Check 6: links
# ---------------------------------------------------------------------------

LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
INLINE_CODE_PATTERN = re.compile(r"`[^`]*`")

# Template files are made entirely of placeholders (<url>, images/01-...svg as syntax
# examples); their "links" are not meant to resolve, so they are skipped here.
LINK_CHECK_EXCEPT_DIR = os.path.join(REPO_ROOT, "docs", "templates")


def check_links(folders, scope_root):
    failures = []
    md_files = list(iter_files(scope_root, {".md"}))
    for path in md_files:
        if os.path.abspath(path).startswith(LINK_CHECK_EXCEPT_DIR + os.sep):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, start=1):
            # Strip inline code spans first: a link-like construct shown as a literal
            # syntax example (`[bitcoin.fr](url)`) is documentation, not a real link.
            scan_line = INLINE_CODE_PATTERN.sub("", line)
            for _text, target in LINK_PATTERN.findall(scan_line):
                if target.startswith("#"):
                    continue
                if target.startswith("http://") or target.startswith("https://"):
                    parsed = urlparse(target)
                    if not parsed.netloc:
                        failures.append(f"{rel(path)}:{i}: malformed URL: {target}")
                    continue
                # relative link or image path
                clean_target = target.split("#", 1)[0]
                if not clean_target:
                    continue
                candidate = os.path.normpath(os.path.join(os.path.dirname(path), clean_target))
                if not os.path.exists(candidate):
                    failures.append(f"{rel(path)}:{i}: relative link does not resolve: {target}")

    for folder, _tier_dir in folders:
        manifest_path = os.path.join(folder, "puzzle.json")
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            continue
        for addr in manifest.get("addresses", []):
            address = addr.get("address", "")
            explorer = addr.get("explorer", "")
            chain = addr.get("chain", "")
            if address and explorer and address not in explorer:
                failures.append(f"{rel(manifest_path)}:1: explorer URL does not contain the address: {explorer}")
            expected_host = EXPLORER_HOST_BY_CHAIN.get(chain)
            if expected_host and explorer and expected_host not in explorer:
                failures.append(f"{rel(manifest_path)}:1: explorer host does not match chain '{chain}': {explorer}")

    return failures


# ---------------------------------------------------------------------------
# Check 7: cross-checks between README and manifest
# ---------------------------------------------------------------------------

def check_cross_references(folders):
    failures = []
    for folder, _tier_dir in folders:
        readme_path = os.path.join(folder, "README.md")
        manifest_path = os.path.join(folder, "puzzle.json")
        if not (os.path.isfile(readme_path) and os.path.isfile(manifest_path)):
            continue
        with open(readme_path, encoding="utf-8") as f:
            readme_text = f.read()
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)

        for addr in manifest.get("addresses", []):
            address = addr.get("address", "")
            if address and f"`{address}`" not in readme_text:
                failures.append(f"{rel(readme_path)}:1: address {address} from puzzle.json not found backticked in README")

        for sol in manifest.get("solutions", []):
            txid = sol.get("payout_txid", "")
            if txid and txid not in readme_text:
                failures.append(f"{rel(readme_path)}:1: payout_txid {txid} from puzzle.json not found in README")

        first_line = readme_text.splitlines()[0] if readme_text.splitlines() else ""
        prize = manifest.get("prize", {})
        asset = str(prize.get("asset", ""))
        if asset and asset not in readme_text:
            failures.append(f"{rel(readme_path)}:1: prize asset '{asset}' not found anywhere in README")

    return failures


# ---------------------------------------------------------------------------
# Check 8: sizes
# ---------------------------------------------------------------------------

def check_sizes(scope_root):
    failures = []
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(scope_root):
        if ".git" in dirpath.split(os.sep):
            continue
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            total_size += size
            ext = os.path.splitext(fn)[1].lower()

            if ext == ".png" and os.path.basename(dirpath) == "images":
                if size > 500 * 1024:
                    failures.append(f"{rel(path)}:1: PNG exceeds 500 KB ({size} bytes)")
                try:
                    from PIL import Image
                    with Image.open(path) as img:
                        if max(img.size) > 1600:
                            failures.append(f"{rel(path)}:1: PNG exceeds 1600 px on the long side ({img.size})")
                except ImportError:
                    pass
                except Exception:
                    pass
            elif ext == ".svg" and os.path.basename(dirpath) == "images":
                if size > 300 * 1024:
                    failures.append(f"{rel(path)}:1: SVG exceeds 300 KB ({size} bytes)")
            elif size > 5 * 1024 * 1024:
                is_artifact = False
                manifest_path = None
                parent = dirpath
                for _ in range(4):
                    candidate = os.path.join(parent, "puzzle.json")
                    if os.path.isfile(candidate):
                        manifest_path = candidate
                        break
                    parent = os.path.dirname(parent)
                if manifest_path:
                    try:
                        with open(manifest_path, encoding="utf-8") as f:
                            manifest = json.load(f)
                        folder_of_manifest = os.path.dirname(manifest_path)
                        rel_path = os.path.relpath(path, folder_of_manifest)
                        for art in manifest.get("artifacts", []):
                            if art.get("path") == rel_path.replace(os.sep, "/"):
                                is_artifact = True
                                if size > 20 * 1024 * 1024:
                                    failures.append(f"{rel(path)}:1: artifact exceeds 20 MB cap ({size} bytes)")
                                break
                    except Exception:
                        pass
                if not is_artifact:
                    failures.append(f"{rel(path)}:1: file exceeds 5 MB and is not listed in artifacts[] ({size} bytes)")

    if total_size > 300 * 1024 * 1024:
        failures.append(f"{rel(scope_root)}:1: repository total size exceeds 300 MB ({total_size} bytes)")

    return failures


# ---------------------------------------------------------------------------
# Check 9: forbidden file types
# ---------------------------------------------------------------------------

def check_forbidden_filetypes(scope_root):
    failures = []
    for path in iter_files(scope_root):
        ext = os.path.splitext(path)[1].lower()
        base = os.path.basename(path)
        if base == "__pycache__" or base == ".DS_Store":
            failures.append(f"{rel(path)}:1: forbidden file present")
            continue
        if ext in FORBIDDEN_EXTENSIONS:
            failures.append(f"{rel(path)}:1: forbidden file extension '{ext}'")
        if ext == ".pdf":
            # allowed only when listed as an author-published puzzle artifact
            folder = os.path.dirname(path)
            manifest_path = os.path.join(folder, "puzzle.json")
            listed = False
            if os.path.isfile(manifest_path):
                try:
                    with open(manifest_path, encoding="utf-8") as f:
                        manifest = json.load(f)
                    rel_name = os.path.relpath(path, folder).replace(os.sep, "/")
                    listed = any(a.get("path") == rel_name for a in manifest.get("artifacts", []))
                except Exception:
                    pass
            if not listed:
                failures.append(f"{rel(path)}:1: .pdf present but not listed in artifacts[]")
        if ext == ".gz" and os.path.getsize(path) > 5 * 1024 * 1024:
            failures.append(f"{rel(path)}:1: .gz exceeds 5 MB")
        if ext == ".zip":
            failures.append(f"{rel(path)}:1: .zip is a forbidden file type")
    for dirpath, dirnames, filenames in os.walk(scope_root):
        if "__pycache__" in dirnames:
            failures.append(f"{rel(os.path.join(dirpath, '__pycache__'))}:1: __pycache__ directory present")
    return failures


# ---------------------------------------------------------------------------
# Check 10: text volume guard
# ---------------------------------------------------------------------------

def check_text_volume(folders):
    failures = []
    for folder, _tier_dir in folders:
        manifest_path = os.path.join(folder, "puzzle.json")
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            manifest = {}
        whitelisted = {a.get("path") for a in manifest.get("artifacts", [])}
        for sub in ("clues", "data"):
            subdir = os.path.join(folder, sub)
            if not os.path.isdir(subdir):
                continue
            for path in iter_files(subdir, {".txt", ".md"}):
                rel_name = os.path.relpath(path, folder).replace(os.sep, "/")
                if rel_name in whitelisted:
                    continue
                try:
                    with open(path, encoding="utf-8") as f:
                        text = f.read()
                except (UnicodeDecodeError, OSError):
                    continue
                word_count = len(text.split())
                if word_count > 20000:
                    failures.append(f"{rel(path)}:1: {word_count} words exceeds the 20,000 word book-text guard and is not whitelisted in artifacts[]")
    return failures


# ---------------------------------------------------------------------------
# Check 11: oracles, script compilation, absolute paths
# ---------------------------------------------------------------------------

def check_oracles_and_scripts(folders, scope_root):
    failures = []

    # validate.py itself necessarily contains the literal substrings it searches for
    # ("/home/", "sys.path", "enigme") as part of this detection logic; skip self-scan.
    self_path = os.path.abspath(__file__)

    for path in iter_files(scope_root, {".py"}):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", path],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            failures.append(f"{rel(path)}:1: py_compile failed: {result.stderr.strip()[:200]}")
        if os.path.abspath(path) == self_path:
            continue
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()
        except (UnicodeDecodeError, OSError):
            lines = []
        for i, line in enumerate(lines, start=1):
            if "/home/" in line:
                failures.append(f"{rel(path)}:{i}: absolute /home/ path in source")
            if "sys.path" in line and "enigme" in line:
                failures.append(f"{rel(path)}:{i}: sys.path hack referencing the private repo")

    for folder, _tier_dir in folders:
        manifest_path = os.path.join(folder, "puzzle.json")
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            continue
        oracle_rel = (manifest.get("derivation") or {}).get("oracle")
        if oracle_rel:
            oracle_path = os.path.join(folder, oracle_rel)
            if not os.path.isfile(oracle_path):
                failures.append(f"{rel(manifest_path)}:1: derivation.oracle points to missing file {oracle_rel}")
                continue
            result = subprocess.run(
                [sys.executable, oracle_path, "--selftest"],
                capture_output=True, text=True, cwd=folder,
            )
            if result.returncode != 0 or "SELFTEST OK" not in result.stdout:
                failures.append(f"{rel(oracle_path)}:1: --selftest did not exit 0 and print SELFTEST OK")

    return failures


# ---------------------------------------------------------------------------
# Check 12: figures
# ---------------------------------------------------------------------------

def check_figures(folders):
    failures = []
    for folder, _tier_dir in folders:
        images_dir = os.path.join(folder, "images")
        readme_path = os.path.join(folder, "README.md")
        if not os.path.isdir(images_dir):
            continue
        readme_text = ""
        if os.path.isfile(readme_path):
            with open(readme_path, encoding="utf-8") as f:
                readme_text = f.read()
        for fn in sorted(os.listdir(images_dir)):
            image_ref = f"images/{fn}"
            if image_ref not in readme_text:
                failures.append(f"{rel(os.path.join(images_dir, fn))}:1: not referenced from README.md")
                continue
            pattern = re.compile(r"!\[([^\]]*)\]\(" + re.escape(image_ref) + r"\)")
            m = pattern.search(readme_text)
            if not m or not m.group(1).strip():
                failures.append(f"{rel(os.path.join(images_dir, fn))}:1: image reference has empty alt text")
            idx = readme_text.find(image_ref)
            after = readme_text[idx: idx + 400]
            if "*Figure" not in after:
                failures.append(f"{rel(os.path.join(images_dir, fn))}:1: no '*Figure' caption line found after the image reference")
    return failures


# ---------------------------------------------------------------------------
# Check 13: dates
# ---------------------------------------------------------------------------

DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")


def check_dates(folders):
    failures = []
    for folder, _tier_dir in folders:
        manifest_path = os.path.join(folder, "puzzle.json")
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            continue
        last_updated = manifest.get("last_updated", "")
        if last_updated and last_updated > TODAY:
            failures.append(f"{rel(manifest_path)}:1: last_updated {last_updated} is in the future")
        for addr in manifest.get("addresses", []):
            vo = addr.get("verified_on", "")
            if vo and vo > TODAY:
                failures.append(f"{rel(manifest_path)}:1: verified_on {vo} is in the future")
        usd_snapshot = manifest.get("prize", {}).get("usd_snapshot")
        if usd_snapshot and usd_snapshot != ROOT_SNAPSHOT_DATE:
            failures.append(f"{rel(manifest_path)}:1: prize.usd_snapshot {usd_snapshot} does not match the root snapshot date {ROOT_SNAPSHOT_DATE}")
    return failures


# ---------------------------------------------------------------------------
# Check 14: index consistency
# ---------------------------------------------------------------------------

def check_index_consistency(scope_root):
    failures = []
    if scope_root != REPO_ROOT:
        return failures
    build_index_path = os.path.join(REPO_ROOT, "tools", "build_index.py")
    result = subprocess.run(
        [sys.executable, build_index_path, "--check"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        failures.append(f"tools/build_index.py:1: --check reports the index/README tables are stale:\n{result.stdout.strip()}")
    return failures


# ---------------------------------------------------------------------------
# Check 15: emptiness
# ---------------------------------------------------------------------------

def check_emptiness(scope_root):
    failures = []
    for dirpath, dirnames, filenames in os.walk(scope_root):
        if ".git" in dirpath.split(os.sep):
            dirnames[:] = [d for d in dirnames if d != ".git"]
            continue
        if not dirnames and not filenames:
            failures.append(f"{rel(dirpath)}:1: empty directory")

    for tier_dir in TIER_DIR_TO_KEY:
        tier_path = os.path.join(scope_root, tier_dir) if scope_root == REPO_ROOT else None
        if not tier_path or not os.path.isdir(tier_path):
            continue
        for entry in sorted(os.listdir(tier_path)):
            folder = os.path.join(tier_path, entry)
            if not os.path.isdir(folder):
                continue
            has_readme = os.path.isfile(os.path.join(folder, "README.md"))
            has_manifest = os.path.isfile(os.path.join(folder, "puzzle.json"))
            if not (has_readme and has_manifest):
                failures.append(f"{rel(folder)}:1: folder is missing README.md and/or puzzle.json")
    return failures


def cleanup_pycache(scope_root):
    """Remove __pycache__ directories and stray .pyc files under scope_root.

    py_compile (run by check 11) creates these as a side effect; leaving them on disk
    would make check 9 (forbidden file types) fail on the *next* run. Called both before
    check 9 (to clean up anything left by an earlier manual run) and after check 11."""
    import shutil
    for dirpath, dirnames, filenames in os.walk(scope_root):
        if "__pycache__" in dirnames:
            shutil.rmtree(os.path.join(dirpath, "__pycache__"), ignore_errors=True)
            dirnames.remove("__pycache__")


def main():
    parser = argparse.ArgumentParser(description="QA runner for open-crypto-puzzles.")
    parser.add_argument("--folder", default=None, help="check one folder only (repo-relative or absolute path)")
    args = parser.parse_args()

    if args.folder:
        scope_root = args.folder if os.path.isabs(args.folder) else os.path.join(REPO_ROOT, args.folder)
        scope_root = os.path.normpath(scope_root)
        if not os.path.isdir(scope_root):
            print(f"error: folder not found: {scope_root}")
            sys.exit(2)
    else:
        scope_root = REPO_ROOT

    folders = find_puzzle_folders(scope_root)
    cleanup_pycache(scope_root)

    report = Report()
    report.record(1, "manifest schema + slug/tier/status consistency", check_manifest(folders))
    report.record(2, "README heading order and status badge", check_headings(folders))
    report.record(3, "forbidden characters", check_forbidden_chars(scope_root))
    report.record(4, "forbidden words", check_forbidden_words(scope_root))
    report.record(5, "French leftovers", [], check_french_leftovers(scope_root))
    report.record(6, "links resolve", check_links(folders, scope_root))
    report.record(7, "README/manifest cross-checks", check_cross_references(folders))
    report.record(8, "file and folder size limits", check_sizes(scope_root))
    report.record(9, "forbidden file types", check_forbidden_filetypes(scope_root))
    report.record(10, "text volume guard (book-text detector)", check_text_volume(folders))
    report.record(11, "oracle self-tests, script compilation, absolute paths", check_oracles_and_scripts(folders, scope_root))
    cleanup_pycache(scope_root)
    report.record(12, "figures referenced and captioned", check_figures(folders))
    report.record(13, "date sanity", check_dates(folders))
    report.record(14, "index (puzzles.json / generated README blocks) up to date", check_index_consistency(scope_root))
    report.record(15, "no empty directories, no incomplete puzzle folders", check_emptiness(scope_root))

    report.print_and_exit()


if __name__ == "__main__":
    main()
