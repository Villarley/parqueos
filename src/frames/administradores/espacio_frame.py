"""
Módulo para la gestión de espacios de parqueo.

Este módulo implementa la interfaz que permite a los administradores
gestionar los espacios de parqueo del sistema.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import modulo_utiles as mu
from frames.base_frame import BaseFrame

ESPACIOS_PATH = "data/pc_espacios.json"

class EspaciosFrame(BaseFrame):
    """
    Frame para la gestión de espacios de parqueo.
    
    Esta clase maneja la interfaz gráfica que permite a los administradores
    gestionar los espacios de parqueo del sistema.
    
    Attributes:
        espacios (dict): Diccionario de espacios de parqueo
        espacio_var (StringVar): Variable para el campo de ID de espacio
        habilitado_var (StringVar): Variable para el estado del espacio
    """
    
    def __init__(self, master, app):
        """
        Inicializa el frame de gestión de espacios.
        
        Args:
            master: Widget padre de este frame
            app: Instancia de la aplicación principal
        """
        super().__init__(master)
        self.app = app
        self.espacios = self.cargar_espacios()
        self.espacio_var = tk.StringVar()
        self.habilitado_var = tk.StringVar(value="S")
        self.crear_widgets()

    def cargar_espacios(self):
        """
        Carga los espacios de parqueo desde el archivo JSON.
        
        Returns:
            dict: Diccionario de espacios de parqueo
        """
        espacios = mu.leer_json(ESPACIOS_PATH)
        if not isinstance(espacios, dict):
            messagebox.showwarning("Advertencia", "No se pudieron cargar los espacios. Se iniciará con un diccionario vacío.")
            return {}
        return espacios

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y secciones principales
        - Lista de espacios existentes
        - Campos para agregar/modificar espacios
        - Botones de gestión
        """
        tk.Label(self, text="🅿️ Gestión de Espacios", font=("Arial", 16, "bold")).pack(pady=20)

        self.tabla = ttk.Treeview(self, columns=("ID", "Habilitado", "Info"), show="headings")
        self.tabla.heading("ID", text="Número espacio")
        self.tabla.heading("Habilitado", text="Habilitado (S/N)")
        self.tabla.heading("Info", text="🔎")

        self.tabla.pack(pady=10)

        self.actualizar_tabla()

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Número de espacio (ej: ESP005):").grid(row=0, column=0)
        tk.Entry(form_frame, textvariable=self.espacio_var).grid(row=0, column=1)

        tk.Label(form_frame, text="¿Habilitado (S/N)?:").grid(row=1, column=0)
        tk.OptionMenu(form_frame, self.habilitado_var, "S", "N").grid(row=1, column=1)

        tk.Button(self, text="➕ Agregar/Actualizar", command=self.agregar_actualizar_espacio).pack(pady=5)
        tk.Button(self, text="💾 Guardar Cambios", command=self.guardar_cambios).pack(pady=5)
        tk.Button(self, text="🔙 Volver", command=self.app.volver, font=("Arial", 12)).pack(pady=20)

    def actualizar_tabla(self):
        """
        Actualiza la lista de espacios de parqueo en la interfaz.
        
        Este método:
        1. Borra todos los elementos actuales de la tabla
        2. Inserta los nuevos espacios en la tabla
        3. Vincula la función de mostrar información a cada espacio
        """
        self.tabla.delete(*self.tabla.get_children())
        for id_espacio, datos in sorted(self.espacios.items()):
            iid = self.tabla.insert("", "end", values=(id_espacio, datos["habilitado"], "ℹ️"))
            self.tabla.item(iid, tags=(id_espacio,))
        self.tabla.tag_bind("ESP", sequence="<<TreeviewSelect>>", callback=self.mostrar_info_espacio)
        self.tabla.bind("<Double-Button-1>", self.on_info_click)

    def on_info_click(self, event):
        """
        Muestra información detallada de un espacio seleccionado.
        
        Args:
            event: Evento que desencadena la llamada a esta función
        """
        selected = self.tabla.focus()
        if not selected:
            return
        values = self.tabla.item(selected, "values")
        if len(values) >= 1:
            espacio_id = values[0]
            self.mostrar_info_espacio(espacio_id)

    def mostrar_info_espacio(self, espacio_id):
        """
        Muestra información detallada de un espacio específico.
        
        Args:
            espacio_id (str): ID del espacio de parqueo
        """
        datos = self.espacios.get(espacio_id, {})
        if not datos.get("usuario"):
            return messagebox.showinfo("Información", f"Espacio {espacio_id} no tiene datos de alquiler activos.")

        contenido = (
            f"Usuario: {datos.get('usuario', '')}\n"
            f"Placa: {datos.get('placa', '')}\n"
            f"Inicio: {datos.get('inicio', '')}\n"
            f"Minutos: {datos.get('tiempo', '')}\n"
            f"Fin: {datos.get('fin', '')}"
        )
        messagebox.showinfo(f"Detalles del espacio {espacio_id}", contenido)

    def agregar_actualizar_espacio(self):
        """
        Agrega o actualiza un espacio de parqueo.
        
        Este método:
        1. Valida los datos ingresados
        2. Verifica que el ID no esté duplicado
        3. Actualiza el espacio en el sistema
        4. Actualiza la interfaz
        """
        espacio_id = self.espacio_var.get().strip().upper()
        habilitado = self.habilitado_var.get()

        if not espacio_id or not espacio_id.isalnum():
            return messagebox.showerror("Error", "ID de espacio inválido.")

        if espacio_id not in self.espacios:
            self.espacios[espacio_id] = {
                "habilitado": habilitado,
                "usuario": "",
                "placa": "",
                "inicio": "",
                "tiempo": 0,
                "fin": ""
            }
        else:
            self.espacios[espacio_id]["habilitado"] = habilitado

        self.actualizar_tabla()
        messagebox.showinfo("Actualizado", f"Espacio {espacio_id} agregado/actualizado.")

    def guardar_cambios(self):
        """
        Guarda los cambios realizados en los espacios de parqueo.
        
        Este método:
        1. Escribe los espacios actualizados en el archivo JSON
        2. Muestra un mensaje de éxito o error
        """
        try:
            mu.escribir_json(ESPACIOS_PATH, self.espacios)
            messagebox.showinfo("Guardado", "Cambios guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los cambios: {str(e)}")
