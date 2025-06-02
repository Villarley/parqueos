"""
Módulo para la generación y visualización de reportes administrativos.

Este módulo implementa la interfaz que permite a los administradores:
- Generar reportes de ingresos
- Ver estadísticas de uso
- Exportar reportes en diferentes formatos
- Filtrar reportes por fecha y tipo

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import modulo_utiles as mu
from frames.base_frame import BaseFrame

ALQUILERES_PATH = "data/pc_alquileres.json"
MULTAS_PATH = "data/pc_multas.json"
ESPACIOS_PATH = "data/pc_espacios.json"

class ReportesAdminFrame(BaseFrame):
    """
    Frame para la gestión de reportes administrativos.
    
    Esta clase maneja la interfaz gráfica que permite a los administradores
    generar y visualizar diferentes tipos de reportes del sistema.
    
    Attributes:
        fecha_inicio_var (StringVar): Variable para la fecha de inicio
        fecha_fin_var (StringVar): Variable para la fecha de fin
        tipo_reporte_var (StringVar): Variable para el tipo de reporte
    """
    
    def __init__(self, master, app):
        """
        Inicializa el frame de reportes.
        
        Args:
            master: Widget padre de este frame
            app: Instancia de la aplicación principal
        """
        super().__init__(master)
        self.app = app
        self.reporte_actual = ""
        self.fecha_inicio_var = tk.StringVar()
        self.fecha_fin_var = tk.StringVar()
        self.tipo_reporte_var = tk.StringVar()
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y secciones principales
        - Campos para seleccionar fechas
        - Selector de tipo de reporte
        - Tabla para mostrar resultados
        - Botones de generación y exportación
        """
        # Título y botón volver
        header_frame = tk.Frame(self)
        header_frame.pack(pady=10)

        tk.Label(
            header_frame,
            text="📊 Reportes Administrativos",
            font=("Arial", 16)
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            header_frame,
            text="🔙 Volver",
            command=self.app.volver,
            font=("Arial", 12),
            width=20
        ).pack(side=tk.RIGHT, padx=20)

        tk.Button(self, text="💵 Ingresos por estacionamiento", command=self.reporte_ingresos).pack(pady=5)
        tk.Button(self, text="📋 Lista de espacios de parqueo", command=self.lista_espacios).pack(pady=5)
        tk.Button(self, text="📆 Historial de espacios usados", command=self.historial_usos).pack(pady=5)
        tk.Button(self, text="⚠️ Historial de multas", command=self.historial_multas).pack(pady=5)

        self.text = tk.Text(self, width=80, height=25)
        self.text.pack(pady=10)

        # Frame para filtros
        filtros_frame = tk.Frame(self)
        filtros_frame.pack(pady=10)

        # Fechas
        tk.Label(filtros_frame, text="Fecha inicio:").grid(row=0, column=0, padx=5)
        tk.Entry(filtros_frame, textvariable=self.fecha_inicio_var).grid(row=0, column=1, padx=5)

        tk.Label(filtros_frame, text="Fecha fin:").grid(row=0, column=2, padx=5)
        tk.Entry(filtros_frame, textvariable=self.fecha_fin_var).grid(row=0, column=3, padx=5)

        # Tipo de reporte
        tk.Label(filtros_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=5)
        tipos = ["Ingresos", "Uso", "Multas", "Usuarios"]
        tk.OptionMenu(filtros_frame, self.tipo_reporte_var, *tipos).grid(row=1, column=1, padx=5)

        # Botones
        tk.Button(filtros_frame, text="Generar", command=self.generar_reporte).grid(row=1, column=2, padx=5)
        tk.Button(filtros_frame, text="Exportar", command=self.exportar_reporte).grid(row=1, column=3, padx=5)

        # Tabla de resultados
        self.tabla = ttk.Treeview(self)
        self.tabla.pack(pady=10, fill=tk.BOTH, expand=True)

    # ------------ Reporte 1: Ingresos por fecha ------------
    def reporte_ingresos(self):
        """
        Genera un reporte de ingresos por estacionamiento.
        
        Este método:
        1. Solicita las fechas de inicio y fin
        2. Valida las fechas ingresadas
        3. Obtiene los alquileres del sistema
        4. Calcula los ingresos por día y total
        5. Muestra los resultados en la interfaz
        """
        fecha_inicio = self.fecha_inicio_var.get()
        fecha_fin = self.fecha_fin_var.get()

        if not all([fecha_inicio, fecha_fin]):
            return messagebox.showerror("Error", "Complete todos los campos.")

        try:
            desde_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            hasta_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")
        except ValueError:
            return messagebox.showerror("Error", "Formato incorrecto. Use dd/mm/yyyy")

        alquileres = mu.leer_json(ALQUILERES_PATH)
        ingresos_por_dia = {}
        total = 0

        for a in alquileres:
            fecha_inicio = datetime.strptime(a["inicio"], "%d/%m/%Y %H:%M")
            fecha = fecha_inicio.date()
            if desde_dt.date() <= fecha <= hasta_dt.date():
                ingresos_por_dia.setdefault(str(fecha), 0)
                ingresos_por_dia[str(fecha)] += a.get("costo_total", 0)
                total += a.get("costo_total", 0)

        contenido = "💵 Ingresos por estacionamiento:\n\n"
        for dia in sorted(ingresos_por_dia):
            contenido += f"{dia}: ₡{ingresos_por_dia[dia]:.2f}\n"
        contenido += f"\nTOTAL: ₡{total:.2f}"
        self.actualizar_texto(contenido)

    # ------------ Reporte 2: Lista de espacios ------------
    def lista_espacios(self):
        """
        Genera una lista de espacios de parqueo.
        
        Este método:
        1. Solicita el tipo de lista a mostrar
        2. Obtiene la lista de espacios del sistema
        3. Filtra la lista según el tipo seleccionado
        4. Muestra los resultados en la interfaz
        """
        espacios = mu.leer_json(ESPACIOS_PATH)
        if not isinstance(espacios, dict):
            return messagebox.showerror("Error", "Error leyendo espacios.")

        opciones = {
            "a": "Mostrar todos",
            "b": "Mostrar ocupados",
            "c": "Mostrar vacíos"
        }

        eleccion = simpledialog.askstring("Tipo de lista", "Elige: a (todos), b (ocupados), c (vacíos):")
        if eleccion not in opciones:
            return

        ahora = datetime.now()
        resultado = []

        for id_esp, datos in sorted(espacios.items()):
            try:
                fin_dt = datetime.strptime(datos["fin"], "%d/%m/%Y %H:%M") if datos["fin"] else None
            except:
                fin_dt = None

            if eleccion == "b" and (not fin_dt or fin_dt < ahora):
                continue
            if eleccion == "c" and fin_dt and fin_dt >= ahora:
                continue

            linea = f"{id_esp} - Habilitado: {datos['habilitado']}"
            if datos["usuario"]:
                linea += f"\n  Placa: {datos['placa']}\n  Inicio: {datos['inicio']}\n  Tiempo: {datos['tiempo']} mins\n  Fin: {datos['fin']}"
            resultado.append(linea)

        contenido = f"{opciones[eleccion]}:\n\n" + "\n\n".join(resultado)
        contenido += f"\n\nTotal espacios listados: {len(resultado)}"
        self.actualizar_texto(contenido)

    # ------------ Reporte 3: Historial de usos ------------
    def historial_usos(self):
        """
        Genera un historial de usos de espacios.
        
        Este método:
        1. Solicita las fechas de inicio y fin
        2. Valida las fechas ingresadas
        3. Obtiene los alquileres del sistema
        4. Filtra los alquileres según las fechas
        5. Muestra los resultados en la interfaz
        """
        fecha_inicio = self.fecha_inicio_var.get()
        fecha_fin = self.fecha_fin_var.get()

        if not all([fecha_inicio, fecha_fin]):
            return messagebox.showerror("Error", "Complete todos los campos.")

        try:
            desde_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            hasta_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")
        except ValueError:
            return messagebox.showerror("Error", "Formato incorrecto.")

        alquileres = mu.leer_json(ALQUILERES_PATH)
        usados = [
            a for a in alquileres
            if desde_dt.date() <= datetime.strptime(a["inicio"], "%d/%m/%Y %H:%M").date() <= hasta_dt.date()
        ]

        usados.sort(key=lambda x: x["inicio"], reverse=True)
        contenido = "📆 Historial de espacios usados:\n\n"
        for a in usados:
            contenido += (
                f"Espacio: {a['espacio_id']}\nInicio: {a['inicio']}\nFin: {a['fin']}\n"
                f"Tiempo: {a['usuario']} - {a['costo_total']}₡\n{'-'*40}\n"
            )
        self.actualizar_texto(contenido if usados else "No hay registros.")

    # ------------ Reporte 4: Historial de multas ------------
    def historial_multas(self):
        """
        Genera un historial de multas.
        
        Este método:
        1. Solicita las fechas de inicio y fin
        2. Valida las fechas ingresadas
        3. Obtiene las multas del sistema
        4. Filtra las multas según las fechas
        5. Muestra los resultados en la interfaz
        """
        fecha_inicio = self.fecha_inicio_var.get()
        fecha_fin = self.fecha_fin_var.get()

        if not all([fecha_inicio, fecha_fin]):
            return messagebox.showerror("Error", "Complete todos los campos.")

        try:
            desde_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            hasta_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")
        except ValueError:
            return messagebox.showerror("Error", "Formato incorrecto.")

        multas = mu.leer_json(MULTAS_PATH)
        filtro = [
            m for m in multas
            if desde_dt.date() <= datetime.strptime(m["fecha"], "%d/%m/%Y %H:%M").date() <= hasta_dt.date()
        ]

        filtro.sort(key=lambda x: x["fecha"], reverse=True)
        contenido = "⚠️ Historial de multas:\n\n"
        total = 0
        for m in filtro:
            contenido += (
                f"Fecha: {m['fecha']}\nEspacio: {m['espacio']}\nPlaca: {m['placa']}\n"
                f"Motivo: {m['detalle']}\n{'-'*40}\n"
            )
            total += int(m.get("monto", 0))
        contenido += f"\nTOTAL ₡ en multas: {total}"
        self.actualizar_texto(contenido if filtro else "No hay multas en ese periodo.")

    def generar_reporte(self):
        """
        Genera un reporte según los filtros seleccionados.
        
        Este método:
        1. Valida las fechas ingresadas
        2. Obtiene el tipo de reporte seleccionado
        3. Genera el reporte correspondiente
        4. Muestra los resultados en la tabla
        """
        fecha_inicio = self.fecha_inicio_var.get()
        fecha_fin = self.fecha_fin_var.get()
        tipo = self.tipo_reporte_var.get()

        if not all([fecha_inicio, fecha_fin, tipo]):
            return messagebox.showerror("Error", "Complete todos los campos.")

        try:
            reporte = mr.generar_reporte(tipo, fecha_inicio, fecha_fin)
            self.mostrar_resultados(reporte)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")

    def mostrar_resultados(self, datos):
        """
        Muestra los resultados del reporte en la tabla.
        
        Args:
            datos (list): Lista de datos del reporte generado
            
        Este método:
        1. Limpia la tabla actual
        2. Configura las columnas según el tipo de reporte
        3. Inserta los datos en la tabla
        """
        self.tabla.delete(*self.tabla.get_children())
        
        if not datos:
            return

        # Configurar columnas según el tipo de reporte
        self.tabla["columns"] = list(datos[0].keys())
        self.tabla["show"] = "headings"

        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)

        # Insertar datos
        for fila in datos:
            self.tabla.insert("", tk.END, values=list(fila.values()))

    def exportar_reporte(self):
        """
        Exporta el reporte actual a un archivo.
        
        Este método:
        1. Verifica que haya datos para exportar
        2. Solicita la ubicación del archivo
        3. Exporta los datos en el formato seleccionado
        4. Muestra mensajes de éxito o error
        """
        if not self.tabla.get_children():
            return messagebox.showerror("Error", "No hay datos para exportar.")

        try:
            mr.exportar_reporte(self.tabla)
            messagebox.showinfo("Éxito", "Reporte exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el reporte: {e}")

    def actualizar_texto(self, texto):
        self.reporte_actual = texto
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, texto)
