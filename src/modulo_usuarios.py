# src/modulo_usuarios.py

import bcrypt
import modulo_utiles as mu

USUARIOS_PATH = "data/pc_usuarios.json"

# ---------------------------
# Registrar un nuevo usuario
# ---------------------------
def registrar_usuario_completo(datos):
    usuarios = mu.leer_json(USUARIOS_PATH)

    if any(u["identificacion"] == datos["identificacion"] for u in usuarios):
        return False

    if any(u["tarjeta"]["numero"] == datos["tarjeta"]["numero"] for u in usuarios):
        return False

    datos["contrasena"] = bcrypt.hashpw(datos["contrasena"].encode(), bcrypt.gensalt()).decode()
    datos["fecha_registro"] = mu.fecha_hora_actual()
    datos["rol"] = "usuario"

    usuarios.append(datos)
    mu.escribir_json(USUARIOS_PATH, usuarios)
    return True

def validar_contrasena(contrasena: str) -> bool:
    """
    Valida si la contraseña es segura:
    - Al menos 8 caracteres
    - Contiene una mayúscula
    - Contiene un número

    Returns:
        bool: True si cumple con los criterios, False si no.
    """
    return (
        len(contrasena) >= 8 and
        any(c.isupper() for c in contrasena) and
        any(c.isdigit() for c in contrasena)
    )

# ---------------------------
# Autenticación
# ---------------------------
def autenticar_usuario(identificacion, contrasena: str) -> dict:
    """
    Autentica un usuario con su identificación y contraseña.
    
    Args:
        identificacion (str): Identificación del usuario
        contrasena (str): Contraseña del usuario
        
    Returns:
        dict: Diccionario con el estado de la autenticación:
            - success (bool): True si la autenticación fue exitosa
            - usuario (dict): Datos del usuario si la autenticación fue exitosa
            - mensaje (str): Mensaje descriptivo del resultado
    """
    try:
        usuarios = mu.leer_json(USUARIOS_PATH)
        if not usuarios:  # Si la lista está vacía
            return {
                "success": False,
                "usuario": None,
                "mensaje": "No hay usuarios registrados en el sistema"
            }
            
        usuario = next((u for u in usuarios if u["identificacion"] == identificacion), None)
        
        if not usuario:
            return {
                "success": False,
                "usuario": None,
                "mensaje": "Usuario no encontrado"
            }
            
        if bcrypt.checkpw(contrasena.encode('utf-8'), usuario["contrasena"].encode('utf-8')):
            return {
                "success": True,
                "usuario": usuario,
                "mensaje": "Autenticación exitosa"
            }
        else:
            return {
                "success": False,
                "usuario": None,
                "mensaje": "Contraseña incorrecta"
            }
    except Exception as e:
        return {
            "success": False,
            "usuario": None,
            "mensaje": f"Error durante la autenticación: {str(e)}"
        }

# ---------------------------
# Actualizar usuario
# ---------------------------
def actualizar_usuario(identificacion, nuevos_datos):
    usuarios = mu.leer_json(USUARIOS_PATH)
    actualizado = False

    for i, u in enumerate(usuarios):
        if u["identificacion"] == identificacion:
            nuevos_datos["contrasena"] = u["contrasena"]  # mantener hash
            nuevos_datos["fecha_registro"] = u["fecha_registro"]
            nuevos_datos["rol"] = u["rol"]
            usuarios[i] = nuevos_datos
            actualizado = True
            break

    if actualizado:
        mu.escribir_json(USUARIOS_PATH, usuarios)
        mu.enviar_correo(
            destino=nuevos_datos["correo"],
            asunto="Actualización de perfil",
            cuerpo=f"Hola {nuevos_datos['nombre']}, tus datos han sido actualizados correctamente."
        )
        return True
    return False

# ---------------------------
# Eliminar usuario
# ---------------------------
def eliminar_usuario(identificacion):
    usuarios = mu.leer_json(USUARIOS_PATH)
    nuevos = [u for u in usuarios if u["identificacion"] != identificacion]
    if len(nuevos) < len(usuarios):
        mu.escribir_json(USUARIOS_PATH, nuevos)
        return True
    return False

# ---------------------------
# Consultar usuario
# ---------------------------
def consultar_usuario(identificacion):
    usuarios = mu.leer_json(USUARIOS_PATH)
    return next((u for u in usuarios if u["identificacion"] == identificacion), None)

# ---------------------------
# Enviar recuperación
# ---------------------------
def enviar_recordatorio_contrasena(correo):
    usuarios = mu.leer_json(USUARIOS_PATH)
    usuario = next((u for u in usuarios if u["correo"] == correo), None)

    if usuario:
        mensaje = f"""Hola {usuario['nombre']},

Has solicitado recuperar tu contraseña.
Este sistema no permite ver tu contraseña por seguridad.
Contacta al administrador para reiniciarla."""
        mu.enviar_correo(correo, "Recuperación de contraseña", mensaje)
        return True
    return False

# ---------------------------
# Cambiar contraseña
# ---------------------------
def actualizar_contrasena(identificacion, nueva):
    usuarios = mu.leer_json(USUARIOS_PATH)
    for u in usuarios:
        if u["identificacion"] == identificacion:
            u["contrasena"] = bcrypt.hashpw(nueva.encode(), bcrypt.gensalt()).decode()
            # 👇 aquí agregas esto
            u.pop("temporal", None)
            mu.escribir_json(USUARIOS_PATH, usuarios)
            return True
    return False

# ---------------------------
# Establecer contraseña temporal
# ---------------------------
def establecer_clave_temporal(correo, nueva_temporal):
    usuarios = mu.leer_json(USUARIOS_PATH)
    for u in usuarios:
        if u["correo"] == correo:
            u["contrasena"] = bcrypt.hashpw(nueva_temporal.encode(), bcrypt.gensalt()).decode()
            u["temporal"] = True  # flag para forzar cambio
            mu.escribir_json(USUARIOS_PATH, usuarios)

            cuerpo = (
                f"Hola {u['nombre']},\n\n"
                f"Tu nueva contraseña temporal es: {nueva_temporal}\n"
                "Esta contraseña es de un solo uso. Debes iniciar sesión y cambiarla inmediatamente."
            )
            mu.enviar_correo(u["correo"], "Contraseña temporal", cuerpo)
            return True
    return False