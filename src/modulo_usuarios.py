# src/modulo_usuarios.py

import bcrypt
import modulo_utiles as mu

USUARIOS_PATH = "data/pc_usuarios.json"

# ---------------------
# Función: Registrar nuevo usuario
# ---------------------
def registrar_usuario(correo: str, contrasena: str, nombre: str, telefono: str, placa: str) -> bool:
    """
    Registra un nuevo usuario si no existe. Retorna True si se registra correctamente.

    Args:
        correo (str): Correo electrónico único
        contrasena (str): Contraseña en texto plano
        nombre (str): Nombre completo
        telefono (str): Teléfono
        placa (str): Placa del vehículo

    Returns:
        bool: True si se registró, False si el correo ya existe.
    """
    usuarios = mu.leer_json(USUARIOS_PATH)

    # Validar si ya existe el correo
    if any(u["correo"] == correo for u in usuarios):
        return False

    # Hashear contraseña
    hashed = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    nuevo_usuario = {
        "correo": correo,
        "contrasena": hashed,
        "nombre": nombre,
        "telefono": telefono,
        "placa": placa,
        "rol": "usuario"
    }

    usuarios.append(nuevo_usuario)
    mu.escribir_json(USUARIOS_PATH, usuarios)
    return True

# ---------------------
# Función: Login de usuario
# ---------------------
def autenticar_usuario(correo: str, contrasena: str) -> dict | None:
    """
    Verifica si las credenciales son válidas.

    Args:
        correo (str): Correo ingresado
        contrasena (str): Contraseña en texto plano

    Returns:
        dict | None: Diccionario del usuario si es válido, None si no.
    """
    usuarios = mu.leer_json(USUARIOS_PATH)
    usuario = next((u for u in usuarios if u["correo"] == correo), None)

    if usuario and bcrypt.checkpw(contrasena.encode('utf-8'), usuario["contrasena"].encode('utf-8')):
        return usuario
    return None

# ---------------------
# Función: Recuperar contraseña (envía por correo)
# ---------------------
def enviar_recordatorio_contrasena(correo: str) -> bool:
    """
    Simula recuperación de contraseña (envío por correo).

    Args:
        correo (str): Correo del usuario

    Returns:
        bool: True si se encontró el usuario y se envió correo, False si no.
    """
    usuarios = mu.leer_json(USUARIOS_PATH)
    usuario = next((u for u in usuarios if u["correo"] == correo), None)

    if usuario:
        mensaje = f"Hola {usuario['nombre']},\n\nHas solicitado recuperar tu contraseña.\n\nEste es un sistema de recuperación. Contacta al administrador para cambiarla."
        mu.enviar_correo(destino=correo, asunto="Recuperación de contraseña", cuerpo=mensaje)
        return True
    return False
