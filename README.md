# Carnaval Data Scraper Project

This project contains scripts to scrape data from [letrasdecarnaval.com](https://letrasdecarnaval.com), specifically focusing on the "Adultos" category for the Carnival of Cádiz.

## Project Structure

```
CarnavalDatos/
├── .env                          # Environment variables (MongoDB credentials)
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── requirements.txt              # Python dependencies
│
├── src/                          # Source code
│   ├── scrapers/                # Web scraping scripts
│   │   └── scraper_historical.py
│   ├── database/                # Database management scripts
│   │   ├── upload_to_mongo.py
│   │   └── upload_to_mongo_v2.py
│   └── authors/                 # Author-related scripts
│       ├── list_authors.py
│       └── update_author_description.py
│
├── data/                         # Project data
│   └── json/                    # JSON files with scraped data
│       └── carnaval_YYYY_adultos_full.json
│
├── docs/                         # Documentation
│   ├── AUTORES_DESCRIPCIONES.md
│   ├── GUIA_PRINCIPIANTES.md
│   ├── MIGRACION_CAMPOS.md
│   ├── explicacion_mongodb.md
│   └── guia_script_upload.md
│
└── utils/                        # Utility scripts
    ├── check_structure.py
    └── debug_env.py
```

## How to Run

### Installation

1. Ensure you have Python installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Scraping Data

Run the historical scraper to fetch data for a range of years (default: 1885-2025):

```bash
python src/scrapers/scraper_historical.py
```

The script fetches:
- Grouping details (Name, Category, Author, Year, Image)
- Author details (Name, Role, Image)
- Lyrics (Title, Type, Views, Content)

Output files are saved to `data/json/` as `carnaval_{year}_adultos_full.json`.

### MongoDB Upload

1. Create a `.env` file in the root directory with your MongoDB credentials:
   ```env
   USERNAME_MONGODB=your_username
   PASSWORD_MONGODB=your_password
   ```

2. Run the upload script:
   ```bash
   python src/database/upload_to_mongo.py
   ```

### Author Management

List all authors:
```bash
python src/authors/list_authors.py
```

Update author descriptions:
```bash
python src/authors/update_author_description.py
```

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

## Documentation

For more detailed information, see the `docs/` directory:
- **GUIA_PRINCIPIANTES.md** - Beginner's guide
- **explicacion_mongodb.md** - MongoDB setup and usage
- **guia_script_upload.md** - Upload script guide
- **AUTORES_DESCRIPCIONES.md** - Author descriptions guide
- **MIGRACION_CAMPOS.md** - Field migration guide

## Notes

- The scraper respects the website by not overwhelming it with requests
- Data for 2021 is limited due to the pandemic
- All JSON files are stored in `data/json/`
