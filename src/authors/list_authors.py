import os
from pymongo import MongoClient
from dotenv import load_dotenv
from collections import defaultdict

def main():
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
    
    # Get all agrupaciones
    agrupaciones = list(collection.find({}))
    
    # Count authors
    author_stats = defaultdict(lambda: {"count": 0, "agrupaciones": [], "has_description": False})
    
    for agrupacion in agrupaciones:
        authors = agrupacion.get('authors', [])
        for author in authors:
            name = author.get('name', '').strip()
            if name:
                author_stats[name]["count"] += 1
                author_stats[name]["agrupaciones"].append(agrupacion.get('name', 'Sin nombre'))
                if author.get('descripcion'):
                    author_stats[name]["has_description"] = True
    
    # Sort by count (most frequent first)
    sorted_authors = sorted(author_stats.items(), key=lambda x: x[1]["count"], reverse=True)
    
    print(f"{'='*80}")
    print(f"📊 AUTORES EN LA BASE DE DATOS")
    print(f"{'='*80}\n")
    print(f"Total de autores únicos: {len(sorted_authors)}\n")
    
    # Show top 50 most frequent authors
    print(f"{'Autor':<40} {'Apariciones':<12} {'Descripción'}")
    print(f"{'-'*40} {'-'*12} {'-'*12}")
    
    for author_name, stats in sorted_authors[:50]:
        has_desc = "✅ Sí" if stats["has_description"] else "❌ No"
        print(f"{author_name:<40} {stats['count']:<12} {has_desc}")
    
    if len(sorted_authors) > 50:
        print(f"\n... y {len(sorted_authors) - 50} autores más\n")
    
    # Summary
    authors_with_desc = sum(1 for _, stats in sorted_authors if stats["has_description"])
    authors_without_desc = len(sorted_authors) - authors_with_desc
    
    print(f"\n{'='*80}")
    print(f"📈 RESUMEN")
    print(f"{'='*80}")
    print(f"Autores con descripción: {authors_with_desc}")
    print(f"Autores sin descripción: {authors_without_desc}")
    print(f"{'='*80}\n")
    
    # Show authors with most appearances (candidates for description)
    print(f"🎯 TOP 10 AUTORES MÁS FRECUENTES (candidatos prioritarios para descripción):\n")
    for i, (author_name, stats) in enumerate(sorted_authors[:10], 1):
        has_desc = "✅" if stats["has_description"] else "❌"
        print(f"{i}. {author_name} - {stats['count']} agrupaciones {has_desc}")
    
    print(f"\n💡 Tip: Usa 'update_author_description.py' para actualizar la descripción de un autor en todas sus apariciones")

if __name__ == "__main__":
    main()
