"""
Módulo para la pantalla de información del sistema para inspectores.

Este módulo implementa la interfaz que muestra información relevante
sobre el sistema de parqueos para los inspectores.
"""

import tkinter as tk
from frames.base_frame import BaseFrame

class AcercaDeFrame(BaseFrame):
    """
    Frame que muestra información sobre el sistema para inspectores.
    
    Esta clase maneja la interfaz gráfica que muestra información
    relevante sobre el sistema de parqueos para los inspectores.
    """
    
    def __init__(self, master):
        """
        Inicializa el frame de información.
        
        Args:
            master: Widget padre de este frame
        """
        super().__init__(master)
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        """
        # Título
        tk.Label(
            self,
            text="ℹ️ Acerca del Sistema",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # Información del sistema
        info_text = """
            "Aplicación de Gestión de Parqueos\n"
            "Autor: Santiago Villarreal\n"
            "Email: santivillarley1010@gmail.com\n"
            "GitHub: github.com/villarley\n"
            "Versión: 1.0.0\n"
            "© 2025 Todos los derechos reservados."
        """
        
        tk.Label(
            self,
            text=info_text,
            justify=tk.LEFT,
            font=("Arial", 12)
        ).pack(pady=20, padx=20)

        # Botón para volver
        tk.Button(
            self,
            text="🔙 Volver",
            command=self.master.volver,
            font=("Arial", 12)
        ).pack(pady=20) 