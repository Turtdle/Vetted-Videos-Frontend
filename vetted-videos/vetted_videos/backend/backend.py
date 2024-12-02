import functools
import json
import os
import time
from typing import TypedDict, List

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import os.path
import reflex as rx
from pymongo import MongoClient

from ..react_oauth_google import (
    GoogleOAuthProvider,
    GoogleLogin,
)

class VideoData(TypedDict):
    username : str
    length : str
    thumbnail : str
    product : str
    link : str
    videoname : str
    tags : list
    docid : str = ""

def connect_to_mongodb():
    """Connect to MongoDB cluster using connection string with password from environment variable."""
    try:
        connection_string = "mongodb+srv://sam:<db_password>@cluster0.vxwvl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        db_password = os.getenv('DB_PASSWORD')
        if not db_password:
            raise ValueError("DB_PASSWORD environment variable not set")
            
        connection_string = connection_string.replace("<db_password>", db_password)
        client = MongoClient(connection_string)
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def get_mongo_entries(
    client: MongoClient,
    database_name: str,
    collection_name: str,
) -> List[VideoData]:
    """
    Retrieves all entries from a MongoDB collection and converts them to VideoData format.
    
    Args:
        client (MongoClient): Initialized MongoDB client instance
        database_name (str): Name of the database
        collection_name (str): Name of the collection
        
    Returns:
        List[VideoData]: List of documents converted to VideoData TypedDict
        
    Raises:
        Exception: If there are issues with data conversion or missing required fields
    """
    try:
        db = client[database_name]
        collection = db[collection_name]
        documents = list(collection.find())
        video_data_list: List[VideoData] = []
        
        for doc in documents:
            try:
                video_data: VideoData = {
                    'username': str(doc.get('username', '')),
                    'length': str(doc.get('length', '')),
                    'thumbnail': str(doc.get('thumbnail', '')),
                    'product': str(doc.get('product', '')),
                    'link': str(doc.get('link', '')),
                    'videoname': str(doc.get('videoname', '')),
                    'tags': list(doc.get('tags', [])),
                    'docid' : str(doc['_id'])
                }
                video_data_list.append(video_data)
                
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error processing document {doc.get('_id', 'unknown')}: {str(e)}")
                continue
        
        print(f"Successfully processed {len(video_data_list)} documents")
        return video_data_list
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

class State(rx.State):
    videos: List[VideoData] = []
    CLIENT_ID : str = ""
    video_to_update : VideoData = VideoData()
    emails : List = []
    emails_str : str = ""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CLIENT_ID = os.getenv('CLIENT_ID', '')
        self.emails = []  # Initialize empty list
        if not self.CLIENT_ID:
            raise ValueError("CLIENT_ID environment variable not set")
        
        self.load_allowed_emails()  # Move email loading to separate method
        self.update_video_list()
        
    id_token_json: str = rx.LocalStorage()

    def get_video_to_update(self):
        return self.video_to_update

    def update_video_list(self):
        fetched_videos = get_mongo_entries(
            client=connect_to_mongodb(), 
            database_name='Landing', 
            collection_name='user_videos'
        )
        self.videos = [dict(video) for video in fetched_videos]
    def on_success(self, id_token: dict):
        self.id_token_json = json.dumps(id_token)
    
    def set_video_to_update(self, video : VideoData):
        self.video_to_update = video

    @rx.var(cache=True)
    def tokeninfo(self) -> dict[str, str]:
        try:
            return verify_oauth2_token(
                json.loads(self.id_token_json)[
                    "credential"
                ],
                requests.Request(),
                self.CLIENT_ID,
            )
        except Exception as exc:
            if self.id_token_json:
                print(f"Error verifying token: {exc}")
        return {}

    def logout(self):
        self.id_token_json = ""
    @rx.var
    def token_is_valid(self) -> bool:
        self.load_allowed_emails()  # Refresh emails list
        try:
            is_valid = bool(
                self.tokeninfo
                and int(self.tokeninfo.get("exp", 0)) > time.time()
                and self.tokeninfo.get("email") in self.emails
            )
            print("Token validation:", {  # Debug print
                "email": self.tokeninfo.get("email"),
                "allowed_emails": self.emails,
                "is_valid": is_valid
            })
            return is_valid
        except Exception as e:
            print(f"Token validation error: {e}")
            return False

    def add_item(self, form_data : VideoData):
        client = connect_to_mongodb()
        try:
            db_name = "Landing"
            collection_name = "user_videos"
            db = client[db_name]
            collection = db[collection_name]
            form_data['tags'] = form_data['tags'].split(',')
            result = collection.insert_one(form_data)
            print(f"\nDocument successfully inserted with ID: {result.inserted_id}")
            self.update_video_list()
            return rx.toast.success(f'Document successfully inserted with ID: {result.inserted_id}')
        except Exception as e:
            print(f"Error inserting document: {e}")
            return rx.toast.error(f"Error inserting document: {e}")
            return False
    def load_allowed_emails(self):
        """Load allowed emails from MongoDB"""
        self.emails = []  # Clear existing emails
        client = connect_to_mongodb()
        try:
            db = client["Landing"]
            collection = db["allowed_emails"]
            documents = list(collection.find())
            self.emails = [str(doc.get('emails')) for doc in documents]
            print("Loaded allowed emails:", self.emails)  # Debug print
        finally:
            if client:
                client.close()
    def update_item(self, form_data: VideoData):
        """
        Updates a video document in MongoDB based on the provided VideoData.
        
        Args:
            form_data (VideoData): The video data to update
            
        Returns:
            dict: Result of the update operation containing success status and message
        """
        client = connect_to_mongodb()
        try:
            db_name = "Landing"
            collection_name = "user_videos"
            db = client[db_name]
            collection = db[collection_name]

            filter_query = {"videoname": self.video_to_update['videoname']}
            tags_split : List = form_data['tags'].split(',')
            form_data['tags'] = tags_split
            for item in form_data:
                
                if form_data[item] == "":
                    if item == "tags":
                        form_data[item] = ','.join(self.video_to_update[item])
                    else:
                        form_data[item] = self.video_to_update[item]
            update_data = {
                "$set": form_data
            }

            result = collection.update_one(
                filter=filter_query,
                update=update_data
            )

            if result.matched_count == 0:
                return rx.toast.error(f"No video found with name {form_data['videname']}")
                

            if result.modified_count == 0:
                return rx.toast.warning(f"Document found but no changes were needed")

            return rx.toast.success(f"Successfully updated video")

        except Exception as e:
            return rx.toast.error(f"Error updating video: {str(e)}")

        
        finally:
            self.update_video_list()
            if client:
                client.close()

    def delete_item(self, video : VideoData):
        try:
            client = connect_to_mongodb()
            db_name = "Landing"
            collection_name = "user_videos"
            db = client[db_name]
            collection = db[collection_name]
            result = collection.delete_one({'link' : video['link']})
            self.update_video_list()
            return rx.toast.success(f'Successfully deleted video with name: {video['videoname']}', position = "bottom-left")
        except Exception as e:
            return rx.toast.error(f"Failed to delete, please contact website admin; error: {e}")
    
    @rx.var(cache=True)
    def protected_content(self) -> rx.Component:
        if self.token_is_valid:
            return rx.link(
                "Home",
                href="home",
            )
        return rx.button(
        "open in tab",
        on_click=rx.redirect(
            "/docs/api-reference/special_events"
        ),
    )