# src/frames/menu_usuario_frame.py

import tkinter as tk
from tkinter import messagebox
from frames.alquilar_frame import AlquilarFrame
from frames.agregar_tiempo_frame import AgregarTiempoFrame
from frames.desaparcar_frame import DesaparcarFrame
from frames.login_frame import LoginFrame

class MenuUsuarioFrame(tk.Frame):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.master = master
        self.usuario = usuario
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text=f"Bienvenido, {self.usuario['nombre']}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="🅿️ Alquilar espacio", width=25,
                  command=lambda: self.master.cambiar_frame(AlquilarFrame, self.usuario)).pack(pady=5)

        tk.Button(self, text="⏱ Agregar tiempo", width=25,
                  command=lambda: self.master.cambiar_frame(AgregarTiempoFrame, self.usuario)).pack(pady=5)

        tk.Button(self, text="🚗 Desaparcar", width=25,
                  command=lambda: self.master.cambiar_frame(DesaparcarFrame, self.usuario)).pack(pady=5)

        tk.Button(self, text="📄 Ver historial (WIP)", width=25,
                  command=self.historial_no_disponible).pack(pady=5)

        tk.Button(self, text="🚪 Cerrar sesión", width=25,
                  command=lambda: self.master.cambiar_frame(LoginFrame)).pack(pady=20)

    def historial_no_disponible(self):
        messagebox.showinfo("En desarrollo", "La funcionalidad de historial aún no está disponible.")
