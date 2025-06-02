"""
Módulo para mostrar información del sistema.

Este módulo implementa la interfaz que muestra información
sobre el sistema de parqueos.
"""

import tkinter as tk
from frames.base_frame import BaseFrame

class AcercaDeFrame(BaseFrame):
    """
    Frame para mostrar información del sistema.
    
    Esta clase maneja la interfaz gráfica que muestra información
    sobre el sistema de parqueos.
    """
    
    def __init__(self, master, app):
        """
        Inicializa el frame de información del sistema.
        
        Args:
            master: Widget padre de este frame
            app: Instancia de la aplicación principal
        """
        super().__init__(master)
        self.app = app
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        """
        # Título
        tk.Label(
            self,
            text="🧠 Acerca del Sistema",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # Información del sistema
        info_frame = tk.Frame(self)
        info_frame.pack(pady=10, padx=20)

        # Versión
        tk.Label(
            info_frame,
            text="Versión: 1.0.0",
            font=("Arial", 12)
        ).pack(pady=5)

        # Descripción
        tk.Label(
            info_frame,
            text="Sistema de Gestión de Parqueos",
            font=("Arial", 12)
        ).pack(pady=5)

        # Características
        tk.Label(
            info_frame,
            text="Características principales:",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        caracteristicas = [
            "• Gestión de espacios de parqueo",
            "• Control de acceso de vehículos",
            "• Generación de reportes",
            "• Configuración del sistema",
            "• Gestión de multas"
        ]

        for caracteristica in caracteristicas:
            tk.Label(
                info_frame,
                text=caracteristica,
                font=("Arial", 11)
            ).pack(pady=2)

        # Botón para volver
        tk.Button(
            self,
            text="🔙 Volver",
            command=self.app.volver,
            font=("Arial", 12)
        ).pack(pady=20) 