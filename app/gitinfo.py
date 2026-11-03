"""Current git commit and dirty flag, so a quality gate can tell which code is running."""
import subprocess
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CACHE_SECONDS = 2
_cache = {"time": 0.0, "value": None}


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=_REPO_ROOT, capture_output=True, text=True, timeout=5, check=True
    )
    return result.stdout.strip()


def get_git_info() -> dict:
    """Return {"commit", "dirty"}. Falls back to unknown/None if git fails."""
    now = time.monotonic()
    if _cache["value"] is not None and now - _cache["time"] < _CACHE_SECONDS:
        return _cache["value"]
    try:
        info = {
            "commit": _git("rev-parse", "--short", "HEAD"),
            "dirty": _git("status", "--porcelain") != "",
        }
    except (OSError, subprocess.SubprocessError):
        info = {"commit": "unknown", "dirty": None}
    _cache["time"] = now
    _cache["value"] = info
    return info
