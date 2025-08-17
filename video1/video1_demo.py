from pathlib import Path
import requests
import sys

BASE_URL = "https://piantech.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (webscraping-course/1.0)"}

BASE_DIR = Path(__file__).parent
DOWNLOADS = BASE_DIR / "downloads"
DOWNLOADS.mkdir(exist_ok=True)

def fetch(url: str, filename: str) -> None:
    print(f"GET {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error fetching {url}: {err}")
        sys.exit(1)
        
    
    dst = DOWNLOADS / filename
    dst.write_text(resp.text, encoding="utf-8")
    print(f"Saved to {dst} ({dst.stat().st_size} bytes)")


def main() -> None:
    fetch(f"{BASE_URL}/robots.txt", "robots_piantech.txt")
    fetch(f"{BASE_URL}", "piantech_home.html")

if __name__ == "__main__":
    main()