# src/frames/desaparcar_frame.py

"""
Módulo para la interfaz de desaparcar vehículos.

Este módulo implementa la interfaz que permite a los usuarios:
- Ver sus alquileres activos
- Liberar espacios de parqueo
- Confirmar la finalización de alquileres

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import messagebox
import modulo_parqueo as mp
from frames.base_frame import BaseFrame

class DesaparcarFrame(BaseFrame):
    """
    Frame para la interfaz de desaparcar vehículos.
    
    Esta clase maneja la interfaz gráfica que permite a los usuarios
    finalizar sus alquileres activos y liberar espacios de parqueo.
    
    Attributes:
        usuario (dict): Información del usuario actual
        alquiler_activo (dict): Información del alquiler activo del usuario
    """
    
    def __init__(self, master, usuario):
        """
        Inicializa el frame de desaparcar.
        
        Args:
            master: Widget padre de este frame
            usuario (dict): Información del usuario actual
        """
        super().__init__(master, usuario)
        self.alquiler_activo = mp.obtener_alquiler_activo(usuario["correo"])
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y mensajes informativos
        - Información del alquiler activo si existe
        - Botón para desaparcar
        - Botón para volver
        """
        tk.Label(self, text="🚗 Desaparcar", font=("Arial", 16)).pack(pady=10)

        if not self.alquiler_activo:
            tk.Label(self, text="No tienes ningún alquiler activo.").pack(pady=10)
            self.crear_boton_volver()
            return

        # Mostrar información del alquiler
        info = f"""
Espacio: {self.alquiler_activo['espacio_id']}
Placa: {self.alquiler_activo['placa']}
Inicio: {self.alquiler_activo['inicio']}
Fin: {self.alquiler_activo['fin']}
Costo: ₡{self.alquiler_activo['costo_total']}
"""
        tk.Label(self, text=info, justify=tk.LEFT).pack(pady=10)

        # Botón para desaparcar
        tk.Button(self, text="Desaparcar", command=self.desaparcar).pack(pady=5)
        self.crear_boton_volver()

    def desaparcar(self):
        """
        Procesa la solicitud de desaparcar un vehículo.
        
        Este método:
        1. Confirma la acción con el usuario
        2. Libera el espacio de parqueo
        3. Finaliza el alquiler
        4. Muestra mensajes de éxito o error
        """
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas desaparcar?"):
            if mp.liberar_espacio(self.alquiler_activo["id"]):
                messagebox.showinfo("Éxito", "Vehículo desaparcado correctamente.")
                self.volver_al_menu()
            else:
                messagebox.showerror("Error", "No se pudo desaparcar el vehículo.")
