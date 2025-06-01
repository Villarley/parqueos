"""
Módulo principal para la aplicación de usuarios del sistema de parqueos.

Este módulo implementa la interfaz gráfica para los usuarios regulares, permitiéndoles:
- Acceder al sistema mediante login
- Navegar entre diferentes frames de la aplicación
- Gestionar sus parqueos y vehículos

La aplicación utiliza Tkinter para la interfaz gráfica y comienza
mostrando la pantalla de inicio de sesión.
"""

import tkinter as tk
from frames.login_frame import LoginFrame

class App(tk.Tk):
    """
    Aplicación principal para usuarios del sistema de parqueos.
    
    Esta clase maneja la ventana principal y la navegación entre diferentes
    frames de la aplicación. Comienza mostrando la pantalla de login.
    
    Attributes:
        current_frame: Frame actualmente mostrado en la aplicación
    """
    
    def __init__(self):
        """
        Inicializa la aplicación de usuarios.
        
        Configura:
        - Título de la ventana
        - Tamaño inicial
        - Capacidad de redimensionar
        - Frame inicial (pantalla de login)
        """
        super().__init__()
        self.title("Parqueo Callejero - Usuario")
        self.geometry("500x500")
        self.resizable(True, True)

        self.current_frame = None
        self.cambiar_frame(LoginFrame)

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

if __name__ == "__main__":
    app = App()
    app.mainloop()
