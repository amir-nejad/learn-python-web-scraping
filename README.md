# Web Scraping Mini-Course (Python)

This repo holds the code I use in my 6-episode YouTube mini-course on **web scraping with Python**.
It’s cross-platform (Windows / macOS / Linux) and kept intentionally simple so you can clone it and practice.

---

## What you’ll build

* **Ep 1 — Setup & First Request:** virtual env, polite HTTP GET, save HTML.
* **Ep 2 — Polite Requests:** headers, timeouts, **exponential back-off** retries.
* **Ep 3 — Parsing HTML:** **BeautifulSoup** → tidy rows → CSV.
* **Ep 4 — Pagination:** crawl many pages with delays/jitter; stop safely.
* **Ep 5 — JavaScript Pages:** render with **Selenium** (headless), then parse.
* **Ep 6 — Save, Clean & Share:** tidy/enrich with **pandas**, export CSV/JSON.

Practice sites: **Books to Scrape**, **Quotes to Scrape**, **httpbin**.

---

## Repo layout

(I don’t use a `/code` subfolder—each episode keeps its `.py` files right inside its folder.)

```
.
├─ video01/
│  ├─ video1_demo.py
│  └─ downloads/                # created at runtime
├─ video02/
│  ├─ video2_requests_demo.py
│  └─ downloads/
├─ video03/
│  ├─ video3_parse_demo.py
│  └─ samples/                  # optional: copy HTML from Ep 2 here
├─ video04/
│  ├─ video4_crawl_demo.py
│  └─ data/                     # downloaded pages
├─ video05/
│  ├─ video5_selenium_demo.py
│  └─ data/
├─ video06/
│  ├─ video6_clean_demo.py
│  └─ data/
├─ requirements.txt
└─ README.md
```

---

## Prereqs

* **Python** ≥ 3.10
* **Chrome/Chromium** installed (for Selenium in Ep 5)
* Internet connection

---

## Setup (one-time)

```bash
# from the repo root
python -m venv .venv

# activate the environment
# macOS/Linux (bash/zsh):  source .venv/bin/activate
# Windows PowerShell:       .\.venv\Scripts\Activate.ps1
# Windows CMD:              .\.venv\Scripts\activate.bat

# install deps
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Tip (Windows): You can use `py` instead of `python`.

---

## Run episodes

> Always activate the virtual environment first (see setup).

```bash
# Episode 1
python video01/video1_demo.py

# Episode 2
python video02/video2_requests_demo.py

# Episode 3 (optional: put HTML samples into video03/samples/)
python video03/video3_parse_demo.py

# Episode 4
python video04/video4_crawl_demo.py

# Episode 5 (needs Chrome/Chromium)
python video05/video5_selenium_demo.py

# Episode 6
python video06/video6_clean_demo.py
```

Outputs land inside each episode’s folder (`downloads/`, `data/`, or `books.csv`).

---

## Scraping etiquette (please)

* Set a realistic **User-Agent**.
* Add short **delays** between pages (+ a little randomness).
* Use **retries with exponential back-off** for transient errors.
* Check **robots.txt** and site rules.
* Avoid personal/sensitive data. This repo is for learning.

---

## Troubleshooting

* **PowerShell can’t activate venv**
  Run PowerShell as Administrator once:
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
  Then: `.\.venv\Scripts\Activate.ps1`

* **Selenium/driver issues (Ep 5)**
  Make sure Chrome/Chromium is installed and up-to-date.
  I use `webdriver-manager` to fetch the right driver automatically.
  If headless is weird, remove `--headless=new` to debug visibly.

* **SSL / certificates**
  Check system time; try: `python -m pip install -U certifi`.

* **403 / blocked**
  Slow down, improve headers, try later, or from a different network.

---

## Use this freely

This repo is here so you can **clone, learn, copy, tweak—even use it in your own projects**.
Credit is appreciated but not required. Have fun and build cool stuff.

---

## Questions?

Open an issue or drop a comment on the YouTube videos. Happy scraping!
