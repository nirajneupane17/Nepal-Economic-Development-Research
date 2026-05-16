"""
╔══════════════════════════════════════════════════════════════╗
║   Nepal Economic Development Research — GitHub Pusher       ║
║   Pushes entire local folder to GitHub via REST API         ║
║   Author : Niraj Neupane                                    ║
║   Usage  : python github_push.py                            ║
╚══════════════════════════════════════════════════════════════╝

Requirements:
    pip install requests

Steps to get a token:
    1. https://github.com/settings/tokens
    2. "Generate new token (classic)"
    3. Tick  ✓ repo  (full control of private repositories)
    4. Generate → copy the token
"""

import os
import sys
import base64
import json
import time
import hashlib
import requests
from pathlib import Path

# ══════════════════════════════════════════════════════════════
#  CONFIGURATION — edit these
# ══════════════════════════════════════════════════════════════
REPO_OWNER = "nirajneupane17"
REPO_NAME  = "Nepal-Economic-Development-Research"
BRANCH     = "main"          # change to "master" if needed

# Folder to upload — "." means the same folder this script is in
# Change to an absolute path if needed, e.g.:
#   SOURCE_DIR = r"C:\Users\Niraj\Downloads\repo"          (Windows)
#   SOURCE_DIR = "/Users/niraj/Downloads/repo"              (Mac/Linux)
SOURCE_DIR = "."

# Files and folders to skip
SKIP_NAMES = {
    ".git", ".gitignore", ".DS_Store", "__pycache__",
    "github_push.py",           # skip this script itself
    "upload_to_github.py",      # skip old script
    "push_to_github.sh",
    "Thumbs.db", "desktop.ini",
}
SKIP_EXTENSIONS = {".pyc", ".pyo", ".log", ".tmp"}

# API
API_BASE = "https://api.github.com"

# Delay between uploads (seconds) — prevents rate-limit errors
UPLOAD_DELAY = 0.4

# ══════════════════════════════════════════════════════════════
#  COLOURS (works on Mac, Linux, Windows 10+)
# ══════════════════════════════════════════════════════════════
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg):   print(f"  {GREEN}✓{RESET}  {msg}")
def err(msg):  print(f"  {RED}✗{RESET}  {msg}")
def info(msg): print(f"  {CYAN}→{RESET}  {msg}")
def warn(msg): print(f"  {YELLOW}!{RESET}  {msg}")

# ══════════════════════════════════════════════════════════════
#  GITHUB API HELPERS
# ══════════════════════════════════════════════════════════════
def headers(token: str) -> dict:
    return {
        "Authorization": f"token {token}",
        "Accept":        "application/vnd.github.v3+json",
        "Content-Type":  "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def verify_token(token: str) -> dict | None:
    """Check token validity and fetch repo info."""
    url = f"{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}"
    r   = requests.get(url, headers=headers(token), timeout=15)
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 401:
        err("Invalid token — check it and try again.")
    elif r.status_code == 404:
        err(f"Repo not found: {REPO_OWNER}/{REPO_NAME}  (check spelling / visibility)")
    else:
        err(f"Unexpected error {r.status_code}: {r.text[:200]}")
    return None


def get_existing_sha(repo_path: str, token: str) -> str | None:
    """Return the blob SHA if the file already exists in the repo."""
    url = f"{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{repo_path}"
    r   = requests.get(url, headers=headers(token),
                       params={"ref": BRANCH}, timeout=15)
    if r.status_code == 200:
        return r.json().get("sha")
    return None


def upload_file(local_path: Path, repo_path: str, token: str) -> str:
    """
    Upload or update one file.
    Returns: "created" | "updated" | "skipped" | "error"
    """
    # Read and encode
    with open(local_path, "rb") as fh:
        raw     = fh.read()
        content = base64.b64encode(raw).decode("utf-8")

    sha = get_existing_sha(repo_path, token)

    payload: dict = {
        "message": f"{'Update' if sha else 'Add'} {repo_path}",
        "content": content,
        "branch":  BRANCH,
    }
    if sha:
        payload["sha"] = sha

    url = f"{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{repo_path}"
    r   = requests.put(url, headers=headers(token),
                       data=json.dumps(payload), timeout=60)

    if r.status_code in (200, 201):
        return "updated" if sha else "created"

    # Decode error
    try:
        msg = r.json().get("message", r.text[:120])
    except Exception:
        msg = r.text[:120]
    err(f"  API {r.status_code}: {msg}")
    return "error"


# ══════════════════════════════════════════════════════════════
#  FILE COLLECTION
# ══════════════════════════════════════════════════════════════
def collect_files(source: Path) -> list[tuple[Path, str]]:
    """
    Walk source directory and return sorted list of
    (local_absolute_path, repo_relative_path) tuples.
    """
    results = []
    for root, dirs, files in os.walk(source):
        # Prune dirs in-place so os.walk skips them
        dirs[:] = [
            d for d in dirs
            if d not in SKIP_NAMES and not d.startswith(".")
        ]
        for fname in files:
            if fname in SKIP_NAMES:
                continue
            if Path(fname).suffix.lower() in SKIP_EXTENSIONS:
                continue
            if fname.startswith("."):
                continue

            local_abs = Path(root) / fname
            rel       = local_abs.relative_to(source)
            repo_path = str(rel).replace(os.sep, "/")  # always forward slashes
            results.append((local_abs, repo_path))

    return sorted(results, key=lambda x: x[1])


def human_size(path: Path) -> str:
    b = path.stat().st_size
    if b < 1024:       return f"{b} B"
    if b < 1024**2:    return f"{b/1024:.1f} KB"
    return             f"{b/1024**2:.1f} MB"


# ══════════════════════════════════════════════════════════════
#  PROGRESS BAR
# ══════════════════════════════════════════════════════════════
def progress_bar(current: int, total: int, width: int = 40) -> str:
    filled = int(width * current / total)
    bar    = "█" * filled + "░" * (width - filled)
    pct    = int(100 * current / total)
    return f"[{bar}] {pct:3d}%  {current}/{total}"


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def main():
    # Header
    print(f"\n{BOLD}{'═'*62}{RESET}")
    print(f"{BOLD}  Nepal Economic Development Research — GitHub Pusher{RESET}")
    print(f"{BOLD}{'═'*62}{RESET}\n")

    source = Path(SOURCE_DIR).resolve()

    print(f"  Repo   : {BOLD}https://github.com/{REPO_OWNER}/{REPO_NAME}{RESET}")
    print(f"  Branch : {BRANCH}")
    print(f"  Source : {source}\n")

    # ── Token ─────────────────────────────────────────────────
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("  Paste your GitHub Personal Access Token")
        print("  (github.com/settings/tokens  →  repo scope)\n")
        token = input("  Token: ").strip()
    if not token:
        err("No token provided. Exiting.")
        sys.exit(1)

    # ── Verify ────────────────────────────────────────────────
    print(f"\n  Verifying token and repository...")
    repo_info = verify_token(token)
    if not repo_info:
        sys.exit(1)

    print(f"\n  {GREEN}Repository found:{RESET}")
    print(f"    Name       : {repo_info['full_name']}")
    print(f"    Visibility : {'Private' if repo_info['private'] else 'Public'}")
    print(f"    Default br : {repo_info['default_branch']}")
    if repo_info['default_branch'] != BRANCH:
        warn(f"Default branch is '{repo_info['default_branch']}' "
             f"but BRANCH is set to '{BRANCH}'. Edit the script if needed.")

    # ── Collect files ─────────────────────────────────────────
    print(f"\n  Scanning {source} ...")
    files = collect_files(source)

    if not files:
        warn("No files found to upload.")
        sys.exit(0)

    total_size = sum(p.stat().st_size for p, _ in files)
    size_mb    = total_size / 1024**2

    print(f"\n  Found {BOLD}{len(files)} files{RESET} "
          f"({size_mb:.1f} MB total)\n")

    for local_path, repo_path in files:
        print(f"    {CYAN}{repo_path}{RESET}  "
              f"{YELLOW}({human_size(local_path)}){RESET}")

    # ── Confirm ───────────────────────────────────────────────
    print(f"\n  {'─'*58}")
    confirm = input(f"\n  Upload all {len(files)} files to GitHub? [YES/no]: ").strip()
    if confirm.upper() not in ("YES", "Y", ""):
        print("  Cancelled.")
        sys.exit(0)

    # ── Upload ────────────────────────────────────────────────
    print(f"\n  {'─'*58}")
    print(f"  Uploading...\n")

    counts = {"created": 0, "updated": 0, "skipped": 0, "error": 0}
    errors = []

    for i, (local_path, repo_path) in enumerate(files, 1):
        # Progress bar
        bar = progress_bar(i - 1, len(files))
        print(f"\r  {bar}", end="", flush=True)
        print()

        size_str = human_size(local_path)
        print(f"  [{i:>3}/{len(files)}] {repo_path}  ({size_str})")

        result = upload_file(local_path, repo_path, token)
        counts[result] += 1

        if result == "created":
            ok(f"Created")
        elif result == "updated":
            ok(f"Updated")
        elif result == "skipped":
            warn(f"Skipped (no change)")
        else:
            err(f"Failed — will retry once")
            time.sleep(2)
            result2 = upload_file(local_path, repo_path, token)
            if result2 in ("created", "updated"):
                ok(f"Retry succeeded")
                counts["error"]   -= 1
                counts[result2]   += 1
            else:
                errors.append(repo_path)

        time.sleep(UPLOAD_DELAY)

    # Final progress bar
    bar = progress_bar(len(files), len(files))
    print(f"\r  {bar}\n")

    # ── Summary ───────────────────────────────────────────────
    print(f"\n  {'═'*58}")
    print(f"  {BOLD}Upload complete!{RESET}\n")
    print(f"    {GREEN}✓ Created : {counts['created']}{RESET}")
    print(f"    {GREEN}✓ Updated : {counts['updated']}{RESET}")
    if counts['skipped']:
        print(f"    {YELLOW}! Skipped : {counts['skipped']}{RESET}")
    if counts['error']:
        print(f"    {RED}✗ Failed  : {counts['error']}{RESET}")
        print(f"\n  Failed files:")
        for f in errors:
            print(f"    {RED}• {f}{RESET}")

    print(f"\n  {BOLD}View your repo:{RESET}")
    print(f"  {CYAN}https://github.com/{REPO_OWNER}/{REPO_NAME}{RESET}")
    print(f"  {'═'*58}\n")


if __name__ == "__main__":
    main()
