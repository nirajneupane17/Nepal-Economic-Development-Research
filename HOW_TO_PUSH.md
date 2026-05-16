# How to Push to GitHub

Two methods. Pick whichever fits your setup.

---

## Method 1 — Python Script (easiest, no git needed)

Works on any machine with Python. Uses the GitHub API to upload files directly.

### Step 1 — Install requests
```bash
pip install requests
```

### Step 2 — Get a GitHub Personal Access Token
1. Go to **https://github.com/settings/tokens**
2. Click **"Generate new token (classic)"**
3. Name it anything (e.g. `nepal-research`)
4. Tick the **`repo`** checkbox (full control)
5. Scroll down → **Generate token**
6. **Copy it immediately** — GitHub only shows it once

### Step 3 — Run the script
```bash
# From inside the unzipped Nepal_Research_GitHub_Package folder:
python upload_to_github.py
```

Paste your token when prompted. Type `YES` to confirm. It uploads every file
and prints a tick for each success.

---

## Method 2 — Git Command Line

### Step 1 — Make the script executable (Mac/Linux)
```bash
chmod +x push_to_github.sh
./push_to_github.sh
```

### On Windows
```cmd
bash push_to_github.sh
```

When prompted, enter **1** (push into existing repo). Git will ask for your
GitHub username and password — use your **token as the password**.

---

## Method 3 — GitHub Desktop (GUI, no terminal)

1. Download **GitHub Desktop** from https://desktop.github.com
2. Sign in with your GitHub account
3. File → **Add local repository** → point to the unzipped folder
4. It detects changes automatically
5. Write a commit message → **Commit to main** → **Push origin**

---

## Method 4 — Drag & Drop on GitHub.com

1. Go to https://github.com/nirajneupane17/Nepal-Economic-Development-Research
2. Click **"uploading an existing file"** link
3. Drag the entire unzipped folder into the upload area
4. GitHub uploads everything
5. Write a commit message → **Commit changes**

> Note: GitHub web uploader has a 100-file limit per upload.
> For this repo (18 files) it works fine.

---

## After Pushing — Verify

Open: https://github.com/nirajneupane17/Nepal-Economic-Development-Research

You should see:
- ✅ The main README rendered with the indicator table and district index
- ✅ `districts/01_Bhojpur/` folder with profile and GIF assets
- ✅ `macro/`, `policy/`, `data/`, `notebooks/` folders
- ✅ 18 files total

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `401 Bad credentials` | Token is wrong or expired — generate a new one |
| `404 Not found` | Check repo name spelling — it's case-sensitive |
| `422 Unprocessable` | File already exists with same content — that's fine, skip it |
| `push rejected` | Your branch may be `master` not `main` — edit script: `BRANCH="master"` |
| Large file error | GIFs >100MB trigger LFS — ours are ~450KB so this won't happen |
