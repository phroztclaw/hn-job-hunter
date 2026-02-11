# HN Job Hunter 🏹

**Stop doomscrolling "Who is hiring". Start applying.**

This simple, powerful CLI tool scans Hacker News "Who is Hiring" threads for exactly what you want—whether that's "Remote Python Contract" or "Rust Freelance in Berlin".

## Features
- 🔍 **Smart Keyword Filtering:** Only see jobs that match your stack.
- 📊 **Relevance Scoring:** Sorts results by keyword density.
- 📄 **Clean Exports:** Outputs directly to CSV (for spreadsheets) or Markdown (for Notion).
- 🚀 **Fast:** Scans hundreds of comments in seconds.

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install requests
   ```

2. **Run the Hunter:**
   ```bash
   python3 job_hunter.py --keywords "remote,python,contract"
   ```

3. **Get Results:**
   Open `leads.txt` (or specify `--output my_jobs.csv --format csv`).

## Advanced Usage

**Export to CSV for Excel/Sheets:**
```bash
python3 job_hunter.py --keywords "react,frontend" --format csv --output frontend_jobs.csv
```

**Find Niche Roles:**
```bash
python3 job_hunter.py --keywords "cobol,banking"
```

## Why?
Because your time is better spent coding than scrolling.

---
*Built by Ka-El. Free for the community.*
