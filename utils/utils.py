import bcrypt
from cryptography.fernet import Fernet
import requests
import os
import pandas as pd
from reportlab.pdfgen import canvas

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


def generar_excel(datos, nombre_archivo="reporte.xlsx"):
    try:
        df = pd.DataFrame(datos)
        df.to_excel(nombre_archivo, index=False)
        print(f"Excel generado: {nombre_archivo}")
    except Exception as e:
        print(f"Error generando Excel: {e}")

def generar_pdf(titulo, texto_lista, nombre_archivo="reporte.pdf"):
    try:
        c = canvas.Canvas(nombre_archivo)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, f"EcoTech Solutions - {titulo}")
        
        c.setFont("Helvetica", 12)
        y = 750
        for linea in texto_lista:
            c.drawString(50, y, str(linea))
            y -= 20
            if y < 50: 
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 800
        c.save()
        print(f"PDF generado exitosamente: {nombre_archivo}")
    except Exception as e:
        print(f"Error generando PDF: {e}")