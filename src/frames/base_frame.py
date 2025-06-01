# src/frames/base_frame.py

"""
Módulo base para los frames de la aplicación de parqueos.

Este módulo proporciona la clase base de la que heredan todos los frames
de la aplicación. Define la funcionalidad común y la estructura básica
que todos los frames deben implementar.
"""

import tkinter as tk

class BaseFrame(tk.Frame):
    """
    Frame base para todas las interfaces de la aplicación.
    
    Esta clase proporciona la funcionalidad básica y estructura común
    para todos los frames de la aplicación. Define métodos estándar
    para la navegación y gestión de la interfaz.
    
    Attributes:
        master: Widget padre de este frame
        usuario: Diccionario con la información del usuario actual
    """
    
    def __init__(self, master, usuario=None):
        """
        Inicializa el frame base.
        
        Args:
            master: Widget padre de este frame
            usuario (dict, optional): Información del usuario actual. Defaults to None.
        """
        super().__init__(master)
        self.master = master
        self.usuario = usuario

    def volver_al_menu(self):
        """Método común para volver al menú principal"""
        from frames.menu_usuario_frame import MenuUsuarioFrame
        self.master.cambiar_frame(MenuUsuarioFrame, self.usuario)

    def crear_boton_volver(self):
        """
        Crea un botón estándar para volver al menú anterior.
        
        Este método crea un botón con el texto "Volver" que al ser presionado
        llama al método volver() del widget padre.
        """
        tk.Button(self, text="🔙 Volver al menú", command=self.volver_al_menu).pack(pady=10) 