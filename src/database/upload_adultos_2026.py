"""
Sube los datos de adultos 2026 a MongoDB (colección 'agrupaciones').
Elimina primero cualquier documento year=2026 existente para evitar duplicados.

Requiere haber ejecutado antes: src/scraper_adultos_2026.py
"""

import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

JSON_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'json', 'carnaval_2026_adultos_full.json')

DEFAULT_FIELDS = {
    'callejera': 'No',
    'descripcion': '',
    'caracteristicas': [],
    'componentes': []
}


def add_defaults(doc):
    for field, value in DEFAULT_FIELDS.items():
        if field not in doc:
            doc[field] = value
    return doc


def main():
    load_dotenv()

    username = os.getenv("USERNAME_MONGODB", "david01mc_db_user")
    password = os.getenv("PASSWORD_MONGODB")

    if not password:
        print("Error: PASSWORD_MONGODB no encontrado en .env")
        return

    uri = f"mongodb+srv://{username}:{password}@carnavalrag.ju1u34a.mongodb.net/?appName=CarnavalRAG"

    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("Conexión a MongoDB correcta.")
    except Exception as e:
        print(f"Error conectando a MongoDB: {e}")
        return

    json_path = os.path.abspath(JSON_FILE)
    if not os.path.exists(json_path):
        print(f"Error: no se encuentra el archivo {json_path}")
        print("Ejecuta primero: python src/scraper_adultos_2026.py")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("El JSON está vacío.")
        return

    collection = client["CarnavalDatos"]["agrupaciones"]

    # Eliminar documentos de 2026 ya existentes para evitar duplicados
    deleted = collection.delete_many({"year": "2026"})
    if deleted.deleted_count:
        print(f"Eliminados {deleted.deleted_count} documentos previos de 2026.")

    docs = [add_defaults(doc) for doc in data]
    result = collection.insert_many(docs)

    print(f"Insertados {len(result.inserted_ids)} documentos de adultos 2026.")
    print("Upload completado.")


if __name__ == "__main__":
    main()
