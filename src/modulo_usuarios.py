# src/modulo_usuarios.py

"""
Módulo para la gestión de usuarios del sistema de parqueos.

Este módulo maneja todas las operaciones relacionadas con los usuarios:
- Registro de nuevos usuarios
- Autenticación
- Actualización de datos
- Gestión de contraseñas
- Recuperación de acceso

El módulo utiliza un archivo JSON para almacenar la información de usuarios (pc_usuarios.json).
Las contraseñas se almacenan de forma segura usando bcrypt para el hashing.
"""

import bcrypt
import modulo_utiles as mu

# Ruta del archivo de usuarios
USUARIOS_PATH = "data/pc_usuarios.json"

# ---------------------------
# Registrar un nuevo usuario
# ---------------------------
def registrar_usuario_completo(datos):
    """
    Registra un nuevo usuario en el sistema.
    
    Args:
        datos (dict): Diccionario con los datos del usuario:
            - identificacion (str): Número de identificación
            - nombre (str): Nombre completo
            - correo (str): Correo electrónico
            - contrasena (str): Contraseña en texto plano
            - tarjeta (dict): Datos de la tarjeta de pago
    
    Returns:
        bool: True si el registro fue exitoso, False en caso contrario
        
    Validaciones:
        - La identificación no debe estar registrada
        - El número de tarjeta no debe estar registrado
        - La contraseña debe cumplir con los requisitos de seguridad
    """
    usuarios = mu.leer_json(USUARIOS_PATH)

    # Validar identificación única
    if any(u["identificacion"] == datos["identificacion"] for u in usuarios):
        return False

    # Validar tarjeta única
    if any(u["tarjeta"]["numero"] == datos["tarjeta"]["numero"] for u in usuarios):
        return False

    # Hashear contraseña y agregar datos adicionales
    datos["contrasena"] = bcrypt.hashpw(datos["contrasena"].encode(), bcrypt.gensalt()).decode()
    datos["fecha_registro"] = mu.fecha_hora_actual()
    datos["rol"] = "usuario"

    # Guardar usuario
    usuarios.append(datos)
    mu.escribir_json(USUARIOS_PATH, usuarios)
    return True

def validar_contrasena(contrasena: str) -> bool:
    """
    Valida si la contraseña cumple con los requisitos de seguridad.
    
    Args:
        contrasena (str): Contraseña a validar
    
    Returns:
        bool: True si cumple con los criterios, False si no
        
    Requisitos:
        - Al menos 8 caracteres
        - Contiene al menos una letra mayúscula
        - Contiene al menos un número
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
            
        # Buscar usuario por identificación
        usuario = next((u for u in usuarios if u["identificacion"] == identificacion), None)
        
        if not usuario:
            return {
                "success": False,
                "usuario": None,
                "mensaje": "Usuario no encontrado"
            }
            
        # Verificar contraseña
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
    """
    Actualiza los datos de un usuario existente.
    
    Args:
        identificacion (str): Identificación del usuario a actualizar
        nuevos_datos (dict): Nuevos datos del usuario
        
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
        
    Notas:
        - Mantiene la contraseña actual
        - Mantiene la fecha de registro
        - Mantiene el rol del usuario
        - Envía correo de confirmación al usuario
    """
    usuarios = mu.leer_json(USUARIOS_PATH)
    actualizado = False

    # Buscar y actualizar usuario
    for i, u in enumerate(usuarios):
        if u["identificacion"] == identificacion:
            # Mantener datos sensibles
            nuevos_datos["contrasena"] = u["contrasena"]
            nuevos_datos["fecha_registro"] = u["fecha_registro"]
            nuevos_datos["rol"] = u["rol"]
            usuarios[i] = nuevos_datos
            actualizado = True
            break

    if actualizado:
        # Guardar cambios y notificar
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
    """
    Elimina un usuario del sistema.
    
    Args:
        identificacion (str): Identificación del usuario a eliminar
        
    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario
    """
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
    """
    Consulta los datos de un usuario.
    
    Args:
        identificacion (str): Identificación del usuario a consultar
        
    Returns:
        dict | None: Datos del usuario si existe, None en caso contrario
    """
    usuarios = mu.leer_json(USUARIOS_PATH)
    return next((u for u in usuarios if u["identificacion"] == identificacion), None)

# ---------------------------
# Enviar recuperación
# ---------------------------
def enviar_recordatorio_contrasena(correo):
    """
    Envía un correo de recuperación de contraseña.
    
    Args:
        correo (str): Correo electrónico del usuario
        
    Returns:
        bool: True si el correo fue enviado, False en caso contrario
        
    Notas:
        - No envía la contraseña actual por seguridad
        - Instruye al usuario a contactar al administrador
    """
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
    """
    Actualiza la contraseña de un usuario.
    
    Args:
        identificacion (str): Identificación del usuario
        nueva (str): Nueva contraseña en texto plano
        
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
        
    Notas:
        - La nueva contraseña se hashea antes de guardar
        - Se elimina el flag de contraseña temporal si existe
    """
    usuarios = mu.leer_json(USUARIOS_PATH)
    for u in usuarios:
        if u["identificacion"] == identificacion:
            u["contrasena"] = bcrypt.hashpw(nueva.encode(), bcrypt.gensalt()).decode()
            u.pop("temporal", None)  # Eliminar flag de temporal si existe
            mu.escribir_json(USUARIOS_PATH, usuarios)
            return True
    return False

# ---------------------------
# Establecer contraseña temporal
# ---------------------------
def establecer_clave_temporal(correo, nueva_temporal):
    """
    Establece una contraseña temporal para un usuario.
    
    Args:
        correo (str): Correo electrónico del usuario
        nueva_temporal (str): Nueva contraseña temporal
        
    Returns:
        bool: True si se estableció la contraseña temporal, False en caso contrario
        
    Notas:
        - La contraseña temporal se hashea antes de guardar
        - Se marca como temporal para forzar su cambio
        - Se envía por correo al usuario
    """
    usuarios = mu.leer_json(USUARIOS_PATH)
    for u in usuarios:
        if u["correo"] == correo:
            # Actualizar contraseña y marcar como temporal
            u["contrasena"] = bcrypt.hashpw(nueva_temporal.encode(), bcrypt.gensalt()).decode()
            u["temporal"] = True
            
            # Guardar cambios
            mu.escribir_json(USUARIOS_PATH, usuarios)

            # Notificar al usuario
            cuerpo = (
                f"Hola {u['nombre']},\n\n"
                f"Tu nueva contraseña temporal es: {nueva_temporal}\n"
                "Esta contraseña es de un solo uso. Debes iniciar sesión y cambiarla inmediatamente."
            )
            mu.enviar_correo(u["correo"], "Contraseña temporal", cuerpo)
            return True
    return False