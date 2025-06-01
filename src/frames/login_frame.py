import tkinter as tk
from tkinter import simpledialog
import string
import random
from tkinter import messagebox
import modulo_usuarios as mu
from frames.base_frame import BaseFrame
from frames.registro_frame import RegistroFrame

class LoginFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Identificación:").pack()
        self.entry_identificacion = tk.Entry(self)
        self.entry_identificacion.pack()

        tk.Label(self, text="Contraseña:").pack()
        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.pack()

        tk.Button(self, text="Iniciar sesión", command=self.login).pack(pady=10)
        tk.Button(self, text="Registrarse", command=lambda: self.master.cambiar_frame(RegistroFrame)).pack()
        tk.Button(self, text="Recuperar contraseña", command=self.recuperar).pack(pady=10)

    def login(self):
        identificacion = self.entry_identificacion.get()
        contrasena = self.entry_contrasena.get()

        resultado = mu.autenticar_usuario(identificacion, contrasena)
        if resultado["success"]:
            usuario = resultado["usuario"]
            if usuario.get("temporal"):  # Tiene contraseña temporal
                messagebox.showinfo("Contraseña temporal", "Debes cambiar tu contraseña ahora.")
                from frames.auth.cambiar_contrasenia_frame import CambiarContrasenaFrame
                self.master.cambiar_frame(CambiarContrasenaFrame, usuario)
                return

            messagebox.showinfo("Bienvenido", f"Hola {usuario['nombre']}")
            from frames.menu_usuario_frame import MenuUsuarioFrame
            self.master.cambiar_frame(MenuUsuarioFrame, usuario)
        else:
            messagebox.showerror("Error", resultado["mensaje"])

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
