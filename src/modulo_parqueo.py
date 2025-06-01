# src/modulo_parqueo.py

"""
Módulo principal para la gestión de parqueos callejeros.

Este módulo maneja todas las operaciones relacionadas con los espacios de parqueo:
- Alquiler de espacios
- Liberación de espacios
- Extensión de tiempo
- Verificación de multas
- Gestión de estados de espacios

El módulo utiliza archivos JSON para almacenar:
- Información de espacios (pc_espacios.json)
- Registro de alquileres (pc_alquileres.json)
- Configuración del sistema (pc_configuracion.json)
"""

from datetime import datetime, timedelta
import uuid
import modulo_utiles as mu

# Rutas de los archivos de datos
ESPACIOS_PATH = "data/pc_espacios.json"
ALQUILERES_PATH = "data/pc_alquileres.json"
CONFIG_PATH = "data/pc_configuracion.json"

# ----------------------------
# Buscar espacios disponibles
# ----------------------------
def obtener_espacios_disponibles() -> list:
    """
    Obtiene la lista de IDs de espacios disponibles para alquilar.
    
    Un espacio se considera disponible si:
    - Está habilitado (habilitado = "S")
    - No tiene usuario asignado (usuario = "")
    
    Returns:
        list: Lista de IDs de espacios disponibles
    """
    espacios = mu.leer_json(ESPACIOS_PATH)
    return [int(id_espacio) for id_espacio, datos in espacios.items() 
            if datos["habilitado"] == "S" and datos["usuario"] == ""]

# ----------------------------
# Alquilar espacio
# ----------------------------
def alquilar_espacio(correo_usuario: str, id_espacio: int, minutos: int, placa: str) -> bool:
    """
    Alquila un espacio de parqueo para un usuario.
    
    Args:
        correo_usuario (str): Correo electrónico del usuario
        id_espacio (int): ID del espacio a alquilar
        minutos (int): Duración del alquiler en minutos
        placa (str): Placa del vehículo
    
    Returns:
        bool: True si el alquiler fue exitoso, False en caso contrario
        
    Validaciones:
        - El espacio debe existir
        - El espacio debe estar habilitado y libre
        - El tiempo mínimo debe cumplir con la configuración
    """
    espacios = mu.leer_json(ESPACIOS_PATH)
    alquileres = mu.leer_json(ALQUILERES_PATH)
    config = mu.leer_json(CONFIG_PATH)

    # Validar existencia y disponibilidad del espacio
    id_espacio_str = str(id_espacio)
    if id_espacio_str not in espacios:
        return False

    espacio = espacios[id_espacio_str]
    if espacio["habilitado"] != "S" or espacio["usuario"] != "":
        return False

    # Validar tiempo mínimo
    if minutos < config["tiempo_minimo"]:
        return False

    # Calcular fechas y costo
    inicio = datetime.now()
    fin = inicio + timedelta(minutes=minutos)
    costo = round((minutos / 60) * config["tarifa"], 2)

    # Crear registro de alquiler
    nuevo = {
        "id": str(uuid.uuid4()),
        "espacio_id": id_espacio,
        "usuario": correo_usuario,
        "inicio": inicio.strftime("%d/%m/%Y %H:%M"),
        "fin": fin.strftime("%d/%m/%Y %H:%M"),
        "estado": "activo",
        "costo_total": costo,
        "placa": placa
    }

    alquileres.append(nuevo)
    
    # Actualizar estado del espacio
    espacio["usuario"] = correo_usuario
    espacio["placa"] = placa
    espacio["inicio"] = inicio.strftime("%d/%m/%Y %H:%M")
    espacio["tiempo"] = minutos
    espacio["fin"] = fin.strftime("%d/%m/%Y %H:%M")

    # Guardar cambios
    mu.escribir_json(ALQUILERES_PATH, alquileres)
    mu.escribir_json(ESPACIOS_PATH, espacios)

    # Notificar al usuario
    cuerpo = (
        f"Hola,\n\nHas alquilado el espacio {id_espacio}.\n"
        f"Placa: {placa}\n"
        f"Inicio: {nuevo['inicio']}\n"
        f"Fin: {nuevo['fin']}\n"
        f"Duración: {minutos} minutos\n"
        f"Costo total: ₡{costo}\n\n"
        f"Gracias por usar el sistema de parqueos."
    )
    mu.enviar_correo(destino=correo_usuario, asunto="Confirmación de alquiler", cuerpo=cuerpo)

    return True

# ----------------------------
# Agregar tiempo
# ----------------------------
def agregar_tiempo_alquiler(id_alquiler: str, minutos_extra: int) -> bool:
    """
    Extiende el tiempo de un alquiler activo.
    
    Args:
        id_alquiler (str): ID del alquiler a extender
        minutos_extra (int): Minutos adicionales a agregar
    
    Returns:
        bool: True si la extensión fue exitosa, False en caso contrario
        
    Validaciones:
        - El alquiler debe existir y estar activo
        - El espacio asociado debe existir
    """
    alquileres = mu.leer_json(ALQUILERES_PATH)
    espacios = mu.leer_json(ESPACIOS_PATH)
    config = mu.leer_json(CONFIG_PATH)

    # Buscar alquiler activo
    alquiler = next((a for a in alquileres if a["id"] == id_alquiler and a["estado"] == "activo"), None)
    if not alquiler:
        return False

    # Calcular nuevo tiempo final y costo adicional
    fin_actual = datetime.strptime(alquiler["fin"], "%d/%m/%Y %H:%M")
    nuevo_fin = fin_actual + timedelta(minutes=minutos_extra)
    costo_extra = round((minutos_extra / 60) * config["tarifa"], 2)

    # Actualizar alquiler
    alquiler["fin"] = nuevo_fin.strftime("%d/%m/%Y %H:%M")
    alquiler["costo_total"] += costo_extra

    # Actualizar espacio
    espacio = espacios[str(alquiler["espacio_id"])]
    espacio["tiempo"] += minutos_extra
    espacio["fin"] = nuevo_fin.strftime("%d/%m/%Y %H:%M")

    # Guardar cambios
    mu.escribir_json(ALQUILERES_PATH, alquileres)
    mu.escribir_json(ESPACIOS_PATH, espacios)

    # Notificar al usuario
    mu.enviar_correo(
        destino=alquiler["usuario"],
        asunto="Tiempo de parqueo extendido",
        cuerpo=(
            f"Se agregó {minutos_extra} minutos al alquiler en el espacio {alquiler['espacio_id']}.\n"
            f"Nuevo tiempo final: {alquiler['fin']}\n"
            f"Nuevo costo total: ₡{alquiler['costo_total']}"
        )
    )

    return True

# ----------------------------
# Desaparcar (liberar)
# ----------------------------
def liberar_espacio(id_alquiler: str) -> bool:
    """
    Libera un espacio de parqueo, finalizando el alquiler activo.
    
    Args:
        id_alquiler (str): ID del alquiler a finalizar
    
    Returns:
        bool: True si la liberación fue exitosa, False en caso contrario
        
    Validaciones:
        - El alquiler debe existir y estar activo
        - El espacio asociado debe existir
    """
    alquileres = mu.leer_json(ALQUILERES_PATH)
    espacios = mu.leer_json(ESPACIOS_PATH)

    # Buscar alquiler activo
    alquiler = next((a for a in alquileres if a["id"] == id_alquiler and a["estado"] == "activo"), None)
    if not alquiler:
        return False

    espacio_id = str(alquiler["espacio_id"])
    if espacio_id not in espacios:
        return False

    # Finalizar alquiler
    alquiler["estado"] = "finalizado"
    
    # Liberar espacio
    espacio = espacios[espacio_id]
    espacio["usuario"] = ""
    espacio["placa"] = ""
    espacio["inicio"] = ""
    espacio["tiempo"] = 0
    espacio["fin"] = ""

    # Guardar cambios
    mu.escribir_json(ALQUILERES_PATH, alquileres)
    mu.escribir_json(ESPACIOS_PATH, espacios)
    return True

# ----------------------------
# Obtener alquiler activo por usuario
# ----------------------------
def obtener_alquiler_activo(correo_usuario: str) -> dict | None:
    """
    Obtiene el alquiler activo de un usuario.
    
    Args:
        correo_usuario (str): Correo electrónico del usuario
    
    Returns:
        dict | None: Diccionario con la información del alquiler activo, o None si no hay alquiler activo
    """
    alquileres = mu.leer_json(ALQUILERES_PATH)
    return next((a for a in alquileres if a["usuario"] == correo_usuario and a["estado"] == "activo"), None)

def verificar_estado_espacio(id_espacio: int) -> str:
    """
    Verifica el estado actual de un espacio de parqueo.
    
    Args:
        id_espacio (int): ID del espacio a verificar
    
    Returns:
        str: Estado del espacio:
            - 'libre': Espacio disponible para alquilar
            - 'ocupado': Espacio actualmente en uso
            - 'no_existe': Espacio no existe o no está habilitado
    """
    espacios = mu.leer_json(ESPACIOS_PATH)
    id_espacio_str = str(id_espacio)
    if id_espacio_str not in espacios:
        return "no_existe"
    
    espacio = espacios[id_espacio_str]
    if espacio["habilitado"] != "S":
        return "no_existe"
    return "ocupado" if espacio["usuario"] else "libre"

# ----------------------------
# Verificar multas por tiempo excedido
# ----------------------------
def verificar_multas():
    """
    Verifica y procesa multas por tiempo excedido en alquileres activos.
    
    Este método:
    1. Revisa todos los alquileres activos
    2. Identifica aquellos que han excedido su tiempo
    3. Genera multas automáticamente
    4. Libera los espacios correspondientes
    5. Notifica a los usuarios afectados
    
    Las multas se generan cuando:
    - El tiempo actual es mayor al tiempo final del alquiler
    - El alquiler aún está marcado como activo
    """
    alquileres = mu.leer_json(ALQUILERES_PATH)
    espacios = mu.leer_json(ESPACIOS_PATH)
    multas = mu.leer_json("data/pc_multas.json")

    ahora = datetime.now()
    cambios = False

    for alquiler in alquileres:
        if alquiler["estado"] == "activo":
            fin = datetime.strptime(alquiler["fin"], "%d/%m/%Y %H:%M")
            if ahora > fin:
                # Finalizar alquiler
                alquiler["estado"] = "finalizado"

                # Liberar espacio
                espacio_id = str(alquiler["espacio_id"])
                if espacio_id in espacios:
                    espacio = espacios[espacio_id]
                    espacio["usuario"] = ""
                    espacio["placa"] = ""
                    espacio["inicio"] = ""
                    espacio["tiempo"] = 0
                    espacio["fin"] = ""

                # Generar multa
                multa = {
                    "correo": alquiler["usuario"],
                    "espacio": alquiler["espacio_id"],
                    "fecha": ahora.strftime("%d/%m/%Y %H:%M"),
                    "placa": alquiler.get("placa", "N/D"),
                    "detalle": "Tiempo de parqueo excedido sin desaparcar"
                }
                multas.append(multa)
                cambios = True

                # Notificar al usuario
                mu.enviar_correo(
                    destino=alquiler["usuario"],
                    asunto="Multa por exceder tiempo",
                    cuerpo=f"Se registró una multa por no desaparcar a tiempo en el espacio {alquiler['espacio_id']}."
                )

    # Guardar cambios si hubo multas
    if cambios:
        mu.escribir_json(ALQUILERES_PATH, alquileres)
        mu.escribir_json(ESPACIOS_PATH, espacios)
        mu.escribir_json("data/pc_multas.json", multas)
