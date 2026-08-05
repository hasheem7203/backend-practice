# Week 5 — Book Scraper

A scraper that collects book listings from [books.toscrape.com](https://books.toscrape.com/), a sandbox site built specifically for scraping practice, extracts and cleans key fields, and saves them as structured JSON records.

## What it does

Follows a 5-stage pipeline:

1. **Fetch** — downloads raw HTML from each page using `requests`, identified with an honest `User-Agent`.
2. **Parse** — loads the HTML into a navigable tree using `BeautifulSoup`.
3. **Extract** — pulls the raw title, price, star rating, and stock status from each book listing.
4. **Clean** — fixes encoding issues (e.g. `Â£` → `£`), converts price to a float, converts rating words (`"Three"`) to integers (`3`), and strips whitespace from stock status.
5. **Structure** — saves all cleaned records to `books.json`.

## Fields collected per book

| Field | Type | Example |
|---|---|---|
| `title` | string | `"A Light in the Attic"` |
| `price` | float | `51.77` |
| `rating` | int (1–5) | `3` |
| `stock` | string | `"In stock"` |

## Responsible scraping practices

- **robots.txt checked** — `https://books.toscrape.com/robots.txt` returns 404 (no rules published), so there are no crawl restrictions to violate.
- **Rate limiting** — a 1-second delay (`time.sleep(1)`) between each page request to avoid overloading the server.
- **Honest identification** — every request sends a custom `User-Agent` header (`RankAI-Week5-Scraper/1.0`) identifying it as a student practice project, rather than spoofing a browser.

## How to run

1. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
2. Install dependencies (if not already installed):
   ```
   pip install requests beautifulsoup4
   ```
3. Run the scraper:
   ```
   python scraper.py
   ```

This scrapes 10 pages (200 books) and saves the results to `books.json` in the same folder.

## Output

`books.json` — a JSON array of book records, e.g.:

```json
[
  {
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "stock": "In stock"
  },
  ...
]
```

## Files

- `scraper.py` — the full pipeline (fetch, parse, extract, clean, structure functions)
- `books.json` — scraped output data
- `README.md` — this file

## Notes

This dataset is intended as the input corpus for Week 6 (RAG pipeline).