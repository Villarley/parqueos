import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_usuarios as mu

class PerfilUsuarioFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.vehiculos_var = tk.StringVar()
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="👤 Mi Perfil", font=("Arial", 16)).pack(pady=10)
        self.mostrar_datos_usuario()
        self.mostrar_vehiculos()

        tk.Button(self, text="➕ Agregar vehículo", command=self.agregar_vehiculo).pack(pady=5)
        tk.Button(self, text="❌ Eliminar cuenta", command=self.eliminar_cuenta).pack(pady=5)
        self.crear_boton_volver()

    def mostrar_datos_usuario(self):
        datos = self.usuario
        for campo in ["nombre", "apellidos", "telefono", "correo", "direccion"]:
            tk.Label(self, text=f"{campo.capitalize()}: {datos[campo]}").pack()

    def mostrar_vehiculos(self):
        vehiculos = self.usuario.get("vehiculos", [])
        tk.Label(self, text="🚗 Vehículos:").pack(pady=(10, 0))

        for v in vehiculos:
            info = f"{v['placa']} - {v.get('marca', '')} {v.get('modelo', '')}".strip()
            tk.Label(self, text=info).pack()

    def agregar_vehiculo(self):
        nueva = tk.simpledialog.askstring("Agregar vehículo", "Placa del nuevo vehículo:")
        if not nueva:
            return
        if any(v["placa"] == nueva for v in self.usuario.get("vehiculos", [])):
            return messagebox.showerror("Error", "Esa placa ya está registrada.")

        nuevo_vehiculo = {"placa": nueva, "marca": "", "modelo": ""}
        self.usuario.setdefault("vehiculos", []).append(nuevo_vehiculo)

        mu.actualizar_usuario(self.usuario["identificacion"], self.usuario)
        messagebox.showinfo("Éxito", "Vehículo agregado.")
        self.master.cambiar_frame(PerfilUsuarioFrame, self.usuario)  # recargar

    def eliminar_cuenta(self):
        confirmar = messagebox.askyesno("Eliminar cuenta", "¿Seguro que deseas eliminar tu cuenta?")
        if confirmar:
            if mu.eliminar_usuario(self.usuario["identificacion"]):
                messagebox.showinfo("Cuenta eliminada", "Tu cuenta ha sido eliminada.")
                from frames.login_frame import LoginFrame
                self.master.cambiar_frame(LoginFrame)
            else:
                messagebox.showerror("Error", "No se pudo eliminar la cuenta.")
