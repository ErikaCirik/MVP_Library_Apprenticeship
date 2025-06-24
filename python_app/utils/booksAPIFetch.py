import requests
import pandas as pd

def fetch_openlibrary_data(title: str):
    url = f"https://openlibrary.org/search.json?title={title}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["numFound"] > 0:
            doc = data["docs"][0]  # use the first match
            return {
                "Title": doc.get("title", ""),
                "Author": doc.get("author_name", [""])[0],
                "First_Publish_Year": doc.get("first_publish_year", ""),
                "ISBN": doc.get("isbn", [""])[0] if "isbn" in doc else "",
                "OpenLibrary_ID": doc.get("key", ""),
            }
        else:
            return None
    except Exception as e:
        print(f"❌ Error for '{title}': {e}")
        return None

def enrich_books(book_df: pd.DataFrame):
    enriched = []

    for title in book_df["Books"].dropna().unique():
        book_data = fetch_openlibrary_data(title)
        if book_data:
            enriched.append(book_data)

    return pd.DataFrame(enriched)
