# src/frames/administradores/menu_frame.py

"""
Módulo para el menú principal de administradores.

Este módulo implementa la interfaz del menú principal que permite a los
administradores acceder a las diferentes funcionalidades del sistema.
"""

import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys
from frames.base_frame import BaseFrame
from frames.administradores.espacio_frame import EspaciosFrame
from frames.administradores.reportes_frame import ReportesAdminFrame
from frames.administradores.configuracion_frame import ConfiguracionFrame
from frames.administradores.acerca_de_frame import AcercaDeFrame

class MenuAdminFrame(BaseFrame):
    """
    Frame para el menú principal de administradores.
    
    Esta clase maneja la interfaz gráfica del menú principal que permite
    a los administradores acceder a las diferentes funcionalidades del sistema.
    """
    
    def __init__(self, master, app):
        """
        Inicializa el frame del menú principal.
        
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
            text="👨‍💼 Menú Administrador",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # Botones principales
        tk.Button(
            self,
            text="🅿️ Espacios",
            command=self.ir_a_espacios,
            font=("Arial", 12),
            width=20
        ).pack(pady=5)

        tk.Button(
            self,
            text="📊 Reportes",
            command=self.ir_a_reportes,
            font=("Arial", 12),
            width=20
        ).pack(pady=5)

        tk.Button(
            self,
            text="⚙️ Configuración",
            command=self.ir_a_configuracion,
            font=("Arial", 12),
            width=20
        ).pack(pady=5)

        tk.Button(
            self,
            text="🧠 Acerca de",
            command=self.ir_a_acerca_de,
            font=("Arial", 12),
            width=20
        ).pack(pady=5)

        tk.Button(
            self,
            text="📘 Ayuda",
            command=self.abrir_ayuda,
            font=("Arial", 12),
            width=20
        ).pack(pady=5)



        tk.Button(
            self,
            text="❌ Cerrar Aplicación",
            command=self.master.quit,
            font=("Arial", 12),
            width=20
        ).pack(pady=5)

    def ir_a_espacios(self):
        """Cambia al frame de gestión de espacios."""
        self.app.cambiar_frame(EspaciosFrame)

    def ir_a_reportes(self):
        """Cambia al frame de reportes."""
        self.app.cambiar_frame(ReportesAdminFrame)

    def ir_a_configuracion(self):
        """Cambia al frame de configuración."""
        self.app.cambiar_frame(ConfiguracionFrame)

    def ir_a_acerca_de(self):
        """Cambia al frame de información del sistema."""
        self.app.cambiar_frame(AcercaDeFrame)

    def abrir_ayuda(self):
        path_pdf = os.path.abspath("docs/manual_ayuda.pdf")
        try:
            if os.name == 'nt':
                os.startfile(path_pdf)
            elif os.name == 'posix':
                subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', path_pdf])
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo abrir el manual de ayuda.\n{e}")

    def cerrar_sesion(self):
        """Cierra la sesión actual y vuelve al menú principal."""
        self.app.volver()
