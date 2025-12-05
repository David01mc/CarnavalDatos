import os
from collections import defaultdict
from pymongo import MongoClient
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from .env
    username = os.getenv("USERNAME_MONGODB")
    password = os.getenv("PASSWORD_MONGODB")
    
    if not password:
        print("Error: Could not find PASSWORD_MONGODB in .env file.")
        return
    
    if not username:
        print("Warning: USERNAME_MONGODB not found in .env, using default 'david01mc_db_user'")
        username = "david01mc_db_user"
    
    # Connection string
    uri = f"mongodb+srv://{username}:{password}@carnavalrag.ju1u34a.mongodb.net/?appName=CarnavalRAG"
    
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("✓ Successfully connected to MongoDB!")
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        return
    
    # Database and Collection
    db = client["CarnavalDatos"]
    collection = db["agrupaciones"]
    
    print("\n=== Phase 1: Building author-agrupaciones index ===")
    
    # Dictionary to map author name -> list of agrupaciones
    autor_to_agrupaciones = defaultdict(list)
    
    # Get all documents
    all_agrupaciones = list(collection.find({}))
    print(f"Found {len(all_agrupaciones)} agrupaciones in database")
    
    # Build the index
    for agrupacion in all_agrupaciones:
        agrupacion_name = agrupacion.get('name', 'Unknown')
        authors = agrupacion.get('authors', [])
        
        for author in authors:
            author_name = author.get('name', '').strip()
            if author_name:
                autor_to_agrupaciones[author_name].append(agrupacion_name)
    
    print(f"✓ Indexed {len(autor_to_agrupaciones)} unique authors")
    
    # Show some examples
    print("\nExample authors and their agrupaciones:")
    for i, (autor, agrupaciones) in enumerate(list(autor_to_agrupaciones.items())[:5]):
        print(f"  - {autor}: {len(agrupaciones)} agrupaciones")
    
    print("\n=== Phase 2: Updating documents ===")
    
    updated_count = 0
    
    for agrupacion in all_agrupaciones:
        agrupacion_id = agrupacion['_id']
        authors = agrupacion.get('authors', [])
        
        if not authors:
            continue
        
        # Update each author with their related agrupaciones
        updated_authors = []
        for author in authors:
            author_name = author.get('name', '').strip()
            
            # Get related agrupaciones for this author
            related_agrupaciones = autor_to_agrupaciones.get(author_name, [])
            
            # If author only appears in one agrupacion, set to ["No hay"]
            if len(related_agrupaciones) <= 1:
                related_agrupaciones = ["No hay"]
            
            # Add the agrupaciones_relacionadas field to the author object
            updated_author = author.copy()
            updated_author['agrupaciones_relacionadas'] = related_agrupaciones
            updated_authors.append(updated_author)
        
        # Update the document in MongoDB
        result = collection.update_one(
            {"_id": agrupacion_id},
            {"$set": {"authors": updated_authors}}
        )
        
        if result.modified_count > 0:
            updated_count += 1
    
    print(f"✓ Updated {updated_count} documents")
    
    print("\n=== Verification ===")
    
    # Show a sample document
    sample = collection.find_one({"authors.0": {"$exists": True}})
    if sample:
        print(f"\nSample agrupacion: {sample.get('name', 'Unknown')}")
        print(f"Authors with related agrupaciones:")
        for author in sample.get('authors', []):
            print(f"  - {author.get('name', 'Unknown')} ({author.get('role', 'Unknown')})")
            related = author.get('agrupaciones_relacionadas', [])
            if related == ["No hay"]:
                print(f"    → No hay otras agrupaciones")
            else:
                print(f"    → {len(related)} agrupaciones relacionadas: {', '.join(related[:3])}{'...' if len(related) > 3 else ''}")
    
    print("\n✓ Process completed successfully!")

if __name__ == "__main__":
    main()
