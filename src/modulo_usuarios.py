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

# ---------------------------
# Autenticación
# ---------------------------
def autenticar_usuario(identificacion, contrasena: str) -> dict | None:
    usuarios = mu.leer_json(USUARIOS_PATH)
    usuario = next((u for u in usuarios if u["identificacion"] == identificacion), None)

    if usuario and bcrypt.checkpw(contrasena.encode('utf-8'), usuario["contrasena"].encode('utf-8')):
        return usuario
    return None

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
