# src/frames/configuracion_frame.py

import tkinter as tk
from tkinter import messagebox
import modulo_utiles as mu
from frames.base_frame import BaseFrame

CONFIG_PATH = "data/pc_configuracion.json"

class ConfiguracionFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="⚙️ Configuración del Sistema", font=("Arial", 16)).pack(pady=10)

        self.config = mu.leer_json(CONFIG_PATH)

        self.entradas = {}

        # Campos editables
        campos = {
            "tarifa_hora": "Tarifa por hora ($)",
            "tiempo_minimo": "Tiempo mínimo (min)",
            "horario_inicio": "Horario inicio (HH:MM)",
            "horario_fin": "Horario fin (HH:MM)",
            "multa_por_hora": "Multa por hora ($)"
        }

        for clave, texto in campos.items():
            tk.Label(self, text=texto).pack()
            entrada = tk.Entry(self)
            entrada.insert(0, str(self.config.get(clave, "")))
            entrada.pack(pady=5)
            self.entradas[clave] = entrada

        # Botones
        tk.Button(self, text="💾 Guardar cambios", command=self.guardar_config).pack(pady=10)
        self.crear_boton_volver()

    def guardar_config(self):
        try:
            nueva_config = {
                "tarifa_hora": float(self.entradas["tarifa_hora"].get()),
                "tiempo_minimo": int(self.entradas["tiempo_minimo"].get()),
                "horario_inicio": self.entradas["horario_inicio"].get(),
                "horario_fin": self.entradas["horario_fin"].get(),
                "multa_por_hora": float(self.entradas["multa_por_hora"].get())
            }
            mu.escribir_json(CONFIG_PATH, nueva_config)
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
