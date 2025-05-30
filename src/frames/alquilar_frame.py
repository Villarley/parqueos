# src/frames/alquilar_frame.py

import tkinter as tk
from tkinter import messagebox
import modulo_parqueo as mp
import modulo_utiles as mu
from frames.base_frame import BaseFrame

class AlquilarFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Selecciona un espacio disponible:", font=("Arial", 12)).pack(pady=5)

        self.espacios_disponibles = mp.obtener_espacios_disponibles()
        self.espacio_var = tk.StringVar()
        opciones = [esp["id"] for esp in self.espacios_disponibles]
        
        if not opciones:
            tk.Label(self, text="⚠️ No hay espacios disponibles").pack()
            self.crear_boton_volver()
            return

        self.espacio_var.set(opciones[0])
        tk.OptionMenu(self, self.espacio_var, *opciones).pack()

        tk.Label(self, text="Tiempo (minutos):").pack(pady=5)
        self.entry_tiempo = tk.Entry(self)
        self.entry_tiempo.pack()

        tk.Button(self, text="✅ Confirmar alquiler", command=self.confirmar_alquiler).pack(pady=10)
        self.crear_boton_volver()

    def confirmar_alquiler(self):
        espacio = self.espacio_var.get()
        tiempo_str = self.entry_tiempo.get()

        if not tiempo_str.isdigit():
            messagebox.showerror("Error", "El tiempo debe ser un número")
            return

        tiempo = int(tiempo_str)

        if mp.alquilar_espacio(self.usuario["correo"], espacio, tiempo):
            messagebox.showinfo("Éxito", f"Espacio {espacio} alquilado por {tiempo} minutos")
            self.volver_al_menu()
        else:
            messagebox.showerror("Error", "No se pudo alquilar el espacio")
