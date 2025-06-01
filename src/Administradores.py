# src/Administradores.py

"""
Módulo principal para la aplicación de administradores del sistema de parqueos.

Este módulo implementa la interfaz gráfica para los administradores, permitiéndoles:
- Acceder al menú principal de administración
- Navegar entre diferentes frames de la aplicación
- Gestionar el sistema de parqueos

La aplicación utiliza Tkinter para la interfaz gráfica y mantiene un historial
de navegación para permitir el retorno a frames anteriores.
"""

import tkinter as tk
from frames.administradores.menu_frame import MenuFrame

class AppAdmin(tk.Tk):
    """
    Aplicación principal para administradores del sistema de parqueos.
    
    Esta clase maneja la ventana principal y la navegación entre diferentes
    frames de la aplicación. Incluye un sistema de historial para permitir
    la navegación hacia atrás.
    
    Attributes:
        current_frame: Frame actualmente mostrado en la aplicación
        frame_history: Lista que mantiene el historial de frames visitados
    """
    
    def __init__(self):
        """
        Inicializa la aplicación de administradores.
        
        Configura:
        - Título de la ventana
        - Tamaño inicial
        - Capacidad de redimensionar
        - Frame inicial (menú de administración)
        - Historial de frames
        """
        super().__init__()
        self.title("Parqueo Callejero - Administración")
        self.geometry("500x500")
        self.resizable(True, True)

        self.current_frame = None
        self.frame_history = []  # Para mantener un historial de frames
        self.cambiar_frame(MenuFrame)

    def cambiar_frame(self, frame_class, *args):
        """
        Cambia el frame actual de la aplicación.
        
        Args:
            frame_class: Clase del nuevo frame a mostrar
            *args: Argumentos adicionales para el constructor del frame
            
        Proceso:
            1. Guarda el frame actual y sus argumentos en el historial
            2. Destruye el frame actual
            3. Crea una nueva instancia del frame especificado
            4. Empaqueta el nuevo frame en la ventana
        """
        if self.current_frame:
            self.frame_history.append((self.current_frame.__class__, args))
            self.current_frame.destroy()

        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

    def volver(self):
        """
        Vuelve al frame anterior en el historial.
        
        Si hay frames en el historial:
            - Recupera el último frame y sus argumentos
            - Navega a ese frame
        Si no hay historial:
            - Navega al menú principal
        """
        if self.frame_history:
            frame_class, args = self.frame_history.pop()
            self.cambiar_frame(frame_class, *args)
        else:
            # Si no hay historial, volver al menú principal
            self.cambiar_frame(MenuFrame)

if __name__ == "__main__":
    app = AppAdmin()
    app.mainloop()
