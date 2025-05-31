import tkinter as tk
from tkinter import messagebox
import modulo_usuarios as mu
import modulo_utiles as utiles
from frames.base_frame import BaseFrame
from frames.registro_vehiculos_frame import RegistroVehiculosFrame

class RegistroFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Registro de Usuario", font=("Arial", 14)).pack(pady=10)

        campos = [
            ("Identificación (1-25)", "identificacion"),
            ("Contraseña (8-16)", "contrasena", True),
            ("Nombre (2-20)", "nombre"),
            ("Apellidos (1-40)", "apellidos"),
            ("Teléfono (8 dígitos)", "telefono"),
            ("Correo electrónico", "correo"),
            ("Dirección física (5-60)", "direccion"),
            ("Tarjeta de crédito/débito (16 dígitos)", "tarjeta_numero"),
            ("Fecha vencimiento (MM/AA)", "tarjeta_vencimiento"),
            ("Código validación (3 dígitos)", "tarjeta_codigo"),
        ]

        self.entradas = {}
        for label, key, *es_contra in campos:
            tk.Label(self, text=label).pack()
            entry = tk.Entry(self, show="*" if es_contra else "")
            entry.pack()
            self.entradas[key] = entry

        tk.Button(self, text="Registrarse", command=self.registrar).pack(pady=10)
        self.crear_boton_volver()

    def registrar(self):
        datos = {k: e.get().strip() for k, e in self.entradas.items()}

        if not (1 <= len(datos["identificacion"]) <= 25):
            return messagebox.showerror("Error", "Identificación inválida.")

        if not utiles.validar_contrasena(datos["contrasena"]):
            return messagebox.showerror("Error", "Contraseña no válida. Debe tener mayúscula, minúscula, número y símbolo.")

        if not (2 <= len(datos["nombre"]) <= 20):
            return messagebox.showerror("Error", "Nombre inválido.")

        if not (1 <= len(datos["apellidos"]) <= 40):
            return messagebox.showerror("Error", "Apellidos inválidos.")

        if not utiles.validar_telefono(datos["telefono"]):
            return messagebox.showerror("Error", "Teléfono inválido.")

        if not utiles.validar_correo(datos["correo"]):
            return messagebox.showerror("Error", "Correo inválido.")

        if not (5 <= len(datos["direccion"]) <= 60):
            return messagebox.showerror("Error", "Dirección inválida.")

        if not (datos["tarjeta_numero"].isdigit() and len(datos["tarjeta_numero"]) == 16):
            return messagebox.showerror("Error", "Número de tarjeta inválido.")

        if not len(datos["tarjeta_vencimiento"]) == 5 or datos["tarjeta_vencimiento"][2] != "/":
            return messagebox.showerror("Error", "Fecha de vencimiento debe tener formato MM/AA.")

        if not (datos["tarjeta_codigo"].isdigit() and len(datos["tarjeta_codigo"]) == 3):
            return messagebox.showerror("Error", "Código de validación inválido.")

        usuario = {
            "identificacion": datos["identificacion"],
            "contrasena": datos["contrasena"],
            "nombre": datos["nombre"],
            "apellidos": datos["apellidos"],
            "telefono": datos["telefono"],
            "correo": datos["correo"],
            "direccion": datos["direccion"],
            "tarjeta": {
                "numero": datos["tarjeta_numero"],
                "vencimiento": datos["tarjeta_vencimiento"],
                "cvv": datos["tarjeta_codigo"]
            },
            "vehiculos": []
        }

        exito = mu.registrar_usuario_completo(usuario)

        if exito:
            messagebox.showinfo("Registro exitoso", "Ahora puedes registrar tus vehículos.")
            self.master.cambiar_frame(RegistroVehiculosFrame, usuario)
        else:
            messagebox.showerror("Error", "No se pudo registrar. Identificación o tarjeta ya en uso.")
