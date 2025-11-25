import requests
from bs4 import BeautifulSoup
import json
import os
import time

BASE_URL = "https://letrasdecarnaval.com"

def get_soup(session, url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_year(session, year):
    print(f"--- Scraping Year {year} ---")
    url = f"{BASE_URL}/anyo/{year}"
    soup = get_soup(session, url)
    if not soup:
        return []

    cards = soup.select('a.card.mb-3.hei-fix')
    groupings = []

    print(f"Found {len(cards)} cards for {year}. Filtering for 'Adultos'...")

    for card in cards:
        category_tag = card.select_one('h5.card-title')
        category_text = category_tag.get_text(strip=True) if category_tag else ""
        
        if "adultos" in category_text.lower():
            title_tag = card.select_one('h4.text-primary')
            title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"
            
            p_tags = card.select('p.card-text')
            year_str = str(year)
            author = ""
            
            for p in p_tags:
                text = p.get_text(strip=True)
                if "Autor" in text:
                    author = text.replace("Autor", "").strip()
            
            link_suffix = card.get('href')
            link = BASE_URL + link_suffix if link_suffix and not link_suffix.startswith('http') else link_suffix

            img_tag = card.select_one('img.img-fluid.card-img-top')
            img_src = img_tag.get('src') if img_tag else ""
            if img_src and not img_src.startswith('http'):
                img_src = BASE_URL + img_src

            groupings.append({
                "name": title,
                "category": category_text,
                "year": year_str,
                "author": author,
                "link": link,
                "image": img_src,
                "authors": [],
                "lyrics": [],
                "youtube": [],
                "spotify": [],
                "posición":""
            })
    
    print(f"Found {len(groupings)} 'Adultos' groupings for {year}.")
    return groupings

def scrape_details(session, grouping):
    if not grouping.get('link'):
        return

    info_url = grouping['link'] + "/informacion"
    # print(f"  Scraping details: {grouping['name']}")
    soup = get_soup(session, info_url)
    if not soup:
        return

    authors = []
    author_containers = soup.select('div.col-6.col-md-4.hei-fix')
    
    for container in author_containers:
        card = container.select_one('a.card')
        if not card:
            continue
        
        name_tag = card.select_one('h5.card-title')
        name = name_tag.get_text(strip=True) if name_tag else "Unknown"
        
        role_tag = card.select_one('p.card-text')
        role = role_tag.get_text(strip=True) if role_tag else ""
        
        img_tag = card.select_one('img.card-img-top')
        img_src = img_tag.get('src') if img_tag else ""
        if img_src and not img_src.startswith('http'):
            img_src = BASE_URL + img_src
            
        author_link = card.get('href')
        if author_link and not author_link.startswith('http'):
            author_link = BASE_URL + author_link
        
        authors.append({
            "name": name,
            "role": role,
            "image": img_src,
            "link": author_link
        })
    
    grouping['authors'] = authors

def scrape_lyrics(session, grouping):
    if not grouping.get('link'):
        return

    # print(f"  Scraping lyrics: {grouping['name']}")
    soup = get_soup(session, grouping['link'])
    if not soup:
        return

    lyrics_list = []
    card_bodies = soup.find_all('div', class_='card-body')
    
    for card in card_bodies:
        link_tag = card.find('a', string=lambda text: text and "Ver letra" in text)
        if not link_tag:
            continue
        
        lyric_url_suffix = link_tag.get('href')
        if not lyric_url_suffix:
            continue
        
        lyric_url = BASE_URL + lyric_url_suffix if not lyric_url_suffix.startswith('http') else lyric_url_suffix
        
        # Type
        type_tag = card.find('p', class_='text-primary')
        lyric_type = type_tag.get_text(strip=True) if type_tag else "Unknown"
        
        # Views
        views_span = card.find('span', class_='d-flex align-items-center')
        views = "0"
        if views_span:
            views = views_span.get_text(strip=True)
        
        # Title
        title_tag = card.find('h4')
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"
        
        # Content
        lyric_soup = get_soup(session, lyric_url)
        if lyric_soup:
            # Last Modification
            last_mod_p = lyric_soup.find('p', string=lambda text: text and "Ultima modificación" in text)
            last_modification = ""
            if last_mod_p:
                last_modification = last_mod_p.get_text(strip=True).replace("Ultima modificación:", "").strip()

            letra_p = lyric_soup.find('p', id='letra')
            if letra_p:
                content = letra_p.get_text(separator="\n", strip=True)
                lyrics_list.append({
                    "title": title,
                    "type": lyric_type,
                    "views": views,
                    "url": lyric_url,
                    "content": content,
                    "last_modification": last_modification
                })
    
    grouping['lyrics'] = lyrics_list

def main():
    session = requests.Session()
    # Headers to look like a browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    start_year = 1982
    end_year = 1885

    OUTPUT_DIR = r"C:\Users\Usuario\Desktop\Scripts\CarnavalDatos\carnavalJSON"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for year in range(start_year, end_year - 1, -1):
        output_file = os.path.join(OUTPUT_DIR, f'carnaval_{year}_adultos_full.json')
        
        # Skip if already exists (optional, but good for resuming)
        # if os.path.exists(output_file):
        #     print(f"File {output_file} already exists. Skipping...")
        #     continue

        groupings = scrape_year(session, year)
        
        total_groupings = len(groupings)
        print(f"Processing {total_groupings} groupings for {year}...")
        
        for i, grouping in enumerate(groupings):
            print(f"[{i+1}/{total_groupings}] {grouping['name']} ({year})")
            scrape_details(session, grouping)
            scrape_lyrics(session, grouping)
            # time.sleep(0.1) # Be gentle

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(groupings, f, ensure_ascii=False, indent=4)
        
        print(f"Saved {output_file}")
        print("-" * 30)

if __name__ == "__main__":
    main()
