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
        tk.Label(self, text="¿Deseas desaparcar tu vehículo?").pack(pady=10)

        espacio = mp.obtener_espacio_actual(self.usuario["correo"])
        if not espacio:
            tk.Label(self, text="⚠️ No tienes un espacio alquilado actualmente").pack()
        else:
            tk.Label(self, text=f"Espacio actual: {espacio['id']}").pack()

        tk.Button(self, text="🚗 Desaparcar", command=self.desaparcar).pack(pady=10)
        self.crear_boton_volver()

    def desaparcar(self):
        if mp.desaparcar(self.usuario["correo"]):
            messagebox.showinfo("Éxito", "Vehículo desaparcardo correctamente")
            self.volver_al_menu()
        else:
            messagebox.showerror("Error", "No se pudo desaparcar. ¿Ya habías liberado el espacio?")
