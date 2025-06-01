import tkinter as tk
from frames.base_frame import BaseFrame

class AcercaDeFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="🧠 Acerca de", font=("Arial", 16)).pack(pady=10)

        info = (
            "Aplicación de Gestión de Parqueos\n"
            "Autor: Santiago Villarreal\n"
            "Email: santivillarley1010@gmail.com\n"
            "GitHub: github.com/villarley\n"
            "Versión: 1.0.0\n"
            "© 2025 Todos los derechos reservados."
        )

        tk.Label(self, text=info, justify="left").pack(pady=10)
        self.crear_boton_volver()
