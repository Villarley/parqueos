"""
Módulo para la interfaz de registro de nuevos usuarios.

Este módulo implementa la interfaz que permite a nuevos usuarios:
- Registrarse en el sistema
- Ingresar sus datos personales
- Configurar su contraseña
- Registrar su tarjeta de pago

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import messagebox
import modulo_usuarios as mu
import modulo_utiles as utiles
from frames.base_frame import BaseFrame
from frames.registro_vehiculos_frame import RegistroVehiculosFrame

class RegistroFrame(BaseFrame):
    """
    Frame para la interfaz de registro de usuarios.
    
    Esta clase maneja la interfaz gráfica que permite a nuevos usuarios
    registrarse en el sistema, incluyendo la validación de datos y
    el proceso de registro.
    
    Attributes:
        identificacion_var (StringVar): Variable para el campo de identificación
        nombre_var (StringVar): Variable para el campo de nombre
        correo_var (StringVar): Variable para el campo de correo
        contrasena_var (StringVar): Variable para el campo de contraseña
        tarjeta_numero_var (StringVar): Variable para el campo de número de tarjeta
        tarjeta_vencimiento_var (StringVar): Variable para el campo de vencimiento
        tarjeta_cvv_var (StringVar): Variable para el campo de CVV
    """
    
    def __init__(self, master):
        """
        Inicializa el frame de registro.
        
        Args:
            master: Widget padre de este frame
        """
        super().__init__(master)
        self.identificacion_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.tarjeta_numero_var = tk.StringVar()
        self.tarjeta_vencimiento_var = tk.StringVar()
        self.tarjeta_cvv_var = tk.StringVar()
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y mensajes informativos
        - Campos para datos personales
        - Campos para datos de tarjeta
        - Botones de registro y volver
        """
        tk.Label(self, text="📝 Registro de Usuario", font=("Arial", 16)).pack(pady=10)

        # Datos personales
        tk.Label(self, text="Datos Personales", font=("Arial", 12)).pack(pady=5)

        tk.Label(self, text="Identificación:").pack()
        tk.Entry(self, textvariable=self.identificacion_var).pack()

        tk.Label(self, text="Nombre completo:").pack()
        tk.Entry(self, textvariable=self.nombre_var).pack()

        tk.Label(self, text="Correo electrónico:").pack()
        tk.Entry(self, textvariable=self.correo_var).pack()

        tk.Label(self, text="Contraseña:").pack()
        tk.Entry(self, textvariable=self.contrasena_var, show="*").pack()

        # Datos de tarjeta
        tk.Label(self, text="Datos de Tarjeta", font=("Arial", 12)).pack(pady=5)

        tk.Label(self, text="Número de tarjeta:").pack()
        tk.Entry(self, textvariable=self.tarjeta_numero_var).pack()

        tk.Label(self, text="Fecha de vencimiento (MM/AA):").pack()
        tk.Entry(self, textvariable=self.tarjeta_vencimiento_var).pack()

        tk.Label(self, text="CVV:").pack()
        tk.Entry(self, textvariable=self.tarjeta_cvv_var, show="*").pack()

        # Botones
        tk.Button(self, text="Registrarse", command=self.registrar_usuario).pack(pady=5)
        self.crear_boton_volver()

    def registrar_usuario(self):
        """
        Procesa el registro de un nuevo usuario.
        
        Este método:
        1. Obtiene y valida todos los datos ingresados
        2. Verifica que no exista un usuario con la misma identificación
        3. Verifica que no exista un usuario con la misma tarjeta
        4. Registra el usuario en el sistema
        5. Muestra mensajes de éxito o error
        """
        # Obtener datos
        datos = {
            "identificacion": self.identificacion_var.get().strip(),
            "nombre": self.nombre_var.get().strip(),
            "correo": self.correo_var.get().strip(),
            "contrasena": self.contrasena_var.get(),
            "tarjeta": {
                "numero": self.tarjeta_numero_var.get().strip(),
                "vencimiento": self.tarjeta_vencimiento_var.get().strip(),
                "cvv": self.tarjeta_cvv_var.get()
            }
        }

        # Validaciones
        if not all([datos["identificacion"], datos["nombre"], datos["correo"], datos["contrasena"]]):
            return messagebox.showerror("Error", "Todos los campos son obligatorios.")

        if not mu.validar_correo(datos["correo"]):
            return messagebox.showerror("Error", "El correo no tiene formato válido.")

        if not mu.validar_contrasena(datos["contrasena"]):
            return messagebox.showerror(
                "Error",
                "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número."
            )

        # Validar tarjeta
        if not all([datos["tarjeta"]["numero"], datos["tarjeta"]["vencimiento"], datos["tarjeta"]["cvv"]]):
            return messagebox.showerror("Error", "Todos los datos de la tarjeta son obligatorios.")

        # Registrar usuario
        if mu.registrar_usuario_completo(datos):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.volver_al_menu()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario.")
