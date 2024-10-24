from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from pyrebase import pyrebase
from kivy.lang import Builder

# Firebase Configuration

config = {
    "apiKey": "AIzaSyCvLjuLnSEDs4UR2lCykeG5UpxuSkwcVPU",
    "authDomain": "projek-python-sample.firebaseapp.com",
    "databaseURL": "https://projek-python-sample-default-rtdb.firebaseio.com",
    "storageBucket": "projek-python-sample.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
Builder.load_file('produk.kv')
# Define the Screens
class MainScreen(Screen):
    pass

class ProdukScreen(Screen):
    # Add Produk Functionality
    def add_produk(self, nama, harga):
        data = {"nama": nama, "harga": harga}
        db.child("produk").push(data)

    # Get Produk Data
    def get_produk(self):
        produk_list = db.child("produk").get()
        if produk_list.each():
            return [(p.key(), p.val()) for p in produk_list.each()]
        return []


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ProdukScreen(name='produk'))
        return sm

if __name__ == '__main__':
    MainApp().run()