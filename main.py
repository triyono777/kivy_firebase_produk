# main.py
from kivy.app import App
from kivy.lang import Builder
from views import ProductList, AddProduct, EditProduct
from kivy.uix.screenmanager import ScreenManager

class MainApp(App):
    def build(self):
        Builder.load_file('product.kv')
        sm = ScreenManager()
        sm.add_widget(ProductList(name='product_list'))
        sm.add_widget(AddProduct(name='add_product'))
        sm.add_widget(EditProduct(name='edit_product'))
        return sm

if __name__ == '__main__':
    MainApp().run()