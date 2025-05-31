# src/frames/menu_usuario_frame.py

import tkinter as tk
from frames.base_frame import BaseFrame
from frames.alquilar_frame import AlquilarFrame
from frames.desaparcar_frame import DesaparcarFrame
from frames.agregar_tiempo_frame import AgregarTiempoFrame
from frames.reportes_frame import ReportesFrame  # ← NUEVO
import modulo_utiles as mu
from frames.user.perfil_usuario_frame import PerfilUsuarioFrame
class MenuUsuarioFrame(BaseFrame):
    def __init__(self, master, usuario):
        mu.actualizar_estados_de_parqueo()
        super().__init__(master, usuario)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text=f"Bienvenido, {self.usuario['nombre']}").pack(pady=10)

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

        self.crear_boton_volver()
