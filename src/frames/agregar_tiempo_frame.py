# src/frames/agregar_tiempo_frame.py

"""
Módulo para la interfaz de agregar tiempo a alquileres.

Este módulo implementa la interfaz que permite a los usuarios:
- Ver su alquiler activo
- Agregar tiempo adicional al alquiler
- Ver el costo del tiempo adicional
- Confirmar la extensión del alquiler

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_parqueo as mp

class AgregarTiempoFrame(BaseFrame):
    """
    Frame para la interfaz de agregar tiempo a alquileres.
    
    Esta clase maneja la interfaz gráfica que permite a los usuarios
    extender la duración de sus alquileres activos.
    
    Attributes:
        usuario (dict): Información del usuario actual
        alquiler_activo (dict): Información del alquiler activo del usuario
        tiempo_var (StringVar): Variable para el campo de tiempo adicional
    """
    
    def __init__(self, master, usuario):
        """
        Inicializa el frame de agregar tiempo.
        
        Args:
            master: Widget padre de este frame
            usuario (dict): Información del usuario actual
        """
        super().__init__(master, usuario)
        self.alquiler_activo = mp.obtener_alquiler_activo(usuario["correo"])
        self.tiempo_var = tk.StringVar()
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y mensajes informativos
        - Información del alquiler activo si existe
        - Campo para ingresar tiempo adicional
        - Botones de confirmación y volver
        """
        tk.Label(self, text="⏰ Agregar tiempo", font=("Arial", 16)).pack(pady=10)

        if not self.alquiler_activo:
            tk.Label(self, text="No tienes ningún alquiler activo.").pack(pady=10)
            self.crear_boton_volver()
            return

        # Mostrar información del alquiler
        info = f"""
Espacio: {self.alquiler_activo['espacio_id']}
Placa: {self.alquiler_activo['placa']}
Inicio: {self.alquiler_activo['inicio']}
Fin actual: {self.alquiler_activo['fin']}
"""
        tk.Label(self, text=info, justify=tk.LEFT).pack(pady=10)

        # Campo para tiempo adicional
        tk.Label(self, text="Minutos adicionales:").pack()
        tk.Entry(self, textvariable=self.tiempo_var).pack()

        # Botones
        tk.Button(self, text="Agregar tiempo", command=self.agregar_tiempo).pack(pady=5)
        self.crear_boton_volver()

    def agregar_tiempo(self):
        """
        Procesa la solicitud de agregar tiempo al alquiler.
        
        Este método:
        1. Valida el tiempo ingresado
        2. Confirma la acción con el usuario
        3. Agrega el tiempo al alquiler
        4. Muestra mensajes de éxito o error
        """
        try:
            minutos = int(self.tiempo_var.get())
            if minutos < 1:
                return messagebox.showerror("Error", "El tiempo debe ser mayor a 0.")
        except ValueError:
            return messagebox.showerror("Error", "Ingrese un número válido de minutos.")

        if messagebox.askyesno("Confirmar", f"¿Agregar {minutos} minutos al alquiler?"):
            if mp.agregar_tiempo_alquiler(self.alquiler_activo["id"], minutos):
                messagebox.showinfo("Éxito", "Tiempo agregado correctamente.")
                self.volver_al_menu()
            else:
                messagebox.showerror("Error", "No se pudo agregar el tiempo.")
