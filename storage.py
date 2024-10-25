from datetime import datetime
import os
import pyrebase
from config import get_firebase_config

class StorageManager:
    config = get_firebase_config()
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    @staticmethod
    def upload_image(file_path, folder="products"):
        """
        Upload image to Firebase Storage
        
        Args:
            file_path (str): Path to local image file
            folder (str): Target folder in Firebase Storage (default: 'products')
            
        Returns:
            dict: Contains upload status and image URL
        """
        try:
            # Generate unique filename using timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file_path)[1]
            firebase_path = f"{folder}/{timestamp}{file_extension}"
            
            # Upload file to Firebase Storage
            StorageManager.storage.child(firebase_path).put(file_path)
            
            # Get the public URL
            image_url = StorageManager.storage.child(firebase_path).get_url(None)
            
            return {
                "status": "success",
                "url": image_url,
                "path": firebase_path
            }
            
        except Exception as e:
            print(f"Error uploading image: {e}")
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
        
        Args:
            firebase_path (str): Path of image in Firebase Storage
            
        Returns:
            dict: Contains deletion status
        """
        try:
            StorageManager.storage.delete(firebase_path)
            return {
                "status": "success",
                "message": "Image deleted successfully"
            }
        except Exception as e:
            print(f"Error deleting image: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    def update_image(old_firebase_path, new_file_path, folder="products"):
        """
        Update image in Firebase Storage (delete old & upload new)
        
        Args:
            old_firebase_path (str): Path of existing image in Firebase Storage
            new_file_path (str): Path to new local image file
            folder (str): Target folder in Firebase Storage (default: 'products')
            
        Returns:
            dict: Contains update status and new image URL
        """
        try:
            # Delete old image if exists
            if old_firebase_path:
                StorageManager.delete_image(old_firebase_path)
            
            # Upload new image
            return StorageManager.upload_image(new_file_path, folder)
            
        except Exception as e:
            print(f"Error updating image: {e}")
            return {
                "status": "error",
                "message": str(e),
                "path": None,
                "url": None
            }