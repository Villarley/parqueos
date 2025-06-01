import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_utiles as mu

ESPACIOS_PATH = "data/pc_espacios.json"
CONFIG_PATH = "data/pc_configuracion.json"

class EspaciosFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.espacios_widgets = []
        self.crear_widgets()

    def crear_widgets(self):
        config = mu.leer_json(CONFIG_PATH)
        if not config:
            messagebox.showerror("Error", "Debe configurar el sistema antes de agregar espacios.")
            self.master.volver()
            return

        tk.Label(self, text="📋 Gestión de Espacios", font=("Arial", 16)).pack(pady=10)

        self.frame_lista = tk.Frame(self)
        self.frame_lista.pack(pady=10)

        self.cargar_espacios()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="✅ Guardar cambios", command=self.guardar_cambios).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="➕ Agregar nuevo espacio", command=self.agregar_espacio).pack(side=tk.LEFT, padx=10)
        self.crear_boton_volver()

    def cargar_espacios(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        self.espacios_widgets = []
        espacios = mu.leer_json(ESPACIOS_PATH)
        for espacio in sorted(espacios, key=lambda e: int(e["id"])):
            frame = tk.Frame(self.frame_lista)
            frame.pack(pady=2, fill='x')

            tk.Label(frame, text=f"Espacio #{espacio['id']}", width=15).pack(side=tk.LEFT)
            habilitado = tk.StringVar(value=espacio["estado"] if espacio["estado"] in ["libre", "ocupado"] else "libre")
            enabled = tk.StringVar(value="S" if espacio.get("habilitado", "S") == "S" else "N")

            tk.OptionMenu(frame, enabled, "S", "N").pack(side=tk.LEFT)
            self.espacios_widgets.append((espacio["id"], enabled))

    def guardar_cambios(self):
        espacios = mu.leer_json(ESPACIOS_PATH)
        diccionario = {e["id"]: e for e in espacios}

        for eid, enabled_var in self.espacios_widgets:
            if eid in diccionario:
                diccionario[eid]["habilitado"] = enabled_var.get()

        mu.escribir_json(ESPACIOS_PATH, list(diccionario.values()))
        messagebox.showinfo("Guardado", "Los cambios fueron guardados.")
        self.cargar_espacios()

    def agregar_espacio(self):
        espacios = mu.leer_json(ESPACIOS_PATH)
        ids = [int(e["id"]) for e in espacios]
        nuevo_id = str(max(ids, default=0) + 1)

        nuevo = {
            "id": nuevo_id,
            "ubicacion": f"Espacio #{nuevo_id}",
            "estado": "libre",
            "habilitado": "S"
        }

        espacios.append(nuevo)
        mu.escribir_json(ESPACIOS_PATH, espacios)
        self.cargar_espacios()
