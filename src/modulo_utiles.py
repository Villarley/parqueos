# src/modulo_utiles.py

import json
import re
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

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
    return re.fullmatch(r'\d{8}', tel) is not None

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

def enviar_correo(destino: str, asunto: str, cuerpo: str, adjunto: str = None) -> bool:
    """
    Envía un correo electrónico usando SMTP.

    Args:
        destino (str): Dirección del destinatario.
        asunto (str): Asunto del correo.
        cuerpo (str): Contenido del mensaje.
        adjunto (str, optional): Ruta al archivo adjunto. Defaults to None.

    Returns:
        bool: True si el correo se envió correctamente, False en caso contrario.
    """
    remitente = 'santivillarley1010@gmail.com'
    clave = 'vhev updw cwgj dvkv'  # Usa clave de aplicación para Gmail

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destino
    msg['Subject'] = asunto

    msg.attach(MIMEText(cuerpo, 'plain'))

    if adjunto:
        with open(adjunto, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(adjunto))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(adjunto)}"'
            msg.attach(part)

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, clave)
        servidor.send_message(msg)
        servidor.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False
    
# ---------------------
# Envío de Correos (versión con adjunto binario y nombre)
# ---------------------

def enviar_correo_con_adjunto_binario(destino: str, asunto: str, cuerpo: str, adjunto: bytes, nombre_adjunto: str) -> bool:
    remitente = 'santivillarley1010@gmail.com'
    clave = 'vhev updw cwgj dvkv'  # clave de aplicación

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destino
    msg['Subject'] = asunto

    msg.attach(MIMEText(cuerpo, 'plain'))

    if adjunto:
        parte_adjunto = MIMEApplication(adjunto, Name=nombre_adjunto)
        parte_adjunto['Content-Disposition'] = f'attachment; filename="{nombre_adjunto}"'
        msg.attach(parte_adjunto)

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, clave)
        servidor.send_message(msg)
        servidor.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo con adjunto binario: {e}")
        return False
# ---------------------
# Actualización automática de espacios vencidos
# ---------------------

ESPACIOS_PATH = "data/pc_espacios.json"
ALQUILERES_PATH = "data/pc_alquileres.json"

def actualizar_estados_de_parqueo():
    """
    Libera automáticamente espacios vencidos y actualiza alquileres de 'activo' a 'finalizado'.
    """
    espacios = leer_json(ESPACIOS_PATH)
    alquileres = leer_json(ALQUILERES_PATH)
    ahora = datetime.now()

    cambios = False

    for espacio_id, espacio in espacios.items():
        # Buscar alquiler ACTIVO más reciente para este espacio
        alquiler = next(
            (a for a in sorted(alquileres, key=lambda x: x["fin"], reverse=True)
             if a["espacio_id"] == int(espacio_id) and a["estado"] == "activo"),
            None
        )

        if alquiler:
            fin_dt = datetime.strptime(alquiler["fin"], "%d/%m/%Y %H:%M")
            if ahora > fin_dt:
                # Cambiar estado del alquiler
                alquiler["estado"] = "finalizado"
                # Liberar el espacio
                espacio["usuario"] = ""
                espacio["placa"] = ""
                espacio["inicio"] = ""
                espacio["tiempo"] = 0
                espacio["fin"] = ""
                cambios = True

    if cambios:
        escribir_json(ESPACIOS_PATH, espacios)
        escribir_json(ALQUILERES_PATH, alquileres)

def convertir_espacios_a_dict():
    """Convierte el formato de espacios de lista a diccionario"""
    espacios = leer_json("data/pc_espacios.json")
    if isinstance(espacios, list):
        nuevo_formato = {}
        for espacio in espacios:
            nuevo_formato[espacio["id"]] = {
                "habilitado": "S",
                "usuario": "",
                "placa": "",
                "inicio": "",
                "tiempo": 0,
                "fin": ""
            }
            # Si el espacio estaba ocupado, mantener esa información
            if espacio.get("estado") == "ocupado":
                nuevo_formato[espacio["id"]]["usuario"] = espacio.get("usuario", "")
                nuevo_formato[espacio["id"]]["placa"] = espacio.get("placa", "")
                nuevo_formato[espacio["id"]]["inicio"] = espacio.get("inicio", "")
                nuevo_formato[espacio["id"]]["tiempo"] = espacio.get("tiempo", 0)
                nuevo_formato[espacio["id"]]["fin"] = espacio.get("fin", "")
        escribir_json("data/pc_espacios.json", nuevo_formato)
        return nuevo_formato
    return espacios
