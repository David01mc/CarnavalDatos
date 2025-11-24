# Carnaval Data Scraper Project

This project contains scripts to scrape data from [letrasdecarnaval.com](https://letrasdecarnaval.com), specifically focusing on the "Adultos" category for the Carnival of Cádiz.

## Project Structure

- **`scraper_historical.py`**: The main script. It scrapes data for a range of years (default: 2017-2025). It fetches:
    - Grouping details (Name, Category, Author, Year, Image).
    - Author details (Name, Role, Image).
    - Lyrics (Title, Type, Views, Content).
- **`carnavalJSON/`**: Directory containing the output JSON files, named `carnaval_{year}_adultos_full.json`.
- **`scraper_details.py`** & **`scraper_lyrics.py`**: Intermediate scripts used during development (superseded by `scraper_historical.py`).

## How to Run

1.  Ensure you have Python installed.
2.  Install dependencies:
    ```bash
    pip install requests beautifulsoup4
    ```
3.  Run the historical scraper:
    ```bash
    python scraper_historical.py
    ```
    This will generate/overwrite the JSON files in the current directory (you may want to move them to `carnavalJSON` manually or update the script).

## Data Format

The output JSON files contain a list of grouping objects. Example structure:

```json
[
    {
        "name": "Name of Grouping",
        "category": "Chirigota Adultos",
        "year": "2025",
        "author": "Author Name",
        "link": "URL",
        "image": "Image URL",
        "authors": [
            {
                "name": "Author Name",
                "role": "Role",
                "image": "Image URL",
                "link": "URL"
            }
        ],
        "lyrics": [
            {
                "title": "Lyric Title",
                "type": "Pasodoble",
                "views": "1234",
                "url": "URL",
                "content": "Full text of the lyric..."
            }
        ]
    }
]
```

## Notes

- The scraper respects the website by not hammering it with too many requests too quickly (though `scraper_historical.py` is designed to be relatively fast).
- 2021 has very few entries due to the pandemic.
