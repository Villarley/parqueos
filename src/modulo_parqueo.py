# src/modulo_parqueo.py

from datetime import datetime, timedelta
import uuid
from src import modulo_utiles as mu

ESPACIOS_PATH = "data/pc_espacios.json"
ALQUILERES_PATH = "data/pc_alquileres.json"
CONFIG_PATH = "data/pc_configuracion.json"

# ----------------------------
# Buscar espacios disponibles
# ----------------------------
def obtener_espacios_disponibles() -> list:
    espacios = mu.leer_json(ESPACIOS_PATH)
    return [e for e in espacios if e["estado"] == "libre"]

# ----------------------------
# Alquilar espacio
# ----------------------------
def alquilar_espacio(correo_usuario: str, id_espacio: str, minutos: int) -> bool:
    espacios = mu.leer_json(ESPACIOS_PATH)
    alquileres = mu.leer_json(ALQUILERES_PATH)
    config = mu.leer_json(CONFIG_PATH)

    espacio = next((e for e in espacios if e["id"] == id_espacio), None)
    if not espacio or espacio["estado"] != "libre":
        return False

    # Mínimo de tiempo
    if minutos < config["tiempo_minimo"]:
        return False

    inicio = datetime.now()
    fin = inicio + timedelta(minutes=minutos)

    nuevo = {
        "id": str(uuid.uuid4()),
        "espacio_id": id_espacio,
        "usuario": correo_usuario,
        "inicio": inicio.strftime("%d/%m/%Y %H:%M"),
        "fin": fin.strftime("%d/%m/%Y %H:%M"),
        "estado": "activo",
        "costo_total": round((minutos / 60) * config["tarifa"], 2)
    }

    alquileres.append(nuevo)

    # Marcar espacio como ocupado
    espacio["estado"] = "ocupado"

    mu.escribir_json(ALQUILERES_PATH, alquileres)
    mu.escribir_json(ESPACIOS_PATH, espacios)

    return True

# ----------------------------
# Agregar tiempo
# ----------------------------
def agregar_tiempo_alquiler(id_alquiler: str, minutos_extra: int) -> bool:
    alquileres = mu.leer_json(ALQUILERES_PATH)
    config = mu.leer_json(CONFIG_PATH)

    alquiler = next((a for a in alquileres if a["id"] == id_alquiler and a["estado"] == "activo"), None)
    if not alquiler:
        return False

    fin_actual = datetime.strptime(alquiler["fin"], "%d/%m/%Y %H:%M")
    nuevo_fin = fin_actual + timedelta(minutes=minutos_extra)

    alquiler["fin"] = nuevo_fin.strftime("%d/%m/%Y %H:%M")
    alquiler["costo_total"] += round((minutos_extra / 60) * config["tarifa"], 2)

    mu.escribir_json(ALQUILERES_PATH, alquileres)
    return True

# ----------------------------
# Desaparcar (liberar)
# ----------------------------
def liberar_espacio(id_alquiler: str) -> bool:
    alquileres = mu.leer_json(ALQUILERES_PATH)
    espacios = mu.leer_json(ESPACIOS_PATH)

    alquiler = next((a for a in alquileres if a["id"] == id_alquiler and a["estado"] == "activo"), None)
    if not alquiler:
        return False

    espacio = next((e for e in espacios if e["id"] == alquiler["espacio_id"]), None)
    if not espacio:
        return False

    alquiler["estado"] = "finalizado"
    espacio["estado"] = "libre"

    mu.escribir_json(ALQUILERES_PATH, alquileres)
    mu.escribir_json(ESPACIOS_PATH, espacios)
    return True
