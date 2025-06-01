# src/modulo_multas.py

from datetime import datetime
import modulo_utiles as mu
import modulo_reportes as mr

MULTAS_PATH = "data/pc_multas.json"
USUARIOS_PATH = "data/pc_usuarios.json"

def registrar_multa(espacio_id, placa, detalle):
    ahora = datetime.now()
    multa = {
        "fecha": ahora.strftime("%d/%m/%Y %H:%M"),
        "espacio": espacio_id,
        "placa": placa,
        "detalle": detalle,
        "correo": obtener_correo_por_placa(placa)
    }

    multas = mu.leer_json(MULTAS_PATH)
    multas.append(multa)
    mu.escribir_json(MULTAS_PATH, multas)

    path_pdf = mr.generar_pdf(multa["correo"] or placa, f"Multa registrada:\n{detalle}")
    enviado = False
    if multa["correo"]:
        enviado = mr.enviar_reporte_pdf(multa["correo"], path_pdf)

    return multa, enviado

def obtener_correo_por_placa(placa):
    usuarios = mu.leer_json(USUARIOS_PATH)
    for u in usuarios:
        for veh in u.get("vehiculos", []):
            if veh["placa"].upper() == placa.upper():
                return u["correo"]
    return ""
