"""
Scraper para obtener los datos de adultos de 2026 en el mismo formato
que los archivos históricos (carnaval_XXXX_adultos_full.json).

Fuente: https://letrasdecarnaval.com/anyo/2026
Salida: data/json/carnaval_2026_adultos_full.json
"""

import sys
import os
import json
import requests

# Añadir el directorio raíz del proyecto al path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

from src.scrapers.scraper_historical import scrape_year, scrape_details, scrape_lyrics

YEAR = 2026
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'json')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f'carnaval_{YEAR}_adultos_full.json')


def main():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/124.0.0.0 Safari/537.36'
    })

    groupings = scrape_year(session, YEAR)

    if not groupings:
        print(f"No se encontraron agrupaciones para {YEAR}. "
              "Comprueba que la URL https://letrasdecarnaval.com/anyo/2026 ya está disponible.")
        return

    total = len(groupings)
    print(f"\nProcesando {total} agrupaciones de {YEAR}...\n")

    for i, grouping in enumerate(groupings, start=1):
        print(f"[{i}/{total}] {grouping['name']}")
        scrape_details(session, grouping)
        scrape_lyrics(session, grouping)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(groupings, f, ensure_ascii=False, indent=4)

    print(f"\nGuardado: {OUTPUT_FILE}")
    print(f"Total agrupaciones: {total}")


if __name__ == "__main__":
    main()
