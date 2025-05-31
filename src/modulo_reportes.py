from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import modulo_utiles as mu
import os
from datetime import datetime

ALQUILERES_PATH = "data/pc_alquileres.json"
MULTAS_PATH = "data/pc_multas.json"
ESPACIOS_PATH = "data/pc_espacios.json"
REPORTE_DIR = "reportes"

# --------------------------------------------------
# Generar PDF genérico (texto plano en líneas)
# --------------------------------------------------
def generar_pdf(destinatario, contenido):
    if not os.path.exists(REPORTE_DIR):
        os.makedirs(REPORTE_DIR)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    archivo = f"{REPORTE_DIR}/reporte_{destinatario.replace('@', '_')}_{timestamp}.pdf"

    doc = SimpleDocTemplate(archivo, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    for linea in contenido.splitlines():
        elementos.append(Paragraph(linea, styles['Normal']))
        elementos.append(Spacer(1, 4))

    doc.build(elementos)
    return archivo

# --------------------------------------------------
# Enviar PDF por correo
# --------------------------------------------------
def enviar_reporte_pdf(destinatario, path_pdf):
    try:
        print(destinatario)
        with open(path_pdf, "rb") as f:
            adjunto = f.read()
        return mu.enviar_correo_con_adjunto_binario(
            destino=destinatario,
            asunto="Reporte de usuario",
            cuerpo="Adjunto encontrarás tu reporte solicitado.",
            adjunto=adjunto,
            nombre_adjunto=os.path.basename(path_pdf)
        )
    except Exception as e:
        print(f"Error al enviar PDF: {e}")
        return False

# --------------------------------------------------
# Generar historial de espacios usados en tabla
# --------------------------------------------------
def generar_historial_espacios_usados(usuario):
    if not os.path.exists(REPORTE_DIR):
        os.makedirs(REPORTE_DIR)

    datos = mu.leer_json(ALQUILERES_PATH)
    alquileres_usuario = [a for a in datos if a["usuario"] == usuario["correo"]]

    if not alquileres_usuario:
        return False, "No hay registros de espacios usados para este usuario."

    archivo_pdf = f"{REPORTE_DIR}/historial_espacios_{usuario['identificacion']}.pdf"
    doc = SimpleDocTemplate(archivo_pdf, pagesize=A4)

    styles = getSampleStyleSheet()
    elementos = []

    titulo = Paragraph("Historial de Espacios Usados", styles['Heading1'])
    usuario_info = Paragraph(
        f"Usuario: {usuario['nombre']} {usuario['apellidos']}<br/>"
        f"Correo: {usuario['correo']}", styles['Normal'])

    elementos.append(titulo)
    elementos.append(usuario_info)
    elementos.append(Spacer(1, 12))

    tabla_datos = [["Espacio", "Inicio", "Fin", "Estado", "Costo"]]
    for a in alquileres_usuario:
        fila = [
            a["espacio_id"],
            a["inicio"],
            a["fin"],
            a["estado"].capitalize(),
            f"¢{a['costo_total']:.2f}"
        ]
        tabla_datos.append(fila)

    tabla = Table(tabla_datos, hAlign='LEFT')
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    elementos.append(tabla)
    doc.build(elementos)
    return True, archivo_pdf
