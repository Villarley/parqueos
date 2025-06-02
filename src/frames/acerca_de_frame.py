"""
Módulo para la pantalla de información del sistema.

Este módulo implementa la interfaz que muestra información sobre:
- El autor del sistema
- Información de contacto
- Versión del software
- Derechos de autor

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from frames.base_frame import BaseFrame

class AcercaDeFrame(BaseFrame):
    """
    Frame para mostrar información del sistema.
    
    Esta clase maneja la interfaz gráfica que muestra información
    sobre el sistema y sus desarrolladores.
    
    Attributes:
        usuario (dict): Información del usuario actual
    """
    
    def __init__(self, master, usuario):
        """
        Inicializa el frame de información.
        
        Args:
            master: Widget padre de este frame
            usuario (dict): Información del usuario actual
        """
        super().__init__(master, usuario)
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y secciones principales
        - Información del sistema
        - Botón de volver
        """
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
