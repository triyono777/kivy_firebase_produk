import pyrebase
from kivy.app import App

from config import get_firebase_config


config = get_firebase_config()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

class AuthService:
    def login(self, email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = user['localId']
            role = db.child("users").child(user_id).child("role").get().val()

            if role != 'admin':
                print("Access Denied: Only admins can access this application.")
                return False, "Access Denied: Only admins can access this application."
            
            App.get_running_app().user_role = role
            return True, "Login successful"
        except Exception as e:
            print(f"Login failed: {e}")
            return False, str(e)

    def register(self, email, password, role='user'):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']
            db.child("users").child(user_id).set({"email": email, "role": role})
            print("Registration successful")
            return True, "Registration successful"
        except Exception as e:
            print(f"Registration failed: {e}")
            return False, str(e)
