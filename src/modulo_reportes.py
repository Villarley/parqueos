"""
Módulo para la generación y envío de reportes en formato PDF.

Este módulo maneja todas las operaciones relacionadas con reportes:
- Generación de PDFs con contenido personalizado
- Envío de reportes por correo electrónico
- Generación de historiales de uso de espacios
- Formateo de tablas y contenido

El módulo utiliza la biblioteca ReportLab para la generación de PDFs
y requiere acceso a los archivos JSON de datos del sistema.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import modulo_utiles as mu
import os
from datetime import datetime

# Rutas de los archivos de datos
ALQUILERES_PATH = "data/pc_alquileres.json"
MULTAS_PATH = "data/pc_multas.json"
ESPACIOS_PATH = "data/pc_espacios.json"
REPORTE_DIR = "reportes"

def generar_pdf(destinatario, contenido):
    """
    Genera un PDF con contenido de texto plano.
    
    Args:
        destinatario (str): Identificador del destinatario (usado en el nombre del archivo)
        contenido (str): Contenido del PDF en formato texto plano
        
    Returns:
        str: Ruta del archivo PDF generado
        
    Notas:
        - El archivo se guarda en el directorio REPORTE_DIR
        - El nombre del archivo incluye el destinatario y un timestamp
        - Cada línea del contenido se convierte en un párrafo separado
    """
    # Crear directorio si no existe
    if not os.path.exists(REPORTE_DIR):
        os.makedirs(REPORTE_DIR)

    # Generar nombre único para el archivo
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    archivo = f"{REPORTE_DIR}/reporte_{destinatario.replace('@', '_')}_{timestamp}.pdf"

    # Configurar documento
    doc = SimpleDocTemplate(archivo, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    # Convertir cada línea en un párrafo
    for linea in contenido.splitlines():
        elementos.append(Paragraph(linea, styles['Normal']))
        elementos.append(Spacer(1, 4))

    # Generar PDF
    doc.build(elementos)
    return archivo

def enviar_reporte_pdf(destinatario, path_pdf):
    """
    Envía un archivo PDF por correo electrónico.
    
    Args:
        destinatario (str): Correo electrónico del destinatario
        path_pdf (str): Ruta del archivo PDF a enviar
        
    Returns:
        bool: True si el envío fue exitoso, False en caso contrario
        
    Notas:
        - El PDF se envía como adjunto
        - Se incluye un mensaje predeterminado en el cuerpo del correo
        - El nombre del archivo adjunto se mantiene igual al original
    """
    try:
        # Leer archivo PDF
        with open(path_pdf, "rb") as f:
            adjunto = f.read()
            
        # Enviar correo con adjunto
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

def generar_historial_espacios_usados(usuario):
    """
    Genera un PDF con el historial de espacios usados por un usuario.
    
    Args:
        usuario (dict): Datos del usuario para el cual generar el historial
        
    Returns:
        tuple: (exito, resultado) donde:
            - exito (bool): True si se generó el reporte, False en caso contrario
            - resultado (str): Ruta del archivo PDF generado o mensaje de error
            
    El reporte incluye:
        - Información del usuario
        - Tabla con historial de espacios usados
        - Detalles de cada uso (espacio, fechas, estado, costo)
    """
    # Crear directorio si no existe
    if not os.path.exists(REPORTE_DIR):
        os.makedirs(REPORTE_DIR)

    # Obtener alquileres del usuario
    datos = mu.leer_json(ALQUILERES_PATH)
    alquileres_usuario = [a for a in datos if a["usuario"] == usuario["correo"]]

    if not alquileres_usuario:
        return False, "No hay registros de espacios usados para este usuario."

    # Configurar documento
    archivo_pdf = f"{REPORTE_DIR}/historial_espacios_{usuario['identificacion']}.pdf"
    doc = SimpleDocTemplate(archivo_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    # Agregar encabezado
    titulo = Paragraph("Historial de Espacios Usados", styles['Heading1'])
    usuario_info = Paragraph(
        f"Usuario: {usuario['nombre']} {usuario['apellidos']}<br/>"
        f"Correo: {usuario['correo']}", styles['Normal'])

    elementos.append(titulo)
    elementos.append(usuario_info)
    elementos.append(Spacer(1, 12))

    # Crear tabla de datos
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

    # Configurar estilo de la tabla
    tabla = Table(tabla_datos, hAlign='LEFT')
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco en encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar todo el contenido
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Líneas de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
    ]))

    elementos.append(tabla)
    doc.build(elementos)
    return True, archivo_pdf
