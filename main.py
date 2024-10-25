from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from auth import AuthService
from views import ProductList, AddProduct, EditProduct
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Muat tampilan dari file .kv
Builder.load_file('auth.kv')
Builder.load_file('product.kv')
Builder.load_file('user.kv') 
# Buat instance AuthService
auth_service = AuthService()
class PenggunaScreen(Screen):
    pass

class PetugasScreen(Screen):
    pass
class LoginScreen(Screen):
    def login(self, email, password):
        success, message = auth_service.login(email, password)
        if success:
            user_role = App.get_running_app().user_role
               # Arahkan berdasarkan peran pengguna
            if user_role == 'admin':
                App.get_running_app().root.current = 'product_list'
            elif user_role == 'petugas':
                App.get_running_app().root.current = 'petugas_screen'
            elif user_role == 'pengguna':
                App.get_running_app().root.current = 'pengguna_screen'
        else:
            print(message)  # Anda dapat mengganti ini dengan popup atau notifikasi
            self.show_popup('Gagal', 'gagal login')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


class RegisterScreen(Screen):
    def register(self, email, password):
        success, message = auth_service.register(email, password, role='pengguna')
        if success:
            print(message)  # Feedback saat registrasi berhasil
            App.get_running_app().root.current = 'login'
        else:
            print(message)  # Anda dapat mengganti ini dengan popup atau notifikasi
            self.show_popup('Gagal', 'gagal daftar')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ProductList(name='product_list'))
        sm.add_widget(AddProduct(name='add_product'))
        sm.add_widget(EditProduct(name='edit_product'))
        sm.add_widget(PetugasScreen(name='petugas_screen'))  # Tambahkan layar petugas
        sm.add_widget(PenggunaScreen(name='pengguna_screen'))
        return sm

if __name__ == '__main__':
    MainApp().run()
