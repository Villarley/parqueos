# src/modulo_multas.py

"""
Módulo para la gestión de multas del sistema de parqueos.

Este módulo maneja todas las operaciones relacionadas con las multas:
- Registro de nuevas multas
- Búsqueda de usuarios por placa
- Generación y envío de reportes PDF

El módulo utiliza archivos JSON para almacenar:
- Registro de multas (pc_multas.json)
- Información de usuarios (pc_usuarios.json)
"""

from datetime import datetime
import modulo_utiles as mu
import modulo_reportes as mr

# Rutas de los archivos de datos
MULTAS_PATH = "data/pc_multas.json"
USUARIOS_PATH = "data/pc_usuarios.json"

def registrar_multa(espacio_id, placa, detalle):
    """
    Registra una nueva multa en el sistema.
    
    Args:
        espacio_id (int): ID del espacio donde se registró la multa
        placa (str): Placa del vehículo multado
        detalle (str): Descripción detallada de la multa
        
    Returns:
        tuple: (multa, enviado) donde:
            - multa (dict): Datos de la multa registrada
            - enviado (bool): True si se envió el correo, False en caso contrario
            
    Proceso:
        1. Crea el registro de la multa con fecha y hora actual
        2. Busca el correo del propietario del vehículo
        3. Genera un PDF con los detalles de la multa
        4. Envía el PDF por correo si se encontró el correo del propietario
    """
    # Crear registro de multa
    ahora = datetime.now()
    multa = {
        "fecha": ahora.strftime("%d/%m/%Y %H:%M"),
        "espacio": espacio_id,
        "placa": placa,
        "detalle": detalle,
        "correo": obtener_correo_por_placa(placa)
    }

    # Guardar multa
    multas = mu.leer_json(MULTAS_PATH)
    multas.append(multa)
    mu.escribir_json(MULTAS_PATH, multas)

    # Generar y enviar reporte
    path_pdf = mr.generar_pdf(multa["correo"] or placa, f"Multa registrada:\n{detalle}")
    enviado = False
    if multa["correo"]:
        enviado = mr.enviar_reporte_pdf(multa["correo"], path_pdf)

    return multa, enviado

def obtener_correo_por_placa(placa):
    """
    Busca el correo electrónico del propietario de un vehículo por su placa.
    
    Args:
        placa (str): Placa del vehículo a buscar
        
    Returns:
        str: Correo electrónico del propietario si se encuentra, cadena vacía en caso contrario
        
    Notas:
        - La búsqueda es case-insensitive (no distingue mayúsculas/minúsculas)
        - Busca en la lista de vehículos de todos los usuarios
    """
    usuarios = mu.leer_json(USUARIOS_PATH)
    for u in usuarios:
        for veh in u.get("vehiculos", []):
            if veh["placa"].upper() == placa.upper():
                return u["correo"]
    return ""
