# storage.py
import pyrebase
from datetime import datetime
import os
from config import get_firebase_config

class StorageManager:
    config = get_firebase_config()
    try:
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        print("Firebase Storage initialized successfully")
    except Exception as e:
        print(f"Error initializing Firebase Storage: {e}")
        raise e

    @staticmethod
    def upload_image(file_path, folder="products"):
        """
        Upload image to Firebase Storage
        """
        try:
            print(f"Attempting to upload image: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return {
                    "status": "error",
                    "message": "File not found",
                    "path": None,
                    "url": None
                }

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file_path)[1]
            firebase_path = f"{folder}/{timestamp}{file_extension}"
            print(f"Generated Firebase path: {firebase_path}")

            # Upload file
            print("Starting upload...")
            StorageManager.storage.child(firebase_path).put(file_path)
            print("Upload completed")

            # Get URL
            print("Getting download URL...")
            image_url = StorageManager.storage.child(firebase_path).get_url(None)
            print(f"Got URL: {image_url}")

            return {
                "status": "success",
                "url": image_url,
                "path": firebase_path
            }

        except Exception as e:
            print(f"Error in upload_image: {str(e)}")
            print(f"Error type: {type(e)}")
            return {
                "status": "error",
                "message": str(e),
                "path": None,
                "url": None
            }

    @staticmethod
    def delete_image(firebase_path):
        """
        Delete image from Firebase Storage
        """
        try:
            print(f"Attempting to delete image: {firebase_path}")
            
            if not firebase_path:
                print("No path provided")
                return {
                    "status": "error",
                    "message": "No image path provided"
                }

            StorageManager.storage.delete(firebase_path)
            print("Delete successful")
            
            return {
                "status": "success",
                "message": "Image deleted successfully"
            }
        except Exception as e:
            print(f"Error in delete_image: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    def update_image(old_firebase_path, new_file_path, folder="products"):
        """
        Update image in Firebase Storage
        """
        try:
            print(f"Attempting to update image. Old path: {old_firebase_path}, New file: {new_file_path}")
            
            # Delete old image if exists
            if old_firebase_path:
                print("Deleting old image...")
                StorageManager.delete_image(old_firebase_path)
            
            # Upload new image
            print("Uploading new image...")
            return StorageManager.upload_image(new_file_path, folder)
            
        except Exception as e:
            print(f"Error in update_image: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "path": None,
                "url": None
            }