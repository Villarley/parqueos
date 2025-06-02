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
from tkinter import messagebox
from frames.administradores.menu_frame import MenuAdminFrame

class AppAdmin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Parqueos - Administrador")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Centrar la ventana
        self.centrar_ventana()
        
        # Inicializar el frame actual
        self.current_frame = None
        self.frame_history = []
        
        # Mostrar el menú de administrador
        self.cambiar_frame(MenuAdminFrame)
        
        # Configurar el protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def cambiar_frame(self, frame_class, *args):
        """Cambia el frame actual por uno nuevo."""
        try:
            # Destruir el frame actual si existe
            if self.current_frame:
                self.current_frame.destroy()
            
            # Crear el nuevo frame
            self.current_frame = frame_class(self.root, self, *args)
            self.current_frame.pack(fill=tk.BOTH, expand=True)
            
            # Agregar el frame al historial
            self.frame_history.append(frame_class)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar de frame: {str(e)}")
            # En caso de error, volver al menú principal
            self.volver()
            
    def volver(self):
        """Vuelve al frame anterior o al menú principal."""
        if len(self.frame_history) > 1:
            # Remover el frame actual del historial
            self.frame_history.pop()
            # Obtener el frame anterior
            previous_frame = self.frame_history[-1]
            # Cambiar al frame anterior
            self.cambiar_frame(previous_frame)
        else:
            # Si no hay historial, volver al menú principal
            self.cambiar_frame(MenuAdminFrame)
            
    def on_closing(self):
        """Maneja el evento de cierre de la ventana."""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            self.root.destroy()
            
    def run(self):
        """Inicia la aplicación."""
        self.root.mainloop()

if __name__ == "__main__":
    app = AppAdmin()
    app.run()
