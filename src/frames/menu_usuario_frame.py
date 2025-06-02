# src/frames/menu_usuario_frame.py

"""
Módulo para el menú principal de usuarios del sistema de parqueos.

Este módulo implementa la interfaz del menú principal que permite a los usuarios:
- Acceder a las diferentes funcionalidades del sistema
- Ver información de su cuenta
- Navegar a otras secciones de la aplicación

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

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
from frames.registro_vehiculos_frame import RegistroVehiculosFrame
import modulo_utiles as mu
import modulo_parqueo as mp

class MenuUsuarioFrame(BaseFrame):
    """
    Frame para el menú principal de usuarios.
    
    Esta clase maneja la interfaz gráfica del menú principal que muestra
    todas las opciones disponibles para los usuarios del sistema.
    
    Attributes:
        usuario (dict): Información del usuario actual
    """
    
    def __init__(self, master, usuario):
        """
        Inicializa el frame del menú principal.
        
        Args:
            master: Widget padre de este frame
            usuario (dict): Información del usuario actual
        """
        mp.verificar_multas()
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
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y mensaje de bienvenida
        - Botones para cada funcionalidad disponible
        - Información del usuario actual
        """
        # Título y bienvenida
        tk.Label(self, text="🏠 Menú Principal", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text=f"Bienvenido, {self.usuario['nombre']}").pack()

        # Botones de funcionalidad
        tk.Button(self, text="🅿️ Alquilar espacio", command=self.ir_a_alquilar).pack(pady=5)
        tk.Button(self, text="🚗 Desaparcar", command=self.ir_a_desaparcar).pack(pady=5)
        tk.Button(self, text="⏰ Agregar tiempo", command=self.ir_a_agregar_tiempo).pack(pady=5)
        tk.Button(self, text="📊 Reportes", command=self.ir_a_reportes).pack(pady=5)
        tk.Button(self, text="👤 Mi Perfil", command=self.ir_a_perfil).pack(pady=5)
        tk.Button(self, text="ℹ️ Acerca de", command=self.ir_a_acerca_de).pack(pady=5)

        # Botón de cerrar sesión
        tk.Button(self, text="🚪 Cerrar sesión", command=self.cerrar_sesion).pack(pady=10)

    def ir_a_alquilar(self):
        """
        Navega a la pantalla de alquiler de espacios.
        """
        self.master.cambiar_frame(AlquilarFrame, self.usuario)

    def ir_a_desaparcar(self):
        """
        Navega a la pantalla de desaparcar vehículos.
        """
        self.master.cambiar_frame(DesaparcarFrame, self.usuario)

    def ir_a_agregar_tiempo(self):
        """
        Navega a la pantalla de agregar tiempo a un alquiler.
        """
        self.master.cambiar_frame(AgregarTiempoFrame, self.usuario)

    def ir_a_registro_vehiculos(self):
        """
        Navega a la pantalla de registro de vehículos.
        """
        self.master.cambiar_frame(RegistroVehiculosFrame, self.usuario)

    def ir_a_reportes(self):
        """
        Navega a la pantalla de reportes.
        """
        self.master.cambiar_frame(ReportesFrame, self.usuario)

    def ir_a_perfil(self):
        """
        Navega a la pantalla de perfil de usuario.
        """
        self.master.cambiar_frame(PerfilUsuarioFrame, self.usuario)

    def ir_a_acerca_de(self):
        """
        Navega a la pantalla de información del sistema.
        """
        self.master.cambiar_frame(AcercaDeFrame, self.usuario)

    def cerrar_sesion(self):
        """
        Cierra la sesión actual y regresa a la pantalla de login.
        """
        from frames.login_frame import LoginFrame
        self.master.cambiar_frame(LoginFrame)
