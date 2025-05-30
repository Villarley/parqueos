# src/frames/agregar_tiempo_frame.py

import tkinter as tk
from tkinter import messagebox
import modulo_parqueo as mp
from frames.base_frame import BaseFrame

class AgregarTiempoFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Espacio actual alquilado:").pack()

        alquiler = mp.obtener_alquiler_activo(self.usuario["correo"])

        if not alquiler:
            tk.Label(self, text="⚠️ No tienes un espacio alquilado").pack()
            self.crear_boton_volver()
            return

        self.alquiler_id = alquiler["id"]

        # Mostrar espacio actual
        tk.Label(self, text=f"Espacio: {alquiler['espacio_id']}").pack(pady=5)

        # Entrada de tiempo adicional
        tk.Label(self, text="Minutos adicionales:").pack()
        self.entry_tiempo = tk.Entry(self)
        self.entry_tiempo.pack()

        # Botones
        tk.Button(self, text="➕ Agregar tiempo", command=self.agregar_tiempo).pack(pady=10)
        self.crear_boton_volver()

    def agregar_tiempo(self):
        tiempo_str = self.entry_tiempo.get()
        if not tiempo_str.isdigit():
            messagebox.showerror("Error", "Ingresa un número válido de minutos")
            return

        tiempo = int(tiempo_str)

        if mp.agregar_tiempo_alquiler(self.alquiler_id, tiempo):
            messagebox.showinfo("Éxito", f"Tiempo agregado correctamente")
            self.volver_al_menu()
        else:
            messagebox.showerror("Error", "No se pudo agregar el tiempo")
