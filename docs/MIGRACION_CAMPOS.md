# Script para Actualizar Datos Existentes con Nuevos Campos

Este script añade los nuevos campos a todas las agrupaciones existentes en MongoDB.

## Opción 1: Actualizar desde MongoDB Compass o mongosh

Ejecuta este comando en MongoDB Compass o en mongosh:

```javascript
db.agrupaciones.updateMany(
  { 
    $or: [
      { callejera: { $exists: false } },
      { descripcion: { $exists: false } },
      { caracteristicas: { $exists: false } },
      { componentes: { $exists: false } }
    ]
  },
  { 
    $set: { 
      callejera: "No",
      descripcion: "",
      caracteristicas: [],
      componentes: []
    } 
  }
)
```

## Opción 2: Script Python

Crea un archivo `migrate_fields.py`:

```python
import os
from pymongo import MongoClient
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    username = os.getenv("USERNAME_MONGODB")
    password = os.getenv("PASSWORD_MONGODB")
    
    if not password:
        print("Error: PASSWORD_MONGODB not found")
        return
    
    if not username:
        username = "david01mc_db_user"
    
    uri = f"mongodb+srv://{username}:{password}@carnavalrag.ju1u34a.mongodb.net/?appName=CarnavalRAG"
    
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    db = client["CarnavalDatos"]
    collection = db["agrupaciones"]
    
    # Actualizar documentos que no tienen los nuevos campos
    result = collection.update_many(
        {
            "$or": [
                {"callejera": {"$exists": False}},
                {"descripcion": {"$exists": False}},
                {"caracteristicas": {"$exists": False}},
                {"componentes": {"$exists": False}}
            ]
        },
        {
            "$set": {
                "callejera": "No",
                "descripcion": "",
                "caracteristicas": [],
                "componentes": []
            }
        }
    )
    
    print(f"✅ Actualizados {result.modified_count} documentos")
    print(f"📊 Total de documentos revisados: {result.matched_count}")

if __name__ == "__main__":
    main()
```

Ejecuta:
```bash
python migrate_fields.py
```

## Opción 3: No hacer nada

Los datos existentes funcionarán perfectamente sin los nuevos campos. La interfaz web los manejará automáticamente con valores por defecto.

## Para Futuros Uploads

Si quieres que los nuevos datos incluyan estos campos desde el principio, usa `upload_to_mongo_v2.py` en lugar de `upload_to_mongo.py`.

El nuevo script añade automáticamente:
- `callejera`: "No"
- `descripcion`: ""
- `caracteristicas`: []
- `componentes`: []

## Recomendación

**No es necesario hacer nada ahora**. Los datos existentes funcionan perfectamente. Cuando edites una agrupación desde la web, podrás añadir los nuevos campos manualmente.

Si en el futuro quieres que todos los datos tengan estos campos, ejecuta la migración con cualquiera de las opciones anteriores.
