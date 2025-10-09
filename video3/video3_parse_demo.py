from pathlib import Path
import csv
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).parent
SAMPLES = BASE_DIR / "downloads"
OUT_FILE = BASE_DIR / "books.csv"

def star_rating(tag: BeautifulSoup) -> int:
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for cls in tag.get("class", []):
        if cls in rating_map:
            return rating_map[cls]
    return 0


def parse_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    books = []
    for pod in soup.select("article.product_pod"):
        books.append({
            "title": pod.h3.a["title"],
            "price": pod.select_one("p.price_color").text,
            "rating": star_rating(pod.select_one(".star-rating")),
        })
    return books


def main() -> None:
    all_books = []
    
    print(SAMPLES.glob("page_*.html"))
    for file in sorted(SAMPLES.glob("page_*.html")):
        print(f"Parsing {file.name}")
        html = file.read_text(encoding="utf-8")
        all_books.extend(parse_page(html))

    print(f"Parsed {len(all_books)} books")
    
    with OUT_FILE.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["title", "price", "rating"])
        writer.writeheader()
        writer.writerows(all_books)
    print(f"Saved {OUT_FILE.relative_to(BASE_DIR.parent)} with {len(all_books)} books.")


if __name__ == "__main__":
    main()