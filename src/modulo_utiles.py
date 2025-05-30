# src/modulo_utiles.py

import json
import re
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------
# Manejo de Archivos JSON
# ---------------------

def leer_json(path: str) -> dict | list:
    """
    Lee un archivo JSON desde la ruta dada y retorna su contenido.
    
    Args:
        path (str): Ruta del archivo JSON.

    Returns:
        dict | list: Contenido del JSON. Retorna {} o [] si hay error.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {} if path.endswith('.json') else []

def escribir_json(path: str, data: dict | list) -> None:
    """
    Escribe datos en un archivo JSON en formato legible.
    
    Args:
        path (str): Ruta del archivo JSON.
        data (dict | list): Datos a escribir.
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# ---------------------
# Validaciones
# ---------------------

def validar_correo(correo: str) -> bool:
    """
    Valida si el correo electrónico tiene formato válido.

    Args:
        correo (str): Correo a validar.

    Returns:
        bool: True si es válido, False en caso contrario.
    """
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

def validar_contrasena(contrasena: str) -> bool:
    """
    Valida si la contraseña es segura:
    - Al menos 8 caracteres
    - Contiene una mayúscula
    - Contiene un número

    Args:
        contrasena (str): Contraseña a validar.

    Returns:
        bool: True si cumple con los criterios, False si no.
    """
    return (
        len(contrasena) >= 8 and
        any(c.isupper() for c in contrasena) and
        any(c.isdigit() for c in contrasena)
    )

def validar_telefono(tel: str) -> bool:
    """
    Valida si el teléfono contiene exactamente 10 dígitos.

    Args:
        tel (str): Teléfono a validar.

    Returns:
        bool: True si es válido, False en caso contrario.
    """
    return re.fullmatch(r'\d{10}', tel) is not None

# ---------------------
# Fecha y Hora Actual
# ---------------------

def fecha_hora_actual() -> str:
    """
    Devuelve la fecha y hora actual con formato: DD/MM/YYYY HH:MM

    Returns:
        str: Fecha y hora como string.
    """
    ahora = datetime.now()
    return ahora.strftime('%d/%m/%Y %H:%M')

# ---------------------
# Envío de Correos
# ---------------------

def enviar_correo(destino: str, asunto: str, cuerpo: str) -> None:
    """
    Envía un correo electrónico usando SMTP.

    Args:
        destino (str): Dirección del destinatario.
        asunto (str): Asunto del correo.
        cuerpo (str): Contenido del mensaje.
    """
    remitente = 'tucorreo@gmail.com'
    clave = 'tu_clave_app'  # Usa clave de aplicación para Gmail

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destino
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, clave)
        servidor.send_message(mensaje)
        servidor.quit()
        print("Correo enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
