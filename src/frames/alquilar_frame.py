# src/frames/alquilar_frame.py

import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_parqueo as mp

class AlquilarFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.espacios_disponibles = []
        self.espacio_var = tk.StringVar()
        self.duracion_var = tk.IntVar(value=30)  # minutos
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="🅿️ Alquilar espacio", font=("Arial", 16)).pack(pady=10)

        self.espacios_disponibles = mp.obtener_espacios_disponibles()
        if not self.espacios_disponibles:
            tk.Label(self, text="No hay espacios disponibles.").pack(pady=10)
            self.crear_boton_volver()
            return

        tk.Label(self, text="Espacio disponible:").pack()
        self.espacio_var.set(self.espacios_disponibles[0]["id"])
        opciones = [e["id"] for e in self.espacios_disponibles]
        tk.OptionMenu(self, self.espacio_var, *opciones).pack()

        tk.Label(self, text="Duración (minutos):").pack()
        tk.Entry(self, textvariable=self.duracion_var).pack()

        tk.Button(self, text="✅ Confirmar alquiler", command=self.confirmar_alquiler).pack(pady=10)

        self.crear_boton_volver()

    def confirmar_alquiler(self):
        espacio_id = self.espacio_var.get()
        duracion = self.duracion_var.get()

        if duracion < 1:
            messagebox.showerror("Error", "La duración mínima debe ser de 1 minuto.")
            return

        exito = mp.alquilar_espacio(self.usuario["correo"], espacio_id, duracion)
        if exito:
            messagebox.showinfo("Éxito", f"Espacio {espacio_id} alquilado por {duracion} minutos.")
            self.volver_al_menu()
        else:
            messagebox.showerror("Error", "No se pudo alquilar el espacio.")
