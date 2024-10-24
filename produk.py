from kivy.uix.screenmanager import Screen
from pyrebase import pyrebase

# Firebase Configuration (this should match with main.py config)
config = {
    "apiKey": "AIzaSyCvLjuLnSEDs4UR2lCykeG5UpxuSkwcVPU",
    "authDomain": "projek-python-sample.firebaseapp.com",
    "databaseURL": "https://projek-python-sample-default-rtdb.firebaseio.com",
    "storageBucket": "projek-python-sample.appspot.com"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()

class ProdukScreen(Screen):
    def add_produk(self, nama, harga):
        data = {"nama": nama, "harga": harga}
        db.child("produk").push(data)

    def get_produk(self):
        produk_list = db.child("produk").get()
        if produk_list.each():
            for produk in produk_list.each():
                print(produk.key(), produk.val())
        else:
            print("No products found.")

    def update_produk(self, produk_id, nama, harga):
        db.child("produk").child(produk_id).update({"nama": nama, "harga": harga})

    def delete_produk(self, produk_id):
        db.child("produk").child(produk_id).remove()
