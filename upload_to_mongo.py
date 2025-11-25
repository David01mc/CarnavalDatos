import os
import json
import glob
from pymongo import MongoClient
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
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
        # Check connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return

    # Database and Collection
    db = client["CarnavalDatos"]
    collection = db["agrupaciones"]

    # Find all JSON files
    json_files = glob.glob("carnavalJSON/*.json")
    print(f"Found {len(json_files)} JSON files.")

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                if data:
                    # Add filename or year/category metadata if needed? 
                    # The data already seems to have 'year' and 'category'.
                    # We can insert_many
                    result = collection.insert_many(data)
                    print(f"Inserted {len(result.inserted_ids)} documents from {json_file}")
                else:
                    print(f"Skipping empty list in {json_file}")
            elif isinstance(data, dict):
                collection.insert_one(data)
                print(f"Inserted 1 document from {json_file}")
            else:
                print(f"Unknown data format in {json_file}")

        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    print("Upload complete.")

if __name__ == "__main__":
    main()
