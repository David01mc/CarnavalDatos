"""
Script para subir los datos de preliminares 2026 a MongoDB
Incluye también placeholders para cuartos, semifinales y final
"""

import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv


def generar_fases_futuras():
    """
    Genera documentos placeholder para cuartos, semifinales y final

    Returns:
        Lista de documentos con las fases futuras
    """
    documentos = []

    # Cuartos de final: Del 30 de enero al 6 de febrero de 2026
    cuartos_fechas = [
        "30/01/2026", "31/01/2026",
        "01/02/2026", "02/02/2026", "03/02/2026", "04/02/2026", "05/02/2026", "06/02/2026"
    ]

    for i, fecha in enumerate(cuartos_fechas, 1):
        documentos.append({
            'año': 2026,
            'fase': 'Cuartos de Final',
            'funcion': f'Cuartos de Final - Función {i}',
            'fecha': fecha,
            'tipo': None,
            'nombre': None,
            'cabeza_serie': None,
            'letra': None,
            'musica': None,
            'direccion': None,
            'localidad': None,
            'año_anterior': None
        })

    # Semifinales: Del 8 al 11 de febrero de 2026
    semifinal_fechas = ["08/02/2026", "09/02/2026", "10/02/2026", "11/02/2026"]

    for i, fecha in enumerate(semifinal_fechas, 1):
        documentos.append({
            'año': 2026,
            'fase': 'Semifinales',
            'funcion': f'Semifinal - Función {i}',
            'fecha': fecha,
            'tipo': None,
            'nombre': None,
            'cabeza_serie': None,
            'letra': None,
            'musica': None,
            'direccion': None,
            'localidad': None,
            'año_anterior': None
        })

    # Final: El 13 de febrero de 2026
    documentos.append({
        'año': 2026,
        'fase': 'Final',
        'funcion': 'Final',
        'fecha': '13/02/2026',
        'tipo': None,
        'nombre': None,
        'cabeza_serie': None,
        'letra': None,
        'musica': None,
        'direccion': None,
        'localidad': None,
        'año_anterior': None
    })

    return documentos


def upload_preliminares_2026():
    """
    Sube los datos de preliminares 2026 a MongoDB en la colección Preliminares2026
    """
    # Cargar variables de entorno
    load_dotenv()

    # Obtener credenciales
    username = os.getenv("USERNAME_MONGODB")
    password = os.getenv("PASSWORD_MONGODB")

    if not password:
        print("Error: No se encontró PASSWORD_MONGODB en el archivo .env")
        return

    if not username:
        print("Warning: USERNAME_MONGODB no encontrado en .env, usando default 'david01mc_db_user'")
        username = "david01mc_db_user"

    # String de conexión
    uri = f"mongodb+srv://{username}:{password}@carnavalrag.ju1u34a.mongodb.net/?appName=CarnavalRAG"

    try:
        # Conectar a MongoDB
        client = MongoClient(uri)
        client.admin.command('ping')
        print("✓ Conectado exitosamente a MongoDB!")
    except Exception as e:
        print(f"✗ Error al conectar a MongoDB: {e}")
        return

    # Base de datos y colección
    db = client["CarnavalDatos"]
    collection = db["Preliminares2026"]

    # Ruta al archivo JSON
    json_file = r'C:\Users\Usuario\Desktop\Scripts\Carnaval\CarnavalDatos\data\Actuaciones\preliminares_2026.json'

    try:
        # Leer el archivo JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\n✓ Archivo JSON cargado: {json_file}")
        print(f"  - Año: {data.get('año')}")
        print(f"  - Fase: {data.get('fase')}")
        print(f"  - Total funciones: {data.get('total_funciones')}")

        # Limpiar la colección antes de insertar (opcional)
        print("\n¿Desea limpiar la colección Preliminares2026 antes de insertar? (s/n): ", end='')
        # Para ejecución automática, comentar las siguientes líneas y descomentar la que sigue
        # respuesta = input().strip().lower()
        respuesta = 's'  # Cambiar a 'n' si no quieres limpiar automáticamente

        if respuesta == 's':
            collection.delete_many({})
            print("✓ Colección limpiada")

        # Preparar documentos para insertar
        # Cada agrupación será un documento separado
        documentos = []

        # 1. Añadir agrupaciones de preliminares
        for funcion in data.get('funciones', []):
            for agrupacion in funcion.get('agrupaciones', []):
                # Crear documento con toda la información
                documento = {
                    'año': data.get('año'),
                    'fase': data.get('fase'),
                    'funcion': funcion.get('funcion'),
                    **agrupacion  # Desempaquetar todos los campos de la agrupación
                }
                documentos.append(documento)

        # 2. Añadir placeholders para cuartos, semifinales y final
        print("\n✓ Añadiendo placeholders para fases futuras...")
        fases_futuras = generar_fases_futuras()
        documentos.extend(fases_futuras)
        print(f"  - Cuartos de Final: 8 funciones")
        print(f"  - Semifinales: 4 funciones")
        print(f"  - Final: 1 función")

        # Insertar documentos
        if documentos:
            result = collection.insert_many(documentos)
            print(f"\n✓ Se insertaron {len(result.inserted_ids)} agrupaciones en la colección Preliminares2026")

            # Mostrar estadísticas
            print("\n=== Estadísticas ===")
            print(f"Total de documentos insertados: {len(documentos)}")

            # Contar por fase
            fases = {}
            for doc in documentos:
                fase = doc.get('fase', 'Sin fase')
                fases[fase] = fases.get(fase, 0) + 1

            print("\nDistribución por fase:")
            for fase, count in sorted(fases.items()):
                print(f"  - {fase}: {count}")

            # Contar por tipo (solo para preliminares)
            tipos = {}
            for doc in documentos:
                if doc.get('fase') == 'Preliminares' and doc.get('tipo'):
                    tipo = doc.get('tipo')
                    tipos[tipo] = tipos.get(tipo, 0) + 1

            if tipos:
                print("\nDistribución por tipo (Preliminares):")
                for tipo, count in sorted(tipos.items()):
                    print(f"  - {tipo}: {count}")

            # Mostrar ejemplo de un documento insertado
            print("\n=== Ejemplo de documento insertado ===")
            ejemplo = collection.find_one()
            print(json.dumps(ejemplo, default=str, ensure_ascii=False, indent=2))

            # Crear índices
            print("\n=== Creando índices ===")
            create_indexes(collection)

        else:
            print("✗ No se encontraron agrupaciones para insertar")

    except FileNotFoundError:
        print(f"✗ Error: No se encontró el archivo {json_file}")
        print("   Ejecuta primero el script scraper_preliminares_2026.py")
    except Exception as e:
        print(f"✗ Error al procesar el archivo: {e}")
    finally:
        client.close()
        print("\n✓ Conexión cerrada")


def create_indexes(collection):
    """
    Crea índices en la colección para optimizar las consultas
    """
    try:
        # Índice por fase (filtrar por Preliminares, Cuartos, Semifinales, Final)
        collection.create_index("fase")
        print("✓ Índice creado: fase")

        # Índice por nombre de agrupación (búsquedas por nombre)
        collection.create_index("nombre")
        print("✓ Índice creado: nombre")

        # Índice por tipo (filtrar por Coro, Comparsa, Chirigota, Cuarteto)
        collection.create_index("tipo")
        print("✓ Índice creado: tipo")

        # Índice por fecha (ordenar/filtrar por fecha)
        collection.create_index("fecha")
        print("✓ Índice creado: fecha")

        # Índice por localidad (búsquedas por localidad)
        collection.create_index("localidad")
        print("✓ Índice creado: localidad")

        # Índice por cabeza de serie (filtrar cabezas de serie)
        collection.create_index("cabeza_serie")
        print("✓ Índice creado: cabeza_serie")

        # Índice compuesto: tipo + fecha (consultas comunes: "chirigotas en fecha X")
        collection.create_index([("tipo", 1), ("fecha", 1)])
        print("✓ Índice compuesto creado: tipo + fecha")

        # Índice compuesto: fecha + cabeza_serie (consultas: "cabezas de serie por fecha")
        collection.create_index([("fecha", 1), ("cabeza_serie", 1)])
        print("✓ Índice compuesto creado: fecha + cabeza_serie")

        # Índice de texto para búsquedas full-text en nombre, letra, dirección
        collection.create_index([
            ("nombre", "text"),
            ("letra", "text"),
            ("direccion", "text")
        ])
        print("✓ Índice de texto creado: nombre, letra, dirección")

        # Mostrar todos los índices
        print("\n=== Lista de índices creados ===")
        for idx in collection.list_indexes():
            print(f"  - {idx['name']}: {idx.get('key', {})}")

    except Exception as e:
        print(f"✗ Error al crear índices: {e}")


if __name__ == "__main__":
    upload_preliminares_2026()
