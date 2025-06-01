"""
Módulo para el cambio de contraseña de usuarios.

Este módulo implementa la interfaz que permite a los usuarios:
- Cambiar su contraseña actual
- Validar la nueva contraseña
- Confirmar el cambio de contraseña

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_usuarios as mu
import bcrypt

class CambiarContraseniaFrame(BaseFrame):
    """
    Frame para el cambio de contraseña.
    
    Esta clase maneja la interfaz gráfica que permite a los usuarios
    cambiar su contraseña de forma segura.
    
    Attributes:
        usuario (dict): Información del usuario actual
        actual_var (StringVar): Variable para la contraseña actual
        nueva_var (StringVar): Variable para la nueva contraseña
        confirmar_var (StringVar): Variable para confirmar la nueva contraseña
    """
    
    def __init__(self, master, usuario):
        """
        Inicializa el frame de cambio de contraseña.
        
        Args:
            master: Widget padre de este frame
            usuario (dict): Información del usuario actual
        """
        super().__init__(master, usuario)
        self.actual_var = tk.StringVar()
        self.nueva_var = tk.StringVar()
        self.confirmar_var = tk.StringVar()
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y mensajes informativos
        - Campos para las contraseñas
        - Botones de confirmación y volver
        """
        tk.Label(self, text="🔑 Cambiar Contraseña", font=("Arial", 16)).pack(pady=10)

        # Campos de contraseña
        tk.Label(self, text="Contraseña actual:").pack()
        tk.Entry(self, textvariable=self.actual_var, show="*").pack()

        tk.Label(self, text="Nueva contraseña:").pack()
        tk.Entry(self, textvariable=self.nueva_var, show="*").pack()

        tk.Label(self, text="Confirmar nueva contraseña:").pack()
        tk.Entry(self, textvariable=self.confirmar_var, show="*").pack()

        # Botones
        tk.Button(self, text="💾 Guardar cambios", command=self.cambiar_contrasenia).pack(pady=5)
        self.crear_boton_volver()

    def cambiar_contrasenia(self):
        """
        Procesa el cambio de contraseña.
        
        Este método:
        1. Valida la contraseña actual
        2. Verifica que la nueva contraseña cumpla los requisitos
        3. Confirma que las contraseñas coincidan
        4. Actualiza la contraseña en el sistema
        5. Muestra mensajes de éxito o error
        """
        actual = self.actual_var.get()
        nueva = self.nueva_var.get()
        confirmar = self.confirmar_var.get()

        # Validaciones
        if not all([actual, nueva, confirmar]):
            return messagebox.showerror("Error", "Todos los campos son obligatorios.")

        if not mu.validar_contrasena(actual, self.usuario["contrasena"]):
            return messagebox.showerror("Error", "La contraseña actual es incorrecta.")

        if not mu.validar_contrasena(nueva):
            return messagebox.showerror(
                "Error",
                "La nueva contraseña debe tener al menos 8 caracteres, una mayúscula y un número."
            )

        if nueva != confirmar:
            return messagebox.showerror("Error", "Las contraseñas no coinciden.")

        # Actualizar contraseña
        if mu.actualizar_contrasena(self.usuario["identificacion"], nueva):
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
            self.volver_al_menu()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la contraseña.")
