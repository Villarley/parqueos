# src/Inspectores.py
"""
Módulo principal para la aplicación de inspectores del sistema de parqueos.

Este módulo implementa la interfaz gráfica para los inspectores, permitiéndoles:
- Acceder al menú principal de inspectores
- Navegar entre diferentes frames de la aplicación
- Gestionar inspecciones de parqueos

La aplicación utiliza Tkinter para la interfaz gráfica y sigue un patrón
de navegación basado en frames.
"""

import tkinter as tk
from frames.inspectores.menu_frame import MenuInspectorFrame

class AppInspectores(tk.Tk):
    """
    Aplicación principal para inspectores del sistema de parqueos.
    
    Esta clase maneja la ventana principal y la navegación entre diferentes
    frames de la aplicación. Hereda de tk.Tk para crear la ventana principal.
    
    Attributes:
        current_frame: Frame actualmente mostrado en la aplicación
    """
    
    def __init__(self):
        """
        Inicializa la aplicación de inspectores.
        
        Configura:
        - Título de la ventana
        - Tamaño inicial
        - Frame inicial (menú de inspectores)
        """
        super().__init__()
        self.title("Sistema de Inspectores - Parqueo Callejero")
        self.geometry("500x500")
        self.current_frame = None
        self.cambiar_frame(MenuInspectorFrame)

    def cambiar_frame(self, frame_class, *args):
        """
        Cambia el frame actual de la aplicación.
        
        Args:
            frame_class: Clase del nuevo frame a mostrar
            *args: Argumentos adicionales para el constructor del frame
            
        Proceso:
            1. Destruye el frame actual si existe
            2. Crea una nueva instancia del frame especificado
            3. Empaqueta el nuevo frame en la ventana
        """
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

    def volver(self):
        """
        Vuelve al menú principal de inspectores.
        
        Este método es un atajo para volver al frame inicial de la aplicación.
        """
        self.cambiar_frame(MenuInspectorFrame)

if __name__ == "__main__":
    app = AppInspectores()
    app.mainloop()
