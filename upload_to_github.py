"""
GitHub Repository Uploader
==========================
Uploads all Nepal Economic Development Research files to your GitHub repo
using the GitHub REST API — no git installation required.

SETUP:
  pip install requests

HOW TO GET YOUR TOKEN:
  1. Go to https://github.com/settings/tokens
  2. Click "Generate new token (classic)"
  3. Give it a name like "nepal-research-upload"
  4. Check the box: repo (full control)
  5. Click "Generate token" — copy it immediately

USAGE:
  python upload_to_github.py

Then paste your token when prompted.
"""

import os
import base64
import json
import time
import requests

# ── CONFIG ────────────────────────────────────────────────────────────────────
REPO_OWNER = "nirajneupane17"
REPO_NAME  = "Nepal-Economic-Development-Research"
BRANCH     = "main"          # change to "master" if your repo uses that
API_BASE   = "https://api.github.com"

# ── FILES TO UPLOAD ──────────────────────────────────────────────────────────
# Edit BASE_DIR to point to your local folder that contains:
#   README.md, LICENSE, data/, districts/, macro/, policy/, notebooks/
BASE_DIR = "."   # current folder by default — adjust if needed

# ── HELPERS ──────────────────────────────────────────────────────────────────
def get_headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

def get_file_sha(path_in_repo, token):
    """Get current SHA of a file (needed to update existing files)."""
    url = f"{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path_in_repo}"
    r = requests.get(url, headers=get_headers(token), params={"ref": BRANCH})
    if r.status_code == 200:
        return r.json().get("sha")
    return None  # file doesn't exist yet

def upload_file(local_path, repo_path, token, commit_message=None):
    """Upload or update a single file."""
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")

    sha = get_file_sha(repo_path, token)
    msg = commit_message or f"Add {repo_path}"

    payload = {
        "message": msg,
        "content": content,
        "branch":  BRANCH,
    }
    if sha:
        payload["sha"] = sha  # required for updates

    url = f"{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{repo_path}"
    r = requests.put(url, headers=get_headers(token), data=json.dumps(payload))

    if r.status_code in (200, 201):
        action = "Updated" if sha else "Created"
        size_kb = os.path.getsize(local_path) // 1024
        print(f"  ✓ {action}: {repo_path} ({size_kb} KB)")
        return True
    else:
        print(f"  ✗ FAILED: {repo_path} — {r.status_code}: {r.json().get('message','')}")
        return False

def collect_files(base_dir):
    """Walk base_dir and return list of (local_path, repo_path) tuples."""
    files = []
    for root, dirs, fnames in os.walk(base_dir):
        # Skip hidden folders
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in fnames:
            if fname.startswith("."):
                continue
            local_path = os.path.join(root, fname)
            # Build repo-relative path (forward slashes)
            repo_path  = os.path.relpath(local_path, base_dir).replace(os.sep, "/")
            files.append((local_path, repo_path))
    return sorted(files)

def verify_token(token):
    """Check token works and repo exists."""
    url = f"{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}"
    r = requests.get(url, headers=get_headers(token))
    if r.status_code == 200:
        data = r.json()
        print(f"\n✅ Repository found: {data['full_name']}")
        print(f"   Description: {data.get('description','—')}")
        print(f"   Default branch: {data.get('default_branch')}")
        print(f"   Stars: {data.get('stargazers_count',0)}")
        return True
    elif r.status_code == 401:
        print("✗ Invalid token. Check it and try again.")
    elif r.status_code == 404:
        print(f"✗ Repo not found: {REPO_OWNER}/{REPO_NAME}. Check spelling.")
    else:
        print(f"✗ Error {r.status_code}: {r.text}")
    return False

# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  Nepal Economic Development Research — GitHub Uploader")
    print("=" * 60)
    print(f"\nTarget: https://github.com/{REPO_OWNER}/{REPO_NAME}")
    print(f"Branch: {BRANCH}")
    print(f"Source: {os.path.abspath(BASE_DIR)}\n")

    # Get token
    token = input("Paste your GitHub Personal Access Token: ").strip()
    if not token:
        print("No token entered. Exiting.")
        return

    # Verify
    if not verify_token(token):
        return

    # Collect files
    files = collect_files(BASE_DIR)
    print(f"\nFound {len(files)} files to upload:\n")
    for _, rp in files:
        print(f"  {rp}")

    print(f"\nReady to upload {len(files)} files to GitHub.")
    confirm = input("Type YES to proceed: ").strip()
    if confirm.upper() != "YES":
        print("Cancelled.")
        return

    # Upload
    print(f"\n{'─'*60}")
    print("Uploading...")
    print(f"{'─'*60}")

    ok = 0
    fail = 0
    for i, (local_path, repo_path) in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] {repo_path}")
        success = upload_file(
            local_path, repo_path, token,
            commit_message=f"Upload {repo_path} — Nepal Economic Development Research"
        )
        if success:
            ok += 1
        else:
            fail += 1
        # Small delay to avoid hitting rate limits
        if i % 5 == 0:
            time.sleep(1)

    # Summary
    print(f"\n{'='*60}")
    print(f"  Done!  ✓ {ok} uploaded   ✗ {fail} failed")
    print(f"  View: https://github.com/{REPO_OWNER}/{REPO_NAME}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
