import tkinter as tk
from tkinter import ttk, messagebox
import modulo_utiles as mu

ESPACIOS_PATH = "data/pc_espacios.json"

class EspaciosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.espacios = self.cargar_espacios()
        self.crear_widgets()

    def cargar_espacios(self):
        espacios = mu.leer_json(ESPACIOS_PATH)
        if not isinstance(espacios, dict):
            messagebox.showwarning("Advertencia", "No se pudieron cargar los espacios. Se iniciará con un diccionario vacío.")
            return {}
        return espacios

    def crear_widgets(self):
        tk.Label(self, text="🚧 Gestión de Espacios", font=("Arial", 16)).pack(pady=10)

        self.tabla = ttk.Treeview(self, columns=("ID", "Habilitado", "Info"), show="headings")
        self.tabla.heading("ID", text="Número espacio")
        self.tabla.heading("Habilitado", text="Habilitado (S/N)")
        self.tabla.heading("Info", text="🔎")

        self.tabla.pack(pady=10)

        self.actualizar_tabla()

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Número de espacio (ej: ESP005):").grid(row=0, column=0)
        self.id_entry = tk.Entry(form_frame)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="¿Habilitado (S/N)?:").grid(row=1, column=0)
        self.habilitado_var = tk.StringVar(value="S")
        tk.OptionMenu(form_frame, self.habilitado_var, "S", "N").grid(row=1, column=1)

        tk.Button(self, text="➕ Agregar/Actualizar", command=self.agregar_actualizar_espacio).pack(pady=5)
        tk.Button(self, text="💾 Guardar Cambios", command=self.guardar_cambios).pack(pady=5)
        tk.Button(self, text="🔙 Volver", command=self.master.volver).pack(pady=5)

    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for id_espacio, datos in sorted(self.espacios.items()):
            iid = self.tabla.insert("", "end", values=(id_espacio, datos["habilitado"], "ℹ️"))
            self.tabla.item(iid, tags=(id_espacio,))
        self.tabla.tag_bind("ESP", sequence="<<TreeviewSelect>>", callback=self.mostrar_info_espacio)
        self.tabla.bind("<Double-Button-1>", self.on_info_click)

    def on_info_click(self, event):
        selected = self.tabla.focus()
        if not selected:
            return
        values = self.tabla.item(selected, "values")
        if len(values) >= 1:
            espacio_id = values[0]
            self.mostrar_info_espacio(espacio_id)

    def mostrar_info_espacio(self, espacio_id):
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
        espacio_id = self.id_entry.get().strip()
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
        try:
            mu.escribir_json(ESPACIOS_PATH, self.espacios)
            messagebox.showinfo("Guardado", "Cambios guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los cambios: {str(e)}")
