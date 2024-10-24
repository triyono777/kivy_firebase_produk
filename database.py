# database.py
import pyrebase
from config import get_firebase_config

class Database:
    config = get_firebase_config()
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    @staticmethod
    def get_all_products():
        try:
            products = Database.db.child("products").get()
            if products.each():
                return [product.val() for product in products.each()]
            return []
        except Exception as e:
            print(f"Error getting products: {e}")
            return []

    @staticmethod
    def add_product(product_data):
        try:
            return Database.db.child("products").push(product_data)
        except Exception as e:
            print(f"Error adding product: {e}")
            raise e

    @staticmethod
    def update_product(product_id, product_data):
        try:
            return Database.db.child("products").child(product_id).update(product_data)
        except Exception as e:
            print(f"Error updating product: {e}")
            raise e

    @staticmethod
    def delete_product(product_id):
        try:
            return Database.db.child("products").child(product_id).remove()
        except Exception as e:
            print(f"Error deleting product: {e}")
            raise e