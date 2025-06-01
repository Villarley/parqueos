# src/frames/administradores/menu_frame.py

import tkinter as tk
from frames.administradores.configuracion_frame import ConfiguracionFrame
from frames.administradores.espacio_frame import EspaciosFrame

class MenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Menú de Administración", font=("Arial", 18)).pack(pady=20)
        tk.Button(self, text="⚙️ Configuración", command=lambda: master.cambiar_frame(ConfiguracionFrame)).pack(pady=5)
        tk.Button(self, text="🚧 Espacios", command=lambda: master.cambiar_frame(EspaciosFrame)).pack(pady=5)
