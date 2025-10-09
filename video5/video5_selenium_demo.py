from pathlib import Path
import csv, sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
OUT_FILE = DATA_DIR / "quotes_js.csv"

URL = "https://quotes.toscrape.com/js/"

def create_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless=new")   # Chromium ≥118
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)

def scrape_quotes(page_source: str) -> list[dict]:
    soup = BeautifulSoup(page_source, "lxml")
    rows = []
    for q in soup.select("div.quote"):
        rows.append({
            "quote" : q.select_one("span.text").get_text(strip=True),
            "author": q.select_one("small.author").text.strip()
        })
    return rows


def main() -> None:
    driver = create_driver()
    try:
        print(f"→ Opening {URL}")
        driver.get(URL)

        # Wait until at least one quote is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.quote"))
        )
        print("✓ Page rendered, extracting HTML…")
        quotes = scrape_quotes(driver.page_source)
        print(f"✓ Extracted {len(quotes)} quotes")

        with OUT_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["quote", "author"])
            writer.writeheader()
            writer.writerows(quotes)
        print(f"Saved → {OUT_FILE.relative_to(BASE_DIR)}")

    finally:
        driver.quit()
        
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted by user")