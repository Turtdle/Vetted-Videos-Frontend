from pymongo import MongoClient
import os
from datetime import datetime

def connect_to_mongodb():
    """Connect to MongoDB cluster using connection string."""
    try:
        # Replace with your connection string
        connection_string = "mongodb+srv://sam:<db_password>@cluster0.vxwvl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        with open("misc-scripts/mongo_db_pass" , "r") as f:
            db_password = f.read().strip()
        connection_string = connection_string.replace("<db_password>", db_password)
        client = MongoClient(connection_string)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def get_user_input():
    """Get document fields from user input."""
    print("\nEnter document information (all fields are required):")
    
    document = {}
    
    # Required fields
    document['username'] = input("Enter username: ").strip()
    while not document['username']:
        document['username'] = input("Username is required. Please enter a username: ").strip()
    
    document['length'] = input("Enter length: ").strip()
    while not document['length']:
        document['length'] = input("Length is required. Please enter length: ").strip()
    
    document['thumbnail'] = input("Enter thumbnail URL: ").strip()
    while not document['thumbnail']:
        document['thumbnail'] = input("Thumbnail URL is required. Please enter thumbnail URL: ").strip()
    
    document['product'] = input("Enter product: ").strip()
    while not document['product']:
        document['product'] = input("Product is required. Please enter product: ").strip()
    
    document['link'] = input("Enter link: ").strip()
    while not document['link']:
        document['link'] = input("Link is required. Please enter link: ").strip()
    
    document['videoname'] = input("Enter video name: ").strip()
    while not document['videoname']:
        document['videoname'] = input("Video name is required. Please enter video name: ").strip()
    
    # Handle tags list (max 10)
    tags = []
    print("\nEnter up to 10 tags (press Enter without input when finished):")
    while len(tags) < 10:
        tag = input(f"Enter tag {len(tags) + 1} (or press Enter to finish): ").strip()
        if not tag:
            break
        tags.append(tag)
    
    if not tags:
        print("At least one tag is required.")
        tag = input("Enter at least one tag: ").strip()
        while not tag:
            tag = input("Tag is required. Please enter a tag: ").strip()
        tags.append(tag)
    
    document['tags'] = tags
    
    # Add timestamp for tracking
    document['created_at'] = datetime.utcnow()
    
    return document

def insert_document(client):
    """Insert a single document into the specified database and collection."""
    try:
        # Specify database and collection names
        db_name = "Landing"
        collection_name = "user_videos"
        
        # Get database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        # Get document data from user
        document = get_user_input()
        
        # Insert document
        result = collection.insert_one(document)
        
        print(f"\nDocument successfully inserted with ID: {result.inserted_id}")
        return True
        
    except Exception as e:
        print(f"Error inserting document: {e}")
        return False

def main():
    # Connect to MongoDB
    client = connect_to_mongodb()
    if not client:
        return
    
    try:
        # Insert document
        insert_document(client)
        
    finally:
        # Close connection
        client.close()
        print("\nMongoDB connection closed.")

if __name__ == "__main__":
    main()