"""
Web scraper para extraer información de las funciones preliminares 2026 del Carnaval de Cádiz
desde codigocarnaval.com
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from typing import List, Dict, Optional
from datetime import datetime


def extraer_fecha_funcion(texto_funcion: str) -> Optional[str]:
    """
    Extrae la fecha de una función y la convierte a formato DD/MM/YYYY

    Args:
        texto_funcion: Texto como "Función 1 - Domingo 11 de enero - Preliminares 2026"

    Returns:
        Fecha en formato DD/MM/YYYY o None si no se puede parsear
    """
    # Mapeo de meses en español a números
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }

    try:
        # Buscar patrón: número + "de" + mes
        # Ejemplo: "11 de enero"
        patron = r'(\d+)\s+de\s+(\w+)'
        match = re.search(patron, texto_funcion.lower())

        if not match:
            return None

        dia = int(match.group(1))
        mes_texto = match.group(2)

        # Extraer el año (buscar 4 dígitos)
        year_match = re.search(r'(\d{4})', texto_funcion)
        if not year_match:
            return None

        año = int(year_match.group(1))

        # Obtener el número del mes
        mes = meses.get(mes_texto)
        if not mes:
            return None

        # Formatear como DD/MM/YYYY
        return f"{dia:02d}/{mes:02d}/{año}"

    except Exception as e:
        print(f"Error al parsear fecha de '{texto_funcion}': {e}")
        return None


def extraer_detalles_agrupacion(url: str, headers: dict) -> Optional[Dict]:
    """
    Extrae los detalles de una agrupación desde su página individual

    Args:
        url: URL de la página de la agrupación
        headers: Headers HTTP para la petición

    Returns:
        Diccionario con los detalles de la agrupación o None si hay error
    """
    try:
        time.sleep(0.5)  # Pausa para no saturar el servidor
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar la lista con los detalles
        ul = soup.find('ul', class_='wp-block-list')
        if not ul:
            return None

        detalles = {}

        # Extraer cada campo de la lista
        for li in ul.find_all('li', recursive=False):
            texto = li.get_text(strip=True)

            # Letra
            if texto.startswith('Letra:'):
                detalles['letra'] = texto.replace('Letra:', '').strip()

            # Música
            elif texto.startswith('Música:'):
                detalles['musica'] = texto.replace('Música:', '').strip()

            # Dirección
            elif texto.startswith('Dirección:'):
                detalles['direccion'] = texto.replace('Dirección:', '').strip()

            # Localidad
            elif texto.startswith('Localidad:'):
                detalles['localidad'] = texto.replace('Localidad:', '').strip()

            # El año anterior
            elif texto.startswith('El año anterior:'):
                # Extraer el nombre de la agrupación anterior
                link = li.find('a')
                if link:
                    nombre_anterior = link.get_text(strip=True)
                    # Extraer la fase (lo que está entre paréntesis)
                    fase_match = re.search(r'\((.*?)\)', texto)
                    fase_anterior = fase_match.group(1) if fase_match else None

                    detalles['año_anterior'] = {
                        'nombre': nombre_anterior,
                        'fase': fase_anterior
                    }
                else:
                    # Si no hay link, puede ser "No participó" u otro texto
                    detalles['año_anterior'] = texto.replace('El año anterior:', '').strip()

        return detalles if detalles else None

    except Exception as e:
        print(f"Error al extraer detalles de {url}: {e}")
        return None


def scrape_preliminares_2026(url: str, incluir_detalles: bool = True) -> List[Dict]:
    """
    Extrae información de las funciones preliminares 2026

    Args:
        url: URL de la página de preliminares 2026
        incluir_detalles: Si True, extrae detalles de cada agrupación (letra, música, etc.)

    Returns:
        Lista de diccionarios con la información de cada función
    """
    # Realizar la petición HTTP
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parsear el HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar todos los h2 que contienen las funciones
    funciones = []
    h2_elements = soup.find_all('h2', class_='wp-block-heading')

    total_agrupaciones = 0
    agrupaciones_procesadas = 0

    for h2 in h2_elements:
        # Buscar el span con id que contenga "funcion" y "preliminares_2026"
        span = h2.find('span', id=re.compile(r'funcion_\d+.*preliminares_2026'))

        if not span:
            continue

        # Extraer el texto de la función
        funcion_text = span.get_text(strip=True)

        # Extraer la fecha de la función
        fecha_funcion = extraer_fecha_funcion(funcion_text)

        # Buscar la lista ul que sigue al h2
        ul = h2.find_next_sibling('ul', class_='wp-block-list')

        if not ul:
            # A veces la lista no es hermana directa, buscar en los siguientes elementos
            next_elem = h2.find_next('ul', class_='wp-block-list')
            if next_elem:
                ul = next_elem

        if not ul:
            continue

        # Extraer las agrupaciones
        agrupaciones = []
        for li in ul.find_all('li', recursive=False):
            # Extraer el tipo de agrupación y detectar si es cabeza de serie
            tipo = None
            cabeza_serie = False

            # Buscar el mark con el tipo (Coro, etc.)
            mark = li.find('mark')
            if mark:
                tipo = mark.get_text(strip=True)
                # Si el mark tiene la clase 'has-inline-color', es cabeza de serie
                if 'has-inline-color' in mark.get('class', []):
                    cabeza_serie = True
            else:
                # Si no hay mark, extraer del texto antes del guión
                text_parts = li.get_text().split('-', 1)
                if len(text_parts) > 0:
                    tipo = text_parts[0].strip()

            # Buscar el enlace de la agrupación
            link = li.find('a')
            if link:
                nombre = link.get_text(strip=True)
                url_agrupacion = link.get('href', '')

                agrupacion_data = {
                    'tipo': tipo,
                    'nombre': nombre,
                    'cabeza_serie': cabeza_serie,
                    'fecha': fecha_funcion
                }

                # Si se requieren detalles, extraerlos de la página de la agrupación
                if incluir_detalles and url_agrupacion:
                    total_agrupaciones += 1
                    print(f"  Extrayendo detalles de: {nombre}... ({agrupaciones_procesadas + 1}/?)")
                    detalles = extraer_detalles_agrupacion(url_agrupacion, headers)
                    if detalles:
                        agrupacion_data.update(detalles)
                    agrupaciones_procesadas += 1

                agrupaciones.append(agrupacion_data)

        # Crear el objeto de la función
        if agrupaciones:
            funcion_data = {
                'funcion': funcion_text,
                'agrupaciones': agrupaciones
            }
            funciones.append(funcion_data)

    return funciones


def save_to_json(data: List[Dict], filename: str):
    """
    Guarda los datos en un archivo JSON

    Args:
        data: Lista de funciones con sus agrupaciones
        filename: Nombre del archivo de salida
    """
    output = {
        'año': 2026,
        'fase': 'Preliminares',
        'total_funciones': len(data),
        'funciones': data
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Datos guardados en {filename}")
    print(f"Total de funciones extraídas: {len(data)}")

    # Mostrar estadísticas
    total_agrupaciones = sum(len(f['agrupaciones']) for f in data)
    print(f"Total de agrupaciones: {total_agrupaciones}")


def main():
    url = 'https://www.codigocarnaval.com/coac/2026/preliminares-2026/'
    output_file = r'C:\Users\Usuario\Desktop\Scripts\Carnaval\CarnavalDatos\data\Actuaciones\preliminares_2026.json'

    print(f"Scrapeando {url}...")
    print("Extrayendo detalles completos de cada agrupación...\n")
    funciones = scrape_preliminares_2026(url, incluir_detalles=True)

    print(f"\n\nSe encontraron {len(funciones)} funciones")

    # Guardar en JSON
    save_to_json(funciones, output_file)

    # Mostrar ejemplo de los primeros datos
    if funciones:
        print("\n=== Ejemplo: Primera función ===")
        print(json.dumps(funciones[0], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
