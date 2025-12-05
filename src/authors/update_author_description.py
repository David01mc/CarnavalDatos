import os
from pymongo import MongoClient
from dotenv import load_dotenv

def update_author_description(author_name, new_description):
    """
    Actualiza la descripción de un autor en TODAS las agrupaciones donde aparece.
    """
    # Load environment variables
    load_dotenv()
    
    mongodb_username = os.getenv("USERNAME_MONGODB")
    mongodb_password = os.getenv("PASSWORD_MONGODB")
    
    if not mongodb_password:
        print("❌ Error: PASSWORD_MONGODB not found in .env")
        return
    
    if not mongodb_username:
        mongodb_username = "david01mc_db_user"
    
    # Connect to MongoDB
    uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}@carnavalrag.ju1u34a.mongodb.net/?appName=CarnavalRAG"
    
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("✅ Connected to MongoDB\n")
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        return
    
    db = client["CarnavalDatos"]
    collection = db["agrupaciones"]
    
    # Find how many agrupaciones have this author
    count = collection.count_documents({"authors.name": author_name})
    
    if count == 0:
        print(f"❌ No se encontró ninguna agrupación con el autor '{author_name}'")
        return
    
    print(f"📊 Encontradas {count} agrupaciones con el autor '{author_name}'")
    print(f"📝 Nueva descripción: {new_description[:100]}...")
    print(f"\n⚠️  Esto actualizará la descripción en TODAS las {count} agrupaciones")
    
    confirm = input(f"\n¿Continuar? (yes/no): ").lower()
    
    if confirm != 'yes':
        print("❌ Cancelado por el usuario")
        return
    
    # Update all occurrences using array filters
    result = collection.update_many(
        {"authors.name": author_name},
        {"$set": {"authors.$[elem].descripcion": new_description}},
        array_filters=[{"elem.name": author_name}]
    )
    
    print(f"\n{'='*60}")
    print(f"✅ Actualización completada!")
    print(f"   Documentos modificados: {result.modified_count}")
    print(f"   Documentos encontrados: {result.matched_count}")
    print(f"{'='*60}\n")

def main():
    print("="*60)
    print("🔄 ACTUALIZAR DESCRIPCIÓN DE AUTOR")
    print("="*60)
    print("\nEste script actualiza la descripción de un autor en")
    print("TODAS las agrupaciones donde aparece.\n")
    
    author_name = input("Nombre del autor (exacto): ").strip()
    
    if not author_name:
        print("❌ Nombre de autor no puede estar vacío")
        return
    
    print(f"\nEscribe la descripción del autor (puede ser multilínea).")
    print("Presiona Enter dos veces cuando termines:\n")
    
    lines = []
    while True:
        line = input()
        if line == "" and len(lines) > 0 and lines[-1] == "":
            break
        lines.append(line)
    
    # Remove the last empty line
    if lines and lines[-1] == "":
        lines.pop()
    
    new_description = "\n".join(lines).strip()
    
    if not new_description:
        print("❌ Descripción no puede estar vacía")
        return
    
    update_author_description(author_name, new_description)

if __name__ == "__main__":
    main()
