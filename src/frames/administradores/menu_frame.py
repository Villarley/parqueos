# src/frames/administradores/menu_frame.py

"""
Módulo para el menú principal de administradores.

Este módulo implementa la interfaz del menú principal que permite a los administradores:
- Acceder a la gestión de espacios
- Ver y generar reportes
- Configurar el sistema
- Gestionar usuarios

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from frames.base_frame import BaseFrame
from frames.administradores.espacio_frame import EspaciosFrame
from frames.administradores.reportes_frame import ReportesAdminFrame
from frames.administradores.configuracion_frame import ConfiguracionFrame

class MenuAdminFrame(BaseFrame):
    """
    Frame para el menú principal de administradores.
    
    Esta clase maneja la interfaz gráfica del menú principal que muestra
    todas las opciones disponibles para los administradores del sistema.
    
    Attributes:
        usuario (dict): Información del administrador actual
    """
    
    def __init__(self, master, usuario):
        """
        Inicializa el frame del menú principal.
        
        Args:
            master: Widget padre de este frame
            usuario (dict): Información del administrador actual
        """
        super().__init__(master, usuario)
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y mensaje de bienvenida
        - Botones para cada funcionalidad disponible
        - Información del administrador actual
        """
        tk.Label(self, text="👨‍💼 Menú Administrador", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text=f"Bienvenido, {self.usuario['nombre']}").pack()

        # Botones de funcionalidad
        tk.Button(self, text="🅿️ Gestión de espacios", command=self.ir_a_espacios).pack(pady=5)
        tk.Button(self, text="📊 Reportes", command=self.ir_a_reportes).pack(pady=5)
        tk.Button(self, text="⚙️ Configuración", command=self.ir_a_configuracion).pack(pady=5)

        # Botón de cerrar sesión
        tk.Button(self, text="🚪 Cerrar sesión", command=self.cerrar_sesion).pack(pady=10)

    def ir_a_espacios(self):
        """
        Navega a la pantalla de gestión de espacios.
        """
        self.master.cambiar_frame(EspaciosFrame)

    def ir_a_reportes(self):
        """
        Navega a la pantalla de reportes.
        """
        self.master.cambiar_frame(ReportesAdminFrame)

    def ir_a_configuracion(self):
        """
        Navega a la pantalla de configuración.
        """
        self.master.cambiar_frame(ConfiguracionFrame)

    def cerrar_sesion(self):
        """
        Cierra la sesión actual y regresa a la pantalla de login.
        """
        from frames.login_frame import LoginFrame
        self.master.cambiar_frame(LoginFrame)
