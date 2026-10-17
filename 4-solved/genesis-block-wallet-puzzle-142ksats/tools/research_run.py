"""Local output setup for bounded research runs; no network operations."""
import os
from pathlib import Path

def setup():
    repo = Path(__file__).resolve().parents[3]
    configured = os.environ.get('PUZZLE_RUN_DIR')
    if not configured:
        raise SystemExit('Set PUZZLE_RUN_DIR to a private directory outside this checkout.')
    output = Path(configured).expanduser().resolve()
    if output == repo or repo in output.parents:
        raise SystemExit('PUZZLE_RUN_DIR must be outside this checkout.')
    os.umask(0o077)
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(output, 0o700)
    return output
