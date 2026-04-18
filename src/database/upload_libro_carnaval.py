"""
Limpia y sube el libro 'El Carnaval de Cádiz' a MongoDB.
Colección: libros
Estrategia: un documento por capítulo (óptimo para RAG).

Fuente: data/output_clean.txt
"""

import os
import re
import json
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

INPUT_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'output_clean.txt')
)

LIBRO_META = {
    "titulo": "El Carnaval de Cádiz.",
    "autor": "XXX",
    "editorial": "YYY",
    "coleccion": "ZZZ",
    "año": 2025,
    "isbn": "111111111111",
}

# Patrón de cabecera de capítulo:
# - "INTRODUCCIÓN" o "BIBLIOGRAFÍA CONSULTADA" (exactas)
# - "N. PALABRAS..." donde N es 1-2 dígitos (evita años como 1936, 2019)
CHAPTER_PATTERN = re.compile(
    r'^(INTRODUCCIÓN|BIBLIOGRAFÍA CONSULTADA|[0-9]{1,2}\. [A-ZÁÉÍÓÚÑÜ].+)$',
    re.MULTILINE
)


# ---------------------------------------------------------------------------
# Limpieza
# ---------------------------------------------------------------------------

REPLACEMENTS = [
    # Artefactos OCR del copyright
    (r'O Mors[eé]s Casacno Osreca', '© Moisés Camacho Ortega'),
    (r'O EniromAL ALMuzara.*', '© Editorial Almuzara, 2025'),
    (r'EorroR1aL ALMUZARA.*ARTE Y PATAIMOMO', 'EDITORIAL ALMUZARA - COLECCIÓN ARTE Y PATRIMONIO'),
    # Guiones de separación de línea (OCR los rompe)
    (r'([a-záéíóúñü])-\n([a-záéíóúñü])', r'\1\2'),
    # Más de 2 saltos de línea consecutivos → 2
    (r'\n{3,}', '\n\n'),
    # Espacios al final de línea
    (r'[ \t]+\n', '\n'),
    # Espacios múltiples internos
    (r'  +', ' '),
]


def clean_text(text: str) -> str:
    for pattern, replacement in REPLACEMENTS:
        text = re.sub(pattern, replacement, text)
    return text.strip()


# ---------------------------------------------------------------------------
# Segmentación por capítulos
# ---------------------------------------------------------------------------

def split_chapters(text: str) -> list[dict]:
    """Divide el texto en capítulos usando las cabeceras detectadas."""
    matches = list(CHAPTER_PATTERN.finditer(text))
    chapters = []

    # Texto antes del primer capítulo (portada, copyright, dedicatoria)
    if matches and matches[0].start() > 0:
        pre = text[:matches[0].start()].strip()
        if pre:
            chapters.append({
                "numero_capitulo": -1,
                "titulo_capitulo": "Portada y créditos",
                "contenido": pre,
            })

    for i, match in enumerate(matches):
        titulo_cap = match.group(0).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        contenido = text[start:end].strip()

        # Número de capítulo
        num_match = re.match(r'^(\d{1,2})\.', titulo_cap)
        if num_match:
            num = int(num_match.group(1))
        elif titulo_cap == "INTRODUCCIÓN":
            num = 0
        else:
            num = 99  # BIBLIOGRAFÍA

        chapters.append({
            "numero_capitulo": num,
            "titulo_capitulo": titulo_cap,
            "contenido": contenido,
        })

    return chapters


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

def build_documents(chapters: list[dict]) -> list[dict]:
    now = datetime.now(timezone.utc)
    docs = []
    for cap in chapters:
        palabras = len(cap["contenido"].split())
        docs.append({
            **LIBRO_META,
            "tipo": "libro",
            "numero_capitulo": cap["numero_capitulo"],
            "titulo_capitulo": cap["titulo_capitulo"],
            "contenido": cap["contenido"],
            "num_palabras": palabras,
            "fecha_subida": now,
        })
    return docs


def main():
    load_dotenv()

    username = os.getenv("USERNAME_MONGODB", "david01mc_db_user")
    password = os.getenv("PASSWORD_MONGODB")
    if not password:
        print("Error: PASSWORD_MONGODB no encontrado en .env")
        return

    if not os.path.exists(INPUT_FILE):
        print(f"Error: no se encuentra {INPUT_FILE}")
        return

    # --- Leer y limpiar ---
    print("Leyendo y limpiando el texto...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw = f.read()

    text = clean_text(raw)

    # --- Segmentar ---
    chapters = split_chapters(text)
    print(f"Capítulos detectados: {len(chapters)}")
    for c in chapters:
        print(f"  [{c['numero_capitulo']:>3}] {c['titulo_capitulo'][:60]}  "
              f"({len(c['contenido'].split())} palabras)")

    # --- Conectar a MongoDB ---
    uri = f"mongodb+srv://{username}:{password}@carnavalrag.ju1u34a.mongodb.net/?appName=CarnavalRAG"
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("\nConexión a MongoDB correcta.")
    except Exception as e:
        print(f"Error conectando: {e}")
        return

    collection = client["CarnavalDatos"]["libros"]

    # Eliminar versión previa del mismo libro para evitar duplicados
    deleted = collection.delete_many({"isbn": LIBRO_META["isbn"]})
    if deleted.deleted_count:
        print(f"Eliminados {deleted.deleted_count} documentos previos del libro.")

    docs = build_documents(chapters)
    result = collection.insert_many(docs)
    print(f"Insertados {len(result.inserted_ids)} documentos en la colección 'libros'.")

    # Índices útiles para RAG
    collection.create_index("isbn")
    collection.create_index("numero_capitulo")
    collection.create_index([("contenido", "text"), ("titulo_capitulo", "text")])
    print("Índices creados.")
    print("\nUpload completado.")


if __name__ == "__main__":
    main()
