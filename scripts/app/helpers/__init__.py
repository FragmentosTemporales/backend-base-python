import json
import os
from app.models import User, UserInfo, Client, Center


basedir = os.path.abspath(os.path.dirname(__file__))

class Installer():
    """Helper to install default info"""
    def __init__(self):
        self.email = os.environ.get("EMAIL")
        self.password = os.environ.get("PASSWORD")
        self.client_data = self.load_data('app/data/client_data.json')
        self.center_data = self.load_data('app/data/center_data.json')
        self.save_user()
        self.save_client()
        self.save_center()
        print("PROCESO FINALIZADO.")

    def load_data(self, url):
        with open(url, 'r') as f:
            data = json.load(f)
        return data
    
    def save_user(self):
        """Save user in DB"""
        print("1/3 INICIANDO CREACION DE ADMIN...")
        user_instance = User(
            email=self.email,
            password=self.password
        )
        user_instance.set_password(self.password)
        user_instance.save_to_db()
        print(f'USER: ', self.email)
        print(f'PASS: ', self.password)

    def save_client(self):
        """Save client in DB"""
        print("2/3 INICIANDO CREACIÓN DE CLIENTE...")
        count = 0
        for client in self.client_data:
            client_instance = Client(**client)
            client_instance.save_to_db()
            count += 1
        print(f'Proceso terminado, {count} objetos procesados.')
    
    def save_center(self):
        """Save center in DB"""
        print("3/3 INICIANDO CREACIÓN DE CENTRO DE TRABAJO...")
        count = 0
        for center in self.center_data:
            center_instante = Center(**center)
            center_instante.save_to_db()
            count += 1
        print(f'Proceso terminado, {count} objetos procesados.')
