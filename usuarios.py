import random
import sqlite3
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime



def generar_codigo():
    return random.randint(111111, 999999)

def obtener_fecha():
    fecha = datetime.now()
    return fecha.strftime('%d-%m-%Y')


def verificar_usuario(correo):
        conexion = None
        try:
            conexion = sqlite3.connect('database/database.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT correo FROM Usuarios WHERE correo == (?)', (correo,))
            resultados = cursor.fetchone()
            conexion.close()
            if resultados != None:
                return True
            else:
                return False
        except sqlite3.Error as e:
            return f'Se produjo un error al procesar tu solicitud. Por favor, intenta nuevamente {e}'
        finally:
            if conexion:
                conexion.close()


class Usuarios:
    def __init__(self, nombre, correo, dirreccion):
        self.nombre = nombre
        self.correo = correo
        self.direccion = dirreccion
        
        
    def verificar_mail(correo):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            return False
        
        parte_local, dominio = correo.rsplit('@', 1)
        
        if '..' in parte_local or parte_local.startswith('.') or parte_local.endswith('.'):
            return False
        
        if len(correo) > 320 or len(parte_local) > 64 or len(dominio) > 255:
            return False
        
        if '.' not in dominio or dominio.startswith('.') or dominio.endswith('.'):
            return False
    
        return True
        
        
    def enviar_mail(self, codigo):
        correo_origen = "pixelcircuit2@gmail.com"  # Tu correo de origen
        contraseña = "skup hhzx avhl liep"  # Contraseña de aplicación generada para Gmail
        correo_destino = self.correo
        asunto = 'Codigo de verificacion'
        mensaje = f'Hola {self.nombre} su codigo de verificacion es {codigo}'
        try:
            # Crear el mensaje
            msg = MIMEMultipart()
            msg['From'] = correo_origen
            msg['To'] = correo_destino
            msg['Subject'] = asunto
            msg.attach(MIMEText(mensaje, 'plain'))
            # Conexión con el servidor SMTP de Gmail
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()  # Usar conexión segura
            servidor.login(correo_origen, contraseña)
            servidor.send_message(msg)
            servidor.quit()
            return f'Enviamos un codigo de verificacion al correo {self.correo}'
        except Exception:
            return f"Ah ocurrido un error al enviar el correo de confimacion"
        
    def registrar_usuario(self):
        conexion = None
        try:
            correo = self.correo
            conexion = sqlite3.connect('database/database.db')
            cursor = conexion.cursor()
            if verificar_usuario(correo) == True:
                return f'El correo ya esta asociado a una cuenta'
            else:
                cursor.execute('INSERT INTO Usuarios(nombre, correo, direccion) VALUES(?, ?, ?)', (self.nombre, self.correo, self.direccion,))
                conexion.commit()
                conexion.close()
            return 'Registro exitoso'
        except sqlite3.Error:
            return f'Se produjo un error al procesar tu solicitud. Por favor, intenta nuevamente.'
        finally:
            if conexion:
                conexion.close()
            
                
    def iniciar_sesion(self):
        conexion = None
        try:
            conexion = sqlite3.connect('database/database.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM Usuarios WHERE nombre == (?) AND correo == (?)', (self.nombre, self.correo,))
            resultado = cursor.fetchone()
            conexion.close()
            if resultado:
                return f'Bienvenido {self.nombre}'
            else:
                return f'Usuario o Correo incorrectos'
        except sqlite3.Error:
            return f'Se produjo un error al procesar tu solicitud. Por favor, intenta nuevamente.'
        finally:
            if conexion:
                conexion.close()
                
                
    def obtener_direccion(correo):
        conexion = None
        try:
            conexion = sqlite3.connect('database/database.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT direccion FROM Usuarios WHERE correo == (?)', (correo,))
            resultado = cursor.fetchone()
            conexion.close()
            if resultado:
                return resultado
        except sqlite3.Error:
            return f'Se produjo un error al procesar tu solicitud. Por favor, intenta nuevamente.'
        finally:
            if conexion:
                conexion.close()
    
    
    
    def obtener_id(correo):
        conexion = None
        try:
            conexion = sqlite3.connect('database/database.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT id FROM Usuarios WHERE correo == (?)', (correo,))
            resultado = cursor.fetchone()
            conexion.close()
            if resultado:
                return resultado
        except sqlite3.Error:
            return f'Se produjo un error al procesar tu solicitud. Por favor, intenta nuevamente.'
        finally:
            if conexion:
                conexion.close()
