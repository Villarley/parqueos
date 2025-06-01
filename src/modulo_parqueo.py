# src/modulo_parqueo.py

from datetime import datetime, timedelta
import uuid
import modulo_utiles as mu

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
def alquilar_espacio(correo_usuario: str, id_espacio: str, minutos: int, placa: str) -> bool:
    espacios = mu.leer_json(ESPACIOS_PATH)
    alquileres = mu.leer_json(ALQUILERES_PATH)
    config = mu.leer_json(CONFIG_PATH)

    espacio = next((e for e in espacios if e["id"] == id_espacio), None)
    if not espacio:
        return False

    if minutos < config["tiempo_minimo"]:
        return False

    inicio = datetime.now()
    fin = inicio + timedelta(minutes=minutos)
    costo = round((minutos / 60) * config["tarifa"], 2)

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
    espacio["estado"] = "ocupado"

    mu.escribir_json(ALQUILERES_PATH, alquileres)
    mu.escribir_json(ESPACIOS_PATH, espacios)

    # Enviar correo de confirmación
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

    # Enviar correo confirmando la extensión
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
# ----------------------------
# Obtener alquiler activo por usuario
# ----------------------------
def obtener_alquiler_activo(correo_usuario: str) -> dict | None:
    alquileres = mu.leer_json(ALQUILERES_PATH)
    return next((a for a in alquileres if a["usuario"] == correo_usuario and a["estado"] == "activo"), None)
def verificar_estado_espacio(id_espacio: str) -> str:
    """
    Devuelve el estado actual del espacio:
    - 'libre'
    - 'ocupado'
    - 'no_existe'
    """
    espacios = mu.leer_json(ESPACIOS_PATH)
    espacio = next((e for e in espacios if e["id"] == id_espacio), None)
    if not espacio:
        return "no_existe"
    return espacio["estado"]
# ----------------------------
# Verificar multas por tiempo excedido
# ----------------------------
def verificar_multas():
    alquileres = mu.leer_json(ALQUILERES_PATH)
    espacios = mu.leer_json(ESPACIOS_PATH)
    multas = mu.leer_json("data/pc_multas.json")

    ahora = datetime.now()
    cambios = False

    for alquiler in alquileres:
        if alquiler["estado"] == "activo":
            fin = datetime.strptime(alquiler["fin"], "%d/%m/%Y %H:%M")
            if ahora > fin:
                alquiler["estado"] = "finalizado"

                espacio = next((e for e in espacios if e["id"] == alquiler["espacio_id"]), None)
                if espacio:
                    espacio["estado"] = "libre"

                multa = {
                    "correo": alquiler["usuario"],
                    "espacio": alquiler["espacio_id"],
                    "fecha": ahora.strftime("%d/%m/%Y %H:%M"),
                    "placa": alquiler.get("placa", "N/D"),  # Si decides registrar placas
                    "detalle": "Tiempo de parqueo excedido sin desaparcar"
                }
                multas.append(multa)
                cambios = True

                # Enviar correo al usuario
                mu.enviar_correo(
                    destino=alquiler["usuario"],
                    asunto="Multa por exceder tiempo",
                    cuerpo=f"Se registró una multa por no desaparcar a tiempo en el espacio {alquiler['espacio_id']}."
                )

    if cambios:
        mu.escribir_json(ALQUILERES_PATH, alquileres)
        mu.escribir_json(ESPACIOS_PATH, espacios)
        mu.escribir_json("data/pc_multas.json", multas)
