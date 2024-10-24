# views.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import Database
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class ProductList(Screen):
    container = ObjectProperty(None)
    
    def on_enter(self):
        self.load_products()
    
    def load_products(self):
        self.container.clear_widgets()
        products = Database.get_all_products()
        
        if products:
            for product in products:
                # Create product display layout
                product_layout = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=120,
                    padding=5
                )
                
                # Safely get product data with default values
                name = product.get('nama', 'No Name')  # Menggunakan 'nama' sesuai dengan input
                price = product.get('harga', 0)        # Menggunakan 'harga' sesuai dengan input
                stock = product.get('stok', 0)         # Menggunakan 'stok' sesuai dengan input
                
                # Create label with product info
                product_info = Label(
                    text=f"Nama: {name}\nHarga: Rp {price}\nStok: {stock}",
                    size_hint_y=None,
                    height=100,
                    text_size=(self.width, None),
                    halign='left'
                )
                
                product_layout.add_widget(product_info)
                self.container.add_widget(product_layout)
        else:
            self.container.add_widget(
                Label(
                    text="No products available",
                    size_hint_y=None,
                    height=100
                )
            )
    
    def show_add_product(self):
        self.manager.current = 'add_product'

class AddProduct(Screen):
    name_input = ObjectProperty(None)
    price_input = ObjectProperty(None)
    stock_input = ObjectProperty(None)
    
    def add_product(self):
        nama = self.name_input.text.strip()
        harga = self.price_input.text.strip()
        stok = self.stock_input.text.strip()
        
        if nama and harga and stok:
            try:
                # Konversi input ke format yang sesuai
                harga_float = float(harga)
                stok_int = int(stok)
                
                # Create product data dengan key yang sesuai
                product_data = {
                    'nama': nama,       # Menggunakan 'nama' sebagai key
                    'harga': harga_float,  # Menggunakan 'harga' sebagai key
                    'stok': stok_int      # Menggunakan 'stok' sebagai key
                }
                
                # Push to Firebase
                Database.add_product(product_data)
                
                # Clear inputs
                self.name_input.text = ''
                self.price_input.text = ''
                self.stock_input.text = ''
                
                # Show success popup
                self.show_popup('Sukses', 'Produk berhasil ditambahkan!')
                
                # Return to product list
                self.manager.current = 'product_list'
            except ValueError:
                self.show_popup('Error', 'Harga dan stok harus berupa angka!')
            except Exception as e:
                self.show_popup('Error', f'Terjadi kesalahan: {str(e)}')
        else:
            self.show_popup('Error', 'Semua field harus diisi!')
    
    def show_popup(self, title, content):
        popup = Popup(
            title=title,
            content=Label(text=content),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
    
    def cancel(self):
        self.manager.current = 'product_list'