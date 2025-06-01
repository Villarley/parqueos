"""
Módulo que implementa la interfaz gráfica para el proceso de alquiler de espacios de parqueo.
Este módulo permite a los usuarios seleccionar un espacio, vehículo y duración para alquilar un parqueo.
"""

import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_parqueo as mp
import modulo_usuarios as mu

class AlquilarFrame(BaseFrame):
    """
    Frame para la interfaz de alquiler de espacios de parqueo.
    
    Esta clase maneja la interfaz gráfica que permite a los usuarios:
    - Seleccionar un espacio de parqueo por su ID
    - Elegir un vehículo de su lista de vehículos registrados
    - Especificar la duración del alquiler
    - Confirmar el alquiler del espacio
    
    Attributes:
        usuario (dict): Diccionario con la información del usuario actual
        placa_var (StringVar): Variable para almacenar la placa del vehículo seleccionado
        espacio_var (StringVar): Variable para almacenar el ID del espacio seleccionado
        duracion_var (StringVar): Variable para almacenar la duración del alquiler
    """
    
    def __init__(self, master, usuario):
        """
        Inicializa el frame de alquiler.
        
        Args:
            master: Widget padre de este frame
            usuario (dict): Información del usuario actual
        """
        super().__init__(master, usuario)
        self.usuario = usuario
        self.placa_var = tk.StringVar()
        self.espacio_var = tk.StringVar()
        self.duracion_var = tk.StringVar()
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Etiquetas y campos de entrada para el ID del espacio
        - Menú desplegable para seleccionar el vehículo
        - Campo para ingresar la duración del alquiler
        - Botones de confirmación y retorno
        """
        tk.Label(self, text="🅿️ Alquilar espacio", font=("Arial", 16)).pack(pady=10)

        # Entrada manual de ID
        tk.Label(self, text="ID del espacio de parqueo:").pack()
        tk.Entry(self, textvariable=self.espacio_var).pack()

        # Vehículos disponibles
        placas = [v["placa"] for v in self.usuario.get("vehiculos", [])]
        if not placas:
            tk.Label(self, text="No tienes vehículos registrados.").pack()
            self.crear_boton_volver()
            return

        tk.Label(self, text="Placa del vehículo:").pack()
        self.placa_var.set(placas[0])
        tk.OptionMenu(self, self.placa_var, *placas).pack()

        # Duración
        tk.Label(self, text="Duración (minutos):").pack()
        tk.Entry(self, textvariable=self.duracion_var).pack()

        tk.Button(self, text="✅ Confirmar alquiler", command=self.confirmar_alquiler).pack(pady=10)
        self.crear_boton_volver()

    def confirmar_alquiler(self):
        """
        Procesa la solicitud de alquiler de un espacio.
        
        Este método:
        1. Valida los datos ingresados (espacio, duración, placa)
        2. Verifica el estado del espacio seleccionado
        3. Intenta realizar el alquiler
        4. Muestra mensajes de éxito o error según corresponda
        
        Validaciones realizadas:
        - El ID del espacio no debe estar vacío
        - La duración debe ser un número entero positivo
        - La placa debe estar seleccionada
        - El espacio debe existir en el sistema
        """
        espacio_id = self.espacio_var.get().strip().upper()
        try:
            duracion = int(self.duracion_var.get())
        except ValueError:
            return messagebox.showerror("Error", "La duración debe ser un número entero.")
            
        placa = self.placa_var.get()

        # Validaciones de datos ingresados
        if not espacio_id:
            return messagebox.showerror("Error", "Debe ingresar un ID de espacio.")
        if duracion < 1:
            return messagebox.showerror("Error", "La duración mínima debe ser de 1 minuto.")
        if not placa:
            return messagebox.showerror("Error", "Debe seleccionar una placa.")

        # Validación del estado del espacio
        estado = mp.verificar_estado_espacio(espacio_id)
        if estado == "no_existe":
            return messagebox.showerror("Error", f"El espacio {espacio_id} no existe.")
        elif estado != "libre":
            continuar = messagebox.askyesno(
                "Espacio ocupado",
                f"El espacio {espacio_id} no está libre (estado: {estado}). ¿Deseas continuar de todos modos?"
            )
            if not continuar:
                return

        # Intento de alquiler del espacio
        exito = mp.alquilar_espacio(
            correo_usuario=self.usuario["correo"],
            id_espacio=espacio_id,
            minutos=duracion,
            placa=placa
        )

        if exito:
            messagebox.showinfo("Éxito", f"Espacio {espacio_id} alquilado por {duracion} minutos.")
            self.volver_al_menu()
        else:
            messagebox.showerror("Error", "No se pudo alquilar el espacio.")
