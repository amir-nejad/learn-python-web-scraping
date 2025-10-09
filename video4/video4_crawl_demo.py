from pathlib import Path
import requests
import time
import random
import sys

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS  = {"User-Agent": "Mozilla/5.0 (webscraping-course/4.1)"}

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

def polite_get(url: str, max_tries: int = 3, backoff: float = 1.5) -> requests.Response:
    for attempt in range(1, max_tries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_tries:
                raise
            sleep_for = backoff * (2 ** (attempt - 1)) + random.uniform(0, 0.5) # jitter 
            print(f"Retrying in {sleep_for:.2f} seconds...")
            time.sleep(sleep_for)
            
def crawl_catalogue(*, start_page: int = 1, max_pages: int = 100, throttle_range: tuple[float, float] = (1.5, 3)) -> int:
    downloaded = 0
    
    for page in range(start_page, start_page + max_pages):
        url = BASE_URL.format(page)
        print(f'Fetching page {page}')
        
        try:
            resp = polite_get(url)
        except requests.exceptions.HTTPError as e:
            status = getattr(e.response, "status_code", None)
            if status == 404:
                print("Reached end of catalogue (404). Stipping...")
                break
            print(f"HTTP error ({status}). Stopping...")
            break
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}. Stopping...")
            break
        
        html = resp.text
        
        dst = DATA_DIR / f"page_{page:02}.html"
        dst.write_text(html, encoding="utf-8")
        print(f"Saved {dst.name} ({dst.stat().st_size}) bytes")
        downloaded += 1
        
        delay = random.uniform(*throttle_range)
        print(f"waiting... {delay:.1f} seconds delay before getting next page.")
        time.sleep(delay)
    
    return downloaded

def main() -> None:
    total = crawl_catalogue(start_page=1, max_pages=100)
    rel = DATA_DIR.relative_to(BASE_DIR)
    print(f"Downloaded {total} page(s) into {rel}")
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interupted by user")