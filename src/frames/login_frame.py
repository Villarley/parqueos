"""
Módulo para la interfaz de inicio de sesión del sistema de parqueos.

Este módulo implementa la pantalla de login que permite a los usuarios:
- Ingresar sus credenciales (identificación y contraseña)
- Acceder al sistema como usuario regular
- Navegar al registro de nuevos usuarios
- Recuperar su contraseña

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import simpledialog
import string
import random
from tkinter import messagebox
import modulo_usuarios as mu
from frames.base_frame import BaseFrame
from frames.registro_frame import RegistroFrame

class LoginFrame(BaseFrame):
    """
    Frame para la interfaz de inicio de sesión.
    
    Esta clase maneja la interfaz gráfica que permite a los usuarios
    autenticarse en el sistema. Incluye campos para identificación y
    contraseña, así como opciones para registro y recuperación.
    
    Attributes:
        identificacion_var (StringVar): Variable para el campo de identificación
        contrasena_var (StringVar): Variable para el campo de contraseña
    """
    
    def __init__(self, master):
        """
        Inicializa el frame de login.
        
        Args:
            master: Widget padre de este frame
        """
        super().__init__(master)
        self.identificacion_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y etiquetas
        - Campos de entrada para identificación y contraseña
        - Botones de inicio de sesión, registro y recuperación
        """
        tk.Label(self, text="🔐 Iniciar Sesión", font=("Arial", 16)).pack(pady=10)

        # Campos de entrada
        tk.Label(self, text="Identificación:").pack()
        tk.Entry(self, textvariable=self.identificacion_var).pack()

        tk.Label(self, text="Contraseña:").pack()
        tk.Entry(self, textvariable=self.contrasena_var, show="*").pack()

        # Botones
        tk.Button(self, text="Ingresar", command=self.iniciar_sesion).pack(pady=5)
        tk.Button(self, text="Registrarse", command=self.ir_a_registro).pack(pady=5)
        tk.Button(self, text="¿Olvidó su contraseña?", command=self.recuperar_contrasena).pack(pady=5)

    def iniciar_sesion(self):
        """
        Procesa el intento de inicio de sesión.
        
        Este método:
        1. Obtiene las credenciales ingresadas
        2. Valida que los campos no estén vacíos
        3. Intenta autenticar al usuario
        4. Navega al menú principal si la autenticación es exitosa
        5. Muestra mensajes de error si hay problemas
        """
        identificacion = self.identificacion_var.get().strip()
        contrasena = self.contrasena_var.get()

        if not identificacion or not contrasena:
            return messagebox.showerror("Error", "Por favor complete todos los campos.")

        resultado = mu.autenticar_usuario(identificacion, contrasena)
        if resultado["success"]:
            from frames.menu_usuario_frame import MenuUsuarioFrame
            self.master.cambiar_frame(MenuUsuarioFrame, resultado["usuario"])
        else:
            messagebox.showerror("Error", resultado["mensaje"])

    def ir_a_registro(self):
        """
        Navega a la pantalla de registro de nuevos usuarios.
        """
        self.master.cambiar_frame(RegistroFrame)

    def recuperar_contrasena(self):
        """
        Inicia el proceso de recuperación de contraseña.
        
        Este método:
        1. Solicita la identificación del usuario
        2. Busca el correo asociado
        3. Envía un correo con instrucciones
        4. Muestra mensajes de éxito o error
        """
        identificacion = self.identificacion_var.get().strip()
        if not identificacion:
            return messagebox.showerror("Error", "Ingrese su identificación.")

        usuario = mu.consultar_usuario(identificacion)
        if not usuario:
            return messagebox.showerror("Error", "Usuario no encontrado.")

        if mu.enviar_recordatorio_contrasena(usuario["correo"]):
            messagebox.showinfo("Éxito", "Se han enviado instrucciones a su correo.")
        else:
            messagebox.showerror("Error", "No se pudo enviar el correo de recuperación.")

    def recuperar(self):
        correo = simpledialog.askstring("Recuperar contraseña", "Ingresa tu correo registrado")
        if not correo:
            return

        clave_temporal = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=10))
        exito = mu.establecer_clave_temporal(correo, clave_temporal)

        if exito:
            messagebox.showinfo("Enviado", "Se ha enviado una contraseña temporal a tu correo.")
        else:
            messagebox.showerror("Error", "Correo no encontrado o inválido.")
