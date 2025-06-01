import tkinter as tk
from tkinter import messagebox
import modulo_utiles as mu

CONFIG_PATH = "data/pc_configuracion.json"

class ConfiguracionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.temp_config = {}
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="⚙️ Configuración del Parqueo", font=("Arial", 16)).pack(pady=10)

        self.entrada_desde = self.crear_entrada("Desde (hh:mm):")
        self.entrada_hasta = self.crear_entrada("Hasta (hh:mm):")
        self.entrada_tarifa = self.crear_entrada("Precio por hora:")
        self.entrada_minimo = self.crear_entrada("Mínimo de minutos:")
        self.entrada_multa = self.crear_entrada("Costo de multa:")

        tk.Button(self, text="✅ Actualizar", command=self.actualizar_config).pack(pady=5)
        tk.Button(self, text="❌ Cancelar", command=self.volver).pack(pady=5)

    def volver(self):
        from frames.administradores.menu_frame import MenuFrame
        self.master.cambiar_frame(MenuFrame)

    def crear_entrada(self, label):
        tk.Label(self, text=label).pack()
        entry = tk.Entry(self)
        entry.pack()
        return entry

    def actualizar_config(self):
        try:
            config = {
                "hora_inicio": self.entrada_desde.get(),
                "hora_fin": self.entrada_hasta.get(),
                "tarifa": int(self.entrada_tarifa.get()),
                "tiempo_minimo": int(self.entrada_minimo.get()),
                "multa": int(self.entrada_multa.get())
            }

            if config["tarifa"] <= 0 or config["tarifa"] % 2 != 0:
                raise ValueError("La tarifa debe ser un número par positivo.")
            if config["tiempo_minimo"] <= 0:
                raise ValueError("El mínimo de tiempo debe ser un entero positivo.")
            if config["multa"] <= 0:
                raise ValueError("La multa debe ser un número positivo.")

            mu.escribir_json(CONFIG_PATH, config)
            messagebox.showinfo("Configuración", "Datos guardados exitosamente.")
            self.volver()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar configuración:\n{e}")
