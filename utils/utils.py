import bcrypt
from cryptography.fernet import Fernet
import requests
import os

def cargar_clave():
    key_path = "config/secret.key"
    if not os.path.exists(key_path):
        os.makedirs("config", exist_ok=True)
        clave = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(clave)
    return open(key_path, "rb").read()

KEY = cargar_clave()
cipher_suite = Fernet(KEY)

def encriptar_dato(dato):
    if not dato: return None
    return cipher_suite.encrypt(dato.encode()).decode()

def desencriptar_dato(dato_enc):
    if not dato_enc: return None
    try:
        return cipher_suite.decrypt(dato_enc.encode()).decode()
    except:
        return "Error: Dato corrupto"

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def consultar_indicadores(indicador, fecha=None):
    url = f'https://mindicador.cl/api/{indicador}'
    if fecha:
        url += f'/{fecha}'
        
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None, "Error API"
            
        data = response.json()
        
        if fecha:
            if 'serie' in data and len(data['serie']) > 0:
                valor = data['serie'][0]['valor']
                fecha_resp = data['serie'][0]['fecha']
                return valor, fecha_resp
            else:
                return None, "No hay datos para esa fecha"
        else:
            val = data['serie'][0]['valor']
            fec = data['serie'][0]['fecha']
            return val, fec
            
    except Exception as e:
        return None, str(e)


