# src/frames/menu_usuario_frame.py

import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

from frames.base_frame import BaseFrame
from frames.alquilar_frame import AlquilarFrame
from frames.desaparcar_frame import DesaparcarFrame
from frames.agregar_tiempo_frame import AgregarTiempoFrame
from frames.reportes_frame import ReportesFrame
from frames.acerca_de_frame import AcercaDeFrame
from frames.user.perfil_usuario_frame import PerfilUsuarioFrame
import modulo_utiles as mu

class MenuUsuarioFrame(BaseFrame):
    def __init__(self, master, usuario):
        mu.actualizar_estados_de_parqueo()
        super().__init__(master, usuario)
        self.crear_widgets()

    def abrir_ayuda(self):
        path_pdf = os.path.abspath("docs/manual_ayuda.pdf")
        try:
            if os.name == 'nt':  # Windows
                os.startfile(path_pdf)
            elif os.name == 'posix':  # macOS / Linux
                subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', path_pdf])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el manual de ayuda.\n{e}")

    def crear_widgets(self):
        nombre = self.usuario['nombre'] if self.usuario else "Usuario"
        tk.Label(self, text=f"Bienvenido, {nombre}").pack(pady=10)

        tk.Button(self, text="🚗 Alquilar espacio", 
                  command=lambda: self.master.cambiar_frame(AlquilarFrame, self.usuario)).pack(pady=5)

        tk.Button(self, text="🅿️ Desaparcar", 
                  command=lambda: self.master.cambiar_frame(DesaparcarFrame, self.usuario)).pack(pady=5)

        tk.Button(self, text="⏱️ Agregar tiempo", 
                  command=lambda: self.master.cambiar_frame(AgregarTiempoFrame, self.usuario)).pack(pady=5)

        tk.Button(self, text="📊 Reportes", 
                  command=lambda: self.master.cambiar_frame(ReportesFrame, self.usuario)).pack(pady=5)

        tk.Button(self, text="👤 Perfil", 
                  command=lambda: self.master.cambiar_frame(PerfilUsuarioFrame, self.usuario)).pack(pady=5)

        tk.Button(self, text="📘 Ayuda", command=self.abrir_ayuda).pack(pady=5)

        tk.Button(self, text="🧠 Acerca de", 
                  command=lambda: self.master.cambiar_frame(AcercaDeFrame, self.usuario)).pack(pady=5)

        self.crear_boton_volver()
