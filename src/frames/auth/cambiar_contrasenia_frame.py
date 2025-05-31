import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_usuarios as mu
import bcrypt

class CambiarContrasenaFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="🔐 Cambiar Contraseña", font=("Arial", 14)).pack(pady=10)

        tk.Label(self, text="Contraseña actual").pack()
        self.entry_actual = tk.Entry(self, show="*")
        self.entry_actual.pack()

        tk.Label(self, text="Nueva contraseña").pack()
        self.entry_nueva = tk.Entry(self, show="*")
        self.entry_nueva.pack()

        tk.Label(self, text="Confirmar nueva contraseña").pack()
        self.entry_confirmar = tk.Entry(self, show="*")
        self.entry_confirmar.pack()

        tk.Button(self, text="Actualizar contraseña", command=self.cambiar_contrasena).pack(pady=10)
        self.crear_boton_volver()

    def cambiar_contrasena(self):
        actual = self.entry_actual.get()
        nueva = self.entry_nueva.get()
        confirmar = self.entry_confirmar.get()

        if nueva != confirmar:
            return messagebox.showerror("Error", "Las contraseñas no coinciden.")

        if not mu.validar_contrasena(nueva):
            return messagebox.showerror("Error", "La nueva contraseña no cumple los requisitos.")

        if not bcrypt.checkpw(actual.encode(), self.usuario["contrasena"].encode()):
            return messagebox.showerror("Error", "La contraseña actual no es correcta.")

        exito = mu.actualizar_contrasena(self.usuario["identificacion"], nueva)

        if exito:
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
            self.master.volver()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la contraseña.")
