# src/frames/desaparcar_frame.py

import tkinter as tk
from tkinter import messagebox
import modulo_parqueo as mp
from frames.base_frame import BaseFrame

class DesaparcarFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="🚗 Desaparcar").pack(pady=10)

        self.alquiler = mp.obtener_alquiler_activo(self.usuario["correo"])
        if not self.alquiler:
            tk.Label(self, text="⚠️ No tienes un espacio alquilado").pack()
            self.crear_boton_volver()
            return

        tk.Label(self, text=f"Espacio ID: {self.alquiler['espacio_id']}").pack()
        tk.Label(self, text=f"Inicio: {self.alquiler['inicio']}").pack()
        tk.Label(self, text=f"Fin programado: {self.alquiler['fin']}").pack()

        tk.Button(self, text="🛑 Finalizar alquiler", command=self.confirmar_liberacion).pack(pady=10)
        self.crear_boton_volver()

    def confirmar_liberacion(self):
        confirm = messagebox.askyesno("Confirmar", "¿Seguro que deseas finalizar el alquiler?")
        if confirm:
            if mp.liberar_espacio(self.alquiler["id"]):
                messagebox.showinfo("Listo", "Espacio liberado exitosamente.")
                self.volver_al_menu()
            else:
                messagebox.showerror("Error", "No se pudo liberar el espacio.")
