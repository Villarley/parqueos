import tkinter as tk
from frames.base_frame import BaseFrame
from frames.configuracion_frame import ConfiguracionFrame
from frames.login_frame import LoginFrame

class MenuAdminFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text=f"Administrador: {self.usuario['nombre']}", font=("Arial", 16)).pack(pady=10)

        tk.Button(
            self,
            text="Configuración general",
            width=30,
            command=lambda: self.master.cambiar_frame(ConfiguracionFrame, self.usuario)
        ).pack(pady=5)

        tk.Button(
            self,
            text="Cerrar sesión",
            width=30,
            command=lambda: self.master.cambiar_frame(LoginFrame)
        ).pack(pady=20)
