"""
src/nlp/config_shelhamer.py - Module 5 Configuration
(COPY AND MODIFY THIS FILE - do not edit the original)

Stores configuration values for the web document EVTL pipeline.
Source: arXiv abstract page for "Agents of Chaos" (2602.20021)

Purpose

  Store configuration values.

Analytical Questions

- What web page URL should be used as the data source?
- Where should raw and processed data be stored?

Notes

Following our process, do NOT edit this _case file directly,
keep it as a working example.

In your custom project,copy this _case.py file and
append with _yourname.py instead.

Then edit your copied Python file to change:
- PAGE_URL (source of the HTML web page document),
- customize your output file name.
"""

from pathlib import Path

# ============================================================
# API CONFIGURATION
# ============================================================

# TODO: In your custom app, change the URL to work with a different page.
PAGE_URLS: list[str] = [
    "https://arxiv.org/abs/2602.20021",  # Original Shelhamer paper
    "https://arxiv.org/abs/2604.01869",  # New paper to analyze
]

# For backward compatibility, keep the first URL as PAGE_URL
PAGE_URL: str = PAGE_URLS[0]

# Let them know who we are (and that we're doing educational web mining).
HTTP_REQUEST_HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (educational-use; web-mining-course)"
}

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
RAW_PATH: Path = DATA_PATH / "raw"
PROCESSED_PATH: Path = DATA_PATH / "processed"

# TODO: In your custom app, change the output file names from case_
# to something that represents YOUR custom project.
RAW_HTML_PATH: Path = RAW_PATH / "shelhamer_raw.html"
PROCESSED_CSV_PATH: Path = PROCESSED_PATH / "shelhamer_processed.csv"
