# src/frames/login_frame.py

import tkinter as tk
from tkinter import messagebox
import modulo_usuarios as mu
from frames.base_frame import BaseFrame

class LoginFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Correo:").pack()
        self.entry_correo = tk.Entry(self)
        self.entry_correo.pack()

        tk.Label(self, text="Contraseña:").pack()
        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.pack()

        tk.Button(self, text="Iniciar sesión", command=self.login).pack(pady=10)
        tk.Button(self, text="Registrarse", command=self.registrarse).pack()
        tk.Button(self, text="Recuperar contraseña", command=self.recuperar).pack(pady=10)

    def login(self):
        correo = self.entry_correo.get()
        contrasena = self.entry_contrasena.get()

        usuario = mu.autenticar_usuario(correo, contrasena)
        if usuario:
            messagebox.showinfo("Bienvenido", f"Hola {usuario['nombre']}")
            from frames.menu_usuario_frame import MenuUsuarioFrame
            self.master.cambiar_frame(MenuUsuarioFrame, usuario)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def registrarse(self):
        correo = self.entry_correo.get()
        contrasena = self.entry_contrasena.get()

        if mu.registrar_usuario(correo, contrasena, "Nuevo Usuario", "0000000000", "ABC123"):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        else:
            messagebox.showerror("Error", "Correo ya registrado")

    def recuperar(self):
        correo = self.entry_correo.get()
        if mu.enviar_recordatorio_contrasena(correo):
            messagebox.showinfo("Enviado", "Correo enviado correctamente")
        else:
            messagebox.showerror("Error", "Correo no encontrado")
