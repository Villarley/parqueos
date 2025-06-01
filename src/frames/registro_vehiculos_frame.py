"""
Módulo para la interfaz de registro de vehículos.

Este módulo implementa la interfaz que permite a los usuarios:
- Registrar nuevos vehículos
- Ver sus vehículos registrados
- Eliminar vehículos de su lista
- Gestionar la información de sus vehículos

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_usuarios as mu

class RegistroVehiculosFrame(BaseFrame):
    """
    Frame para la interfaz de registro de vehículos.
    
    Esta clase maneja la interfaz gráfica que permite a los usuarios
    gestionar su lista de vehículos registrados.
    
    Attributes:
        usuario (dict): Información del usuario actual
        placa_var (StringVar): Variable para el campo de placa
        marca_var (StringVar): Variable para el campo de marca
        modelo_var (StringVar): Variable para el campo de modelo
        color_var (StringVar): Variable para el campo de color
    """
    
    def __init__(self, master, usuario):
        """
        Inicializa el frame de registro de vehículos.
        
        Args:
            master: Widget padre de este frame
            usuario (dict): Información del usuario actual
        """
        super().__init__(master, usuario)
        self.placa_var = tk.StringVar()
        self.marca_var = tk.StringVar()
        self.modelo_var = tk.StringVar()
        self.color_var = tk.StringVar()
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y mensajes informativos
        - Campos para ingresar datos del vehículo
        - Lista de vehículos registrados
        - Botones de registro y eliminación
        - Botón para volver
        """
        tk.Label(self, text="🚗 Registro de Vehículos", font=("Arial", 16)).pack(pady=10)

        # Campos de entrada
        tk.Label(self, text="Placa:").pack()
        tk.Entry(self, textvariable=self.placa_var).pack()

        tk.Label(self, text="Marca:").pack()
        tk.Entry(self, textvariable=self.marca_var).pack()

        tk.Label(self, text="Modelo:").pack()
        tk.Entry(self, textvariable=self.modelo_var).pack()

        tk.Label(self, text="Color:").pack()
        tk.Entry(self, textvariable=self.color_var).pack()

        # Botón de registro
        tk.Button(self, text="Registrar vehículo", command=self.registrar_vehiculo).pack(pady=5)

        # Lista de vehículos
        tk.Label(self, text="Vehículos registrados:", font=("Arial", 12)).pack(pady=10)
        self.mostrar_vehiculos()

        self.crear_boton_volver()

    def mostrar_vehiculos(self):
        """
        Muestra la lista de vehículos registrados del usuario.
        
        Este método:
        1. Obtiene la lista de vehículos del usuario
        2. Crea un frame para cada vehículo
        3. Muestra la información de cada vehículo
        4. Agrega botón de eliminación para cada vehículo
        """
        for vehiculo in self.usuario.get("vehiculos", []):
            frame = tk.Frame(self)
            frame.pack(pady=5, padx=10, fill=tk.X)

            info = f"{vehiculo['placa']} - {vehiculo['marca']} {vehiculo['modelo']} ({vehiculo['color']})"
            tk.Label(frame, text=info).pack(side=tk.LEFT)

            tk.Button(
                frame,
                text="❌",
                command=lambda v=vehiculo: self.eliminar_vehiculo(v)
            ).pack(side=tk.RIGHT)

    def registrar_vehiculo(self):
        """
        Registra un nuevo vehículo para el usuario.
        
        Este método:
        1. Valida los datos ingresados
        2. Verifica que la placa no esté duplicada
        3. Agrega el vehículo a la lista del usuario
        4. Actualiza la interfaz
        5. Muestra mensajes de éxito o error
        """
        # Obtener datos
        placa = self.placa_var.get().strip().upper()
        marca = self.marca_var.get().strip()
        modelo = self.modelo_var.get().strip()
        color = self.color_var.get().strip()

        # Validaciones
        if not all([placa, marca, modelo, color]):
            return messagebox.showerror("Error", "Todos los campos son obligatorios.")

        # Verificar placa duplicada
        if any(v["placa"] == placa for v in self.usuario.get("vehiculos", [])):
            return messagebox.showerror("Error", "Esta placa ya está registrada.")

        # Crear vehículo
        vehiculo = {
            "placa": placa,
            "marca": marca,
            "modelo": modelo,
            "color": color
        }

        # Agregar a la lista
        if "vehiculos" not in self.usuario:
            self.usuario["vehiculos"] = []
        self.usuario["vehiculos"].append(vehiculo)

        # Actualizar en la base de datos
        if mu.actualizar_usuario(self.usuario["identificacion"], self.usuario):
            messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")
            self.limpiar_campos()
            self.crear_widgets()  # Actualizar lista
        else:
            messagebox.showerror("Error", "No se pudo registrar el vehículo.")

    def eliminar_vehiculo(self, vehiculo):
        """
        Elimina un vehículo de la lista del usuario.
        
        Args:
            vehiculo (dict): Información del vehículo a eliminar
            
        Este método:
        1. Confirma la eliminación con el usuario
        2. Elimina el vehículo de la lista
        3. Actualiza la base de datos
        4. Actualiza la interfaz
        """
        if messagebox.askyesno("Confirmar", f"¿Eliminar el vehículo {vehiculo['placa']}?"):
            self.usuario["vehiculos"].remove(vehiculo)
            if mu.actualizar_usuario(self.usuario["identificacion"], self.usuario):
                messagebox.showinfo("Éxito", "Vehículo eliminado correctamente.")
                self.crear_widgets()  # Actualizar lista
            else:
                messagebox.showerror("Error", "No se pudo eliminar el vehículo.")

    def limpiar_campos(self):
        """
        Limpia los campos de entrada del formulario.
        """
        self.placa_var.set("")
        self.marca_var.set("")
        self.modelo_var.set("")
        self.color_var.set("")
