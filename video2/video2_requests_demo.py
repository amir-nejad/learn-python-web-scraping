from pathlib import Path
import requests, time, random, sys

BASE_URL = "https://books.toscrape.com"
HEADERS  = {"User-Agent": "Mozilla/5.0 (webscraping-course/2.0)"}

BASE_DIR = Path(__file__).parent
DOWNLOADS = BASE_DIR / "downloads"
DOWNLOADS.mkdir(exist_ok=True)

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
            
            
def save_html(content: str, filename:str) -> Path:
    path = DOWNLOADS / filename
    path.write_text(content, encoding="utf-8")
    print(f"Saved HTML content to {path}")
    return path

def main() -> None:
    url_home = BASE_URL
    print(f"Fetching {url_home}...")
    
    home_resp = polite_get(url_home)
    save_html(home_resp.text, "page_home.html")

    url_books = f"{BASE_URL}/catalogue/page-1.html"
    print(f"Fetching {url_books}...")
    books_resp = polite_get(url_books)
    save_html(books_resp.text, "page_books.html")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    else:
        print("Script completed successfully.")