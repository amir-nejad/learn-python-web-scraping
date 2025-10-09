from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

BOOKS_CSV = DATA_DIR / "books.csv"
BOOKS_JSON = DATA_DIR / "books_clean.json"

# w3schools.com => pandas
def clean_books(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    
    df.columns = [col.strip() for col in df.columns]
    
    df["price"] = df["price"].astype(str).str.replace("Â£", "").astype(float)
    df["rating"] = pd.to_numeric(df["rating"], downcast="integer", errors="coerce")
    
    df["tier"] = pd.cut(
        df["price"],
        bins=[0, 20, 40, 60, float("inf")],
        labels=["Budget", "Standard", "Premium", "Luxury"]
        )
    
    df = df.drop_duplicates(subset=["title"])
    return df

def main() -> None:
    print(f'Loading {BOOKS_CSV.name}...')
    books_df = clean_books(BOOKS_CSV)
    print(f'Books rows after cleaning: {len(books_df)}')
    
    books_df.to_json(
        BOOKS_JSON,
        orient="records",
        indent=2,
        force_ascii=False
    )
    
    print(f'Saved -> {BOOKS_JSON.relative_to(BASE_DIR)}')
    
    print(f'\nTop 3 most expensive books:')
    
    print(
        books_df.sort_values("price", ascending=False)
                .loc[:, ["title", "price"]]
                .head(3)
                .to_string(index=False)
    )

if __name__ == "__main__":
    main()    